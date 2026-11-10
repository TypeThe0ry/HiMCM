"""Rebase established controlled extensions without changing their assumptions."""
import argparse
import copy
import struct
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from scipy.optimize import brentq
from task4_user_v203_revision import revised_bounds
from task4_user_v136_revision import revised_bounds as old_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT, NAMES, weights, score


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(folder, name, value):
    if isinstance(value, pd.DataFrame):
        value.to_csv(folder / (name + '.csv'), index=False)
    else:
        (folder / (name + '.json')).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')



def compare_preference_matrices(actual, expected):
    """Enforce bit-exact inputs, permitting roundoff only in three derived diagnostics."""
    allowed = {('independent_living_priority', 'diagnostic', key)
               for key in ('lambda_max', 'CI', 'CR')}
    differences = {}
    def visit(a, b, path=()):
        if isinstance(a, dict) and isinstance(b, dict):
            assert a.keys() == b.keys(), path
            for key in a: visit(a[key], b[key], path + (key,))
        elif isinstance(a, list) and isinstance(b, list):
            assert len(a) == len(b), path
            for i, (x, y) in enumerate(zip(a, b)): visit(x, y, path + (i,))
        elif path in allowed:
            assert isinstance(a, float) and isinstance(b, float), path
            difference = abs(a - b)
            assert np.isfinite(difference) and difference <= 1e-12, path
            differences['/'.join(path)] = difference
        elif isinstance(a, float) and isinstance(b, float):
            assert struct.pack('!d', a) == struct.pack('!d', b), path
        else:
            assert type(a) is type(b) and a == b, path
    visit(actual, expected)
    assert len(differences) == len(allowed)
    return differences

def test_preference_matrix_guard(actual, expected):
    perturbed = copy.deepcopy(actual)
    perturbed['baseline']['matrix'][0][1] = np.nextafter(
        perturbed['baseline']['matrix'][0][1], float('inf')).item()
    try:
        compare_preference_matrices(perturbed, expected)
    except AssertionError:
        return
    raise AssertionError('preference matrix guard accepted a one-ULP input change')

def preferences(out):
    from task4_v125_preferences import calculate
    f, lo, hi = revised_bounds()
    result = calculate(f.city.tolist(), lo, hi)
    for key in ['ranks', 'weights', 'mc']:
        save(out, {'mc':'mc_city_summary'}.get(key, key), result[key])
    save(out, 'scenario_matrices', result['scenario_matrices'])
    prior = ROOT / 'results/task4_v137_preferences'
    pd.testing.assert_frame_equal(result['weights'], pd.read_csv(prior / 'weights.csv', float_precision='round_trip'), check_exact=True)
    old_matrices = json.loads((prior / 'scenario_matrices.json').read_text())
    differences = compare_preference_matrices(result['scenario_matrices'], old_matrices)
    test_preference_matrix_guard(result['scenario_matrices'], old_matrices)
    assert (out / 'weights.csv').read_bytes() == (prior / 'weights.csv').read_bytes()
    save(out, 'summary', dict(version='V203', primary='V203', profiles=result['profiles'],
                             preference_evidence='Unchanged analyst-designed multipliers; no survey or age-specific elicitation',
                             ahp_interpretation='Exact ratio reconstruction; consistency is algebraic',
                             assumptions_and_weights_exactly_match_V137=True, weights_csv_byte_exact=True,
                             matrix_inputs_bit_exact=True, matrix_guard_perturbation_test=True,
                             allowed_derived_diagnostic_differences=differences,
                             maximum_derived_diagnostic_difference=max(differences.values()),
                             derived_diagnostic_tolerance=1e-12))


def future(out):
    from task4_v125_future import run, SCENARIOS
    tables, report = run(revised_bounds, paired_mc=True)
    for key, table in tables.items():
        save(out, key, table)
    report.update(version='V203', primary='V203', interpretation='Unchanged hypothetical raw shocks and paired MC; not a fitted trend or forecast',
                  scenario_definitions=SCENARIOS)
    save(out, 'summary', report)


def method(out):
    from task4_v122_method_country import method_results
    from task4_v137_method_country import independent_method_check, CASE_FILES
    f, lo, hi = revised_bounds()
    reports, frames, components = [], [], []
    for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        rows, comp, report = method_results(f, lo, hi, 'V203', w, ref)
        independent_method_check(rows, report, lo, hi, w)
        reports.append(report)
        frames.append(rows)
        components.append(comp)
    save(out, 'method_ranks', pd.concat(frames, ignore_index=True))
    save(out, 'method_components', pd.concat(components, ignore_index=True))
    frozen = {}
    prior = ROOT / 'results/task4_v137_method_country'
    for name in CASE_FILES:
        (out / name).write_bytes((prior / name).read_bytes())
        frozen[name] = sha(out / name)
    old = json.loads((prior / 'summary.json').read_text())
    save(out, 'summary', dict(version='V203', method_cases=reports, same_country_pairs_in_main16=0,
                             historical_case_scope=old['frozen_case_scope'], frozen_case_sha256=frozen,
                             country_pairs=old['country_pairs'], country_comparability=old['country_comparability'],
                             equity=old['equity'], age_evidence=old['age_evidence']))


