"""Offline integrity and literal-table checks; admission remains a scope decision."""
import hashlib,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
meta=json.loads((P/'retrieval.json').read_text())
f=P/'canton_2025_2026_original.pdf'
assert len(f.read_bytes())==meta['bytes']
assert hashlib.sha256(f.read_bytes()).hexdigest()==meta['sha256']
t=subprocess.check_output(['pdftotext','-layout','-f','15','-l','15',str(f),'-']).decode()
assert re.search(r'Mittelschule\s+3\s+2 812\s+1271\s+1 541\s+54\.8',t)
assert re.search(r'Mittelschule\s+63\.0 %\s+1 771\.6',t)
assert re.search(r'Mittelschulen\s+3 617\s+2 179\s+2 227',t)
s=json.loads((P/'scope.json').read_text())
assert s['source_sha256']==meta['sha256']
assert s['admission']['admitted'] is False and s['admission']['PTR_computed'] is False
print('PASS: original SHA/size, three separate page15 entries, no admission')
