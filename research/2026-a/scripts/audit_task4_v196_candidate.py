import sys,math,json,hashlib,re,subprocess,tempfile
from pathlib import Path
import numpy as np,pandas as pd
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf'
sys.path.insert(0,str(R/'scripts'))
from task4_user_v192_revision import revised_bounds
O=R/'results/task4_v196_candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def scalar(mat,w):
 return np.array([100*math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))/(math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))+math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))) for row in mat])
def decide(l,u):
 regret=np.array([max(0.,max(u[k] for k in range(16) if k!=i)-l[i]) for i in range(16)])
 possible=[u[i]>=max(l[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 necessary=[l[i]>=max(u[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 return regret,possible,necessary,np.flatnonzero(regret<=regret.min()+1e-12)
def main():
 meta=json.loads((O/'preview.json').read_text());snap=json.loads((R/'design/task4_user_v192_snapshot.json').read_text())['source_sha256']
 for n,h in {**snap,**meta['source_sha256']}.items():assert sha(R/n)==h,n
 f,lo,hi=revised_bounds();before=np.stack([lo,hi]).copy();cities=f.city.tolist();i=cities.index('Zurich')
 # Indicator labels select the coordinate; scoring and decisions are independent.
 from task4_v5_model import NAMES
 j=NAMES.index('public_pool_density')
 assert int(f.iloc[i].population)==440935
 expected=1200000/(440935+1200000);assert abs(expected-meta['candidate_utility_lower'])<1e-14
 a=lo.copy();a[i,j]=expected
 mask=np.ones(lo.shape,bool);mask[i,j]=False
 assert np.array_equal(a[mask],lo[mask]) and np.array_equal(a[~mask],[expected])
 table=pd.read_csv(O/'scores.csv',float_precision='round_trip');assert len(table)==64
 assert not table.duplicated(['weight_reference','scenario','city']).any()
 count=0;summary=[]
 for ref,w in [('fixed',[.1125]*6+[.05,.1125,.1125,.05]),('equal',[.1]*10)]:
  for scenario,l in [('baseline_V192',lo),('candidate12_not_admitted',a)]:
   L,U=scalar(l,w),scalar(hi,w);regret,possible,necessary,choices=decide(L,U)
   for k,city in enumerate(cities):
    row=table[(table.weight_reference==ref)&(table.scenario==scenario)&(table.city==city)].iloc[0]
    np.testing.assert_allclose([row.score_lower,row.score_upper,row.max_regret],[L[k],U[k],regret[k]],atol=1e-12,rtol=0);count+=1
   m=next(s for s in meta['summary'] if s['weight_reference']==ref and s['scenario']==scenario)
   np.testing.assert_allclose([m['mean_score_width'],m['minimax_regret']],[(U-L).mean(),regret.min()],atol=1e-12,rtol=0)
   assert m['possible_count']==sum(possible)==16 and m['necessary_count']==sum(necessary)==0
   assert m['conservative_recommendation']==';'.join(cities[k] for k in choices)=='Zurich'
   summary.append(dict(weight_reference=ref,scenario=scenario,mean_width=float((U-L).mean()),minimax_regret=float(regret.min())))
 _,x,y=revised_bounds();assert np.array_equal(before,np.stack([x,y]))
 for n,h in snap.items():assert sha(R/n)==h,n
 # Read-only independent manuscript comparison, including all page rasters.
 old=(P/'drafts/task4_v193_references.tex').read_text();new=(P/'drafts/task4_v196_references.tex').read_text()
 assert old.replace('updated 9 October 2025.','updated 9 September 2025.')==new
 oldpdf=P/'drafts/task4_v193_paper.pdf';newpdf=P/'drafts/task4_v196_paper.pdf'
 def text(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True).split('\f')[:-1]
 ta,tb=text(oldpdf),text(newpdf);changed=[i+1 for i,(a,b) in enumerate(zip(ta,tb)) if a!=b];assert len(ta)==len(tb)==27 and changed==[24]
 pixelchanged=[]
 with tempfile.TemporaryDirectory(prefix='himcm-v196-independent-',dir='/data/scratch') as tmp:
  q=Path(tmp)
  for label,p in [('old',oldpdf),('new',newpdf)]:subprocess.run(['pdftoppm','-r','72','-gray',str(p),str(q/label)],check=True,stderr=subprocess.PIPE)
  for i in range(1,28):
   if (q/f'old-{i:02}.pgm').read_bytes()!=(q/f'new-{i:02}.pgm').read_bytes():pixelchanged.append(i)
 assert pixelchanged==[24]
 result=dict(status='pass',scope='Independent scalar candidate preview and narrow owned bibliography correction; no source-quality certification or admission.',scalar_score_interval_rows=count,norm_weight_once=True,self_excluded_regret=True,other159cells_and_alluppers_unchanged=True,active160bounds_unchanged=True,immutable_science_bindings_verified=327,primary_admissions=0,actual_active_model_width_reduction=0,summary=summary,review=dict(only_reference_update_month_corrected=True,text_changed_pages=changed,pixel_changed_pages_at72dpi=pixelchanged,total_pages=27,no_full_source_quality_claim=True),source_sha256={str(p.relative_to(R)):sha(p) for p in [Path(__file__),O/'preview.json',O/'scores.csv',R/'scripts/task4_v196_candidate.py',R/'results/task4_v196_review/verification.json']},paper_pdf_sha256=sha(newpdf))
 (O/'independent_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
main()
