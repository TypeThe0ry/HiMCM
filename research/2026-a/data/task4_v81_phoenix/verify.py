"""Verify the retained NCES school identity and official school-address original."""
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parent
r=json.loads((HERE/'crosscheck.json').read_text())
p=HERE/r['nces_source_relative']
assert hashlib.sha256(p.read_bytes()).hexdigest()==r['nces_source_sha256']
rows=json.loads(p.read_text())['features']
a=[x['attributes'] for x in rows if str(x['attributes']['NCESSCH'])==r['nces_id']]
assert len(a)==1
for raw,key in [('SURVYEAR','nces_reference_year'),('LCITY','nces_physical_city'),('NMCNTY','nces_county'),('LSTREET1','nces_street')]:
    assert a[0][raw]==r[key]
d=json.loads((HERE/'download.json').read_text());b=(HERE/'ridgeview_school.html').read_bytes()
assert len(b)==d['bytes'] and hashlib.sha256(b).hexdigest()==d['sha256']
assert b'San Tan Valley' in b and b'1645 W Skyline Drive' in b
assert r['appendix_city']=='PHOENIX' and r['nces_physical_city']=='San Tan Valley'
assert r['main_model_admitted'] is False
print('Physical-city crosscheck passed; appendix teacher count remains reader-only and unadmitted.')
