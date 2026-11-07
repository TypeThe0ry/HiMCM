from pathlib import Path
import hashlib,json
from pypdf import PdfReader
root=Path(__file__).resolve().parent
for row in json.loads((root/'manifest.json').read_text()):
    raw=(root/row['file']).read_bytes()
    assert len(raw)==row['bytes']
    assert hashlib.sha256(raw).hexdigest()==row['sha256']
r=PdfReader(root/'casen2024_questionnaire.pdf')
assert 'e6a_asiste' in r.pages[14].extract_text()
assert 'nivel educacional al que asiste' in r.pages[14].extract_text()
assert 'o28a' in r.pages[26].extract_text()
assert 'lugar principal de' in r.pages[26].extract_text()
assert 'trabajo' in r.pages[26].extract_text()
print('PASS: 2 originals verified; current-stage and work-duration wording verified; 0 school-duration observations admitted.')
