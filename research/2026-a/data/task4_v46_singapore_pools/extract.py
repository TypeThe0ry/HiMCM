"""Audit the downloaded 2024 census snapshot without inventing public access."""
from pathlib import Path
import csv
import hashlib
import json

P = Path(__file__).resolve().parent

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        b=(P/r['file']).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    with (P/'sport_facilities.csv').open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f))
    pools=[r for r in rows if r['SportsFacility']=='Swimming Pool']
    assert len(rows)==16595 and len(pools)==3533
    columns=list(rows[0])
    with (P/'pool_rows.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,columns);w.writeheader();w.writerows(pools)
    result=dict(source_dataset='d_2cfb0867cdeb2b7303068995699dc33b',
        census_year=2024,snapshot_acquired='2026-11-07',
        total_rows=len(rows),swimming_pool_rows=len(pools),
        distinct_complete_pool_rows=len({tuple(r[k] for k in columns) for r in pools}),
        distinct_name_postcode_pairs=len({(r['VenueName'],r['PostalCode']) for r in pools}),
        distinct_coordinate_pairs=len({(r['Latitude'],r['Longitude']) for r in pools}),
        public_access_field_present=False,operating_status_field_present=False,
        licensed_facility_register=False,main_admitted=False,
        current_citywide_public_venue_upper_bound=None,
        conditional_enumerated_frame_upper_bound=len(pools),
        upper_bound_condition='Only within the enumerated census frame, assuming every target venue contributes at least one swimming-pool row; not a certified 2026 citywide upper bound.',
        duplicate_warning='Pool units and multiple rows per venue are not independent public venue counts; rounded coordinates must not automatically merge physical venues.')
    (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
