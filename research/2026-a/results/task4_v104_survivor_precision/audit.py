"""Independent long-double continuous enclosures; no model/root solver imports."""
import csv,hashlib,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;D=np.longdouble
s=json.loads((P/'summary.json').read_text());prior=P.parent/'task4_v103_survivor_search'
assert hashlib.sha256((prior/'summary.json').read_bytes()).hexdigest()==s['prior_summary_sha256']
p=json.loads((prior/'summary.json').read_text());pa=json.loads((prior/'audit.json').read_text())
assert p['minimum_proved'] and p['certified_minimum']==pa['certified_minimum']==4
assert p['successful_sets']==[s['keep_indices']] and pa['all_23_candidate_sets_verified']
with (P.parent/'task4_v102_intake/utility_bounds.csv').open() as f:r=list(csv.DictReader(f))
cities=list(dict.fromkeys(x['city'] for x in r));names=list(dict.fromkeys(x['indicator'] for x in r))
lo=np.array([D(x['lower']) for x in r]).reshape(25,10);hi=np.array([D(x['upper']) for x in r]).reshape(25,10)
before=np.stack([lo,hi]).copy();assert hashlib.sha256(before.astype('<f8').tobytes()).hexdigest()==s['input_bounds_sha256']==p['input_bounds_sha256']
keep=s['keep_indices'];inside=np.zeros(25,bool);inside[keep]=True;outside=np.flatnonzero(~inside)
mask=np.zeros_like(lo,bool);mask[:,[names.index(n) for n in s['measured_indicators']]]=True

def score(x,a):
 w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
 pos=np.sqrt((w*x*x).sum(axis=1));neg=np.sqrt((w*(1-x)**2).sum(axis=1));return 100*pos/(pos+neg)

def bounds(delta):
 width=np.minimum(D(str(delta)),hi-lo)
 low=lo.copy();up=hi.copy()
 low[mask&inside[:,None]]=(hi-width)[mask&inside[:,None]]
 up[mask&~inside[:,None]]=(lo+width)[mask&~inside[:,None]]
 assert np.all(low>=lo) and np.all(up<=hi) and np.all(low<=up)
 assert np.max(abs((up-low)[mask]-width[mask]))<D('1e-18')
 assert np.array_equal(low[~mask],lo[~mask]) and np.array_equal(up[~mask],hi[~mask])
 return low,up

cases=s['grid']+s['frontier']['steps']+[s['frontier']['feasible'],s['frontier']['infeasible']]
unique={float(x['delta']):x for x in cases};checked=[];last=None
for delta,r in sorted(unique.items()):
 low,up=bounds(delta)
 if last is not None:assert np.all(low<=last[0]) and np.all(up>=last[1])
 last=(low,up)
 if r['status']=='impossible_four_set':
  i=r['outside_index'];a=D(str(r['witness_alpha']));assert i in outside and D('.05')<=a<=D('.2')
  gap=score(up,a)[i]-max(score(low,a)[keep]);assert gap>D('1e-8') and abs(gap-D(str(r['strict_score_gap'])))<D('1e-11')
  checked.append(dict(delta=delta,status='strict_failure_verified',gap=float(gap),outside_city=cities[i]))
 else:
  assert r['status']=='four_set_feasible'
  stack=[(D('.05'),D('.2'),0)];leaves=[]
  while stack:
   a,b,depth=stack.pop()
   ls=np.array([score(low,t)[keep] for t in (a,b)]);us=np.array([score(up,t)[outside] for t in (a,b)])
   gap=ls.min(axis=0).max()-us.max(axis=0).max()-D('2e-9')
   if gap>D('1e-8'):leaves.append(dict(lower=float(a),upper=float(b),gap_lower=float(gap)))
   else:
    assert depth<25,'Unresolved enclosure'
    mid=(a+b)/2;stack.extend([(a,mid,depth+1),(mid,b,depth+1)])
  leaves.sort(key=lambda x:x['lower']);assert leaves[0]['lower']==.05 and leaves[-1]['upper']==.2
  assert all(x['upper']==y['lower'] for x,y in zip(leaves,leaves[1:]))
  checked.append(dict(delta=delta,status='continuous_feasibility_verified',leaves=leaves,minimum_gap_lower=min(x['gap_lower'] for x in leaves)))
f=s['frontier'];assert f['status']=='bracketed'
a,b=f['feasible']['delta'],f['infeasible']['delta']
assert (a,b)==(.00921630859375,.00927734375) and b-a==f['bracket_width'] and b-a<=1e-4
assert np.array_equal(np.stack([lo,hi]),before)
five=s['five_set_at_delta_001']
assert five['delta']==.01 and five['status']=='five_set_feasible' and five['certified_minimum']==5
assert any(x['delta']==.01 and x['status']=='strict_failure_verified' for x in checked)
keep=five['keep_indices'];assert keep==[1,3,7,22,23]
assert five['keep_cities']==[cities[i] for i in keep]
inside=np.zeros(25,bool);inside[keep]=True;outside=np.flatnonzero(~inside)
low,up=bounds(.01);stack=[(D('.05'),D('.2'),0)];five_leaves=[]
while stack:
 a,b,depth=stack.pop()
 ls=np.array([score(low,t)[keep] for t in (a,b)]);us=np.array([score(up,t)[outside] for t in (a,b)])
 gap=ls.min(axis=0).max()-us.max(axis=0).max()-D('2e-9')
 if gap>D('1e-8'):five_leaves.append(dict(lower=float(a),upper=float(b),gap_lower=float(gap)))
 else:
  assert depth<25,'Unresolved five-set enclosure'
  mid=(a+b)/2;stack.extend([(a,mid,depth+1),(mid,b,depth+1)])
five_leaves.sort(key=lambda x:x['lower'])
assert five_leaves[0]['lower']==.05 and five_leaves[-1]['upper']==.2
assert all(x['upper']==y['lower'] for x,y in zip(five_leaves,five_leaves[1:]))
five_check=dict(delta=.01,certified_minimum=5,keep_cities=five['keep_cities'],leaves=five_leaves,
 lower_bound_reason='Unique feasible four-set at zero width strictly fails at delta .01; every other <=4 set already fails at zero and widening cannot restore it.')
a,b=f['feasible']['delta'],f['infeasible']['delta']
result=dict(method='Independent long-double adaptive endpoint score enclosures; no polynomial solver/model imports',input_hash_verified=True,
 summary_sha256=hashlib.sha256((P/'summary.json').read_bytes()).hexdigest(),five_set_at_delta_001=five_check,
 prior_unique_four_set_proof_verified=True,nested_residual_intervals_verified=True,nonselected_and_original_bounds_preserved=True,
 feasible_threshold=a,infeasible_threshold=b,checked_distinct_widths=len(checked),checks=checked,
 logic='For prescribed widths, putting K intervals against upper endpoints maximizes their lower scores; putting outsider intervals against lower endpoints minimizes their upper scores. The point-revelation impossibility of every other <=4 set persists under widening.',
 limitation='Prescribed residual width min(delta, original width), not an at-most error allowance. Numerical padded continuous enclosure, not formal interval arithmetic. Only delta .01 has an independently certified matching five-set here; other failed widths establish at least five.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
