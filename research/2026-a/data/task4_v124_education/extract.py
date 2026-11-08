"""Offline rejection/provenance audit; there are no admitted observations."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = ROOT / 'data/task4_v117_team_intake/city_indicators.csv'
EXPECTED_INPUT = '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'


def main():
    original_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert original_hash == EXPECTED_INPUT
    manifest = json.loads((HERE / 'sources.json').read_text())
    assert manifest['access_date'] == '2026-11-09'
    for row in manifest['sources']:
        assert hashlib.sha256((HERE / row['file']).read_bytes()).hexdigest() == row['sha256']
    zurich = json.loads((HERE / 'zurich_canton_staff_fte.json').read_text())
    expected_keys = {'Schuljahr', 'Schultyp', 'Vollzeiteinheiten'}
    assert zurich['data'] and all(set(row) == expected_keys for row in zurich['data'])
    assert {row['Schultyp'] for row in zurich['data']} == {'Mittelschule', 'Berufsbildung'}
    assert 'im Kanton' in zurich['meta']['readingExampleContent']
    assert 'öffentlich finanzierten' in zurich['meta']['title']
    assert '15.9.' in zurich['meta']['description']
    assert any(row['Schuljahr'] == '2025/26' for row in zurich['data'])
    bfs = (HERE / 'bfs_public_teacher_table.html').read_text()
    bfs_text = re.sub('<[^>]*>', ' ', bfs)
    assert 'öffentliche Schulen' in bfs_text and 'in Personen' in bfs_text
    ireland = json.loads((HERE / 'ireland_EDA82.json').read_text())
    assert len(ireland['dimension']) == 3
    assert {d['label'] for d in ireland['dimension'].values()} == {'School Type', 'Year', 'Statistic'}
    assert ireland['extension']['official']
    pdftext = subprocess.check_output(['pdftotext', '-layout', str(HERE / 'ireland_workforce_quality2026.pdf'), '-'], text=True)
    stored = (HERE / 'ireland_workforce_quality2026.txt').read_text()
    assert stored == pdftext
    text = re.sub(r'\s+', ' ', pdftext)
    assert 'They are not published at this level.' in text
    assert 'Calculations are aggregated to county level' in text
    assert 'data is not published at roll number or PPSN level' in text
    zurich_excerpt = (HERE / 'zurich_yearbook2011_scope_excerpt.txt').read_text()
    assert 'T_15.1.19' in zurich_excerpt and 'T_15.2.1' in zurich_excerpt
    assert 'Voll- und Teilzeitbeschäftigte' in zurich_excerpt
    assert 'Gymnasium (Unterstufe)' in zurich_excerpt
    helsinki_excerpt = (HERE / 'helsinki_yearbook2024_scope_excerpt.txt').read_text()
    assert 'Opettajien antamat opetustunnit' in helsinki_excerpt
    assert 'Kansalaisopistot' in helsinki_excerpt and 'Lukiokoulutus' in helsinki_excerpt
    attempts = json.loads((HERE / 'attempts.json').read_text())
    assert attempts and all(r['date'] == '2026-11-09' and not r['admitted'] for r in attempts)
    observations = json.loads((HERE / 'observations.json').read_text())
    assert observations == []
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == original_hash
    audit = dict(status='pass', dataset='user16 V121 unchanged',
        access_date='2026-11-09', admitted_cells=0, attempts=len(attempts),
        cities_checked=['Zurich', 'Helsinki', 'Dublin'],
        canton_FTE_not_substituted_for_city=True,
        public_canton_headcount_not_used_as_all_provider_city_FTE_superset=True,
        ireland_roll_level_nonpublication_verified=True,
        teaching_hours_headcounts_allocations_not_substituted_for_FTE=True,
        original_CSV_sha256=original_hash, observations_empty=True,
        model_registry_or_bound_writes=False)
    (HERE / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
