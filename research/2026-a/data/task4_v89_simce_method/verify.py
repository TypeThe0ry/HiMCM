"""Verify archived official SIMCE methodology originals."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
for name,source in json.loads((HERE/'manifest.json').read_text()).items():
    raw=(HERE/name).read_bytes()
    assert raw.startswith(b'%PDF')
    assert len(raw)==source['bytes']
    assert hashlib.sha256(raw).hexdigest()==source['sha256']
print('Verified two official SIMCE technical reports')
