"""Independent threshold enumeration, tail-selection LP, and immutable-file audit."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.optimize import linprog

R = Path(__file__).resolve().parents[1]
P = Path('/data/projects/HiMCM-Overleaf')
O = R/'results/task4_v158_joint_gap'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    s = json.loads((O/'summary.json').read_text())
    for n,h in {**s['source_sha256'], **s['scientific_file_sha256']}.items():
        assert sha(R/n) == h, n
    for n,h in s['manuscript_files_unchanged_sha256'].items():
        assert sha(P/n) == h, n
    assert sha(R/'scripts/task4_v158_joint_gap.py') == s['generator_sha256']
    src=json.loads((R/'data/task4_v116_ibb/aggregate_results.json').read_text())
    q=np.array([math.exp(-float(t)/30) for t in src['duration_histogram']])
    w=np.array([x['weight'] for x in src['duration_histogram'].values()],float)
    U=src['summary']['weight_unknown']+src['optional_membership']['weight_total']
    N=w.sum()+U
    for row in s['rows']:
        a=row['alpha']
        # Convex piecewise-linear numerator reaches a minimum at a breakpoint.
        candidates=np.r_[0,q,1]
        objectives=[np.dot(w,q-z)+np.dot(w,np.maximum(z-q,0))/a for z in candidates]
        assert abs(min(objectives)/N-row['sharp_joint_lower'])<1e-12
        z=row['attaining_unknown_utility']
        qw=np.r_[q,z]; ww=np.r_[w,U]
        lp=linprog(qw,A_eq=np.ones((1,len(qw))),b_eq=[a*N],bounds=[(0,m) for m in ww],method='highs')
        assert lp.success
        low=lp.fun/(a*N); mean=np.dot(qw,ww)/N
        assert abs(low-row['witness_lower_tail'])<1e-12
        assert abs(mean-low-row['sharp_joint_lower'])<1e-12
        assert 0 < z < 1 and math.isfinite(-30*math.log(z))
    result=dict(status='pass',iteration='V158',independent_checks='All observed threshold breakpoints + 3 mass-selection LPs; analytic all-completion proof in README',
                joint_epigraph_LPs=s['successful_joint_LPs'],random_completions=s['random_completion_checks'],
                scientific_files_unchanged=len(s['scientific_file_sha256']),manuscript_files_unchanged=len(s['manuscript_files_unchanged_sha256']),
                summary_sha256=sha(O/'summary.json'),verifier_sha256=sha(Path(__file__)),
                current_data_admissions=0,current_score_width_change=0,manuscript_changed=False)
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
