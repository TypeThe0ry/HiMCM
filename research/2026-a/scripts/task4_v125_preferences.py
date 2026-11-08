"""Controlled migration of V122 analyst preferences from V121 to V124 evidence."""
from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_ahp_mc_baseline import interval_metrics, rank_metrics, score_many
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import revised_bounds as control_bounds
from task4_user_v124_revision import MANIFEST, revised_bounds
from task4_v122_preferences import (
    CONCENTRATIONS, DRAWS, MULTIPLIERS, SEED, digest, independent_decisions, profile,
)
from task4_v5_model import NAMES, ROOT, weights

OUT = ROOT / 'results/task4_v125_preferences'
OLD = ROOT / 'results/task4_v122_preferences'
MC_COLUMNS = ['minimax_recommendation_frequency', 'mean_decision_rank',
              'top3_decision_frequency', 'possible_champion_frequency',
              'necessary_champion_frequency']


def calculate(cities, lo, hi):
    """Retain the frozen V122 output schema and recheck every simulation draw."""
    base = weights(.1)
    baseline = evaluate(cities, lo, hi, base)
    ranks, weight_rows, mc_rows, reports, matrices = [], [], [], [], {}
    for name in MULTIPLIERS:
        w, multiplier, matrix, document, diagnostic = profile(name, base)
        matrices[name] = dict(**document, raw_multiplier=multiplier.tolist(),
                              weights=w.tolist(), diagnostic=diagnostic)
        weight_rows.extend(dict(profile=name, indicator=n, baseline_weight=float(base[j]),
            raw_multiplier=float(multiplier[j]), weight=float(w[j]),
            multiplier_source='analyst-designed') for j, n in enumerate(NAMES))
        frame = evaluate(cities, lo, hi, w)
        lower, upper, regret, possible, necessary = independent_decisions(lo, hi, w)
        expected_rank = np.array([1 + np.sum(regret < x) for x in regret])
        for col, values in [('score_lower', lower), ('score_upper', upper), ('max_regret', regret),
                            ('decision_rank', expected_rank), ('possible_champion', possible),
                            ('necessary_champion', necessary)]:
            np.testing.assert_allclose(frame[col], values, atol=1e-12, rtol=0)
        frame['baseline_decision_rank'] = baseline.decision_rank
        frame['rank_change_positive_improves'] = baseline.decision_rank - frame.decision_rank
        ranks.append(frame.assign(profile=name))
        settings = []
        for concentration in CONCENTRATIONS:
            sampled = np.random.default_rng(np.random.SeedSequence([SEED, concentration])).dirichlet(
                concentration * w, size=DRAWS)
            l, u = score_many(lo, sampled), score_many(hi, sampled)
            rr, pp, nn, _, _ = interval_metrics(l, u)
            mc_rank, recommendation, top3 = rank_metrics(rr, descending=False)
            np.testing.assert_allclose(recommendation.sum(1), 1, atol=1e-12, rtol=0)
            np.testing.assert_allclose(top3.sum(1), 3, atol=1e-12, rtol=0)
            # Separate norm calculation and explicit self-excluded competitors.
            il, iu, ir, ip, inn = independent_decisions(lo, hi, sampled)
            for actual, expected in [(l, il), (u, iu), (rr, ir)]:
                np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
            np.testing.assert_array_equal(pp, ip)
            np.testing.assert_array_equal(nn, inn)
            for i, city in enumerate(cities):
                ahead = np.sum(ir < ir[:, i, None] - 1e-12, axis=1)
                tied = np.sum(np.abs(ir - ir[:, i, None]) <= 1e-12, axis=1)
                expected_arrays = [np.clip((1 - ahead) / tied, 0, 1),
                                   1 + ahead + (tied - 1) / 2,
                                   np.clip((3 - ahead) / tied, 0, 1)]
                for actual_draws, expected_draws in zip(
                        [recommendation[:, i], mc_rank[:, i], top3[:, i]], expected_arrays):
                    np.testing.assert_array_equal(actual_draws, expected_draws)
                expected = [x.mean() for x in expected_arrays]
                actual = [recommendation[:, i].mean(), mc_rank[:, i].mean(), top3[:, i].mean()]
                np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
                mc_rows.append(dict(profile=name, city=city, draws=DRAWS, concentration=concentration,
                    minimax_recommendation_frequency=float(actual[0]),
                    mean_decision_rank=float(actual[1]), top3_decision_frequency=float(actual[2]),
                    possible_champion_frequency=float(pp[:, i].mean()),
                    necessary_champion_frequency=float(nn[:, i].mean())))
            settings.append(dict(concentration=concentration,
                most_recommended=cities[int(np.argmax(recommendation.mean(0)))],
                most_recommended_frequency=float(recommendation.mean(0).max())))
        reports.append(dict(profile=name,
            minimax_choices=frame.loc[frame.decision_rank == 1, 'city'].tolist(),
            possible_champions=frame.loc[frame.possible_champion, 'city'].tolist(),
            necessary_champions=frame.loc[frame.necessary_champion, 'city'].tolist(),
            kendall_tau_b_vs_baseline=float(kendalltau(baseline.decision_rank, frame.decision_rank).statistic),
            mean_score_interval_width=float((frame.score_upper - frame.score_lower).mean()),
            consistency_ratio=diagnostic['CR'], mc_settings=settings))
    mc = pd.DataFrame(mc_rows)
    baseline_mc = mc[mc.profile == 'baseline'].set_index(['concentration', 'city'])
    for col in MC_COLUMNS:
        mc[col + '_change_vs_baseline'] = [row[col] - baseline_mc.loc[(row['concentration'], row['city']), col]
                                         for row in mc.to_dict('records')]
    return dict(ranks=pd.concat(ranks, ignore_index=True), weights=pd.DataFrame(weight_rows),
                mc=mc, profiles=reports, scenario_matrices=matrices)


