"""Offline candidate extraction; no edits to registered model or submitted CSV."""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    manifest = json.loads((HERE / 'sources.json').read_text())
    for record in manifest['sources']:
        path = HERE / record['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], path
    metadata = json.loads((HERE / 'kolada_N17816_metadata.json').read_text())['values'][0]
    municipality = json.loads((HERE / 'kolada_0180_municipality.json').read_text())['values'][0]
    data = json.loads((HERE / 'kolada_stockholm_2025.json').read_text())['values']
    assert metadata['id'] == 'N17816' and metadata['auspice'] == 'T'
    assert metadata['municipality_type'] == 'K'
    assert metadata['operating_area'] == 'Gymnasieskola åk 1-3'
    assert 'gymnasieskola belägen i kommunen' in metadata['description']
    assert 'heltidstjänst' in metadata['description']
    assert '15 oktober' in metadata['description']
    assert 'Skolverket (Siris)' in metadata['description']
    assert municipality == {'id': '0180', 'title': 'Stockholm', 'type': 'K'}
    assert len(data) == 1
    row = data[0]
    assert row['kpi'] == 'N17816' and row['period'] == 2025 and row['municipality'] == '0180'
    assert len(row['values']) == 1
    value = row['values'][0]
    assert value['gender'] == 'T' and value['status'] == '' and not value['isdeleted']
    raw = Decimal(str(value['value']))
    # Deliberately retain only one decimal of the published ratio. This is a
    # conservative precision envelope, not an estimated measurement-error CI.
    rounded = raw.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
    lower, upper = rounded - Decimal('0.05'), rounded + Decimal('0.05')
    assert lower <= raw <= upper
    docs = re.sub(r'\s+', ' ', re.sub('<[^>]*>', ' ', (HERE / 'kolada_api_documentation.html').read_text()))
    assert 'T – total regi, dvs för all verksamhet oavsett regi' in docs
    assert 'Referensåret för den data som publiceras på nästa publiceringsdatum' in docs
    school_metadata = json.loads((HERE / 'skolverket_underlag_metadata.json').read_text())
    time = next(x for x in school_metadata['variables'] if x['code'] == 'time')
    assert dict(zip(time['values'], time['valueTexts']))['2025'] == '2025/26'
    source_hashes = {
        str((HERE / r['file']).relative_to(ROOT)): r['sha256']
        for r in manifest['sources'] if not r['file'].startswith('paris_')
    }
    observations = [{
        'city': 'Stockholm', 'indicator': 'upper_secondary_ptr', 'kind': 'ratio_interval',
        'ratio_bounds': [float(lower), float(upper)], 'published_api_ratio': float(raw),
        'published_period': 2025, 'school_year': '2025/26',
        'utility_after': [15 / (15 + float(upper)), 15 / (15 + float(lower))],
        'source_hashes': source_hashes,
        'scope': 'Upper-secondary school years 1-3, schools located in Stockholm municipality, all providers, pupils per teacher FTE; 15 October snapshot. School-resource proxy, not ages14-18 resident-only measurement.',
        'precision_rule': 'API ratio 16.42091405 intentionally coarsened to 16.4 with a half-last-digit envelope [16.35,16.45]; not a confidence interval or independently identified measurement-error bound.',
        'candidate_only': True,
    }]
    (HERE / 'observations.json').write_text(json.dumps(observations, indent=2, ensure_ascii=False) + '\n')
    # Denominator mismatch evidence is extracted from the original official PDF.
    paris = subprocess.check_output(['pdftotext', '-f', '4', '-l', '8', '-layout', str(HERE / 'paris_chiffres_2025.pdf'), '-'], text=True)
    assert '72 476' in paris and '15 940' in paris and '2d degré' in paris
    (HERE / 'paris_relevant_pages.txt').write_text(paris)
    print(json.dumps(observations, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
