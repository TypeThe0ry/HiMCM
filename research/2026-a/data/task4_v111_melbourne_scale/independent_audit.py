"""Independent raw Melbourne endpoint calculation and NYC archive identity audit."""
import hashlib,importlib.util,json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
P=Path(__file__).resolve().parent;DATA=P.parent;ROOT=DATA.parent
s=json.loads((P/'summary.json').read_text());hashes={}
for row in s['sources']:
 p=ROOT/row['path'];h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==row['sha256'];hashes[row['path']]=h
p=pd.read_csv(DATA/'task4_school_commute_extra/person_vista_2024_2025.csv')
j=pd.read_csv(DATA/'task4_school_commute_extra/journey_to_education_vista_2024_2025.csv')
st=pd.read_csv(DATA/'task4_v44_melbourne/stops_vista_2024_2025.csv',usecols=['stopid','hhid','persid','destplace2'])
p=p.loc[p.studying.eq('Secondary')&p.homeregion_ASGS.eq('Greater Melbourne')&p.dayType.eq('Weekday')&p.agegroup.eq('15->19')].copy();assert len(p)==171 and p.persid.is_unique
j=j.merge(p[['hhid','persid']],on=['hhid','persid'],validate='many_to_one');assert j.start_loc.eq('FROM_HOME').all() and j.end_loc.eq('TO_EDUCATION').all()
np.testing.assert_allclose(j.end_time-j.start_time,j.journey_elapsed_time)
j=j.merge(st,left_on=['end_stopid','hhid','persid'],right_on=['stopid','hhid','persid'],validate='many_to_one',how='left');j=j.sort_values(['persid','start_time','jteid']).groupby('persid',sort=False).head(1)
p=p.merge(j[['persid','destplace2','journey_elapsed_time']],on='persid',how='left',validate='one_to_one')
cols=['perspoststratweight']+['perspoststratweight_GROUP_'+str(k) for k in range(1,11)];w=p[cols].to_numpy();complete=np.isfinite(w).all(1)&(w[:,0]>0)&(w[:,1:]>=0).all(1)
assert complete.sum()==170;assert s['melbourne_scope']['strict_full_target_interval']==[0,1] and s['melbourne_scope']['unbounded_missing_weight_persons']==1
p=p[complete];w=w[complete].astype(np.longdouble);d=p.journey_elapsed_time.to_numpy();valid=np.isfinite(d)&(d>=0)&p.destplace2.eq('Secondary School').to_numpy();assert valid.sum()==100 and p.journey_elapsed_time.isna().sum()==63
errors=[]
for row in s['melbourne_scenarios']:
 tau=row['tau_minutes'];values=np.exp(-np.where(valid,d,0).astype(np.longdouble)/tau);x=np.stack([np.where(valid,values,0),np.where(valid,values,1)])
 means=x@w/w.sum(0);se=np.sqrt(np.longdouble('.9')*((means[:,1:]-means[:,[0]])**2).sum(1));ci=[max(0,means[0,0]-t.ppf(.975,9)*se[0]),min(1,means[1,0]+t.ppf(.975,9)*se[1])]
 for a,b in [(means[:,0],[row['utility_lower'],row['utility_upper']]),(means[:,1:],row['endpoint_replicates']),(se,row['endpoint_se']),(ci,[row['sampling_lower'],row['sampling_upper']])]:
  err=float(np.max(abs(np.array(a)-np.array(b))));assert err<1e-13;errors.append(err)
 scenario=next(r for r in s['scenarios'] if r['city']=='Melbourne' and r['tau_minutes']==tau);np.testing.assert_allclose(ci,[scenario['utility_lower'],scenario['utility_upper']],rtol=0,atol=1e-13)
v26=DATA/'task4_v26_nyc_tau';ny=json.loads((v26/'summary.json').read_text())
for row in ny['sources']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
spec=importlib.util.spec_from_file_location('historical_nyc_rebuild',v26/'extract_tau.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);persons,households,_=mod.reproduce_roster()
assert len(persons)==603 and len(households)==5766 and persons.duration_minutes.notna().sum()==410
for row in s['scenarios']:
 if row['city']=='New York':
  original=next(r for r in ny['scenarios'] if r['age_scope']=='under19' and r['tau_minutes']==row['tau_minutes']);assert original['known_students']==460 and original['optional_students']==33
  assert [row['utility_lower'],row['utility_upper'],row['point_lower'],row['point_upper']]==[original[k] for k in ['sampling_lower','sampling_upper','utility_lower','utility_upper']]
current=pd.read_csv(ROOT/'results/task4_v108_intake/utility_bounds.csv')
for city in ['Melbourne','New York']:
 row=next(r for r in s['scenarios'] if r['city']==city and r['tau_minutes']==30);base=current[(current.city==city)&(current.indicator=='travel')].iloc[0]
 np.testing.assert_allclose([row['utility_lower'],row['utility_upper']],[base.lower,base.upper],rtol=0,atol=1e-14)
assert len(s['scenarios'])==10
result=dict(status='passed',summary_sha256=hashlib.sha256((P/'summary.json').read_bytes()).hexdigest(),script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),ten_scenarios_checked=True,tau30_current_v108_verified=True,melbourne_independent_longdouble_max_error=max(errors),melbourne_full_target_unidentified=True,melbourne_conditional_complete_weight_target=170,melbourne_verified_durations=100,melbourne_unknown_utilities=70,nyc_source_hashes_verified=True,nyc_raw_roster_rebuilt=True,nyc_bootstrap_rerun=False,source_hashes=hashes,limitations=['Melbourne scenario is conditional on complete weights; the171-person full target remains[0,1].','Melbourne age15-19 and Greater Melbourne are not exact14-18/municipality.','NYC reuse is warranted by unchanged archived source hashes and reconstructed roster, not a new bootstrap validation. Historical2010-11/fixed-weight bootstrap qualifications remain.','Discrete per-scale envelopes, not simultaneous inference or interpolation guarantee.'])
(P/'independent_audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Independent check passed; maximum Melbourne error',max(errors))
