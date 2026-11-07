import hashlib
import json
from pathlib import Path

p = Path(__file__).resolve().parent
for item in json.loads((p / 'manifest.json').read_text())['files']:
    raw = (p / item['file']).read_bytes()
    assert len(raw) == item['bytes']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']
assert (p / 'glendale_2019_active_transportation.pdf').read_bytes().startswith(b'%PDF')
s = (p / 'glendale_pdf_page30_excerpt.txt').read_text()
for term in ['2015 TRP survey', '15.0 miles', '7.1 miles', 'Of students that use alternative modes', '8.6 percent']:
    assert term in s, term
print('PASS: original PDF and response hashes; county student miles, no Phoenix high-school duration admitted')
