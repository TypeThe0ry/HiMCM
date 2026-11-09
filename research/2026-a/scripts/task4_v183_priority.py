"""V181 user16 acquisition limits for its 13 completely missing utility cells.

Information values condition on exact utility resolution, not on a probability
distribution or on actually obtaining a complete, correctly scoped source.
"""
import hashlib
from pathlib import Path
from itertools import combinations, product
import json
import subprocess

import numpy as np
import pandas as pd

from task4_interval_decision import interval_decision, voi_1d
from task4_user_city_indicators import SOURCE
from task4_user_v181_revision import MANIFEST, revised_bounds
from task4_v124_priority import independent_scores
from task4_v5_model import ROOT, NAMES, SPEC, score, weights

OUT = ROOT/'results/task4_v183_priority'


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
    snapshot = ROOT/'design/task4_user_v181_snapshot.json'
    source_hashes=json.loads(snapshot.read_text())['source_sha256']
    # Two mutable navigation pointers were frozen before V182 activation.
    # Validate their current declared roles, then bind current bytes explicitly.
    navigation={'design/task4_user_current_model.json','design/task4_user_current_extensions.json'}
    assert navigation.issubset(source_hashes)
    model=json.loads((ROOT/'design/task4_user_current_model.json').read_text())
    ext=json.loads((ROOT/'design/task4_user_current_extensions.json').read_text())
    assert model['version']=='V181' and model['module']=='task4_user_v181_revision'
    assert ext['extension_version']==ext['primary_evidence_version']=='V181'
    source_hashes={name:(digest(ROOT/name) if name in navigation else h) for name,h in source_hashes.items()}
    for name, expected in source_hashes.items():
        assert digest(ROOT/name)==expected,name
    paths=[ROOT/name for name in source_hashes]
    paths += [SOURCE,MANIFEST,snapshot,Path(__file__),ROOT/'scripts/task4_v155_priority.py',
              *[p for p in (ROOT/'results/task4_v155_priority').iterdir() if p.is_file()]]
    hashes={str(p.relative_to(ROOT)):digest(p) for p in sorted(set(paths))}
    registry_path='design/task4_user_current_model.json'
    live_registry=json.loads((ROOT/registry_path).read_text())
    assert live_registry['version']=='V181' and live_registry['module']=='task4_user_v181_revision'
    frozen_registry_sha=digest(ROOT/registry_path)
    frame, lo, hi = revised_bounds(); cities = frame.city.tolist(); n = len(cities)
    original = np.stack([lo, hi]).copy()
    missing = (lo == 0) & (hi == 1)
    assert n == 16 and lo.shape == (16, 10) and missing.sum() == 13
    assert np.sum(hi > lo) == 48 and np.sum(~missing) == 147
    saved = pd.read_csv(ROOT/'results/task4_user_v181_revision/current_ranks.csv')
    endpoints, priorities, joints, joint_endpoints, thresholds, baselines, audit_cases = [], [], [], [], [], [], []
    lower_only, switches, joint_audits = [], [], []
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

        def conditioned(i, js, values, exact=True):
            nonlocal count
            a, b = lo.copy(), hi.copy(); a[i, js] = values
            if exact:
                b[i, js] = values
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
            necessary = np.array([l[k] >= max(np.delete(u, k))-1e-12 for k in range(n)])
            np.testing.assert_array_equal(necessary, d['necessary_champion'])
            np.testing.assert_array_equal(d['best_rank'], [1+sum(np.delete(l, k) > u[k]+1e-12) for k in range(n)])
            np.testing.assert_array_equal(d['worst_rank'], [1+sum(np.delete(u, k) > l[k]+1e-12) for k in range(n)])
            rr = independent_regrets(l, u)
            np.testing.assert_array_equal(d['minimax_choices'], np.flatnonzero(rr <= rr.min()+1e-12))
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
                x = (left+right)/2
                switches.append(dict(weight_reference=reference, city=cities[i], indicators=NAMES[j],
                    acquisition='exact_utility', utility_threshold=x,
                    raw_PTR_or_density_threshold=raw_from_utility(j, x),
                    interpretation='Focal minimax at or above utility threshold; equality may tie. Other cells fixed.'))
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

        # A real inventory/mean usually yields [x,1], not exact utility x.
        # Retain the upper bound and record conditional effects without VOI guarantees.
        def lower_only_group(i, js, label):
            rows = []
            for x in np.linspace(0, 1, 21):
                l, u, d = conditioned(i, js, float(x), exact=False)
                row = dict(weight_reference=reference, city=cities[i],
                    indicators=';'.join(NAMES[j] for j in js), group=label,
                    observed_utility_lower=float(x), retained_utility_upper=1,
                    possible_count=int(d['possible_champion'].sum()),
                    excluded_cities=';'.join(cities[k] for k in range(n) if not d['possible_champion'][k]),
                    minimax_choices=';'.join(cities[k] for k in d['minimax_choices']),
                    minimax_regret_after=d['minimax_regret'],
                    minimax_regret_reduction=current_risk-d['minimax_regret'],
                    focal_score_lower=float(l[i]), focal_score_upper=float(u[i]),
                    scope='Hypothetical lower-bound-only information; x=1 may be a limiting raw endpoint, not an obtainable observation')
                lower_only.append(row); rows.append(row)
            assert np.all(np.diff([r['minimax_regret_after'] for r in rows]) <= 1e-10)
            assert all(cities[i] not in r['excluded_cities'].split(';') for r in rows)
            # Other cities keep fixed regret when only the focal lower bound rises.
            l0, u0, d0 = conditioned(i, js, 0., exact=False)
            l1, u1, d1 = conditioned(i, js, 1., exact=False)
            if i not in d0['minimax_choices'] and i in d1['minimax_choices']:
                target = np.delete(independent_regrets(l0, u0), i).min()
                left, right = 0., 1.
                for _ in range(50):
                    x = (left+right)/2
                    a = lo.copy(); a[i, js] = x
                    rr = independent_regrets(independent_scores(a, w), independent_scores(hi, w))
                    if rr[i] > target: left = x
                    else: right = x
                x = (left+right)/2
                switches.append(dict(weight_reference=reference, city=cities[i],
                    indicators=';'.join(NAMES[j] for j in js), acquisition='lower_bound_only',
                    utility_threshold=x,
                    raw_PTR_or_density_threshold=raw_from_utility(js[0], x) if len(js)==1 else np.nan,
                    interpretation='Focal minimax at or above lower-utility threshold; upper bound remains 1; equality may tie.'))

        for i, j in zip(*np.where(missing)):
            lower_only_group(i, [j], 'single')

        # Same-city joint limits, retaining all already partial source cells.
        for i, city in enumerate(cities):
            js = np.flatnonzero(missing[i]).tolist()
            if not js:
                continue
            if len(js) > 1:
                lower_only_group(i, js, 'all_city_missing')
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
                    # Independent mixed-coordinate probes supplement the monotone
                    # endpoint ceiling: a joint completion need not share one x.
                    probes = 0
                    for values in product((0., .25, .5, .75, 1.), repeat=size):
                        _, _, d = conditioned(i, list(group), list(values))
                        assert 16-int(d['possible_champion'].sum()) <= joints[-1]['optimistic_champion_exclusions']
                        assert current_risk-d['minimax_regret'] <= joints[-1]['best_endpoint_regret_reduction']+1e-10
                        probes += 1
                    joint_audits.append(dict(weight_reference=reference, city=city,
                        indicators=candidates[0]['indicators'], mixed_coordinate_probes=probes))

    # Check recorded recommendation crossings with independent norms/regrets on
    # both sides, including the diagonal specified for a joint lower-bound route.
    for row in switches:
        w = weights(.1) if row['weight_reference'] == 'fixed' else np.ones(10)/10
        i = cities.index(row['city']); js = [NAMES.index(x) for x in row['indicators'].split(';')]
        x = row['utility_threshold']
        assert 1e-7 < x < 1-1e-7
        for shift, sign in [(-1e-7, 1), (1e-7, -1)]:
            a, b = lo.copy(), hi.copy(); a[i, js] = x+shift
            if row['acquisition'] == 'exact_utility': b[i, js] = x+shift
            rr = independent_regrets(independent_scores(a, w), independent_scores(b, w))
            assert sign*(rr[i]-np.delete(rr, i).min()) > 0
        row['matched_mean_minutes_upper_for_Jensen_lower'] = (
            -30*np.log(x) if js == [NAMES.index('travel')] and row['acquisition'] == 'lower_bound_only' else np.nan)

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
    pd.DataFrame(switches).to_csv(OUT/'recommendation_thresholds.csv', index=False)
    pd.DataFrame(lower_only).to_csv(OUT/'lower_only_information.csv', index=False)
    pd.DataFrame([dict(city=cities[i], indicator=NAMES[j]) for i, j in zip(*np.where(missing))]).to_csv(OUT/'missing_cells.csv', index=False)
    previews = []
    for path, expected in hashes.items():
        assert digest(ROOT/path) == expected, path
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([final_l, final_u]))
    summary = dict(version='V183 acquisition diagnosis on active V181 user16',
        fully_missing_cells=13, protected_nonfullymissing_cells=147, point_cells=112, partial_interval_cells=35,
        baseline=baselines, independent_score_regret_champion_evaluations=count,
        exact_resolution_VOI_cases=len(audit_cases), no_MC_or_random_missing_value_completion=True,
        interpretation='Conditional deterministic information limits, not observed improvement, a source availability probability or a prediction',
        guarantee_scope='Guarantees condition on complete exact utility identification of one cell. A partial inventory, teacher interval or Jensen mean does not automatically satisfy that condition.',
        endpoint_scope='Closed utility endpoints can be limiting raw values; ceilings need not be physically attainable',
        registry_snapshot='design/task4_user_v181_snapshot.json', frozen_registry_sha256=frozen_registry_sha,
        source_sha256=hashes)
    old_priority=pd.read_csv(ROOT/'results/task4_v155_priority/priority.csv')
    comparison=pr.merge(old_priority,on=['weight_reference','city','indicator'],
                        suffixes=('_V183','_V155'),how='outer',indicator=True)
    comparison.to_csv(OUT/'V155_comparison.csv',index=False)
    removed=comparison[comparison['_merge'].eq('right_only')][['city','indicator']].drop_duplicates()
    assert removed.to_records(index=False).tolist()==[('Amsterdam','public_transport_density')]
    assert not comparison['_merge'].eq('left_only').any()
    paired=comparison[comparison['_merge'].eq('both')]
    assert len(paired)==26
    metrics=['guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','optimistic_champion_exclusions']
    deltas={name:float((paired[name+'_V183']-paired[name+'_V155']).abs().max()) for name in metrics}
    summary['V155_comparison']=dict(previous_missing=14,current_missing=13,
        removed_fullymissing_keys=[['Amsterdam','public_transport_density']],
        remaining_paired_rows=26,maximum_absolute_metric_changes=deltas,
        interpretation='Amsterdam transport now has a protected conditional mapped-inventory lower bound; its residual partial uncertainty is assessed separately, not discarded.')
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass',
        exact_resolution_cases=audit_cases, independent_evaluations=count,
        V181_baseline_matches_saved_ranks=True, all147_nonfullymissing_cells_preserved=True,
        current_registry_original_CSV_and_all160_bounds_unchanged=True,
        V181_snapshot_and_all_existing_artifacts_byte_unchanged=True,
        protected_file_count=len(hashes), source_hashes_before_after_match=True,
        live_registry_version_during_audit=live_registry['version'],
        live_registry_sha256_before=hashes[registry_path], live_registry_sha256_after=digest(ROOT/registry_path),
        live_registry_used_as_input=False, snapshot_pinned_V181_registry=True, historical_snapshot_navigation_exceptions=sorted(navigation),
        candidate_lower_only_previews=len(previews), candidate_primary_admissions=0,
        lower_only_scenarios=len(lower_only), exact_and_lower_only_not_conflated=True,
        recommendation_crossings_independently_checked=len(switches),
        joint_mixed_coordinate_checks=joint_audits,
        value_of_information_optimizer_independently_recomputed=True), indent=2)+'\n')
    print(json.dumps(summary, indent=2)); print(pr.to_string(index=False))


if __name__ == '__main__':
    main()
