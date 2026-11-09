"""Weighted utility-error sensitivity for the retained historical gap; no ranking change."""
from pathlib import Path
import hashlib,json,math
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'results/task4_v162_tail_error'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def tail(cells,a):
 N=sum(w for q,w in cells);remaining=a*N;value=0.
 for q,w in sorted(cells):
  used=min(w,remaining);value+=q*used;remaining-=used
  if remaining<=1e-7:return value/(a*N)
 raise AssertionError('Tail not filled')
def main():
 source=R/'data/task4_v116_ibb/aggregate_results.json';s=json.loads(source.read_text());a=.2
 cells=sorted((math.exp(-float(t)/30),float(x['weight'])) for t,x in s['duration_histogram'].items())
 q=np.array([v for v,w in cells]);w=np.array([w for v,w in cells]);W=w.sum();U=s['summary']['weight_unknown'];B=s['optional_membership']['weight_total'];N=W+U+B
 zs=sorted(set([0.,1.,*q,*[a*high+(1-a)*low for i,low in enumerate(q) for high in q[i+1:]]]))
 zero=1-w.max()/W;rows=[];witnesses=[]
 for delta in [0.,.01,.05,.1,.2,.5,zero]:
  best=None
  for z in zs:
   costs=np.maximum(q-z,0)+(1/a-1)*np.maximum(z-q,0)
   left=(1-delta)*W;kept=np.zeros(len(q))
   for i in np.argsort(costs,kind='stable'):
    take=min(left,w[i]);kept[i]=take;left-=take
    if left<=1e-7:break
   value=float(np.dot(kept,costs))/N
   if best is None or value<best[0]-1e-14:best=(value,float(z),kept)
  gap,z,kept=best;edited=w-kept
  completion=list(zip(q,kept))+[(z,float(edited.sum()+U+B))]
  mean=sum(x*m for x,m in completion)/N;low=tail(completion,a)
  assert abs(mean-low-gap)<1e-11
  assert abs(edited.sum()-delta*W)<1e-6
  rows.append(dict(observed_weight_error_fraction=delta,editable_weight=delta*W,sharp_gap_in_fractional_mass_set=gap,attaining_unknown_and_edited_utility=z,attaining_minutes=-30*math.log(z) if z else None,witness_mean=mean,witness_lower_tail=low))
  witnesses.append(dict(delta=delta,bins=[dict(original_utility=float(x),original_weight=float(m),kept_weight=float(k),editable_weight=float(m-k)) for x,m,k in zip(q,w,kept)],reassigned_utility=z))
 prior=json.loads((R/'results/task4_v158_joint_gap/summary.json').read_text());assert abs(rows[0]['sharp_gap_in_fractional_mass_set']-prior['rows'][1]['sharp_joint_lower'])<1e-12
 result=dict(iteration='V162',scope='Hypothetical observed-utility errors only; fixed cohort and weights; weighted-mass relaxation, not whole-person corruption',city='Istanbul',year=2012,alpha=a,observed_weight=W,known_unknown_weight=U,optional_weight=B,max_denominator=N,breakpoints=len(zs),rows=rows,zero_gap_threshold_observed_weight_fraction=zero,largest_observed_utility_tie_weight=float(w.max()),error_rates_estimated=False,raw_record_source_upgraded=False,source_representation=s['provider'],primary_data_admissions=0,primary_score_width_change=0,current_model='V154 unchanged',current_paper='V160 unchanged',source_sha256={str(source.relative_to(R)):sha(source)},generator_sha256=sha(Path(__file__)))
 (O/'summary.json').write_text(json.dumps(result,indent=2)+'\n');(O/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
