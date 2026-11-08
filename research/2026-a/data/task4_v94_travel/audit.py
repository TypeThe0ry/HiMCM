"""Conditional sample subgroup bounds from explicitly marked reader transcription."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
P=Path(__file__).resolve().parent
sys.path.insert(0,str(P.parents[1]/'scripts'))
from task4_subgroup_bounds import subgroup_bounds

def main():
 m=json.loads((P/'manifest.json').read_text())
 assert hashlib.sha256((P/'reader_transcription.json').read_bytes()).hexdigest()==m['transcription_sha256']
 assert hashlib.sha256((P/m['reused_solver']).resolve().read_bytes()).hexdigest()==m['reused_solver_sha256']
 for f in m['files']:
  b=(P/f['file']).read_bytes();assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
 t=json.loads((P/'reader_transcription.json').read_text())
 counts=np.array(t['time_bin_counts']);assert counts.sum()==sum(t['school_type_counts'].values())==573
 n=t['school_type_counts']['SMA']+t['school_type_counts']['SMK'];assert n==262
 low=np.exp(-np.array([float('inf') if x is None else x for x in t['conservative_time_upper']])/30)
 high=np.exp(-np.array(t['conservative_time_lower'])/30)
 bound=subgroup_bounds(counts,low,high,[n,n])
 # Independent linear-programming extremizers and explicit integer allocations.
 a=linprog(low,A_eq=[np.ones(6)],b_eq=[n],bounds=list(zip(np.zeros(6),counts)),method='highs')
 b=linprog(-high,A_eq=[np.ones(6)],b_eq=[n],bounds=list(zip(np.zeros(6),counts)),method='highs')
 assert a.success and b.success
 allocation_lower=np.array([0,0,207,40,13,2]);allocation_upper=np.array([25,237,0,0,0,0])
 assert allocation_lower.sum()==allocation_upper.sum()==n
 assert np.all(allocation_lower<=counts) and np.all(allocation_upper<=counts)
 np.testing.assert_allclose(bound,[a.fun/n,-b.fun/n],rtol=0,atol=1e-12)
 np.testing.assert_allclose(bound,[allocation_lower@low/n,allocation_upper@high/n],rtol=0,atol=1e-12)
 output=dict(main_admitted=False,source_original_histogram_bytes_acquired=False,parent_sample=573,upper_secondary_school_type_subgroup=262,conservative_bin_closures_minutes=list(zip(t['conservative_time_lower'],t['conservative_time_upper'])),parent_histogram_utility_bounds=[float(counts@low/573),float(counts@high/573)],subgroup_utility_bounds=list(bound),lower_allocation=allocation_lower.tolist(),upper_allocation=allocation_upper.tolist(),lp_and_explicit_allocation_checks=True,scope='Unweighted valid respondent subgroup at SMA/SMK schools; conditional on reader-transcribed marginals, not actual school-type-by-time observations, age14-18 or DKI Jakarta city inference')
 (P/'summary.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output,indent=2))
if __name__=='__main__':main()
