"""Read-only independent audit of conditional cell-resolution certificates.

By default, prints the report to stdout and checks the derived table without
writing files. Use --output PATH --overwrite to write the JSON report; add
--rebuild-optimal-table to intentionally regenerate the derived CSV as well.
"""
import hashlib, itertools, json, math
from pathlib import Path
import numpy as np
import pandas as pd
from task4_audit_output import audit_parser, check_output, emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1]; O=R/'results/current_joint_collection'
CANONICAL=O/'verification.json'
parser=audit_parser(__doc__)
parser.add_argument('--rebuild-optimal-table',action='store_true',help='Explicitly regenerate optimal_three_cell_sets.csv')
args=parser.parse_args()
check_output(args,CANONICAL,R.parents[1])
if args.rebuild_optimal_table:
 if args.output is None or Path(args.output).expanduser().resolve()!=CANONICAL.resolve() or not args.overwrite:
  parser.error('--rebuild-optimal-table requires --output pointing to this audit’s canonical verification.json and --overwrite')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b,tol=2e-9): assert abs(float(a)-float(b))<tol,(a,b)
def score(x,w):
 a=math.sqrt(math.fsum(float(q)*float(z)**2 for q,z in zip(w,x)))
 b=math.sqrt(math.fsum(float(q)*(1-float(z))**2 for q,z in zip(w,x)))
 return 100*a/(a+b)
f,lo,hi=revised_bounds(); cities=f.city.tolist(); assert lo.shape==(16,10) and (lo<hi).sum()==48
snapshot=json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256']; assert len(snapshot)==548
protected=json.loads((R/'results/current_paper_review/current_verification.json').read_text())
for n,h in snapshot.items(): assert sha(R/n)==h,n
for group,num in [('additional_source_scope_sha256',22),('additional_figure_inputs_sha256',27),('additional_student_inputs_sha256',12),('additional_ai_inputs_sha256',6)]:
 assert len(protected[group])==num
 for n,h in protected[group].items(): assert sha(R/n)==h,n
