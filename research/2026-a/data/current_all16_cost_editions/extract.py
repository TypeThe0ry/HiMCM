#!/usr/bin/env python3
"""Extract the archived Numbeo edition cells for the original 16 cities; offline only."""
import argparse, csv, hashlib, html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
INPUT = ROOT / 'research/2026-a/data/task4_v117_team_intake/city_indicators.csv'
SOURCES = ROOT / 'research/2026-a/data/city_matrix_25_audit/sources'
OUT = ROOT / 'research/2026-a/data/current_all16_cost_editions'
EDITIONS = [('2026', '2026'), ('mid', 'Mid-Year'), ('current', 'Current (Nov 7 archive)')]
INDICATORS = {'cli': ('cost-of-living', 'Cost of Living Index'), 'pir': ('property-investment', 'Price To Income Ratio')}
COUNTRY_ALIASES = {('Prague', 'Czechia'): 'Czech Republic'}


def text(fragment):
    fragment = re.sub(r'<[^>]+>', '', fragment)
    return re.sub(r'\s+', ' ', html.unescape(fragment)).strip()


def rows(path):
    raw = path.read_bytes()
    source = raw.decode('utf-8', errors='replace')
    table = re.search(r'<table\b(?=[^>]*\bid=["\']t2["\'])[^>]*>(.*?)</table>', source, re.I|re.S)
    if not table:
        raise ValueError(f'No table t2 in {path}')
    result = {}
    for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>', table.group(1), re.I|re.S):
        cells = [text(x) for x in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', tr, re.I|re.S)]
        if not cells or cells[0].lower() == 'rank' or len(cells) < 3: continue
        city = cells[1]
        rank = len(result) + 1  # source rows are already ordered by rank; displayed rank cell is blank
        result[city] = (rank, cells)
    return raw, result


def build():
    original = list(csv.DictReader(INPUT.open(encoding='utf-8-sig', newline='')))
    cache, files = {}, {}
    for ind, (prefix, _) in INDICATORS.items():
        for edition, _label in EDITIONS:
            p = SOURCES / f'{prefix}_{edition}.html'
            raw, table = rows(p)
            cache[(ind, edition)] = table
            files[str(p.relative_to(ROOT))] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
    out = []
    for record in original:
        for ind in ('cli', 'pir'):
            city, country = record['city'], record['country']
            alias_country = COUNTRY_ALIASES.get((city, country), country)
            source_city = f'{city}, {alias_country}'
            vals, ranks, links, matched = {}, {}, {}, []
            for edition, _ in EDITIONS:
                found = cache[(ind, edition)].get(source_city)
                vals[edition], ranks[edition], links[edition] = ('', '', '')
                if found:
                    rank, cells = found
                    col = 2
                    vals[edition], ranks[edition] = cells[col], rank
                    prefix = INDICATORS[ind][0]
                    links[edition] = f'../city_matrix_25_audit/sources/{prefix}_{edition}.html#t2'
                    if float(cells[col]) == float(record[ind]): matched.append(edition)
            out.append({
                'city': city, 'country': country, 'indicator': ind,
                'input_value': record[ind], 'input_year': record[f'{ind}_year'], 'input_flag': record[f'{ind}_flag'],
                '2026_value': vals['2026'], '2026_rank': ranks['2026'], '2026_source': links['2026'],
                'mid_value': vals['mid'], 'mid_rank': ranks['mid'], 'mid_source': links['mid'],
                'current_value': vals['current'], 'current_rank': ranks['current'], 'current_source': links['current'],
                'exact_matches': '|'.join(matched), 'source_label': 'Numbeo archived table t2; 2026 annual edition / 2026 Mid-Year / Current Nov 7 archive',
                'source_city_alias': source_city if source_city != f'{city}, {country}' else ''
            })
    return out, files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write comparison.csv and summary.json; default emits CSV on stdout')
    args = ap.parse_args()
    data, files = build()
    fields = list(data[0])
    import io
    buf = io.StringIO(newline='')
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator='\n'); w.writeheader(); w.writerows(data)
    if not args.write:
        print(buf.getvalue(), end=''); return
    (OUT/'comparison.csv').write_text(buf.getvalue(), encoding='utf-8', newline='')
    missing = {f'{ind}_{edition}': sum(not x[f'{edition}_value'] for x in data if x['indicator']==ind) for ind in ('cli','pir') for edition,_ in EDITIONS}
    summary = {
      'input': str(INPUT.relative_to(ROOT)), 'source_files': files,
      'scope': {'cities': len(data)//2, 'indicators': ['cli','pir'], 'cells_expected': len(data)*3, 'cells_available': len(data)*3-sum(missing.values()), 'missing_cells_by_indicator_edition': missing},
      'exact_match_counts_by_indicator_edition': {ind: {edition: sum(edition in x['exact_matches'].split('|') for x in data if x['indicator']==ind) for edition,_ in EDITIONS} for ind in ('cli','pir')},
      'exact_match_row_counts': {ind: sum(bool(x['exact_matches']) for x in data if x['indicator']==ind) for ind in ('cli','pir')},
      'lineage_unknowns': ['Original CSV does not identify source URL, retrieval date, table cell, Numbeo edition, or extraction method for CLI/PIR.', 'City boundary equivalence between the CSV entries and Numbeo rows is not documented.', 'Input year 2026 does not establish that values were measured over calendar year 2026.'],
      'source_labels': {'2026': 'Numbeo annual 2026 edition, not a claim of calendar-year measurement', 'mid': 'Numbeo 2026 Mid-Year edition', 'current': 'Current table copied to archive Nov 7, 2026; not live current data'},
      'matching': 'Exact displayed city and country after explicit country alias map only; repeated exact values may match multiple editions. A nonmatch is not evidence the input is erroneous; absent source cells remain blank, never zero.'
    }
    (OUT/'summary.json').write_text(json.dumps(summary, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f"wrote {len(data)} rows; {summary['scope']['cells_available']}/{summary['scope']['cells_expected']} edition cells present")

if __name__ == '__main__': main()
