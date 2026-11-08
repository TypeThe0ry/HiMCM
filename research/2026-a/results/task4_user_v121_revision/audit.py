"""Independent V120 restoration and V121 evidence-only/weight-sensitivity audit.

Run after the V121 manifest and generated result files are complete. Shared
factories supply arrays for interface checks only; the audit derives admissions,
scores, decisions and Monte Carlo summaries without shared scoring helpers.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[1]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'scripts'))
from task4_user_v120_revision import revised_bounds as v120_bounds
from task4_user_v118_revision import revised_bounds as v118_bounds
from task4_user_v121_revision import revised_bounds as v121_bounds

NAMES = ['homicide_rate', 'pm25', 'cost_living_index', 'price_income_ratio',
         'upper_secondary_ptr', 'research_he_density', 'public_transport_density',
         'travel', 'fixed_broadband_mbps', 'public_pool_density']
INPUT = ROOT/'data/task4_v117_team_intake/city_indicators.csv'
INPUT_SHA = '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
REFERENCES = {'fixed': np.array([.1125]*6+[.05,.1125,.1125,.05]),
              'equal': np.ones(10)/10}
TOL = 1e-12


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scores(z, w):
    """Broadcast, weight each squared coordinate once, then sum explicitly."""
    a = np.sqrt(np.sum(np.asarray(w)[..., None, :]*np.square(z), axis=-1))
    b = np.sqrt(np.sum(np.asarray(w)[..., None, :]*np.square(1-z), axis=-1))
    return 100*a/(a+b)


def decisions(lower, upper):
    """Derive each city's competitor set explicitly, excluding itself."""
    n = lower.shape[-1]
    regret, possible, necessary, best, worst = [], [], [], [], []
    for i in range(n):
        others = [k for k in range(n) if k != i]
        other_l = np.max(lower[..., others], axis=-1)
        other_u = np.max(upper[..., others], axis=-1)
        regret.append(np.maximum(0, other_u-lower[..., i]))
        possible.append(upper[..., i] >= other_l-TOL)
        necessary.append(lower[..., i] >= other_u-TOL)
        best.append(1+np.sum(lower[..., others] > upper[..., i, None]+TOL, axis=-1))
        worst.append(1+np.sum(upper[..., others] > lower[..., i, None]+TOL, axis=-1))
    return {name: np.stack(values, axis=-1) for name, values in [
        ('max_regret', regret), ('possible_champion', possible),
        ('necessary_champion', necessary), ('best_rank', best), ('worst_rank', worst)]}


def competition_rank(values, descending=False):
    return np.array([1+np.sum(values > x if descending else values < x) for x in values])


def saved_bounds(path, scenario, cities):
    rows = pd.read_csv(path)
    rows = rows[rows.scenario == scenario].set_index(['city', 'indicator'])
    index = pd.MultiIndex.from_product([cities, NAMES], names=['city', 'indicator'])
    assert len(rows) == 160 and rows.index.is_unique
    rows = rows.loc[index]
    return rows.lower.to_numpy().reshape(16, 10), rows.upper.to_numpy().reshape(16, 10)


