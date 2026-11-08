"""Read original OOXML using standard library; preserve geography and staff scope."""
from pathlib import Path
import csv,hashlib,json,re,xml.etree.ElementTree as ET,zipfile
P=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def rows(path):
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None
        ss=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',NS)]
        result=[]
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:row',NS):
            d={}
            for c in row:
                v=c.find('s:v',NS);t=v.text if v is not None else ''
                d[re.sub('[0-9]','',c.attrib['r'])]=ss[int(t)] if c.get('t')=='s' else t
            result.append(d)
        return result

def extract():
    for r in json.loads((P/'manifest.json').read_text()):
        assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    pupils=rows(next(P.glob('DE_MATH*.xlsx')));staff=rows(next(P.glob('DE_EKPAID*.xlsx')))
    assert pupils[0]['A']=='Διεύθυνση' and staff[0]['A']=='Περιφέρεια'
    selected=[r for r in pupils[1:] if r.get('A')=='ΔΙΕΥΘΥΝΣΗ Δ.Ε. Α΄ ΑΘΗΝΑΣ']
    actual=[]
    for r in selected:
        assert sum(int(r.get(c) or 0) for c in 'DEFGHI')==int(r['J'])
        if r['B'] in ['Λύκεια','Επαγγελματικά Λύκεια']:
            n=int(r['J']);scope='whole lyceum row'
        else:
            n=sum(int(r.get(c) or 0) for c in 'EGI');scope='upper-secondary attached classes only'
        if n:actual.append({'directorate':r['A'],'school_family':r['B'],'school_type':r['C'],'upper_secondary_pupils':n,'scope':scope})
    attiki=[r for r in staff[1:] if 'ΑΤΤΙΚΗΣ' in r.get('A','')]
    assert any('ΕΙΔΙΚΟ ΒΟΗΘΗΤΙΚΟ ΠΡΟΣΩΠΙΚΟ' in r.get('C','') for r in attiki)
    assert any('Μειωμένου Ωραρίου' in v for v in staff[0].values())
    for r in attiki:
        assert sum(int(v or 0) for c,v in r.items() if c not in ['A','B','C','AC'])==int(r['AC'])
    result={'main_admitted':False,'new_admitted_cells':0,'academic_year':'2024/2025','release_directory_year':2026,'pupil_rows_excluding_header':len(pupils)-1,'staff_rows_excluding_header':len(staff)-1,'a_athens_directorate_rows':len(selected),'a_athens_selected_upper_secondary_pupils':sum(r['upper_secondary_pupils'] for r in actual),'a_athens_component_rows':actual,'attiki_personnel_specialty_rows':len(attiki),'attiki_listed_personnel_including_support':sum(int(r['AC']) for r in attiki),'municipality_resolved':False,'staff_is_verified_teacher_headcount':False,'staff_is_fte':False,'private_coverage_verified':False,'reason_not_admitted':'Pupils grouped by education directorate; personnel grouped by region and include support staff and different employment modes. No city school linkage, no upper-secondary-only teacher split, no complete public/private coverage definition. Cannot pair with historical2018/2019 pupils.'}
    return result
if __name__=='__main__':
    x=extract();(P/'summary.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');print(json.dumps(x,ensure_ascii=False,indent=2))
