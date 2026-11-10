"""Derive within-setting mean-rank comparisons from frozen simultaneous bands.

This reads existing V203 exports; no new draws, rankings or model inputs.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import argparse
import csv
import hashlib
import json
import math
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT.parents[2] / 'HiMCM-Overleaf'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def write_rows(path, records):
    with path.open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(records)


def tracked_hashes(repo):
    names = subprocess.check_output(['git', '-C', str(repo), 'ls-files', '-z']).decode().split('\0')[:-1]
    return {name: sha(repo / name) for name in names}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path,
                        default=ROOT / 'results/task4_v203_mean_rank_comparisons')
    out = parser.parse_args().output_dir
    if out.exists() and (not out.is_dir() or any(out.iterdir())):
        raise ValueError('Choose a new or empty output directory; frozen results are not overwritten')
    prior = ROOT / 'results/task4_v203_mc_precision'
    summary = read(prior / 'summary.json')
    assert summary['base_means'] > 0 and summary['familywise_alpha'] == .05
    for name, expected in summary['input_sha256'].items():
        assert sha(ROOT / name) == expected, name
    inputs = [prior / x for x in ['mean_bounds.csv', 'summary.json']]
    inputs += [Path(__file__)]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    groups = defaultdict(list)
    for row in rows(prior / 'mean_bounds.csv'):
        if row['metric'] == 'mean_decision_rank':
            groups[row['family'], row['setting']].append(row)
    assert len(groups) == summary['settings']
    assert sum(map(len, groups.values())) == summary['mean_rank_means']
    pairs, settings, city_rows = [], [], []
    for (family, setting), group in sorted(groups.items()):
        assert len(group) == len({r['city'] for r in group}) == 16
        group.sort(key=lambda r: r['city'])
        better = defaultdict(list)
        worse = defaultdict(list)
        local = []
        for a, b in combinations(group, 2):
            lower = float(a['lower']) - float(b['upper'])
            upper = float(a['upper']) - float(b['lower'])
            # Guard signs at floating arithmetic resolution; no change to the bands.
            classification = 'unresolved'
            if upper < -1e-12:
                classification = 'a_lower_expected_mean_rank'
                better[b['city']].append(a['city'])
                worse[a['city']].append(b['city'])
            elif lower > 1e-12:
                classification = 'b_lower_expected_mean_rank'
                better[a['city']].append(b['city'])
                worse[b['city']].append(a['city'])
            record = dict(family=family, setting=setting, city_a=a['city'], city_b=b['city'],
                          sample_mean_a=float(a['estimate']), sample_mean_b=float(b['estimate']),
                          gap_a_minus_b=float(a['estimate']) - float(b['estimate']),
                          gap_lower=lower, gap_upper=upper, classification=classification)
            local.append(record)
        unresolved_front = sorted(r['city'] for r in group if not better[r['city']])
        sample_min = min(float(r['estimate']) for r in group)
        sample_leaders = sorted(r['city'] for r in group if float(r['estimate']) == sample_min)
        for row in group:
            city_rows.append(dict(family=family, setting=setting, city=row['city'],
                                  sample_mean=float(row['estimate']), lower=float(row['lower']),
                                  upper=float(row['upper']),
                                  certified_better_cities=json.dumps(sorted(better[row['city']])),
                                  certified_worse_cities=json.dumps(sorted(worse[row['city']])),
                                  in_unresolved_front=not better[row['city']]))
        settings.append(dict(family=family, setting=setting, pairs=len(local),
                             certified_pairs=sum(r['classification'] != 'unresolved' for r in local),
                             unresolved_pairs=sum(r['classification'] == 'unresolved' for r in local),
                             sample_mean_leaders=json.dumps(sample_leaders),
                             unresolved_mean_rank_front=json.dumps(unresolved_front),
                             unique_smallest_expectation_certified=len(unresolved_front) == 1))
        pairs.extend(local)
    assert len(pairs) == sum(math.comb(len(group), 2) for group in groups.values())
    for name, expected in hashes.items():
        assert sha(ROOT / name) == expected, name
    out.mkdir(parents=True, exist_ok=True)
    for name, data in [('pairs.csv', pairs), ('settings.csv', settings), ('cities.csv', city_rows)]:
        write_rows(out / name, data)
    report = dict(version='V203', primary_science='V203 staged', current_paper='unchanged',
                  settings=len(groups), unordered_within_setting_pairs=len(pairs),
                  certified_pairs=sum(r['classification'] != 'unresolved' for r in pairs),
                  unresolved_pairs=sum(r['classification'] == 'unresolved' for r in pairs),
                  settings_with_unique_smallest_expected_mean_rank=sum(r['unique_smallest_expectation_certified'] for r in settings),
                  inherited_common_event_base_means=summary['base_means'], inherited_familywise_alpha=.05,
                  additional_multiplicity_penalty=False,
                  scope='Expected mean decision ranks under declared conditional simulation laws; smaller is better. No real-world winner claim.',
                  arithmetic='[L_a-U_b,U_a-L_b]; strict signs use 1e-12 numerical guard',
                  raw_draws_replayed=False, activated_data_admissions=0, active_model_changed=False,
                  manuscript_changed=False, input_sha256=hashes)
    (out / 'summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'input_sha256'}, indent=2))


if __name__ == '__main__':
    main()
