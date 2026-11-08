"""Analyst AHP weight scenarios on frozen V121 user16 evidence intervals."""
import hashlib
import json

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_ahp_mc_baseline import ahp_weights, interval_metrics, rank_metrics, score_many
from task4_user_city_indicators import SOURCE, evaluate
from task4_user_v121_revision import MANIFEST, revised_bounds
from task4_v5_model import NAMES, ROOT, weights

OUT = ROOT/'results/task4_v122_preferences'
HISTORICAL = ROOT/'results/task4_v119_preferences'
MULTIPLIERS = {'baseline': {},
              'education_priority': {'upper_secondary_ptr': 2, 'research_he_density': 2},
              'independent_living_priority': {'travel': 2, 'public_transport_density': 2}}
SEED, DRAWS, CONCENTRATIONS = 20261108, 10000, (20, 100, 500)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_scores(z, w):
    a = np.sqrt(np.sum(np.asarray(w)[..., None, :]*z*z, axis=-1))
    b = np.sqrt(np.sum(np.asarray(w)[..., None, :]*(1-z)**2, axis=-1))
    return 100*a/(a+b)


def independent_decisions(lo, hi, w):
    lower, upper = independent_scores(lo, w), independent_scores(hi, w)
    n = lower.shape[-1]
    regrets, possible, necessary = [], [], []
    for i in range(n):
        other = [k for k in range(n) if k != i]
        top_u, top_l = upper[..., other].max(axis=-1), lower[..., other].max(axis=-1)
        regrets.append(np.maximum(0, top_u-lower[..., i]))
        possible.append(upper[..., i] >= top_l-1e-12)
        necessary.append(lower[..., i] >= top_u-1e-12)
    return lower, upper, np.stack(regrets, axis=-1), np.stack(possible, axis=-1), np.stack(necessary, axis=-1)


def profile(name, base):
    multiplier = np.array([MULTIPLIERS[name].get(n, 1) for n in NAMES], float)
    w = base*multiplier
    w /= w.sum()
    matrix = w[:, None]/w[None, :]
    document = dict(source='Declared analyst multipliers applied to inherited policy weights',
                    respondents='None; no student survey or expert elicitation',
                    elicitation_date='Not elicited',
                    judgment_method='Exact ratios A_ij=w_i/w_j; not age-specific measured preferences',
                    indicators=NAMES, matrix=matrix.tolist())
    recovered, diagnostic = ahp_weights(document, NAMES)
    np.testing.assert_allclose(recovered, w, atol=1e-12, rtol=0)
    np.testing.assert_allclose(matrix*matrix.T, 1, atol=1e-12, rtol=0)
    np.testing.assert_allclose(matrix @ w, 10*w, atol=1e-12, rtol=0)
    assert np.all(matrix > 0) and np.array_equal(matrix.diagonal(), np.ones(10))
    assert np.linalg.matrix_rank(matrix, tol=1e-10) == 1
    assert diagnostic['CR'] < 1e-10
    # Check transitivity independently of the eigenvector routine.
    np.testing.assert_allclose(matrix[:, :, None]*matrix[None, :, :],
                               np.broadcast_to(matrix[:, None, :], (10, 10, 10)), atol=1e-12, rtol=0)
    diagnostic.update(positive=True, unit_diagonal=True, reciprocal=True,
                      rank_one=True, multiplicative_transitivity=True)
    return w, multiplier, matrix, document, diagnostic


