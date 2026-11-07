"""Expand actual upper-secondary coverage without assigning shared teachers."""
import importlib.util
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_tokyo_official_revision import tokyo_bounds
from task4_singapore_coverage_revision import allocation_utility
from task4_continuous_preferences import feasible_preferences
from task4_acquisition_limits import certificate

SOURCE = ROOT / 'data/task4_v47_tokyo_coverage'


def observation():
    spec = importlib.util.spec_from_file_location('tokyo_coverage_extract', SOURCE / 'extract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    record = module.extract()
    assert record == json.loads((SOURCE / 'summary.json').read_text())
    return record


def tokyo_coverage_bounds(withdraw=False):
    r = observation()
    lo, hi = tokyo_bounds()
    i, j = CITIES.index('Tokyo'), NAMES.index('upper_secondary_ptr')
    np.testing.assert_allclose([lo[i, j], hi[i, j]], [r['baseline_utility']] * 2, rtol=0, atol=1e-12)
    interval = allocation_utility(r['expanded_students'], r['baseline_main_duty_teachers'],
                                  r['integrated_all_course_main_duty_teachers'])
    np.testing.assert_allclose(interval, r['expanded_utility_interval'], rtol=0, atol=1e-12)
    lo[i, j], hi[i, j] = (0, 1) if withdraw else interval
    return lo, hi


def main():
    r = observation()
    teachers = r['baseline_main_duty_teachers'] + np.arange(r['integrated_all_course_main_duty_teachers'] + 1)
    values = 15 * teachers / (r['expanded_students'] + 15 * teachers)
    assert np.all(np.diff(values) > 0)
    np.testing.assert_allclose([values.min(), values.max()], r['expanded_utility_interval'])
    before = tokyo_bounds()
    base, _ = summarize(*before, weights())
    i, j = CITIES.index('Tokyo'), NAMES.index('upper_secondary_ptr')
    keep = np.ones(before[0].shape, bool)
    keep[i, j] = False
    frames, stats = [], []
    for label, (lo, hi) in [('v46_regular_high_school', before),
                           ('v47_expanded_allocation', tokyo_coverage_bounds()),
                           ('tokyo_education_withdrawal', tokyo_coverage_bounds(True))]:
        np.testing.assert_array_equal(lo[keep], before[0][keep])
        np.testing.assert_array_equal(hi[keep], before[1][keep])
        assert np.all((0 <= lo) & (lo <= hi) & (hi <= 1))
        rank, decision = summarize(lo, hi, weights())
        rank['scenario'] = label
        frames.append(rank)
        possible = [c for k, c in enumerate(CITIES)
                    if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']]
        stats.append(dict(scenario=label, choice=[CITIES[k] for k in decision['minimax_choices']],
            tokyo_education_utility=[float(lo[i, j]), float(hi[i, j])],
            tokyo=rank.loc[rank.city == 'Tokyo', ['score_lower', 'score_upper', 'decision_rank', 'max_regret']].iloc[0].to_dict(),
            phoenix_rank=int(rank.loc[rank.city == 'Phoenix', 'decision_rank'].iloc[0]),
            changed_ranks=int((rank.decision_rank != base.decision_rank).sum()),
            kendall_tau=float(kendalltau(rank.decision_rank, base.decision_rank).statistic),
            possible_champions=int(rank.possible_champion.sum()), continuous_alpha_possible=possible))
    lo, hi = tokyo_coverage_bounds()
    mask = np.zeros_like(lo, bool)
    mask[:, [j, NAMES.index('travel')]] = True
    cert = certificate(lo, hi, mask)
    out = ROOT / 'results/task4_v47_tokyo_coverage'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    result = dict(main_admitted=False, primary_scenario='v47_expanded_allocation',
        baseline='V46 tokyo_bounds', changed_city_indicator_cells=1,
        scope=r['coverage'], added_students=r['added_upper_course_students'],
        teacher_allocation=r['added_upper_course_teacher_interval'],
        alpha_fixed=.1, alpha_range=[.05, .2],
        source_manifest_sha256=hashlib.sha256((SOURCE / 'manifest.json').read_bytes()).hexdigest(),
        perfect_education_travel_unavoidable_counts=dict(fixed=sum(x['fixed_unavoidable'] for x in cert),
                                                       continuous=sum(x['continuous_unavoidable'] for x in cert)),
        scenarios=stats)
    (out / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in s.items() if k != 'continuous_alpha_possible'} for s in stats], indent=2))


if __name__ == '__main__':
    main()
