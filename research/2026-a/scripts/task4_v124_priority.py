"""V121 user16: perfect-resolution limits for currently fully missing cells.

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
from task4_user_v121_revision import MANIFEST, revised_bounds
from task4_v5_model import NAMES, ROOT, SPEC, score, weights

OUT = ROOT / 'results/task4_v124_priority'


def independent_scores(x, w):
    """Audit the shared score through direct vector norms."""
    a = np.linalg.norm(x * np.sqrt(w), axis=1)
    b = np.linalg.norm((1 - x) * np.sqrt(w), axis=1)
    return 100 * a / (a + b)


def zurich_ptr_sensitivity(frame, lo, hi):
    """One-cell resolution of the existing unknown PTR; no new observation."""
    cities = frame.city.tolist()
    i, j = cities.index('Zurich'), NAMES.index('upper_secondary_ptr')
    assert (lo[i, j], hi[i, j]) == (0, 1)
    other = np.arange(len(cities)) != i
    rows, reports, interval_rows = [], [], []
    checked = 0
    for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10)/10)]:
        def calc(xlo, xhi):
            nonlocal checked
            assert 0 <= xlo <= xhi <= 1
            a, b = lo.copy(), hi.copy()
            a[i, j], b[i, j] = xlo, xhi
            protected = np.ones(lo.shape, bool); protected[i, j] = False
            np.testing.assert_array_equal(a[protected], lo[protected])
            np.testing.assert_array_equal(b[protected], hi[protected])
            L, U = independent_scores(a, w), independent_scores(b, w)
            d = interval_decision(score(a, w), score(b, w))
            regret = np.array([max(0., max(np.delete(U, k))-L[k]) for k in range(len(cities))])
            np.testing.assert_allclose(d['max_regret'], regret, atol=1e-12, rtol=0)
            checked += 1
            return float(regret[i]-regret[other].min()), L, U, d

        sampled_gaps = []
        for x in np.linspace(0, 1, 201):
            gap, L, U, d = calc(float(x), float(x))
            sampled_gaps.append(gap)
            choices = ';'.join(cities[k] for k in d['minimax_choices'])
            rows.append(dict(weight_reference=reference, utility=float(x),
                implied_exact_ptr=float(15*(1-x)/x) if x else np.inf,
                minimax_choices=choices, zurich_regret=float(d['max_regret'][i]),
                best_other_regret=float(d['max_regret'][other].min()),
                zurich_gap_to_best_other=gap,
                zurich_score_lower=float(L[i]), zurich_score_upper=float(U[i]),
                possible_count=int(d['possible_champion'].sum())))
        assert np.all(np.diff(sampled_gaps) <= 1e-10)
        g0, L0, U0, d0 = calc(0, 0)
        g1, _, U1, d1 = calc(1, 1)
        # Nonfocal regrets are max(q, fixed_other_upper)-fixed_lower.
        # Their pairwise differences are piecewise linear in focal upper q;
        # checking all knots proves a common best competitor for every q.
        knots = {float(U0[i]), float(U1[i])}
        for k in np.flatnonzero(other):
            knot = max(U1[t] for t in range(len(cities)) if t not in {i, int(k)})
            if U0[i] <= knot <= U1[i]:
                knots.add(float(knot))
        common_best = set(np.flatnonzero(other))
        for q in sorted(knots):
            Uq = U0.copy(); Uq[i] = q
            rq = np.array([max(0., max(np.delete(Uq, k))-L0[k]) for k in range(len(cities))])
            common_best &= {int(k) for k in np.flatnonzero(other)
                            if rq[k] <= rq[other].min()+1e-12}
        assert len(common_best) == 1
        best_other_city = cities[common_best.pop()]
        report = dict(weight_reference=reference,
            exact_observation_scope='Only Zurich PTR becomes exact; all other139 nonfullymissing and20 otherfullymissing cells remain unchanged',
            gap_at_utility0=g0, gap_at_utility1=g1,
            recommendation_at_utility0=[cities[k] for k in d0['minimax_choices']],
            recommendation_at_utility1=[cities[k] for k in d1['minimax_choices']],
            best_other_city_for_every_admissible_PTR_upper=best_other_city,
            competitor_piecewise_linear_knots_verified=sorted(knots),
            monotonic_gap='Zurich regret decreases with its lower utility; every other regret is nondecreasing with its upper utility. The gap is nonincreasing in either bound.',
            exact_ptr_switch=None)
        if g0 > 0 > g1:
            left, right = 0., 1.
            for _ in range(55):
                x = (left+right)/2
                if calc(x, x)[0] > 0:
                    left = x
                else:
                    right = x
            x = (left+right)/2
            gap, _, _, tied = calc(x, x)
            assert abs(gap) < 1e-10
            assert calc(x-1e-6, x-1e-6)[0] > 1e-10
            assert calc(x+1e-6, x+1e-6)[0] < -1e-10
            report['exact_ptr_switch'] = dict(utility_threshold=x,
                ptr_threshold=15*(1-x)/x,
                tied_choices=[cities[k] for k in tied['minimax_choices']],
                utility_below=best_other_city, utility_above='Zurich',
                ptr_above=best_other_city, ptr_below='Zurich',
                interval_sufficient_conditions='PTR upper below threshold guarantees Zurich; PTR lower above threshold guarantees Singapore. Straddling intervals need the full two-bound calculation.')
            # A straddling interval can keep Zurich because its upper score
            # still enters the competitor regrets. Record the actual boundary.
            for xlo in np.linspace(0, x, 6)[:-1]:
                assert calc(float(xlo), float(xlo))[0] > 1e-10
                assert calc(float(xlo), 1.)[0] < -1e-10
                left, right = float(xlo), 1.
                for _ in range(55):
                    mid = (left+right)/2
                    if calc(float(xlo), mid)[0] > 0:
                        left = mid
                    else:
                        right = mid
                xhi = (left+right)/2
                g, _, _, d = calc(float(xlo), xhi)
                assert abs(g) < 1e-10
                interval_rows.append(dict(weight_reference=reference,
                    utility_lower=float(xlo), utility_upper_tie_threshold=xhi,
                    ptr_lower_at_threshold=15*(1-xhi)/xhi,
                    ptr_upper_at_threshold=15*(1-xlo)/xlo if xlo else np.inf,
                    minimax_choices_at_threshold=';'.join(cities[k] for k in d['minimax_choices']),
                    rule='At fixed utility lower, upper below threshold favors Singapore; above favors Zurich. All other bounds unchanged.'))
        else:
            assert g0 < 0 and g1 < 0
            report['all_admissible_PTR_intervals'] = 'Zurich remains strict minimax for every 0<=utility_lower<=utility_upper<=1, by monotonicity and the all-low maximum gap.'
        # Independent rectangle probes include broad, narrow and straddling intervals.
        interval_choices = set()
        for xlo in np.linspace(0, 1, 11):
            for xhi in np.linspace(xlo, 1, 11):
                _, _, _, d = calc(float(xlo), float(xhi))
                interval_choices.update(cities[k] for k in d['minimax_choices'])
        report['choices_in_121_interval_probes'] = sorted(interval_choices)
        reports.append(report)
    return rows, reports, interval_rows, checked


def missing_ptr_recommendation_thresholds(frame, lo, hi):
    """Exact-cell hypothetical thresholds for decision relevance, not exclusion."""
    cities = frame.city.tolist()
    j = NAMES.index('upper_secondary_ptr')
    records, checked = [], 0
    for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10)/10)]:
        for i, city in enumerate(cities):
            if (lo[i, j], hi[i, j]) != (0, 1):
                continue
            other = np.arange(len(cities)) != i
            def calc(x):
                nonlocal checked
                a, b = lo.copy(), hi.copy(); a[i, j] = b[i, j] = x
                L, U = independent_scores(a, w), independent_scores(b, w)
                r = np.array([max(0., max(np.delete(U, k))-L[k]) for k in range(len(cities))])
                d = interval_decision(score(a, w), score(b, w))
                np.testing.assert_allclose(d['max_regret'], r, atol=1e-12, rtol=0)
                checked += 1
                return float(r[i]-r[other].min()), d
            g0, d0 = calc(0); g1, d1 = calc(1); g15, d15 = calc(.5)
            record = dict(weight_reference=reference, city=city,
                gap_at_utility0=g0, gap_at_utility1=g1,
                assumed_PTR15_minimax_choices=';'.join(cities[k] for k in d15['minimax_choices']),
                assumed_PTR15_focal_gap=g15,
                exact_utility_threshold=np.nan, exact_PTR_threshold=np.nan,
                interpretation='Hypothetical exact matched-school PTR; only this currently fully missing cell changes')
            if g0 > 0 > g1:
                left, right = 0., 1.
                for _ in range(55):
                    x = (left+right)/2
                    if calc(x)[0] > 0:
                        left = x
                    else:
                        right = x
                x = (left+right)/2; gap, d = calc(x)
                assert abs(gap) < 1e-10
                assert calc(x-1e-6)[0] > 1e-10 and calc(x+1e-6)[0] < -1e-10
                record.update(status='focal_recommendation_switch', exact_utility_threshold=x,
                    exact_PTR_threshold=15*(1-x)/x,
                    tied_choices=';'.join(cities[k] for k in d['minimax_choices']),
                    strict_rule='Exact PTR below threshold favors focal city; above threshold focal city is not minimax')
            elif g0 < 0 and g1 < 0:
                record.update(status='focal_remains_strict_minimax_for_all_exact_PTR',
                              tied_choices='', strict_rule='No switch within utility[0,1]')
            else:
                assert g0 > 0 and g1 > 0
                record.update(status='focal_never_minimax_for_any_exact_PTR',
                              tied_choices='', strict_rule='No switch within utility[0,1]')
            records.append(record)
    return records, checked


def main():
    protected_paths = [SOURCE, MANIFEST,
                       ROOT / 'design/task4_user_v118_admissions.json',
                       ROOT / 'design/task4_user_v120_admissions.json',
                       ROOT / 'scripts/task4_user_v121_revision.py',
                       ROOT / 'results/task4_user_v121_revision/current_ranks.csv',
                       ROOT / 'results/task4_user_v121_revision/utility_bounds.csv']
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in protected_paths}
    registry = ROOT / 'design/task4_user_current_model.json'
    registry_before = hashlib.sha256(registry.read_bytes()).hexdigest()
    frame, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    n = len(cities)
    assert n == 16 and lo.shape == (16, 10)
    missing = (lo == 0) & (hi == 1)
    assert missing.sum() == 21 and (hi > lo).sum() == 48
    endpoints, subsets, singles, joints, thresholds, bases = [], [], [], [], [], []
    references = []
    audited_cases = 0
    rng = np.random.default_rng(20261108)

    for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        L, U = score(lo, w), score(hi, w)
        base = interval_decision(L, U)
        assert base['possible_champion'].all()
        saved = pd.read_csv(ROOT/'results/task4_user_v121_revision/current_ranks.csv')
        saved = saved[(saved.weight_reference == ref) & (saved.scenario == 'after_conditional')].set_index('city').loc[cities]
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

    ptr_rows, ptr_reports, interval_rows, ptr_checks = zurich_ptr_sensitivity(frame, lo, hi)
    ptr_switches, ptr_switch_checks = missing_ptr_recommendation_thresholds(frame, lo, hi)
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
    pd.DataFrame(ptr_rows).to_csv(OUT/'zurich_ptr_exact_grid.csv', index=False)
    pd.DataFrame(interval_rows).to_csv(OUT/'zurich_ptr_interval_boundary.csv', index=False)
    pd.DataFrame(ptr_switches).to_csv(OUT/'ptr_recommendation_thresholds.csv', index=False)
    summary = dict(base='V121 user16', baseline_minimax='Zurich',
                   baseline_possible_count=16, fully_missing_cells=int(missing.sum()),
                   baseline_references=references,
                   unresolved_cells=int((hi > lo).sum()),
                   scope='Acquisition limits only; no new observation, modified weight or CSV value',
                   uncertain_partial_cells_not_resolved=int(((hi > lo) & ~missing).sum()),
                   endpoint_sufficiency='Only one city changes; its own exclusion cannot coexist with exclusion of a baseline-possible competitor. All-low and all-high corners maximize the two types respectively.',
                   joint_threshold_scope='Common-coordinate sufficient thresholds, not necessary thresholds for arbitrary joint evidence; strict separation needed, ties remain possible.',
                   independent_score_regret_cases=audited_cases,
                   zurich_PTR_conditioning=ptr_reports,
                   independent_zurich_PTR_cases=ptr_checks,
                   independent_other_PTR_threshold_cases=ptr_switch_checks,
                   all_nonmissing_bounds_preserved=True,
                   input_sha256={str(p.relative_to(ROOT)): digest for p, digest in protected.items()})
    for p, digest in protected.items():
        assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
    assert hashlib.sha256(registry.read_bytes()).hexdigest() == registry_before
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass',
        baseline_V121_scores_and_regrets_match=True, fully_missing_cells=21,
        protected_nonfullymissing_cells=139, existing_partial_intervals_preserved=27,
        weights_anchors_and_self_exclusion_unchanged=True,
        independent_norm_regret_cases=audited_cases,
        independent_zurich_PTR_cases=ptr_checks,
        independent_all_PTR_threshold_cases=ptr_switch_checks,
        all_point_and_nonfullymissing_cells_exactly_preserved=True,
        source_hashes_and_current_registry_unchanged=True), indent=2)+'\n')
    print(json.dumps(summary, indent=2))
    print(pd.DataFrame(joints).sort_values(sort, ascending=ascending).to_string(index=False))


if __name__ == '__main__':
    main()
