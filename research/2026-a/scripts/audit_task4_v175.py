"""Audit every derived comparison using Decimal and original MC exports."""
from collections import defaultdict
from decimal import Decimal, localcontext
from itertools import combinations
from pathlib import Path
import csv
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results/task4_v175_mean_rank_comparisons'
PAPER = ROOT.parents[2] / 'HiMCM-Overleaf'


def read(path):
    return json.loads(path.read_text())


def rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    report = read(OUT / 'summary.json')
    for name, expected in report['input_sha256'].items():
        assert sha(ROOT / name) == expected, name
    prior = ROOT / 'results/task4_v169_mc_precision'
    for name, expected in read(prior / 'summary.json')['input_sha256'].items():
        assert sha(ROOT / name) == expected, name
    originals = {}
    for family, name, fields in [
        ('preferences', 'task4_v154_preferences/mc_city_summary.csv', ['profile', 'concentration']),
        ('future_shocks', 'task4_v154_future/future_mc_city_summary.csv', ['scenario', 'weight_reference', 'evidence_arm']),
        ('weights_only', 'task4_v154_future/weight_mc_city_summary.csv', ['scenario', 'weight_reference', 'evidence_arm', 'concentration'])
    ]:
        for row in rows(ROOT / 'results' / name):
            key = (family, json.dumps({k: row[k] for k in fields}, sort_keys=True), row['city'])
            assert key not in originals
            originals[key] = Decimal(row['mean_decision_rank'])
    assert len(originals) == 592
    groups = defaultdict(dict)
    with localcontext() as context:
        context.prec = 50
        width = Decimal(15) * ((Decimal(4128) / Decimal('.05')).ln() / Decimal(20000)).sqrt()
        for row in rows(prior / 'mean_bounds.csv'):
            if row['metric'] != 'mean_decision_rank':
                continue
            key = (row['family'], row['setting'], row['city'])
            estimate = Decimal(row['estimate'])
            assert estimate == originals[key]
            lower, upper = max(Decimal(1), estimate - width), min(Decimal(16), estimate + width)
            assert abs(lower - Decimal(row['lower'])) < Decimal('1e-14')
            assert abs(upper - Decimal(row['upper'])) < Decimal('1e-14')
            groups[key[:2]][key[2]] = (estimate, lower, upper)
        actual = {(x['family'], x['setting'], x['city_a'], x['city_b']): x for x in rows(OUT / 'pairs.csv')}
        assert len(actual) == 4440
        expected_keys = set()
        certified = 0
        min_separation = Decimal('Infinity')
        fronts, counts, adjacency = {}, {}, {}
        for group, values in groups.items():
            assert len(values) == 16
            better, worse = defaultdict(set), defaultdict(set)
            count = 0
            for a, b in combinations(sorted(values), 2):
                key = (*group, a, b)
                expected_keys.add(key)
                x = actual[key]
                av, al, au = values[a]
                bv, bl, bu = values[b]
                low, high = al - bu, au - bl
                for field, value in [('sample_mean_a', av), ('sample_mean_b', bv), ('gap_a_minus_b', av-bv), ('gap_lower', low), ('gap_upper', high)]:
                    assert abs(Decimal(x[field]) - value) < Decimal('2e-14'), (key, field)
                classification = 'unresolved'
                if high < Decimal('-1e-12'):
                    classification = 'a_lower_expected_mean_rank'
                    better[b].add(a)
                    worse[a].add(b)
                    min_separation = min(min_separation, -high)
                elif low > Decimal('1e-12'):
                    classification = 'b_lower_expected_mean_rank'
                    better[a].add(b)
                    worse[b].add(a)
                    min_separation = min(min_separation, low)
                assert x['classification'] == classification, key
                count += classification != 'unresolved'
            for a in values:
                assert a not in better[a] and not (better[a] & worse[a])
                for b in worse[a]:
                    assert worse[b] <= worse[a], 'Certified interval order must be transitive'
                adjacency[*group, a] = (better[a], worse[a])
            fronts[group] = {a for a in values if not better[a]}
            assert fronts[group]
            if len(fronts[group]) == 1:
                leader = next(iter(fronts[group]))
                assert len(worse[leader]) == 15
            counts[group] = count
            certified += count
        assert set(actual) == expected_keys
        city_rows = rows(OUT / 'cities.csv')
        assert len(city_rows) == len({(x['family'], x['setting'], x['city']) for x in city_rows}) == 592
        for x in city_rows:
            group = (x['family'], x['setting'])
            better, worse = adjacency[*group, x['city']]
            assert set(json.loads(x['certified_better_cities'])) == better
            assert set(json.loads(x['certified_worse_cities'])) == worse
            assert (x['in_unresolved_front'] == 'True') == (x['city'] in fronts[group])
        setting_rows = rows(OUT / 'settings.csv')
        assert len(setting_rows) == len({(x['family'], x['setting']) for x in setting_rows}) == 37
        for x in setting_rows:
            group = (x['family'], x['setting'])
            values = groups[group]
            assert int(x['pairs']) == 120 and int(x['certified_pairs']) == counts[group]
            assert int(x['unresolved_pairs']) == 120 - counts[group]
            assert set(json.loads(x['unresolved_mean_rank_front'])) == fronts[group]
            minimum = min(v[0] for v in values.values())
            assert set(json.loads(x['sample_mean_leaders'])) == {a for a, v in values.items() if v[0] == minimum}
            assert (x['unique_smallest_expectation_certified'] == 'True') == (len(fronts[group]) == 1)
    assert report['certified_pairs'] == certified == 4254
    assert report['unresolved_pairs'] == 186
    assert report['settings_with_unique_smallest_expected_mean_rank'] == sum(len(x) == 1 for x in fronts.values()) == 22
    protected = read(OUT / 'protected_files.json')
    for name, expected in protected['science'].items():
        assert sha(ROOT / name) == expected, name
    for name, expected in protected['paper'].items():
        assert sha(PAPER / name) == expected, name
    result = dict(version='V175', status='pass', independent_decimal_precision=50,
                  original_MC_mean_rows_checked=592, pairwise_rows_checked=4440,
                  city_rows_checked=592, setting_rows_checked=37,
                  certified=certified, unresolved=186,
                  smallest_certified_zero_separation=str(min_separation),
                  acyclic_transitive_interval_order=True, singleton_front_beats_all_15=True,
                  scientific_files_unchanged=len(protected['science']),
                  existing_paper_files_unchanged=len(protected['paper']),
                  raw_draws_replayed=False, manuscript_changed=False,
                  output_sha256={p.name: sha(p) for p in [OUT/'pairs.csv', OUT/'cities.csv', OUT/'settings.csv', OUT/'summary.json']},
                  audit_script_sha256=sha(Path(__file__)))
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
