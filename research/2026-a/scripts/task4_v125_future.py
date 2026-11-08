"""V124 future stresses, paired historical-proxy withdrawal, and V121 controls.

Only this module's output directory is written. V122 pure mathematical helpers
are reused; independently inverted raw values audit their V124 transformations.
"""
import hashlib
import json
import math
from io import StringIO

import numpy as np
import pandas as pd

from task4_ahp_mc_baseline import score_many
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import revised_bounds as v121_bounds
from task4_user_v124_revision import MANIFEST, revised_bounds, without_historical_proxy
from task4_v122_future import (DRAWS, IMPROVE, SCENARIOS, SEED, TOL, WEIGHT_SEED,
                               decision, multipliers, score, selfcheck, threshold, transform)
from task4_v5_model import NAMES, ROOT, SPEC, weights

OUT = ROOT / 'results/task4_v125_future'
FROZEN = ROOT / 'results/task4_v122_future'
REFERENCES = [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]


def raw_transform(lo, hi, factors, means):
    """Independent scalar inversion to raw criteria, including endpoint limits."""
    factors = np.asarray(factors)
    assert factors.shape == lo.shape
    a, b = np.empty_like(lo), np.empty_like(hi)
    for i in range(len(lo)):
        for j, (name, benefit, anchor, _) in enumerate(SPEC):
            r = float(factors[i, j])
            if name == 'travel':
                if np.isfinite(means[i]):
                    a[i, j], b[i, j] = math.exp(-r * means[i] / 30), 1
                elif r < 1:
                    a[i, j], b[i, j] = lo[i, j], hi[i, j] ** r
                else:
                    a[i, j], b[i, j] = lo[i, j] ** r, hi[i, j]
            else:
                def one(u):
                    if u == 0 or u == 1:
                        return float(u)
                    raw = anchor * u / (1-u) if benefit else anchor * (1/u-1)
                    raw *= r
                    return raw/(anchor+raw) if benefit else anchor/(anchor+raw)
                a[i, j], b[i, j] = one(lo[i, j]), one(hi[i, j])
    return a, b


def scalar_scores(x, w):
    result = []
    for row in x:
        p = math.sqrt(sum(float(w[j]) * float(row[j])**2 for j in range(10)))
        n = math.sqrt(sum(float(w[j]) * (1-float(row[j]))**2 for j in range(10)))
        result.append(100*p/(p+n))
    return np.array(result)


def scalar_decision(lower, upper):
    """Direct i!=k loops distinguish exclusion of self from any diagonal trick."""
    regret, possible = [], []
    for i in range(len(lower)):
        regret.append(max(0, max(upper[k] for k in range(len(lower)) if k != i)-lower[i]))
        possible.append(upper[i] >= max(lower[k] for k in range(len(lower)) if k != i)-TOL)
    regret = np.array(regret)
    selected = regret <= min(regret)+TOL
    rank = np.array([1+sum(regret[i] > g+TOL for g in regret) for i in range(len(regret))])
    return regret, selected/selected.sum(), rank, np.array(possible)


def adversarial_decision_check():
    # A city's own high upper bound must not inflate that city's regret.
    lower, upper = np.array([0., 70., 80.]), np.array([100., 70., 80.])
    actual = decision(lower, upper)
    np.testing.assert_array_equal(actual[0], [80., 30., 20.])
    for x, y in zip(actual, scalar_decision(lower, upper)):
        np.testing.assert_array_equal(x, y)
    # Equal minimax choices share one unit of recommendation credit.
    actual = decision(np.array([80., 80., 20.]), np.array([80., 80., 20.]))
    np.testing.assert_array_equal(actual[1], [.5, .5, 0.])
    np.testing.assert_array_equal(actual[2], [1, 1, 3])
    np.testing.assert_array_equal(actual[3], [True, True, False])


def audit_setting(lo, hi, factors, means, w):
    a, b = transform(lo, hi, factors, means)
    independent_a, independent_b = raw_transform(lo, hi, factors, means)
    np.testing.assert_allclose(a, independent_a, rtol=0, atol=2e-14)
    np.testing.assert_allclose(b, independent_b, rtol=0, atol=2e-14)
    unknown = (lo == 0) & (hi == 1)
    np.testing.assert_array_equal(a[unknown], np.zeros(unknown.sum()))
    np.testing.assert_array_equal(b[unknown], np.ones(unknown.sum()))
    for x in (a, b):
        np.testing.assert_allclose(score(x, w), scalar_scores(x, w), atol=2e-13, rtol=0)
    expected = scalar_decision(scalar_scores(independent_a, w), scalar_scores(independent_b, w))
    actual = decision(score(a, w), score(b, w))
    for x, y in zip(actual, expected):
        np.testing.assert_allclose(x, y, rtol=0, atol=3e-13)


