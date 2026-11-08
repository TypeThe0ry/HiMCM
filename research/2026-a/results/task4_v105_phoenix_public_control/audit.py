"""Independent long-double numeric review, without model/scoring imports."""
import csv,hashlib,json
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parent;D=np.longdouble

def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def score(x,a):
 w=np.full(10,(1-a)/8,dtype=D);w[[6,9]]=a/2
 plus=np.sqrt((w*x*x).sum(axis=1));minus=np.sqrt((w*(1-x)**2).sum(axis=1));return 100*plus/(plus+minus)
def regret(l,u):return np.array([max(D(0),np.delete(u,i).max()-l[i]) for i in range(25)])
s=json.loads((P/'summary.json').read_text());src=P.parent.parent/'data/task4_v105_phoenix/summary.json'
assert hashlib.sha256(src.read_bytes()).hexdigest()==s['source_summary_sha256']
source=json.loads(src.read_text());raw=rows(P/'utility_bounds.csv');rank=rows(P/'ranks.csv');certs=rows(P/'recommendation_certificate.csv')
assert len(raw)==750 and len(rank)==75
base=rows(P.parent/'task4_v102_intake/utility_bounds.csv');cities=list(dict.fromkeys(r['city'] for r in base));names=list(dict.fromkeys(r['indicator'] for r in base))
blo=np.array([D(r['lower']) for r in base]).reshape(25,10);bhi=np.array([D(r['upper']) for r in base]).reshape(25,10)
assert hashlib.sha256(np.stack([blo,bhi]).astype('<f8').tobytes()).hexdigest()==s['input_bounds_sha256']
i,j=cities.index('Phoenix'),names.index('upper_secondary_ptr');mask=np.ones((25,10),bool);mask[i,j]=False
expected={'current_all_city':(D(0),D(1))}
for y in source['years']:
 nlo,nhi=y['grade9_12_lower'],y['including_possible_ungraded_upper'];tlo,thi=D(str(y['known_strict_teacher_fte_lower'])),y['teacher_fte_upper']
 expected['public_only_'+y['year']]=(D(0) if nhi is None else 15*tlo/(D(nhi)+15*tlo),D(1) if thi is None else 15*D(str(thi))/(D(nlo)+15*D(str(thi))))
assert set(expected)=={r['scenario'] for r in raw}=={r['scenario'] for r in rank}
error=D(0);reports=[];base_rank=None
for report in s['scenarios']:
 label=report['scenario'];b=[r for r in raw if r['scenario']==label];rr=[r for r in rank if r['scenario']==label]
 assert [(r['city'],r['indicator']) for r in b]==[(c,n) for c in cities for n in names]
 lo=np.array([D(r['lower']) for r in b]).reshape(25,10);hi=np.array([D(r['upper']) for r in b]).reshape(25,10)
 assert np.array_equal(lo[mask],blo[mask]) and np.array_equal(hi[mask],bhi[mask])
 assert abs(lo[i,j]-expected[label][0])<D('1e-15') and hi[i,j]==expected[label][1]
 l,u=score(lo,D('.1')),score(hi,D('.1'));reg=regret(l,u);dr=[]
 for k,r in enumerate(rr):
  assert r['city']==cities[k]
  for name,value in [('score_lower',l[k]),('score_upper',u[k]),('max_regret',reg[k])]:error=max(error,abs(value-D(r[name])))
  others=np.arange(25)!=k
  assertions={'decision_rank':1+sum(reg<reg[k]),'best_rank':1+sum(l[others]>u[k]+D('1e-12')),'worst_rank':1+sum(u[others]>l[k]+D('1e-12'))}
  for name,v in assertions.items():assert int(r[name])==v
  assert (r['possible_champion']=='True')==(u[k]>=max(l[others])-D('1e-12'))
  assert (r['necessary_champion']=='True')==(l[k]>=max(u[others])-D('1e-12'))
  dr.append(assertions['decision_rank'])
 if base_rank is None:base_rank=dr
 assert sum(a!=b for a,b in zip(dr,base_rank))==report['changed_ranks_vs_main']
 pairs=[np.sign(dr[a]-dr[b])*np.sign(base_rank[a]-base_rank[b]) for a in range(25) for b in range(a+1,25)]
 denom=np.sqrt(sum(dr[a]!=dr[b] for a in range(25) for b in range(a+1,25))*sum(base_rank[a]!=base_rank[b] for a in range(25) for b in range(a+1,25)))
 assert abs(sum(pairs)/denom-report['kendall_tau_vs_main'])<1e-12
 assert report['continuous_possible_champions']==cities and all(r['possible_champion']=='True' for r in rr)
 leaves=sorted([r for r in certs if r['scenario']==label],key=lambda r:float(r['alpha_lower']));last=D('.05');gaps=[]
 for leaf in leaves:
  a,b=D(leaf['alpha_lower']),D(leaf['alpha_upper']);assert a==last;last=b
  ls=np.array([score(lo,t) for t in (a,b)]);us=np.array([score(hi,t) for t in (a,b)])
  low=regret(ls.max(axis=0)+D('1e-9'),us.min(axis=0)-D('1e-9'));high=regret(ls.min(axis=0)-D('1e-9'),us.max(axis=0)+D('1e-9'))
  winner=int(leaf['winner']);gap=np.delete(low,winner).min()-high[winner]
  assert leaf['certified']=='True' and gap>D('1e-8') and cities[winner]=='Singapore'
  error=max(error,abs(gap-D(leaf['regret_gap_lower'])));gaps.append(float(gap))
 assert last==D('.2') and report['continuous_recommendation']==dict(unresolved=0,winners=['Singapore'])
 assert report['choice']==[cities[k] for k in np.flatnonzero(reg<=reg.min()+D('1e-12'))]
 reports.append(dict(scenario=label,utility=[float(x) for x in expected[label]],phoenix_rank=int(dr[i]),checked_certificate_leaves=len(leaves),minimum_gap=min(gaps)))
assert error<D('1e-11') and not s['main_admitted'] and s['actual_changed_cells']==0
out=dict(method='Independent long-double scores, regret, ranking, tau-b pair counts and continuous endpoint enclosures; no model imports',source_hash_verified=True,input_hash_verified=True,checked_utility_rows=750,checked_rank_rows=75,other249cells_unchanged=True,maximum_discrepancy=float(error),scenarios=reports,scope='Public-only slot diagnostics, not equivalent all-city rankings or causal education changes; original inputs remain unchanged.')
(P/'audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
