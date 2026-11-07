"""Extract official London sixth-form pupils and containing workforce estimate."""
import gzip,hashlib,json,io
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parent
for m in json.loads((ROOT/'manifest.json').read_text()):
    z=(ROOT/m['file']).read_bytes();assert len(z)==m['bytes'] and hashlib.sha256(z).hexdigest()==m['sha256']
    if m['file'].endswith('.gz'):
        b=gzip.decompress(z);assert len(b)==m['uncompressed_bytes'] and hashlib.sha256(b).hexdigest()==m['uncompressed_sha256']
w=pd.read_csv(ROOT/'workforce.csv.gz',low_memory=False)
p=pd.read_csv(ROOT/'pupils.csv.gz',low_memory=False)
wr=w[(w.time_period==202425)&(w.geographic_level=='Regional')&(w.region_name.isin(['Inner London','Outer London']))&(w.school_type=='State-funded secondary')]
pr=p[(p.time_period==202425)&(p.geographic_level=='Regional')&(p.region_name=='London')&(p.phase_type_grouping=='State-funded secondary')&(p.sex=='Total')&(p.ncyear.isin(['Year 12','Year 13']))]
assert len(wr)==2 and len(pr)==2
s=pd.to_numeric(pr.headcount).sum();t=pd.to_numeric(wr.hc_all_teachers).sum();fte=pd.to_numeric(wr.fte_all_teachers).sum()
assert s==106046 and abs(t-38178.63636)<1e-8
for year in ['Year 12','Year 13']:
    subset=p[(p.time_period==202425)&(p.geographic_level=='Regional')&(p.region_name=='London')&(p.phase_type_grouping=='State-funded secondary')&(p.ncyear==year)]
    assert subset[subset.sex.isin(['Male','Female'])].headcount.sum()==subset[subset.sex=='Total'].headcount.iloc[0]
r=dict(city='London',year='2024/25',pupil_census='January 2025',workforce_census='November 2024',year12_pupils=56499,year13_pupils=49547,students=int(s),secondary_teacher_headcount_estimate=float(t),secondary_teacher_fte_estimate=float(fte),conditional_ptr_lower=float(s/t),conditional_utility_upper=float(15/(15+s/t)),utility_lower=0,main_admitted=False,requires='Treat published workforce estimate as a containing teacher total for the later pupil census; state-funded secondary school sector only, excludes independent and FE colleges. Sixth-form teacher allocation unknown. No bound on workforce estimation error established. Workforce excludes some former FE sixth-form colleges now academies and groups multi-contract teachers by main contract; containment across pupil/workforce populations is unverified.',pupil_rows=pr[['ncyear','headcount','full_time','part_time']].to_dict('records'),teacher_rows=wr[['region_name','hc_all_teachers','fte_all_teachers']].to_dict('records'))
(ROOT/'observation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