def diagnostics(out):
    f, lo, hi = revised_bounds()
    cities = f.city.tolist()
    reports, completion_rows, case_rows, vintage_rows, vintage_reports = [], [], [], [], []
    points = pd.read_csv(ROOT / 'results/task4_v143_vintage/submitted_points.csv')
    point_lookup = {(r.city, r.indicator): r for r in points.itertuples()}
    for ref, w in [('fixed', weights(.1)), ('equal', np.ones(10) / 10)]:
        interval = evaluate(cities, lo, hi, w)
        mid = evaluate(cities, (lo + hi) / 2, (lo + hi) / 2, w)
        reports.append(dict(weight_reference=ref, changed_city_decision_ranks=int((interval.decision_rank != mid.decision_rank).sum()),
                            kendall_tau_b=float(kendalltau(interval.decision_rank, mid.decision_rank).statistic)))
        for case in ['baseline', 'pre2020_points', 'after2025_points', 'non_ok_points', 'union_points', 'withdraw_Zurich_homicide', 'withdraw_Amsterdam_homicide']:
            l, h = lo.copy(), hi.copy()
            count = 0
            for i,c in enumerate(cities):
                for j,n in enumerate(NAMES):
                    row = point_lookup.get((c,n))
                    if row is None:
                        continue
                    early, late, flag = row.submitted_year < 2020, row.submitted_year > 2025, row.submitted_flag != 'ok'
                    remove = {'baseline':False,'pre2020_points':early,'after2025_points':late,'non_ok_points':flag,'union_points':early or late or flag,
                              'withdraw_Zurich_homicide':c == 'Zurich' and j == 0,
                              'withdraw_Amsterdam_homicide':c == 'Amsterdam' and j == 0}[case]
                    if remove:
                        assert lo[i,j] == hi[i,j]
                        l[i,j], h[i,j] = 0, 1
                        count += 1
            result = evaluate(cities, l, h, w)
            vintage_rows.append(result.assign(scenario=case, weight_reference=ref))
            vintage_reports.append(dict(scenario=case, weight_reference=ref, withdrawn_point_cells=count,
                                        minimax_choices=result.loc[result.decision_rank == 1,'city'].tolist(),
                                        mean_interval_width=float((result.score_upper-result.score_lower).mean())))
    # Every city remains a strict winner in its own interior completion.
    for target, city in enumerate(cities):
        u = lo + .05 * (hi - lo)
        u[target] = lo[target] + .95 * (hi[target] - lo[target])
        for i,c in enumerate(cities):
            for j,n in enumerate(NAMES):
                completion_rows.append(dict(target=city, city=c, indicator=n, utility=u[i,j]))
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            scores = score(u,w)
            margin = float(scores[target] - np.delete(scores,target).max())
            assert margin > 0
            case_rows.append(dict(target=city, weight_reference=ref, strict_margin=margin))
    thresholds = []
    z = cities.index('Zurich')
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        def gap(rate):
            l,h = lo.copy(),hi.copy()
            l[z,0] = h[z,0] = 2/(2+rate)
            t = evaluate(cities,l,h,w)
            return float(t.iloc[z].max_regret - t.drop(z).max_regret.min())
        # The focal-city regret gap is monotone nondecreasing as its
        # homicide rate rises: Zurich's score falls while others are fixed.
        left, right = gap(0), gap(5)
        assert left <= right + 1e-10
        if left * right < 0:
            rate = float(brentq(gap, 0, 5, xtol=1e-14))
            assert gap(rate-1e-8) < 0 < gap(rate+1e-8)
            thresholds.append(dict(weight_reference=ref, status='crossing_found',
                                   rate_per100000=rate, search_interval=[0, 5],
                                   endpoint_gaps=[left, right]))
        elif left == 0 or right == 0:
            thresholds.append(dict(weight_reference=ref, status='endpoint_tie',
                                   rate_per100000=0. if left == 0 else 5.,
                                   search_interval=[0, 5], endpoint_gaps=[left, right]))
        else:
            thresholds.append(dict(weight_reference=ref, status='no_crossing_in_interval',
                                   rate_per100000=None, search_interval=[0, 5],
                                   endpoint_gaps=[left, right]))
    save(out,'vintage_ranks',pd.concat(vintage_rows,ignore_index=True))
    save(out,'witness_utilities',pd.DataFrame(completion_rows))
    save(out,'witness_cases',pd.DataFrame(case_rows))
    save(out,'summary',dict(version='V203',revision_diagnostics=reports,vintage_cases=vintage_reports,
                            hypothetical_rate_thresholds=thresholds,
                            minimum_strict_margin_by_weight={ref:min(r['strict_margin'] for r in case_rows if r['weight_reference']==ref) for ref in ['fixed','equal']},
                            uncertain_cells=48,point_cells=112,
                            scope='Same established point withdrawal, midpoint diagnostic, interior witnesses and hypothetical cutoffs rebased to V203; none is observation or prediction'))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('part',choices=['preferences','future','method','diagnostics'])
    part=parser.parse_args().part
    out=ROOT / ('results/task4_v203_'+part)
    if out.exists() and any(out.iterdir()):
        raise ValueError('Choose an absent or empty V203 output directory')
    out.mkdir(exist_ok=True)
    globals()[part](out)
    print('V203',part,'complete')
