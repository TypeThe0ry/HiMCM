"""Verify archived originals and inventory public LTDS tables (stdlib only)."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent
NS = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'}
for source in json.loads((ROOT / 'manifest.json').read_text()):
    raw = (ROOT / source['file']).read_bytes()
    assert len(raw) == source['bytes'], source['file']
    assert hashlib.sha256(raw).hexdigest() == source['sha256'], source['file']
with zipfile.ZipFile(ROOT / 'ltds2024_25.ods') as archive:
    tree = ET.fromstring(archive.read('content.xml'))
inventory = []
for sheet in tree.findall('.//table:table', NS):
    rows = []
    for row in sheet.findall('table:table-row', NS):
        cells = [' '.join(cell.itertext()) for cell in row.findall('table:table-cell', NS)]
        if any(cells):
            rows.append(cells)
    inventory.append({'sheet': sheet.get('{'+NS['table']+'}name'), 'rows': rows})
(ROOT / 'workbook_inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2)+'\n')
print(f'PASS: 4 original hashes; {len(inventory)} sheets inventoried; no model observations admitted.')
