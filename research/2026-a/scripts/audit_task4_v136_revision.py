"""Independent staged V136 one-cell admission, withdrawal and weight audit.

Rebuild the London bound and all saved static/MC results independently,
while preserving the live registry and all frozen V130/V131 evidence.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from task4_user_v130_revision import revised_bounds as previous_bounds
from task4_user_v136_revision import revised_bounds, OUT, MANIFEST
from task4_user_city_indicators import SOURCE
from task4_v123_revision_diagnostic import independent_intervals, independent_scores
from task4_v5_model import ROOT, NAMES

REFERENCES = {'fixed': np.array([.1125]*6+[.05,.1125,.1125,.05]), 'equal': np.ones(10)/10}
EXPECTED_KEYS = {('London', 'public_transport_density')}
COUNTS = {'London': 59}
INPUT_SHA = '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(a, b, label='', atol=1e-12):
    np.testing.assert_allclose(a, b, atol=atol, rtol=0, err_msg=label)


def city_rows(frame, cities, **filters):
    selected = frame
    for key, value in filters.items():
        selected = selected[selected[key] == value]
    assert len(selected) == 16 and selected.city.is_unique
    return selected.set_index('city').loc[cities]


def bounds_rows(frame, cities, scenario):
    selected = frame[frame.scenario == scenario]
    assert len(selected) == 160 and not selected.duplicated(['city', 'indicator']).any()
    index = pd.MultiIndex.from_product([cities, NAMES], names=['city', 'indicator'])
    selected = selected.set_index(['city', 'indicator']).loc[index]
    return selected.lower.to_numpy().reshape(16, 10), selected.upper.to_numpy().reshape(16, 10)


def main():
    registry = ROOT/'design/task4_user_current_model.json'
    registry_before = registry.read_bytes()
    manifest = json.loads(MANIFEST.read_text())
    frame, lo0, hi0 = previous_bounds()
    _, lo, hi = revised_bounds()
    cities = frame.city.tolist()
    keys = EXPECTED_KEYS
    observations = manifest['observations']
    assert {(r['city'], r['indicator']) for r in observations} == keys
    assert sha(SOURCE) == INPUT_SHA
    assert len(cities)==16 and lo.shape==(16,10)
    protected = {str(p.relative_to(ROOT)): sha(p) for p in ROOT.glob('results/task4_v131*/**/*') if p.is_file()}
    frozen = json.loads((ROOT/'design/task4_user_v130_snapshot.json').read_text())['source_sha256']
    protected.update(frozen)
    for path, expected in protected.items():
        assert sha(ROOT/path)==expected, path
    for path, expected in manifest['source_hashes'].items():
        assert sha(ROOT/path)==expected, path
    old = ROOT/'results/task4_user_v130_revision'
    def expected_bounds(selected):
        a,b=lo0.copy(),hi0.copy()
        if ('London','public_transport_density') in selected:
            row=observations[0]
            assert row['raw_count']==59 and row['population']==9122909
            i,j=cities.index('London'),NAMES.index('public_transport_density')
            assert [a[i,j],b[i,j]]==[0,1]
            a[i,j]=59/(9122909/2000+59)
            close([a[i,j],1],row['utility_after'])
        keep=~((lo0==0)&(hi0==1))
        np.testing.assert_array_equal(a[keep],lo0[keep])
        np.testing.assert_array_equal(b[keep],hi0[keep])
        return a,b
    expected_l, expected_u = expected_bounds(keys)
    close(lo, expected_l, atol=1e-15); close(hi, expected_u, atol=1e-15)
    cases = {'before': (lo0.copy(), hi0.copy())}
    for key in sorted(keys):
        cases['only:'+':'.join(key)] = expected_bounds({key})
        cases['without:'+':'.join(key)] = expected_bounds(keys-{key})
        _, a, b = revised_bounds({key})
        close(a, cases['only:'+':'.join(key)][0], atol=1e-15)
        close(b, cases['only:'+':'.join(key)][1], atol=1e-15)
    cases['after_conditional'] = (expected_l, expected_u)
    historical_keys = {(row['city'], row['indicator']) for row in observations if row.get('historical_inventory_proxy')}
    cases['withdraw_new_historical_inventories'] = expected_bounds(keys-historical_keys)
    cases['withdraw_all_new'] = expected_bounds(set())
    _, a, b = revised_bounds(set())
    np.testing.assert_array_equal(a, lo0); np.testing.assert_array_equal(b, hi0)
    for name, base in [('before_withdraw_historical_stage_proxy', (lo0, hi0)),
                       ('withdraw_historical_stage_proxy', (expected_l, expected_u))]:
        a, b = (x.copy() for x in base)
        a[cities.index('Singapore'), 7], b[cities.index('Singapore'), 7] = 0, 1
        cases[name] = (a, b)
    assert len(cases) == 8
    allr = pd.read_csv(OUT/'all_ranks.csv'); allb = pd.read_csv(OUT/'utility_bounds.csv')
    prior = pd.read_csv(old/'current_ranks.csv')
    prior_b = pd.read_csv(old/'utility_bounds.csv')
    assert set(allr.scenario) == set(allb.scenario) == set(cases)
    assert len(allr) == 256 and len(allb) == 1280
    summary = json.loads((OUT/'summary.json').read_text())
    assert summary['version'] == 'V136' and summary['baseline'] == 'V130 user16'
    assert summary['changed_cells'] == 1 and summary['unchanged_cells'] == 159
    assert summary['protected_nonmissing_cells'] == 144
    assert summary['input_sha256'] == INPUT_SHA and summary['admissions_sha256'] == sha(MANIFEST)
    assert (summary['point_cells'], summary['partial_cells'], summary['fully_missing_cells']) == (112, 33, 15)
    assert len(summary['results']) == 16
    before_saved = bounds_rows(allb, cities, 'before')
    previous_saved = bounds_rows(prior_b, cities, 'after_conditional')
    np.testing.assert_array_equal(before_saved, previous_saved)
    static_checks = []
    for name, (a, b) in cases.items():
        recorded_l, recorded_u = bounds_rows(allb, cities, name)
        close(recorded_l, a, atol=1e-15); close(recorded_u, b, atol=1e-15)
        for reference, w in REFERENCES.items():
            rows = city_rows(allr, cities, scenario=name, weight_reference=reference)
            d = independent_intervals(a, b, w)
            for col, value in d.items():
                close(rows[col], value, f'{name}/{reference}/{col}')
            midpoint = independent_scores((a+b)/2, w)
            close(rows.midpoint_illustrative_score, midpoint)
            close(rows.midpoint_illustrative_rank, [1+sum(midpoint > x) for x in midpoint])
            oldrows = city_rows(prior, cities, scenario='after_conditional', weight_reference=reference)
            close(rows.previous_decision_rank, oldrows.decision_rank)
            close(rows.rank_change_positive_improves, oldrows.decision_rank-rows.decision_rank)
            if name in {'before', 'withdraw_all_new'}:
                for col in d:
                    close(rows[col], oldrows[col], 'before/withdrawal vs V130')
            result = next(x for x in summary['results'] if x['scenario'] == name and x['weight_reference'] == reference)
            assert result['possible_champions'] == [cities[k] for k in np.flatnonzero(d['possible_champion'])]
            assert result['necessary_champions'] == [cities[k] for k in np.flatnonzero(d['necessary_champion'])]
            assert result['minimax_choices'] == [cities[k] for k in np.flatnonzero(d['decision_rank'] == 1)]
            close(result['mean_width'], np.mean(d['score_upper']-d['score_lower']))
            static_checks.append(dict(scenario=name, weight_reference=reference,
                mean_width=result['mean_width'], choices=result['minimax_choices'],
                possible_count=len(result['possible_champions']), necessary_count=len(result['necessary_champions'])))
    pd.testing.assert_frame_equal(pd.read_csv(OUT/'current_ranks.csv'),
                                  allr[allr.scenario == 'after_conditional'].reset_index(drop=True))

    # Same prescribed streams, independently weighted Euclidean coordinates.
    # No random variable for any missing/partial utility is introduced.
    mc = pd.read_csv(OUT/'mc_city_summary.csv'); prior_mc = pd.read_csv(old/'mc_city_summary.csv')
    mc_names = ['before', 'after_conditional', 'before_withdraw_historical_stage_proxy', 'withdraw_historical_stage_proxy']
    assert len(mc) == 384 and set(mc.scenario) == set(mc_names)
    assert summary['mc_seed'] == 20261108 and summary['mc_draws_per_setting'] == 10000
    mc_checks = []
    for reference, center in REFERENCES.items():
        for concentration in (20, 100, 500):
            sampled = np.random.default_rng(np.random.SeedSequence([20261108, concentration])).dirichlet(concentration*center, 10000)
            for name in mc_names:
                a, b = cases[name]
                distances_l = np.linalg.norm(a[None]*np.sqrt(sampled[:, None]), axis=-1)
                gaps_l = np.linalg.norm((1-a)[None]*np.sqrt(sampled[:, None]), axis=-1)
                lower = 100*distances_l/(distances_l+gaps_l)
                distances_u = np.linalg.norm(b[None]*np.sqrt(sampled[:, None]), axis=-1)
                gaps_u = np.linalg.norm((1-b)[None]*np.sqrt(sampled[:, None]), axis=-1)
                upper = 100*distances_u/(distances_u+gaps_u)
                regret = np.stack([np.maximum(0, np.delete(upper, i, axis=1).max(1)-lower[:, i]) for i in range(16)], axis=1)
                rows = city_rows(mc, cities, scenario=name, weight_reference=reference, concentration=concentration)
                frequencies = []
                for i in range(16):
                    ahead = np.sum(regret < regret[:, i, None]-1e-12, axis=1)
                    tied = np.sum(np.abs(regret-regret[:, i, None]) <= 1e-12, axis=1)
                    frequency = float(np.clip((1-ahead)/tied, 0, 1).mean())
                    frequencies.append(frequency)
                    expected = [frequency, float((1+ahead+(tied-1)/2).mean()),
                        float((upper[:, i] >= np.delete(lower, i, axis=1).max(1)-1e-12).mean())]
                    close(rows.iloc[i][['minimax_recommendation_frequency', 'mean_decision_rank',
                                        'possible_champion_frequency']].to_numpy(float), expected,
                          f'MC/{name}/{reference}/{concentration}/{cities[i]}', atol=1e-11)
                close(sum(frequencies), 1)
                if name == 'before':
                    oldrows = city_rows(prior_mc, cities, scenario='after_conditional', weight_reference=reference, concentration=concentration)
                    for col in ['minimax_recommendation_frequency', 'mean_decision_rank', 'possible_champion_frequency']:
                        close(rows[col], oldrows[col], 'before MC vs V130')
                mc_checks.append(dict(scenario=name, weight_reference=reference, concentration=concentration))
    assert len(static_checks) == 16 and len(mc_checks) == 24
    assert registry.read_bytes()==registry_before and sha(SOURCE)==INPUT_SHA
    for path, expected in protected.items():
        assert sha(ROOT/path)==expected, path
    for path, expected in manifest['source_hashes'].items():
        assert sha(ROOT/path)==expected, path
    report=dict(status='pass',version='V136 controlled evidence; registry unchanged',registry_version_during_audit=json.loads(registry_before)['version'],changed_cells=1,
        protected_nonfullymissing_cells=144,point_cells=112,partial_cells=33,fully_missing_cells=15,
        independent_static_cases=len(static_checks),independent_MC_cases=len(mc_checks),draws_per_setting=10000,
        static_checks=static_checks,MC_checks=mc_checks,full_withdrawal_restores_V130=True,
        before_static_and_MC_match_V130_with_tolerance=True,numerical_MC_tolerance=1e-11,original_CSV_and_registry_unchanged=True,
        protected_sha256=protected,source_files_verified=len(manifest['source_hashes']),
        result_sha256={str(p.relative_to(ROOT)):sha(p) for p in OUT.glob('*.csv')},
        summary_sha256=sha(OUT/'summary.json'),admissions_sha256=sha(MANIFEST),
        audit_script_sha256=sha(Path(__file__)))
    receipt=OUT/('recheck_audit.json' if (OUT/'revision_audit.json').exists() else 'revision_audit.json')
    receipt.write_text(json.dumps(report,indent=2)+'\n')
    print('PASS: 1 changed /144 protected,16 static,24 MC groups,withdrawal and prior controls')

if __name__=='__main__':
    main()