def exact_control(control, lo, hi, cities):
    """Read round-trip floats so CSV decimal parsing cannot mimic a scientific drift."""
    for key, filename in [('ranks', 'ranks.csv'), ('weights', 'weights.csv'), ('mc', 'mc_city_summary.csv')]:
        expected = pd.read_csv(OLD / filename, float_precision='round_trip')
        pd.testing.assert_frame_equal(control[key], expected, check_exact=True)
    expected_bounds = pd.read_csv(OLD / 'utility_bounds.csv', float_precision='round_trip')
    actual_bounds = pd.DataFrame([dict(city=c, indicator=n, lower=lo[i, j], upper=hi[i, j])
                                  for i, c in enumerate(cities) for j, n in enumerate(NAMES)])
    pd.testing.assert_frame_equal(actual_bounds, expected_bounds, check_exact=True)
    assert control['scenario_matrices'] == json.loads((OLD / 'scenario_matrices.json').read_text())
    expected_summary = json.loads((OLD / 'summary.json').read_text())
    assert control['profiles'] == expected_summary['profiles']


def main():
    paths = [SOURCE, MANIFEST, Path(__file__),
             ROOT / 'design/task4_user_current_model.json',
             ROOT / 'design/task4_user_v121_admissions.json',
             ROOT / 'scripts/task4_user_v124_revision.py',
             ROOT / 'scripts/task4_user_v121_revision.py',
             ROOT / 'scripts/task4_v122_preferences.py',
             ROOT / 'scripts/task4_ahp_mc_baseline.py',
             ROOT / 'scripts/task4_interval_decision.py',
             ROOT / 'scripts/task4_v5_model.py',
             ROOT / 'scripts/task4_user_city_indicators.py',
             *[p for p in OLD.iterdir() if p.is_file()],
             ROOT / 'results/task4_user_v124_revision/current_ranks.csv',
             ROOT / 'results/task4_user_v124_revision/mc_city_summary.csv']
    source_hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    # Actual simulations rarely tie; explicit cases check fractional slot credit.
    synthetic = np.array([[0., 0., 1., 2.], [0., 0., 0., 0.], [0., 1., 1., 1.]])
    synthetic_rank, synthetic_first, synthetic_top3 = rank_metrics(synthetic, descending=False)
    np.testing.assert_array_equal(synthetic_rank,
        [[1.5, 1.5, 3., 4.], [2.5, 2.5, 2.5, 2.5], [1., 3., 3., 3.]])
    np.testing.assert_array_equal(synthetic_first,
        [[.5, .5, 0., 0.], [.25, .25, .25, .25], [1., 0., 0., 0.]])
    np.testing.assert_allclose(synthetic_top3,
        [[1., 1., 1., 0.], [.75, .75, .75, .75], [1., 2 / 3, 2 / 3, 2 / 3]], atol=1e-14, rtol=0)
    f0, l0, h0 = control_bounds()
    frame, lo, hi = revised_bounds()
    pd.testing.assert_frame_equal(frame, f0, check_exact=True)
    cities = frame.city.tolist()
    assert len(cities) == 16 and lo.shape == (16, 10)
    original = np.stack([lo, hi]).copy()
    assert np.count_nonzero((lo != l0) | (hi != h0)) == 2
    assert np.all(lo >= l0) and np.all(hi <= h0)
    control = calculate(cities, l0, h0)
    exact_control(control, l0, h0, cities)
    current = calculate(cities, lo, hi)
    pd.testing.assert_frame_equal(current['weights'], control['weights'], check_exact=True)
    assert current['scenario_matrices'] == control['scenario_matrices']
    saved = pd.read_csv(ROOT / 'results/task4_user_v124_revision/current_ranks.csv',
                        float_precision='round_trip')
    baseline = current['ranks'][current['ranks'].profile == 'baseline']
    saved = saved[(saved.scenario == 'after_conditional') & (saved.weight_reference == 'fixed')]
    cols = [c for c in baseline.columns if c not in ['profile', 'baseline_decision_rank', 'rank_change_positive_improves']]
    pd.testing.assert_frame_equal(baseline[cols], saved[cols].reset_index(drop=True), check_exact=True)
    saved_mc = pd.read_csv(ROOT / 'results/task4_user_v124_revision/mc_city_summary.csv',
                          float_precision='round_trip')
    for concentration in CONCENTRATIONS:
        old = saved_mc[(saved_mc.scenario == 'after_conditional') & (saved_mc.weight_reference == 'fixed') &
                       (saved_mc.concentration == concentration)].set_index('city').loc[cities]
        new = current['mc'][(current['mc'].profile == 'baseline') &
                            (current['mc'].concentration == concentration)].set_index('city').loc[cities]
        for col in ['minimax_recommendation_frequency', 'mean_decision_rank', 'possible_champion_frequency']:
            np.testing.assert_array_equal(new[col], old[col])
    comparison = current['ranks'].merge(control['ranks'], on=['profile', 'city'], suffixes=('_v124', '_v121'))
    comparison['decision_rank_change_positive_improves'] = comparison.decision_rank_v121 - comparison.decision_rank_v124
    comparison['score_lower_change_v124_minus_v121'] = comparison.score_lower_v124 - comparison.score_lower_v121
    comparison['score_upper_change_v124_minus_v121'] = comparison.score_upper_v124 - comparison.score_upper_v121
    comparison['width_reduction'] = (comparison.score_upper_v121 - comparison.score_lower_v121 -
                                    comparison.score_upper_v124 + comparison.score_lower_v124)
    mc_comparison = current['mc'].merge(control['mc'], on=['profile', 'city', 'concentration', 'draws'],
                                       suffixes=('_v124', '_v121'))
    for col in MC_COLUMNS:
        mc_comparison[col + '_change_v124_minus_v121'] = mc_comparison[col + '_v124'] - mc_comparison[col + '_v121']
    comparisons = []
    for name in MULTIPLIERS:
        r = comparison[comparison.profile == name]
        m = mc_comparison[mc_comparison.profile == name]
        old_profile = next(x for x in control['profiles'] if x['profile'] == name)
        new_profile = next(x for x in current['profiles'] if x['profile'] == name)
        comparisons.append(dict(profile=name, old_V122_input='V121 user16', new_V125_input='V124 user16',
            old_minimax_choices=old_profile['minimax_choices'], new_minimax_choices=new_profile['minimax_choices'],
            changed_decision_ranks=int(np.count_nonzero(r.decision_rank_change_positive_improves)),
            kendall_tau_b_between_evidence_versions=float(kendalltau(r.decision_rank_v121, r.decision_rank_v124).statistic),
            old_mean_score_width=old_profile['mean_score_interval_width'],
            new_mean_score_width=new_profile['mean_score_interval_width'],
            changed_mc_city_rows=int(np.any(m[[c + '_change_v124_minus_v121' for c in MC_COLUMNS]].to_numpy() != 0, axis=1).sum()),
            largest_absolute_recommendation_frequency_change=float(m.minimax_recommendation_frequency_change_v124_minus_v121.abs().max()),
            largest_absolute_mean_rank_change=float(m.mean_decision_rank_change_v124_minus_v121.abs().max())))
    for path, expected in source_hashes.items():
        assert digest(ROOT / path) == expected, path
    _, check_l, check_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([check_l, check_u]))
    OUT.mkdir(parents=True, exist_ok=True)
    current['ranks'].to_csv(OUT / 'ranks.csv', index=False)
    current['weights'].to_csv(OUT / 'weights.csv', index=False)
    current['mc'].to_csv(OUT / 'mc_city_summary.csv', index=False)
    control['ranks'].to_csv(OUT / 'control_v121_ranks.csv', index=False)
    control['mc'].to_csv(OUT / 'control_v121_mc_city_summary.csv', index=False)
    comparison.to_csv(OUT / 'v122_rank_comparison.csv', index=False)
    mc_comparison.to_csv(OUT / 'v122_mc_comparison.csv', index=False)
    pd.DataFrame([dict(city=c, indicator=n, lower=lo[i, j], upper=hi[i, j])
                  for i, c in enumerate(cities) for j, n in enumerate(NAMES)]).to_csv(OUT / 'utility_bounds.csv', index=False)
    (OUT / 'scenario_matrices.json').write_text(json.dumps(current['scenario_matrices'], indent=2) + '\n')
    for name, document in current['scenario_matrices'].items():
        pd.DataFrame(document['matrix'], index=NAMES, columns=NAMES).rename_axis('indicator').to_csv(OUT / f'{name}_matrix.csv')
    summary = dict(version='V125', input_version='V124 user16', control_input='V121 user16',
        profiles=current['profiles'],
        preference_evidence='Unchanged analyst-designed2x multipliers; no student survey, expert elicitation or measured age preference',
        ahp_interpretation='Exact-ratio AHP weight reconstruction; CR assesses algebraic consistency only',
        seed=SEED, concentrations=list(CONCENTRATIONS), draws_per_setting=DRAWS,
        total_draws=3 * len(CONCENTRATIONS) * DRAWS,
        total_draws_current=3 * len(CONCENTRATIONS) * DRAWS,
        total_draws_control=3 * len(CONCENTRATIONS) * DRAWS,
        random_generator='default_rng(SeedSequence([20261108, concentration])) reset per profile and concentration',
        mc_interpretation='Weight-conditional decision frequencies; not actual winning probabilities. Evidence intervals are not sampled.',
        ranking_policy='Deterministic interval minimax regret remains primary; mean ranks and frequencies are sensitivity summaries.',
        controlled_v122_comparison='V121 control exactly reproduces frozen V122 ranks, MC, weights, matrices and profile summaries. Same weights/seeds/draws applied to V124; only two new facility lower bounds differ.',
        historical_comparison=comparisons, source_hashes=source_hashes)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    audit = dict(status='pass', main_input_shape=[16, 10], changed_evidence_cells=2,
        V121_control_exactly_matches_frozen_V122=['ranks', 'weights', 'mc_all9_settings_all144_city_rows',
                                                'all160_bounds', 'scenario_matrices', 'profile_summaries'],
        deterministic_profile_checks=6, independent_mc_settings=18, draws_per_setting=DRAWS,
        explicit_fractional_tie_cases=3,
        every_draw_independent_tie_credits_ranks_and_top3_checked=True,
        independent_quantities=['weighted norms', 'self-excluded regret', 'possible/necessary champion',
                                'tie-credit recommendation', 'mean rank', 'top3 membership'],
        unchanged_profiles_weights_seeds_and_draws=True,
        V124_baseline_ranks_and_all3_MC_settings_exactly_match=True,
        source_CSV_registry_legacy_files_and_hashes_unchanged=True,
        V124_all160_bounds_exactly_unchanged=True)
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(dict(profiles=current['profiles'], comparison=comparisons), indent=2))


if __name__ == '__main__':
    main()