def run(factory, paired_mc=False):
    frame, lo, hi = factory()
    cities = frame.city.tolist()
    means = frame.commute_min.to_numpy(dtype=float)
    assert lo.shape == hi.shape == (16, 10)
    checks = selfcheck(lo, hi, means, cities)
    adversarial_decision_check()
    arms = [('conditional', lo, hi), ('withdraw_historical_stage_proxy',
                                     *without_historical_proxy(frame, lo, hi))]
    rank_rows, bound_rows, summaries, thresholds, scans = [], [], [], [], []
    for arm, l, h in arms:
        for ref, w in REFERENCES:
            baseline = evaluate(cities, l, h, w)
            for label, changes in SCENARIOS.items():
                factors = multipliers(l.shape, changes)
                audit_setting(l, h, factors, means, w)
                a, b = transform(l, h, factors, means)
                result = evaluate(cities, a, b, w)
                result['baseline_decision_rank'] = baseline.decision_rank
                result['rank_change_positive_improves'] = baseline.decision_rank-result.decision_rank
                result['score_lower_change'] = result.score_lower-baseline.score_lower
                result['score_upper_change'] = result.score_upper-baseline.score_upper
                rank_rows.append(result.assign(evidence_arm=arm, scenario=label, weight_reference=ref))
                summaries.append(dict(evidence_arm=arm, scenario=label, weight_reference=ref,
                    minimax_choices=result.loc[result.max_regret <= result.max_regret.min()+TOL, 'city'].tolist(),
                    possible_champions=result.loc[result.possible_champion, 'city'].tolist(),
                    mean_score_interval_width=float((result.score_upper-result.score_lower).mean())))
                if ref == 'fixed':
                    bound_rows.extend(dict(evidence_arm=arm, scenario=label, city=c, indicator=n,
                        lower=a[i, j], upper=b[i, j]) for i, c in enumerate(cities) for j, n in enumerate(NAMES))
            # Frozen V122 threshold coverage is conditional; retain that exact scope.
            if arm == 'conditional':
                for city in cities:
                    record, scan = threshold(cities, l, h, w, means, city)
                    thresholds.append(dict(weight_reference=ref, **record))
                    scans.extend(dict(weight_reference=ref, **r) for r in scan)
                    # Independently recompute all101 raw-scale scan points and crossing sides.
                    k = cities.index(city)
                    independent_gaps = []
                    for row in scan:
                        f = multipliers(l.shape, dict.fromkeys(IMPROVE, row['raw_multiplier']-1), [k])
                        a, b = raw_transform(l, h, f, means)
                        regrets = scalar_decision(scalar_scores(a, w), scalar_scores(b, w))[0]
                        independent_gaps.append(regrets[k]-np.delete(regrets, k).min())
                    np.testing.assert_allclose(independent_gaps,
                        [r['regret_gap_to_best_other'] for r in scan], rtol=0, atol=3e-13)
                    if record['status'] == 'crossing_found':
                        crossing = record['threshold_raw_multiplier']
                        for epsilon, sign in [(-1e-6, -1), (1e-6, 1)]:
                            f = multipliers(l.shape, dict.fromkeys(IMPROVE, crossing+epsilon-1), [k])
                            a, b = raw_transform(l, h, f, means)
                            regrets = scalar_decision(scalar_scores(a, w), scalar_scores(b, w))[0]
                            assert sign*(regrets[k]-np.delete(regrets, k).min()) > TOL

    rng = np.random.default_rng(SEED)
    common = rng.uniform(0, 1, (DRAWS, 1))
    local = rng.uniform(0, 1, (DRAWS, len(cities)))
    delta = .05*common+.05*local
    assert np.all((0 <= delta) & (delta <= .1))
    mc, weight_mc = [], []
    for arm, l, h in (arms if paired_mc else arms[:1]):
        arm_column = dict(evidence_arm=arm) if paired_mc else {}
        for ref, w in REFERENCES:
            L0, U0 = score(l, w), score(h, w)
            for label, changes in SCENARIOS.items():
                if label == 'baseline':
                    continue
                factors = np.ones((DRAWS, *l.shape))
                for name, change in changes.items():
                    factors[..., NAMES.index(name)] = 1+np.sign(change)*delta
                a, b = transform(l, h, factors, means)
                L, U = score(a, w), score(b, w)
                unknown = (l == 0) & (h == 1)
                assert np.all(a[:, unknown] == 0) and np.all(b[:, unknown] == 1)
                regret, credit, rank, possible = decision(L, U)
                np.testing.assert_allclose(credit.sum(1), 1)
                for d in (0, 1, DRAWS-1):
                    audit_setting(l, h, factors[d], means, w)
                    for expected, actual in zip(scalar_decision(scalar_scores(a[d], w),
                            scalar_scores(b[d], w)), (regret[d], credit[d], rank[d], possible[d])):
                        np.testing.assert_allclose(actual, expected, rtol=0, atol=3e-13)
                for i, city in enumerate(cities):
                    row = dict(random_source='future_shocks_only', scenario=label,
                        weight_reference=ref, city=city,
                        recommendation_frequency=float(credit[:, i].mean()),
                        possible_champion_frequency=float(possible[:, i].mean()),
                        mean_decision_rank=float(rank[:, i].mean()))
                    for endpoint, changes_at_endpoint in [('lower', L[:, i]-L0[i]), ('upper', U[:, i]-U0[i])]:
                        for suffix, quantile in [('05', .05), ('50', .5), ('95', .95)]:
                            row[f'score_{endpoint}_change_p{suffix}'] = float(np.quantile(changes_at_endpoint, quantile))
                    mc.append(dict(**row, **arm_column))
            sampled_w = np.random.default_rng(np.random.SeedSequence(WEIGHT_SEED)).dirichlet(100*w, DRAWS)
            for label, changes in SCENARIOS.items():
                factors = multipliers(l.shape, changes)
                a, b = transform(l, h, factors, means)
                L, U = score_many(a, sampled_w), score_many(b, sampled_w)
                _, credit, rank, possible = decision(L, U)
                np.testing.assert_allclose(credit.sum(1), 1)
                for d in (0, 1, DRAWS-1):
                    audit_setting(l, h, factors, means, sampled_w[d])
                    for expected, actual in zip(scalar_decision(scalar_scores(a, sampled_w[d]),
                            scalar_scores(b, sampled_w[d])), decision(L[d], U[d])):
                        np.testing.assert_allclose(actual, expected, rtol=0, atol=3e-13)
                for i, city in enumerate(cities):
                    weight_mc.append(dict(random_source='weights_only', scenario=label,
                        weight_reference=ref, concentration=100, city=city,
                        recommendation_frequency=float(credit[:, i].mean()),
                        possible_champion_frequency=float(possible[:, i].mean()),
                        mean_decision_rank=float(rank[:, i].mean()), **arm_column))
    tables = dict(ranks=pd.concat(rank_rows, ignore_index=True),
        utility_bounds=pd.DataFrame(bound_rows), thresholds=pd.DataFrame(thresholds),
        threshold_scan=pd.DataFrame(scans), future_mc_city_summary=pd.DataFrame(mc),
        weight_mc_city_summary=pd.DataFrame(weight_mc))
    checks.update(independent_raw_inversion=True, all_deterministic_unknown_cells_preserved=True,
        all_future_mc_draws_unknown_cells_preserved=True,
        adversarial_self_exclusion_and_equal_tie_credit=True,
        scalar_self_excluded_regret_rank_possible_and_tie_credit=True,
        threshold_independent_scan_points=32*101, threshold_crossing_sides=True,
        future_mc_independent_draws_per_setting=3, future_mc_settings=12 if paired_mc else 6,
        weight_mc_independent_draws_per_setting=3, weight_mc_settings=16 if paired_mc else 8,
        paired_mc_same_shocks_and_weights=paired_mc)
    return tables, dict(checks=checks, scenarios=summaries, thresholds=thresholds)


