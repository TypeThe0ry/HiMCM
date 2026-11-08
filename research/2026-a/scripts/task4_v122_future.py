"""V121-based conditional future stresses; no extrapolated historical trend."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from task4_ahp_mc_baseline import score_many
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import MANIFEST, revised_bounds, without_historical_proxy
from task4_v5_model import NAMES, ROOT, SPEC, weights

OUT = ROOT / 'results/task4_v122_future'
TOL = 1e-10
DRAWS = 10000
SEED = 20261108122
WEIGHT_SEED = [20261108, 100]
SCENARIOS = {
    'baseline': {},
    'resource_expansion': {'research_he_density': .1, 'public_transport_density': .1,
                           'public_pool_density': .1},
    'living_pressure': {'cost_living_index': .1, 'price_income_ratio': .1, 'travel': .1},
    'balanced_improvement': {'upper_secondary_ptr': -.1, 'pm25': -.1, 'travel': -.1},
}
IMPROVE = ['upper_secondary_ptr', 'pm25', 'travel']


def multipliers(shape, changes, rows=None):
    result = np.ones(shape)
    rows = np.arange(shape[-2]) if rows is None else np.asarray(rows)
    for name, change in changes.items():
        result[..., rows, NAMES.index(name)] = 1 + change
    return result


def transform(lo, hi, factors, mean_minutes):
    """Raw scaling for ordinary criteria; moment bounds for mean travel utility.

    factors has shape (..., cities, criteria). Existing unknowns stay unknown.
    A fresh transformation always starts from V121 bounds, not from a prior
    outer approximation. Singapore moment envelopes generally are not reversible.
    """
    factors = np.asarray(factors, float)
    assert factors.shape[-2:] == lo.shape and np.all(factors > 0)
    a = np.broadcast_to(lo, factors.shape).copy()
    b = np.broadcast_to(hi, factors.shape).copy()
    for j, (name, benefit, _, _) in enumerate(SPEC):
        r = factors[..., j]
        if name == 'travel':
            # q=exp(-t/30), q'=q**r. Concave powers r<1 obey
            # E[q] <= E[q**r] <= E[q]**r; convex r>1 reverse these.
            a[..., j] = np.where(r < 1, lo[:, j], lo[:, j] ** r)
            b[..., j] = np.where(r < 1, hi[:, j] ** r, hi[:, j])
            known = np.isfinite(mean_minutes)
            assert np.all(hi[known, j] == 1)
            np.testing.assert_allclose(lo[known, j], np.exp(-mean_minutes[known] / 30),
                                       rtol=0, atol=1e-14)
            a[..., known, j] = np.exp(-r[..., known] * mean_minutes[known] / 30)
        else:
            def mapped(u):
                return r * u / (1 - u + r * u) if benefit else u / (u + r * (1 - u))
            a[..., j], b[..., j] = mapped(lo[:, j]), mapped(hi[:, j])
    assert np.all(np.isfinite(a)) and np.all(np.isfinite(b))
    assert np.all((0 <= a) & (a <= b) & (b <= 1))
    unchanged = factors == 1
    np.testing.assert_allclose(a[unchanged], np.broadcast_to(lo, factors.shape)[unchanged],
                               rtol=0, atol=1e-14)
    np.testing.assert_allclose(b[unchanged], np.broadcast_to(hi, factors.shape)[unchanged],
                               rtol=0, atol=1e-14)
    return a, b


def score(x, w):
    positive = np.sqrt(np.sum(x * x * w, axis=-1))
    negative = np.sqrt(np.sum((1 - x) ** 2 * w, axis=-1))
    return 100 * positive / (positive + negative)


def decision(lower, upper):
    """Vectorized self-excluded regret, with equal recommendation credit for ties."""
    n = lower.shape[-1]
    others = ~np.eye(n, dtype=bool)
    other_upper = np.where(others, upper[..., None, :], -np.inf).max(-1)
    other_lower = np.where(others, lower[..., None, :], -np.inf).max(-1)
    regret = np.maximum(0, other_upper - lower)
    recommended = regret <= regret.min(-1, keepdims=True) + TOL
    credit = recommended / recommended.sum(-1, keepdims=True)
    rank = 1 + (regret[..., :, None] > regret[..., None, :] + TOL).sum(-1)
    possible = upper >= other_lower - TOL
    return regret, credit, rank, possible


def threshold(cities, lo, hi, w, mean_minutes, city):
    k = cities.index(city)
    other = np.arange(len(cities)) != k

    def calc(r):
        m = multipliers(lo.shape, dict.fromkeys(IMPROVE, r - 1), [k])
        a, b = transform(lo, hi, m, mean_minutes)
        regret, _, _, _ = decision(score(a, w), score(b, w))
        return float(regret[k] - regret[other].min()), regret

    grid = np.linspace(1, .5, 101)
    values = [calc(float(r))[0] for r in grid]
    assert np.all(np.diff(values) <= 1e-9)
    record = dict(city=city, baseline_gap_to_best_other=values[0],
                  gap_at_50pct_cost_reduction=values[-1], status='not_reached',
                  threshold_raw_multiplier=None, required_cost_reduction_fraction=None)
    hits = np.flatnonzero(np.asarray(values) < -TOL)
    if len(hits):
        h = int(hits[0])
        if h == 0:
            record.update(status='already_strict_minimax', threshold_raw_multiplier=1.,
                          required_cost_reduction_fraction=0.)
        else:
            left, right = float(grid[h]), float(grid[h - 1])
            for _ in range(45):
                mid = (left + right) / 2
                if calc(mid)[0] < 0:
                    left = mid
                else:
                    right = mid
            r = (left + right) / 2
            gap, regret = calc(r)
            assert abs(gap) < 1e-8
            assert calc(r - 1e-6)[0] < -TOL and calc(r + 1e-6)[0] > TOL
            best_other = regret[other].min()
            record.update(status='crossing_found', threshold_raw_multiplier=r,
                          required_cost_reduction_fraction=1 - r,
                          threshold_bracket=[left, right], regret_gap_at_threshold=gap,
                          binding_best_other_cities=[cities[i] for i in range(len(cities))
                              if i != k and regret[i] <= best_other + TOL],
                          strict_rule='candidate regret is strictly below every other city regret; equality is a tied recommendation')
    elif abs(values[-1]) <= TOL:
        record['status'] = 'tie_only_at_endpoint'
    return record, [dict(city=city, raw_multiplier=float(r), regret_gap_to_best_other=g)
                    for r, g in zip(grid, values)]


def selfcheck(lo, hi, means, cities):
    """Check transformation mathematics and compare decisions with existing helper."""
    a, b = transform(lo, hi, np.ones_like(lo), means)
    np.testing.assert_array_equal(a, lo)
    np.testing.assert_array_equal(b, hi)
    # Ordinary raw-scale mappings are reversible; moment outer bounds are not.
    for name in set(NAMES) - {'travel'}:
        m = multipliers(lo.shape, {name: .1})
        a, b = transform(lo, hi, m, means)
        c, d = transform(a, b, multipliers(lo.shape, {name: 1 / 1.1 - 1}), means)
        np.testing.assert_allclose(c, lo, atol=1e-14, rtol=0)
        np.testing.assert_allclose(d, hi, atol=1e-14, rtol=0)
    # Discrete q mixtures verify the direction and both sharp moment endpoints.
    rng = np.random.default_rng(SEED + 1)
    for r in (.5, .9, 1., 1.1, 2.):
        q = rng.random((200, 7))
        p = rng.dirichlet(np.ones(7), len(q))
        moment, powered = (q * p).sum(1), (q ** r * p).sum(1)
        lower = moment if r < 1 else moment ** r
        upper = moment ** r if r < 1 else moment
        assert np.all(powered >= lower - 1e-14) and np.all(powered <= upper + 1e-14)
        # Constant q attains moment**r; a {0,1} mixture attains moment.
        for u in (0., .2, .7, 1.):
            endpoints = sorted([u, u ** r])
            assert endpoints[0] <= u ** r <= endpoints[1]
            assert endpoints[0] <= u <= endpoints[1]
    # Singapore exposes the tempting, invalid two-endpoint power shortcut.
    k, j = cities.index('Singapore'), NAMES.index('travel')
    l, u = lo[k, j], hi[k, j]
    a, b = transform(lo, hi, multipliers(lo.shape, {'travel': -.1}), means)
    assert a[k, j] == l and abs(b[k, j] - u ** .9) < 1e-14
    assert l ** .9 > a[k, j]  # Bernoulli q of mean l rules out that raised lower bound.
    a, b = transform(lo, hi, multipliers(lo.shape, {'travel': .1}), means)
    assert abs(a[k, j] - l ** 1.1) < 1e-14 and b[k, j] == u
    for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        old = evaluate(cities, lo, hi, w)
        L, U = score(lo, w), score(hi, w)
        regret, _, rank, possible = decision(L, U)
        np.testing.assert_allclose(old.max_regret, regret, atol=1e-12, rtol=0)
        np.testing.assert_array_equal(old.decision_rank, rank)
        np.testing.assert_array_equal(old.possible_champion, possible)
    return dict(identity=True, ordinary_raw_reversibility=True,
                travel_moment_discrete_mixtures=1000, sharp_endpoint_mixtures=True,
                singapore_invalid_power_shortcut_rejected=True,
                static_decisions_match_registered_helper=True)


def main():
    source_paths = [SOURCE, MANIFEST, Path(__file__),
                    ROOT / 'scripts/task4_user_v121_revision.py',
                    ROOT / 'scripts/task4_user_v120_revision.py',
                    ROOT / 'scripts/task4_user_v118_revision.py',
                    ROOT / 'scripts/task4_user_city_indicators.py',
                    ROOT / 'scripts/task4_v5_model.py',
                    ROOT / 'design/task4_user_current_model.json']
    protected = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in source_paths}
    frame, lo, hi = revised_bounds()
    cities, means = frame.city.tolist(), frame.commute_min.to_numpy(dtype=float)
    assert lo.shape == (16, 10) and len(cities) == 16
    checks = selfcheck(lo, hi, means, cities)
    arms = [('conditional', lo, hi), ('withdraw_historical_stage_proxy',
                                     *without_historical_proxy(frame, lo, hi))]
    rank_rows, bound_rows, summaries, thresholds, scans = [], [], [], [], []
    references = [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]
    for arm, l, h in arms:
        for ref, w in references:
            baseline = evaluate(cities, l, h, w)
            for label, changes in SCENARIOS.items():
                a, b = transform(l, h, multipliers(l.shape, changes), means)
                result = evaluate(cities, a, b, w)
                result['baseline_decision_rank'] = baseline.decision_rank
                result['rank_change_positive_improves'] = baseline.decision_rank - result.decision_rank
                result['score_lower_change'] = result.score_lower - baseline.score_lower
                result['score_upper_change'] = result.score_upper - baseline.score_upper
                rank_rows.append(result.assign(evidence_arm=arm, scenario=label, weight_reference=ref))
                summaries.append(dict(evidence_arm=arm, scenario=label, weight_reference=ref,
                    minimax_choices=result.loc[result.max_regret <= result.max_regret.min() + TOL, 'city'].tolist(),
                    possible_champions=result.loc[result.possible_champion, 'city'].tolist(),
                    mean_score_interval_width=float((result.score_upper - result.score_lower).mean())))
                if ref == 'fixed':
                    bound_rows.extend(dict(evidence_arm=arm, scenario=label, city=c, indicator=n,
                        lower=a[i, j], upper=b[i, j]) for i, c in enumerate(cities) for j, n in enumerate(NAMES))
            if arm == 'conditional':
                for city in cities:
                    result, scan = threshold(cities, l, h, w, means, city)
                    thresholds.append(dict(weight_reference=ref, **result))
                    scans.extend(dict(weight_reference=ref, **row) for row in scan)

    # Future shock simulation: fixed criterion weights, no draw of unknown cells.
    # Delta=.05*C+.05*I, C and I independent U[0,1]; common C shared by all
    # cities and affected criteria, I shared by affected criteria within a city.
    rng = np.random.default_rng(SEED)
    common = rng.uniform(0, 1, (DRAWS, 1))
    local = rng.uniform(0, 1, (DRAWS, len(cities)))
    delta = .05 * common + .05 * local
    assert np.all((0 <= delta) & (delta <= .1))
    mc, weight_mc = [], []
    for ref, w in references:
        L0, U0 = score(lo, w), score(hi, w)
        for label, changes in SCENARIOS.items():
            if label == 'baseline':
                continue
            factors = np.ones((DRAWS, *lo.shape))
            for name, change in changes.items():
                factors[..., NAMES.index(name)] = 1 + np.sign(change) * delta
            a, b = transform(lo, hi, factors, means)
            L, U = score(a, w), score(b, w)
            regret, credit, rank, possible = decision(L, U)
            np.testing.assert_allclose(credit.sum(1), 1)
            # Independent scalar score/decision recomputation on fixed draws.
            for d in (0, 1, DRAWS - 1):
                independent_l, independent_u = [], []
                for x in (a[d], b[d]):
                    distances = [sum(float(w[j] * x[i, j] ** 2) for j in range(10)) ** .5 for i in range(16)]
                    negatives = [sum(float(w[j] * (1 - x[i, j]) ** 2) for j in range(10)) ** .5 for i in range(16)]
                    target = [100 * p / (p + q) for p, q in zip(distances, negatives)]
                    (independent_l if len(independent_l) == 0 else independent_u).extend(target)
                independent_r = [max(0, max(independent_u[k] for k in range(16) if k != i) - independent_l[i]) for i in range(16)]
                np.testing.assert_allclose(independent_r, regret[d], atol=1e-12, rtol=0)
            for i, city in enumerate(cities):
                mc.append(dict(random_source='future_shocks_only', scenario=label,
                    weight_reference=ref, city=city,
                    recommendation_frequency=float(credit[:, i].mean()),
                    possible_champion_frequency=float(possible[:, i].mean()),
                    mean_decision_rank=float(rank[:, i].mean()),
                    score_lower_change_p05=float(np.quantile(L[:, i] - L0[i], .05)),
                    score_lower_change_p50=float(np.quantile(L[:, i] - L0[i], .5)),
                    score_lower_change_p95=float(np.quantile(L[:, i] - L0[i], .95)),
                    score_upper_change_p05=float(np.quantile(U[:, i] - U0[i], .05)),
                    score_upper_change_p50=float(np.quantile(U[:, i] - U0[i], .5)),
                    score_upper_change_p95=float(np.quantile(U[:, i] - U0[i], .95))))
        # Separate sensitivity to preferences: future multipliers now deterministic.
        sampled_w = np.random.default_rng(np.random.SeedSequence(WEIGHT_SEED)).dirichlet(100 * w, DRAWS)
        for label, changes in SCENARIOS.items():
            a, b = transform(lo, hi, multipliers(lo.shape, changes), means)
            L, U = score_many(a, sampled_w), score_many(b, sampled_w)
            _, credit, rank, possible = decision(L, U)
            for i, city in enumerate(cities):
                weight_mc.append(dict(random_source='weights_only', scenario=label,
                    weight_reference=ref, concentration=100, city=city,
                    recommendation_frequency=float(credit[:, i].mean()),
                    possible_champion_frequency=float(possible[:, i].mean()),
                    mean_decision_rank=float(rank[:, i].mean())))
    checks['future_mc_independent_scalar_draws_per_setting'] = 3
    checks['future_mc_settings'] = 6
    # Same weights as V121: do not reinterpret a changed random stream as evidence.
    weight_table = pd.DataFrame(weight_mc)
    old_mc = pd.read_csv(ROOT / 'results/task4_user_v121_revision/mc_city_summary.csv',
                         float_precision='round_trip')
    for ref, _ in references:
        old = old_mc[(old_mc.scenario == 'after_conditional') &
                     (old_mc.weight_reference == ref) & (old_mc.concentration == 100)].set_index('city').loc[cities]
        new = weight_table[(weight_table.scenario == 'baseline') &
                           (weight_table.weight_reference == ref)].set_index('city').loc[cities]
        for current, previous in [('recommendation_frequency', 'minimax_recommendation_frequency'),
                                  ('mean_decision_rank', 'mean_decision_rank'),
                                  ('possible_champion_frequency', 'possible_champion_frequency')]:
            np.testing.assert_array_equal(new[current], old[previous])
    checks['weight_mc_baseline_exactly_matches_V121_all_cities_both_references'] = True
    for path, digest in protected.items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    OUT.mkdir(exist_ok=True, parents=True)
    pd.concat(rank_rows, ignore_index=True).to_csv(OUT / 'ranks.csv', index=False)
    pd.DataFrame(bound_rows).to_csv(OUT / 'utility_bounds.csv', index=False)
    pd.DataFrame(thresholds).to_csv(OUT / 'thresholds.csv', index=False)
    pd.DataFrame(scans).to_csv(OUT / 'threshold_scan.csv', index=False)
    pd.DataFrame(mc).to_csv(OUT / 'future_mc_city_summary.csv', index=False)
    weight_table.to_csv(OUT / 'weight_mc_city_summary.csv', index=False)
    summary = dict(version='V122', baseline='16-city V121 conditional evidence',
        interpretation='Conditional stress tests without a calendar date; not a calibrated forecast or historical trend fit.',
        deterministic_raw_changes=SCENARIOS,
        future_mc=dict(draws=DRAWS, seed=SEED, weight_randomness=False,
            common_distribution='C~Uniform[0,1], one per draw, shared across all cities and affected criteria',
            city_distribution='I_i~Uniform[0,1], independent by city and draw, shared across affected criteria within a city',
            shock_magnitude='.05*C+.05*I_i in [0,.1]',
            raw_multipliers='1+shock_magnitude for resource_expansion/living_pressure; 1-shock_magnitude for balanced_improvement',
            calibration='Analyst-declared uncalibrated stress distribution; frequencies conditional on this distribution, not actual future winning probabilities.'),
        weight_mc=dict(draws=DRAWS, seed=WEIGHT_SEED, concentration=100,
            distribution='Dirichlet(100*reference_weights)', future_shock_randomness=False,
            interpretation='Preference sensitivity, separate from future shock simulation'),
        travel_rule='Known submitted means use Jensen exp(-r*mean/30), upper1. Mean-utility-only bounds [L,U] use [L,U**r] for r<1 and [L**r,U] for r>1. Full unknowns stay[0,1]. Moment outer envelopes are generally not reversible.',
        scope='Conditional mixed-vintage resources; same fixed utility anchors. Facility growth assumes relevant supply follows scenario multiplier; inventories remain lower-bound proxies. No missing value is randomly filled.',
        threshold_rule='Only the focal city changes PTR, PM2.5 and travel raw scale by a common r in[.5,1]. Compare its maximum regret with the best of all other cities; threshold is a conditional recommendation switch, not an identified performance win.',
        weights={ref: w.tolist() for ref, w in references}, source_sha256=protected,
        checks=checks, scenarios=summaries, thresholds=thresholds)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(dict(scenarios=summaries, thresholds=thresholds), indent=2))


if __name__ == '__main__':
    main()
