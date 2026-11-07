"""Offline verification of archived official catalogue evidence, not travel data."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent
for row in json.loads((root / 'manifest.json').read_text()):
    data = (root / row['file']).read_bytes()
    assert len(data) == row['bytes']
    assert hashlib.sha256(data).hexdigest() == row['sha256']
catalogue = (root / 'tu_archive_catalogue.html').read_text()
fields = (root / 'tu_archive_person_fields.html').read_text()
assert '1992-2003' in catalogue
assert 'Søg om adgang' in catalogue
assert 'bkom' in fields and 'pvgt' in fields
assert 'højeste gennemførte uddannelse' in fields
report = json.loads((root / 'audit.json').read_text())
assert report['new_admissible_observations'] == 0
assert report['model_input_changed'] is False
print('PASS: two source hashes, historical period, access application and education definition; no model input added')
