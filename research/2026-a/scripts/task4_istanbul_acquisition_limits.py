"""Endpoint certificates for Istanbul-only acquisition within fixed V114 bounds."""
import hashlib
import json

import numpy as np

from task4_v114_istanbul_revision import istanbul_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, score


def run():
    lo, hi = istanbul_bounds()
    i, j = CITIES.index('Istanbul'), NAMES.index('travel')
    other = np.arange(len(CITIES)) != i
    assert lo.shape == hi.shape == (25, 10)
    assert np.array_equal([lo[i, j], hi[i, j]], [0, 1])
    original = np.stack([lo, hi]).copy()
    results = []
    for label, w in [('inherited', weights(.1)), ('equal', np.ones(10) / 10)]:
        assert np.all(w > 0) and np.isclose(w.sum(), 1)
        lower, upper = score(lo, w), score(hi, w)
        # Monotonicity: minimizing every nontravel upper endpoint gives the
        # smallest attainable Istanbul upper score while travel stays [0,1].
        limiting_upper = lo.copy()
        limiting_upper[i, j] = hi[i, j]
        minimum_upper = float(score(limiting_upper, w)[i])
        rival_max_lower = float(lower[other].max())
        # Even the most optimistic exact Istanbul realization cannot lift its
        # lower score above the original upper score. Other city bounds stay fixed.
        maximum_lower = float(upper[i])
        rival_min_upper = float(upper[other].min())
        possible_before = [CITIES[k] for k in range(len(CITIES))
                           if upper[k] >= np.max(np.delete(lower, k)) - 1e-12]
        assert len(possible_before) == 25
        assert minimum_upper > rival_max_lower
        assert maximum_lower < rival_min_upper
        # At the opposite extreme, exact worst-endpoint Istanbul can itself
        # be excluded, so 24 is attainable within the mathematical box.
        assert lower[i] < rival_max_lower
        results.append(dict(
            weight_reference=label, weights=dict(zip(NAMES, w.tolist())),
            current_istanbul_lower=float(lower[i]),
            current_istanbul_upper=float(upper[i]),
            minimum_istanbul_upper_if_travel_unresolved=minimum_upper,
            maximum_rival_lower=rival_max_lower,
            maximum_rival_lower_city=CITIES[int(np.argmax(np.where(other, lower, -np.inf)))],
            unresolved_travel_survival_margin=minimum_upper-rival_max_lower,
            maximum_istanbul_lower_under_any_legal_refinement=maximum_lower,
            minimum_rival_upper=rival_min_upper,
            minimum_rival_upper_city=CITIES[int(np.argmin(np.where(other, upper, np.inf)))],
            rival_nonexclusion_margin=rival_min_upper-maximum_lower,
            possible_champions_before=25,
            possible_champions_if_travel_stays_unresolved=25,
            minimum_possible_champion_count_with_istanbul_only_refinement=24,
            other_cities_excludable_by_istanbul_only_refinement=[]))
    np.testing.assert_array_equal(np.stack([lo, hi]), original)
    out = ROOT / 'results/task4_istanbul_acquisition_limits'
    out.mkdir(parents=True, exist_ok=True)
    result = dict(
        baseline='V114', certificate_type='monotone-score endpoint certificate; no new observation',
        scope='Fixed other-city cells, fixed V114 utility transforms, and each of two explicitly fixed weight vectors. No assertion for arbitrary or Monte Carlo weights.',
        assumptions='Independent closed utility boxes; refinements are nested within current bounds. Endpoint attainment is mathematical, not a prediction that collected data will equal an endpoint.',
        formula='C(z)=100*sqrt(sum(w*z^2))/(sqrt(sum(w*z^2))+sqrt(sum(w*(1-z)^2))). City i is possible iff upper_i >= max(lower_others).',
        proof='Positive weights make C nondecreasing in every utility. The smallest attainable upper_i with travel unresolved is C(lower_i except travel=1). The largest attainable lower_i under any refinement is C(upper_i). Compare these with unchanged rival lower and upper endpoints.',
        registry_changed=False, input_bounds_changed=False,
        input_bounds_sha256=hashlib.sha256(original.astype('<f8').tobytes()).hexdigest(),
        scenarios=results)
    (out / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    run()
