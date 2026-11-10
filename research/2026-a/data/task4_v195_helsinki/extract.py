"""Verify archived raw bytes and extract the new registry-method passage."""
from pathlib import Path
import hashlib,json,html
P=Path(__file__).resolve().parent
receipts=json.loads((P/'retrievals.json').read_text())
for r in receipts:
 if r.get('file'):
  b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
s=(P/'parliament_HE143_2025_original.html').read_text()
start=s.index('Opetus- ja kulttuuriministeriö selvitti rekisteriaineistojen')
end=s.index('\\u003C/p>',start)
t=html.unescape(s[start:end]).strip()
assert 'Vuoden 2022 lopussa noin 900 opettajaa' in t
assert 'noin neljää prosenttia' in t
assert 'ei ole välttämättä täysin luotettavaa' in t
(P/'registry_passage_extracted.txt').write_text(t+'\n')
print('PASS: raw size/SHA; registry passage literal claims; zero PTR derivation')
