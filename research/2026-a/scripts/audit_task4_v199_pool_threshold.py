"""Independent bisection and integer audit of conditional V199 pool thresholds."""
import csv
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from task4_user_v197_revision import revised_bounds
from task4_v5_model import ROOT, NAMES

OUT = ROOT / 'results/task4_v199_priority'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def scores(a, weights):
    result = []
    for row in a:
        plus = math.sqrt(math.fsum(float(w) * float(x)**2 for w, x in zip(weights, row)))
        minus = math.sqrt(math.fsum(float(w) * (1-float(x))**2 for w, x in zip(weights, row)))
        result.append(100 * plus / (plus + minus))
    return result

def main():
    inputs = [OUT/'pool_count_thresholds.json', OUT/'pool_count_threshold_probes.csv', ROOT/'scripts/task4_v199_pool_threshold.py', ROOT/'design/task4_user_v197_snapshot.json']
    nav = [ROOT/'design'/f'task4_user_current_{n}.json' for n in ['model','extensions','review','delivery']]
    protected = {str(p.relative_to(ROOT)): sha(p) for p in inputs + nav}
    report = json.loads(inputs[0].read_text())
    snapshot = json.loads(inputs[3].read_text())['source_sha256']
    assert len(snapshot) == 361
    for name, digest in snapshot.items():
        assert sha(ROOT/name) == digest, name
    for name, digest in report['source_sha256'].items():
        assert sha(ROOT/name) == digest, name
    f, lo, hi = revised_bounds()
    original = np.stack([lo,hi]).copy()
    cities = f.city.tolist()
    i, j = cities.index('Singapore'), NAMES.index('public_pool_density')
    pop = int(f.iloc[i].population)
    assert pop == 6036900 and int(f.iloc[i].population_year) == 2024 and hi[i,j] == 1.0
    with inputs[1].open(newline='') as fp:
        probes = list(csv.DictReader(fp))
    assert len(probes) == 6
    verified = []
    for ref, weights in [('fixed', [0.1125]*6+[0.05,0.1125,0.1125,0.05]), ('equal', [0.1]*10)]:
        upper = scores(hi, weights)
        def case(count):
            density = count * 100000 / pop
            value = density / (1 + density)
            assert lo[i,j] - 1e-14 <= value <= hi[i,j]
            a = lo.copy()
            a[i,j] = value
            mask = np.ones_like(lo, dtype=bool)
            mask[i,j] = False
            np.testing.assert_array_equal(a[mask], lo[mask])
            lower = scores(a, weights)
            regrets = [max(0., max(upper[k] for k in range(16) if k != c) - lower[c]) for c in range(16)]
            others = min(regrets[k] for k in range(16) if k != i)
            choices = ';'.join(cities[k] for k in range(16) if regrets[k] <= min(regrets)+1e-12)
            return regrets[i]-others, choices
        left, right = 7., 500.
        assert case(left)[0] > 0 and case(right)[0] < 0
        for _ in range(80):
            mid = (left+right)/2
            if case(mid)[0] > 0:
                left = mid
            else:
                right = mid
        root = (left+right)/2
        integer = math.floor(root)+1
        record = next(x for x in report['results'] if x['weight_reference'] == ref)
        assert abs(record['continuous_count_tie']-root) < 1e-9
        assert record['first_integer_count_for_strict_Singapore_recommendation'] == integer
        assert record['population'] == pop and record['population_year'] == 2024 and record['utility_upper_retained'] == hi[i,j]
        assert all(case(n)[0] > 0 for n in range(7, integer))
        assert case(integer)[0] < 0 and case(integer)[1] == 'Singapore'
        rows = [p for p in probes if p['weight_reference'] == ref]
        assert {int(p['pool_count']) for p in rows} == {7,integer-1,integer}
        for p in rows:
            gap, choices = case(int(p['pool_count']))
            assert abs(gap-float(p['regret_gap_Singapore_minus_best_other'])) < 1e-10
            assert choices == p['conservative_recommendation']
        verified.append(dict(weight_reference=ref, continuous_count_tie=root, first_strict_integer=integer, gap_previous=case(integer-1)[0], gap_first=case(integer)[0]))
    _, a, b = revised_bounds()
    np.testing.assert_array_equal(original, np.stack([a,b]))
    for name, digest in {**snapshot, **protected}.items():
        assert sha(ROOT/name) == digest, name
    verification = dict(status='pass', method='Independent scalar weights-once scores, self-excluded regret, bisection and exhaustive retained integer probes before first strict recommendation', results=verified, immutable_snapshot_bindings=len(snapshot), original_160_bounds_and_four_navigation_files_unchanged=True, scope='Conditional mathematical thresholds only; not observations or admissions.', source_sha256={**protected, str(Path(__file__).relative_to(ROOT)): sha(Path(__file__))})
    (OUT/'pool_threshold_verification.json').write_text(json.dumps(verification, indent=2)+'\n')
    print(json.dumps(verification, indent=2))

if __name__ == '__main__':
    main()
