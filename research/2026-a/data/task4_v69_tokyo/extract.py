"""Bound Tokyo special-needs upper-secondary coverage from official aggregate pools."""
import csv,hashlib,json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def cells(path,sheet='sheet1'):
    with ZipFile(path) as z:
        strings=[''.join(t.text or '' for t in list(s.findall('s:t',NS))+list(s.findall('s:r/s:t',NS))) for s in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        out={}
        for c in ET.fromstring(z.read('xl/worksheets/'+sheet+'.xml')).findall('.//s:c',NS):
            v=c.find('s:v',NS)
            if v is not None:out[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
        return out

def num(x):return int(x.replace(',','').strip())
def extract():
    for item in json.loads((ROOT/'manifest.json').read_text()):
        b=(ROOT/item['file']).read_bytes();assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
    raw=(ROOT/'gk25qv1011.csv').read_text(encoding='utf-8-sig')
    rows=list(csv.DictReader(raw.splitlines()))
    selected=[r for r in rows if r.get('西暦（年度）')=='2025' and r.get('地域階層')=='0' and r.get('地域')=='総数']
    assert len(selected)==1;r=selected[0]
    upper=num(r['在学者数／高等部（人）']);teachers=num(r['教員数（本務者）（人）'])
    assert (upper,teachers)==(6063,7018)
    assert num(r['在学者数（人）'])==sum(num(r['在学者数／'+stage+'（人）']) for stage in ['幼稚部','小学部','中学部','高等部'])==15868
    assert teachers==num(r['教員数（本務者）／男（人）'])+num(r['教員数（本務者）／女（人）'])
    assert '都外にある区立の学校を含んだ数値' in raw
    a=cells(ROOT/'soukatsu.xlsx');b=cells(ROOT/'ichiran1.xlsx');d=cells(ROOT/'ichiran2.xlsx')
    assert a['AB4']=='高等部' and a['AC5']=='本科' and a['AL5']=='専攻科'
    assert b['AC3']=='高等部' and b['AD4']=='本科' and b['AM4']=='専攻科'
    public=num(a['AB10']);advanced=sum(num(a[col+'10']) for col in ['AL','AM','AN'])
    assert public==num(b['AC87'])==5854 and advanced==sum(num(b[col+'87']) for col in ['AM','AN','AO'])==46
    assert public-advanced==sum(num(b[col+'87']) for col in ['AD','AE','AF','AG','AH','AI','AJ','AK','AL'])==5808
    # All prefecture-external municipal schools identified in the same-year public roster have zero high-department pupils.
    external=[]
    for row in range(9,89):
        address=d.get('AX'+str(row),'')
        if address.startswith(('千葉県','静岡県')):
            school_id=d['A'+str(row)]
            matches=[k for k,v in b.items() if k.startswith('A') and k[1:].isdigit() and v==school_id]
            assert len(matches)==1;student_row=matches[0][1:]
            assert num(b['AC'+student_row])==0
            external.append(dict(school_id=school_id,name=d['E'+str(row)],address=address,upper_students=0,student_cell='AC'+student_row,address_cell='AX'+str(row)))
    assert len(external)==3
    mapping=cells(ROOT/'isced2011_mapping_japan.xlsx','sheet3')
    for row,code in [(39,'344'),(46,'354'),(57,'444'),(62,'454')]:
        assert mapping['T'+str(row)]==code and 'Special Needs Education School' in mapping['G'+str(row)]
    assert mapping['C39']=='2019/2020'
    nlo,nhi=public-advanced,upper-advanced
    def total_csv(path,kind):
        text=path.read_text(encoding='utf-8-sig')
        assert '＊' not in text and '都外' not in text
        rs=[r for r in csv.DictReader(text.splitlines()) if r.get('西暦（年度）')=='2025' and r.get('地域階層')=='0' and r.get('種別')==kind]
        assert len(rs)==1
        return rs[0]
    ordinary=total_csv(ROOT.parent/'task4_v46_tokyo/gk25qv0711.csv','総数（国・公・私立）')
    integrated=total_csv(ROOT.parent/'task4_v47_tokyo_coverage/gk25qv0911.csv','総数（国・公立）')
    old_n=num(ordinary['生徒数（人）'])+num(integrated['後期課程／生徒数（人）'])
    old_t=num(ordinary['教員数（本務者）（人）']);old_pool=num(integrated['教員数（本務者）（人）'])
    assert (old_n,old_t,old_pool)==(306903,19446,555)
    N=[old_n+nlo,old_n+nhi];T=[old_t,old_t+old_pool+teachers]
    U=[15*T[0]/(N[1]+15*T[0]),15*T[1]/(N[0]+15*T[1])]
    return dict(city='Tokyo',observation_date='2025-05-01',mapping_reference='2019/2020',mapping_sheet='2021提出版Scope UOE (xl/worksheets/sheet3.xml)',
        special_high_department_total=upper,special_public_high_department=public,special_public_advanced=advanced,
        special_national_private_high_department_unclassified=upper-public,special_upper_students_interval=[nlo,nhi],
        special_all_stage_main_post_teacher_pool=teachers,special_upper_teacher_interval=[0,teachers],
        external_municipal_schools=external,
        expanded_students_interval=N,expanded_teachers_interval=T,expanded_utility_interval=U,
        source_cells={'all_ownership':'gk25qv1011.csv 2025 total row','public_high':'soukatsu!AB10 = ichiran1!AC87','public_advanced':'soukatsu!AL10:AN10 = ichiran1!AM87:AO87','mapping':'sheet3!G39/T39,G46/T46,G57/T57,G62/T62'},
        scope='Tokyo reported ordinary full/day-evening high schools, latter secondary-school course, plus special-needs honka. National/private advanced pupils and stage teacher allocation remain unknown. Teachers retain official main-post school headcount, not FTE or classroom-only teachers.',
        omitted=['correspondence schools','upper-secondary vocational-school courses','college-of-technology lower years','international schools outside these statutory categories'])
if __name__=='__main__':
    r=extract();(ROOT/'summary.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
