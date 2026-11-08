"""Independent long-double verification of four saved Warsaw scenarios."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
P=Path(__file__).resolve().parents[2]
def read(p):
 with p.open() as f:return list(csv.DictReader(f))
rows=read(P/'results/task4_v96_warsaw_revision/utility_bounds.csv');ranks=read(P/'results/task4_v96_warsaw_revision/ranks.csv')
scenarios=list(dict.fromkeys(r['scenario'] for r in rows)); cities=list(dict.fromkeys(r['city'] for r in rows)); indicators=list(dict.fromkeys(r['indicator'] for r in rows))
assert len(rows)==1000 and len(cities)==25 and len(indicators)==10
base={(r['city'],r['indicator']):(r['lower'],r['upper']) for r in read(P/'results/task4_v95_intake/utility_bounds.csv')}
assert {(r['city'],r['indicator']):(r['lower'],r['upper']) for r in rows if r['scenario']==scenarios[0]}==base
D=np.longdouble
mat={}
def score(x,alpha):
 w=np.full(10,(1-D(str(alpha)))/8,dtype=D);w[[6,9]]=D(str(alpha))/2
 good=np.sqrt(np.sum(w*x*x,axis=1));bad=np.sqrt(np.sum(w*(1-x)**2,axis=1));return 100*good/(good+bad)
maxerr=D(0)
for s in scenarios:
 rr=[r for r in rows if r['scenario']==s]
 assert [(r['city'],r['indicator']) for r in rr]==[(c,i) for c in cities for i in indicators]
 lo=np.array([D(r['lower']) for r in rr]).reshape(25,10);hi=np.array([D(r['upper']) for r in rr]).reshape(25,10);mat[s]=(lo,hi)
 changed=[(r['city'],r['indicator']) for r in rr if (r['lower'],r['upper'])!=base[(r['city'],r['indicator'])]]
 assert changed==([] if s==scenarios[0] else [('Warsaw','upper_secondary_ptr')])
 ls,us=score(lo,.1),score(hi,.1);reg=np.array([max(0,np.delete(us,i).max()-ls[i]) for i in range(25)])
 rank=np.array([1+sum(reg < x-D('1e-12')) for x in reg])
 result=[r for r in ranks if r['scenario']==s]
 assert [r['city'] for r in result]==cities
 for i,r in enumerate(result):
  for key,calc in [('score_lower',ls),('score_upper',us),('max_regret',reg)]:
   error=abs(D(r[key])-calc[i]);maxerr=max(maxerr,error);assert error<D('1e-11'),(s,key,error)
  assert int(r['decision_rank'])==rank[i]
  assert (r['possible_champion']=='True')==(us[i]>=np.delete(ls,i).max()-D('1e-12'))
  assert (r['necessary_champion']=='True')==(ls[i]>=np.delete(us,i).max())
  assert int(r['best_rank'])==1+sum(np.delete(ls,i)>us[i])
  assert int(r['worst_rank'])==1+sum(np.delete(us,i)>=ls[i])
 print(s,'verified 25 rows; Warsaw rank',rank[cities.index('Warsaw')])
i,j=cities.index('Warsaw'),indicators.index('upper_secondary_ptr')
assert abs(mat['v96_general_year_only'][1][i,j]-15*D(5655)/(87748+15*D(5655)))<D('1e-15')
assert mat['strict_scope_withdrawal'][0][i,j]==0 and mat['strict_scope_withdrawal'][1][i,j]==1
for a,b in zip(mat['v96_warsaw_resources'],mat['v91_before']):
 r=a.copy();r[i,j]=b[i,j];assert np.array_equal(r,b)
cert=read(P/'results/task4_v96_warsaw_revision/recommendation_certificate.csv')
for s in scenarios:
 cs=[r for r in cert if r['scenario']==s];assert D(cs[0]['alpha_lower'])==D('.05') and D(cs[-1]['alpha_upper'])==D('.2')
 assert all(a['alpha_upper']==b['alpha_lower'] for a,b in zip(cs,cs[1:]))
 lo,hi=mat[s]
 for r in cs:
  ls=np.array([score(lo,r[k]) for k in ['alpha_lower','alpha_upper']]);us=np.array([score(hi,r[k]) for k in ['alpha_lower','alpha_upper']]);pad=D('1e-9')
  lmin,lmax=ls.min(0)-pad,ls.max(0)+pad;umin,umax=us.min(0)-pad,us.max(0)+pad
  rmin=np.array([max(0,np.delete(umin,i).max()-lmax[i]) for i in range(25)]);rmax=np.array([max(0,np.delete(umax,i).max()-lmin[i]) for i in range(25)])
  winner=int(r['winner']);gap=np.delete(rmin,winner).min()-rmax[winner]
  assert r['certified']=='True' and cities[winner]==r['city']=='Singapore' and gap>D('1e-8')
  assert abs(gap-D(r['regret_gap_lower']))<D('1e-11')
sumfile=P/'results/task4_v96_warsaw_revision/summary.json';summary=json.loads(sumfile.read_text());assert summary['source_summary_sha256']==hashlib.sha256((P/'data/task4_v96_warsaw/summary.json').read_bytes()).hexdigest()
print('PASS baseline exact 250; non-target exact 249; 100 score/regret/rank rows; all',len(cert),'certificate leaves; source summary SHA; maximum score error',str(maxerr))
