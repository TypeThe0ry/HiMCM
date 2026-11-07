"""Phoenix adverse-outcome acquisition certificates with finite residual intervals.

These hypothetical intervals never replace observed evidence. Residual width is
relative to each existing cell, and also specifies an adverse endpoint location.
"""
import itertools
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, NAMES, summarize, weights
from task4_singapore_coverage_revision import singapore_bounds
from task4_continuous_preferences import feasible_preferences


def minimum_bundles(lo, hi, city_index, residual):
    if not np.isfinite(residual) or not 0 <= residual <= 1:
        raise ValueError('Residual fraction must be in [0,1]')
    unknown = np.flatnonzero(hi[city_index] - lo[city_index] > 1e-12)
    rivals = lo[np.arange(len(lo)) != city_index]
    for size in range(len(unknown) + 1):
        found = []
        for subset in itertools.combinations(unknown, size):
            row = hi[city_index].copy()
            js = list(subset)
            row[js] = lo[city_index, js] + residual * (hi[city_index, js] - lo[city_index, js])
            if not feasible_preferences(row, rivals)['possible']:
                found.append(subset)
        if found:
            return size, found
    return None, []


def main():
    # Ties remain possible; an already dominated city needs no measurement.
    tied = np.full((3,10), .5)
    assert minimum_bundles(tied, tied, 0, .1) == (None, [])
    dominated = tied.copy(); dominated[0] = .4
    assert minimum_bundles(dominated, dominated, 0, .1) == (0, [()])
    for invalid in [-.1, 1.1, float('nan')]:
        try: minimum_bundles(tied, tied, 0, invalid)
        except ValueError: pass
        else: raise AssertionError('Invalid residual fraction accepted')
    lo, hi = singapore_bounds()
    saved = np.stack([lo, hi]).copy()
    i = CITIES.index('Phoenix')
    rows, details = [], []
    previous = 0
    for rho in [0, .01, .025, .05, .1, .2, .5, 1]:
        minimum, options = minimum_bundles(lo, hi, i, rho)
        ordered = np.inf if minimum is None else minimum
        assert ordered >= previous
        previous = ordered
        rows.append(dict(residual_fraction=rho, minimum_measurements=minimum, minimal_bundle_count=len(options)))
        for subset in options:
            details.append(dict(residual_fraction=rho, size=minimum, indicators='|'.join(NAMES[j] for j in subset)))
    # Existing exact-outcome search must be recovered at zero residual width.
    from task4_robust_acquisition import bundles
    original, _ = bundles(lo, hi)
    assert rows[0]['minimum_measurements'] == original[i]['minimum_measurements']
    assert rows[0]['minimal_bundle_count'] == original[i]['minimal_bundle_count']
    assert rows[-1]['minimum_measurements'] is None
    # Identical width at the favorable endpoint leaves the original upper bound
    # untouched, so precision alone cannot guarantee exclusion.
    assert feasible_preferences(hi[i], lo[np.arange(len(lo)) != i])['possible']
    np.testing.assert_array_equal(np.stack([lo, hi]), saved)
    rank, diagnostic = summarize(lo, hi, weights())
    reference = pd.read_csv(ROOT/'results/task4_v38_singapore/ranks.csv')
    reference = reference[reference.scenario == 'expanded_coverage_allocation']
    assert reference.city.tolist() == rank.city.tolist()
    for col in ['score_lower', 'score_upper', 'decision_rank', 'max_regret']:
        np.testing.assert_allclose(rank[col], reference[col], atol=1e-12, rtol=0)
    out = ROOT/'results/task4_v39_finite_precision'; out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'minimum_measurements.csv', index=False)
    pd.DataFrame(details).to_csv(out/'minimal_bundles.csv', index=False)
    rank.to_csv(out/'ranks.csv', index=False)
    summary = dict(baseline='V38 singapore_bounds', new_admitted_observations=0,
        possible_champions=int(rank.possible_champion.sum()), choice=[CITIES[k] for k in diagnostic['minimax_choices']],
        alpha_range=[.05,.2], city='Phoenix', input_bounds_sha256=hashlib.sha256(saved.astype('<f8').tobytes()).hexdigest(),
        interpretation='Hypothetical intervals [lo,lo+rho*(hi-lo)] require both adverse outcomes and limited residual width. Equal-width favorable intervals retain the original upper bound and cannot guarantee exclusion. Counts are distinct model criteria, not surveys or source files.',
        scenarios=rows)
    (out/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
