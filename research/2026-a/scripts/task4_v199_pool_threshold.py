"""Conditional Singapore pool-count thresholds for source triage, not new data."""
import hashlib,json,math
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v197_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,weights,score
O=ROOT/'results/task4_v199_priority'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(a,w):
 out=[]
 for r in a:
  p=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,r)))
  n=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,r)))
  out.append(100*p/(p+n))
 return np.array(out)
def main():
 f,lo,hi=revised_bounds();initial=np.stack([lo,hi]).copy();cities=f.city.tolist();i=cities.index('Singapore');j=NAMES.index('public_pool_density');pop=int(f.iloc[i].population);assert pop==6036900
 assert int(f.iloc[i].population_year)==2024
 results=[];probes=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  U=scalar(hi,w)
  def case(count):
   a=lo.copy();d=count*100000/pop;a[i,j]=d/(1+d);L=scalar(a,w)
   np.testing.assert_allclose(L,score(a,w),rtol=0,atol=3e-13)
   r=np.array([max(0.,max(np.delete(U,k))-L[k]) for k in range(16)])
   return float(r[i]-np.delete(r,i).min()),r
  root=brentq(lambda n:case(n)[0],7,500,xtol=1e-12)
  n0,n1=math.floor(root),math.floor(root)+1
  assert case(n0)[0]>0 and case(n1)[0]<0
  for n in [7,n0,n1]:
   gap,r=case(n);probes.append(dict(weight_reference=ref,pool_count=n,regret_gap_Singapore_minus_best_other=gap,conservative_recommendation=';'.join(cities[k] for k in range(16) if r[k]<=r.min()+1e-12)))
  results.append(dict(weight_reference=ref,continuous_count_tie=root,first_integer_count_for_strict_Singapore_recommendation=n1,population=pop,population_year=2024,utility_upper_retained=1.))
 _,a,b=revised_bounds();np.testing.assert_array_equal(initial,np.stack([a,b]))
 O.mkdir(exist_ok=True);pd.DataFrame(probes).to_csv(O/'pool_count_threshold_probes.csv',index=False)
 report=dict(status='conditional_source_triage',base_science='V197 unchanged',paper='V198 unchanged',results=results,other159cells_alluppers_and_weights_fixed=True,primary_admissions=0,actual_active_model_width_reduction=0,scope='A verified compatible physical public-venue lower count would set only Singapore pool utility lower. Integer threshold is a deterministic model condition, not an observed count, prediction, policy feasibility or winner probability. Equality may tie; inventory/current opening and scope require independent source review.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'design/task4_user_v197_snapshot.json']})
 (O/'pool_count_thresholds.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
