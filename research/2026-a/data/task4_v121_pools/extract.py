"""Offline extraction of the current Stockholm municipal swimming-facility subset."""
from pathlib import Path
from html import unescape
import hashlib
import json
import re
import csv

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    texts = {}
    for filename in ('stockholm_simhallarna.html', 'stockholm_overview.html'):
        html = (HERE / filename).read_text()
        main_html = re.search(r'<main\b.*?</main>', html, re.S).group()
        texts[filename] = re.sub(r'\s+', ' ', unescape(re.sub('<[^>]+>', ' ', main_html))).strip()
    assert 'Stockholms stad har 13 simhallar' in texts['stockholm_overview.html']
    html = (HERE / 'stockholm_simhallarna.html').read_text()
    catalogue = re.search(r'<main\b.*?</main>', html, re.S).group().split('Simhallar i Stockholm')[0]
    headings = [unescape(re.sub('<[^>]+>', ' ', m)).strip()
                for m in re.findall(r'<h3\b[^>]*>(.*?)</h3>', catalogue, re.S)]
    closed = [h for h in headings if 'stängd för renovering' in h]
    assert closed == ['Vällingby simhall (stängd för renovering)']
    facilities = [h for h in headings if h not in closed]
    assert len(facilities) == len(set(facilities)) == 13, facilities
    assert 'Nälstabadet' in facilities
    with (ROOT / 'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig') as stream:
        row = next(r for r in csv.DictReader(stream) if r['city'] == 'Stockholm')
    population = int(row['population'])
    assert population == 999200 and row['pools_per_100k'] == ''
    density = len(facilities) * 100000 / population
    observation = dict(
        city='Stockholm', indicator='public_pool_density', raw_count=len(facilities),
        population=population, population_year=2025, sourceyear=2026,
        utility_before=[0, 1], utility_after=[density / (1 + density), 1],
        density_per_100000_lower=density, lower_bound_only=True,
        source_url='https://motionera.stockholm/trana-gymma-simma/simhallarna/',
        source_files=['stockholm_simhallarna.html', 'stockholm_overview.html'],
        accessed='2026-11-08',
        scope='Current municipal public swimming-facility subset in Stockholm. '
              '13 distinct named facilities, excluding Vällingby closed for renovation; '
              'includes Nälstabadet, operated year-round during that renovation. '
              'Count facilities once, not individual basins. Current web snapshot with fixed attachment population.',
        limitations='Not an all-provider census, not teenage accessibility or use. '
                    'Unknown other providers retain upper utility 1. '
                    'Page footer says updated 2025-06-18 but this is an accessed-2026 snapshot, '
                    'not a reconstructed 2025 inventory.')
    (HERE / 'observations.json').write_text(json.dumps([observation], ensure_ascii=False, indent=2) + '\n')
    (HERE / 'facilities.json').write_text(json.dumps(dict(included=facilities, excluded_closed=closed), ensure_ascii=False, indent=2) + '\n')
    (HERE / 'source_text.json').write_text(json.dumps(texts, ensure_ascii=False, indent=2) + '\n')
    paths = ['stockholm_simhallarna.html', 'stockholm_overview.html', 'extract.py',
             'observations.json', 'facilities.json', 'source_text.json']
    (HERE / 'manifest.json').write_text(json.dumps(dict(
        accessed='2026-11-08', provider='Stockholms stad',
        sources={
            'stockholm_simhallarna.html': 'https://motionera.stockholm/trana-gymma-simma/simhallarna/',
            'stockholm_overview.html': 'https://motionera.stockholm/trana-gymma-simma/'},
        source_hashes={p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in paths}
    ), ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(observation, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
