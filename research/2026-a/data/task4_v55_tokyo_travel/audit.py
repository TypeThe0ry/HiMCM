"""Audit the geography and school-stage dimensions of the official R3 table."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

def main():
    for source in json.loads((P/'manifest.json').read_text()):
        b=(P/source['file']).read_bytes()
        assert len(b)==source['bytes'] and hashlib.sha256(b).hexdigest()==source['sha256']
    with zipfile.ZipFile(P/'mean_duration_R3.xlsx') as z:
        strings=[''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',N)]
        rows=[]
        for row in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('m:sheetData/m:row',N):
            cells={}
            for c in row:
                v=c.find('m:v',N);value='' if v is None else v.text
                if c.get('t')=='s':value=strings[int(value)]
                cells[''.join(x for x in c.get('r') if x.isalpha())]=value
            rows.append(cells)
    header=rows[3]
    assert [header[c] for c in 'EFGH']==['平日／休日','都市','性別','目的種類']
    data=rows[4:]
    geographies=sorted({r['F'] for r in data if r.get('F')})
    assert len(geographies)==11 and '全国計' in geographies
    assert not any('東京' in r for r in geographies)
    example=next(r for r in data if r.get('A')=='1' and r.get('B')=='1' and r.get('C')=='1' and r.get('D')=='2')
    assert example['H']=='通学' and abs(float(example['R'])-26.844338168)<1e-10
    guide=subprocess.check_output(['pdftotext','-layout',str(P/'mlit_guide2024.pdf'),'-'],text=True)
    assert '東京区部' in guide and '稲城市' in guide and '青梅市' in guide
    assert '70 を下回る' in guide
    result=dict(survey_year=2021,guide_revision='2024-03',source_sheet='c001_R3',
                published_dimensions=[header[c] for c in 'EFGH'],geographies=geographies,
                exact_tokyo_city_row=False,current_upper_secondary_dimension=False,
                illustration_only=dict(geography=example['F'],sex=example['G'],purpose=example['H'],day=example['E'],mean_minutes=float(example['R']),
                    interpretation='Grouped major-metropolitan central cities, all school stages; not Tokyo high-school observation'),
                guide_notes=['Tokyo wards, Inagi and Ome are separate sampled geographies; not entire Tokyo metropolis census',
                             'Cross-table precision flag1 marks cells with fewer than70 trips; not a respondent denominator'],
                new_admitted_city_observations=0,decision='Preserve Tokyo travel interval; grouped school-trip means do not identify target geography or school stage')
    (P/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
