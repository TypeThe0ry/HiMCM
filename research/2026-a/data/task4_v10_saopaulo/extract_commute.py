"""Observed OD2023 high-school cohort; mirror provenance keeps admission conditional."""
from pathlib import Path
import gzip, hashlib, json, tempfile, math
from collections import defaultdict, Counter
from dbfread import DBF
P=Path(__file__).resolve().parent

def person_bound(rows):
    school=[r for r in rows if r['MOTIVO_D']==4]
    if not school:return 0.,1.,'no_school_journey'
    if any(r['N_VIAG'] is None or r['N_VIAG']<=0 for r in school):return 0.,1.,'unknown_order'
    first=min(r['N_VIAG'] for r in school); selected=[r for r in school if r['N_VIAG']==first]
    if len(selected)!=1:return 0.,1.,'ambiguous_order'
    r=selected[0]
    if r['MOTIVO_O']!=8:return 0.,1.,'first_school_journey_not_from_home'
    clocks=[r[k] for k in ['H_SAIDA','MIN_SAIDA','H_CHEG','MIN_CHEG']]
    if any(v is None for v in clocks):return 0.,1.,'missing_clock'
    h,m,hh,mm=clocks
    if not (0<=h<24 and 0<=hh<24 and 0<=m<60 and 0<=mm<60):return 0.,1.,'invalid_clock'
    dt=(60*hh+mm-60*h-m)%1440;t=r['DURACAO']
    if t is None or t<=0 or t!=dt:return 0.,1.,'duration_clock_mismatch'
    if r['DIA_SEM'] not in [2,3,4,5,6]:return 0.,1.,'weekday_unverified'
    u=math.exp(-t/30)
    return u,u,'observed_direct_journey'

def main():
    manifest=json.loads((P/'microdata_manifest.json').read_text())
    raw=gzip.decompress((P/'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==manifest['files'][0]['sha256']
    for entry in manifest['files'][1:]:
        file=P/Path(entry['path']).name
        assert hashlib.sha256(file.read_bytes()).hexdigest()==entry['sha256']
    mapping=list(DBF(str(P/'Municipios_2023.dbf'),encoding='latin1'))
    assert any(r['NumeroMuni']==36 and str(r['CD_IBGE'])=='3550308' for r in mapping)
    people=defaultdict(list);total=0
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'data.dbf';f.write_bytes(raw)
        for r in DBF(str(f),encoding='latin1'):
            total+=1
            if r['ESTUDA']==4:people[r['ID_PESS']].append(r)
    records=[]
    for pid,rows in people.items():
        for key in ['MUNI_DOM','ESTUDA','FE_PESS','DATA']:
            assert len({r[key] for r in rows})==1,(pid,key)
        assert sum(r['F_PESS']==1 for r in rows)==1
        w=rows[0]['FE_PESS'];assert w is not None and math.isfinite(w) and w>0
        l,h,status=person_bound(rows)
        records.append(dict(municipality=rows[0]['MUNI_DOM'],weight=w,lower=l,upper=h,status=status))
    result={'raw_rows':total,'cohort_definition':'ESTUDA=4, current upper-secondary enrolment; no age proxy','main_admitted':False,'reason':'public research mirror; official byte identity and city-definition alignment not yet verified','scopes':{}}
    for scope,rows in [('metro',records),('municipality_sao_paulo',[r for r in records if r['municipality']==36])]:
        den=sum(r['weight'] for r in rows)
        result['scopes'][scope]={'students':len(rows),'weighted_students':den,'status_counts':dict(Counter(r['status'] for r in rows)),'utility_lower':sum(r['weight']*r['lower'] for r in rows)/den,'utility_upper':sum(r['weight']*r['upper'] for r in rows)/den}
    (P/'commute_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
