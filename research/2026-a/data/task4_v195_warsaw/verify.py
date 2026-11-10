"""Offline verification of failed official file captures, never data admission."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
rows=json.loads((P/'retrievals.json').read_text())
assert len(rows)==2
for r in rows:
 b=(P/r['file']).read_bytes()
 assert len(b)==r['bytes']==0 and r['status']==202
 assert r['content_type'].startswith('text/html')
 assert hashlib.sha256(b).hexdigest()==r['sha256']
print('PASS: 2 HTTP202 empty HTML responses; no presentation/PDF obtained; 0 admissions')
