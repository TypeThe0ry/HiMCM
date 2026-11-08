"""Verify archived-report evidence without treating it as the missing questionnaire."""
import hashlib,json,zipfile
from pathlib import Path
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'audit.json').read_text())
p=HERE/r['report_file']
assert hashlib.sha256(p.read_bytes()).hexdigest()==r['report_sha256']
t=PdfReader(p).pages[r['report_pdf_page']-1].extract_text()
assert 'adjuntan como anexos digitales' in t and 'Cuestionarios' in t
zpath=HERE/r['archive_file']
if zpath.exists():
 assert hashlib.sha256(zpath.read_bytes()).hexdigest()==r['archive_sha256']
 with zipfile.ZipFile(zpath) as z:assert z.namelist()==r['archive_members']
assert r['main_admitted'] is False and r['new_admissible_travel_observations']==0
print('PASS: report identifies separate questionnaire annex; no stage inference admitted')