def compare_control(tables, summary):
    frozen_summary = json.loads((FROZEN/'summary.json').read_text())
    checks = {}
    for name, table in tables.items():
        frozen = pd.read_csv(FROZEN/(name+'.csv'), float_precision='round_trip')
        # Apply the same CSV serialization as frozen output, including object/list columns.
        regenerated = pd.read_csv(StringIO(table.to_csv(index=False)), float_precision='round_trip')
        pd.testing.assert_frame_equal(regenerated, frozen, check_exact=True)
        checks[name] = dict(rows=len(frozen), all_columns_exact=True)
    assert summary['scenarios'] == frozen_summary['scenarios']
    assert summary['thresholds'] == frozen_summary['thresholds']
    return dict(factory='V121', frozen_version='V122', tables=checks,
                summary_scenarios_exact=True, summary_thresholds_exact=True)


def baseline_mc_check(table, cities):
    old = pd.read_csv(ROOT/'results/task4_user_v124_revision/mc_city_summary.csv', float_precision='round_trip')
    for ref, _ in REFERENCES:
        for arm, scenario in [('conditional', 'after_conditional'),
                              ('withdraw_historical_stage_proxy', 'withdraw_historical_stage_proxy')]:
            previous = old[(old.scenario == scenario) & (old.weight_reference == ref)
                           & (old.concentration == 100)].set_index('city').loc[cities]
            current = table[(table.scenario == 'baseline') & (table.weight_reference == ref)
                            & (table.evidence_arm == arm)].set_index('city').loc[cities]
            for now, before in [('recommendation_frequency', 'minimax_recommendation_frequency'),
                                ('mean_decision_rank', 'mean_decision_rank'),
                                ('possible_champion_frequency', 'possible_champion_frequency')]:
                np.testing.assert_array_equal(current[now], previous[before])


