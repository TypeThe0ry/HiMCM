"""Verify the preserved web response and the bounded population exclusion."""
import hashlib
import json
from pathlib import Path

p = Path(__file__).resolve().parent
m = json.loads((p / 'manifest.json').read_text())
b = (p / m['file']).read_bytes()
assert len(b) == m['bytes']
assert hashlib.sha256(b).hexdigest() == m['sha256']
s = json.loads(b)
a = json.loads((p / 'audit.json').read_text())
assert '2022 Maricopa County' in s and 'workforce commute' in s
for field in a['fields']:
    assert field + ' ( type:' in s, field
assert a['new_admissible_observations'] == 0
assert a['student_count_field'] is None
assert a['school_site_field'] is None
assert a['age_or_grade_field'] is None
print('PASS: archive hash and workforce schema; 0 high-school observations admitted')
