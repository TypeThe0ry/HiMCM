"""Independently audit single-point withdrawal; stdout by default."""
from pathlib import Path
import csv, hashlib, json, math
import numpy as np
import pandas as pd
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import SOURCE, build, FIELDS
from task4_v5_model import NAMES, weights
from task4_audit_output import audit_parser, check_output, emit_report

R=Path(__file__).resolve().parents[1]; O=R/'results/current_point_withdrawal'; REPO=R.parents[1]; P=REPO.parent/'HiMCM-Overleaf'
args=audit_parser(__doc__).parse_args(); check_output(args,O/'verification.json',REPO)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def close(a,b): return math.isclose(float(a),float(b),rel_tol=0,abs_tol=2e-10)
def same(a,b):
 if pd.isna(b): return a==''
 try: return close(a,b)
 except (ValueError,TypeError): return a==str(b)
def read(name):
 with (O/name).open(newline='') as fh: return list(csv.DictReader(fh))
s=json.loads((O/'summary.json').read_text())
for n,h in s['source_sha256'].items(): assert sha(R/n)==h,n
for n,h in s['output_sha256'].items(): assert sha(O/n)==h,n
snapshot=json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256']
v=json.loads((R/'results/current_paper_review/current_verification.json').read_text()); extra={}
for k,d in v.items():
 if k.startswith('additional_') and k.endswith('_sha256'): extra.update(d)
assert len(snapshot)==548 and len(extra)==77
def check_bindings():
 for mapping in (snapshot,extra):
  for n,h in mapping.items(): assert sha(R/n)==h,n
check_bindings()
resources=[Path('main.tex'),Path('ref.bib'),Path('mcmthesis.cls')]+sorted(x.relative_to(P) for x in (P/'figures').glob('*') if x.is_file()); assert len(resources)==7
assert set(map(str,resources))==set(v['current_files_sha256'])
paper={str(p):v['current_files_sha256'][str(p)] for p in resources}
def check_paper():
 for n,h in paper.items(): assert sha(P/n)==h and sha(REPO/'paper/current'/n)==h,n
check_paper()
f,lo,hi=revised_bounds(); raw=pd.read_csv(SOURCE); oldlo,oldhi,_=build(raw); cities=f.city.tolist()
assert cities==raw.city.tolist() and lo.shape==(16,10)
mask=lo==hi; assert mask.sum()==112 and (~mask).sum()==48 and np.array_equal(mask,oldlo==oldhi)
assert np.array_equal(lo[mask],oldlo[mask]) and np.array_equal(hi[mask],oldhi[mask])
ws={'fixed':[.1125]*6+[.05,.1125,.1125,.05], 'equal':[.1]*10}
assert np.allclose(weights(.1),ws['fixed'],rtol=0,atol=1e-16)
def calc(a,b,w):
 def sc(z):
  x=math.sqrt(sum(w[j]*float(z[j])**2 for j in range(10)));y=math.sqrt(sum(w[j]*(1-float(z[j]))**2 for j in range(10)));return 100*x/(x+y)
 L=[sc(row) for row in a]; U=[sc(row) for row in b]
 regret=[max(0.,max(U[k] for k in range(16) if k!=i)-L[i]) for i in range(16)]
 best=[1+sum(L[k]>U[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
 worst=[1+sum(U[k]>L[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
 possible=[U[i]>=max(L[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 necessary=[L[i]>=max(U[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 choices=[cities[i] for i,r in enumerate(regret) if r<=min(regret)+1e-12]
 rank=[1+sum(x<regret[i]-1e-10 for x in regret) for i in range(16)]
 return L,U,regret,best,worst,possible,necessary,choices,rank
cases=read('cases.csv'); ranks=read('ranks.csv'); assert len(cases)==224 and len(ranks)==3584
cases_by={(x['weight_reference'],x['withdrawn_city'],x['indicator']):x for x in cases}
ranks_by={(x['weight_reference'],x['withdrawn_city'],x['indicator'],x['city']):x for x in ranks}
assert len(cases_by)==224 and len(ranks_by)==3584
changed={}
for ref,w in ws.items():
 base=calc(lo,hi,w); bc=base[7]; bmin=min(base[2]); bw=sum(u-l for l,u in zip(base[0],base[1]))/16
 assert s['baseline'][ref]['choices']==bc and close(s['baseline'][ref]['minimax_regret'],bmin) and close(s['baseline'][ref]['mean_width'],bw)
 changed[ref]=0
 for i,j in np.argwhere(mask):
  a=lo.copy();b=hi.copy();a[i,j]=0;b[i,j]=1; assert np.array_equal(a[~mask],lo[~mask]) and np.array_equal(b[~mask],hi[~mask])
  L,U,reg,br,wr,pc,nc,choice,dr=calc(a,b,w); case=cases_by[(ref,cities[i],NAMES[j])]; field=FIELDS[j]; source=raw.iloc[i]
  assert case['input_field']==field and same(case['submitted_value'],source[field]) and same(case['submitted_year'],source.get(field+'_year')) and same(case['submitted_flag'],source.get(field+'_flag'))
  assert close(case['retained_utility'],lo[i,j]) and json.loads(case['baseline_choices'])==bc and json.loads(case['after_choices'])==choice
  ch=choice!=bc;changed[ref]+=ch; assert (case['recommendation_set_changed']=='True')==ch
  mw=sum(u-l for l,u in zip(L,U))/16
  assert close(case['baseline_choice_excess_regret'],min(reg[cities.index(c)] for c in bc)-min(reg)) and close(case['post_minimax_regret'],min(reg)) and close(case['baseline_minimax_regret'],bmin) and close(case['mean_width'],mw) and close(case['mean_width_increase'],mw-bw)
  assert int(case['possible_champions'])==sum(pc) and int(case['necessary_champions'])==sum(nc)
  for k,c in enumerate(cities):
   row=ranks_by[(ref,cities[i],NAMES[j],c)]
   assert close(row['score_lower'],L[k]) and close(row['score_upper'],U[k]) and close(row['max_regret'],reg[k])
   assert int(row['best_rank'])==br[k] and int(row['worst_rank'])==wr[k] and int(row['decision_rank'])==dr[k]
   assert (row['possible_champion']=='True')==pc[k] and (row['necessary_champion']=='True')==nc[k]
assert changed==s['changed_recommendation_cases']=={'fixed':10,'equal':35}
assert s['point_cells']==112 and s['existing_interval_cells_held_fixed']==48 and s['weight_references']==2 and s['cases']==224 and s['rank_rows']==3584 and s['primary_admissions']==s['actual_primary_width_reduction']==0
check_bindings();check_paper()
report={'status':'pass','arithmetic':'independent scalar math.sqrt, binary64; absolute tolerance 2e-10, recommendation tolerance 1e-12','point_cells_matching_original':112,'fixed_interval_cells':48,'cases_checked':224,'rank_rows_checked':3584,'changed_recommendation_cases':changed,'snapshot_hashes_checked':len(snapshot),'supplement_hashes_checked':len(extra),'paper_resources_and_mirror_sha256':paper,'scope':'Hypothetical withdrawal to [0,1] represents ignorance stress, not evidence of an erroneous observation or correction to the primary model.','source_sha256':{'scripts/audit_current_point_withdrawal.py':sha(Path(__file__)),'scripts/task4_audit_output.py':sha(R/'scripts/task4_audit_output.py'),'results/current_point_withdrawal/summary.json':sha(O/'summary.json'),**{f'results/current_point_withdrawal/{n}':sha(O/n) for n in s['output_sha256']}}}
emit_report(report,args,O/'verification.json',REPO)
