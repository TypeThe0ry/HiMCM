"""Milan municipal metro inventory: original responses to a conservative hub count."""
from pathlib import Path
import csv
import hashlib
import json
import math

P = Path(__file__).resolve().parent
ALIASES = {
    'SAN AMBROGIO': 'SANT_AMBROGIO', 'S.AMBROGIO': 'SANT_AMBROGIO',
    'LOTTO M5': 'LOTTO', 'LOTTO FIERAMILANOCITY': 'LOTTO',
    'LORETO M2': 'LORETO', 'LORETO M1': 'LORETO',
    'DUOMO M3': 'DUOMO', 'DUOMO M1': 'DUOMO',
    'CADORNA FN M2': 'CADORNA_FN', 'CADORNA FN M1': 'CADORNA_FN',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    retrieval = json.loads((P / 'retrieval.json').read_text())
    originals = {}
    for row in retrieval:
        assert row['status'] == 200, row
        assert sha(P / row['file']) == row['sha256'], row['file']
        originals[row['file']] = row['sha256']
    layers = json.loads((P / 'layers_original.json').read_text())['layers']
    layer = next(x for x in layers if x['id'] == 0)
    assert layer['name'] == 'Stazioni_Metro'
    assert '16/10/2024' in layer['description']
    assert next(x for x in layers if x['id'] == 3)['name'] == 'Accessi_Metro'
    geo = json.loads((P / 'stations_original.geojson').read_text())
    assert not geo.get('exceededTransferLimit', False)
    features = geo['features']
    native_ids = json.loads((P / 'ids_original.json').read_text())['objectIds']
    assert len(features) == len(native_ids) == 130
    assert {f['properties']['OBJECTID'] for f in features} == set(native_ids)
    retained, omitted = [], []
    for f in features:
        a = f['properties']
        lon, lat = f['geometry']['coordinates'][:2]
        row = dict(objectid=a['OBJECTID'], id_amat=a['id_amat'], name=a['nome'],
                   lines=a['linee'], municipality_code=a['cod_istat'], municipality=a['comune'],
                   municipio=a['id_municipio'], longitude=lon, latitude=lat,
                   hub=ALIASES.get(a['nome'], a['nome']))
        if a['cod_istat'] == '015146' and a['comune'] == 'Milano':
            assert a['id_municipio'] in range(1, 10)
            assert f['geometry']['type'] == 'Point' and 9 < lon < 9.4 and 45.3 < lat < 45.6
            retained.append(row)
        else:
            row['reason'] = 'No matching municipal code/name; omitted, not inferred to be inside or outside'
            omitted.append(row)
    assert len(retained) == 109 and len(omitted) == 21
    assert len({r['id_amat'] for r in retained}) == 109
    groups = {}
    for row in retained:
        groups.setdefault(row['hub'], []).append(row)
    duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
    assert len(groups) == 104 and set(duplicate_groups) == {'SANT_AMBROGIO', 'LOTTO', 'LORETO', 'DUOMO', 'CADORNA_FN'}
    for members in duplicate_groups.values():
        assert len(members) == 2
    # Proximity diagnoses aliases; names plus the operator's interchange map
    # justify these five consolidations. It is not a clustering rule.
    near = []
    for i, a in enumerate(retained):
        for b in retained[i + 1:]:
            d = 111200 * math.hypot((a['longitude'] - b['longitude']) * math.cos(math.radians(a['latitude'])), a['latitude'] - b['latitude'])
            if d < 280:
                near.append(dict(first=a['name'], second=b['name'], approximate_metres=d,
                                 consolidated=a['hub'] == b['hub']))
    assert sum(x['consolidated'] for x in near) == 5
    assert len(near) == 7  # Wagner/Buonarroti and Duomo/Cordusio stay distinct.
    for name, rows in [('retained_line_station_records.csv', retained), ('omitted_records.csv', omitted), ('near_pairs.csv', near)]:
        with (P / name).open('w', newline='') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    hubs = [dict(hub=k, names=' | '.join(r['name'] for r in v),
                 objectids='|'.join(str(r['objectid']) for r in v),
                 native_ids='|'.join(str(r['id_amat']) for r in v),
                 line_station_records=len(v)) for k, v in sorted(groups.items())]
    with (P / 'retained_hubs.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(hubs[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(hubs)
    result = dict(city='Milan', source_date='2024-10-16 stated in municipal layer metadata',
                  total_station_layer_records=130, municipal_line_station_records=109,
                  municipal_unique_station_hubs=104, omitted_geography_records=21,
                  consolidated_interchanges=list(sorted(duplicate_groups)),
                  operator_map='Original ATM schema_rete_metro.pdf, V26B label; publication date unreported; visually reviewed for five interchange pairs',
                  geography='Official municipal code 015146, comune Milano, and municipio 1–9; coordinate sanity check only, not independent boundary overlay',
                  count_scope='Historical metro station/hub subset; excludes access-layer entrances, bus/tram/rail inventories and unmatched geography; not a claim of present service or individual access',
                  historical_inventory_proxy=True, lower_bound_only=True,
                  map_visual_review=True, originals_sha256=originals,
                  derived_sha256={n: sha(P / n) for n in ['retained_line_station_records.csv', 'omitted_records.csv', 'near_pairs.csv', 'retained_hubs.csv']},
                  extractor_sha256=sha(Path(__file__)))
    (P / 'extraction.json').write_text(json.dumps(result, indent=2) + '\n')
    print('130 records; 109 municipal line records; 104 distinct station/hubs')


if __name__ == '__main__':
    main()
