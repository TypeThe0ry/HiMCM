from collections import Counter
import hashlib
import json
from pathlib import Path

path = Path(__file__).resolve().parent
raw = (path / 'kanton_zh_wfs.geojson').read_bytes()
metadata = json.loads((path / 'provenance.json').read_text())
assert hashlib.sha256(raw).hexdigest() == metadata['sha256']
data = json.loads(raw)
features = data['features']
assert len(features) == metadata['feature_count'] == data['numberMatched']
zurich = [f['properties'] for f in features if f['properties']['cname'] == 'Zürich']
assert len(zurich) == metadata['cname_exact_Zürich'] == 479
print('All features:', len(features))
print('Exact cname Zürich:', len(zurich))
print('Without listed lines:', sum(not p['linien'] for p in zurich))
print('Repeated names:', {k: v for k, v in Counter(p['chstname'] for p in zurich).items() if v > 1})
