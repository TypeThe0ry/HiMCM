from pathlib import Path
import hashlib,json
p=Path(__file__).parent
manifest=json.loads((p/'source_manifest.json').read_text())
for row in manifest['files']:
    b=(p/row['file']).read_bytes()
    assert len(b)==row['bytes']
    assert hashlib.sha256(b).hexdigest()==row['sha256']
for f,ids in [('metadata_session_expanded.html',['378626']),('metadata_split_0.html',['378627']),('metadata_split_1.html',['378628'])]:
    text=(p/f).read_text().lower()
    for v in ids: assert 'cechid="'+v+'"' in text
assert b'100' in (p/'variables.response').read_bytes()
print('PASS: source hashes, metadata variable IDs, and archived API limit response; no values admitted')
