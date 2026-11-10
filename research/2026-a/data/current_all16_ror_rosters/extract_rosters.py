#!/usr/bin/env python3
"""Extract current 16-city ROR education rosters from the archived JSON snapshot."""
from __future__ import annotations
import csv, hashlib, io, json, unicodedata, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
ROR = ROOT / 'research/2026-a/data/task4_v5_resources/ror_2026_10_06.zip'
CITY_CSV = ROOT / 'research/2026-a/data/task4_v117_team_intake/city_indicators.csv'
EXPECTED_SHA256 = '555b38a4b586759de1fa278b0e751433a13dd541f375097db53b186cfcdc768a'
# Explicit alternate spellings only. No aliases were needed for these source labels.
CITY_NAMES = ('Vienna','Zurich','Helsinki','Berlin','London','Amsterdam','Stockholm','Paris',
              'Madrid','Milan','Dublin','Oslo','Prague','Warsaw','Singapore','Tokyo')
ALIASES: dict[str, list[str]] = {city: [] for city in CITY_NAMES}

def norm(s: str) -> str:
    # Exact normalized comparison; no substring, edit-distance, or fuzzy matching.
    decomposed = unicodedata.normalize('NFKD', s.strip()).casefold()
    return ' '.join(''.join(c for c in decomposed if not unicodedata.combining(c)).split())

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def display_name(rec: dict) -> str:
    names = rec.get('names', [])
    for wanted in ('ror_display', 'label'):
        for name in names:
            if wanted in name.get('types', []): return name.get('value', '')
    return ''

def main() -> None:
    digest = sha256(ROR)
    if digest != EXPECTED_SHA256: raise SystemExit(f'ROR archive SHA256 mismatch: {digest}')
    city_rows = list(csv.DictReader(CITY_CSV.open(encoding='utf-8-sig', newline='')))
    city_by_key = {}
    for c in city_rows:
        for n in [c['city'], *ALIASES[c['city']]]:
            key = (c['iso2'], norm(n))
            if key in city_by_key and city_by_key[key] != c['city']:
                raise ValueError(f'Non-unique city alias key: {key}')
            city_by_key[key] = c['city']
    rosters = {c['city']: {} for c in city_rows}
    first_csv = {c['city']: set() for c in city_rows}
    with zipfile.ZipFile(ROR) as z:
        json_name = next(n for n in z.namelist() if n.endswith('.json'))
        with z.open(json_name) as f: records = json.load(f)
        for rec in records:
            if rec.get('status') != 'active' or 'education' not in rec.get('types', []): continue
            rid = rec['id'].rstrip('/').split('/')[-1]
            matched = []
            for loc in rec.get('locations', []):
                details = loc.get('geonames_details', {})
                city = city_by_key.get((details.get('country_code', ''), norm(details.get('name', ''))))
                if city: matched.append(loc)
            for city in sorted({city_by_key[(loc['geonames_details']['country_code'], norm(loc['geonames_details']['name']))] for loc in matched}):
                city_locs = [loc for loc in matched if city_by_key[(loc['geonames_details']['country_code'], norm(loc['geonames_details']['name']))] == city]
                rosters[city][rid] = {'record': rec, 'matched_locations': city_locs}
        csv_name = next(n for n in z.namelist() if n.endswith('.csv'))
        with z.open(csv_name) as raw:
            reader = csv.DictReader(io.TextIOWrapper(raw, encoding='utf-8-sig', newline=''))
            for row in reader:
                if row['status'] != 'active' or 'education' not in {x.strip() for x in row['types'].split(';')}: continue
                country = row['locations.geonames_details.country_code']
                locname = row['locations.geonames_details.name']
                city = city_by_key.get((country, norm(locname)))
                if city: first_csv[city].add(row['id'].rstrip('/').split('/')[-1])
    fields = ['matched_city','matched_iso2','id','display_name','status','types','matched_locations_json','all_locations_json']
    with (OUT/'ror_education_rosters.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n'); w.writeheader()
        for city in CITY_NAMES:
            for rid,item in sorted(rosters[city].items()):
                rec=item['record']
                w.writerow({'matched_city':city,'matched_iso2':next(c['iso2'] for c in city_rows if c['city']==city),
                  'id':rec['id'],'display_name':display_name(rec),'status':rec['status'],
                  'types':'; '.join(rec.get('types',[])),
                  'matched_locations_json':json.dumps(item['matched_locations'],ensure_ascii=False,separators=(',',':')),
                  'all_locations_json':json.dumps(rec.get('locations',[]),ensure_ascii=False,separators=(',',':'))})
    comparisons=[]
    missing_ids={}
    for c in city_rows:
        city=c['city']; json_ids=set(rosters[city]); csv_ids=first_csv[city]
        missing_ids[city]=sorted(json_ids-csv_ids)
        comparisons.append({'city':city,'country':c['country'],'iso2':c['iso2'],
          'original_he_count':float(c['he_count']) if c['he_count'] else None,
          'json_any_location_unique_ror_id_count':len(json_ids),
          'csv_first_location_count':len(csv_ids),
          'json_minus_original_he_count':len(json_ids)-float(c['he_count']) if c['he_count'] else None,
          'json_minus_csv_first_location_count':len(json_ids)-len(csv_ids),
          'missing_from_csv_first_location_count':len(missing_ids[city]),
          'unmatched_reason':None if json_ids else 'No active education-tagged record matched exact normalized GeoNames city name and country code.'})
    srcsha=sha256(CITY_CSV)
    result={'sources':{'ror_archive':str(ROR.relative_to(ROOT)),'ror_archive_sha256':digest,
      'ror_json_member':json_name,'ror_json_record_count':len(records),'ror_csv_member':csv_name,
      'original_city_csv':str(CITY_CSV.relative_to(ROOT)),'original_city_csv_sha256':srcsha},
      'selection':{'status':'active','types_contains':'education','location_rule':'any JSON location with exact normalized GeoNames city name and matching country code',
      'normalization':'Unicode NFKD; remove combining marks; casefold; trim/collapse whitespace',
      'aliases':ALIASES,'fuzzy_matching':False,'per_city_unique_key':'ROR id'},
      'scope_note':'An education tag does not certify a university or local resource access. Counts do not establish municipal polygon coverage or the lineage of the original he_count extraction.',
      'cities':comparisons,'unique_ror_ids_across_all_city_rosters':len({rid for roster in rosters.values() for rid in roster}),
      'missing_from_csv_first_location_ids_by_city':missing_ids}
    (OUT/'city_comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {OUT / "ror_education_rosters.csv"}')
    print(f'Wrote {OUT / "city_comparison.json"}')
    print(f'ROR JSON records: {len(records)}; unique IDs across city rosters: {result["unique_ror_ids_across_all_city_rosters"]}')
    for c in comparisons: print(f"{c['city']}: JSON={c['json_any_location_unique_ror_id_count']} CSV-first-location={c['csv_first_location_count']} original_he_count={c['original_he_count']}")

if __name__ == '__main__': main()
