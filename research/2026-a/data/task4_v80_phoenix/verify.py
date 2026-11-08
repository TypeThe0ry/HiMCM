"""Verify selected reader evidence, without claiming original PDF integrity."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'manifest.json').read_text())
assert not manifest['official_original_pdf_obtained']
for r in manifest['files']:
    raw=(HERE/r['file']).read_bytes()
    assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
s=(HERE/'reader_selected_response.txt').read_text()
assert re.search(r'Phoenix Union High School District</td>\s*<td>1330</td>\s*<td>85%</td>\s*<td>3%</td>\s*<td>12%</td>',s)
assert re.search(r'Phoenix Union High School District</td>\s*<td>1330</td>\s*<td>85%</td>\s*<td>2%</td>\s*<td>12%</td>',s)
print('Selected reader rows agree on count1330; switching percentage conflict retained; no main admission.')
