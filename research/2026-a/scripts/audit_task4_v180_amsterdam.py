"""Audit Amsterdam's candidate inventory and preview; leave current models frozen."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
from html import unescape
from matplotlib.path import Path as PolygonPath
import csv
import hashlib
import importlib
import json
import math
import os
import re
import subprocess
import sys
from urllib.parse import parse_qs, urlparse
import numpy as np

sys.dont_write_bytecode = True
R = Path(__file__).resolve().parents[1]
D = R / 'data/task4_v180_amsterdam'
O = R / 'results/task4_v180_amsterdam_candidate'
P = R.parents[2] / 'HiMCM-Overleaf'


def read(path):
    return json.loads(path.read_text())


def rows(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible(path):
    raw = re.sub(r'<(script|style)\b[^>]*>.*?</\1\s*>', '', path.read_text(), flags=re.I | re.S)
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', raw)).split())


def polygons(document):
    geometry = document['features'][0]['geometry']
    assert geometry['type'] in ['MultiPolygon', 'Polygon']
    values = geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]
    result = [[np.asarray(ring, dtype=float) for ring in polygon] for polygon in values]
    for polygon in result:
        for ring in polygon:
            assert ring.shape[1] == 2 and len(ring) >= 4 and np.array_equal(ring[0], ring[-1])
            assert np.isfinite(ring).all() and np.all((ring[:, 0] > 3) & (ring[:, 0] < 6))
            assert np.all((ring[:, 1] > 51) & (ring[:, 1] < 54))
    return result


def membership(points, values):
    inside = np.zeros(len(points), dtype=bool)
    for polygon in values:
        keep = PolygonPath(polygon[0]).contains_points(points)
        for hole in polygon[1:]:
            keep &= ~PolygonPath(hole).contains_points(points)
        inside |= keep
    return inside


def project(points):
    process = subprocess.run(['cs2cs', '-f', '%.6f', 'OGC:CRS84', 'EPSG:28992'],
                             input=''.join(f'{x:.17g} {y:.17g}\n' for x, y in points),
                             text=True, capture_output=True, check=True,
                             env={**os.environ, 'PROJ_NETWORK': 'OFF'})
    result = np.asarray([[float(value) for value in line.split()[:2]] for line in process.stdout.splitlines()])
    assert result.shape == points.shape and np.isfinite(result).all()
    assert np.all((result[:, 0] > 100000) & (result[:, 0] < 150000))
    assert np.all((result[:, 1] > 460000) & (result[:, 1] < 510000))
    return result


def projected_polygons(values):
    flat = np.concatenate([ring for polygon in values for ring in polygon])
    projected = project(flat)
    position, result = 0, []
    for polygon in values:
        current = []
        for ring in polygon:
            current.append(projected[position:position + len(ring)])
            position += len(ring)
        result.append(current)
    assert position == len(projected)
    return result


def segment_distances(points, values):
    # Independent vectorized projection onto every exterior/hole segment.
    starts = np.concatenate([ring[:-1] for polygon in values for ring in polygon])
    ends = np.concatenate([ring[1:] for polygon in values for ring in polygon])
    vectors = ends - starts
    lengths = np.einsum('ij,ij->i', vectors, vectors)
    answer = []
    for point in points:
        delta = point - starts
        t = np.divide(np.einsum('ij,ij->i', delta, vectors), lengths,
                      out=np.zeros_like(lengths), where=lengths != 0)
        residual = delta - np.clip(t, 0, 1)[:, None] * vectors
        answer.append(float(np.sqrt(np.einsum('ij,ij->i', residual, residual)).min()))
    return np.asarray(answer)


def norm_score(utility, weights):
    positive = math.sqrt(math.fsum(w * x * x for w, x in zip(weights, utility)))
    negative = math.sqrt(math.fsum(w * (1 - x) * (1 - x) for w, x in zip(weights, utility)))
    return 100 * positive / (positive + negative)


def independent_scores(lower, upper, weights):
    low = [norm_score(row, weights) for row in lower]
    high = [norm_score(row, weights) for row in upper]
    midpoint = [norm_score((a + b) / 2, weights) for a, b in zip(lower, upper)]
    regret = [max(0, max(high[j] for j in range(16) if j != i) - low[i]) for i in range(16)]
    result = []
    for i in range(16):
        others = [j for j in range(16) if j != i]
        result.append(dict(score_lower=low[i], score_upper=high[i], max_regret=regret[i],
                           midpoint_illustrative_score=midpoint[i],
                           best_rank=1 + sum(low[j] > high[i] + 1e-12 for j in others),
                           worst_rank=1 + sum(high[j] > low[i] + 1e-12 for j in others),
                           decision_rank=1 + sum(value < regret[i] - 1e-12 for value in regret),
                           midpoint_illustrative_rank=1 + sum(value > midpoint[i] + 1e-12 for value in midpoint),
                           possible_champion=high[i] >= max(low[j] for j in others) - 1e-12,
                           necessary_champion=low[i] >= max(high[j] for j in others) - 1e-12))
    return result


def check_score_row(saved, expected):
    for key, value in expected.items():
        if isinstance(value, bool):
            assert saved[key] == str(value), key
        elif isinstance(value, int):
            assert float(saved[key]) == value, key
        else:
            assert abs(float(saved[key]) - value) <= 1e-11, key


def main():
    summary = read(O / 'summary.json')
    extraction = read(D / 'extraction.json')
    protected = read(O / 'protected_files.json')
    receipts = read(D / 'retrievals.json')
    assert len(receipts) == len({row['file'] for row in receipts}) == 9
    for record in receipts:
        path = D / record['file']
        assert record['http_status'] == 200 and path.stat().st_size == record['bytes']
        assert sha(path) == record['sha256']
        assert record['url'] == record['final_url']
        assert urlparse(record['url']).hostname in ['maps.amsterdam.nl', 'service.pdok.nl']
    for filename, expected in summary['source_sha256'].items():
        assert sha(R / filename) == expected, filename
    assert len(summary['source_sha256']) == 15
    requests = {record['file']: record for record in receipts}
    assert requests['stops_metadata_original.json']['body'] == {'ID': 649}
    assert requests['city_metadata_original.json']['body'] == {'ID': 541}
    query = parse_qs(urlparse(requests['cbs_boundary2025_original.geojson']['url']).query)
    assert query['srsName'] == ['EPSG:4326']
    assert query['typeNames'] == ['gebiedsindelingen:gemeente_niet_gegeneraliseerd']
    assert 'GM0363' in query['filter'][0]

    metadata, data = read(D / 'stops_metadata_original.json'), read(D / 'stops2026_original.geojson')
    assert metadata[0] == data['name'] == 'TRAMMETRO_PUNTEN_2026'
    assert metadata[3] == len(data['features']) == 239 and metadata[4] == 2026
    assert 'samengevoegd tot 1 opstappunt' in metadata[6]
    assert len({feature['id'] for feature in data['features']}) == 239
    assert Counter(feature['properties']['Modaliteit'] for feature in data['features']) == {'Tram': 200, 'Metro': 39}
    metros = [feature for feature in data['features'] if feature['properties']['Modaliteit'] == 'Metro']
    assert all(feature['geometry']['type'] == 'Point' for feature in data['features'])
    points = np.asarray([feature['geometry']['coordinates'] for feature in metros])
    assert points.shape == (39, 2)
    assert len({tuple(point) for point in points}) == len({feature['properties']['Naam'].casefold().strip() for feature in metros}) == 39
    local, national = read(D / 'city2026_original.geojson'), read(D / 'cbs_boundary2025_original.geojson')
    assert len(local['features']) == len(national['features']) == national['numberMatched'] == 1
    assert local['features'][0]['properties']['Gemeente'] == 'Amsterdam'
    assert national['features'][0]['properties']['statcode'] == 'GM0363'
    assert national['features'][0]['properties']['jrstatcode'] == '2025GM0363'
    assert read(D / 'city_metadata_original.json')[4] == 'Maart 2026'
    geography = [polygons(document) for document in [local, national]]
    inside = [membership(points, values) for values in geography]
    rd_points = project(points)
    rd_geography = [projected_polygons(values) for values in geography]
    distances = [segment_distances(rd_points, values) for values in rd_geography]
    for mask, values in zip(inside, rd_geography):
        np.testing.assert_array_equal(mask, membership(rd_points, values))
    assert np.array_equal(inside[0], inside[1]) and sum(inside[0]) == 35
    screen = inside[0] & inside[1] & (distances[0] >= 100) & (distances[1] >= 100)
    assert sum(screen) == 32
    outside = [feature['id'] for feature, keep in zip(metros, inside[0]) if not keep]
    near = [feature['id'] for feature, nominal, keep in zip(metros, inside[0], screen) if nominal and not keep]
    retained = [feature['id'] for feature, keep in zip(metros, screen) if keep]
    assert outside == extraction['outside_ids'] == [178, 191, 192, 213]
    assert near == extraction['near_boundary_omission_ids'] == [164, 174, 196]
    assert retained == extraction['retained_ids'] and len(retained) == 32
    saved_groups = rows(D / 'mapped_metro_groups.csv')
    assert len(saved_groups) == 39
    largest_distance_error = 0.0
    for index, (feature, saved) in enumerate(zip(metros, saved_groups)):
        assert int(saved['provider_id']) == feature['id']
        assert saved['station_name'] == feature['properties']['Naam']
        assert saved['lines'] == feature['properties']['Lijn']
        assert [float(saved['longitude']), float(saved['latitude'])] == feature['geometry']['coordinates']
        assert saved['municipal2026_inside'] == str(bool(inside[0][index]))
        assert saved['cbs2025_inside'] == str(bool(inside[1][index]))
        assert saved['retained_candidate'] == str(bool(screen[index]))
        reason = '' if screen[index] else ('outside_both_nominal_boundaries' if not inside[0][index] else 'within_declared_100m_nominal_boundary_screen')
        assert saved['exclusion_reason'] == reason
        for field, values in zip(['municipal_boundary_distance_m', 'cbs_boundary_distance_m'], distances):
            error = abs(float(saved[field]) - values[index])
            assert error <= 1e-5
            largest_distance_error = max(largest_distance_error, error)

    map_text = visible(D / 'trammetro_original.html')
    assert 'samengevoegd tot 1 opstappunt' in map_text and 'NIET de actuele routes' in map_text
    assert 'Tijdelijke omleidingen zijn niet opgenomen' in map_text
    terms = visible(D / 'maps_terms_original.html')
    assert 'voor elk wettig doel' in terms and 'bronvermelding niet verplicht' in terms
    assert 'de originele dataset voor iedereen gratis beschikbaar is bij de Gemeente' in terms
    assert 'die ook op de doorgeleverde dataset van toepassing zijn' in terms
    assert 'https://creativecommons.org/licenses/by/4.0/deed.nl' in (D / 'pdok_capabilities_original.xml').read_text()
    notice = (D / 'README.md').read_text()
    for phrase in ['original datasets are freely available', 'terms', 'also apply to redistributed',
                   'rather than legally mandatory', 'not endorsed', 'CC BY4.0', '不是CC BY',
                   '不是提供方定位误差界', '不能改标2025观测']:
        assert phrase in notice
    for saved in saved_groups:
        if int(saved['provider_id']) in near:
            assert f"| {saved['provider_id']} | {saved['station_name']} | {float(saved['municipal_boundary_distance_m']):.2f} | {float(saved['cbs_boundary_distance_m']):.2f} |" in notice
    assert extraction['dataset_year'] == 2026 and extraction['exact_inventory_date'] == 'unreported'
    assert extraction['primary_admissions'] == 0 and extraction['declared_boundary_screen_metres'] == 100
    assert 'not a provider positional-error bound' in extraction['screen_interpretation']

    model = read(R / 'design/task4_user_current_model.json')
    assert model['version'] == 'V154' and model['primary_dataset'] == 'user-provided16-city CSV'
    sys.path.insert(0, str(R / 'scripts'))
    factory = getattr(importlib.import_module(model['module']), model['factory'])
    frame, baseline_lower, upper = factory()
    baseline_copy, upper_copy = baseline_lower.copy(), upper.copy()
    from task4_v5_model import NAMES
    assert baseline_lower.shape == upper.shape == (16, 10)
    cities = frame.city.tolist()
    city_index, indicator_index = cities.index('Amsterdam'), NAMES.index('public_transport_density')
    assert indicator_index == 6 and model['fixed_auxiliary_weight_total'] == .1
    assert int(frame.iloc[city_index].population) == 941927 and int(frame.iloc[city_index].population_year) == 2025
    assert baseline_lower[city_index, indicator_index] == 0 and upper[city_index, indicator_index] == 1
    frozen = {(r['city'], r['indicator']): r for r in rows(R / model['results'] / 'utility_bounds.csv') if r['scenario'] == 'after_conditional'}
    assert len(frozen) == 160
    for i, city in enumerate(cities):
        for j, indicator in enumerate(NAMES):
            record = frozen[city, indicator]
            assert abs(float(record['lower']) - baseline_lower[i, j]) <= 2e-15
            assert abs(float(record['upper']) - upper[i, j]) <= 2e-15
    previews = rows(O / 'preview_ranks.csv')
    indexed = {(r['scenario'], r['weight_reference'], r['city']): r for r in previews}
    bounds = {r['scenario']: r for r in rows(O / 'candidate_bounds.csv')}
    old_ranks = {(r['weight_reference'], r['city']): r for r in rows(R / model['results'] / 'current_ranks.csv') if r['scenario'] == 'after_conditional'}
    assert len(previews) == len(indexed) == 96 and len(bounds) == 3
    settings = {(r['scenario'], r['weight_reference']): r for r in summary['scenarios']}
    assert len(settings) == 6
    utility_fractions, width_changes = {}, {}
    for scenario, count in [('V154_baseline', 0), ('candidate_screened32', 32), ('nominal35_diagnostic', 35)]:
        exact = Fraction(count * 100000, 50 * 941927 + count * 100000)
        utility_fractions[scenario] = str(exact)
        saved = bounds[scenario]
        assert saved['city'] == 'Amsterdam' and saved['indicator'] == 'public_transport_density'
        assert saved['count'] == ('not_observed' if scenario == 'V154_baseline' else str(count))
        if scenario == 'V154_baseline':
            assert 'not observed zero' in saved['count_interpretation']
        assert (saved['population'], saved['population_year'], saved['inventory_metadata_year']) == ('941927', '2025', '2026')
        assert abs(float(saved['lower']) - float(exact)) <= 2e-16 and float(saved['upper']) == 1
        assert saved['primary_admitted'] == 'False'
        lower = baseline_lower.copy()
        lower[city_index, indicator_index] = float(exact)
        mask = np.ones((16, 10), dtype=bool)
        mask[city_index, indicator_index] = False
        assert np.array_equal(lower[mask], baseline_copy[mask]) and np.array_equal(upper, upper_copy)
        for reference, weights in [('fixed', [.05 if j in [6, 9] else .1125 for j in range(10)]), ('equal', [.1] * 10)]:
            expected = independent_scores(lower, upper, weights)
            for city, result in zip(cities, expected):
                check_score_row(indexed[scenario, reference, city], result)
                if scenario == 'V154_baseline':
                    check_score_row(old_ranks[reference, city], result)
            setting = settings[scenario, reference]
            width = math.fsum(r['score_upper'] - r['score_lower'] for r in expected) / 16
            assert abs(setting['mean_score_interval_width'] - width) <= 1e-11
            assert setting['conservative_recommendation'] == [cities[i] for i, r in enumerate(expected) if r['decision_rank'] == 1] == ['Zurich']
            assert setting['possible_champions'] == sum(r['possible_champion'] for r in expected) == 16
            assert setting['necessary_champions'] == sum(r['necessary_champion'] for r in expected) == 0
            if scenario == 'candidate_screened32':
                width_changes[reference] = settings['V154_baseline', reference]['mean_score_interval_width'] - width
    np.testing.assert_array_equal(baseline_lower, baseline_copy)
    np.testing.assert_array_equal(upper, upper_copy)
    np.testing.assert_array_equal(factory()[1], baseline_copy)
    np.testing.assert_array_equal(factory()[2], upper_copy)
    assert summary['primary_admissions'] == 0 and summary['MC_rerun'] is False
    assert summary['candidate_count'] == 32 and summary['nominal_inside_count'] == 35
    assert summary['current_primary'] == 'V154 unchanged' and summary['current_paper'] == 'V179 unchanged'
    assert 'not a backdated2025 count or measured positional-error guarantee' in summary['utility_scope']

    snapshot = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    assert protected['science'] == snapshot and len(snapshot) == 187
    assert len(protected['paper']) == 639 and len(protected['registries']) == 3
    for root, mapping in [(R, snapshot), (P, protected['paper']), (R / 'design', protected['registries'])]:
        for name, expected in mapping.items():
            assert sha(root / name) == expected, name
    for name, field, version in [('task4_user_current_model.json', 'version', 'V154'),
                                  ('task4_user_current_extensions.json', 'extension_version', 'V154'),
                                  ('task4_user_current_review.json', 'version', 'V179')]:
        path = R / 'design' / name
        assert read(path)[field] == version
        assert path.read_bytes() == subprocess.check_output(['git', '-C', str(R.parents[1]), 'show', 'HEAD:research/2026-a/design/' + name])
    review = read(R / 'design/task4_user_current_review.json')
    assert read(P / 'drafts/task4_current_review.json') == review and sha(P / review['pdf']) == review['pdf_sha256']
    version = subprocess.run(['proj'], input='', text=True, capture_output=True).stderr.splitlines()[0]
    assert version == extraction['projection_version']
    report = dict(version='V180 candidate only', status='pass', archived_original_responses_checked=9,
                  source_hash_bindings_checked=15, native_objects=239, native_modalities={'Tram': 200, 'Metro': 39},
                  unique_metro_ids_names_coordinates=39, nominal_points_in_both_boundaries=35,
                  independently_retained_candidate_groups=32, outside_ids=outside, nominal_boundary_omission_ids=near,
                  independent_geometry='Matplotlib polygon/hole membership in both longitude-latitude and projected coordinates',
                  independent_boundary_distances='Vectorized NumPy segment minima after the same declared offline PROJ transform',
                  largest_distance_arithmetic_difference_metres=largest_distance_error,
                  distance_comparison_tolerance_metres=1e-5, projection_version=version, PROJ_NETWORK='OFF',
                  screen_metres=100, screen_is_analyst_selection_not_provider_accuracy_bound=True,
                  exact_inventory_date_unreported=True, inventory_metadata_year=2026, retained_population_year=2025,
                  source_unit='Mapped Metro-designated boarding/station groups; no platform, operational-service, student-access or 2025 count claim',
                  municipal_terms_and_redistribution_notice_checked=True, municipal_attribution_mandatory_under_terms=False,
                  pdok_boundary_CC_BY_4=True, preview_city_weight_scenario_rows_checked=96,
                  independent_preview='Scalar fsum weighted norms, self-excluded regret, rank bounds/flags and midpoint diagnostics',
                  baseline_utility_cells_checked=160, exact_utility_fractions=utility_fractions,
                  candidate_mean_width_reduction=width_changes, other159_cells_and_all160_uppers_preserved=True,
                  primary_admissions=0, active_primary='V154 unchanged', active_paper='V179 unchanged',
                  full_extension_migration_executed=False, MC_rerun=False, manuscript_changed=False,
                  scientific_files_unchanged=187, existing_paper_files_unchanged=639, registries_unchanged=3,
                  canonical_pdf_sha256=review['pdf_sha256'], auditor_sha256=sha(Path(__file__)),
                  audited_output_sha256={str(path.relative_to(R)): sha(path) for path in
                                         [D / 'extraction.json', D / 'mapped_metro_groups.csv', O / 'summary.json',
                                          O / 'candidate_bounds.csv', O / 'preview_ranks.csv', O / 'protected_files.json']})
    (O / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
