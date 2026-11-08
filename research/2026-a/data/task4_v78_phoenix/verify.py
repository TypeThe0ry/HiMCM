"""Check the archived reader-note files, not original PDF authenticity."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'manifest.json').read_text())
assert manifest['evidence_type'] == 'selected_web_reader_transcription_not_original_pdf'
for item in manifest['files']:
    blob = (HERE / item['file']).read_bytes()
    assert len(blob) == item['bytes']
    assert hashlib.sha256(blob).hexdigest() == item['sha256']
assert 19941 + 9565 + 721 == 30227
assert 1976699 + 961850 + 70470 == 3009019
assert manifest['main_bound_changed'] is False
print('Reader-note integrity and county-row arithmetic passed; no city bound admitted.')
