"""Independent long-double scores and continuous endpoint enclosures."""
import csv,hashlib,itertools,json,sys,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
P=Path(__file__).resolve().parent;J=P.parent/'task4_v109_joint_acquisition';D=np.longdouble
s=json.loads((P/'summary.json').read_text());j=json.loads((J/'summary.json').read_text())
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
r=rows(J/'baseline/utility_bounds.csv');cities=list(dict.fromkeys(x['city'] for x in r));names=list(dict.fromkeys(x['indicator'] for x in r))
lo=np.array([D(x['lower']) for x in r]).reshape(25,10);hi=np.array([D(x['upper']) for x in r]).reshape(25,10)
hashv=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()
assert hashv==s['input_bounds_sha256']==j['input_bounds_sha256']
assert hashlib.sha256((J/'summary.json').read_bytes()).hexdigest()==s['source_summary_sha256']
amin,amax=map(lambda x:D(str(x)),s['alpha_range'])
def score(x,a):
 a=D(str(a));w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
 p=np.sqrt((w*x*x).sum(1));n=np.sqrt((w*(1-x)**2).sum(1));return 100*p/(p+n)
def enclose(l,u,keep,outside):
 stack=[(amin,amax,0)];leaves=[]
 while stack:
  a,b,d=stack.pop();ls=np.array([score(l,t)[keep] for t in (a,b)]);us=np.array([score(u,t)[outside] for t in (a,b)])
  gap=ls.min(0).max()-us.max(0).max()-D('2e-9')
  if gap>D('1e-8'):leaves.append(float(gap))
  else:
   assert d<25,'Unresolved continuous enclosure'
   m=(a+b)/2;stack.extend([(a,m,d+1),(m,b,d+1)])
 return dict(leaves=len(leaves),minimum_gap_lower=min(leaves))
def mask_for(ns):
 m=np.zeros_like(lo,bool);m[:,[names.index(n) for n in ns]]=True;return m
cert=rows(J/'unavoidable_certificates.csv');points=rows(J/'hypothetical_exact_values.csv');feas=json.loads((J/'city_feasibility.json').read_text());joint=[]
for case in j['scenarios']:
 name,mode=case['scenario'],case['mode'];m=mask_for(case['measured_indicators']);l=lo.copy();u=hi.copy();anchors=[cities.index(c) for c in case['anchor_cities']]
 if name=='phoenix_education_and_travel':m[np.arange(25)!=cities.index('Phoenix')]=False
 for row in points:
  if (row['scenario'],row['mode'])!=(name,mode):continue
  i,k=cities.index(row['city']),names.index(row['indicator']);v=D(row['hypothetical_exact_value']);assert m[i,k]
  assert abs(v-(hi[i,k] if i in anchors else lo[i,k]))<D('1e-15');l[i,k]=u[i,k]=v
 assert np.all(l[m]==u[m]) and np.array_equal(l[~m],lo[~m]) and np.array_equal(u[~m],hi[~m])
 mandatory=[]
 for row in cert:
  if row['scenario']!=name:continue
  i=int(row['index']);worst=np.where(m,lo,hi);best=np.where(m,hi,lo)
  if mode=='fixed':
   gap=score(worst,j['fixed_alpha'])[i]-np.delete(score(best,j['fixed_alpha']),i).max();assert abs(gap-D(row['worst_fixed_margin']))<D('1e-11')
   assert (gap>=-D('1e-10'))==(row['fixed_unavoidable']=='True')
  if row[mode+'_unavoidable']=='True':
   a=j['fixed_alpha'] if mode=='fixed' else float(row['witness_alpha']);gap=score(worst,a)[i]-np.delete(score(best,a),i).max();assert gap>=-D('1e-10');mandatory.append(cities[i])
  elif mode=='continuous':enclose(best,worst,[k for k in range(25) if k!=i],[i])
 assert mandatory==case['unavoidable_cities']
 survivors=[]
 for row in feas:
  if (row['scenario'],row['mode'])!=(name,mode):continue
  i=row['index'];others=[k for k in range(25) if k!=i]
  if row['possible']:
   a=row['witness_alpha'];assert amin<=D(str(a))<=amax
   assert score(u,a)[i]-score(l,a)[others].max()>=-D('1e-10');survivors.append(cities[i])
  elif mode=='fixed':assert score(u,j['fixed_alpha'])[i]-score(l,j['fixed_alpha'])[others].max()<-D('1e-10')
  else:enclose(l,u,others,[i])
 assert survivors==case['surviving_cities'];assert len(survivors)==case['attained_count_upper_bound']
 assert max(1,len(mandatory))==case['universal_count_lower_bound']
 assert case['joint_minimum_certified']==(case['attained_count_upper_bound']==case['universal_count_lower_bound'])
 joint.append(dict(scenario=name,mode=mode,lower=case['universal_count_lower_bound'],upper=len(survivors)))
m=mask_for(s['measured_indicators']);required=[cities.index(c) for c in s['required_cities']]
assert s['required_cities']==next(x for x in j['scenarios'] if x['scenario']=='both_plus_homicide_rate' and x['mode']=='continuous')['unavoidable_cities']
def bounds(keep,delta):
 inside=np.zeros(25,bool);inside[keep]=True;width=np.minimum(D(str(delta)),hi-lo);l=lo.copy();u=hi.copy()
 l[m&inside[:,None]]=(hi-width)[m&inside[:,None]];u[m&~inside[:,None]]=(lo+width)[m&~inside[:,None]]
 assert np.max(abs((u-l)[m]-width[m]))<D('1e-18');return l,u,list(np.flatnonzero(~inside))
