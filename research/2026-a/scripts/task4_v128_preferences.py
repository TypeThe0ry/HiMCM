"""Controlled migration of unchanged analyst preferences to frozen V127 evidence."""
from pathlib import Path
import json

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_ahp_mc_baseline import rank_metrics
from task4_user_city_indicators import SOURCE
from task4_user_v121_revision import revised_bounds as control_bounds
from task4_user_v124_revision import revised_bounds as previous_bounds
from task4_user_v127_revision import MANIFEST, revised_bounds
from task4_v122_preferences import CONCENTRATIONS, DRAWS, MULTIPLIERS, SEED, digest
from task4_v125_preferences import MC_COLUMNS, calculate, exact_control
from task4_v5_model import NAMES, ROOT

OUT = ROOT / 'results/task4_v128_preferences'
OLD = ROOT / 'results/task4_v125_preferences'
SNAPSHOT = ROOT / 'design/task4_user_v127_snapshot.json'


def frozen_previous():
    return dict(ranks=pd.read_csv(OLD / 'ranks.csv', float_precision='round_trip'),
                weights=pd.read_csv(OLD / 'weights.csv', float_precision='round_trip'),
                mc=pd.read_csv(OLD / 'mc_city_summary.csv', float_precision='round_trip'),
                profiles=json.loads((OLD / 'summary.json').read_text())['profiles'],
                scenario_matrices=json.loads((OLD / 'scenario_matrices.json').read_text()))


def compare(current, old, old_version):
    suffix = ('_v127', '_' + old_version)
    rank = current['ranks'].merge(old['ranks'], on=['profile', 'city'], suffixes=suffix,
                                  validate='one_to_one')
    rank['decision_rank_change_positive_improves'] = rank['decision_rank_' + old_version] - rank.decision_rank_v127
    for end in ['lower', 'upper']:
        rank[f'score_{end}_change_v127_minus_{old_version}'] = rank[f'score_{end}_v127'] - rank[f'score_{end}_{old_version}']
    rank['width_reduction'] = (rank['score_upper_' + old_version] - rank['score_lower_' + old_version]
                               - rank.score_upper_v127 + rank.score_lower_v127)
    mc = current['mc'].merge(old['mc'], on=['profile', 'city', 'concentration', 'draws'],
                             suffixes=suffix, validate='one_to_one')
    for col in MC_COLUMNS:
        mc[f'{col}_change_v127_minus_{old_version}'] = mc[col + '_v127'] - mc[col + '_' + old_version]
    reports = []
    for name in MULTIPLIERS:
        r, m = rank[rank.profile == name], mc[mc.profile == name]
        before = next(p for p in old['profiles'] if p['profile'] == name)
        after = next(p for p in current['profiles'] if p['profile'] == name)
        reports.append(dict(profile=name, old_input=old_version, new_input='v127',
            old_minimax_choices=before['minimax_choices'], new_minimax_choices=after['minimax_choices'],
            changed_decision_ranks=int(np.count_nonzero(r.decision_rank_change_positive_improves)),
            kendall_tau_b_between_evidence_versions=float(kendalltau(r['decision_rank_' + old_version], r.decision_rank_v127).statistic),
            old_mean_score_width=before['mean_score_interval_width'], new_mean_score_width=after['mean_score_interval_width'],
            old_tau_vs_own_baseline=before['kendall_tau_b_vs_baseline'],
            new_tau_vs_own_baseline=after['kendall_tau_b_vs_baseline'],
            changed_mc_city_rows=int(np.any(m[[f'{c}_change_v127_minus_{old_version}' for c in MC_COLUMNS]].to_numpy() != 0, axis=1).sum()),
            largest_absolute_recommendation_frequency_change=float(m[f'minimax_recommendation_frequency_change_v127_minus_{old_version}'].abs().max()),
            largest_absolute_mean_rank_change=float(m[f'mean_decision_rank_change_v127_minus_{old_version}'].abs().max())))
    return rank, mc, reports


