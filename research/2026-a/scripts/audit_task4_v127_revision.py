"""Independent V127 two-cell admission, withdrawal and weight-sensitivity audit.

Factories provide interface arrays only. Admissions are rebuilt directly from
the manifest, static scores use prior independent norms/self-excluded formulas,
and all Monte Carlo quantities are independently broadcast from fixed bounds.
Rechecks accept the frozen V124 pre-activation or V127 activated registry and
write a separate receipt, preserving the original pre-activation audit.
"""
import hashlib
import json
import subprocess

import numpy as np
import pandas as pd

from task4_user_v124_revision import revised_bounds as previous_bounds
from task4_user_v127_revision import revised_bounds, OUT, MANIFEST
from task4_user_city_indicators import SOURCE
from task4_v123_revision_diagnostic import independent_intervals, independent_scores
from task4_v5_model import ROOT, NAMES

REFERENCES = {'fixed': np.array([.1125]*6+[.05,.1125,.1125,.05]), 'equal': np.ones(10)/10}
EXPECTED_KEYS = {('Prague', 'public_transport_density'), ('Vienna', 'public_transport_density')}
COUNTS = {'Prague': 57, 'Vienna': 99}
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
    assert sha(SOURCE) == INPUT_SHA
    registry = ROOT/'design/task4_user_current_model.json'
    registry_before = registry.read_bytes()
    registry_data = json.loads(registry_before)
    registry_version = registry_data['version']
    assert registry_version in {'V124', 'V127'}, 'Expected V124 or activated V127 registry'
    snapshot = ROOT/'design/task4_user_v127_snapshot.json'
    snapshot_before = snapshot.read_bytes()
    snapshot_data = json.loads(snapshot_before)
    assert snapshot_data['version'] == 'V127'
    receipt = OUT/'revision_audit.json'
    receipt_before = receipt.read_bytes()
    receipt_expected_sha = snapshot_data['source_sha256'][str(receipt.relative_to(ROOT))]
    assert sha(receipt) == receipt_expected_sha, 'Original pre-activation receipt changed'
    receipt_data = json.loads(receipt_before)
    assert receipt_data['status'] == 'pass' and receipt_data['registry_still_V124_during_audit']
    if registry_version == 'V124':
        expected_registry = subprocess.check_output([
            'git', '-C', str(ROOT.parents[1]), 'show',
            '8565a65:'+str(registry.relative_to(ROOT.parents[1]))])
        assert registry_before == expected_registry, 'Registry differs from frozen V124 state'
        registry_state = 'pre_activation_frozen_V124'
        output_receipt = OUT/'pre_activation_reaudit.json'
    else:
        assert sha(registry) == snapshot_data['source_sha256'][str(registry.relative_to(ROOT))]
        assert registry_data['module'] == 'task4_user_v127_revision'
        assert registry_data['factory'] == 'revised_bounds'
        assert registry_data['admissions'] == 'design/task4_user_v127_admissions.json'
        assert registry_data['results'] == 'results/task4_user_v127_revision'
        registry_state = 'post_activation_snapshot_matched_V127'
        output_receipt = OUT/'post_activation_audit.json'
    protected_primary = {
        path: expected for path, expected in snapshot_data['source_sha256'].items()
        if path != str(registry.relative_to(ROOT))}
    for path, expected in protected_primary.items():
        assert sha(ROOT/path) == expected, path
    manifest_before = MANIFEST.read_bytes()
    manifest = json.loads(manifest_before)
    assert manifest['version'] == 'V127' and manifest['input_sha256'] == INPUT_SHA
    assert len(manifest['source_hashes']) == 70
    for path, expected in manifest['source_hashes'].items():
        assert sha(ROOT/path) == expected, path
    old = ROOT/'results/task4_user_v124_revision'
    old_hashes = {}
    for name in ['current_ranks.csv', 'all_ranks.csv', 'utility_bounds.csv', 'summary.json', 'mc_city_summary.csv']:
        path = old/name
        original = subprocess.check_output(['git', '-C', str(ROOT.parents[1]), 'show',
                                            '8565a65:'+str(path.relative_to(ROOT.parents[1]))])
        assert path.read_bytes() == original, f'Frozen V124 output changed: {name}'
        old_hashes[name] = sha(path)
    frame, lo0, hi0 = previous_bounds(); cities = frame.city.tolist()
    new_frame, lo, hi = revised_bounds()
    assert cities == new_frame.city.tolist() and lo.shape == hi.shape == (16, 10)
    keep = ~((lo0 == 0) & (hi0 == 1))
    assert keep.sum() == 141
    np.testing.assert_array_equal(lo[keep], lo0[keep]); np.testing.assert_array_equal(hi[keep], hi0[keep])
    assert np.all(lo >= lo0) and np.all(hi <= hi0)
    changed = {(cities[i], NAMES[j]) for i, j in zip(*np.where((lo != lo0) | (hi != hi0)))}
    assert changed == EXPECTED_KEYS
    observations = manifest['observations']
    keys = {(row['city'], row['indicator']) for row in observations}
    assert keys == EXPECTED_KEYS and len(observations) == 2

    def expected_bounds(selected):
        a, b = lo0.copy(), hi0.copy()
        for row in observations:
            key = row['city'], row['indicator']
            i, j = cities.index(row['city']), NAMES.index(row['indicator'])
            assert (lo0[i, j], hi0[i, j]) == (0, 1)
            assert row['raw_count'] == COUNTS[row['city']]
            assert row['population'] == frame.iloc[i].population
            assert row['lower_bound_only'] and row['utility_after'][1] == 1
            assert row['admission_decision'].startswith('Accepted')
            # Algebraically independent unit conversion: u=c/(P/2000+c).
            lower = row['raw_count']/(row['population']/2000+row['raw_count'])
            close([lower, 1], row['utility_after'], 'admission formula')
            if key in selected:
                a[i, j], b[i, j] = lower, 1
        np.testing.assert_array_equal(a[keep], lo0[keep]); np.testing.assert_array_equal(b[keep], hi0[keep])
        return a, b

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
    assert len(cases) == 10
    allr = pd.read_csv(OUT/'all_ranks.csv'); allb = pd.read_csv(OUT/'utility_bounds.csv')
    prior = pd.read_csv(old/'current_ranks.csv')
    prior_b = pd.read_csv(old/'utility_bounds.csv')
    assert set(allr.scenario) == set(allb.scenario) == set(cases)
    assert len(allr) == 320 and len(allb) == 1600
    summary = json.loads((OUT/'summary.json').read_text())
    assert summary['version'] == 'V127' and summary['baseline'] == 'V124 user16'
    assert summary['changed_cells'] == 2 and summary['unchanged_cells'] == 158
    assert summary['protected_nonmissing_cells'] == 141
    assert summary['input_sha256'] == INPUT_SHA and summary['admissions_sha256'] == sha(MANIFEST)
    assert (summary['point_cells'], summary['partial_cells'], summary['fully_missing_cells']) == (112, 31, 17)
    assert len(summary['results']) == 20
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
                    close(rows[col], oldrows[col], 'before/withdrawal vs V124')
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
                        close(rows[col], oldrows[col], 'before MC vs V124')
                mc_checks.append(dict(scenario=name, weight_reference=reference, concentration=concentration))
    assert len(static_checks) == 20 and len(mc_checks) == 24
    assert sha(SOURCE) == INPUT_SHA and registry.read_bytes() == registry_before and MANIFEST.read_bytes() == manifest_before
    assert snapshot.read_bytes() == snapshot_before and receipt.read_bytes() == receipt_before
    for path, expected in protected_primary.items():
        assert sha(ROOT/path) == expected, path
    for path, expected in manifest['source_hashes'].items():
        assert sha(ROOT/path) == expected, path
    for name, expected in old_hashes.items():
        assert sha(old/name) == expected
    _, final_l, final_u = revised_bounds()
    np.testing.assert_array_equal(final_l, lo); np.testing.assert_array_equal(final_u, hi)
    result = dict(status='pass', shape=[16, 10], changed_cells=2, unchanged_cells=158,
        changed_keys=sorted([list(x) for x in changed]), protected_nonfullymissing_cells=141,
        all_original_and_V124_nonfullymissing_values_exactly_preserved=True,
        source_files_hashed=70, source_hashes_before_after_match=True,
        V124_baseline_outputs_byte_equal_commit_8565a65=old_hashes,
        before_bounds_exact_equal_saved_V124=True, full_withdrawal_factory_exact_restores_V124=True,
        independent_static_cases=20, static_checks=static_checks,
        independent_weight_MC_cases=24, MC_checks=mc_checks, draws_per_setting=10000,
        seed_stream_unchanged=True, missing_or_partial_values_not_randomly_sampled=True,
        before_static_and_MC_matches_saved_V124=True, all_new_supplements_withdrawable=True,
        point_cells=112, partial_cells=31, fully_missing_cells=17,
        original_csv_sha256=INPUT_SHA, registry_version_during_audit=registry_version,
        registry_state=registry_state, registry_sha256=sha(registry),
        registry_bytes_before_after_unchanged=True,
        original_pre_activation_receipt_sha256=receipt_expected_sha,
        original_pre_activation_receipt_bytes_unchanged=True,
        V127_snapshot_sha256=sha(snapshot), V127_snapshot_bytes_unchanged=True,
        frozen_primary_snapshot_nonregistry_hashes_match=True,
        audit_script_sha256=sha(ROOT/'scripts/audit_task4_v127_revision.py'),
        source_CSV_registry_manifest_old_results_and_final_bounds_unchanged=True,
        output_sha256={p.name: sha(p) for p in sorted(OUT.glob('*.csv'))},
        summary_sha256=sha(OUT/'summary.json'), admissions_sha256=sha(MANIFEST))
    output_receipt.write_text(json.dumps(result, indent=2)+'\n')
    print(f'PASS: V127 2/158/141, 70 source hashes, 20 static cases and 24 MC settings; '
          f'registry {registry_version}, receipt {output_receipt.name}')


if __name__ == '__main__':
    main()
