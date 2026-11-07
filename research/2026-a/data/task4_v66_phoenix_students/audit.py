"""Check source integrity and reject school-level/geographic substitution."""
import hashlib
import json
import re
from pathlib import Path

p = Path(__file__).resolve().parent
for f in json.loads((p / 'manifest.json').read_text())['files']:
    b = (p / f['file']).read_bytes()
    assert len(b) == f['bytes']
    assert hashlib.sha256(b).hexdigest() == f['sha256']
s = re.sub('<[^>]+>', ' ', (p / 'phoenix_srts_pmc.html').read_text())
for term in ['2751', '35 schools', 'grades 3–8', '2010 and 2014']:
    assert term in s, term
a = json.loads((p / 'audit.json').read_text())
assert a['admissible_observations'] == 0
assert not a['model_input_changed'] and not a['missing_interval_changed']
assert a['sources'][0]['grades'] == list(range(3, 9))
assert a['sources'][1]['decision'] == 'do_not_admit'
print('PASS: source hashes, actual grades 3–8 survey, zero admissible high-school observations')
