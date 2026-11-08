#!/usr/bin/env python3
"""Stage-harmonized city PISA outcomes; no automatic main-model admission."""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
REPS=[f'W_FSTURWT{i}' for i in range(1,81)]
THRESHOLD=420.07

def combine(p,r):
 sampling=float(np.mean(4/80*np.sum((r-p[:,None])**2,axis=1)))
 between=float(np.var(p,ddof=1));v=sampling+1.1*between
 return dict(mean=float(p.mean()),standard_error=float(np.sqrt(v)),sampling_variance=sampling,between_pv_variance=between,total_variance=v,normal_95_lower=float(p.mean()-1.96*np.sqrt(v)),normal_95_upper=float(p.mean()+1.96*np.sqrt(v)))

def estimates(d,subject,threshold=None):
 pv=d[[f'PV{i}{subject}' for i in range(1,11)]].to_numpy(float)
 assert np.isfinite(pv).all(), 'Nonfinite plausible value'
 if threshold is not None:pv=(pv>=threshold).astype(float)
 w=d.W_FSTUWT.to_numpy(float);rw=d[REPS].to_numpy(float)
 assert np.isfinite(pv).all() and np.isfinite(w).all() and np.isfinite(rw).all()
 assert (w>0).all() and (rw>=0).all() and (rw.sum(axis=0)>0).all()
 return np.sum(pv*w[:,None],axis=0)/w.sum(),pv.T@rw/rw.sum(axis=0)

def main():
 for filename,source in json.loads((HERE/'sources_manifest.json').read_text()).items():
  assert hashlib.sha256((HERE/filename).read_bytes()).hexdigest()==source['sha256'], 'Threshold source checksum mismatch'
 manifest=json.loads((HERE/'manifest.json').read_text());p=HERE/manifest['derived_file']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==manifest['derived_sha256']
 assert hashlib.sha256((HERE.parent/'task4_v86_bogota/manifest.json').read_bytes()).hexdigest()==manifest['baseline_manifest_sha256']
 d=pd.read_csv(p);assert len(d)==manifest['rows']
 rows=[];domains=[];cross=[];rep_rows=[]
 for city,group in d.groupby('city',sort=True):
  assert group.ISCEDP.notna().all()
  hs=group.ISCEDP.ge(300)&group.ISCEDP.lt(400)
  grade=group.ST001D01T.ge(10)&group.ST001D01T.le(13)
  for (isc,gr),n in group.groupby(['ISCEDP','ST001D01T'],dropna=False).size().items():cross.append(dict(city=city,iscedp=isc,grade=gr,n=int(n)))
  if city=='Bogota':assert np.array_equal(hs,grade)
  masks={'all_pisa':np.ones(len(group),dtype=bool),'isced3':hs,'grade_ge10':grade}
  for domain,mask in masks.items():
   sub=group.loc[mask]
   assert len(sub)>0
   domains.append(dict(city=city,domain=domain,n=len(sub),schools=int(sub.CNTSCHID.nunique()),weighted_population=float(sub.W_FSTUWT.sum()),weighted_share=float(sub.W_FSTUWT.sum()/group.W_FSTUWT.sum()),age_min=float(sub.AGE.min()),age_max=float(sub.AGE.max()),age_missing=int(sub.AGE.isna().sum()),grade_rule_disagreement_n=int((hs!=grade).sum())))
   for subject,metric,threshold in [('MATH','math_mean',None),('READ','reading_mean',None),('SCIE','science_mean',None),('MATH','math_level2_fraction',THRESHOLD)]:
    point,rep=estimates(sub,subject,threshold);row=dict(city=city,domain=domain,metric=metric,**combine(point,rep));rows.append(row)
    for m in range(10):rep_rows.append(dict(city=city,domain=domain,metric=metric,pv=m+1,estimate=point[m],**{f'replicate_{k+1}':rep[m,k] for k in range(80)}))
 # V86 Bogota group reproduction is checked against already-hashed subset rather than a mutable results file.
 old=pd.read_csv(HERE.parent/'task4_v86_bogota/bogota_pisa2022_selected.csv.gz')
 expected=json.loads((HERE.parent/'task4_v86_bogota/manifest.json').read_text())
 assert hashlib.sha256((HERE.parent/'task4_v86_bogota'/expected['derived_file']).read_bytes()).hexdigest()==expected['derived_sha256']
 assert set(old.CNTSTUID)==set(d[d.city.eq('Bogota')].CNTSTUID)
 for s,metric in [('MATH','math_mean'),('READ','reading_mean'),('SCIE','science_mean')]:
  a,b=estimates(old[old.ST001D01T.isin([10,11])],s);match=next(r for r in rows if r['city']=='Bogota' and r['domain']=='isced3' and r['metric']==metric)
  assert abs(match['mean']-combine(a,b)['mean'])<1e-10
 assert abs(next(r['mean'] for r in rows if r['city']=='Bogota' and r['domain']=='all_pisa' and r['metric']=='math_level2_fraction')-0.48192695594)<1e-9
 for name,items in [('outcomes.csv',rows),('domains.csv',domains),('stage_grade_crosstab.csv',cross),('pv_replicate_estimates.csv',rep_rows)]:pd.DataFrame(items).to_csv(HERE/name,index=False)
 summary={'main_admitted':False,'population':'PISA2022 age-cohort students in identified school regions; current programme ISCED3; not all 14–18-year-old residents','mathematics_level2_threshold':THRESHOLD,'threshold_source':'https://nces.ed.gov/surveys/pisa/pisa2022/technical-notes/index.asp','variance':'Mean of ten Fay-BRR sampling variances (4/80), plus1.1 times sample variance across ten PV estimates','intervals':'Individual approximate normal95%; no simultaneous coverage claimed; proficiency limits not clipped in output','domains':domains,'outcomes':rows}
 (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(pd.DataFrame(rows).query("metric=='math_level2_fraction'")[['city','domain','mean','standard_error']].to_string(index=False))
if __name__=='__main__':main()
