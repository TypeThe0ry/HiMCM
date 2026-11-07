"""Extract MOE table cells using only the Python standard library."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def extract():
    for item in json.loads((ROOT/'manifest.json').read_text()):
        raw = (ROOT/item['file']).read_bytes()
        assert len(raw) == item['bytes']
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
    sheets = {}
    with ZipFile(ROOT/'tables2025.xlsx') as archive:
        strings = [''.join(x.itertext()) for x in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
        rels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(archive.read('xl/workbook.xml')).find('s:sheets', NS):
            name = sheet.attrib['name']
            if name not in ('3', '21'):
                continue
            target = rels[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            path = target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells = {}
            for cell in ET.fromstring(archive.read(path)).findall('.//s:c', NS):
                value = cell.find('s:v', NS)
                if value is not None:
                    cells[cell.attrib['r']] = strings[int(value.text)] if cell.attrib.get('t') == 's' else value.text
            sheets[name] = cells
    t, e = sheets['3'], sheets['21']
    assert t['C2'] == 'Teacher' and t['C3'] == 'Total'
    assert t['B12'] == 'Specialised Independent' and t['A14'] == 'Pre-University'
    assert e['A25'] == 'Pre-University' and e['B25'] == 'Total'
    assert e['B33'] == 'Specialised Independent'
    total, omitted = int(e['S25']), int(e['S33'])
    teachers, pool = int(t['C14']), int(t['C12'])
    assert teachers == sum(int(t[c]) for c in ('C15','C16','C17'))
    assert int(t['C4']) == sum(int(t[c]) for c in ('C5','C8','C14'))
    assert int(t['C8']) == sum(int(t[c]) for c in ('C9','C10','C11','C12','C13'))
    assert (total, omitted, teachers, pool) == (25130,748,1979,404)
    return dict(city='Singapore', year=2024, students=total, prior_matched_students=total-omitted,
                specialised_independent_students=omitted, classified_preuniversity_teacher_headcount=teachers,
                specialised_independent_teacher_pool=pool, teacher_allocation_interval=[0,pool],
                ptr_lower=total/(teachers+pool), ptr_upper=total/teachers,
                utility_lower=15*teachers/(15*teachers+total),
                utility_upper=15*(teachers+pool)/(15*(teachers+pool)+total),
                teacher_classification_note=t['A19'], part_time_note=t['A20'], exclusions=t['A18'],
                cells={'students':'21!S25','omitted_students':'21!S33','baseline_teachers':'3!C14','sis_teacher_pool':'3!C12'},
                scope='Pre-university JC/CI/Pre-U centres. Conditional allocation of reported teacher headcounts; not actual teaching hours, FTE, or all classification uncertainty.')

if __name__ == '__main__':
    result = extract()
    (ROOT/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
