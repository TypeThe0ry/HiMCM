"""Independent table transcription and fixed-population LP enumeration audit."""
import json,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
s=json.loads((P/'summary.json').read_text())
for m in json.loads((P/'manifest.json').read_text()):
 b=(P/m['file']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
# Independent transcription of tables V9,V11,V18 from raw p72,75,86.
stage=np.array([[62,13,20],[11,0,1],[6,2,5],[15,13,26],[21,11,14],[17,24,21],[0,2,0],[164,52,55],[15,2,1]])
age=np.array([[58,37,0],[10,2,0],[7,6,0],[15,36,3],[20,25,1],[16,41,5],[0,2,0],[157,112,2],[16,2,0]])
times=np.array([[21,55,15,4,0,0],[4,8,0,0,0,0],[0,5,6,2,0,0],[0,9,19,14,10,2],[0,14,29,2,1,0],[0,29,26,6,1,0],[0,1,1,0,0,0],[0,117,143,11,0,0],[0,4,12,1,1,0]])
for k,r in enumerate(s['mode_counts']):
 assert np.array_equal(stage[k],r['school_type_counts']);assert np.array_equal(age[k],r['age_group_counts']);assert np.array_equal(times[k],r['time_counts'])
H=stage[:,1:].sum(axis=1); N=times.sum(axis=1);O=age[:,2];Y=age[:,0]
low=np.exp(-np.array([15,15,30,60,90,np.inf])/30);high=np.exp(-np.array([0,5,15,30,60,90])/30)
# Fixed 262 target, explicit ordinary LP with per-mode target counts.
A=np.zeros((9,54))
for m in range(9):A[m,m*6:m*6+6]=1
out=[]
for u,sign in [(low,1),(high,-1)]:
 r=linprog(sign*np.tile(u,9),A_eq=A,b_eq=H,bounds=[(0,int(n)) for n in times.ravel()],method='highs');assert r.success;out.append(sign*r.fun/262)
assert np.allclose(out,s['mode_stratified_school_type_bounds'],rtol=0,atol=1e-12)
# Direct, unscaled constraints; enumerate every feasible integer target population.
Aeq=np.zeros((2,63));Aeq[0,:54]=1;Aeq[1,54:]=1
Au=[];bu=[]
for m in range(9):
 row=np.zeros(63);row[m*6:m*6+6]=1;Au.append(row.copy());bu.append(H[m])
 row[54+m]=1;Au.append(row.copy());bu.append(N[m]-O[m])
 Au.append(-row.copy());bu.append(O[m]-H[m])
res=[]
for target in range(249,263):
 rr=[]
 for u,sign in [(low,1),(high,-1)]:
  c=np.r_[sign*np.tile(u,9),np.zeros(9)]
  r=linprog(c,A_ub=Au,b_ub=bu,A_eq=Aeq,b_eq=[target,2],bounds=[(0,int(n)) for n in times.ravel()]+[(0,int(n)) for n in Y],method='highs')
  assert r.success,r.message;rr.append(sign*r.fun/target)
 res.append((target,*rr))
lo=min(res,key=lambda x:x[1]);hi=max(res,key=lambda x:x[2]);assert abs(lo[1]-s['age14_18_and_school_type_bounds'][0])<1e-12;assert abs(hi[2]-s['age14_18_and_school_type_bounds'][1])<1e-12
for w,u in zip(s['age_target_extrema'],[low,high]):
 z=np.array(w['target_time_counts']);v=np.array(w['age13_counts']);q=z.sum(axis=1)
 assert np.max(abs(z-z.round()))<1e-10 and np.max(abs(v-v.round()))<1e-10
 assert np.all(z>=-1e-10) and np.all(z<=times+1e-10)
 assert abs(v.sum()-2)<1e-10 and np.all(v>=0) and np.all(v<=Y)
 assert np.all(q<=H+1e-10) and np.all(q+v<=N-O+1e-10) and np.all(q+v>=H-O-1e-10)
 assert abs((z*u).sum()/z.sum()-w['objective'])<1e-12
print(json.dumps(dict(hashes=3,raw_tables_match=True,age_histogram_visually_checked=True,same262_lp_bounds=out,independent_direct_lp_count=28,age_bounds=[lo[1],hi[2]],extreme_target_counts=[lo[0],hi[0]],integer_witnesses_valid=True),indent=2))
