"""Independent long-double replay of saved stress results; no model imports."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
D = np.longdouble

def rows(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))

def calculate(z, alpha):
    w = np.full(10, (1-alpha)/8, dtype=D)
    w[[6, 9]] = alpha/2
    positive = np.sqrt(np.sum(w*z*z, axis=1))
    negative = np.sqrt(np.sum(w*(1-z)*(1-z), axis=1))
    return 100*positive/(positive+negative)

def regret(lower, upper):
    return np.array([max(D(0), max(np.delete(upper, i))-lower[i]) for i in range(len(lower))])

def expanded(lo, hi, epsilon, target):
    l, h = lo.copy(), hi.copy()
    index = slice(None) if target is None else target
    l[index] = np.maximum(0, l[index]-epsilon)
    h[index] = np.minimum(1, h[index]+epsilon)
    return l, h

def enclosure(lo, hi, e0, e1, a0, a1, target):
    small_l, small_h = expanded(lo, hi, e0, target)
    large_l, large_h = expanded(lo, hi, e1, target)
    padding = D('1e-9')
    lower_min = np.minimum(calculate(large_l, a0), calculate(large_l, a1))-padding
    lower_max = np.maximum(calculate(small_l, a0), calculate(small_l, a1))+padding
    upper_min = np.minimum(calculate(small_h, a0), calculate(small_h, a1))-padding
    upper_max = np.maximum(calculate(large_h, a0), calculate(large_h, a1))+padding
    return regret(lower_max, upper_min), regret(lower_min, upper_max)

def main():
    summary = json.loads((HERE/'summary.json').read_text())
    saved = rows(HERE/'baseline/utility_bounds.csv')
    cities = list(dict.fromkeys(r['city'] for r in saved))
    assert len(saved) == 250 and len(cities) == 25
    lo = np.array([D(r['lower']) for r in saved]).reshape(25, 10)
    hi = np.array([D(r['upper']) for r in saved]).reshape(25, 10)
    digest = hashlib.sha256(np.stack([lo, hi]).astype('<f8').tobytes()).hexdigest()
    assert digest == summary['input_bounds_sha256']
    choice = cities.index(summary['baseline_choice'])
    max_error = D(0)
    scenarios = rows(HERE/'scenario_ranks.csv')
    cache = {}
    for r in scenarios:
        key = r['structure'], D(r['epsilon']), D(r['alpha'])
        if key not in cache:
            target = None if key[0] == 'uniform' else choice
            l, h = expanded(lo, hi, D(key[1]), target)
            lower, upper = calculate(l, D(key[2])), calculate(h, D(key[2]))
            rr = regret(lower, upper)
            cache[key] = lower, upper, rr
        lower, upper, rr = cache[key]
        i = cities.index(r['city'])
        for field, value in [('score_lower', lower[i]), ('score_upper', upper[i]), ('max_regret', rr[i])]:
            max_error = max(max_error, abs(value-D(r[field])))
        assert int(r['decision_rank']) == 1+sum(rr < rr[i])
        assert (r['possible_champion'] == 'True') == (upper[i] >= max(np.delete(lower, i))-D('1e-12'))
    assert max_error < D('1e-11')
    # Independently recompute the reported failure witness and all summary cases.
    for case in summary['scenarios']:
        key = case['structure'], D(str(case['epsilon'])), D(str(case['alpha']))
        lower, upper, rr = cache[key]
        gap = min(np.delete(rr, choice))-rr[choice]
        assert abs(gap-D(str(case['baseline_choice_gap']))) < D('1e-11')
        assert case['choices'] == [cities[i] for i in range(25) if abs(rr[i]-min(rr)) < D('1e-10')]
        possible = sum(upper[i] >= max(np.delete(lower,i))-D('1e-12') for i in range(25))
        assert case['possible_champions'] == possible
    failures = [c for c in summary['scenarios'] if c['structure'] == 'recommendation_city_only' and c['baseline_choice_gap'] < -1e-8]
    assert summary['targeted_failure_witness'] == min(failures, key=lambda c:(c['epsilon'],c['alpha']))
    gap_error = D(0)
    counts = []
    for name, target, emax in [('uniform_prefix_certificate.csv', None, D('.2')),
                               ('targeted_prefix_certificate.csv', choice, D('.042'))]:
        rectangles = rows(HERE/name)
        area = D(0)
        coordinates = []
        for r in rectangles:
            e0, e1, a0, a1 = [D(r[k]) for k in ('epsilon_lower', 'epsilon_upper', 'alpha_lower', 'alpha_upper')]
            assert 0 <= e0 < e1 <= emax and D('.05') <= a0 < a1 <= D('.2')
            low, high = enclosure(lo, hi, e0, e1, a0, a1, target)
            gap = min(np.delete(low, choice))-high[choice]
            gap_error = max(gap_error, abs(gap-D(r['gap_lower'])))
            assert (r['certified'] == 'True') == (gap > D('1e-8'))
            assert r['certified'] == 'True'
            area += (e1-e0)*(a1-a0)
            coordinates.append((e0, e1, a0, a1))
        assert abs(area-emax*D('.15')) < D('1e-16')
        for k, (e0, e1, a0, a1) in enumerate(coordinates):
            for f0, f1, b0, b1 in coordinates[k+1:]:
                assert min(e1, f1) <= max(e0, f0) or min(a1, b1) <= max(a0, b0)
        counts.append(len(rectangles))
    fixed = rows(HERE/'targeted_epsilon02_certificate.csv')
    last = D('.05')
    for r in fixed:
        a0, a1 = D(r['alpha_lower']), D(r['alpha_upper'])
        assert a0 == last
        last = a1
        winner = cities.index(r['city'])
        assert winner == int(r['winner'])
        low, high = enclosure(lo, hi, D('.2'), D('.2'), a0, a1, choice)
        gap = min(np.delete(low, winner))-high[winner]
        gap_error = max(gap_error, abs(gap-D(r['regret_gap_lower'])))
        assert r['certified'] == 'True' and gap > D('1e-8')
    assert last == D('.2') and gap_error < D('1e-11')
    assert summary['uniform_certificate']['leaves'] == counts[0]
    assert summary['targeted_prefix_certificate']['leaves'] == counts[1]
    assert summary['targeted_fixed_certificate']['leaves'] == len(fixed)
    assert all(summary[k]['unresolved'] == 0 for k in
               ('uniform_certificate', 'targeted_prefix_certificate', 'targeted_fixed_certificate'))
    old_saved = rows(HERE.parent/'task4_v93_joint_stress/baseline/utility_bounds.csv')
    changed = []
    for old, new in zip(old_saved, saved):
        assert (old['city'], old['indicator']) == (new['city'], new['indicator'])
        if (old['lower'], old['upper']) != (new['lower'], new['upper']):
            changed.append((new['city'], new['indicator']))
    assert len(old_saved) == len(saved) and changed == [('Warsaw', 'upper_secondary_ptr')]
    prior = json.loads((HERE.parent/'task4_v93_joint_stress/summary.json').read_text())
    assert prior['model_version'] == 'V91' and summary['model_version'] == 'V96'
    diagnostic_keys = ['uniform_certificate', 'targeted_prefix_certificate', 'targeted_fixed_certificate', 'targeted_failure_witness']
    same_diagnostics = all(prior[k] == summary[k] for k in diagnostic_keys)
    result = dict(independent_arithmetic='NumPy longdouble from saved 250 bounds; no model scoring imports',
        input_hash_verified=True, changed_cells_vs_V93=changed, summary_cases_and_failure_witness_verified=True, checked_scenario_rows=len(scenarios), checked_scenarios=len(cache),
        maximum_score_or_regret_discrepancy=float(max_error),
        maximum_enclosure_gap_discrepancy=float(gap_error),
        prefix_rectangles_cover_domains_without_interior_overlap=True,
        prefix_leaf_counts=counts, fixed_expansion_alpha_leaves=len(fixed),
        historical_model='V91', current_model='V96', specified_diagnostics_exactly_equal_to_V93=same_diagnostics)
    (HERE/'independent_check.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
