"""Verify the archived Valley Metro OD2023 source and relevant variable definitions."""
import hashlib,json
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'manifest.json').read_text())
for f in m['files']:
 b=(ROOT/f['file']).read_bytes()
 assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
r=PdfReader(ROOT/'valley_metro_od2023.pdf');assert len(r.pages)==103
s='\n'.join(x.extract_text() or '' for x in r.pages)
for value in ['STUDENT_STATUS','K-12th grade','YOUR_AGE','16 - 18','TIME_ON','OPPO_DIR_TRIP_TIME']:
 assert value in s,value
assert 'BOARD this bus' in s
print('Verified: OD2023 original, 103 pages, K–12/age categories and boarding/reverse-trip clocks; no model observation admitted')