def main():
    snapshot = json.loads(SNAPSHOT.read_text())
    assert snapshot['version'] == 'V127'
    for name, expected in snapshot['source_sha256'].items():
        assert digest(ROOT / name) == expected, name
    paths = [SOURCE, MANIFEST, SNAPSHOT, Path(__file__),
             *[ROOT / p for p in snapshot['source_sha256']],
             *[ROOT / f'scripts/{p}.py' for p in ['task4_v125_preferences', 'task4_v122_preferences',
               'task4_user_v124_revision', 'task4_user_v121_revision', 'task4_user_city_indicators',
               'task4_ahp_mc_baseline', 'task4_interval_decision', 'task4_v5_model']],
             ROOT / 'design/task4_user_v124_admissions.json', ROOT / 'design/task4_user_v121_admissions.json',
             *[p for d in ['task4_v122_preferences', 'task4_v125_preferences']
               for p in (ROOT / 'results' / d).iterdir() if p.is_file()]]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in paths}
    synthetic = np.array([[0., 0., 1., 2.], [0., 0., 0., 0.], [0., 1., 1., 1.]])
    ranks, first, top3 = rank_metrics(synthetic, descending=False)
    np.testing.assert_array_equal(ranks, [[1.5, 1.5, 3., 4.], [2.5] * 4, [1., 3., 3., 3.]])
    np.testing.assert_array_equal(first, [[.5, .5, 0., 0.], [.25] * 4, [1., 0., 0., 0.]])
    np.testing.assert_allclose(top3, [[1., 1., 1., 0.], [.75] * 4, [1., 2/3, 2/3, 2/3]], atol=1e-14, rtol=0)
    f0, l0, h0 = control_bounds()
    fp, lp, hp = previous_bounds()
    frame, lo, hi = revised_bounds()
    pd.testing.assert_frame_equal(frame, f0, check_exact=True)
    pd.testing.assert_frame_equal(frame, fp, check_exact=True)
    cities = frame.city.tolist()
    assert len(cities) == 16 and lo.shape == hi.shape == (16, 10)
    assert np.count_nonzero(lo != l0) == 4 and np.array_equal(hi, h0)
    assert np.count_nonzero(lo != lp) == 2 and np.array_equal(hi, hp)
    protected = ~((lp == 0) & (hp == 1))
    assert protected.sum() == 141
    np.testing.assert_array_equal(np.stack([lo, hi])[:, protected], np.stack([lp, hp])[:, protected])
    assert np.all(lo >= l0) and np.all(hi <= h0)
    original = np.stack([lo, hi]).copy()
    control = calculate(cities, l0, h0)
    exact_control(control, l0, h0, cities)
    previous = frozen_previous()
    old_bounds = pd.read_csv(OLD / 'utility_bounds.csv', float_precision='round_trip')
    bounds = lambda l, h: pd.DataFrame([dict(city=c, indicator=n, lower=l[i,j], upper=h[i,j])
                       for i,c in enumerate(cities) for j,n in enumerate(NAMES)])
    pd.testing.assert_frame_equal(bounds(lp, hp), old_bounds, check_exact=True)
    current = calculate(cities, lo, hi)
    for old in [control, previous]:
        pd.testing.assert_frame_equal(current['weights'], old['weights'], check_exact=True)
        assert current['scenario_matrices'] == old['scenario_matrices']
    saved = pd.read_csv(ROOT / 'results/task4_user_v127_revision/current_ranks.csv', float_precision='round_trip')
    baseline = current['ranks'][current['ranks'].profile == 'baseline']
    saved = saved[(saved.scenario == 'after_conditional') & (saved.weight_reference == 'fixed')]
    cols = [c for c in baseline if c not in ['profile', 'baseline_decision_rank', 'rank_change_positive_improves']]
    pd.testing.assert_frame_equal(baseline[cols], saved[cols].reset_index(drop=True), check_exact=True)
    smc = pd.read_csv(ROOT / 'results/task4_user_v127_revision/mc_city_summary.csv', float_precision='round_trip')
    for k in CONCENTRATIONS:
        old = smc[(smc.scenario == 'after_conditional') & (smc.weight_reference == 'fixed') & (smc.concentration == k)].set_index('city').loc[cities]
        new = current['mc'][(current['mc'].profile == 'baseline') & (current['mc'].concentration == k)].set_index('city').loc[cities]
        for c in ['minimax_recommendation_frequency', 'mean_decision_rank', 'possible_champion_frequency']:
            np.testing.assert_array_equal(new[c], old[c])
    c0, m0, r0 = compare(current, control, 'v121')
    cp, mp, rp = compare(current, previous, 'v124')
    for name, expected in hashes.items():
        assert digest(ROOT / name) == expected, name
    _, check_l, check_h = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([check_l, check_h]))
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in [('ranks.csv', current['ranks']), ('weights.csv', current['weights']),
            ('mc_city_summary.csv', current['mc']), ('control_v121_ranks.csv', control['ranks']),
            ('control_v121_mc_city_summary.csv', control['mc']), ('v122_rank_comparison.csv', c0),
            ('v122_mc_comparison.csv', m0), ('v125_rank_comparison.csv', cp), ('v125_mc_comparison.csv', mp),
            ('utility_bounds.csv', bounds(lo, hi))]:
        data.to_csv(OUT / name, index=False)
    (OUT / 'scenario_matrices.json').write_text(json.dumps(current['scenario_matrices'], indent=2) + '\n')
    for name, doc in current['scenario_matrices'].items():
        pd.DataFrame(doc['matrix'], index=NAMES, columns=NAMES).rename_axis('indicator').to_csv(OUT / f'{name}_matrix.csv')
    summary = dict(version='V128', input_version='V127 user16', control_input='V121 user16',
        previous_input='V124 user16 (frozen V125 preferences)', profiles=current['profiles'],
        preference_evidence='Unchanged analyst-designed2x multipliers; no student survey, expert elicitation or measured age preference',
        ahp_interpretation='Exact-ratio AHP reconstruction; CR checks algebraic consistency only',
        seed=SEED, concentrations=list(CONCENTRATIONS), draws_per_setting=DRAWS,
        total_draws=3*len(CONCENTRATIONS)*DRAWS, total_draws_current=3*len(CONCENTRATIONS)*DRAWS,
        total_draws_control=3*len(CONCENTRATIONS)*DRAWS,
        random_generator='default_rng(SeedSequence([20261108, concentration])) reset per profile and concentration',
        mc_interpretation='Weight-conditional recommendation frequencies, not real winning probabilities; no missing utility completion sampled',
        ranking_policy='Deterministic interval minimax regret remains primary; MC mean ranks/frequencies are sensitivity summaries',
        controlled_v122_comparison='V121 control exactly reproduces frozen V122 ranks, MC, weights, bounds, matrices and profile summaries. V127 differs in four utility lower bounds.',
        controlled_v125_comparison='Frozen V125 matching city/profile/concentration/draw columns paired against V127; V124 bounds and all preferences verified unchanged. Two new utility lower bounds differ.',
        historical_comparison=r0, previous_evidence_comparison=rp,
        changed_lower_bounds_since_V121=[dict(city=cities[i], indicator=NAMES[j], before=float(l0[i,j]), after=float(lo[i,j])) for i,j in zip(*np.where(lo != l0))],
        changed_lower_bounds_since_V124=[dict(city=cities[i], indicator=NAMES[j], before=float(lp[i,j]), after=float(lo[i,j])) for i,j in zip(*np.where(lo != lp))],
        source_hashes=hashes)
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    audit = dict(status='pass', main_input_shape=[16,10], changed_evidence_cells_vs_V121=4,
        changed_evidence_cells_vs_V124=2, protected_V124_nonfullymissing_cells=141,
        V121_control_exactly_matches_frozen_V122=['ranks','weights','all144_MC_rows','all160_bounds','scenario_matrices','profile_summaries'],
        V125_frozen_bounds_exactly_match_V124_factory=True, paired_V125_comparison_rows=dict(ranks=len(cp), mc=len(mp)),
        deterministic_profile_checks=6, independent_mc_settings=18, draws_per_setting=DRAWS,
        explicit_fractional_tie_cases=3, every_draw_independent_tie_credits_ranks_and_top3_checked=True,
        independent_quantities=['weighted norms','self-excluded regret','possible/necessary champion','tie credits','mean ranks','top3'],
        unchanged_profiles_weights_seeds_draws=True, V127_primary_baseline_ranks_and_all3_MC_settings_exact=True,
        immutable_snapshot_verified_before_and_after=True, protected_source_hashes_unchanged=True,
        all160_V127_bounds_unchanged=True, writes_only_new_result_directory=True)
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps(dict(profiles=current['profiles'], previous_evidence_comparison=rp), indent=2))


if __name__ == '__main__':
    main()