def main():
    old_summary = json.loads((FROZEN/'summary.json').read_text())
    source_paths = set(old_summary['source_sha256'])
    source_paths.update(['scripts/task4_v125_future.py', 'scripts/task4_user_v124_revision.py',
                         'design/task4_user_v124_admissions.json'])
    source_paths.update(str(p.relative_to(ROOT)) for p in FROZEN.iterdir() if p.is_file())
    source_paths.add('results/task4_user_v124_revision/mc_city_summary.csv')
    protected = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(source_paths)}
    control_tables, control_summary = run(v121_bounds)
    control = compare_control(control_tables, control_summary)
    tables, summary = run(revised_bounds, paired_mc=True)
    frame, lo, hi = revised_bounds()
    baseline_mc_check(tables['weight_mc_city_summary'], frame.city.tolist())
    _, old_lo, old_hi = v121_bounds()
    np.testing.assert_array_equal(hi, old_hi)
    changes = [dict(city=frame.city.iloc[i], indicator=NAMES[j],
                    previous_lower=float(old_lo[i, j]), current_lower=float(lo[i, j]),
                    previous_upper=float(old_hi[i, j]), current_upper=float(hi[i, j]))
               for i, j in zip(*np.where(lo != old_lo))]
    comparisons = {}
    for name in ['ranks', 'thresholds', 'future_mc_city_summary', 'weight_mc_city_summary']:
        old, current = control_tables[name], tables[name]
        if name in ['future_mc_city_summary', 'weight_mc_city_summary']:
            current = current[current.evidence_arm == 'conditional'].drop(columns='evidence_arm')
        keys = [c for c in ['evidence_arm', 'scenario', 'weight_reference', 'city'] if c in old.columns]
        joined = current.merge(old, on=keys, suffixes=('_v124', '_v121'), validate='one_to_one')
        comparisons[name] = joined
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path
    summary.update(version='V125', baseline='16-city V124 conditional evidence',
        interpretation=old_summary['interpretation'], deterministic_raw_changes=SCENARIOS,
        future_mc={**old_summary['future_mc'], 'evidence_arms':'conditional and historical-stage-proxy withdrawal, identical random draws'},
        weight_mc={**old_summary['weight_mc'], 'evidence_arms':'conditional and historical-stage-proxy withdrawal, identical weights'},
        travel_rule=old_summary['travel_rule'], scope=old_summary['scope'], threshold_rule=old_summary['threshold_rule'],
        threshold_evidence_arm='conditional, matching frozenV122 scope',
        weights={ref:w.tolist() for ref,w in REFERENCES}, source_sha256=protected,
        v121_control_reproduction=control, changed_input_bounds=changes,
        source_admissions=str(MANIFEST.relative_to(ROOT)),
        no_missing_cell_imputation=True, no_calendar_prediction=True)
    summary['checks']['weight_mc_baseline_exactly_matches_V124_both_arms_and_references'] = True
    OUT.mkdir(exist_ok=True, parents=True)
    for name, table in tables.items():
        table.to_csv(OUT/(name+'.csv'), index=False)
    for name, table in comparisons.items():
        table.to_csv(OUT/(name+'_v121_comparison.csv'), index=False)
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(dict(control=control, changed_bounds=changes,
                         scenarios=summary['scenarios']), indent=2))


if __name__ == '__main__':
    main()