paper=R.parents[2]/'HiMCM-Overleaf'
assert len(protected['current_files_sha256'])==7
for n,h in protected['current_files_sha256'].items(): assert sha(paper/n)==h,n
summary=json.loads((O/'summary.json').read_text()); fronts=pd.read_csv(O/'frontiers.csv',keep_default_na=False)
for n,h in summary['source_sha256'].items(): assert sha(R/n)==h,n
for n,h in summary['output_sha256'].items(): assert sha(O/n)==h,n
assert len(summary['source_sha256'])==3 and summary['certificate_plans']==32
plans=pd.read_csv(O/'candidate_minimums.csv'); measures=pd.read_csv(O/'measurements.csv'); certs=pd.read_csv(O/'certificates.csv'); ties=pd.read_csv(O/'tie_completion.csv'); budgets=pd.read_csv(O/'all_budgets.csv'); outputs=[]; allsets=[]
for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
 frontier=[]; subsets=[]
 for i in range(16):
  js=np.flatnonzero(lo[i]<hi[i]).tolist(); entries=[]; masks={}
  for k in range(len(js)+1):
   vals=[]
   for ss in itertools.combinations(js,k):
    a=lo[i].copy();b=hi[i].copy();a[list(ss)]=hi[i,list(ss)];b[list(ss)]=lo[i,list(ss)]
    v=(score(a,w),score(b,w));masks[ss]=v;vals.append(v)
   entries.append((max(v[0] for v in vals),min(v[1] for v in vals)))
  frontier.append(entries);subsets.append(masks)
  exported=fronts[(fronts.weight_reference==ref)&(fronts.city==cities[i])];assert len(exported)==len(entries)
  for k,(target,rival) in enumerate(entries):
   row=exported[exported.resolved_cells==k];assert len(row)==1;row=row.iloc[0]
   close(row.target_max_lower,target);close(row.rival_min_upper,rival)
   for field,which in [('target_subset',0),('rival_subset',1)]:
    names=row[field].split(';') if row[field] else [];assert len(names)==k and len(set(names))==k
    subset=tuple(sorted(NAMES.index(n) for n in names));assert subset in masks;close(masks[subset][which],(target,rival)[which])
 assert len(fronts[fronts.weight_reference==ref])==sum(map(len,frontier))
 gaps=[abs(a-b) for i,rows in enumerate(frontier) for a,_ in rows for j,r in enumerate(frontier) if i!=j for _,b in r]
 for i,city in enumerate(cities):
  costs=[]
  for k,(target,_) in enumerate(frontier[i]):
   per=[]
   for j in range(16):
    if j==i: continue
    valid=[t for t,(_,u) in enumerate(frontier[j]) if target-u>1e-10]
    if not valid:break
    per.append(min(valid))
   feasible=len(per)==15
   row=budgets[(budgets.weight_reference==ref)&(budgets.target_city==city)&(budgets.target_resolved_cells==k)].iloc[0]
   assert bool(row.feasible)==feasible
   if feasible:
    cost=k+sum(per);assert int(row.total_resolved_cells)==cost;costs.append(cost)
  plan=plans[(plans.weight_reference==ref)&(plans.target_city==city)].iloc[0]; assert min(costs)==int(plan.total_resolved_cells)
  m=measures[measures.plan_id==plan.plan_id]; assert len(m)==min(costs) and not m.duplicated(['city','indicator']).any()
  a=lo.copy();b=hi.copy()
  for r in m.itertuples():
   j=cities.index(r.city); t=NAMES.index(r.indicator); assert lo[j,t]<r.utility_observed<hi[j,t];close(r.prior_lower,lo[j,t]);close(r.prior_upper,hi[j,t]);a[j,t]=b[j,t]=r.utility_observed
  L=[score(x,w) for x in a];U=[score(x,w) for x in b]; margin=L[i]-max(U[j] for j in range(16) if i!=j); assert margin>1e-10;close(margin,plan.interior_strict_margin)
  cr=certs[certs.plan_id==plan.plan_id];assert len(cr)==16 and cr.city.nunique()==16
  for r in cr.itertuples():
   j=cities.index(r.city);close(r.post_score_lower,L[j]);close(r.post_score_upper,U[j]);assert bool(r.target)==(j==i)
 L=[score(x,w) for x in lo]; U=[score(x,w) for x in hi]; left=max(L);right=min(U);assert left<right
 tie=ties[ties.weight_reference==ref];assert len(tie)==160 and not tie.duplicated(['city','indicator']).any()
 for i,city in enumerate(cities):
  part=tie[tie.city==city].set_index('indicator'); x=np.array([part.loc[n,'utility'] for n in NAMES]); assert np.all(x>=lo[i]-1e-14) and np.all(x<=hi[i]+1e-14);close(score(x,w),part.iloc[0].target_score,1e-10)
 # Exhaust all 48-choose-3 sets, for the sole globally optimal target Zurich.
 target=cities.index('Zurich'); cells=list(zip(*np.where(lo<hi))); found=0
 for chosen in itertools.combinations(cells,3):
  by=[[] for _ in cities]
  for i,j in chosen: by[i].append(j)
  threshold=subsets[target][tuple(by[target])][0]
  if all(threshold-subsets[i][tuple(by[i])][1]>1e-10 for i in range(16) if i!=target):
   found+=1;allsets.append(dict(weight_reference=ref,target_city='Zurich',cells='; '.join(cities[i]+':'+NAMES[j] for i,j in chosen),endpoint_margin=threshold-max(subsets[i][tuple(by[i])][1] for i in range(16) if i!=target)))
 assert found>0
 sr=next(x for x in summary['weights'] if x['weight_reference']==ref)
 refplans=plans[plans.weight_reference==ref];best=int(refplans.total_resolved_cells.min()); assert sr['min_exact_cells']==best
 assert set(sr['optimistic_targets'])==set(refplans[refplans.total_resolved_cells==best].target_city)
 close(sr['minimum_frontier_comparison_abs_gap'],min(gaps));close(sr['common_score_interval'][0],left);close(sr['common_score_interval'][1],right);close(sr['tie_target_score'],(left+right)/2)
 outputs.append(dict(weight_reference=ref,min_all_frontier_abs_gap=min(gaps),common_score_interval=[left,right],optimal_three_cell_sets=found,combinations_examined=math.comb(48,3)))
table=O/'optimal_three_cell_sets.csv'
expected_table=pd.DataFrame(allsets).to_csv(index=False).encode('utf-8')
if args.rebuild_optimal_table:
 table.write_bytes(expected_table)
else:
 assert table.read_bytes()==expected_table,'derived optimal-three-cell table differs from independently enumerated result; use --rebuild-optimal-table with --output pointing to the canonical report and --overwrite to regenerate'
report=dict(status='pass',scope='Independent exhaustive row subset frontiers; strict interior utility witnesses and approximate tie checked in the rectangular model; no claim of raw-data realizability.',candidate_plans=32,tie_cells=320,core_hashes=len(snapshot),supplemental_hashes=67,paper_resource_hashes=7,weights=outputs,primary_output_hashes={p.name:sha(p) for p in sorted(O.glob('*.csv'))},summary_sha256=sha(O/'summary.json'),primary_collector_sha256=sha(R/'scripts/task4_current_joint_collection.py'),audit_script_sha256=sha(Path(__file__)))
emit_report(report,args,CANONICAL,R.parents[1])
