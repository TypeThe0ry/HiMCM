"""Verify archived official workbook; extract Nairobi enrollment without imputing teachers."""
import hashlib,json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def extract():
    for entry in json.loads((ROOT/'manifest.json').read_text()):
        raw=(ROOT/entry['file']).read_bytes()
        assert len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256']
    result={}
    with ZipFile(ROOT/'knbs2025_education.xlsx') as z:
        strings=[''.join(x.itertext()) for x in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rels={r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        for sheet in ET.fromstring(z.read('xl/workbook.xml')).find('s:sheets',NS):
            name=sheet.attrib['name']
            if name not in ['TAB 15.6','TAB 15.4b','TAB 15.1_15.3']:continue
            target=rels[sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
            path=target.lstrip('/') if target.startswith('/') else 'xl/'+target
            cells={}
            for cell in ET.fromstring(z.read(path)).findall('.//s:c',NS):
                v=cell.find('s:v',NS)
                if v is not None:cells[cell.attrib['r']]=strings[int(v.text)] if cell.attrib.get('t')=='s' else v.text
            result[name]=cells
    sec=result['TAB 15.6'];jun=result['TAB 15.4b']
    assert sec['A51'].strip()=='Nairobi City' and sec['H4']=='2024*'
    assert jun['A51'].strip()=='Nairobi City' and jun['C4']=='2024*'
    data=dict(city='Nairobi',year=2024,status='enrollment_only_teacher_missing_not_admitted',
        secondary_students=int(sec['H51']),secondary_cell='TAB 15.6!H51',
        junior_students_not_in_secondary=int(jun['C51']),junior_cell='TAB 15.4b!C51',
        teachers=None,ptr=None,utility_interval=[0,1],
        reason='County-specific secondary enrollment verified, but Table15.3 supplies national teacher totals only; no matching Nairobi teacher denominator.',
        secondary_table_notes={k:v for k,v in sec.items() if int(''.join(filter(str.isdigit,k)))>51})
    assert data['secondary_students']==129988 and data['junior_students_not_in_secondary']==158570
    (ROOT/'enrollment_observation.json').write_text(json.dumps(data,indent=2)+'\n')
    (ROOT/'teacher_table_extract.json').write_text(json.dumps(result['TAB 15.1_15.3'],indent=2)+'\n')
    print(json.dumps(data,indent=2))
if __name__=='__main__':extract()
