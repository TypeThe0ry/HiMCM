"""Offline OECD codebook field audit. Python standard library only."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import csv,hashlib,json,re
P=Path(__file__).resolve().parent
source=P/'pisa2022_codebook.xlsx'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with ZipFile(source) as z:
    ss=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml'))]
    rows=[]; current=''
    for r in E.fromstring(z.read('xl/worksheets/sheet6.xml')).findall('.//m:row',ns):
        d={}
        for c in r.findall('m:c',ns):
            v=c.find('m:v',ns); t='' if v is None else v.text
            d[re.sub('[0-9]','',c.attrib['r'])]=ss[int(t)] if c.attrib.get('t')=='s' and t else t
        if d.get('A'): current=d['A']
        rows.append({'row':r.attrib['r'],'variable':current,'is_variable':bool(d.get('A')),'cells':d})
fields=[r for r in rows if r['is_variable']]
selected=[r for r in rows if (r['variable'] in ['REGION','SUBNATIO','STRATUM'] and any(x in str(r['cells']) for x in ['TUR','Türkiye','Istanbul','İstanbul'])) or (r['is_variable'] and re.search(r'commut|travel|way to school|distance|transport',str(r['cells']),re.I))]
(P/'field_audit.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
with (P/'student_variable_labels.csv').open('w') as f:
    w=csv.writer(f);w.writerow(['excel_row','variable','label'])
    w.writerows((r['row'],r['variable'],r['cells'].get('B','')) for r in fields)
assert any(r['variable']=='ST265Q01JA' for r in selected)
assert any(r['variable']=='REGION' and '79200' in str(r['cells']) for r in selected)
assert not any('istanbul' in str(r).lower() or 'İstanbul' in str(r) for r in rows)
manifest={'source_url':'https://webfs.oecd.org/pisa2022/CY08MSP_CODEBOOK_27thJune24.xlsx','file':source.name,'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'bytes':source.stat().st_size,'student_sheet':'CY08MSP_STU_QQQ / xl/worksheets/sheet6.xml','variable_rows':len(fields),'retrieved':'2026-11-07'}
(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: archived OECD workbook parsed; student labels and exact geography/commute candidates extracted;',len(fields),'variable rows')
