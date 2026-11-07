"""Audit official ISCED mapping and bound MOE's reported secondary teacher allocation."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parent
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def sheets(path):
    result = {}
    with ZipFile(path) as z:
        ss = [''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels = {r.attrib['Id']: r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sh in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets', NS):
            t = rels[sh.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            path = t.lstrip('/') if t.startswith('/') else 'xl/' + t
            cells = {}
            for c in ET.fromstring(z.read(path)).findall('.//s:c', NS):
                v = c.find('s:v', NS)
                if v is not None:
                    cells[c.attrib['r']] = ss[int(v.text)] if c.attrib.get('t') == 's' else v.text
            result[sh.attrib['name']] = cells
    return result

def extract():
    for folder in (ROOT, ROOT.parent/'task4_v38_singapore'):
        for item in json.loads((folder/'manifest.json').read_text()):
            b = (folder/item['file']).read_bytes()
            assert len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256']
    mapping = next(iter(sheets(ROOT/'isced2011_mapping.xlsx').values()))
    assert mapping['A3'] == 'School Year reference: 2023'
    for row, label, code in [(14,'Secondary 3 - 5','343'),(15,'Secondary 3 - 4','343'),(17,'Junior Colleges','444')]:
        assert mapping['B'+str(row)] == label and mapping['R'+str(row)] == code
    data = sheets(ROOT.parent/'task4_v38_singapore/tables2025.xlsx')
    t, g, a, e = (data[s] for s in ('3','4','6','21'))
    assert t['A8'] == 'Secondary' and t['C2'] == 'Teacher'
    secondary_teachers = int(t['C8']); assert secondary_teachers == sum(int(t['C'+str(r)]) for r in range(9,14)) == 12353
    teachers = int(t['C4'])
    assert t['A4'] == 'All Levels' and teachers == sum(int(t[c]) for c in ('C5','C8','C14')) == 29605
    assert [g['B'+str(r)] for r in (14,15,16)] == ['Secondary 3','Secondary 4','Secondary 5']
    totals = [int(g['C'+str(r)]) for r in (14,15,16)]
    assert totals == [int(a['L'+str(r)]) for r in (16,24,32)] == [39977,39611,1981]
    normal_technical = sum(int(a['L'+str(r)]) for r in (22,30))
    assert a['B22'] == a['B30'] == 'N(T)' and normal_technical == 9721
    assert 'Specialised Schools' in a['A34'] and 'after completing ISC' in a['A34']
    assert e['B23'] == 'Specialised' and e['S2'] == '2024'
    specialised = int(e['S23']); assert specialised == 2838
    total = sum(totals)
    minimum = total-specialised
    broader_minimum = total-normal_technical
    assert 0 < broader_minimum <= minimum <= total
    return dict(city='Singapore',mapping_year=2023,observations_year=2024,
        isced_programme_codes={'Secondary 3-5 Normal':'343','Secondary 3-4 Express':'343','Junior Colleges':'444'},
        reported_secondary3_5_students=total,reported_normal_technical_secondary3_4=normal_technical,
        specialised_all_secondary_student_cap=specialised,
        students_interval=[minimum,total],broader_students_interval=[broader_minimum,total],
        teachers_interval=[0,teachers],secondary_classified_teachers_interval=[0,secondary_teachers],
        secondary_classified_utility_interval=[0,15*secondary_teachers/(15*secondary_teachers+minimum)],utility_interval=[0,15*teachers/(15*teachers+minimum)],
        broader_utility_interval=[0,15*teachers/(15*teachers+broader_minimum)],
        teacher_classification_note=t['A19'],teacher_part_time_note=t['A20'],
        special_programme_note=a['A34'],school_scope_note=a['A36'],
        source_cells={'mapping':'first sheet!A3,B14:R17','grades':'4!C14:C16 = 6!L16,L24,L32','technical':'6!L22,L30','specialised_cap':'21!S23','teacher_pool':'3!C4','secondary_classified_teacher_pool':'3!C8'},
        scope='Conditional entire reported MOE school Teacher pool and mapped secondary school courses; not all-city international/private-school coverage, actual upper-secondary teacher FTE, or an age14-18-only ratio.',
        all_city_unconditional_utility_interval=[0,1])

if __name__ == '__main__':
    result = extract()
    (ROOT/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
