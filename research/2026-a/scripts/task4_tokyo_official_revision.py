"""Tokyo 2025 same-scope PTR and verified university-headquarters lower bound."""
import hashlib
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_melbourne_observed_travel import melbourne_bounds
from task4_continuous_preferences import feasible_preferences
from task4_acquisition_limits import certificate

SOURCE = ROOT / 'data/task4_v46_tokyo'


def observation():
    spec = importlib.util.spec_from_file_location('tokyo_extract', SOURCE / 'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record = module.extract()
    assert record == json.loads((SOURCE / 'summary.json').read_text())
    return record


def tokyo_bounds(education=True, resources=True, withdraw=False):
    data = observation()
    lo, hi = melbourne_bounds()
    i = CITIES.index('Tokyo')
    j, k = NAMES.index('upper_secondary_ptr'), NAMES.index('research_he_density')
    before, after = data['school_year_comparison']
    assert before['year'] == 2024 and after['year'] == 2025
    np.testing.assert_allclose([lo[i, j], hi[i, j]], [before['utility']] * 2, rtol=0, atol=1e-12)
    assert lo[i, k] == 0 and hi[i, k] == 1
    if education:
        lo[i, j] = hi[i, j] = after['utility']
    if resources:
        he = data['higher_education']
        assert he['finite_all_he_upper_supported'] is False and he['utility_upper'] == 1
        lo[i, k] = he['conditional_all_he_utility_lower']
    if withdraw:
        lo[i, [j, k]], hi[i, [j, k]] = 0, 1
    return lo, hi


def main():
    before = melbourne_bounds()
    baseline, _ = summarize(*before, weights())
    scenarios = [('v44_before', before), ('ptr_year_only', tokyo_bounds(resources=False)),
                 ('university_lower_only', tokyo_bounds(education=False)),
                 ('v46_combined', tokyo_bounds()), ('tokyo_scope_withdrawal', tokyo_bounds(withdraw=True))]
    frames, summaries = [], []
    i = CITIES.index('Tokyo')
    allowed = np.zeros(before[0].shape, bool)
    allowed[i, [NAMES.index('upper_secondary_ptr'), NAMES.index('research_he_density')]] = True
    for name, (lo, hi) in scenarios:
        np.testing.assert_array_equal(lo[~allowed], before[0][~allowed])
        np.testing.assert_array_equal(hi[~allowed], before[1][~allowed])
        assert np.all((0 <= lo) & (lo <= hi) & (hi <= 1))
        rank, decision = summarize(lo, hi, weights())
        rank['scenario'] = name
        frames.append(rank)
        continuous = [c for k, c in enumerate(CITIES)
                      if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']]
        summaries.append(dict(scenario=name, choice=[CITIES[k] for k in decision['minimax_choices']],
            changed_ranks=int((rank.decision_rank != baseline.decision_rank).sum()),
            kendall_tau=float(kendalltau(rank.decision_rank, baseline.decision_rank).statistic),
            possible_champions=int(rank.possible_champion.sum()), continuous_alpha_possible=continuous,
            tokyo=rank.loc[rank.city == 'Tokyo', ['score_lower', 'score_upper', 'decision_rank', 'max_regret']].iloc[0].to_dict(),
            phoenix_rank=int(rank.loc[rank.city == 'Phoenix', 'decision_rank'].iloc[0])))
    out = ROOT / 'results/task4_v46_tokyo'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    summary = dict(main_admitted=False, primary_scenario='v46_combined',
        scope='Tokyo Metropolis; school/main-duty-teacher resource ratio, recognized university headquarters as institutional location; not student learning quality or campus access',
        baseline='V44 melbourne_bounds', alpha_fixed=.1, alpha_range=[.05, .2],
        source_manifest_sha256=hashlib.sha256((SOURCE / 'manifest.json').read_bytes()).hexdigest(),
        scenarios=summaries)
    lo, hi = tokyo_bounds()
    mask = np.zeros_like(lo, bool)
    mask[:, [NAMES.index('upper_secondary_ptr'), NAMES.index('travel')]] = True
    certified = certificate(lo, hi, mask)
    summary['rechecked_all_city_education_and_travel_perfect_measurement'] = dict(
        fixed_unavoidable_count=sum(r['fixed_unavoidable'] for r in certified),
        continuous_unavoidable_count=sum(r['continuous_unavoidable'] for r in certified))
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in row.items() if k != 'continuous_alpha_possible'}
                      for row in summaries], indent=2))


if __name__ == '__main__':
    main()
