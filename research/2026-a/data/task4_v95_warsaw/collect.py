"""Acquire pinned official inputs without changing their original bytes."""
import hashlib,json,ssl,urllib.request
from pathlib import Path
import certifi
P=Path(__file__).resolve().parent
for row in json.loads((P/'manifest.json').read_text()):
 p=P/row['file']
 if not p.exists():
  b=urllib.request.urlopen(row['url'],timeout=45,context=ssl.create_default_context(cafile=certifi.where())).read()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:
   raise ValueError('Source bytes changed; inspect as a new version: '+row['file'])
  p.write_bytes(b)
 assert p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
print('All three pinned official sources verified')
