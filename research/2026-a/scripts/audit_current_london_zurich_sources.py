"""Read-only London teacher-envelope and Zurich broadband source checks."""
from pathlib import Path
from html.parser import HTMLParser
import csv, hashlib, json, math, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from task4_audit_output import audit_parser, check_output, emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES

R = Path(__file__).resolve().parents[1]; G = R.parents[1]; P = G.parent / 'HiMCM-Overleaf'
L = R / 'data/current_london_teacher_envelope'; Z = R / 'data/current_zurich_broadband_source'
O = R / 'results/current_london_zurich_review/verification.json'
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class Broadband(HTMLParser):
    """Parse the fixed-median table independently of the regex extractor."""
    def __init__(self):
        super().__init__(); self.depth = 0; self.active = None
        self.row = None; self.cell = None; self.rows = []; self.text = []
        self.speed_header = False; self.download_headers = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'div':
            self.depth += 1
            if attrs.get('id') == 'column-fixedMedian': self.active = self.depth
        if not self.active: return
        if tag == 'tr': self.row = {'cells': [], 'links': []}
        if tag == 'td' and self.row is not None: self.cell = []
        if tag == 'a' and self.row is not None: self.row['links'].append(attrs.get('href'))
        if tag == 'th' and attrs.get('class') == 'speed': self.speed_header = True
        if tag == 'use' and self.speed_header and attrs.get('xlink:href') == '#icon-download': self.download_headers += 1
    def handle_data(self, data):
        self.text.append(data)
        if self.cell is not None: self.cell.append(data)
    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.row['cells'].append(' '.join(''.join(self.cell).split())); self.cell = None
        if tag == 'tr' and self.row is not None: self.rows.append(self.row); self.row = None
        if tag == 'th': self.speed_header = False
        if tag == 'div':
            if self.depth == self.active: self.active = None
            self.depth -= 1

