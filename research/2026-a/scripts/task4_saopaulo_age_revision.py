"""Align existing observed high-school diaries to the requested age 14--18."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize
from task4_tokyo_coverage_revision import tokyo_coverage_bounds
from task4_continuous_preferences import feasible_preferences
from task4_acquisition_limits import certificate

SOURCE = ROOT / 'data/task4_v48_saopaulo_age'


def observation():
    for item in json.loads((SOURCE / 'manifest.json').read_text()):
        raw = (SOURCE / item['file']).read_bytes()
        assert len(raw) == item['bytes']
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
    record = json.loads((SOURCE / 'summary.json').read_text())
    assert record['unknown_age_students'] == record['unknown_weight_students'] == 0
    assert record['main_admitted'] is False
    assert record['bootstrap']['paired_draws'] is True
    assert record['bootstrap']['design_valid_confidence_interval'] is False
    audit = pd.read_csv(SOURCE / 'municipal_students_audit.csv')
    assert audit.person_id.is_unique and (audit.current_study == 4).all()
    assert np.array_equal(audit.age14_18, audit.age.between(14, 18))
    for scope, selected in [('all_age', audit), ('age14_18', audit[audit.age14_18])]:
        expected = record['scopes'][scope]
        assert len(selected) == expected['students']
        for column in ['utility_lower', 'utility_upper']:
            np.testing.assert_allclose(np.average(selected[column], weights=selected.person_weight),
                                       expected[column], rtol=0, atol=1e-12)
    return record


def saopaulo_age_bounds(sampling=True, withdraw=False):
    record = observation()
    old = record['scopes']['all_age']
    new = record['scopes']['age14_18']
    lo, hi = tokyo_coverage_bounds()
    i, j = CITIES.index('Sao Paulo'), NAMES.index('travel')
    np.testing.assert_allclose([lo[i, j], hi[i, j]],
                               [old['sampling_lower'], old['sampling_upper']], rtol=0, atol=1e-12)
    prefix = 'sampling' if sampling else 'utility'
    lo[i, j], hi[i, j] = (0, 1) if withdraw else (new[prefix + '_lower'], new[prefix + '_upper'])
    return lo, hi


def main():
    data = observation()
    before = tokyo_coverage_bounds()
    baseline, _ = summarize(*before, weights())
    frames, stats = [], []
    i, j = CITIES.index('Sao Paulo'), NAMES.index('travel')
    keep = np.ones(before[0].shape, bool)
    keep[i, j] = False
    scenarios = [('v47_all_age', before), ('age14_18_identification', saopaulo_age_bounds(False)),
                 ('v48_age14_18_sampling', saopaulo_age_bounds()), ('source_withdrawal', saopaulo_age_bounds(withdraw=True))]
    for label, (lo, hi) in scenarios:
        np.testing.assert_array_equal(lo[keep], before[0][keep])
        np.testing.assert_array_equal(hi[keep], before[1][keep])
        assert np.all((0 <= lo) & (lo <= hi) & (hi <= 1))
        rank, decision = summarize(lo, hi, weights())
        rank['scenario'] = label
        frames.append(rank)
        continuous = [c for k, c in enumerate(CITIES)
                      if feasible_preferences(hi[k], lo[np.arange(len(lo)) != k])['possible']]
        stats.append(dict(scenario=label, choice=[CITIES[k] for k in decision['minimax_choices']],
            sao_paulo_utility=[float(lo[i, j]), float(hi[i, j])],
            sao_paulo=rank.loc[rank.city == 'Sao Paulo', ['score_lower', 'score_upper', 'max_regret', 'decision_rank']].iloc[0].to_dict(),
            phoenix_rank=int(rank.loc[rank.city == 'Phoenix', 'decision_rank'].iloc[0]),
            changed_ranks=int((rank.decision_rank != baseline.decision_rank).sum()),
            kendall_tau=float(kendalltau(rank.decision_rank, baseline.decision_rank).statistic),
            possible_champions=int(rank.possible_champion.sum()), continuous_alpha_possible=continuous))
    lo, hi = saopaulo_age_bounds()
    mask = np.zeros_like(lo, bool)
    mask[:, [NAMES.index('upper_secondary_ptr'), j]] = True
    cert = certificate(lo, hi, mask)
    out = ROOT / 'results/task4_v48_saopaulo_age'
    out.mkdir(parents=True, exist_ok=True)
    pd.concat(frames).to_csv(out / 'ranks.csv', index=False)
    summary = dict(main_admitted=False, primary_scenario='v48_age14_18_sampling', baseline='V47 tokyo_coverage_bounds',
        scope=data['geography'] + '; actual current upper-secondary enrolment and exact age 14--18',
        design_valid_confidence_interval=False, official_byte_identity_verified=False,
        changed_city_indicator_cells=1, alpha_fixed=.1, alpha_range=[.05, .2],
        source_manifest_sha256=hashlib.sha256((SOURCE / 'manifest.json').read_bytes()).hexdigest(),
        observation_sha256=hashlib.sha256((SOURCE / 'summary.json').read_bytes()).hexdigest(),
        perfect_education_travel_unavoidable_counts=dict(fixed=sum(x['fixed_unavoidable'] for x in cert),
                                                       continuous=sum(x['continuous_unavoidable'] for x in cert)),
        scenarios=stats)
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps([{k: v for k, v in s.items() if k != 'continuous_alpha_possible'} for s in stats], indent=2))


if __name__ == '__main__':
    main()
