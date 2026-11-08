"""Keep unknown test-record mass explicit in Phoenix published-rate descriptors.

Gamma is a hypothetical share, not inferred from the fraction of missing rows.
The linear programs independently optimize all school-record weights/outcomes
under the stated nonnegative continuous-mass relaxation. No city admission.
"""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    sources = json.loads((HERE / 'inputs.json').read_text())
    frames = []
    for name, digest in sources.items():
        path = ROOT / name
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
        frames.append(pd.read_csv(path, dtype={'nces_id': str}))
    data = pd.concat(frames, ignore_index=True)
    assert len(data) == 319 and not data.duplicated(['nces_id', 'subject']).any()
    assert (data.fiscalYear == 2025).all() and (data.grade == 11).all()
    scenarios, subjects = [], []
    maximum_lp_error = 0.0
    for subject, group in data.groupby('subject'):
        n = group.numberTested.to_numpy(float)
        p = group.percentagePassed.to_numpy(float)
        known_n = np.isfinite(n) & (n >= 0)
        known_p = np.isfinite(p) & (p >= 0)
        assert ((p[known_p] >= 0) & (p[known_p] <= 100)).all()
        lower = np.where(known_p, p / 100, 0)
        upper = np.where(known_p, p / 100, 1)
        total = n[known_n].sum()
        a = np.dot(n[known_n], lower[known_n]) / total
        b = np.dot(n[known_n], upper[known_n]) / total
        missing_low, missing_high = lower[~known_n].min(), upper[~known_n].max()
        subjects.append(dict(subject=subject, school_subject_records=len(group),
            known_test_records=float(total), unknown_count_rows=int((~known_n).sum()),
            unknown_count_but_published_rate_rows=int((~known_n & known_p).sum()),
            known_mass_lower=float(a), known_mass_upper=float(b),
            unknown_mass_rate_lower=float(missing_low), unknown_mass_rate_upper=float(missing_high),
            unidentified_mass_closure_lower=float(min(a, missing_low)),
            unidentified_mass_closure_upper=float(max(b, missing_high))))
        # gamma=1 is the closure as missing mass grows without a finite cap.
        # Published known counts remain positive, so this endpoint is a limit.
        for gamma in [0, .01, .05, .10, .20, .50]:
            fixed_weights = (1-gamma) * n[known_n] / total
            bounds = [(float(w), float(w)) for w in fixed_weights]
            bounds += [(0, float(gamma))] * int((~known_n).sum())
            order = np.r_[np.flatnonzero(known_n), np.flatnonzero(~known_n)]
            low_lp = linprog(lower[order], A_eq=np.ones((1, len(group))), b_eq=[1],
                             bounds=bounds, method='highs')
            high_lp = linprog(-upper[order], A_eq=np.ones((1, len(group))), b_eq=[1],
                              bounds=bounds, method='highs')
            assert low_lp.success and high_lp.success
            lo = (1-gamma)*a + gamma*missing_low
            hi = (1-gamma)*b + gamma*missing_high
            error = max(abs(low_lp.fun-lo), abs(-high_lp.fun-hi))
            maximum_lp_error = max(maximum_lp_error, error)
            assert error < 1e-10
            scenarios.append(dict(subject=subject, hypothetical_unknown_mass_share=gamma,
                descriptor_lower_percent=100*lo, descriptor_upper_percent=100*hi,
                scenario_only=True))
    pd.DataFrame(scenarios).to_csv(HERE / 'scenarios.csv', index=False)
    result = dict(main_admitted=False, observed_city_cells_changed=0,
        subjects=subjects, scenarios=len(scenarios), independent_school_weight_lp_checks=2*len(scenarios),
        maximum_lp_error=maximum_lp_error,
        interpretation='Published-percentage weighted descriptor, not reconstructed pass rates. '
        'Unknown tested mass remains unidentified; nonnegative continuous weights allow conservative '
        'zero allocations. Gamma zero and one can be closure limits, not observed mass claims. '
        'No private/uncovered/resident population extrapolation or international test calibration.')
    (HERE / 'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