def workbook_rows(path):
    selected = {}
    with zipfile.ZipFile(path) as archive:
        strings = [''.join(item.itertext()) for item in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        for _, row in ET.iterparse(archive.open('xl/worksheets/sheet1.xml'), events=('end',)):
            if not row.tag.endswith('}row'): continue
            number = int(row.get('r'))
            if number in (1, 9, 14261):
                cells = {}
                for cell in row:
                    value = cell.find('{*}v')
                    if value is not None: cells[cell.get('r').rstrip('0123456789')] = strings[int(value.text)] if cell.get('t') == 's' else value.text
                selected[number] = cells
            row.clear()
            if number == 14261: break
    return selected

def main():
    args = audit_parser(__doc__).parse_args(); check_output(args, O, G)
    receipt = read(Z / 'source_reuse_receipt.json')
    for name, digest in receipt['source_sha256'].items(): assert sha(R / name) == digest, name
    extracted = json.loads(subprocess.check_output([sys.executable, str(Z / 'extract.py')], text=True))
    assert extracted == receipt
    raw = (R / receipt['archive_file']).read_bytes()
    parser = Broadband(); parser.feed(raw.decode())
    rows = [row for row in parser.rows if '/global-index/switzerland?city=Zürich#fixed' in row['links']]
    assert len(rows) == 1 and rows[0]['cells'] == ['18', '+3', 'Zürich, Switzerland', '286.35']
    assert parser.download_headers == 2
    text = ' '.join(' '.join(parser.text).split())
    assert 'September 2026' in text and 'median download speeds' in text
    assert 'Results are updated mid-month for the previous three months.' in text
    coordinates = receipt['extraction_coordinates']
    assert raw[coordinates['byte_start_0based']:coordinates['byte_end_exclusive']].decode() == receipt['publisher_row_html']
    assert raw[:coordinates['byte_start_0based']].count(b'\n') + 1 == coordinates['line_start_1based']
    assert receipt['publisher_measure_field'] == 'fixedMedian' and receipt['direction'] == 'download'
    assert receipt['original_csv_extraction_lineage_verified'] is False and receipt['municipal_boundary_equivalence_verified'] is False

    london_receipts = read(L / 'receipts.json')
    assert len(london_receipts) == 3 and [r['status'] for r in london_receipts] == [403, 200, 200]
    for item in london_receipts:
        path = L / item['file']; assert path.stat().st_size == item['bytes'] and sha(path) == item['sha256']
        assert datetime.fromisoformat(item['utc']).utcoffset() is not None
    pupil_body = (L / 'raw/pupil_census.html').read_text()
    assert 'January 2025' in pupil_body and 'November School Workforce Census' in pupil_body
    offline = read(L / 'offline_record.json'); workbook = (L / offline['source']).resolve()
    assert sha(workbook) == offline['source_sha256'] == '8a90bb200fa76c3ba8d4a0a87d8e7258ae61bce5ee766586e2527e202a1d368e'
    original = next(item for item in read(R / 'data/task4_v36_london/manifest.json') if item['file'] == workbook.name)
    assert sha(workbook) == original['sha256'] and workbook.stat().st_size == original['bytes']
    sheet = workbook_rows(workbook)
    assert 'November 2024' in sheet[1]['A']
    for location, cell in offline['cells'].items():
        column = location.rstrip('0123456789')
        assert sheet[9][column] == cell['column']
        observed = sheet[14261][column]
        if isinstance(cell['value'], (float, int)): assert float(observed) == cell['value']
        else: assert observed == cell['value']
    assert sheet[14261]['F'] == '140564' and sheet[14261]['AG'] == '11.2'
    assert sheet[14261]['D'] == 'Lambeth' and sheet[14261]['L'] == 'Inner London'
    assert sheet[14261]['H'] == 'Free schools 16 to 19'
    scope = read(L / 'scope.json')
    assert scope['teacher_lower_bound'] is None and scope['pupil_upper_bound'] is None
    assert scope['contact_hours_conversion_required'] is False and scope['contract_FTE_permitted'] is True
    assert scope['primary_admissions'] == scope['actual_primary_width_reduction'] == 0

    current = read(R / 'results/current_paper_review/current_verification.json')
    core = read(R / 'design/task4_user_v203_snapshot.json')['source_sha256']; extra = {}
    for name, group in current.items():
        if name.startswith('additional_') and name.endswith('_sha256'): extra.update(group)
    assert len(core) == 548 and len(extra) == 77 and len(current['edition_source_sha256']) == 24
    for name, digest in {**core, **extra, **current['withdrawal_source_sha256'], **current['edition_source_sha256']}.items(): assert sha(R / name) == digest, name
    for name, digest in current['current_files_sha256'].items(): assert sha(P / name) == sha(G / 'paper/current' / name) == digest
    assert sha(G / 'paper/current/main.pdf') == current['pdf_sha256']
    frame, low, high = revised_bounds(); cities = frame.city.tolist()
    i = cities.index('London'); j = NAMES.index('upper_secondary_ptr'); assert low[i,j] == 0 and high[i,j] == 1
    i = cities.index('Zurich'); j = NAMES.index('fixed_broadband_mbps')
    assert low[i,j] == high[i,j] and math.isclose(low[i,j], 286.35/(100+286.35), rel_tol=0, abs_tol=1e-15)
    with (R / 'results/current_point_withdrawal/cases.csv').open() as stream:
        cases = [row for row in csv.DictReader(stream) if row['withdrawn_city'] == 'Zurich' and row['indicator'] == 'fixed_broadband_mbps']
    assert len(cases) == 2
    for row in cases:
        assert json.loads(row['after_choices']) == ['Oslo']
        assert json.loads(row['baseline_choices']) == (['Oslo'] if row['weight_reference'] == 'fixed' else ['Zurich'])
    sources = [p for directory in [L,Z] for p in sorted(directory.rglob('*')) if p.is_file()]
    sources += [workbook, R/'data/task4_v36_london/manifest.json', R/receipt['archive_file'], R/'data/task4_v5_resources/manifest.json', Path(__file__), R/'scripts/task4_audit_output.py']
    report = {'status':'pass scoped source review','new_successful_HTTP_bodies':2,'new_blocked_HTTP403_body':1,
        'independent_readers':{'workbook':'Standard-library OOXML shared strings, header9 and row14261','broadband':'HTMLParser compared with separate regex extractor; city-row byte coordinates and download header checked'},
        'reused_original_workbooks':1,'school_record':{'URN':140564,'row':14261,'classroom_teacher_FTE_published':11.2,'leadership_FTE_published':6.6,'all_teacher_FTE_published':17.8,'strict_target_stage_lower_bound_verified':False},
        'London_complete_pupil_upper_bound_verified':False,'London_PTR_utility':[0,1],
        'Zurich_broadband':{'publisher_match_Mbps':286.35,'statistic':'fixed broadband median download','publication_label':'September 2026','rolling_period':'Previous three months per page; exact city-row start/end unverified','original_input_lineage_verified':False,'municipal_boundary_equivalence_verified':False},
        'primary_admissions':0,'actual_primary_width_reduction':0,'core_bindings_checked':548,'supplemental_bindings_checked':77,
        'withdrawal_evidence_entries_checked':len(current['withdrawal_source_sha256']),'edition_evidence_entries_checked':24,'paper_dependencies_each_copy':7,'current_PDF_unchanged':True,
        'source_sha256':{str(p.relative_to(R)):sha(p) for p in sources},
        'scope':'Actual published school FTE row and exact publisher broadband match; no complete city teacher ratio, FTE contact-hour conversion, original input lineage, municipal-boundary certification, new observation or paper/model change. Reference-pair proxy is distinct from common-date measurement; neither resolves the incomplete all-provider pupil envelope.'}
    emit_report(report,args,O,G)

if __name__ == '__main__': main()
