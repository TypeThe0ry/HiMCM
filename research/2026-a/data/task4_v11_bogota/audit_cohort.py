"""Audit historical school cohort without equating attainment with current grade."""
from pathlib import Path
import gzip,hashlib,json,io
import pandas as pd
P=Path(__file__).resolve().parent

def main():
    tables={}
    for r in json.loads((P/'manifest.json').read_text())['files']:
        raw=(P/r['archived_name']).read_bytes()
        if r['archived_name'].endswith('.gz'):raw=gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest()==r['sha256']
        if r['original_name'].endswith('.csv'):
            tables[r['original_name']]=pd.read_csv(io.BytesIO(raw),sep=';',dtype=str,encoding='utf-8-sig')
    h=tables['HogaresEODH2019.csv'].rename(columns={'Id_Hogar':'id_hogar'})
    p=tables['PersonasEODH2019.csv'];v=tables['ViajesEODH2019.csv'];a=tables['Aux_DuraciónEODH2019.csv']
    assert h.id_hogar.is_unique and not p.duplicated(['id_hogar','id_persona']).any()
    p=p.merge(h[['id_hogar','municipio']],on='id_hogar',how='left',validate='many_to_one',indicator=True)
    assert p['_merge'].eq('both').all()
    occupation=['p6_id_ocupacion','p6_id_ocupacion_O1','p6_id_ocupacion_O2','p6_id_ocupacion_O3']
    school=p[occupation].apply(pd.to_numeric,errors='coerce').eq(1).any(axis=1)
    city=pd.to_numeric(p.municipio,errors='coerce').eq(11001)
    result={'rows':{k:len(f) for k,f in tables.items()},'bogota_people':int(city.sum()),'current_school_students_metro':int(school.sum()),'current_school_students_bogota':int((school&city).sum()),'bogota_school_students_by_attainment':p.loc[school&city,'p5_id_nivel_educativo'].fillna('missing').value_counts().sort_index().to_dict(),'trips_duplicate_keys':int(v.duplicated(['id_hogar','id_persona','id_viaje']).sum()),'duration_duplicate_keys':int(a.duplicated(['id_hogar','id_persona','id_viaje']).sum()),'main_admitted':False,'unresolved':'School occupation is observed, current upper-secondary grade is not. p5 is maximum educational attainment. Historical 2019 mirror provenance.'}
    (P/'cohort_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
