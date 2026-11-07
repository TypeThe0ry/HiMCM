"""Check mirrored Parquet core fields against archived University Chile CSVs."""
import io,json,tarfile,hashlib
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent

def main():
    checks=[]
    with tarfile.open(P/'eod2012.tgz') as t:
        for label,filename,key,fields in [
            ('hogares','Hogares.csv','Hogar',['Comuna','TipoDia','Temporada','Zona']),
            ('personas','personas.csv','Persona',['Hogar','Estudios','Curso','Actividad','DondeEstudia','Factor_LaboralNormal']),
            ('viajes','viajes.csv','Viaje',['Hogar','Persona','Proposito','HoraIni','HoraFin','TiempoViaje','FactorLaboralNormal'])]:
            raw=pd.read_csv(io.BytesIO(t.extractfile('eod2012/EOD_STGO/'+filename).read()),sep=';',decimal=',',encoding='utf-8-sig',low_memory=False)
            converted=pd.read_parquet(P/(label+'.parquet'))
            assert raw[key].is_unique and converted[key].is_unique
            raw=raw.set_index(key).sort_index();converted=converted.set_index(key).sort_index()
            assert raw.index.equals(converted.index)
            for col in fields:
                a=raw[col];b=converted[col]
                if pd.api.types.is_numeric_dtype(a) and pd.api.types.is_numeric_dtype(b):ok=np.allclose(a.to_numpy(float),b.to_numpy(float),equal_nan=True)
                else:ok=a.fillna('').astype(str).equals(b.fillna('').astype(str))
                assert ok,(label,col)
                checks.append(dict(table=label,field=col,rows=len(raw),equal=True))
    people=pd.read_parquet(P/'personas.parquet');homes=pd.read_parquet(P/'hogares.parquet')
    joined=people.merge(homes[['Hogar','Comuna']],on='Hogar',validate='many_to_one')
    candidate=joined[joined.Actividad.fillna('').str.split(';').apply(lambda x:'B' in x)&joined.DondeEstudia.eq(4)&joined.Estudios.isin([5,7])]
    summary=dict(core_field_checks=checks,university_archive_sha256=hashlib.sha256((P/'eod2012.tgz').read_bytes()).hexdigest(),candidate_metro=len(candidate),candidate_santiago_comuna=int(candidate.Comuna.eq('SANTIAGO').sum()),candidate_definition='Actividad includes B, DondeEstudia=4, Estudios in {5,7}; provisional classification, not verified current high-school cohort',main_admission=False)
    (P/'raw_verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps({k:v for k,v in summary.items() if k!='core_field_checks'},indent=2))
if __name__=='__main__':main()
