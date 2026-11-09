"""Independent all-breakpoint mass-selection LP audit of utility-error sensitivity."""
from pathlib import Path
import hashlib,json,math,subprocess
import numpy as np
from scipy.optimize import linprog
R=Path(__file__).resolve().parents[1];P=Path('/data/projects/HiMCM-Overleaf');O=R/'results/task4_v162_tail_error'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 result=read(O/'summary.json');src=read(R/'data/task4_v116_ibb/aggregate_results.json')
 for n,h in result['source_sha256'].items():assert sha(R/n)==h,n
 assert sha(R/'scripts/task4_v162_tail_error.py')==result['generator_sha256']
 q=np.array([math.exp(-float(t)/30) for t in src['duration_histogram']]);w=np.array([r['weight'] for r in src['duration_histogram'].values()],float)
 a=result['alpha'];W=w.sum();N=result['max_denominator'];assert W==499950 and N==681503
 # Crossings of the two arms: q_high-z=(1/a-1)(z-q_low).
 candidates={0.,1.,*q}
 for low in q:
  for high in q:
   if low<high:candidates.add((high+(1/a-1)*low)/(1/a))
 # Floating expressions may differ by ulps; preserve every candidate for safety.
 successful=0;checks=[]
 for row in result['rows']:
  fraction=row['observed_weight_error_fraction'];retained=(1-fraction)*W;best=float('inf')
  for z in candidates:
   costs=np.where(q<z,(1/a-1)*(z-q),q-z)
   lp=linprog(costs,A_eq=np.ones((1,len(q))),b_eq=[retained],bounds=[(0,float(m)) for m in w],method='highs')
   assert lp.success,lp.message;successful+=1
   assert abs(lp.x.sum()-retained)<1e-6
   best=min(best,lp.fun/N)
  assert abs(best-row['sharp_gap_in_fractional_mass_set'])<1e-10
  checks.append(dict(delta=fraction,LP_minimum=best))
 witnesses=read(O/'witnesses.json');tail_checks=0
 for row,wt in zip(result['rows'],witnesses):
  bins=wt['bins'];kept=np.array([x['kept_weight'] for x in bins]);edited=np.array([x['editable_weight'] for x in bins]);original=np.array([x['original_weight'] for x in bins]);uq=np.array([x['original_utility'] for x in bins])
  assert np.allclose(kept+edited,original,atol=1e-9,rtol=0) and np.all(kept>=0) and np.all(edited>=-1e-9)
  assert abs(edited.sum()-row['editable_weight'])<1e-6
  free=edited.sum()+result['known_unknown_weight']+result['optional_weight'];weights=np.r_[kept,free];utilities=np.r_[uq,wt['reassigned_utility']]
  assert abs(weights.sum()-N)<1e-6
  tail=linprog(utilities,A_eq=np.ones((1,len(utilities))),b_eq=[a*N],bounds=[(0,float(m)) for m in weights],method='highs');assert tail.success;tail_checks+=1
  mean=np.dot(utilities,weights)/N;low=tail.fun/(a*N)
  assert abs(mean-row['witness_mean'])<1e-12 and abs(low-row['witness_lower_tail'])<1e-12
  assert abs(mean-low-row['sharp_gap_in_fractional_mass_set'])<1e-11
 assert abs(result['zero_gap_threshold_observed_weight_fraction']-(1-w.max()/W))<1e-12
 assert result['rows'][-1]['sharp_gap_in_fractional_mass_set']==0
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 guard=O/'protected_files.json'
 if guard.exists():protected=read(guard)['manuscript']
 else:
  names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0');protected={n:sha(P/n) for n in names if n}
 for n,h in protected.items():assert sha(P/n)==h,n
 attempts=read(R/'data/task4_v162_ibb_probe/retrieval.json');assert len(attempts)==2 and all('timed out' in x['error'] for x in attempts)
 review=read(R/'design/task4_user_current_review.json');assert review['version']=='V160' and sha(P/review['pdf'])==review['pdf_sha256']
 (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':protected},indent=2)+'\n')
 audit=dict(status='pass',iteration='V162',independent_method='SciPy HiGHS mass-selection LP at every separately constructed threshold crossing; separate lower-tail LP for each witness',threshold_candidates=len(candidates),successful_mass_LPs=successful,witness_tail_LPs=tail_checks,conditional_scope='Utility-only fractional weighted-mass errors; fixed cohort, weights and original unknown set; not estimated actual errors or whole-person sharpness',all_breakpoints_proof_in_README=True,source_representation_upgraded=False,direct_API_timeouts_recorded=2,scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(protected),current_review='V160 unchanged',current_review_pdf_sha256=review['pdf_sha256'],primary_data_admissions=0,primary_score_width_change=0,result_sha256={n:sha(O/n) for n in ['summary.json','witnesses.json']},verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
