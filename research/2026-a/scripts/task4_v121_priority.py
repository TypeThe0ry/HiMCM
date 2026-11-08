"""V120 user16: perfect-resolution limits for currently fully missing cells.

Joint acquisition changes one city's missing cells only. These deterministic
limits do not predict the measurements that a real source will supply.
"""
import hashlib
from itertools import combinations
import json

import numpy as np
import pandas as pd

from task4_interval_decision import interval_decision
from task4_user_city_indicators import SOURCE
from task4_user_v120_revision import MANIFEST, revised_bounds
from task4_v5_model import NAMES, ROOT, SPEC, score, weights

OUT = ROOT / 'results/task4_v121_priority'


def independent_scores(x, w):
    """Audit the shared score through direct vector norms."""
    a = np.linalg.norm(x * np.sqrt(w), axis=1)
    b = np.linalg.norm((1 - x) * np.sqrt(w), axis=1)
    return 100 * a / (a + b)


def main():
    protected_paths = [SOURCE, MANIFEST,
                       ROOT / 'design/task4_user_v118_admissions.json',
                       ROOT / 'scripts/task4_user_v120_revision.py']
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in protected_paths}
    registry = ROOT / 'design/task4_user_current_model.json'
    registry_before = hashlib.sha256(registry.read_bytes()).hexdigest()
    frame, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    n = len(cities)
    assert n == 16 and lo.shape == (16, 10)
    missing = (lo == 0) & (hi == 1)
    assert missing.sum() == 26
    endpoints, subsets, singles, joints, thresholds, bases = [], [], [], [], [], []
    references = []
    audited_cases = 0
    rng = np.random.default_rng(20261108)

    for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        L, U = score(lo, w), score(hi, w)
        base = interval_decision(L, U)
        assert base['possible_champion'].all()
        saved = pd.read_csv(ROOT/'results/task4_user_v120_revision/current_ranks.csv')
        saved = saved[saved.weight_reference == ref].set_index('city').loc[cities]
        for column, values in [('score_lower', L), ('score_upper', U),
                               ('max_regret', base['max_regret'])]:
            np.testing.assert_allclose(saved[column], values, atol=1e-12, rtol=0)
        references.append(dict(weight_reference=ref,
                               mean_score_width=float(np.mean(U-L)),
                               possible_count=int(base['possible_champion'].sum()),
                               minimax_choices=[cities[k] for k in base['minimax_choices']]))
        for i, city in enumerate(cities):
            bases.append(dict(weight_reference=ref, city=city,
                              score_lower=L[i], score_upper=U[i],
                              max_regret=base['max_regret'][i],
                              decision_rank=int(1 + np.sum(base['max_regret'] < base['max_regret'][i])),
                              possible_champion=bool(base['possible_champion'][i]),
                              full_missing_count=int(missing[i].sum())))
            js = np.flatnonzero(missing[i]).tolist()
            if not js:
                continue

            def evaluate(indices, values):
                nonlocal audited_cases
                a, b = lo.copy(), hi.copy()
                a[i, indices] = b[i, indices] = values
                np.testing.assert_array_equal(a[~missing], lo[~missing])
                np.testing.assert_array_equal(b[~missing], hi[~missing])
                l, u = score(a, w), score(b, w)
                other = np.arange(n) != i
                np.testing.assert_array_equal(l[other], L[other])
                np.testing.assert_array_equal(u[other], U[other])
                np.testing.assert_allclose(l, independent_scores(a, w), atol=1e-12, rtol=0)
                np.testing.assert_allclose(u, independent_scores(b, w), atol=1e-12, rtol=0)
                d = interval_decision(l, u)
                independent_regret = [max(0., max(np.delete(u, k)) - l[k])
                                      for k in range(n)]
                np.testing.assert_allclose(d['max_regret'], independent_regret,
                                           atol=1e-12, rtol=0)
                audited_cases += 1
                return l, u, d

            for size in range(1, len(js) + 1):
                for group in combinations(js, size):
                    indices = list(group)
                    label = ';'.join(NAMES[j] for j in group)
                    candidates = []
                    for end, x in [('lower', 0.), ('upper', 1.)]:
                        l, u, d = evaluate(indices, x)
                        excluded = [cities[k] for k in range(n)
                                    if not d['possible_champion'][k]]
                        row = dict(weight_reference=ref, city=city,
                                   indicators=label, cell_count=size,
                                   endpoint=end, resolved_utility=x,
                                   possible_count=n-len(excluded),
                                   excluded_count=len(excluded),
                                   excluded_cities=';'.join(excluded),
                                   score_lower_before=L[i], score_upper_before=U[i],
                                   score_lower_after=l[i], score_upper_after=u[i],
                                   focal_decision_rank=int(1 + np.sum(d['max_regret'] < d['max_regret'][i])),
                                   minimax_choices=';'.join(cities[k] for k in d['minimax_choices']))
                        endpoints.append(row)
                        candidates.append(row)
                    low, high = candidates
                    limit = max(low['excluded_count'], high['excluded_count'])
                    # All baseline cities are possible. Own exclusion and
                    # exclusion of a competitor cannot coexist. The all-low
                    # and all-high corners therefore bound every interior
                    # resolution, including unequal coordinates.
                    for values in rng.uniform(0, 1, (12, size)):
                        assert n - evaluate(indices, values)[2]['possible_champion'].sum() <= limit
                    row = dict(weight_reference=ref, city=city, indicators=label,
                               cell_count=size, optimistic_exclusions=limit,
                               high_endpoint_exclusions=high['excluded_count'],
                               low_endpoint_exclusions=low['excluded_count'],
                               high_endpoint_excluded_cities=high['excluded_cities'],
                               low_endpoint_excluded_cities=low['excluded_cities'],
                               high_endpoint_city_lower=high['score_lower_after'],
                               low_endpoint_city_upper=low['score_upper_after'],
                               high_endpoint_decision_rank=high['focal_decision_rank'],
                               low_endpoint_decision_rank=low['focal_decision_rank'],
                               baseline_city_upper=U[i],
                               lower_score_gain=high['score_lower_after']-L[i],
                               upper_score_reduction=U[i]-low['score_upper_after'])
                    subsets.append(row)
                    if size == 1:
                        singles.append(dict(row, indicator=NAMES[group[0]]))
                    if size == len(js):
                        joints.append(row)

                    # Joint thresholds follow the common-utility diagonal.
                    # They are sufficient for all selected lower bounds above
                    # x (or upper bounds below x), not necessary multivariate
                    # conditions. For one cell the threshold is exact.
                    targets = [(k, U[k], 'lower_above') for k in range(n)
                               if k != i and high['score_lower_after'] > U[k]+1e-12]
                    if low['excluded_count']:
                        targets.append((i, max(np.delete(L, i)), 'upper_below'))
                    for k, target, direction in targets:
                        left, right = 0., 1.
                        for _ in range(50):
                            mid = (left+right)/2
                            a, b, _ = evaluate(indices, mid)
                            y = a[i] if direction == 'lower_above' else b[i]
                            if y < target:
                                left = mid
                            else:
                                right = mid
                        x = (left+right)/2
                        a, b, _ = evaluate(indices, x)
                        y = a[i] if direction == 'lower_above' else b[i]
                        assert abs(y-target) < 1e-10
                        record = dict(weight_reference=ref, source_city=city,
                                      indicators=label, cell_count=size,
                                      excluded_city=cities[k], direction=direction,
                                      common_utility_threshold=x,
                                      score_at_threshold=y, target_score=target,
                                      interpretation='Exact single-cell threshold' if size == 1 else
                                      'Sufficient common-coordinate threshold; not necessary for unequal joint evidence',
                                      strict_requirement='Every selected lower utility strictly above threshold' if direction == 'lower_above' else
                                      'Every selected upper utility strictly below threshold')
                        if size == 1:
                            j = group[0]
                            if NAMES[j] == 'travel':
                                if direction == 'lower_above':
                                    record['sufficient_matched_mean_minutes_below'] = -30*np.log(x)
                            else:
                                _, benefit, anchor, _ = SPEC[j]
                                record['raw_threshold'] = anchor*x/(1-x) if benefit else anchor*(1-x)/x
                                record['raw_requirement'] = ('above' if benefit else 'below') if direction == 'lower_above' else ('below' if benefit else 'above')
                        thresholds.append(record)

    OUT.mkdir(parents=True, exist_ok=True)
    sort = ['weight_reference', 'optimistic_exclusions', 'high_endpoint_city_lower', 'city']
    ascending = [True, False, False, True]
    for name, rows in [('joint_priority', joints), ('subset_limits', subsets),
                       ('single_cell_priority', singles)]:
        pd.DataFrame(rows).sort_values(sort, ascending=ascending).to_csv(OUT/f'{name}.csv', index=False)
    pd.DataFrame(endpoints).to_csv(OUT/'endpoint_limits.csv', index=False)
    pd.DataFrame(thresholds).to_csv(OUT/'exclusion_thresholds.csv', index=False)
    pd.DataFrame(bases).to_csv(OUT/'baseline.csv', index=False)
    pd.DataFrame([dict(city=cities[i], indicator=NAMES[j])
                  for i, j in zip(*np.where(missing))]).to_csv(OUT/'missing_cells.csv', index=False)
    summary = dict(base='V120 user16', baseline_minimax='Zurich',
                   baseline_possible_count=16, fully_missing_cells=int(missing.sum()),
                   baseline_references=references,
                   unresolved_cells=int((hi > lo).sum()),
                   scope='Acquisition limits only; no new observation, modified weight or CSV value',
                   uncertain_partial_cells_not_resolved=int(((hi > lo) & ~missing).sum()),
                   endpoint_sufficiency='Only one city changes; its own exclusion cannot coexist with exclusion of a baseline-possible competitor. All-low and all-high corners maximize the two types respectively.',
                   joint_threshold_scope='Common-coordinate sufficient thresholds, not necessary thresholds for arbitrary joint evidence; strict separation needed, ties remain possible.',
                   independent_score_regret_cases=audited_cases,
                   all_nonmissing_bounds_preserved=True,
                   input_sha256={str(p.relative_to(ROOT)): digest for p, digest in protected.items()})
    for p, digest in protected.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
    assert hashlib.sha256(registry.read_bytes()).hexdigest() == registry_before
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    print(pd.DataFrame(joints).sort_values(sort, ascending=ascending).to_string(index=False))


if __name__ == '__main__':
    main()
