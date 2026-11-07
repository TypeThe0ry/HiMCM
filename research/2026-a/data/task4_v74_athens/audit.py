"""Verify acquired source metadata, never treat failed downloads as observations."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
    raw=(P/r['file']).read_bytes()
    assert len(raw)==r['bytes']
    assert hashlib.sha256(raw).hexdigest()==r['sha256']
teacher=json.loads((P/'teacher_metadata.json').read_text())['result']
assert 'ιδιωτικές σχολικές μονάδες' in teacher['notes']
for name in ('minedu_students_school','minedu_schools'):
    row=json.loads((P/(name+'_metadata.json')).read_text())
    assert row['projection'] and len(row['resources'])==2
    assert all(r['datastore_active'] is False for r in row['resources'])
assert not (P/'students_school.csv').exists()
assert not (P/'students_school.zip').exists()
assert not (P/'schools_directory.zip').exists()
print('Three metadata artifacts verified; zero acquired pupil/teacher observations.')
