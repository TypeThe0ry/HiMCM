"""Independent linear-program check of V152 fractional weighted tails."""
from pathlib import Path
import hashlib
import json
import math
import numpy as np
from scipy.optimize import linprog

R = Path(__file__).resolve().parents[1]
P = Path('/data/projects/HiMCM-Overleaf')
O = R / 'results/task4_v152_tail_access'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    result = json.loads((O / 'summary.json').read_text())
    for name, digest in result['source_sha256'].items():
        assert sha(R / name) == digest
    assert sha(R / 'scripts/task4_v152_tail_access.py') == result['generator_sha256']
    assert sha(O / 'tail_bounds.csv') == result['tail_csv_sha256']
    source = json.loads((R / 'data/task4_v116_ibb/aggregate_results.json').read_text())
    minutes = np.array([float(t) for t in source['duration_histogram']])
    utilities = np.exp(-minutes / 30)
    weights = np.array([row['weight'] for row in source['duration_histogram'].values()], dtype=float)
    unknown = source['summary']['weight_unknown']
    optional = source['optional_membership']['weight_total']
    N = source['summary']['weight_total'] + optional
    assert sum(row['n'] for row in source['duration_histogram'].values()) == 1811
    assert weights.sum() == 499950
    assert unknown + optional > .2 * N
    lp_checks = 0

    def lp_tail(q, w, alpha):
        nonlocal lp_checks
        target = alpha * w.sum()
        solved = linprog(q, A_eq=np.ones((1, len(q))), b_eq=[target],
                         bounds=[(0, x) for x in w], method='highs')
        assert solved.success, solved.message
        assert abs(solved.x.sum() - target) < 1e-6
        lp_checks += 1
        return solved.fun / target

    rng = np.random.default_rng(152)
    for row in result['lower_tail_rows']:
        a = row['tail_fraction']
        for endpoint, key in [(0, 'lower_closure'), (1, 'upper_closure')]:
            actual = lp_tail(np.r_[utilities, endpoint], np.r_[weights, unknown + optional], a)
            assert math.isclose(actual, row[key], abs_tol=1e-12)
        observed = lp_tail(utilities, weights, a)
        assert math.isclose(observed, row['observed_only_tail'], abs_tol=1e-12)
        # Covers a larger aggregate relaxation than the discrete optional roster.
        # It is a diagnostic in addition to the analytic monotonicity proof.
        for included in np.linspace(0, optional, 21):
            for q_unknown in [0, .1, .5, .9, 1]:
                q = np.r_[utilities, q_unknown, q_unknown]
                w = np.r_[weights, unknown, included]
                value = lp_tail(q, w, a)
                assert row['lower_closure'] - 1e-10 <= value <= row['upper_closure'] + 1e-10
                gap = np.dot(q, w) / w.sum() - value
                assert gap + 1e-10 >= row['certified_mean_minus_tail_lower']
        for _ in range(30):
            free_weights = rng.dirichlet(np.ones(7)) * unknown
            q = np.r_[utilities, rng.uniform(0, 1, 7), rng.uniform()]
            w = np.r_[weights, free_weights, rng.uniform(0, optional)]
            value = lp_tail(q, w, a)
            assert row['lower_closure'] - 1e-10 <= value <= row['upper_closure'] + 1e-10
            assert np.dot(q, w) / w.sum() - value + 1e-10 >= row['certified_mean_minus_tail_lower']
    historical = source['historical_conditional_bounds']
    assert np.allclose(result['mean_utility_closure'], [historical['lower'], historical['upper']], atol=1e-12, rtol=0)
    baseline = json.loads((R / 'results/task4_v151_shared_entry/verification.json').read_text())
    scientific = baseline['scientific_file_sha256']
    manuscript = baseline['manuscript_files_unchanged_sha256']
    entry = json.loads((R / 'results/task4_v151_shared_entry/delivery.json').read_text())['support_file_sha256']
    for name, digest in scientific.items():
        assert sha(R / name) == digest, name
    for name, digest in {**manuscript, **entry}.items():
        assert sha(P / name) == digest, name
    audit = dict(status='pass', iteration='V152', independent_solver='SciPy HiGHS linear programming; weighted mass selection',
                 successful_linear_programs=lp_checks, seed=152,
                 source_count_and_mass_checks=True, historical_mean_reproduced=True,
                 protected_scientific_files=len(scientific), unchanged_manuscript_and_entry_files=len({**manuscript, **entry}),
                 primary_data_admissions=0, primary_score_interval_width_reduction=0,
                 source_current_year_transferred=False, sampling_confidence_interval=False,
                 gap_lower_bound_claim='conservative; joint sharpness not asserted',
                 source_sha256={str((O / name).relative_to(R)): sha(O / name) for name in ['summary.json', 'tail_bounds.csv']},
                 verifier_sha256=sha(Path(__file__)))
    (O / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
