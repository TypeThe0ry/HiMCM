"""Verify original XLSX bytes and extract cached source cells, using stdlib only."""
import csv
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
manifest = json.loads((HERE / 'manifest.json').read_text())
raw = HERE / manifest['file']
assert raw.stat().st_size == manifest['bytes']
assert hashlib.sha256(raw.read_bytes()).hexdigest() == manifest['sha256']
with zipfile.ZipFile(raw) as z:
    strings = [''.join(node.itertext()) for node in ET.fromstring(z.read('xl/sharedStrings.xml'))]
    def cells(sheet):
        result = {}
        for cell in ET.fromstring(z.read(f'xl/worksheets/sheet{sheet}.xml')).findall('.//m:c', NS):
            value = cell.find('m:v', NS)
            if value is not None and value.text:
                result[cell.attrib['r']] = strings[int(value.text)] if cell.attrib.get('t') == 's' else value.text
        return result
    staff, schools, instructions = cells(7), cells(15), cells(19)
    assert staff['D5'] == 'July 1, 2024' and staff['F5'] == 'June 30, 2025'
    assert [staff[f'T{r}'] for r in (6, 7, 8)] == ['3', '3', '0']
    assert schools['B1'] == 'NORTH STAR CHARTER SCHOOL, INC.'
    assert schools['B2'] == '078945000'
    assert schools['B10'] == 'ARIZONA PREPARATORY ACADEMY' and schools['C10'] == '078945201'
    assert not any(f'B{r}' in schools for r in range(11, 100))
    assert 'only 1 line' in instructions['C34'] and 'Do not include instructional aides' in instructions['C34']
roster_path = HERE.parent / 'task4_v85_phoenix_public' / 'missing_staff_records.csv'
with roster_path.open() as stream:
    matches = [r for r in csv.DictReader(stream) if r['NCESSCH'] == '040030302181']
assert len(matches) == 1
r = matches[0]
assert r['SCH_NAME'] == 'Arizona Preparatory Academy' and 'North Star' in r['LEA_NAME']
ccd_path = HERE.parent / 'task4_v42_phoenix_coverage' / 'arizona_page_0.json'
ccd = [f['attributes'] for f in json.loads(ccd_path.read_text())['features'] if f['attributes']['NCESSCH'] == r['NCESSCH']]
assert len(ccd) == 1
ccd = ccd[0]
assert ccd['SURVYEAR'] == '2024-2025' and ccd['FTE'] == 6
assert ccd['SCH_NAME'] == 'Arizona Preparatory Academy' and 'North Star' in ccd['LEA_NAME']
assert (ccd['GSLO'], ccd['GSHI'], ccd['MEMBER']) == ('09', '12', 233)
result = {
    'charter': schools['B1'], 'charter_ctds': schools['B2'],
    'school': schools['B10'], 'school_ctds': schools['C10'],
    'ncessch_name_and_operator_crosswalk': r['NCESSCH'],
    'roster_source_sha256': hashlib.sha256(roster_path.read_bytes()).hexdigest(),
    'period': 'FY2025', 'source_sheet': 'Page 6',
    'ccd_2024_25_corroboration': {k: ccd[k] for k in ('NCESSCH', 'SURVYEAR', 'LEAID', 'ST_LEAID', 'GSLO', 'GSHI', 'MEMBER', 'FTE')},
    'ccd_source_sha256': hashlib.sha256(ccd_path.read_bytes()).hexdigest(),
    'fte_cells': {f'T{n}': float(staff[f'T{n}']) for n in (6, 7, 8)},
    'certified_fte': 3, 'noncertified_fte': 3, 'contract_fte': 0,
    'reported_teacher_fte_total': 6,
    'definition_cell': 'Instructions!C34', 'definition': instructions['C34'],
    'model_admission': False,
    'reason': 'FY2025 does not resolve FY2023/24 teacher missingness. Charter snapshot/grade allocation is not a city-complete teacher denominator.'
}
print(json.dumps(result, indent=2))