def main():
    assert sha(INPUT) == INPUT_SHA
    for filename in ['task4_user_v118_admissions.json', 'task4_user_v120_admissions.json']:
        historical_manifest = json.loads((ROOT/'design'/filename).read_text())
        assert historical_manifest['input_sha256'] == INPUT_SHA
        for path, digest in historical_manifest['source_hashes'].items():
            assert sha(ROOT/path) == digest, path
    immutable = {}
    for filename in ['current_ranks.csv', 'all_ranks.csv', 'utility_bounds.csv',
                     'mc_city_summary.csv', 'summary.json']:
        path = ROOT/'results/task4_user_v120_revision'/filename
        original = subprocess.check_output(['git', '-C', str(REPO), 'show',
                                           'e122d68:'+str(path.relative_to(REPO))])
        assert path.read_bytes() == original, filename
        immutable[str(path.relative_to(ROOT))] = sha(path)
    frame, old_l, old_u = v120_bounds()
    f118, l118, u118 = v118_bounds()
    cities = frame.city.tolist()
    assert len(cities) == 16 and old_l.shape == old_u.shape == (16, 10)
    assert cities == pd.read_csv(INPUT).city.tolist() == f118.city.tolist()
    assert int(np.sum((old_l != l118) | (old_u != u118))) == 4
    protected118 = ~((l118 == 0) & (u118 == 1))
    assert protected118.sum() == 130
    np.testing.assert_array_equal(old_l[protected118], l118[protected118])
    np.testing.assert_array_equal(old_u[protected118], u118[protected118])
    saved_l, saved_u = saved_bounds(ROOT/'results/task4_user_v120_revision/utility_bounds.csv',
                                    'after_conditional', cities)
    np.testing.assert_allclose(old_l, saved_l, atol=1e-15, rtol=0)
    np.testing.assert_allclose(old_u, saved_u, atol=1e-15, rtol=0)
    baseline = pd.read_csv(ROOT/'results/task4_user_v120_revision/current_ranks.csv')
    for ref, w in REFERENCES.items():
        assert w.sum() == 1
        l, u = scores(old_l, w), scores(old_u, w)
        d = decisions(l, u)
        prior = baseline[baseline.weight_reference == ref].set_index('city').loc[cities]
        for col, x in [('score_lower', l), ('score_upper', u), *d.items()]:
            np.testing.assert_allclose(prior[col], x, atol=1e-12, rtol=0)
        np.testing.assert_array_equal(prior.decision_rank, competition_rank(d['max_regret']))
        assert cities[np.argmin(d['max_regret'])] == 'Zurich'
        assert d['possible_champion'].sum() == 16
        if ref == 'fixed':
            assert abs(np.mean(u-l)-16.93440560207023) < 1e-12

    manifest_path = ROOT/'design/task4_user_v121_admissions.json'
    manifest = json.loads(manifest_path.read_text())
    assert manifest['input_sha256'] == INPUT_SHA
    for path, digest in manifest['source_hashes'].items():
        assert sha(ROOT/path) == digest, path
    observations = manifest['observations']
    keys = {(r['city'], r['indicator']) for r in observations}
    assert len(keys) == len(observations)
    protected = ~((old_l == 0) & (old_u == 1))
    assert protected.sum() == 134

    def admitted(selected):
        lo, hi = old_l.copy(), old_u.copy()
        for row in observations:
            key = (row['city'], row['indicator'])
            i, j = cities.index(row['city']), NAMES.index(row['indicator'])
            assert (old_l[i, j], old_u[i, j]) == (0, 1)
            if key not in selected:
                continue
            if row.get('kind') == 'ratio_interval':
                assert row['indicator'] == 'upper_secondary_ptr'
                low, high = row['ratio_bounds']
                assert 0 <= low <= high
                bounds = [15/(15+high), 15/(15+low)]
            else:
                assert row['indicator'] in ['public_pool_density', 'public_transport_density']
                assert row['population'] == frame.iloc[i].population
                assert row['raw_count'] > 0 and row['lower_bound_only']
                density = row['raw_count']/(row['population']/100000)
                anchor = 1 if row['indicator'] == 'public_pool_density' else 50
                bounds = [density/(anchor+density), 1.]
            np.testing.assert_allclose(bounds, row['utility_after'], atol=1e-12, rtol=0)
            lo[i, j], hi[i, j] = bounds
        np.testing.assert_array_equal(lo[protected], old_l[protected])
        np.testing.assert_array_equal(hi[protected], old_u[protected])
        return lo, hi

    def historical_withdrawal(bounds):
        lo, hi = (x.copy() for x in bounds)
        i, j = cities.index('Singapore'), NAMES.index('travel')
        lo[i, j], hi[i, j] = 0, 1
        return lo, hi

    cases = {'before': (old_l, old_u)}
    cases.update({('only:'+':'.join(key)): admitted({key}) for key in sorted(keys)})
    cases['after_conditional'] = admitted(keys)
    cases.update({('without:'+':'.join(key)): admitted(keys-{key}) for key in sorted(keys)})
    cases['withdraw_all_new'] = admitted(set())
    inventory_keys = {(r['city'], r['indicator']) for r in observations
                      if r.get('historical_inventory_proxy')}
    cases['withdraw_new_historical_inventories'] = admitted(keys-inventory_keys)
    cases['before_withdraw_historical_stage_proxy'] = historical_withdrawal((old_l, old_u))
    cases['withdraw_historical_stage_proxy'] = historical_withdrawal(cases['after_conditional'])
    _, new_l, new_u = v121_bounds()
    np.testing.assert_allclose(new_l, cases['after_conditional'][0], atol=1e-15, rtol=0)
    np.testing.assert_allclose(new_u, cases['after_conditional'][1], atol=1e-15, rtol=0)
    changed = set((cities[i], NAMES[j]) for i, j in zip(*np.where((new_l != old_l) | (new_u != old_u))))
    assert changed == keys
    _, withdrawn_l, withdrawn_u = v121_bounds(set())
    np.testing.assert_array_equal(withdrawn_l, old_l)
    np.testing.assert_array_equal(withdrawn_u, old_u)
    for key in sorted(keys):
        _, lo, hi = v121_bounds({key})
        np.testing.assert_allclose(lo, admitted({key})[0], atol=1e-15, rtol=0)
        np.testing.assert_allclose(hi, admitted({key})[1], atol=1e-15, rtol=0)
    ranks = pd.read_csv(OUT/'all_ranks.csv')
    assert set(ranks.scenario) == set(cases)
    assert len(ranks) == len(cases)*2*16
    summary = json.loads((OUT/'summary.json').read_text())
    assert summary['changed_cells'] == len(keys) and summary['unchanged_cells'] == 160-len(keys)
    assert summary['protected_nonmissing_cells'] == 134
    assert summary['point_cells'] == np.sum(new_l == new_u)
    assert summary['partial_cells'] == np.sum((new_l < new_u) & ((new_l > 0) | (new_u < 1)))
    assert summary['fully_missing_cells'] == np.sum((new_l == 0) & (new_u == 1))
    assert summary['input_sha256'] == INPUT_SHA
    assert summary['admissions_sha256'] == sha(manifest_path)
    scenario_audit = []
    for name, (lo, hi) in cases.items():
        recorded_l, recorded_u = saved_bounds(OUT/'utility_bounds.csv', name, cities)
        np.testing.assert_allclose(recorded_l, lo, atol=1e-15, rtol=0)
        np.testing.assert_allclose(recorded_u, hi, atol=1e-15, rtol=0)
        for ref, w in REFERENCES.items():
            l, u = scores(lo, w), scores(hi, w)
            d = decisions(l, u)
            rows = ranks[(ranks.scenario == name) & (ranks.weight_reference == ref)].set_index('city').loc[cities]
            mids = scores((lo+hi)/2, w)
            expected = dict(score_lower=l, score_upper=u, **d,
                            decision_rank=competition_rank(d['max_regret']),
                            midpoint_illustrative_score=mids,
                            midpoint_illustrative_rank=competition_rank(mids, descending=True))
            prior = baseline[baseline.weight_reference == ref].set_index('city').loc[cities]
            expected['previous_decision_rank'] = prior.decision_rank.to_numpy()
            expected['rank_change_positive_improves'] = expected['previous_decision_rank']-expected['decision_rank']
            for col, x in expected.items():
                np.testing.assert_allclose(rows[col], x, atol=1e-12, rtol=0, err_msg=f'{name}/{ref}/{col}')
            s = next(x for x in summary['results'] if x['scenario'] == name and x['weight_reference'] == ref)
            assert s['possible_champions'] == [cities[k] for k in np.flatnonzero(d['possible_champion'])]
            assert s['necessary_champions'] == [cities[k] for k in np.flatnonzero(d['necessary_champion'])]
            assert s['minimax_choices'] == [cities[k] for k in np.flatnonzero(expected['decision_rank'] == 1)]
            assert abs(s['mean_width']-np.mean(u-l)) < 1e-12
            scenario_audit.append(dict(scenario=name, weight_reference=ref, mean_width=s['mean_width'],
                                       possible_count=len(s['possible_champions']), choices=s['minimax_choices']))
    current = pd.read_csv(OUT/'current_ranks.csv')
    pd.testing.assert_frame_equal(current, ranks[ranks.scenario == 'after_conditional'].reset_index(drop=True))

    mc = pd.read_csv(OUT/'mc_city_summary.csv')
    mc_cases = ['before', 'after_conditional', 'before_withdraw_historical_stage_proxy',
                'withdraw_historical_stage_proxy']
    assert len(mc) == 4*2*3*16 and set(mc.scenario) == set(mc_cases)
    assert summary['mc_seed'] == 20261108 and summary['mc_draws_per_setting'] == 10000
    for ref, center in REFERENCES.items():
        for concentration in (20, 100, 500):
            sampled = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(
                concentration*center, 10000)
            for name in mc_cases:
                lo, hi = cases[name]
                d = decisions(scores(lo, sampled), scores(hi, sampled))
                regrets = d['max_regret']
                mean_rank, frequency = [], []
                for i in range(16):
                    ahead = np.sum(regrets < regrets[:, i, None]-TOL, axis=1)
                    tied = np.sum(np.abs(regrets-regrets[:, i, None]) <= TOL, axis=1)
                    mean_rank.append(np.mean(1+ahead+(tied-1)/2))
                    frequency.append(np.mean(np.where(ahead == 0, 1/tied, 0)))
                rows = mc[(mc.scenario == name) & (mc.weight_reference == ref) &
                          (mc.concentration == concentration)].set_index('city').loc[cities]
                for col, x in [('minimax_recommendation_frequency', frequency),
                               ('mean_decision_rank', mean_rank),
                               ('possible_champion_frequency', d['possible_champion'].mean(axis=0))]:
                    np.testing.assert_allclose(rows[col], x, atol=1e-12, rtol=0,
                                               err_msg=f'MC/{ref}/{concentration}/{name}/{col}')
                assert abs(sum(frequency)-1) < 1e-12
    assert sha(INPUT) == INPUT_SHA
    result = dict(status='pass', baseline_commit='e122d68',
                  V120_changed_cells=4, V120_unchanged_cells=156,
                  V120_protected_nonmissing_cells=130,
                  V121_changed_cells=sorted([list(key) for key in changed]),
                  V121_protected_nonmissing_cells=134,
                  baseline_exact_files=immutable,
                  original_csv_sha256=INPUT_SHA,
                  all_scenarios_independent_scores_self_excluded_regrets_ranks_champions=True,
                  full_withdrawal_exactly_restores_V120=True,
                  MC_independent_settings=24, MC_checked_city_rows=384,
                  MC_recommendation_frequency_mean_rank_possible_frequency=True,
                  scenario_audit=scenario_audit,
                  output_sha256={p.name: sha(p) for p in [OUT/'current_ranks.csv', OUT/'all_ranks.csv',
                                                        OUT/'utility_bounds.csv', OUT/'mc_city_summary.csv',
                                                        OUT/'summary.json', manifest_path]})
    (OUT/'audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: V120 restored; V121 evidence-only scenarios and all 24 MC settings independently verified')


if __name__ == '__main__':
    main()
