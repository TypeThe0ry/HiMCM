"""Independent 80-digit scalar audit; reports to stdout without writing by default.

Explicit report delivery: python audit_task4_v205_point_error.py --output /tmp/point-audit.json
Use --overwrite to replace an existing report.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import csv, hashlib, json
import numpy as np
from task4_user_v205_revision import revised_bounds
from task4_v5_model import NAMES
from task4_audit_output import audit_parser, check_output, emit_report
getcontext().prec=80
R=Path(__file__).resolve().parents[1]; O=R/'results/task4_v205_point_error'; P=R.parents[2]/'HiMCM-Overleaf'
args=audit_parser(__doc__).parse_args()
check_output(args,O/'verification.json',R.parents[1])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda n:list(csv.DictReader((O/n).open(newline='')))
df=lambda x:D.from_float(float(x))
close=lambda x,y,t=D('2e-10'):abs(D(str(x))-y)<=t
summary=json.loads((O/'summary.json').read_text())
for p,h in summary['source_sha256'].items(): assert sha(R/p)==h,p
for p,h in summary['output_sha256'].items(): assert sha(O/p)==h,p
snapshot=(lambda x:{**x['upstream_source_sha256'],**x['source_sha256']})(json.loads((R/'design/task4_user_v205_snapshot.json').read_text()));assert len(snapshot)==773
extra={}
for p,h in snapshot.items():assert sha(R/p)==h,p
paper_hashes={}
f,l,h=revised_bounds();cities=f.city.tolist();assert l.shape==h.shape==(16,10)
mask=l==h;assert mask.sum()==112 and (~mask).sum()==48
lo=[[df(x) for x in row] for row in l];hi=[[df(x) for x in row] for row in h]
weights={'fixed':list(map(D,['.1125']*6+['.05','.1125','.1125','.05'])),'equal':[D('.1')]*10}
cache={}
def evaluate(ref,e):
 e=df(e);key=(ref,e)
 if key in cache:return cache[key]
 w=weights[ref]
 def sc(row):
  good=sum(w[j]*row[j]**2 for j in range(10)).sqrt();bad=sum(w[j]*(1-row[j])**2 for j in range(10)).sqrt();return 100*good/(good+bad)
 a=[[max(D(0),lo[i][j]-e) if mask[i,j] else lo[i][j] for j in range(10)] for i in range(16)]
 b=[[min(D(1),hi[i][j]+e) if mask[i,j] else hi[i][j] for j in range(10)] for i in range(16)]
 L=list(map(sc,a));U=list(map(sc,b));rr=[max(D(0),max(U[k] for k in range(16) if k!=i)-L[i]) for i in range(16)]
 cache[key]=(a,b,L,U,rr);return cache[key]
leaves=read('leaves.csv');counts={};minimum=None
for ref in weights:
 rows=[x for x in leaves if x['weight_reference']==ref];assert rows and float(rows[0]['epsilon_lower'])==0 and float(rows[-1]['epsilon_upper'])==.2
 for x,y in zip(rows,rows[1:]):assert x['epsilon_upper']==y['epsilon_lower']
 certified=0;unresolved=0
 for row in rows:
  a=float(row['epsilon_lower']);b=float(row['epsilon_upper']);assert 0<=a<b<=.2
  r0=evaluate(ref,a)[4];r1=evaluate(ref,b)[4];assert all(x<=y+D('1e-65') for x,y in zip(r0,r1))
  i=cities.index(row['candidate']);gap=min(r0[j] for j in range(16) if j!=i)-r1[i]-D('2e-9')
  assert close(row['strict_gap_lower'],gap) and close(row['candidate_regret_right'],r1[i]) and close(row['minimum_other_regret_left'],min(r0[j] for j in range(16) if j!=i))
  if row['certified']=='True':
   assert row['winner']==row['candidate'] and gap>0;certified+=1;minimum=gap if minimum is None else min(minimum,gap)
  else:
   assert row['winner']=='' and b-a<=1.00000001e-9;unresolved+=1
 counts[ref]={'positive_gap_leaves':certified,'unresolved_leaves':unresolved,'total':len(rows)}
 assert counts[ref]['total']>0
ranks=read('ranks.csv');bounds=read('bounds.csv');witnesses=read('switch_witnesses.csv');assert len(ranks)==256 and len(bounds)==2560 and len(witnesses)==2
assert len({(x['weight_reference'],x['epsilon'],x['city']) for x in ranks})==256
for row in ranks:
 ref=row['weight_reference'];i=cities.index(row['city']);a,b,L,U,r=evaluate(ref,row['epsilon'])
 assert close(row['score_lower'],L[i]) and close(row['score_upper'],U[i]) and close(row['max_regret'],r[i]);assert int(row['decision_rank'])==1+sum(x<r[i]-D('1e-10') for x in r)
assert len({(x['weight_reference'],x['epsilon'],x['city'],x['indicator']) for x in bounds})==2560
for row in bounds:
 i=cities.index(row['city']);j=NAMES.index(row['indicator']);a,b,*_=evaluate(row['weight_reference'],row['epsilon']);assert (row['originally_point']=='True')==mask[i,j]
 assert close(row['lower'],a[i][j],D('2e-16')) and close(row['upper'],b[i][j],D('2e-16'))
 if not mask[i,j]:assert df(row['lower'])==lo[i][j] and df(row['upper'])==hi[i][j]
for row in witnesses:
 ref=row['weight_reference'];e=float(row['epsilon']);r=evaluate(ref,e)[4];order=sorted(range(16),key=lambda i:r[i]);i,j=order[:2];assert row['winner']==cities[i] and row['runner_up']==cities[j] and r[j]>r[i]
 assert close(row['winner_regret'],r[i]) and close(row['strict_gap'],r[j]-r[i]);assert e<float(row['band_lower']) if row['side']=='left' else e>float(row['band_upper'])
for mapping in (snapshot,extra):
 for p,h in mapping.items():assert sha(R/p)==h,p
for p,h in paper_hashes.items():assert sha(P/p)==h and sha(R.parents[1]/'paper/current'/p)==h
result={'status':'pass','arithmetic':'80-digit Decimal; exact binary64 input conversion, decimal weights; numerical audit, not directed-rounding interval arithmetic','endpoint_enclosures':'Nested boxes and monotone nondecreasing individual regrets; all recorded certificate endpoint inequalities checked independently','leaf_counts':counts,'minimum_positive_padded_gap':str(minimum),'ranks_checked':len(ranks),'bounds_checked':len(bounds),'witnesses_checked':len(witnesses),'point_cells':112,'unchanged_interval_cells':48,'snapshot_hashes_checked':len(snapshot),'supplement_hashes_checked':len(extra),'paper_resources_and_mirror_sha256':paper_hashes,'fixed_unresolved_bands':[[float(x['epsilon_lower']),float(x['epsilon_upper'])] for x in leaves if x['weight_reference']=='fixed' and x['certified']=='False'],'scope':'Hypothetical additive utility radius; unresolved band does not establish unique switch, and no physical error calibration is implied.','source_sha256':{'scripts/audit_task4_v205_point_error.py':sha(Path(__file__)),'scripts/task4_audit_output.py':sha(R/'scripts/task4_audit_output.py'),'scripts/task4_v205_point_error.py':sha(R/'scripts/task4_v205_point_error.py'),'results/task4_v205_point_error/summary.json':sha(O/'summary.json'),**{f'results/task4_v205_point_error/{p}':sha(O/p) for p in summary['output_sha256']}}}
emit_report(result,args,O/'verification.json',R.parents[1])
