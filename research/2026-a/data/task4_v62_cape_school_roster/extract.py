"""Read official school roster without conflating secondary and grades10–12."""
import json,hashlib,csv,re
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
raw=P/'western_cape_q3_2025.xlsx';m=json.loads((P/'manifest.json').read_text())
assert hashlib.sha256(raw.read_bytes()).hexdigest()==m['sha256']
with ZipFile(raw) as z:
 ss=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
 rows=[]
 for row in E.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('s:sheetData/s:row',ns):
  d={}
  for c in row:
   v=c.find('s:v',ns)
   if v is not None:d[re.sub('[0-9]','',c.attrib['r'])]=ss[int(v.text)] if c.attrib.get('t')=='s' else v.text
  rows.append(d)
header=rows[0];data=[{name:r.get(col,'') for col,name in header.items()} for r in rows[1:] if r.get('A','')]
city=[r for r in data if r['LMunName']=='CITY OF CAPE TOWN' and r['Status']=='OPEN']
assert len({r['NatEmis'] for r in city})==len(city)
summary=[]
for phase,sector in sorted({(r['Phase_PED'],r['Sector']) for r in city}):
 part=[r for r in city if r['Phase_PED']==phase and r['Sector']==sector]
 def count(k):return sum(float(r[k]) for r in part if r[k])
 summary.append(dict(phase=phase,sector=sector,schools=len(part),reported_learners_sum=count('Learners2025'),reported_educators_sum=count('Educators2025'),missing_learners=sum(not r['Learners2025'] for r in part),missing_educators=sum(not r['Educators2025'] for r in part),zero_learners=sum(r['Learners2025']=='0' for r in part),zero_educators=sum(r['Educators2025']=='0' for r in part)))
with (P/'city_phase_counts.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(summary[0]),lineterminator='\n');w.writeheader();w.writerows(summary)
with (P/'missing_count_schools.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['NatEmis','Official_Institution_Name','Phase_PED','Sector','Learners2025','Educators2025'],lineterminator='\n');w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in city if not r['Learners2025'] or not r['Educators2025'])
result=dict(source_sha256=m['sha256'],source_rows=len(data),open_city_schools=len(city),data_years=sorted({r['DataYear'] for r in city}),groups=summary,main_admitted=False,changed_model_cells=0,reason='School phase and whole-school counts do not identify grades10–12 enrollment or teacher assignment; roster completeness and zero semantics require verification.')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
