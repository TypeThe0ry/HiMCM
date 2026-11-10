"""V203 point-utility uncertainty stress; primary inputs remain unchanged.

Only 112 point utilities widen additively. This is a specified uncertainty
scenario, not an observed/calibrated error rate, raw-value percentage or CI.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES,weights,score
R=Path(__file__).resolve().parents[1];O=R/'results/current_point_error'
PAD=1e-9;WIDTH=1e-9;MAX_EPS=.2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 f,lo,hi=revised_bounds();cities=f.city.tolist();mask=lo==hi;assert lo.shape==(16,10) and mask.sum()==112 and (~mask).sum()==48
 snapshot=json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256']
 for name,h in snapshot.items():assert sha(R/name)==h,name
 def bounds(e):
  a=lo.copy();b=hi.copy();a[mask]=np.maximum(0,lo[mask]-e);b[mask]=np.minimum(1,hi[mask]+e)
  assert np.array_equal(a[~mask],lo[~mask]) and np.array_equal(b[~mask],hi[~mask]);return a,b
 leaves=[];rankrows=[];boundrows=[];reports=[];witnesses=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  cache={}
  def evaluate(e):
   if e not in cache:
    a,b=bounds(e);L,U=score(a,w),score(b,w);rr=np.array([max(0.,float(np.delete(U,i).max()-L[i])) for i in range(16)]);cache[e]=(L,U,rr)
   return cache[e]
  baseline=int(np.argmin(evaluate(0.)[2]));pending=[(0.,MAX_EPS,0)];local=[]
  while pending:
   e0,e1,depth=pending.pop();r0=evaluate(e0)[2];r1=evaluate(e1)[2];c=int(np.argmin(r1));gap=float(np.delete(r0,c).min()-r1[c]-2*PAD);ok=gap>0
   if ok or e1-e0<=WIDTH:
    local.append(dict(weight_reference=ref,epsilon_lower=e0,epsilon_upper=e1,certified=ok,winner=cities[c] if ok else '',candidate=cities[c],strict_gap_lower=gap,candidate_regret_right=float(r1[c]),minimum_other_regret_left=float(np.delete(r0,c).min()),depth=depth))
   else:
    assert depth<40 and len(local)+len(pending)<100000,'Unresolved complexity cap'
    mid=(e0+e1)/2;pending.extend([(mid,e1,depth+1),(e0,mid,depth+1)])
  local.sort(key=lambda x:x['epsilon_lower']);assert local[0]['epsilon_lower']==0 and local[-1]['epsilon_upper']==MAX_EPS
  assert all(a['epsilon_upper']==b['epsilon_lower'] for a,b in zip(local,local[1:]));leaves+=local
  groups=[]
  for row in local:
   label=row['winner'] if row['certified'] else 'unresolved'
   if groups and groups[-1]['label']==label:groups[-1]['epsilon_upper']=row['epsilon_upper'];groups[-1]['leaves']+=1
   else:groups.append(dict(label=label,epsilon_lower=row['epsilon_lower'],epsilon_upper=row['epsilon_upper'],leaves=1))
  for group in groups:
   if group['label']!='unresolved':continue
   for side,e in [('left',max(0.,group['epsilon_lower']-1e-6)),('right',min(MAX_EPS,group['epsilon_upper']+1e-6))]:
    r=evaluate(e)[2];s=np.argsort(r);witnesses.append(dict(weight_reference=ref,band_lower=group['epsilon_lower'],band_upper=group['epsilon_upper'],side=side,epsilon=e,winner=cities[s[0]],winner_regret=float(r[s[0]]),runner_up=cities[s[1]],strict_gap=float(r[s[1]]-r[s[0]])))
  cases=[]
  for e in [0.,.001,.005,.01,.025,.05,.1,.2]:
   a,b=bounds(e);L,U,rr=evaluate(e);best=float(rr.min());chosen=[cities[i] for i in range(16) if rr[i]-best<1e-10];cases.append(dict(epsilon=e,minimax_choices=chosen,minimum_regret=best,mean_score_interval_width=float((U-L).mean())))
   for i,city in enumerate(cities):rankrows.append(dict(weight_reference=ref,epsilon=e,city=city,score_lower=float(L[i]),score_upper=float(U[i]),max_regret=float(rr[i]),decision_rank=int(1+(rr<rr[i]-1e-10).sum())))
   for i,city in enumerate(cities):
    for j,name in enumerate(NAMES):boundrows.append(dict(weight_reference=ref,epsilon=e,city=city,indicator=name,originally_point=bool(mask[i,j]),lower=float(a[i,j]),upper=float(b[i,j])))
  reports.append(dict(weight_reference=ref,baseline_recommendation=cities[baseline],groups=groups,leaves=len(local),unresolved_leaves=sum(not r['certified'] for r in local),padding=PAD,maximum_unresolved_leaf_width=WIDTH,cases=cases))
 O.mkdir(exist_ok=True)
 for name,rows in [('leaves.csv',leaves),('ranks.csv',rankrows),('bounds.csv',boundrows),('switch_witnesses.csv',witnesses)]:pd.DataFrame(rows).to_csv(O/name,index=False)
 for name,h in snapshot.items():assert sha(R/name)==h,name
 v=json.loads((R/'results/current_paper_review/current_verification.json').read_text())
 for group in ['additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256']:
  for name,h in v[group].items():assert sha(R/name)==h,name
 report=dict(status='computed; independent audit recorded separately',primary_model='V203 unchanged',point_utility_cells_widened=112,other_interval_cells_unchanged=48,epsilon_domain=[0,MAX_EPS],weights=reports,primary_admissions=0,actual_active_score_width_change=0,scope='Hypothetical independent additive uncertainty of point utilities only; not raw-value percentage, calibrated source errors, confidence intervals, probabilities, or a new primary model. Mean-derived partial travel bounds are not widened here.',interpretation='The winner is recomputed for each expanded uncertainty box. Stability does not certify identical recommendations for every exact perturbed point dataset inside that box.',certificate='Each regret is nondecreasing under nested boxes; endpoint regret ranges give numerical whole-interval winner certificates with padding. Unresolved bands retained; no monotone regret-difference or exact crossing assumption.',independent_verification='results/current_point_error/verification.json',source_sha256={'design/task4_user_v203_snapshot.json':sha(R/'design/task4_user_v203_snapshot.json'),'scripts/task4_current_point_error.py':sha(Path(__file__))},output_sha256={name:sha(O/name) for name in ['leaves.csv','ranks.csv','bounds.csv','switch_witnesses.csv']})
 (O/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps([{k:r[k] for k in ['weight_reference','groups','leaves','unresolved_leaves']} for r in reports],indent=2))
if __name__=='__main__':main()
