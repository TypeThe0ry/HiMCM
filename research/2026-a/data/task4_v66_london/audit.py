"""Verify downloaded original; audit PDF keyword page locations, not admission."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'manifest.json').read_text())
for row in rows:
    if row['status']!=200:continue
    data=(ROOT/row['file']).read_bytes()
    assert len(data)==row['bytes']
    assert hashlib.sha256(data).hexdigest()==row['sha256']
reader=PdfReader(ROOT/'ltds2025_report.pdf')
hits={k:[i+1 for i,p in enumerate(reader.pages) if k in p.extract_text().lower()] for k in ['school','education','journey time','travel time','sixth']}
print(json.dumps(dict(original_verified=True,pages=len(reader.pages),keyword_pages=hits,new_admitted_observations=0),indent=2))
