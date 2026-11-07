"""Compare scoped VISTA observations without claiming exact target admission."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_singapore_coverage_revision import singapore_bounds
from task4_continuous_preferences import feasible_preferences

SOURCE = ROOT / 'data/task4_v44_melbourne'


def observation():
    for item in json.loads((SOURCE / 'manifest.json').read_text()):
        raw = (SOURCE / item['file']).read_bytes()
        assert len(raw) == item['bytes']
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
    return json.loads((SOURCE / 'summary.json').read_text())


def melbourne_bounds():
    """V44 conditional baseline: same V23 scope, verified secondary destination."""
    row = observation()
    lo, hi = singapore_bounds()
    i, j = CITIES.index('Melbourne'), NAMES.index('travel')
    lo[i, j], hi[i, j] = row['all_resident_secondary_age_15_19']['linear_sampling_envelope']
    return lo, hi


def check_same_observations():
    old = pd.read_csv(ROOT / 'data/task4_v23_melbourne_roster/roster_audit.csv')
    old = old[(old.agegroup == '15->19') & old.has_observed_journey].set_index('persid').sort_index()
    new = pd.read_csv(SOURCE / 'first_weekday_journeys.csv')
    new = new[new.agegroup == '15->19'].set_index('persid').sort_index()
    assert old.index.equals(new.index) and len(new) == 107
    assert old.jteid.equals(new.jteid)
    columns = ['start_time', 'journey_elapsed_time', 'perspoststratweight']
    columns += ['perspoststratweight_GROUP_' + str(r) for r in range(1, 11)]
    np.testing.assert_allclose(old[columns], new[columns], rtol=0, atol=1e-12)
    assert new.loc[new.destplace2 != 'Secondary School', 'destplace2'].value_counts().to_dict() == {
        'School NEC': 3, 'Primary School': 3, 'Tertiary': 1}


def main():
    check_same_observations()
    observations = observation()
    assert observations['exact_14_18_membership_identified'] is False
    assert observations['main_admission'] is False
    baseline_lo, baseline_hi = singapore_bounds()
    i, j = CITIES.index('Melbourne'), NAMES.index('travel')
    old = json.loads((ROOT / 'data/task4_v23_melbourne_roster/summary.json').read_text())['scopes']['secondary_15_19']
    np.testing.assert_allclose([baseline_lo[i, j], baseline_hi[i, j]],
                               [old['sampling_lower'], old['sampling_upper']], rtol=0, atol=1e-12)
    baseline, _ = summarize(baseline_lo, baseline_hi, weights())
    scenarios = [
        ('v38_before_destination_check', None, None),
        ('v44_destination_check_same_inference', 'all_resident_secondary_age_15_19', 'linear_sampling_envelope'),
        ('resident_15_19_elapsed_identification', 'all_resident_secondary_age_15_19', 'utility_identification_interval'),
        ('resident_15_19_elapsed_sampling', 'all_resident_secondary_age_15_19', 'sampling_envelope'),
        ('resident_15_19_leg_sampling', 'all_resident_secondary_age_15_19_leg_time', 'sampling_envelope'),
        ('attender_15_19_elapsed_sampling', 'secondary_age_15_19', 'sampling_envelope'),
        ('all_age_resident_secondary_sampling', 'all_resident_secondary', 'sampling_envelope'),
        ('strict_target_withdrawal', None, 'unknown'),
    ]
    frames, results = [], []
    for label, population, interval in scenarios:
        lo, hi = baseline_lo.copy(), baseline_hi.copy()
        if population:
            lo[i, j], hi[i, j] = observations[population][interval]
        elif interval == 'unknown':
            lo[i, j], hi[i, j] = 0, 1
        assert 0 <= lo[i, j] <= hi[i, j] <= 1
        keep = np.ones(lo.shape, bool)
        keep[i, j] = False
        np.testing.assert_array_equal(lo[keep], baseline_lo[keep])
        np.testing.assert_array_equal(hi[keep], baseline_hi[keep])
        if label == 'v44_destination_check_same_inference':
            np.testing.assert_array_equal(lo, melbourne_bounds()[0])
            np.testing.assert_array_equal(hi, melbourne_bounds()[1])
            assert lo[i, j] <= baseline_lo[i, j] <= baseline_hi[i, j] <= hi[i, j]
        rank, decision = summarize(lo, hi, weights())
        rank['scenario'] = label
        frames.append(rank)
        continuous = [city for k, city in enumerate(CITIES)
                      if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']]
        results.append(dict(scenario=label, source_population=population,
            travel_utility_bounds=[float(lo[i, j]), float(hi[i, j])],
            choice=[CITIES[k] for k in decision['minimax_choices']],
            possible_champions=rank.loc[rank.possible_champion, 'city'].tolist(),
            continuous_alpha_possible=continuous,
            changed_ranks=int((rank.decision_rank != baseline.decision_rank).sum()),
            kendall_tau=float(kendalltau(rank.decision_rank, baseline.decision_rank).statistic),
            melbourne=rank.loc[rank.city == 'Melbourne',
                ['decision_rank', 'score_lower', 'score_upper', 'max_regret']].iloc[0].to_dict(),
            phoenix_rank=int(rank.loc[rank.city == 'Phoenix', 'decision_rank'].iloc[0])))
    out = ROOT / 'results/task4_v44_melbourne'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    summary = dict(baseline='V38 singapore_bounds with V23 Melbourne roster',
        primary_scenario='v44_destination_check_same_inference',
        main_admitted=False, scenario_scope='Greater Melbourne current Secondary students with valid official person weights; released age 15-19 band, not exact 14-18 or municipality',
        missing_journey_rule='No qualifying diary journey or uncertain destination retains utility [0,1]',
        alpha_fixed=.1, alpha_range=[.05, .2],
        observation_sha256=hashlib.sha256((SOURCE / 'summary.json').read_bytes()).hexdigest(),
        scenarios=results)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in row.items()
                      if k not in ('possible_champions', 'continuous_alpha_possible')}
                     for row in results], indent=2))


if __name__ == '__main__':
    main()
