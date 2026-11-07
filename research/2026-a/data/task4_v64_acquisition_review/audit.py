"""Independent CSV-based audit: no imports from the acquisition implementation."""
from pathlib import Path
from itertools import combinations
import hashlib,json
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
OUT=ROOT/'results/task4_v64_continuous_acquisition'
source=ROOT/'results/task4_v63_cape_2025/utility_bounds.csv'
b=pd.read_csv(source);b=b[b.scenario=='v63_ghs2025_age14_18']
cities=list(dict.fromkeys(b.city));names=list(dict.fromkeys(b.indicator))
lo=b.lower.to_numpy().reshape(len(cities),len(names));hi=b.upper.to_numpy().reshape(lo.shape)
eval=pd.read_csv(OUT/'bundle_evaluations.csv').fillna({'indicators':''})
cert=pd.read_csv(OUT/'bundle_certificates.csv')
minimum=pd.read_csv(OUT/'minimum_bundles.csv')

def scores(u,alpha):
 w=np.array([alpha/2 if n in ('public_transport_density','public_pool_density') else (1-alpha)/8 for n in names])
 plus=np.sqrt(np.sum(w*u*u,axis=1));minus=np.sqrt(np.sum(w*(1-u)*(1-u),axis=1))
 return 100*plus/(plus+minus)

def risk(l,h,alpha):
 a,z=scores(l,alpha),scores(h,alpha)
 return np.array([max(0,max(z[k] for k in range(len(cities)) if k!=i)-a[i]) for i in range(len(cities))])

def gap(l,h,i,alpha):
 r=risk(l,h,alpha)
 return min(r[k] for k in range(len(cities)) if k!=i)-r[i]

focal=[]
for city in ['Phoenix','Shanghai']:
 i=cities.index(city);unknown=np.flatnonzero(hi[i]-lo[i]>1e-12).tolist()
 current=minimum[minimum.city==city].iloc[0]
 expected=int(current.smallest_certified_continuous_bundle)
 e=eval[eval.city==city]
 smaller=e[e['size']<expected]
 expected_subsets={tuple(js) for size in range(expected) for js in combinations(unknown,size)}
 observed_subsets={tuple(names.index(n) for n in row.indicators.split('|')) if row.indicators else () for row in smaller.itertuples()}
 assert expected_subsets==observed_subsets and len(smaller)==len(expected_subsets)
 assert (smaller.status=='excluded_by_witness').all()
 witness_gaps=[]
 for row in smaller.itertuples():
  js=[names.index(n) for n in row.indicators.split('|')] if row.indicators else []
  l=lo.copy();l[i,js]=hi[i,js]
  v=gap(l,hi,i,row.witness_alpha)
  assert .05<=row.witness_alpha<=.2 and v < -1e-8
  assert abs(v-row.witness_margin)<2e-10
  witness_gaps.append(v)
 # Exhaustively calculate fixed-alpha minimum independently, not the old helper.
 fixed=None
 for size in range(len(unknown)+1):
  success=False
  for js in combinations(unknown,size):
   l=lo.copy();l[i,list(js)]=hi[i,list(js)]
   if gap(l,hi,i,.1)>1e-9:success=True
  if success:fixed=size;break
 assert fixed==int(current.fixed_alpha_minimum)
 successes=e[e.status=='certified_outer_box']
 assert len(successes)==int(current.certified_minimal_bundles)
 leaves_checked=0;cert_min=float('inf')
 for row in successes.itertuples():
  js=[names.index(n) for n in row.indicators.split('|')] if row.indicators else []
  l=lo.copy();l[i,js]=hi[i,js]
  leaves=cert[(cert.city==city)&(cert.indicators==row.indicators)].sort_values('alpha_lower')
  assert len(leaves)>0 and abs(leaves.iloc[0].alpha_lower-.05)<1e-15 and abs(leaves.iloc[-1].alpha_upper-.2)<1e-15
  assert (leaves.certified==True).all() and (leaves.winner==i).all()
  np.testing.assert_allclose(leaves.alpha_upper.to_numpy()[:-1],leaves.alpha_lower.to_numpy()[1:],rtol=0,atol=1e-15)
  for leaf in leaves.itertuples():
   assert leaf.alpha_upper>leaf.alpha_lower
   ls=np.array([scores(l,a) for a in [leaf.alpha_lower,leaf.alpha_upper]])
   us=np.array([scores(hi,a) for a in [leaf.alpha_lower,leaf.alpha_upper]])
   low=np.array([max(0,max(us[:,k].min()-1e-9 for k in range(len(cities)) if k!=j)-(ls[:,j].max()+1e-9)) for j in range(len(cities))])
   high=np.array([max(0,max(us[:,k].max()+1e-9 for k in range(len(cities)) if k!=j)-(ls[:,j].min()-1e-9)) for j in range(len(cities))])
   v=min(low[k] for k in range(len(cities)) if k!=i)-high[i]
   assert v>1e-8 and abs(v-leaf.regret_gap_lower)<2e-10
   cert_min=min(cert_min,v);leaves_checked+=1
 focal.append(dict(city=city,fixed_minimum=fixed,continuous_minimum=expected,all_smaller_subsets_verified=len(smaller),largest_negative_witness=max(witness_gaps),certified_bundles=len(successes),certified_leaves=leaves_checked,minimum_certificate_gap=cert_min))
assert [(r['fixed_minimum'],r['continuous_minimum']) for r in focal]==[(3,4),(2,3)]
result=dict(review='Independent formulas and exhaustive subset coverage for Phoenix and Shanghai',focal=focal,
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),algorithm_sha256=hashlib.sha256((ROOT/'scripts/task4_continuous_acquisition.py').read_bytes()).hexdigest(),
 conclusions=['Counts are city-indicator exact measurements, not data sources or collection costs.','Success assumes favorable observations jointly at upper endpoints in a rectangular outer model.','Not guaranteed observed values, actual performance champions, or identified physical joint feasibility.','All smaller subsets have strict negative witnesses; all successful certificate leaves cover the full alpha interval with target as unique minimax recommendation.','Numerical certificates use padding and tolerances, not formal interval arithmetic.'],files_changed_outside_review=False)
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(focal,indent=2))
