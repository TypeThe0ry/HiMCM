"""Check published youth tables, provenance and unchanged science/paper inputs."""
import csv
import hashlib
import json
import subprocess
import tempfile
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_audit_output import audit_parser, check_output, emit_report

R = Path(__file__).resolve().parents[1]
G = R.parents[1]
D = R / 'data/current_oslo_youth2026'
O = R / 'results/current_oslo_youth2026'
# Root transcription from rendered original physical pages13/21/28. Each row is
# meeting places, sports facilities, culture, transport, sports participation,
# financial constraint. This reference does not call the extraction routine.
VISUAL_LOWER = {
    'Stovner': [61,67,50,69,55,18], 'Grorud': [70,72,44,70,60,21],
    'Alna': [64,66,43,71,59,17], 'Søndre Nordstr.': [71,72,50,73,60,16],
    'Gamle Oslo': [66,72,58,77,61,19], 'Grünerløkka': [55,71,58,78,60,17],
    'Bjerke': [54,69,52,76,67,13], 'Sagene': [66,77,70,83,61,15],
    'Østensjø': [64,76,49,81,67,13], 'St. Hanshaugen': [73,68,70,84,57,15],
    'Frogner': [58,70,69,80,68,13], 'Nordstrand': [65,82,73,86,74,10],
    'Ullern': [51,82,57,82,74,9], 'Nordre Aker': [54,83,66,87,80,9],
    'Vestre Aker': [48,82,60,84,76,8]}
MEASURES = ['meeting_places_good','sports_facilities_good','cultural_provision_good',
            'public_transport_good','sports_club_previous_month','parents_lack_activity_money']


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.urls.append(urljoin('https://www.ungdata.no/rapporter/', dict(attrs).get('href','')))


def main():
    args = audit_parser(__doc__).parse_args()
    canonical = O / 'verification.json'
    check_output(args, canonical, G)
    protection = protected_inputs()
    receipts = list(D.glob('*.receipt.json'))
    assert len(receipts) == 6
    status = Counter()
    links = Links(); links.feed((D/'catalogue.html').read_text())
    for p in receipts:
        m = read(p); body = D / p.name.removesuffix('.receipt.json')
        assert sha(body) == m['sha256'] and body.stat().st_size == m['bytes']
        assert datetime.fromisoformat(m['started_utc']).utcoffset() is not None
        status[m['status']] += 1
        if body.suffix == '.pdf':
            assert m['status'] == 200 and m['content_type'] == 'application/pdf'
            assert body.read_bytes().startswith(b'%PDF')
            assert links.urls.count(m['requested_url']) == 1
    assert status == {200:5,404:1}
    assert read(D/'project.html.receipt.json')['status'] == 404
    with (O/'published_district_values.csv').open() as f:
        rows = list(csv.DictReader(f))
    indexed = {(r['stage'],r['district'],r['measure']):r for r in rows}
    assert len(rows) == len(indexed) == 180
    for district, values in VISUAL_LOWER.items():
        for measure, value in zip(MEASURES, values):
            row = indexed['lower',district,measure]
            assert int(row['published_percent']) == value
            assert row['use_status'] == 'descriptive_context'
    assert sum(r['use_status'] == 'quarantined_local_identity_mismatch' for r in rows) == 90
    summary = read(O/'summary.json')
    for k, measure in enumerate(MEASURES):
        vals = [v[k] for v in VISUAL_LOWER.values()]
        expected = summary['lower_stage_ranges'][measure]
        assert [expected['min_percent'],expected['max_percent'],expected['spread_percentage_points']] == [min(vals),max(vals),max(vals)-min(vals)]
        assert expected['minimum_districts'] == [d for d,v in VISUAL_LOWER.items() if v[k] == min(vals)]
        assert expected['maximum_districts'] == [d for d,v in VISUAL_LOWER.items() if v[k] == max(vals)]
    # Numeric outputs are replayed into a fresh external directory, never in place.
    with tempfile.TemporaryDirectory(prefix='himcm-youth-qa-',dir='/data/scratch') as tmp:
        dest = Path(tmp)/'replay'
        subprocess.run([__import__('sys').executable, str(R/'scripts/task4_current_oslo_youth2026.py'),
                        '--output-dir', str(dest)], check=True, stdout=subprocess.PIPE)
        for name in ['published_district_values.csv','summary.json']:
            assert (dest/name).read_bytes() == (O/name).read_bytes()
    assert protected_inputs() == protection
    current = read(R/'results/current_paper_review/current_verification.json')
    for name, digest in current['edition_source_sha256'].items():
        assert sha(R/name) == digest
    sources = [*sorted(D.iterdir()),O/'summary.json',O/'published_district_values.csv',O/'README.md',
               Path(__file__),R/'scripts/task4_current_oslo_youth2026.py',
               R/'scripts/audit_current_oslo_cost_ptr_sources.py',R/'scripts/task4_audit_output.py',
               R/'design/task4_user_v203_snapshot.json']
    report = dict(status='pass bounded resident-district source review',**protection,
        edition_entries_checked=24, HTTP200_bodies=5, HTTP404_bodies=1,
        lower_cells_against_visual_transcription=90,
        same_stage_duplicate_table_cells_checked=180, distinct_samples_replicated=0,
        upper_local_charts_quarantined=True, upper_table_cells_quarantined=90,
        root_visual_pages=[13,21,28], physical_pages=True,
        output_files_bytewise_reproduced=2, item_denominators_obtained=False,
        exact_age_or_cross_stage_contrast_calculated=False,
        primary_admissions=0, actual_primary_width_reduction=0,
        changes_primary_model=False, changes_manuscript=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in sources if p.is_file()},
        scope='Published rounded district table extraction, duplicate-publication consistency,90 lower-stage visual values and existing science/paper preservation. Upper local identity mismatch retained; no respondent microdata, significance, causal or comprehensive chart certification.')
    emit_report(report,args,canonical,G)


if __name__ == '__main__':
    main()
