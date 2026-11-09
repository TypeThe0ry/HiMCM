"""Extract a conservative mapped-metro subset; no city model is modified."""
from pathlib import Path
import csv
import hashlib
import json
import math
import os
import subprocess

D = Path(__file__).resolve().parent
SCREEN_METRES = 100


def read(name):
    return json.loads((D / name).read_text())


def rings(geometry):
    assert geometry['type'] in {'Polygon', 'MultiPolygon'}
    return [geometry['coordinates']] if geometry['type'] == 'Polygon' else geometry['coordinates']


def in_ring(point, ring):
    assert ring[0] == ring[-1]
    x, y = point
    inside = False
    for (a, b), (c, d) in zip(ring, ring[1:]):
        if (b > y) != (d > y) and x < a + (c-a)*(y-b)/(d-b):
            inside = not inside
    return inside


def contains(point, polygons):
    return any(in_ring(point, polygon[0]) and not any(in_ring(point, hole) for hole in polygon[1:]) for polygon in polygons)


def project(points):
    command = ['cs2cs', '-f', '%.6f', 'OGC:CRS84', 'EPSG:28992']
    payload = ''.join(f'{x:.17g} {y:.17g}\n' for x, y in points)
    process = subprocess.run(command, input=payload, text=True, capture_output=True, check=True,
                             env={**os.environ, 'PROJ_NETWORK': 'OFF'})
    result = [tuple(map(float, line.split()[:2])) for line in process.stdout.splitlines()]
    assert len(result) == len(points) and all(100000 < x < 150000 and 460000 < y < 510000 for x, y in result)
    return result


def project_polygons(polygons):
    sizes = [[len(ring) for ring in polygon] for polygon in polygons]
    values = iter(project([point for polygon in polygons for ring in polygon for point in ring]))
    return [[[next(values) for _ in range(size)] for size in polygon] for polygon in sizes]


def boundary_distance(point, polygons):
    x, y = point
    minimum = math.inf
    for polygon in polygons:
        for ring in polygon:
            for (a, b), (c, d) in zip(ring, ring[1:]):
                dx, dy = c-a, d-b
                length = dx*dx + dy*dy
                t = max(0, min(1, ((x-a)*dx+(y-b)*dy)/length)) if length else 0
                minimum = min(minimum, math.hypot(x-a-t*dx, y-b-t*dy))
    return minimum


def main():
    receipts = read('retrievals.json')
    assert len(receipts) == len({r['file'] for r in receipts}) == 9
    for receipt in receipts:
        raw = (D / receipt['file']).read_bytes()
        assert receipt['http_status'] == 200 and len(raw) == receipt['bytes']
        assert hashlib.sha256(raw).hexdigest() == receipt['sha256']
    metadata = read('stops_metadata_original.json')
    data = read('stops2026_original.geojson')
    assert metadata[0] == data['name'] == 'TRAMMETRO_PUNTEN_2026'
    assert metadata[3] == len(data['features']) == 239 and metadata[4] == 2026
    assert 'samengevoegd tot 1 opstappunt' in metadata[6]
    assert len({f['id'] for f in data['features']}) == 239
    assert all(f['geometry']['type'] == 'Point' for f in data['features'])
    metros = [f for f in data['features'] if f['properties']['Modaliteit'] == 'Metro']
    assert len(metros) == len({f['properties']['Naam'].casefold() for f in metros}) == len({tuple(f['geometry']['coordinates']) for f in metros}) == 39
    local, national = read('city2026_original.geojson'), read('cbs_boundary2025_original.geojson')
    assert len(local['features']) == len(national['features']) == national['numberMatched'] == 1
    assert local['features'][0]['properties']['Gemeente'] == 'Amsterdam'
    assert national['features'][0]['properties']['statcode'] == 'GM0363'
    assert national['features'][0]['properties']['jrstatcode'] == '2025GM0363'
    assert read('city_metadata_original.json')[4] == 'Maart 2026'
    polygons = [rings(x['features'][0]['geometry']) for x in [local, national]]
    rd_polygons = [project_polygons(p) for p in polygons]
    points = [f['geometry']['coordinates'] for f in metros]
    rd_points = project(points)
    records = []
    for feature, point, rd_point in zip(metros, points, rd_points):
        inside = [contains(point, p) for p in polygons]
        distances = [boundary_distance(rd_point, p) for p in rd_polygons]
        retained = all(inside) and min(distances) >= SCREEN_METRES
        records.append(dict(provider_id=feature['id'], station_name=feature['properties']['Naam'],
                            lines=feature['properties']['Lijn'], longitude=point[0], latitude=point[1],
                            municipal2026_inside=inside[0], cbs2025_inside=inside[1],
                            municipal_boundary_distance_m=distances[0], cbs_boundary_distance_m=distances[1],
                            retained_candidate=retained,
                            exclusion_reason='' if retained else ('outside_both_nominal_boundaries' if not any(inside) else 'within_declared_100m_nominal_boundary_screen')))
    assert sum(r['municipal2026_inside'] for r in records) == sum(r['cbs2025_inside'] for r in records) == 35
    assert sum(r['retained_candidate'] for r in records) == 32
    with (D / 'mapped_metro_groups.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(records)
    version = subprocess.run(['proj'], input='', text=True, capture_output=True).stderr.splitlines()[0]
    result = dict(version='V180 candidate only', dataset_year=2026, exact_inventory_date='unreported',
                  published_objects=239, metro_groups=39, nominal_inside_both_boundaries=35,
                  declared_boundary_screen_metres=SCREEN_METRES, retained_candidate_count=32,
                  outside_ids=[r['provider_id'] for r in records if r['exclusion_reason']=='outside_both_nominal_boundaries'],
                  near_boundary_omission_ids=[r['provider_id'] for r in records if r['exclusion_reason']=='within_declared_100m_nominal_boundary_screen'],
                  retained_ids=[r['provider_id'] for r in records if r['retained_candidate']],
                  coordinate_transform='cs2cs -f %.6f OGC:CRS84 EPSG:28992;PROJ_NETWORK=OFF',
                  projection_version=version,
                  screen_interpretation='Analyst conservative selection of mapped representative points;not a provider positional-error bound or guarantee all entrances/platforms are within the municipality',
                  inventory_interpretation='Mapped Metro boarding/station groups already merge nearby halts;not current operational routes,2025 observation,individual access or complete transport coverage',
                  primary_admissions=0)
    (D / 'extraction.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    main()
