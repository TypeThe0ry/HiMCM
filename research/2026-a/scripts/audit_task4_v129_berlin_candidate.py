"""Independently review the Berlin source candidate; never activate a model."""
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / 'data/task4_v129_transport'
OUT = ROOT / 'results/task4_v129_candidate_review'
sys.path.insert(0, str(ROOT / 'scripts'))
from task4_user_v127_revision import revised_bounds
from task4_v5_model import NAMES


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


class SourceHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.payload = []
        self.text = []
        self.canonical = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('id') == '__NEXT_DATA__':
            self.active = True
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'script':
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.payload.append(data)
        else:
            self.text.append(data)


def main():
    snapshot = ROOT / 'design/task4_user_v127_snapshot.json'
    frozen = json.loads(snapshot.read_text())['source_sha256']
    frozen = {**frozen, 'design/task4_user_v127_snapshot.json': sha(snapshot),
              'data/task4_v117_team_intake/city_indicators.csv':
              '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'}
    registry = ROOT / 'design/task4_user_current_model.json'
    registry_before = sha(registry)
    registry_original = subprocess.check_output(['git', '-C', str(ROOT.parents[1]), 'show',
        '59edddf:research/2026-a/design/task4_user_current_model.json'])
    assert hashlib.sha256(registry_original).hexdigest() == frozen['design/task4_user_current_model.json']
    def verify_frozen():
        assert sha(registry) == registry_before
        assert all(sha(ROOT / p) == expected for p, expected in frozen.items()
                   if p != 'design/task4_user_current_model.json')
    verify_frozen()
    source_hashes = {}
    stations = {}
    names = {}
    line_counts = []
    for line in range(1, 10):
        path = HERE / f'berlin_u{line}.html'
        source_hashes[path.name] = sha(path)
        parser = SourceHTML()
        parser.feed(path.read_text())
        assert parser.canonical == [f'https://www.bvg.de/de/verbindungen/linienuebersicht/u{line}']
        route = json.loads(''.join(parser.payload))['props']['pageProps']['pageJson']['main']['fgiPearlString']['initialRouteData']
        assert str(route['lineType']) == '2'
        selected = []
        for segment in route['routeSegments']:
            for stop in segment['stops']:
                assert segment['fareZone'] == stop['zone']
                if stop['zone'] != 'A':
                    continue
                slug, title = stop['slug'], stop['title']
                prefix = next(p for p in ['S+U ', 'U '] if title.startswith(p))
                name = title[len(prefix):].replace('\u200b', '')
                assert names.setdefault(name, slug) == slug
                station = stations.setdefault(slug, {'name': name, 'lines': set(), 'appearances': []})
                assert station['name'] == name
                station['lines'].add(f'U{line}')
                station['appearances'].append((f'U{line}', {t['name'] for t in stop.get('transfers', {}).get('subway', [])}))
                selected.append(slug)
        assert len(selected) == len(set(selected))
        line_counts.append(len(selected))
    assert line_counts == [13, 23, 16, 5, 13, 14, 22, 15, 10]
    assert sum(line_counts) == 131 and len(stations) == len(names) == 100
    for station in stations.values():
        for own, transfers in station['appearances']:
            assert station['lines'] - {own} <= transfers
    zone = HERE / 'berlin_zone_definition.html'
    parser = SourceHTML()
    parser.feed(zone.read_text())
    assert parser.canonical == ['https://www.bvg.de/de/abos-und-tickets/tarifzonen-und-tarifbestimmungen']
    zone_text = ' '.join(' '.join(parser.text).split())
    assert 'Berliner Innenstadt bis einschließlich S-Bahn Ring' in zone_text
    source_hashes[zone.name] = sha(zone)
    candidate = json.loads((HERE / 'observations.json').read_text())
    assert len(candidate) == 1 and candidate[0]['raw_count'] == 100
    archived = json.loads((HERE / 'berlin_stations.json').read_text())
    assert {r['station_slug'] for r in archived} == set(stations)
    assert len(archived) == 100
    for row in archived:
        assert row['station_name'] == stations[row['station_slug']]['name']
        assert set(row['subway_lines']) == stations[row['station_slug']]['lines']
    frame, lo, hi = revised_bounds()
    i, j = frame.city.tolist().index('Berlin'), NAMES.index('public_transport_density')
    assert [lo[i, j], hi[i, j]] == [0, 1]
    population = float(frame.iloc[i].population)
    assert population == candidate[0]['population'] == 3700577
    density = 100 * 100000 / population
    utility = density / (50 + density)
    np.testing.assert_allclose(candidate[0]['utility_after'], [utility, 1], atol=1e-15, rtol=0)
    previews = list(csv.DictReader((ROOT / 'results/task4_v129_priority/candidate_lower_only_previews.csv').open()))
    assert len(previews) == 2
    comparisons = []
    for row in previews:
        w = (np.array([.1125] * 6 + [.05, .1125, .1125, .05])
             if row['weight_reference'] == 'fixed' else np.ones(10) / 10)
        def scores(a):
            d0 = np.linalg.norm(a * np.sqrt(w), axis=1)
            d1 = np.linalg.norm((1-a) * np.sqrt(w), axis=1)
            return 100 * d0 / (d0+d1)
        lower = scores(lo)
        upper = scores(hi)
        a = lo.copy()
        a[i, j] = utility
        after = scores(a)
        np.testing.assert_array_equal(after[np.arange(16) != i], lower[np.arange(16) != i])
        regret = np.array([max(0., max(np.delete(upper, k))-after[k]) for k in range(16)])
        possible = [upper[k] >= max(np.delete(after, k)) for k in range(16)]
        np.testing.assert_allclose([after[i], np.mean(upper-after), regret[i], regret.min()],
            [float(row[k]) for k in ['focal_lower_after', 'global_mean_width_after',
                                     'focal_max_regret_after', 'minimax_regret_after']], atol=1e-12, rtol=0)
        assert sum(possible) == 16 and frame.iloc[int(np.argmin(regret))].city == 'Zurich'
        comparisons.append(dict(weight_reference=row['weight_reference'],
            candidate_mean_width=float(np.mean(upper-after)),
            candidate_mean_width_reduction=float(np.mean(after-lower)),
            candidate_relative_width_reduction_percent=float(100*np.mean(after-lower)/np.mean(upper-lower)),
            candidate_focal_score_lower=float(after[i]), possible_champions=16,
            conservative_choice='Zurich'))
    verify_frozen()
    OUT.mkdir(parents=True, exist_ok=True)
    report = dict(status='pass', source_review='qualified conditional public-metro inventory candidate',
        primary_admissions=0, registry_changed=False, station_complexes=100,
        line_appearances=131, geography='Publisher-defined Berlin inner-city zone A; no polygon overlay claimed',
        observed_year=2026, population_year=2025, population=population,
        utility_candidate=[utility, 1], canonical_urls_verified=10,
        source_hashes=source_hashes, candidate_files_sha256={p.name: sha(p) for p in
            [HERE / 'extract.py', HERE / 'manifest.json', HERE / 'observations.json', HERE / 'berlin_stations.json']},
        native_id_name_bijection=True, interchanges_reconciled=True,
        independent_HTMLParser_used=True, independent_preview_checks=comparisons,
        frozen_V127_sha256=frozen, live_registry_sha256_before_after=registry_before,
        live_registry_used_as_input=False,
        remaining_work='Controlled admission/withdrawal audit, primary and extension reruns, and unified manuscript migration before activation. This receipt does not change the V127 primary model.',
        limitations='Static as-accessed inventory; no all-station live-service, individual accessibility or universal teenage eligibility audit. Other modes and outer-city stations remain uncounted.')
    (OUT / 'audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['status', 'primary_admissions', 'station_complexes',
          'line_appearances', 'utility_candidate', 'independent_preview_checks']}, indent=2))


if __name__ == '__main__':
    main()
