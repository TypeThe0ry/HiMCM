"""Independently check generated ROR rosters and JSON/CSV location differences."""
from pathlib import Path
import csv, hashlib, io, json, unicodedata, zipfile
from task4_audit_output import audit_parser, check_output, emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
D = R / 'data/current_all16_ror_rosters'
O = R / 'results/current_all16_ror_review/verification.json'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(encoding='utf-8-sig', newline='') as f: return list(csv.DictReader(f))
def read(p): return json.loads(p.read_text())
def norm(s):
    return ' '.join(''.join(c for c in unicodedata.normalize('NFKD', s).casefold()
                            if not unicodedata.combining(c)).split())

def main():
    a = audit_parser(__doc__).parse_args(); check_output(a, O, G)
    archive = R / 'data/task4_v5_resources/ror_2026_10_06.zip'
    assert sha(archive) == '555b38a4b586759de1fa278b0e751433a13dd541f375097db53b186cfcdc768a'
    with zipfile.ZipFile(archive) as z:
        members = [n for n in z.namelist() if n.endswith('.json')]
        assert members == ['v2.14-2026-10-06-ror-data.json']
        records = json.loads(z.read(members[0]))
        flat = list(csv.DictReader(io.TextIOWrapper(z.open('v2.14-2026-10-06-ror-data.csv'), encoding='utf-8-sig')))
    assert len(records) == 144717
    raw = rows(R / 'data/task4_v117_team_intake/city_indicators.csv')
    assert len(raw) == 16
    roster = rows(D / 'ror_education_rosters.csv')
    assert len(roster) == len({x['id'] for x in roster}) == 1008
    comparison = read(D / 'city_comparison.json')
    assert comparison['unique_ror_ids_across_all_city_rosters'] == 1008
    assert comparison['sources']['ror_archive_sha256'] == sha(archive)
    assert comparison['sources']['original_city_csv_sha256'] == sha(R / 'data/task4_v117_team_intake/city_indicators.csv')
    assert all(not v for v in comparison['selection']['aliases'].values())
    expected_counts = [42,23,14,55,156,15,24,105,41,17,28,28,54,65,118,223]
    results = []
    for city, expected_count, saved in zip(raw, expected_counts, comparison['cities'], strict=True):
        matches = {}
        for item in records:
            if item['status'] != 'active' or 'education' not in item['types']: continue
            locations = [l for l in item['locations']
                         if l['geonames_details']['country_code'] == city['iso2']
                         and norm(l['geonames_details']['name']) == norm(city['city'])]
            if locations: matches[item['id']] = (item, locations)
        selected = [x for x in roster if x['matched_city'] == city['city']]
        assert {x['id'] for x in selected} == set(matches)
        assert len(matches) == expected_count == saved['json_any_location_unique_ror_id_count']
        assert saved['city'] == city['city'] and saved['iso2'] == city['iso2']
        assert saved['original_he_count'] == float(city['he_count'])
        assert saved['json_minus_original_he_count'] == expected_count - float(city['he_count'])
        for x in selected:
            item, locations = matches[x['id']]
            assert x['status'] == item['status'] == 'active'
            assert {v.strip() for v in x['types'].split(';')} == set(item['types'])
            assert x['display_name'] == next(n['value'] for n in item['names'] if 'ror_display' in n['types'])
            assert json.loads(x['matched_locations_json']) == locations
            assert json.loads(x['all_locations_json']) == item['locations']
            assert x['matched_iso2'] == city['iso2']
        first_ids = {x['id'] for x in flat if x['status'] == 'active' and 'education' in [v.strip() for v in x['types'].split(';')] and x['locations.geonames_details.country_code'] == city['iso2'] and norm(x['locations.geonames_details.name']) == norm(city['city'])}
        assert first_ids <= set(matches)
        assert len(first_ids) == saved['csv_first_location_count']
        missing = sorted(x.rsplit('/',1)[-1] for x in set(matches)-first_ids)
        assert missing == comparison['missing_from_csv_first_location_ids_by_city'][city['city']]
        assert saved['json_minus_csv_first_location_count'] == saved['missing_from_csv_first_location_count'] == len(missing)
        results.append(dict(city=city['city'], CSV_first_location_count=len(first_ids), missing_from_CSV_first_location=missing, original_count=int(city['he_count']),
                            roster_count=expected_count, count_matches=expected_count == int(city['he_count']),
                            geonames_ids=sorted({l['geonames_id'] for _, locs in matches.values() for l in locs})))
    sg = [r for r in records if r['status'] == 'active' and 'education' in r['types']
          and any(l['geonames_details']['country_code'] == 'SG' for l in r['locations'])]
    assert len(sg) == 120
    assert sum(any(l['geonames_id'] == 1880252 for l in r['locations']) for r in sg) == 118
    assert sum(x['count_matches'] for x in results) == 4
    assert sum(len(x['missing_from_CSV_first_location']) for x in results) == 2
    assert sum(any(l['geonames_id'] == 1881955 for l in r['locations']) for r in sg) == 2
    current = read(R / 'results/current_paper_review/current_verification.json')
    protected = protected_inputs()
    for n,h in current['edition_source_sha256'].items(): assert sha(R / n) == h
    sources = [archive, R / 'data/task4_v117_team_intake/city_indicators.csv',
               *sorted(D.glob('*')), Path(__file__)]
    report = dict(status='pass scoped offline roster comparison', **protected,
                  edition_entries_checked=24, JSON_records_examined=144717,
                  matched_unique_ROR_IDs=1008, CSV_first_location_omitted_IDs=2, cities=results,
                  exact_count_matches=4, different_counts=12, Singapore_country_count=120,
                  original_extraction_lineages_verified=0, accredited_HE_counts_verified=0,
                  primary_admissions=0, actual_primary_width_reduction=0,
                  source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
                  scope='JSON independently checks generated roster membership, display names, status, types and geographic IDs; the archive CSV first-location omissions are checked separately. Education tags and GeoNames labels do not establish higher-education eligibility or municipal coverage. Count differences are not proof of original input errors; primary and paper unchanged.')
    emit_report(report,a,O,G)

if __name__ == '__main__': main()
