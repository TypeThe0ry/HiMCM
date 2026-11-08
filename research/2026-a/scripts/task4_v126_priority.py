"""V124 user16 acquisition limits for its 19 completely missing utility cells.

Information values condition on exact utility resolution, not on a probability
distribution or on actually obtaining a complete, correctly scoped source.
"""
import hashlib
from itertools import combinations
import json

import numpy as np
import pandas as pd

from task4_interval_decision import interval_decision, voi_1d
from task4_user_city_indicators import SOURCE
from task4_user_v124_revision import MANIFEST, revised_bounds
from task4_v124_priority import independent_scores
from task4_v5_model import ROOT, NAMES, SPEC, score, weights

OUT = ROOT/'results/task4_v126_priority'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_regrets(lower, upper):
    return np.array([max(0., max(np.delete(upper, i))-lower[i]) for i in range(len(lower))])


def raw_from_utility(j, x):
    if NAMES[j] == 'travel':
        return np.nan
    _, benefit, anchor, _ = SPEC[j]
    if benefit:
        return anchor*x/(1-x) if x < 1 else np.inf
    return anchor*(1-x)/x if x else np.inf


def main():
    paths = [SOURCE, MANIFEST, ROOT/'design/task4_user_current_model.json',
        ROOT/'scripts/task4_user_v124_revision.py', ROOT/'scripts/task4_interval_decision.py',
        ROOT/'scripts/task4_v124_priority.py', ROOT/'scripts/task4_v5_model.py',
        *[(ROOT/'results/task4_user_v124_revision'/name) for name in
          ['current_ranks.csv', 'all_ranks.csv', 'utility_bounds.csv', 'summary.json', 'mc_city_summary.csv']]]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    registry = json.loads((ROOT/'design/task4_user_current_model.json').read_text())
    assert registry['version'] == 'V124' and registry['module'] == 'task4_user_v124_revision'
    frame, lo, hi = revised_bounds(); cities = frame.city.tolist(); n = len(cities)
    original = np.stack([lo, hi]).copy()
    missing = (lo == 0) & (hi == 1)
    assert n == 16 and lo.shape == (16, 10) and missing.sum() == 19
    assert np.sum(hi > lo) == 48 and np.sum(~missing) == 141
    saved = pd.read_csv(ROOT/'results/task4_user_v124_revision/current_ranks.csv')
    endpoints, priorities, joints, joint_endpoints, thresholds, baselines, audit_cases = [], [], [], [], [], [], []
    count = 0
    for reference, w in [('fixed', weights(.1)), ('equal', np.ones(10)/10)]:
        if reference == 'fixed':
            np.testing.assert_array_equal(w, np.array([.1125]*6+[.05,.1125,.1125,.05]))
        L, U = score(lo, w), score(hi, w)
        base = interval_decision(L, U)
        assert base['possible_champion'].sum() == 16 and not base['necessary_champion'].any()
        old = saved[(saved.weight_reference == reference) & (saved.scenario == 'after_conditional')].set_index('city').loc[cities]
        for col, expected in [('score_lower', L), ('score_upper', U), ('max_regret', base['max_regret'])]:
            np.testing.assert_allclose(old[col], expected, atol=1e-12, rtol=0)
        current_risk = base['minimax_regret']
        baselines.append(dict(weight_reference=reference, minimax_regret=current_risk,
            choices=[cities[i] for i in base['minimax_choices']], possible_count=16,
            mean_score_interval_width=float(np.mean(U-L))))

        def conditioned(i, js, values):
            nonlocal count
            a, b = lo.copy(), hi.copy(); a[i, js] = b[i, js] = values
            np.testing.assert_array_equal(a[~missing], lo[~missing])
            np.testing.assert_array_equal(b[~missing], hi[~missing])
            l, u = score(a, w), score(b, w)
            np.testing.assert_allclose(l, independent_scores(a, w), atol=1e-12, rtol=0)
            np.testing.assert_allclose(u, independent_scores(b, w), atol=1e-12, rtol=0)
            others = np.arange(n) != i
            np.testing.assert_array_equal(l[others], L[others]); np.testing.assert_array_equal(u[others], U[others])
            d = interval_decision(l, u)
            np.testing.assert_allclose(d['max_regret'], independent_regrets(l, u), atol=1e-12, rtol=0)
            p = np.array([u[k] >= max(np.delete(l, k))-1e-12 for k in range(n)])
            np.testing.assert_array_equal(p, d['possible_champion'])
            assert d['minimax_regret'] <= current_risk+1e-10
            count += 1
            return l, u, d

        for i, j in zip(*np.where(missing)):
            def callback(x):
                l, u, _ = conditioned(i, [j], x)
                return l, u
            endpoint_cases = []
            for label, x in [('lower', 0.), ('upper', 1.)]:
                l, u, d = conditioned(i, [j], x)
                endpoint_cases.append((l, u, d))
                endpoints.append(dict(weight_reference=reference, city=cities[i], indicator=NAMES[j],
                    endpoint=label, resolved_utility=x, implied_raw_PTR_or_density=raw_from_utility(j, x),
                    possible_count=int(d['possible_champion'].sum()),
                    excluded_cities=';'.join(cities[k] for k in range(n) if not d['possible_champion'][k]),
                    minimax_choices=';'.join(cities[k] for k in d['minimax_choices']),
                    minimax_regret_before=current_risk, minimax_regret_after=d['minimax_regret'],
                    minimax_regret_reduction=current_risk-d['minimax_regret'],
                    focal_lower=float(l[i]), focal_upper=float(u[i]),
                    focal_score_width_reduction=float((U[i]-L[i])-(u[i]-l[i])),
                    interpretation='Perfect utility identification at a closed endpoint; not observed evidence'))
            voi = voi_1d(callback, i, 0., 1., baseline=(L, U))
            # Independently optimize the one-city two-branch envelope. The
            # focal regret decreases, best-other regret increases with x.
            def branches(x):
                a, b = lo.copy(), hi.copy(); a[i, j] = b[i, j] = x
                rr = independent_regrets(independent_scores(a, w), independent_scores(b, w))
                return float(rr[i]), float(np.delete(rr, i).min())
            candidates = [0., 1.]
            left, right = 0., 1.
            if branches(0)[0] >= branches(0)[1] and branches(1)[0] <= branches(1)[1]:
                for _ in range(60):
                    mid = (left+right)/2; a, b = branches(mid)
                    if a > b:
                        left = mid
                    else:
                        right = mid
                candidates += [left, right]
            risks = [min(branches(x)) for x in candidates]
            worst, best = max(risks), min(min(branches(0)), min(branches(1)))
            np.testing.assert_allclose([voi['worst_post_regret'], voi['best_post_regret']], [worst, best], atol=1e-10, rtol=0)
            np.testing.assert_allclose([voi['guaranteed_gain'], voi['best_possible_gain']],
                                       [current_risk-worst, current_risk-best], atol=1e-10, rtol=0)
            optimistic_exclusions = max(16-int(case[2]['possible_champion'].sum()) for case in endpoint_cases)
            for x in np.linspace(0, 1, 21):
                _, _, d = conditioned(i, [j], float(x))
                assert best-1e-10 <= d['minimax_regret'] <= worst+1e-10
                assert 16-int(d['possible_champion'].sum()) <= optimistic_exclusions
            priority = dict(weight_reference=reference, city=cities[i], indicator=NAMES[j],
                guaranteed_exact_resolution_regret_reduction=voi['guaranteed_gain'],
                best_possible_exact_resolution_regret_reduction=voi['best_possible_gain'],
                worst_post_regret=worst, best_post_regret=best,
                optimistic_champion_exclusions=optimistic_exclusions,
                low_endpoint_choices=';'.join(cities[k] for k in endpoint_cases[0][2]['minimax_choices']),
                high_endpoint_choices=';'.join(cities[k] for k in endpoint_cases[1][2]['minimax_choices']),
                current_focal_upper=U[i], hypothetical_resolution='Exact utility in[0,1], not raw-source acquisition probability',
                actual_partial_source_rule='Inventory count or matched travel mean generally raises only the lower utility; exact-resolution guarantees do not apply')
            priorities.append(priority)
            # Single-cell exclusion thresholds support source triage.
            low, high = endpoint_cases
            targets = [(k, U[k], 'lower_above') for k in range(n)
                       if k != i and high[0][i] > U[k]+1e-12]
            if not low[2]['possible_champion'][i]:
                targets.append((i, max(np.delete(L, i)), 'upper_below'))
            for k, target, direction in targets:
                left, right = 0., 1.
                for _ in range(50):
                    x = (left+right)/2; l, u, _ = conditioned(i, [j], x)
                    value = l[i] if direction == 'lower_above' else u[i]
                    if value < target:
                        left = x
                    else:
                        right = x
                x = (left+right)/2
                thresholds.append(dict(weight_reference=reference, source_city=cities[i], indicator=NAMES[j],
                    excluded_city=cities[k], direction=direction, utility_threshold=x,
                    raw_PTR_or_density_threshold=raw_from_utility(j, x),
                    strict_rule='Observed lower utility strictly above threshold' if direction == 'lower_above' else
                                'Observed upper utility strictly below threshold',
                    travel_scope='A mean alone does not supply an upper utility bound; matched bins or distribution needed' if NAMES[j] == 'travel' else ''))
            audit_cases.append(dict(weight_reference=reference, city=cities[i], indicator=NAMES[j],
                                   independent_two_branch_value_of_information=True))

        # Same-city joint limits, retaining all already partial source cells.
        for i, city in enumerate(cities):
            js = np.flatnonzero(missing[i]).tolist()
            if not js:
                continue
            for size in range(1, len(js)+1):
                for group in combinations(js, size):
                    candidates = []
                    for label, x in [('lower', 0.), ('upper', 1.)]:
                        l, u, d = conditioned(i, list(group), x)
                        row = dict(weight_reference=reference, city=city, indicators=';'.join(NAMES[j] for j in group),
                            cell_count=size, all_city_full_missing_cells=(size == len(js)),
                            endpoint=label, resolved_utility=x, possible_count=int(d['possible_champion'].sum()),
                            excluded_cities=';'.join(cities[k] for k in range(n) if not d['possible_champion'][k]),
                            minimax_choices=';'.join(cities[k] for k in d['minimax_choices']),
                            minimax_regret_after=d['minimax_regret'],
                            minimax_regret_reduction=current_risk-d['minimax_regret'],
                            focal_lower=float(l[i]), focal_upper=float(u[i]))
                        joint_endpoints.append(row); candidates.append(row)
                    joints.append(dict(weight_reference=reference, city=city, indicators=candidates[0]['indicators'],
                        cell_count=size, all_city_full_missing_cells=(size == len(js)),
                        optimistic_champion_exclusions=max(16-r['possible_count'] for r in candidates),
                        high_endpoint_exclusions=16-candidates[1]['possible_count'],
                        best_endpoint_regret_reduction=max(r['minimax_regret_reduction'] for r in candidates)))

    OUT.mkdir(parents=True, exist_ok=True)
    pr = pd.DataFrame(priorities).sort_values(['weight_reference', 'guaranteed_exact_resolution_regret_reduction',
        'best_possible_exact_resolution_regret_reduction'], ascending=[True, False, False])
    pr.to_csv(OUT/'priority.csv', index=False)
    pd.DataFrame(endpoints).to_csv(OUT/'endpoint_information.csv', index=False)
    joint = pd.DataFrame(joints).sort_values(['weight_reference', 'optimistic_champion_exclusions',
        'best_endpoint_regret_reduction'], ascending=[True, False, False])
    joint.to_csv(OUT/'joint_subset_limits.csv', index=False)
    joint[joint.all_city_full_missing_cells].to_csv(OUT/'joint_priority.csv', index=False)
    pd.DataFrame(joint_endpoints).to_csv(OUT/'joint_endpoint_information.csv', index=False)
    pd.DataFrame(thresholds).to_csv(OUT/'exclusion_thresholds.csv', index=False)
    pd.DataFrame([dict(city=cities[i], indicator=NAMES[j]) for i, j in zip(*np.where(missing))]).to_csv(OUT/'missing_cells.csv', index=False)
    for path, expected in hashes.items():
        assert digest(ROOT/path) == expected, path
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([final_l, final_u]))
    summary = dict(version='V126 acquisition diagnosis on frozen V124 user16',
        fully_missing_cells=19, protected_nonfullymissing_cells=141, point_cells=112, partial_interval_cells=29,
        baseline=baselines, independent_score_regret_champion_evaluations=count,
        exact_resolution_VOI_cases=len(audit_cases), no_MC_or_random_missing_value_completion=True,
        interpretation='Conditional deterministic information limits, not observed improvement, a source availability probability or a prediction',
        guarantee_scope='Guarantees condition on complete exact utility identification of one cell. A partial inventory, teacher interval or Jensen mean does not automatically satisfy that condition.',
        endpoint_scope='Closed utility endpoints can be limiting raw values; ceilings need not be physically attainable',
        source_sha256=hashes)
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass',
        exact_resolution_cases=audit_cases, independent_evaluations=count,
        V124_baseline_matches_saved_ranks=True, all141_nonfullymissing_cells_preserved=True,
        current_registry_original_CSV_and_all160_bounds_unchanged=True,
        value_of_information_optimizer_independently_recomputed=True), indent=2)+'\n')
    print(json.dumps(summary, indent=2)); print(pr.to_string(index=False))


if __name__ == '__main__':
    main()
