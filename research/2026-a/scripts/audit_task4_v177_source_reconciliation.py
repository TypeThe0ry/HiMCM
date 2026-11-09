"""Independently audit V177 archived-source scope and exact rational arithmetic.

Reads frozen outputs and original inputs; writes only this round's verification.
No source re-fetch, model evaluation, Monte Carlo draw or manuscript edit occurs.
"""
from pathlib import Path
from fractions import Fraction
from html import unescape
import csv
import hashlib
import json
import re
import subprocess

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
D = R / 'data/task4_v177_source_reconciliation'
O = R / 'results/task4_v177_source_reconciliation'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def visible(path):
    raw = path.read_text()
    raw = re.sub(r'<(script|style|noscript)\b[^>]*>.*?</\1\s*>', '', raw,
                 flags=re.I | re.S)
    return ' '.join(unescape(re.sub(r'<[^>]+>', ' ', raw)).split())


def close_display(value, exact):
    # Finite decimal output is an approximate display, not outward rounding.
    assert abs(Fraction(value) - exact) <= Fraction(1, 10**40), value


def main():
    result = read(O / 'reconciliation.json')
    scope = read(O / 'source_scope.json')
    binding = read(O / 'source_bindings.json')
    protected = read(O / 'protected_files.json')
    retrievals = read(D / 'retrievals.json')
    source = R / 'data/task4_v117_team_intake/city_indicators.csv'
    assert sha(source) == binding['source_csv_sha256']
    assert sha(D / 'retrievals.json') == binding['retrieval_manifest_sha256']
    assert sha(R / 'scripts/task4_v177_source_reconciliation.py') == binding['script_sha256']
    urls = {
        'zurich_population2024_original.html': 'https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2025/02/fast-450000-einwohnerinnen-in-der-stadt-zuerich.html',
        'ireland_mip2026_notes_original.html': 'https://www.cso.ie/en/releasesandpublications/ep/p-mip/measuringirelandsprogress2026/backgroundnotes/',
    }
    assert len(retrievals) == len(urls) == 2
    assert {item['file'] for item in retrievals} == set(urls) == set(binding['files'])
    for item in retrievals:
        path = D / item['file']
        assert item['url'] == item['final_url'] == urls[item['file']]
        assert item['http_status'] == 200 and item['content_type'].startswith('text/html')
        assert path.stat().st_size == item['bytes']
        assert sha(path) == item['sha256'] == binding['files'][item['file']]

    population_text = visible(D / 'zurich_population2024_original.html')
    assert 'Ende 2024 wohnten 448 664 Personen in der Stadt Zürich.' in population_text
    official = scope['zurich_population']
    assert (official['value'], official['year'], official['geography']) == (448664, 2024, 'Stadt Zürich')
    assert official['use'] == 'source reconciliation only'
    assert 'end of year' in official['reference']
    assert 'not a crime-rate denominator certification' in result['official_population_observation']

    notes = visible(D / 'ireland_mip2026_notes_original.html')
    section = notes.split('Pupil-teacher ratio (4.3)', 1)[1].split('Literacy (4.5)', 1)[0]
    assert 'in Ireland ISCED level 3 includes ISCED level 2' in section
    assert 'full-time equivalent pupils' in section and 'full-time equivalent teachers' in section
    assert 'CSO statistical release, 20 October 2026' in notes
    assert 'title reflects the year of publication' in notes
    assert 'For each indicator, the latest available data is presented.' in notes
    ireland = scope['ireland_notes']
    assert ireland['publication'] == '20 October2026'
    assert ireland['geographic_scope'] == 'Ireland,not Dublin city'
    assert ireland['education_section'] == '4.3'
    assert ireland['stage_warning'] == 'Ireland ISCED3 includesISCED2'
    assert ireland['no_matched_city_teaching_FTE_acquired'] is True
    assert ireland['mixed_stage_teacher_superset_not_ruled_out_in_principle'] is True
    assert 'publication year' in ireland['year_warning']

    with source.open(encoding='utf-8-sig') as stream:
        row = next(r for r in csv.DictReader(stream) if r['city'] == 'Zurich')
    count, rate, population = (Fraction(row[k]) for k in
                               ['homicide_numerator', 'homicide_per_100k', 'population'])
    assert (count, rate, population) == (1, Fraction(14, 100), 440935)
    assert Fraction(result['retained_count']) == count
    assert Fraction(result['retained_rate']) == rate
    for out_key, in_key in [('retained_rate_year', 'homicide_per_100k_year'),
                            ('retained_population_year', 'population_year'),
                            ('retained_flag', 'homicide_per_100k_flag')]:
        assert result[out_key] == row[in_key]
    assert (row['homicide_per_100k_year'], row['population_year'], row['homicide_per_100k_flag']) == ('2024', '2025', 'SUSPECT')
    lower_rate, upper_rate = rate - Fraction(5, 1000), rate + Fraction(5, 1000)
    assert list(map(Fraction, result['assumed_nearest_two_decimal_rate_envelope'])) == [lower_rate, upper_rate]
    low, high = count * 100000 / upper_rate, count * 100000 / lower_rate
    close_display(result['implied_population_for_exact_point_rate'], count * 100000 / rate)
    for displayed, exact in zip(result['compatible_population_closed_envelope'], [low, high]):
        close_display(displayed, exact)
    assert 'Hypothetical closed outer envelope' in result['rounding_assumption_status']
    assert 'actual supplied rounding convention unknown' in result['rounding_assumption_status']
    assert 'rounded to50 significant digits' in result['numerical_display']
    assert 'No boundary classification relies on display rounding' in result['numerical_display']
    alternatives = {r['population_source']: r for r in result['alternatives']}
    expected_populations = {'retained_2025_population': population,
                            'municipal_release_end2024_population': Fraction(official['value'])}
    assert set(alternatives) == set(expected_populations)
    for name, exact_population in expected_populations.items():
        alternative = alternatives[name]
        assert Fraction(alternative['population']) == exact_population
        close_display(alternative['arithmetic_count_per100000'], count * 100000 / exact_population)
        close_display(alternative['implied_count_at_point_rate'], rate * exact_population / 100000)
        assert alternative['within_assumed_rounding_envelope'] == (low <= exact_population <= high) is False
        assert low - exact_population > 200000
    assert result['primary_admissions'] == result['score_interval_width_change'] == 0
    assert result['manuscript_changed'] is False
    assert 'Original rate source, unit and denominator remain unestablished.' in result['conclusion']
    assert set(result['inference_not_made']) == {
        'corrected annual city homicide-victim rate',
        'falsehood of every alternative city definition',
        'one-sided victim-count bound from offence counts',
        'replacement of any user value',
    }

    science = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    assert protected['science'] == science and len(science) == 187
    assert len(protected['paper']) == 615
    for root, records in [(R, science), (P, protected['paper'])]:
        for name, expected in records.items():
            assert sha(root / name) == expected, name
    registry_hashes = {}
    for filename, field, version in [
        ('task4_user_current_model.json', 'version', 'V154'),
        ('task4_user_current_extensions.json', 'extension_version', 'V154'),
        ('task4_user_current_review.json', 'version', 'V176'),
    ]:
        relative = 'research/2026-a/design/' + filename
        path = R / 'design' / filename
        assert path.read_bytes() == subprocess.check_output(['git', '-C', str(R.parents[1]), 'show', 'HEAD:' + relative])
        assert read(path)[field] == version
        registry_hashes[relative] = sha(path)
    review = read(R / 'design/task4_user_current_review.json')
    assert read(P / 'drafts/task4_current_review.json') == review
    assert sha(P / review['pdf']) == review['pdf_sha256']
    report = dict(version='V177', status='pass', independent_arithmetic='Fraction exact rational quotients and membership',
                  numeric_display_absolute_tolerance='1e-40; display agreement only, not directed outward endpoint certification',
                  alternatives_checked=2, exact_minimum_population_separation_over_200000=True,
                  archived_originals_identity_checked=2, refetched_sources=False,
                  source_scope='End2024 municipal population and CSO MIP2026 table4.3 national mixed-stage metadata only',
                  hypothetical_rounding_only=True, corrected_rate_inferred=False,
                  scientific_files_unchanged=187, existing_paper_files_unchanged=615,
                  registries_unchanged_from_HEAD=registry_hashes,
                  current_paper='V176 unchanged', primary_model='V154 unchanged',
                  canonical_pdf_sha256=review['pdf_sha256'], new_data_admitted=0,
                  model_score_probes=False, MC_rerun=False, manuscript_changed=False,
                  auditor_sha256=sha(Path(__file__)),
                  audited_output_sha256={name: sha(O / name) for name in
                                         ['reconciliation.json', 'source_scope.json', 'source_bindings.json', 'protected_files.json']})
    (O / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
