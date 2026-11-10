"""Optimistic exact-cell collection certificates in the unchanged V203 box.

Minimize resolved utility cells, not source files or research cost. This is a
conditional information diagnostic, not an observation or additional ranking.
"""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES,weights,score
R=Path(__file__).resolve().parents[1];O=R/'results/current_joint_collection';TOL=1e-10
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 model=json.loads((R/'design/task4_user_current_model.json').read_text());assert model['version']=='V203'
 snapshot=json.loads((R/model['snapshot']).read_text())['source_sha256']
 for name,h in snapshot.items():assert sha(R/name)==h,name
 f,lo,hi=revised_bounds();cities=f.city.tolist();uncertain=lo<hi;assert lo.shape==(16,10) and int(uncertain.sum())==48
 frontier_rows=[];plans=[];all_budgets=[];measurements=[];certificates=[];tie_rows=[];summaries=[]
 for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  front=[];comparison_gaps=[]
  for i,city in enumerate(cities):
   js=np.flatnonzero(uncertain[i]).tolist();entries={}
   for k in range(len(js)+1):
    candidates=[]
    for subset in itertools.combinations(js,k):
     a=lo[i].copy();b=hi[i].copy();a[list(subset)]=hi[i,list(subset)];b[list(subset)]=lo[i,list(subset)]
     candidates.append((float(score(a[None,:],w)[0]),float(score(b[None,:],w)[0]),subset))
    high=max(candidates,key=lambda z:z[0]);low=min(candidates,key=lambda z:z[1])
    entries[k]=dict(target_lower=high[0],target_mask=high[2],rival_upper=low[1],rival_mask=low[2])
    frontier_rows.append(dict(weight_reference=ref,city=city,resolved_cells=k,target_max_lower=high[0],target_subset=';'.join(NAMES[j] for j in high[2]),rival_min_upper=low[1],rival_subset=';'.join(NAMES[j] for j in low[2])))
   front.append(entries)
  comparison_gaps=[abs(t['target_lower']-r['rival_upper']) for i in range(16) for t in front[i].values() for j in range(16) if i!=j for r in front[j].values()]
  for i,city in enumerate(cities):
   options=[]
   for k,t in front[i].items():
    threshold=t['target_lower'];chosen={i:t['target_mask']};upper=[];feasible=True
    for j in range(16):
     if i==j:continue
     possible=[(n,r) for n,r in front[j].items() if threshold-r['rival_upper']>TOL]
     if not possible:feasible=False;break
     n,r=min(possible,key=lambda q:q[0]);chosen[j]=r['rival_mask'];upper.append(r['rival_upper'])
    row=dict(weight_reference=ref,target_city=city,target_resolved_cells=k,favourable_target_lower=threshold,feasible=feasible,total_resolved_cells=sum(map(len,chosen.values())) if feasible else None,endpoint_strict_margin=threshold-max(upper) if feasible else None)
    all_budgets.append(row)
    if feasible:options.append((row,chosen))
   assert options,city
   row,chosen=min(options,key=lambda z:(z[0]['total_resolved_cells'],-z[0]['endpoint_strict_margin']))
   # Interior selected observations avoid claiming endpoint utilities are finite observations.
   for eps in [1e-6,1e-8,1e-10,1e-12]:
    a=lo.copy();b=hi.copy()
    for j,subset in chosen.items():
     for t in subset:
      value=(hi[j,t]-eps*(hi[j,t]-lo[j,t])) if j==i else (lo[j,t]+eps*(hi[j,t]-lo[j,t]));a[j,t]=b[j,t]=value
    L,U=score(a,w),score(b,w);margin=float(L[i]-np.max(np.delete(U,i)))
    if margin>TOL:break
   else:raise AssertionError('No strict interior witness')
   plan_id=f'{ref}:{city}';plan=dict(row,plan_id=plan_id,competitor_resolved_cells=row['total_resolved_cells']-row['target_resolved_cells'],competitor_cities_measured=sum(bool(v) for j,v in chosen.items() if j!=i),interior_fraction=eps,interior_target_lower=float(L[i]),interior_max_rival_upper=float(np.max(np.delete(U,i))),interior_strict_margin=margin)
   plans.append(plan)
   for j,subset in chosen.items():
    for t in subset:
     assert lo[j,t]<a[j,t]<hi[j,t]
     measurements.append(dict(plan_id=plan_id,weight_reference=ref,target_city=city,city=cities[j],indicator=NAMES[t],prior_lower=float(lo[j,t]),prior_upper=float(hi[j,t]),utility_observed=float(a[j,t]),role='target' if j==i else 'competitor'))
   for j,name in enumerate(cities):certificates.append(dict(plan_id=plan_id,city=name,post_score_lower=float(L[j]),post_score_upper=float(U[j]),target=(j==i)))
  L,U=score(lo,w),score(hi,w);left,right=float(L.max()),float(U.min());assert right-left>TOL
  tie_score=(left+right)/2
  for i,city in enumerate(cities):
   a,b=0.,1.
   for _ in range(100):
    t=(a+b)/2;x=lo[i]+t*(hi[i]-lo[i]);value=float(score(x[None,:],w)[0])
    if value<tie_score:a=t
    else:b=t
   x=lo[i]+((a+b)/2)*(hi[i]-lo[i]);value=float(score(x[None,:],w)[0]);assert abs(value-tie_score)<1e-11
   for j,indicator in enumerate(NAMES):tie_rows.append(dict(weight_reference=ref,city=city,indicator=indicator,utility=float(x[j]),score=value,target_score=tie_score))
  selected=[p for p in plans if p['weight_reference']==ref];best=min(p['total_resolved_cells'] for p in selected)
  summaries.append(dict(weight_reference=ref,min_exact_cells=best,optimistic_targets=[p['target_city'] for p in selected if p['total_resolved_cells']==best],minimum_frontier_comparison_abs_gap=min(comparison_gaps),comparison_tolerance=TOL,common_score_interval=[left,right],tie_target_score=tie_score))
 O.mkdir(exist_ok=True)
 for name,rows in [('frontiers.csv',frontier_rows),('all_budgets.csv',all_budgets),('candidate_minimums.csv',plans),('measurements.csv',measurements),('certificates.csv',certificates),('tie_completion.csv',tie_rows)]:pd.DataFrame(rows).to_csv(O/name,index=False)
 protected=json.loads((R/'results/current_paper_review/current_verification.json').read_text())
 for group in ['additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256']:
  for name,h in protected[group].items():assert sha(R/name)==h,name
 for name,h in snapshot.items():assert sha(R/name)==h,name
 report=dict(status='computed; independent audit recorded separately',independent_verification='results/current_joint_collection/verification.json',primary_model='V203 unchanged',exact_utility_cells=48,weights=summaries,certificate_plans=len(plans),primary_admissions=0,actual_score_width_reduction=0,scope='Optimistic full utility identification inside a declared independent rectangular box, not source availability, raw-data cost, attainable integer counts or physical joint feasibility; no probabilities or guarantee for actual observations. Strictly interior utility witnesses do not prove raw-data realizability.',tie_scope='A simultaneous tie exists by continuity within the common score interval of the rectangular model; numerical witnesses approximate it. Not an observed or predicted real-world tie.',source_sha256={'design/task4_user_current_model.json':sha(R/'design/task4_user_current_model.json'),'design/task4_user_v203_snapshot.json':sha(R/'design/task4_user_v203_snapshot.json'),'scripts/task4_current_joint_collection.py':sha(Path(__file__))},output_sha256={name:sha(O/name) for name in ['frontiers.csv','all_budgets.csv','candidate_minimums.csv','measurements.csv','certificates.csv','tie_completion.csv']})
 (O/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
