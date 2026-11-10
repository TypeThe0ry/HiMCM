"""Independent LP audit of the reduced historical tail-gap certificate."""
import csv
import hashlib
import json
import math
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_audit_output import audit_parser,check_output,emit_report

R=Path(__file__).resolve().parents[1];G=R.parents[1]
O=R/'results/current_tail_endpoint_review'


def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open() as f:return list(csv.DictReader(f))


def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G)
    protection=protected_inputs()
    source=R/'data/task4_v116_ibb/aggregate_results.json';s=read(source)
    old=read(R/'results/task4_v162_tail_error/summary.json');current=read(O/'summary.json')
    durations=list(s['duration_histogram'])
    q=np.array([math.exp(-float(t)/30) for t in durations])
    w=np.array([s['duration_histogram'][t]['weight'] for t in durations],float)
    W=float(w.sum());N=W+s['summary']['weight_unknown']+s['optional_membership']['weight_total']
    assert len(q)==49 and (W,N)==(499950,681503)
    thresholds=sorted({0.,1.,*q});assert len(thresholds)==51
    saved=rows(O/'endpoint_values.csv');assert len(saved)==357
    table={(int(r['case']),float(r['threshold_utility'])):float(r['gap']) for r in saved}
    assert len(table)==357
    allocations=rows(O/'witnesses.csv');assert len(allocations)==343
    alpha=.2;maximum_difference=maximum_mass_residual=maximum_bound_violation=0.
    checks=[];tail_error=0.;lp_count=0
    for case,(old_row,new_row) in enumerate(zip(old['rows'],current['rows'])):
        assert new_row['case']==case
        delta=Fraction(new_row['delta_exact']);retained=float((1-delta)*int(W))
        assert abs(float(delta)-old_row['observed_weight_error_fraction'])<1e-15
        saved_case=sorted((z,v) for (j,z),v in table.items() if j==case)
        np.testing.assert_allclose([z for z,v in saved_case],thresholds,atol=2e-16,rtol=0)
        best=math.inf
        for z,(_,saved_gap) in zip(thresholds,saved_case):
            costs=q-z+np.maximum(z-q,0)/alpha
            lp=linprog(costs,A_eq=np.ones((1,len(q))),b_eq=[retained],
                       bounds=[(0,float(v)) for v in w],method='highs')
            assert lp.success,lp.message;lp_count+=1
            maximum_mass_residual=max(maximum_mass_residual,abs(lp.x.sum()-retained))
            maximum_bound_violation=max(maximum_bound_violation,float(np.max(-lp.x)),float(np.max(lp.x-w)))
            gap=float(lp.fun/N);best=min(best,gap)
            maximum_difference=max(maximum_difference,abs(gap-saved_gap))
        assert abs(best-float(new_row['sharp_gap']))<1e-10
        assert abs(best-old_row['sharp_gap_in_fractional_mass_set'])<1e-10
        # Check the NEW witness, including its actual lowest-alpha tail by LP.
        wt={str(x['original_minutes']):x for x in allocations if int(x['case'])==case}
        assert set(wt)==set(durations)
        kept=np.array([float(wt[t]['kept_weight']) for t in durations])
        edited=np.array([float(wt[t]['edited_weight']) for t in durations])
        np.testing.assert_allclose(kept+edited,w,atol=1e-9,rtol=0)
        assert np.all(kept>=0) and np.all(edited>=0)
        assert abs(kept.sum()-retained)<1e-7
        z=math.exp(-new_row['attaining_minutes']/30)
        free=edited.sum()+s['summary']['weight_unknown']+s['optional_membership']['weight_total']
        utilities=np.r_[q,z];masses=np.r_[kept,free]
        assert abs(masses.sum()-N)<1e-7
        tail=linprog(utilities,A_eq=np.ones((1,len(masses))),b_eq=[alpha*N],
                     bounds=[(0,float(v)) for v in masses],method='highs')
        assert tail.success
        mean=float(utilities@masses/N);low=float(tail.fun/(alpha*N))
        errors=[abs(mean-float(new_row['witness_mean'])),abs(low-float(new_row['witness_lower_tail'])),
                abs(mean-low-float(new_row['sharp_gap']))]
        tail_error=max(tail_error,*errors)
        checks.append(dict(case=case,delta=float(delta),LP_minimum=best,
                           difference_from_frozen=best-old_row['sharp_gap_in_fractional_mass_set']))
    assert lp_count==357 and len(checks)==7
    assert maximum_difference<1e-10 and maximum_mass_residual<1e-6
    assert maximum_bound_violation<1e-7 and tail_error<1e-10
    assert Fraction(current['exact_zero_gap_budget'])==Fraction(int(W)-int(w.max()),int(W))
    assert float(current['rows'][-1]['sharp_gap'])==0
    with tempfile.TemporaryDirectory(prefix='himcm-tail-replay-',dir='/data/scratch') as tmp:
        dest=Path(tmp)/'replay'
        subprocess.run([sys.executable,str(R/'scripts/task4_current_tail_endpoints.py'),
                        '--output-dir',str(dest)],check=True,stdout=subprocess.PIPE)
        for name in ['summary.json','endpoint_values.csv','witnesses.csv']:
            assert (O/name).read_bytes()==(dest/name).read_bytes()
    assert protected_inputs()==protection
    paper=read(R/'results/current_paper_review/current_verification.json')
    for n,h in paper['edition_source_sha256'].items():assert sha(R/n)==h
    sources=[source,R/'results/task4_v158_joint_gap/summary.json',
             R/'results/task4_v162_tail_error/summary.json',R/'results/task4_v162_tail_error/witnesses.json',
             R/'results/task4_v162_tail_error/verification.json',O/'summary.json',O/'endpoint_values.csv',
             O/'witnesses.csv',O/'README.md',O/'peer_review.json',Path(__file__),
             R/'scripts/task4_current_tail_endpoints.py',R/'scripts/audit_current_oslo_cost_ptr_sources.py',
             R/'scripts/task4_audit_output.py']
    report=dict(status='pass reduced-endpoint certificate audit',**protection,
        edition_entries_checked=24,thresholds=51,budget_cases=7,successful_mass_LPs=lp_count,
        new_witness_tail_LPs=7,maximum_endpoint_objective_difference=maximum_difference,
        maximum_mass_equality_residual=maximum_mass_residual,
        maximum_bound_violation=maximum_bound_violation,maximum_new_witness_error=tail_error,
        comparisons=checks,output_files_bytewise_reproduced=3,
        proof_scope='Fixed fractional utility-mass edits; concavity between observed knots; alpha1/5',
        source_representation_upgraded=False,error_rates_estimated=False,
        primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,
        changes_manuscript=False,MC_replayed=False,TeX_replayed=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in sources})
    emit_report(report,a,canonical,G)


if __name__=='__main__':main()
