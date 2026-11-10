"""Bound the decision value of two transit lower-bound acquisitions, offline."""
from pathlib import Path
import hashlib
import itertools
import json
import math
import numpy as np
import pandas as pd
from task4_user_v204_revision import revised_bounds
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import NAMES, weights

R = Path(__file__).resolve().parents[1]
O = R / 'results/current_two_city_transit_ceiling'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def scalar_scores(a, w):
    rows = []
    for row in a:
        positive = math.sqrt(sum(float(v) * float(x)**2 for v, x in zip(w, row)))
        negative = math.sqrt(sum(float(v) * (1-float(x))**2 for v, x in zip(w, row)))
        rows.append(100 * positive / (positive + negative))
    return np.array(rows)


def main():
    if O.exists():
        raise ValueError('Output already exists; preserve the previous certificate')
    frame, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    targets = ['Helsinki', 'Dublin']
    ii = [cities.index(c) for c in targets]
    j = NAMES.index('public_transport_density')
    assert all(hi[i, j] == 1 for i in ii)
    source_paths = [SOURCE, Path(__file__), R/'design/task4_user_v204_snapshot.json']
    # Pin every imported local model implementation, including upstream factories.
    import sys
    source_paths += [Path(m.__file__).resolve() for m in list(sys.modules.values())
                     if getattr(m, '__file__', None)
                     and Path(m.__file__).resolve().parent == R/'scripts']
    sources = {str(p.relative_to(R)): sha(p) for p in sorted(set(source_paths))}
    rows, checks = [], []
    for ref, w in [('fixed', weights(.1)), ('equal', np.full(10, .1))]:
        base = evaluate(cities, lo, hi, w)
        choice = base.loc[base.decision_rank.eq(1), 'city'].tolist()
        assert len(choice) == 1 and choice[0] not in targets
        for selected in itertools.product([False, True], repeat=2):
            a = lo.copy()
            for i, use in zip(ii, selected):
                if use:
                    a[i, j] = 1
            result = evaluate(cities, a, hi, w)
            lower, upper = scalar_scores(a, w), scalar_scores(hi, w)
            regrets = np.array([max(0., max(upper[k]-lower[i] for k in range(16) if k != i))
                                for i in range(16)])
            possible = np.array([lower[np.arange(16) != i].max() <= upper[i]
                                 for i in range(16)])
            np.testing.assert_allclose(result.score_lower, lower, atol=1e-12, rtol=0)
            np.testing.assert_allclose(result.score_upper, upper, atol=1e-12, rtol=0)
            np.testing.assert_allclose(result.max_regret, regrets, atol=1e-12, rtol=0)
            np.testing.assert_array_equal(result.possible_champion, possible)
            assert result.loc[result.decision_rank.eq(1), 'city'].tolist() == choice
            assert possible.all() and not result.necessary_champion.any()
            label = '+'.join(c for c, use in zip(targets, selected) if use) or 'retained'
            rows.append(result.assign(scenario=label, weight_reference=ref))
            winner = cities.index(choice[0])
            checks.append(dict(weight_reference=ref, scenario=label,
                recommendation=choice, possible_champions=int(possible.sum()),
                necessary_champions=int(result.necessary_champion.sum()),
                mean_width=float((upper-lower).mean()),
                minimax_regret=float(regrets[winner]),
                strict_choice_margin=float(np.delete(regrets, winner).min()-regrets[winner])))
        # U is fixed; an altered city's regret decreases with its own L only.
        # Other cities' regrets remain constant. At both lower bounds = 1 the
        # retained choice is still strictly best, hence so throughout the box.
    pd.testing.assert_frame_equal(frame, revised_bounds()[0])
    np.testing.assert_array_equal(lo, revised_bounds()[1])
    np.testing.assert_array_equal(hi, revised_bounds()[2])
    assert all(sha(R/p) == h for p, h in sources.items())
    O.mkdir(parents=True)
    pd.concat(rows, ignore_index=True).to_csv(O/'city_cases.csv', index=False)
    report = dict(status='pass bounded acquisition ceiling', primary_model='V204 unchanged',
        targets=targets, indicator=NAMES[j], checks=checks,
        source_sha256=sources, output_sha256={'city_cases.csv':sha(O/'city_cases.csv')},
        scalar_city_cases=128, primary_admissions=0, actual_primary_width_reduction=0,
        changes_primary_model=False, changes_manuscript=False,
        scope='Hypothetical lower-bound refinements only; all upper bounds and other cells fixed. '
              'The utility-one endpoint is a relaxation, not a finite stop count or observed evidence. '
              'Endpoint monotonicity certifies unchanged strict conservative choices and 16 possible/0 necessary '
              'throughout the two-coordinate lower-bound box. It does not certify full rankings, '
              'other data/weight changes, or absence of value for narrowing individual city scores.')
    (O/'verification.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status':report['status'], 'checks':checks}, indent=2))


if __name__ == '__main__':
    main()
