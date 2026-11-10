"""Decode the archived Oslo crime cells without changing the supplied input."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

R = Path(__file__).resolve().parents[1]
D = R / 'data/current_oslo_homicide_lineage'
SOURCE = R / 'data/task4_v117_team_intake/city_indicators.csv'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def decode(obj, coords):
    flat = sum(obj['dimension'][key]['category']['index'][coords[key]] * math.prod(obj['size'][i+1:])
               for i, key in enumerate(obj['id']))
    return obj['value'][str(flat)]


def audit():
    for source in json.loads((D/'sources.json').read_text())['sources']:
        p = D/source['file']
        assert p.stat().st_size == source['bytes'] and sha(p) == source['sha256']
    row = next(r for r in csv.DictReader(SOURCE.open(encoding='utf-8-sig', newline='')) if r['city'] == 'Oslo')
    assert (row['homicide_per_100k'], row['homicide_per_100k_year'], row['homicide_per_100k_flag'],
            row['homicide_numerator']) == ('1.71', '2008', 'STALE', '12.0')
    rows = []
    for file, dataset in [('eurostat_offences_2008.json', 'CRIM_HOM_OCIT'),
                          ('eurostat_victims_2008.json', 'CRIM_HOM_VCIT')]:
        obj = json.loads((D/file).read_text())
        assert obj['extension']['id'] == dataset
        assert obj['dimension']['cities']['category']['label']['NO001C'] == 'Oslo (greater city)'
        coords = dict(freq='A', cities='NO001C', time='2008')
        if 'sex' in obj['id']:
            coords['sex'] = 'T'
        for unit, expected in [('NR', 12), ('P_HTHAB', 2.14)]:
            value = decode(obj, dict(coords, unit=unit))
            assert value == expected
            rows.append(dict(dataset=dataset, unit=unit, value=value))
    files = [p for p in D.iterdir() if p.is_file()] + [SOURCE, Path(__file__).resolve()]
    return dict(status='pass bounded archive and JSON-stat check',
        source_sha256={str(p.relative_to(R)): sha(p) for p in sorted(files)},
        decoded_cells=rows, submitted_rate=1.71, rate_numeric_match=False,
        numerator_numeric_match=True, original_extraction_lineage_verified=False,
        historical_boundary_and_original_denominator_verified=False,
        independent_review='Luna tbz_packet_check: all4 raw hashes/sizes, independent dimension decoding, '
                           'original CSV and methodological guide pp11–12 checked; no issue found.',
        primary_admissions=0, actual_primary_width_reduction=0,
        changes_primary_model=False, changes_manuscript=False,
        scope='Count-only current-series match, distinct offence/victim concepts. '
              'Neither a replacement rate nor proof the supplied rate is wrong. '
              'The current greater-city label does not establish the2008 boundary.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = json.dumps(audit(), ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as handle:
            handle.write(raw)
    else:
        print(raw, end='')
