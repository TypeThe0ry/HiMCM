"""Independent public-histogram and explicit order-statistic percentile check.
Does not rerun raw extraction or bootstrap resampling.
"""
import csv,hashlib,json,math
from pathlib import Path
P=Path(__file__).resolve().parent
s=json.loads((P/'summary.json').read_text());a=json.loads((P/'aggregate.json').read_text());reps=json.loads((P/'bootstrap_endpoints.json').read_text());hashes={}
for r in json.loads((P/'manifest.json').read_text()):
 h=hashlib.sha256((P/r['file']).read_bytes()).hexdigest();assert h==r['sha256'];hashes[r['file']]=h
old=json.loads((P.parent/'task4_v48_saopaulo_age/summary.json').read_text());o=old['scopes']['age14_18']
assert a['students']==o['students']==1690 and a['status_counts']==o['status_counts']
hist=a['weighted_duration_histogram'];assert sum(x[0] for x in hist.values())==1690 and hist['unresolved'][0]==201
assert a['all_municipal_households']==old['bootstrap']['all_households_including_zero_eligible']==21917 and a['zones']==329
assert s['bootstrap']['replicates']==2000 and s['bootstrap']['seed']==20261107
# numpy's default quantile equals linear interpolation at (n-1)*q.
def quantile(values,q):
 v=sorted(values);position=(len(v)-1)*q;i=math.floor(position);f=position-i
 return v[i]*(1-f)+v[min(i+1,len(v)-1)]*f
checks=[];den=math.fsum(x[1] for x in hist.values());assert abs(den-o['weighted_students'])<1e-7
for k,tau in enumerate(a['taus']):
 numerator=math.fsum(x[1]*math.exp(-float(duration)/tau) for duration,x in hist.items() if duration!='unresolved');low=numerator/den;high=(numerator+hist['unresolved'][1])/den
 e=reps[str(tau)];assert len(e)==2000 and all(0<=v[0]<=v[1]<=1 for v in e)
 interval=[min(low,quantile([v[0] for v in e],.025)),max(high,quantile([v[1] for v in e],.975))]
 row=next(r for r in s['scenarios'] if r['tau_minutes']==tau);assert row['city']=='Sao Paulo'
 errors=[abs(x-y) for x,y in zip([low,high]+interval,[row['point_lower'],row['point_upper'],row['utility_lower'],row['utility_upper']])];assert max(errors)<1e-12
 totals=a['point_weighted_sums'][3*k:3*k+3];assert max(abs(x-y/totals[2]) for x,y in zip([low,high],totals[:2]))<1e-12
 if tau==30:
  assert max(abs(x-o[key]) for x,key in zip([low,high]+interval,['utility_lower','utility_upper','sampling_lower','sampling_upper']))<1e-12
 checks.append(dict(tau_minutes=tau,point_bounds=[low,high],sampling_envelope=interval,max_error=max(errors)))
with (P.parents[1]/'results/task4_v108_intake/utility_bounds.csv').open() as f:current=next(r for r in csv.DictReader(f) if r['city']=='Sao Paulo' and r['indicator']=='travel')
base=next(r for r in checks if r['tau_minutes']==30);assert max(abs(x-float(current[k])) for x,k in zip(base['sampling_envelope'],['lower','upper']))<1e-12
result=dict(status='passed',method='Independent math.fsum duration-histogram means and explicit sorted linear percentile interpolation; no main derive imports',checks=checks,source_hashes=hashes,summary_sha256=hashlib.sha256((P/'summary.json').read_bytes()).hexdigest(),audit_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),tau30_v48_and_current_v108_verified=True,raw_bootstrap_resampling_independently_verified=False,limitations=['Audit verifies released aggregate moments and bootstrap endpoint percentile calculations, not raw-record extraction or 2000 resampling draws.','Published input raw hash is inherited provenance; no new official byte-identity verification.','Exploratory fixed-weight bootstrap and per-scale intervals, not official design-valid CI or simultaneous band.'])
(P/'independent_audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Five Sao Paulo scenarios independently verified')
