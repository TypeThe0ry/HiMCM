"""Published marginal constraints; no fabricated student-level joint table."""
import hashlib,json,re,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from pypdf import PdfReader
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'scripts'))
from task4_subgroup_bounds import subgroup_bounds
MODES=['Jalan Kaki','Sepeda','Bus Sekolah','Angkutan Umum','Transportasi Online','Motor','Mobil','Diantar Motor','Diantar Mobil']

def extract_table(text,anchor,n):
 t=text.split(anchor,1)[1]
 return np.array([[int(x) for x in re.search(r'(?m)^'+re.escape(mode)+r'\s+'+r'\s+'.join([r'(\d+)']*(n+1))+r'\s*$',t).groups()] for mode in MODES])

def age_lp(counts,H,old,young,utility):
 # y_mb=z_mb*t, v_m=age13_m*t, t=1/target_count.
 M,B=counts.shape;K=M*B;T=K+M;N=counts.sum(axis=1)
 eq=[];rhs=[];a=np.zeros(T+1);a[:K]=1;eq.append(a);rhs.append(1)
 a=np.zeros(T+1);a[K:T]=1;a[T]=-2;eq.append(a);rhs.append(0)
 ub=[]
 for m in range(M):
  ix=slice(m*B,(m+1)*B)
  for b in range(B):
   a=np.zeros(T+1);a[m*B+b]=1;a[T]=-counts[m,b];ub.append(a)
  # target mass at most high-school count and age-eligible count
  a=np.zeros(T+1);a[ix]=1;a[T]=-H[m];ub.append(a)
  a=np.zeros(T+1);a[ix]=1;a[K+m]=1;a[T]=-(N[m]-old[m]);ub.append(a)
  # intersection lower bound H - age-outside
  a=np.zeros(T+1);a[ix]=-1;a[K+m]=-1;a[T]=H[m]-old[m];ub.append(a)
  a=np.zeros(T+1);a[K+m]=1;a[T]=-young[m];ub.append(a)
 c=np.zeros(T+1);c[:K]=np.tile(utility,M)
 r=linprog(c,A_ub=ub,b_ub=np.zeros(len(ub)),A_eq=eq,b_eq=rhs,bounds=[(0,None)]*T+[(1/262,1/249)],method='highs')
 assert r.success,r.message
 t=r.x[T];z=r.x[:K].reshape(M,B)/t;age13=r.x[K:T]/t
 assert abs(z.sum()-1/t)<1e-7 and abs(age13.sum()-2)<1e-7
 assert np.all(z>=-1e-7) and np.all(z<=counts+1e-7)
 mass=z.sum(axis=1);A=N-old-age13
 assert np.all(mass<=np.minimum(H,A)+1e-7) and np.all(mass>=np.maximum(0,H+A-N)-1e-7)
 assert np.all(age13>=-1e-7) and np.all(age13<=young+1e-7)
 integer=np.max(np.abs(np.r_[z.ravel(),age13]-np.round(np.r_[z.ravel(),age13])))<1e-7
 return dict(objective=float(r.fun),target_count=float(1/t),integer_count_witness=bool(integer),target_time_counts=z.tolist(),age13_counts=age13.tolist())

def main():
 for name,digest in json.loads((P/'reused_sources.json').read_text()).items():assert hashlib.sha256((P.parents[1]/name).read_bytes()).hexdigest()==digest
 for row in json.loads((P/'manifest.json').read_text()):assert hashlib.sha256((P/row['file']).read_bytes()).hexdigest()==row['sha256']
 pages=PdfReader(P/'thesis_chapter5.pdf').pages
 stage=extract_table(pages[18].extract_text(),'Tabel V. 11',3)
 times=extract_table(pages[29].extract_text(),'Waktu Tempuh Total',6)
 age=extract_table(pages[15].extract_text(),'Tabel V. 9',3)
 assert np.array_equal(stage[:,-1],times[:,-1]) and np.array_equal(stage[:,-1],age[:,-1])
 assert np.array_equal(stage[:,:-1].sum(axis=0),[311,119,143])
 assert np.array_equal(times[:,:-1].sum(axis=0),[25,242,251,40,13,2])
 assert np.array_equal(age[:,:-1].sum(axis=0),[299,263,11])
 for a in (stage,times,age):assert np.array_equal(a[:,:-1].sum(axis=1),a[:,-1])
 # Exact age histogram is separately visually checked at printed p64.
 exact_age={13:2,14:70,15:227,16:97,17:128,18:38,19:8,20:3}
 assert re.search(r'\b2\s+70\s+227\s+97\s+128\s+38\s+8\s+3\b',pages[7].extract_text())
 assert sum(exact_age.values())==573 and sum(v for k,v in exact_age.items() if k<16)==299 and sum(v for k,v in exact_age.items() if 16<=k<=18)==263
 counts=times[:,:-1];H=stage[:,1]+stage[:,2]
 low=np.exp(-np.array([15,15,30,60,90,np.inf])/30);high=np.exp(-np.array([0,5,15,30,60,90])/30)
 parent=subgroup_bounds(counts.sum(axis=0),low,high,[262,262])
 previous=json.loads((P.parent/'task4_v94_travel/summary.json').read_text())
 np.testing.assert_allclose(parent,previous['subgroup_utility_bounds'],rtol=0,atol=1e-15)
 modes=[subgroup_bounds(counts[m],low,high,[H[m],H[m]]) for m in range(9)]
 strat=np.sum(np.array(modes)*H[:,None],axis=0)/262
 alo=age_lp(counts,H,age[:,2],age[:,0],low)
 ahi=age_lp(counts,H,age[:,2],age[:,0],-high);ahi['objective']=-ahi['objective']
 assert alo['integer_count_witness'] and ahi['integer_count_witness']
 result=dict(main_admitted=False,original_thesis_bytes_acquired=True,parent_n=573,school_type_subgroup_n=262,
   legacy_marginal_bounds=list(parent),mode_stratified_school_type_bounds=strat.tolist(),
   width_reduction_fraction=float(1-(strat[1]-strat[0])/(parent[1]-parent[0])),
   age14_18_and_school_type_bounds=[alo['objective'],ahi['objective']],age_target_extrema=[alo,ahi],
   exact_age_counts=exact_age,mode_counts=[dict(mode=MODES[m],school_type_counts=stage[m,:3].tolist(),time_counts=counts[m].tolist(),age_group_counts=age[m,:3].tolist()) for m in range(9)],
   scope='Unweighted valid respondents at sampled Central Jakarta public schools; source-compatible marginal envelopes, not DKI city inference or sampling confidence intervals.',
   first_bin_policy='Keep V94 conservative 0-15 closure for matched comparison; thesis table and blank questionnaire both say under5, journal prose conflicts.')
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['mode_counts','age_target_extrema']},indent=2))
if __name__=='__main__':main()
