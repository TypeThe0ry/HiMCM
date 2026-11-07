"""Locate actual November2024 predecessor workforce row; do not impute successor."""
from pathlib import Path
import json,hashlib,zipfile,re,csv,xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parent
SRC=ROOT.parent/'task4_v36_london'
m=next(m for m in json.loads((SRC/'manifest.json').read_text()) if m['file']=='workforce.xlsx')
raw=(SRC/'workforce.xlsx').read_bytes();assert hashlib.sha256(raw).hexdigest()==m['sha256'] and len(raw)==m['bytes']
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
rows=[]
with zipfile.ZipFile(SRC/'workforce.xlsx') as z:
 strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 book=E.fromstring(z.read('xl/workbook.xml'));assert len(book.findall('.//m:sheet',ns))==1
 root=E.fromstring(z.read('xl/worksheets/sheet1.xml'));head={}
 for row in root.findall('.//m:row',ns):
  vals={}
  for c in row:
   v=c.find('m:v',ns)
   if v is not None:vals[re.sub(r'\d','',c.attrib['r'])]=strings[int(v.text)] if c.attrib.get('t')=='s' else v.text
  if row.attrib['r']=='1':assert any('November 2024' in s for s in vals.values())
  if row.attrib['r']=='9':head=vals
  elif int(row.attrib['r'])>=10:rows.append({head[k]:v for k,v in vals.items() if k in head})
lookup={r['URN']:r for r in rows if 'URN' in r}
assert len(lookup)==len(rows)
for urn in ['150889','135584','134369','137928','100847','100799','102544']:assert urn not in lookup
with (SRC/'school_match.csv').open() as f:
 current=next(r for r in csv.DictReader(f) if r['urn']=='150889')
assert float(current['upper_students'])==181 and current['_merge']=='left_only'
r=lookup['100642']
keep=['URN','School Name','LAEstab','School Phase','School Type','Total Number of Teachers (Headcount)','Total Number of Teachers (Full-Time Equivalent)']
selected={k:v for k,v in r.items() if k in keep or k=='Total Number of Teachers (FTE)'}
assert selected['School Name']=='London Nautical School'
result=dict(source_file='../task4_v36_london/workforce.xlsx',source_sha256=m['sha256'],workforce_census='November 2024',predecessor_row=selected,current_urn='150889',current_year12_13_pupils=181,direct_match_added=0,conditional_continuity_only=True,remaining_other_unmatched_urns=['135584','134369','137928'])
(ROOT/'predecessor_row.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