expected={tuple(sorted(required+list(extra))) for size in range(len(required),s['certified_minimum']+1) for extra in itertools.combinations([i for i in range(25) if i not in required],size-len(required))}
assert {tuple(x['keep_indices']) for x in s['records']}==expected
success=[]
for row in s['records']:
 keep=row['keep_indices'];l,u,out=bounds(keep,0)
 if row['status']=='excluded_by_strict_witness':
  i=row['outside_index'];assert i in out;gap=score(u,row['alpha'])[i]-score(l,row['alpha'])[keep].max();assert gap>D('1e-8') and abs(gap-D(str(row['score_gap'])))<D('1e-11')
 else:assert row['status']=='feasible_survivor_superset';enclose(l,u,keep,out);success.append(keep)
assert success==s['successful_sets'] and s['minimum_proved'] and s['certified_minimum']==4
checks=[]
for p in s['precision']:
 keep=p['keep_indices'];f=p['frontier'];cases=p['grid']+f['steps']+[f['feasible'],f['infeasible']];unique={x['delta']:x for x in cases};prev=None
 for delta,row in sorted(unique.items()):
  l,u,out=bounds(keep,delta)
  if prev is not None:assert np.all(l<=prev[0]) and np.all(u>=prev[1])
  prev=l,u
  if row['status']=='impossible_four_set':
   i=row['outside_index'];assert i in out;gap=score(u,row['witness_alpha'])[i]-score(l,row['witness_alpha'])[keep].max();assert gap>D('1e-8') and abs(gap-D(str(row['strict_score_gap'])))<D('1e-11');detail={'strict_gap':float(gap)}
  else:assert row['status']=='four_set_feasible';detail=enclose(l,u,keep,out)
  checks.append(dict(keep=keep,delta=delta,status=row['status'],**detail))
 assert f['status']=='bracketed' and 0<f['infeasible']['delta']-f['feasible']['delta']<=1e-4
g=s['global_minimum_size_frontier']
assert g['minimum_set_size']==4 and g['all_minimum_sets_enumerated']
assert g['feasible_width']==max(p['frontier']['feasible']['delta'] for p in s['precision'])
assert g['infeasible_width']==max(p['frontier']['infeasible']['delta'] for p in s['precision'])
# Exercise the real wrapper validation/output guard while mocking costly searches.
sys.path.insert(0,str(P.parents[1]/'scripts'))
import task4_registered_survivor_search as wrapper
config=dict(model_version=s['model_version'],fixed_alpha=s['fixed_alpha'],alpha_range=s['alpha_range'])
def fake_search(*args):return {k:s[k] for k in ('certified_minimum','attained_upper_bound','minimum_proved','successful_sets','records')}
def fake_frontier(l,u,m,k,a):return next(p['frontier'] for p in s['precision'] if p['keep_indices']==k)
def fake_evaluate(l,u,m,k,d,a):return next(r for p in s['precision'] if p['keep_indices']==k for r in p['grid'] if r['delta']==d)
validation=[]
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);prior=tmp/'prior.json';prior.write_text(json.dumps(j));out=tmp/'output'
 with patch.object(wrapper,'current_bounds',return_value=(lo.astype(float),hi.astype(float),config)),patch.object(wrapper,'search',side_effect=fake_search),patch.object(wrapper,'frontier',side_effect=fake_frontier),patch.object(wrapper,'evaluate',side_effect=fake_evaluate):
  wrapper.run(out,prior);wrapper.run(out,prior);validation.append('same model/weights rerun accepted')
  for key,value in [('model_version','WRONG'),('input_bounds_sha256','0'*64),('fixed_alpha',.15),('alpha_range',[.06,.19])]:
   bad=dict(j);bad[key]=value;prior.write_text(json.dumps(bad))
   try:wrapper.run(tmp/('bad_'+key),prior)
   except ValueError:validation.append('source '+key+' mismatch rejected')
   else:raise AssertionError('source '+key+' mismatch accepted')
  prior.write_text(json.dumps(j));changed=dict(config,fixed_alpha=.15)
  with patch.object(wrapper,'current_bounds',return_value=(lo.astype(float),hi.astype(float),changed)):
   try:wrapper.run(out,prior)
   except ValueError:validation.append('existing output changed weights rejected')
   else:raise AssertionError('changed output weights accepted')

result=dict(method='Independent long-double scores, monotone-alpha endpoint enclosures padded by 2e-9; no main scoring or polynomial solver imports',summary_sha256=hashlib.sha256((P/'summary.json').read_bytes()).hexdigest(),input_bounds_sha256=hashv,wrapper_validation=validation,global_minimum_size_frontier_verified=g,joint_scenarios_verified=joint,enumerated_candidate_sets=len(expected),certified_minimum=4,successful_sets=success,precision_checks=checks,scope='Independent utility boxes, shared hypothetical revelations, prescribed residual widths; no new observations. Numerical enclosures, not formal directed interval arithmetic.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
