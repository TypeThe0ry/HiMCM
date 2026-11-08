"""Extract a public metro subset from original operator and city OGD files.

Static register supply, not real-time departures or adolescent accessibility.
The source's DIVA groups stopping positions into station areas (schema p.4).
"""
import csv
import hashlib
import json
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from matplotlib.path import Path as PolygonPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT/'data/task4_v117_team_intake/city_indicators.csv'
INPUT_SHA = '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'


def rows(name, delimiter=';'):
    with (HERE/name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream, delimiter=delimiter))


def normalized(text):
    return ' '.join(unicodedata.normalize('NFC', text).casefold().split())


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == INPUT_SHA
    receipts = json.loads((HERE/'retrievals.json').read_text())
    for receipt in receipts:
        assert hashlib.sha256((HERE/receipt['file']).read_bytes()).hexdigest() == receipt['sha256']
    version = rows('version.csv')
    assert version == [{'DateValidFrom': '2026-11-08T17:50:01+01:00', 'VersionDate': '2026-11-08T17:50:01+01:00'}]
    stops, positions, lines, patterns = [rows(x) for x in ['stop_areas.csv', 'stop_positions.csv', 'lines.csv', 'route_patterns.csv']]
    areas = {r['DIVA']: r for r in stops}
    points = {r['StopID']: r for r in positions}
    routes = {r['LineID']: r for r in lines}
    assert len(areas) == len(stops) == 2008
    assert len(points) == len(positions) == 5125
    assert len(routes) == len(lines) == 205 and len(patterns) == 87774
    boundary = json.loads((HERE/'vienna_boundary.geojson').read_text())
    assert boundary['numberReturned'] == boundary['numberMatched'] == 1
    assert boundary['crs']['properties']['name'].endswith('EPSG::4326')
    feature = boundary['features'][0]
    assert feature['properties']['STATAUSTRIA_GEM_KENN'] == 90001
    assert feature['properties']['NAME_GEMG'] == 'STADT WIEN'
    assert feature['properties']['LU_DATE'] == '2026-09-01Z'
    assert feature['geometry']['type'] == 'Polygon'
    rings = [PolygonPath(np.asarray(r, float)) for r in feature['geometry']['coordinates']]

    references = defaultdict(lambda: dict(modes=set(), lines=set(), stop_ids=set(), pattern_records=0))
    rejected = Counter()
    for row in patterns:
        route, point = routes.get(row['LineID']), points.get(row['StopID'])
        if route is None or point is None:
            rejected['unmatched_line_or_stopping_position_pattern_rows'] += 1
            continue
        if route['MeansOfTransport'] not in {'ptMetro', 'ptTram', 'ptBusCity'}:
            rejected['other_mode_pattern_rows'] += 1
            continue
        area = areas.get(point['DIVA'])
        if area is None:
            rejected['unmatched_DIVA_pattern_rows'] += 1
            continue
        entry = references[point['DIVA']]
        entry['modes'].add(route['MeansOfTransport'])
        entry['lines'].add(route['LineText'])
        entry['stop_ids'].add(point['StopID'])
        entry['pattern_records'] += 1

    names, omissions = defaultdict(list), []
    for diva, evidence in sorted(references.items()):
        area = areas[diva]
        name = normalized(area['PlatformText'])
        try:
            point = tuple(float(area[x]) for x in ['Longitude', 'Latitude'])
        except (ValueError, TypeError):
            point = (0., 0.)
        inside = rings[0].contains_point(point) and not any(r.contains_point(point) for r in rings[1:])
        if area['Municipality'] != 'Wien' or not inside or not name:
            omissions.append(dict(DIVA=diva, source_name=area['PlatformText'], municipality=area['Municipality'],
                                  longitude=point[0], latitude=point[1], inside_city_polygon=bool(inside)))
            continue
        names[name].append((diva, area, evidence))
    broad_count = len(names)
    assert len(references) == 1722 and sum(map(len, names.values())) == 1703
    assert broad_count == 1695 and len(omissions) == 19
    # Pattern files also contain depot/non-passenger movements. Their entire
    # all-mode register is not an admissible public-stop inventory. Qualify the
    # metro subset against a second, explicitly existing city station layer.
    all_mode_names = names
    names = {key: group for key, group in names.items()
             if any('ptMetro' in x[2]['modes'] for x in group)}
    assert len(names) == 99
    city_stations = json.loads((HERE/'review_source_ubahn_stations_original.geojson').read_text())
    assert city_stations['numberReturned'] == city_stations['numberMatched'] == 99
    assert city_stations['crs']['properties']['name'].endswith('EPSG::4326')
    aliases = {'bhf. heiligenstadt': 'heiligenstadt', 'bhf. hütteldorf': 'hütteldorf',
               'bhf. meidling': 'bahnhof meidling', 'hauptbahnhof': 'südtiroler platz - hauptbahnhof',
               'kaisermühlen, vic': 'kaisermühlen-vic', 'messe-prater': 'messe prater',
               'mitte-landstrasse': 'landstrasse', 'ober st. veit': 'ober sankt veit',
               'unter st. veit': 'unter sankt veit'}
    municipal = {normalized(f['properties']['HTXT']): f for f in city_stations['features']}
    assert len(municipal) == 99
    assert {aliases.get(key, key) for key in names} == set(municipal)
    distances = []
    for key, group in names.items():
        feature = municipal[aliases.get(key, key)]
        assert feature['geometry']['type'] == 'Point'
        point = np.array(feature['geometry']['coordinates'], float)
        assert rings[0].contains_point(point) and not any(r.contains_point(point) for r in rings[1:])
        registered = np.array([float(group[0][1]['Longitude']), float(group[0][1]['Latitude'])])
        # An independent location check for each explicit spelling alias, not
        # an automated fuzzy match or an assumed station operating status.
        distance = np.linalg.norm((registered-point)*np.array([111320*np.cos(np.deg2rad(point[1])), 111320]))
        assert distance < 500, (key, distance)
        distances.append(float(distance))
    count = len(names)
    records = []
    for key, members in sorted(names.items()):
        records.append(dict(normalized_name=key, display_name=members[0][1]['PlatformText'].strip(),
                            DIVA_ids=';'.join(x[0] for x in members),
                            source_area_count=len(members),
                            modes=';'.join(sorted(set().union(*(x[2]['modes'] for x in members)))),
                            lines=';'.join(sorted(set().union(*(x[2]['lines'] for x in members)))),
                            stopping_position_count=len(set().union(*(x[2]['stop_ids'] for x in members))),
                            longitude=members[0][1]['Longitude'], latitude=members[0][1]['Latitude'],
                            municipal_station_name=municipal[aliases.get(key,key)]['properties']['HTXT'],
                            municipal_feature_id=municipal[aliases.get(key,key)]['id']))
    for filename, data in [('vienna_stop_area_subset.csv', records), ('omitted_areas.csv', omissions)]:
        with (HERE/filename).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0])); writer.writeheader(); writer.writerows(data)

    with SOURCE.open(encoding='utf-8-sig', newline='') as stream:
        source = next(r for r in csv.DictReader(stream) if r['city'] == 'Vienna')
    population = int(source['population']); assert population == 2028399 and source['population_year'] == '2025'
    assert source['transit_share_pct'] == ''
    density = 100000*count/population; lower = density/(50+density)
    observation = dict(city='Vienna', indicator='public_transport_density', raw_count=count,
        population=population, population_year=2025, sourceyear=2026,
        population_source='Unchanged original team CSV; not externally rechecked',
        access_date='2026-11-09', record_date=version[0]['VersionDate'],
        utility_before=[0, 1], utility_after=[lower, 1], utility_anchor=50,
        density_per_100000_lower=density, lower_bound_only=True,
        candidate_only=True, admissible='conditional_inventory_lower_bound', historical_inventory_proxy=False,
        source_url='https://www.wienerlinien.at/ogd_realtime/doku/',
        scope='99 unique metro DIVA station areas in the2026 versioned operator register. Join metro route patterns through stopping positions, require municipality label Wien and points inside official Vienna polygon, and cross-match all99 with the separate official existing U-Bahn station layer. Nine explicit spelling aliases also pass coordinate checks. The broad1695-name all-mode register is rejected because it contains depot/non-passenger movements. Other public transport facilities remain uncounted.',
        limitations='Current versioned static inventory with unchanged2025 population. DIVA is a provider station-area grouping, not a platform count. Pattern membership does not prove a departure on access day, service frequency, universal teenage eligibility or household access. Geometry uses source representative coordinates; uncertain/omitted areas are uncounted. This is not a2025 same-year, complete all-provider or real-time operation census; upper utility remains1.',
        source_files=[r['file'] for r in receipts if not r['file'].startswith('rejected_')])
    (HERE/'observations.json').write_text(json.dumps([observation], ensure_ascii=False, indent=2)+'\n')
    audit = dict(status='pass', version_date=version[0], source_area_rows=len(stops),
        source_stopping_positions=len(positions), source_pattern_rows=len(patterns),
        referenced_regular_mode_DIVA_areas=len(references), eligible_city_DIVA_areas=1703,
        rejected_unqualified_all_mode_name_count=broad_count, same_name_pairs_in_broad_diagnosis=8, omitted_broad_areas=19,
        public_metro_station_areas=count, existing_municipal_layer_cross_matches=99,
        maximum_source_representative_point_distance_metres=max(distances), explicit_aliases=aliases,
        rejected_pattern_rows=dict(rejected), original_user_csv_sha256=INPUT_SHA,
        lower_utility=lower, upper_utility=1, original_csv_unchanged=True,
        boundary_source_date='2026-09-01', provider_municipality_code_not_assumed_equal_to_official_city_code=True)
    (HERE/'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