def main():
    paths = [SOURCE, MANIFEST, ROOT/'scripts/task4_user_v121_revision.py',
             ROOT/'results/task4_user_v121_revision/current_ranks.csv',
             ROOT/'results/task4_user_v121_revision/mc_city_summary.csv',
             HISTORICAL/'weights.csv', HISTORICAL/'ranks.csv', HISTORICAL/'mc_city_summary.csv']
    source_hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    source, lo, hi = revised_bounds()
    original = np.stack([lo, hi]).copy()
    cities = source.city.tolist()
    assert len(cities) == 16 and lo.shape == (16, 10)
    base = weights(.1)
    np.testing.assert_array_equal(base, np.array([.1125]*6+[.05,.1125,.1125,.05]))
    baseline = evaluate(cities, lo, hi, base)
    saved = pd.read_csv(ROOT/'results/task4_user_v121_revision/current_ranks.csv')
    saved = saved[(saved.weight_reference == 'fixed') & (saved.scenario == 'after_conditional')]
    pd.testing.assert_frame_equal(baseline, saved[baseline.columns].reset_index(drop=True),
                                  check_exact=False, rtol=1e-12, atol=1e-12)
    historical_weights = pd.read_csv(HISTORICAL/'weights.csv')
    OUT.mkdir(parents=True, exist_ok=True)
    ranks, weight_rows, mc_rows, reports, documents = [], [], [], [], {}
    for name in MULTIPLIERS:
        w, multiplier, matrix, doc, diagnostic = profile(name, base)
        prior_w = historical_weights[historical_weights.profile == name].set_index('indicator').loc[NAMES]
        np.testing.assert_allclose(w, prior_w.weight, atol=1e-15, rtol=0)
        np.testing.assert_array_equal(multiplier, prior_w.raw_multiplier)
        documents[name] = dict(**doc, raw_multiplier=multiplier.tolist(), weights=w.tolist(), diagnostic=diagnostic)
        pd.DataFrame(matrix, index=NAMES, columns=NAMES).rename_axis('indicator').to_csv(OUT/f'{name}_matrix.csv')
        weight_rows.extend(dict(profile=name, indicator=n, baseline_weight=float(base[j]),
                                raw_multiplier=float(multiplier[j]), weight=float(w[j]),
                                multiplier_source='analyst-designed') for j, n in enumerate(NAMES))
        frame = evaluate(cities, lo, hi, w)
        lower, upper, regret, possible, necessary = independent_decisions(lo, hi, w)
        expected_rank = np.array([1+np.sum(regret < x) for x in regret])
        for col, values in [('score_lower', lower), ('score_upper', upper), ('max_regret', regret),
                            ('decision_rank', expected_rank), ('possible_champion', possible),
                            ('necessary_champion', necessary)]:
            np.testing.assert_allclose(frame[col], values, atol=1e-12, rtol=0)
        frame['baseline_decision_rank'] = baseline.decision_rank
        frame['rank_change_positive_improves'] = baseline.decision_rank-frame.decision_rank
        ranks.append(frame.assign(profile=name))
        mc_report = []
        for concentration in CONCENTRATIONS:
            sampled = np.random.default_rng(np.random.SeedSequence([SEED, concentration])).dirichlet(
                concentration*w, size=DRAWS)
            l, u = score_many(lo, sampled), score_many(hi, sampled)
            rr, pp, nn, _, _ = interval_metrics(l, u)
            mc_rank, recommendation, top3 = rank_metrics(rr, descending=False)
            np.testing.assert_allclose(recommendation.sum(axis=1), 1, atol=1e-12, rtol=0)
            np.testing.assert_allclose(top3.sum(axis=1), 3, atol=1e-12, rtol=0)
            # Independent broadcast score and city-by-city tie accounting.
            il, iu, ir, ip, inn = independent_decisions(lo, hi, sampled)
            for actual, expected in [(l, il), (u, iu), (rr, ir)]:
                np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
            np.testing.assert_array_equal(pp, ip)
            np.testing.assert_array_equal(nn, inn)
            for i, city in enumerate(cities):
                ahead = np.sum(ir < ir[:, i, None]-1e-12, axis=1)
                tied = np.sum(np.abs(ir-ir[:, i, None]) <= 1e-12, axis=1)
                expected = [np.mean(np.clip((1-ahead)/tied, 0, 1)),
                            np.mean(1+ahead+(tied-1)/2),
                            np.mean(np.clip((3-ahead)/tied, 0, 1))]
                actual = [recommendation[:, i].mean(), mc_rank[:, i].mean(), top3[:, i].mean()]
                np.testing.assert_allclose(actual, expected, atol=1e-12, rtol=0)
                mc_rows.append(dict(profile=name, city=city, draws=DRAWS, concentration=concentration,
                                    minimax_recommendation_frequency=float(actual[0]),
                                    mean_decision_rank=float(actual[1]),
                                    top3_decision_frequency=float(actual[2]),
                                    possible_champion_frequency=float(pp[:, i].mean()),
                                    necessary_champion_frequency=float(nn[:, i].mean())))
            mc_report.append(dict(concentration=concentration,
                                  most_recommended=cities[int(np.argmax(recommendation.mean(axis=0)))],
                                  most_recommended_frequency=float(recommendation.mean(axis=0).max())))
        reports.append(dict(profile=name,
                            minimax_choices=frame.loc[frame.decision_rank == 1, 'city'].tolist(),
                            possible_champions=frame.loc[frame.possible_champion, 'city'].tolist(),
                            necessary_champions=frame.loc[frame.necessary_champion, 'city'].tolist(),
                            kendall_tau_b_vs_baseline=float(kendalltau(baseline.decision_rank, frame.decision_rank).statistic),
                            mean_score_interval_width=float((frame.score_upper-frame.score_lower).mean()),
                            consistency_ratio=diagnostic['CR'], mc_settings=mc_report))
    all_ranks, mc = pd.concat(ranks, ignore_index=True), pd.DataFrame(mc_rows)
    baseline_mc = mc[mc.profile == 'baseline'].set_index(['concentration', 'city'])
    for col in ['minimax_recommendation_frequency', 'mean_decision_rank', 'top3_decision_frequency',
                'possible_champion_frequency', 'necessary_champion_frequency']:
        mc[col+'_change_vs_baseline'] = [row[col]-baseline_mc.loc[(row['concentration'], row['city']), col]
                                        for row in mc.to_dict('records')]
    prior_mc = pd.read_csv(ROOT/'results/task4_user_v121_revision/mc_city_summary.csv')
    for concentration in CONCENTRATIONS:
        rows = prior_mc[(prior_mc.scenario == 'after_conditional') & (prior_mc.weight_reference == 'fixed') &
                        (prior_mc.concentration == concentration)].set_index('city').loc[cities]
        for col in ['minimax_recommendation_frequency', 'mean_decision_rank', 'possible_champion_frequency']:
            np.testing.assert_allclose(baseline_mc.loc[concentration].loc[cities, col], rows[col], atol=1e-12, rtol=0)
    old_ranks = pd.read_csv(HISTORICAL/'ranks.csv')
    old_mc = pd.read_csv(HISTORICAL/'mc_city_summary.csv')
    comparison = all_ranks.merge(old_ranks, on=['profile', 'city'], suffixes=('_v121', '_v118'))
    comparison['decision_rank_change_positive_improves'] = comparison.decision_rank_v118-comparison.decision_rank_v121
    comparison['score_width_v118'] = comparison.score_upper_v118-comparison.score_lower_v118
    comparison['score_width_v121'] = comparison.score_upper_v121-comparison.score_lower_v121
    comparison['width_reduction'] = comparison.score_width_v118-comparison.score_width_v121
    assert np.all(comparison.score_lower_v121 >= comparison.score_lower_v118-1e-12)
    assert np.all(comparison.score_upper_v121 <= comparison.score_upper_v118+1e-12)
    historical_comparison = []
    for name in MULTIPLIERS:
        rows = comparison[comparison.profile == name]
        historical_comparison.append(dict(profile=name,
            old_V119_input='V118 user16', new_V122_input='V121 user16',
            old_minimax_choices=rows.loc[rows.decision_rank_v118 == 1, 'city'].tolist(),
            new_minimax_choices=rows.loc[rows.decision_rank_v121 == 1, 'city'].tolist(),
            old_mean_score_width=float(rows.score_width_v118.mean()),
            new_mean_score_width=float(rows.score_width_v121.mean()),
            kendall_tau_b_between_evidence_versions=float(kendalltau(rows.decision_rank_v118, rows.decision_rank_v121).statistic)))
    comparison_mc = mc[mc.concentration == 100].merge(old_mc, on=['profile', 'city'], suffixes=('_v121', '_v118'))
    for col in ['minimax_recommendation_frequency', 'mean_decision_rank', 'possible_champion_frequency']:
        comparison_mc[col+'_change_from_v119'] = comparison_mc[col+'_v121']-comparison_mc[col+'_v118']
    all_ranks.to_csv(OUT/'ranks.csv', index=False)
    pd.DataFrame(weight_rows).to_csv(OUT/'weights.csv', index=False)
    mc.to_csv(OUT/'mc_city_summary.csv', index=False)
    comparison.to_csv(OUT/'v119_rank_comparison.csv', index=False)
    comparison_mc.to_csv(OUT/'v119_mc_comparison_k100.csv', index=False)
    pd.DataFrame([dict(city=c, indicator=n, lower=lo[i, j], upper=hi[i, j])
                  for i, c in enumerate(cities) for j, n in enumerate(NAMES)]).to_csv(OUT/'utility_bounds.csv', index=False)
    (OUT/'scenario_matrices.json').write_text(json.dumps(documents, indent=2)+'\n')
    summary = dict(version='V122', input_version='V121 user16', profiles=reports,
                   preference_evidence='Analyst-designed 2x multipliers, no student survey, expert elicitation or measured age preference',
                   ahp_interpretation='Exact-ratio weight reconstruction; CR assesses algebraic consistency only',
                   seed=SEED, concentrations=list(CONCENTRATIONS), draws_per_setting=DRAWS,
                   total_draws=3*len(CONCENTRATIONS)*DRAWS,
                   random_generator='default_rng(SeedSequence([20261108, concentration])) reset per profile and concentration',
                   mc_interpretation='Weight-conditional decision frequencies, not actual winning probabilities. Evidence intervals not sampled.',
                   ranking_policy='Deterministic interval minimax regret remains primary; MC mean ranks are sensitivity summaries only',
                   historical_comparison=historical_comparison,
                   controlled_v119_comparison='Same profile weights, seed and k100 distribution; old V119 uses V118 evidence, new V122 uses V121 evidence. k20/k500 and top3 have no old V119 counterpart.',
                   source_hashes=source_hashes)
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    for path, expected in source_hashes.items():
        assert digest(ROOT/path) == expected, path
    _, check_l, check_u = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([check_l, check_u]))
    (OUT/'audit.json').write_text(json.dumps(dict(status='pass', deterministic_profile_checks=3,
        ahp_properties_checked=['positive', 'unit diagonal', 'reciprocal', 'eigenvector recovery', 'rank one', 'multiplicative transitivity', 'CR near zero'],
        independent_mc_settings=9, draws_per_setting=DRAWS, independent_mc_city_rows=144,
        independent_quantities=['scores', 'self-excluded regret', 'recommendation frequency', 'mean rank', 'top3 frequency', 'possible/necessary champion'],
        V121_baseline_ranks_and_three_MC_settings_reconciled=True,
        historical_profile_weights_identical=True, source_hashes_unchanged=True,
        V121_all160_bounds_exactly_unchanged=True), indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
