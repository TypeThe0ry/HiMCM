"""Verify archived official source and its model-definition rejection locator."""
from pathlib import Path
import hashlib,html,json,re
P=Path(__file__).resolve().parent
rows=json.loads((P/'retrievals.json').read_text())
r=next(x for x in rows if x.get('status')==200)
p=P/r['file'];data=p.read_bytes()
assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256']
s=html.unescape(data.decode())
notes=re.findall(r'<dfn title="(.*?)">Anm\. 2</dfn>',s,re.S)
assert len(notes)==1
note=notes[0]
for term in ['Geschwindigkeitsmodell','schnellste Route','Wohngebäude','PKW']:
 assert term in note,term
assert '<indicator-block name="J5.1"' in s
print('PASS: archived SHA/bytes; Anm.2 identifies modeled fastest-road travel, not observed duration')
