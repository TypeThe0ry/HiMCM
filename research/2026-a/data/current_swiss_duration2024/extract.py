"""Read-only extraction of archived national Swiss work-duration data (not city data)."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as E,zipfile
P=Path(__file__).resolve().parent
for row in json.loads((P/'retrievals.json').read_text()):
 raw=(P/row['file']).read_bytes()
 assert row['status']==200 and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(P/'duration.xlsx') as z:
 strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
 cells={}
 for c in E.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:c',ns):
  v=c.find('s:v',ns)
  if v is not None:cells[c.get('r')]=strings[int(v.text)] if c.get('t')=='s' else float(v.text)
 assert str(cells['AV3']).strip()=='2024'
 rows=[]
 for i in range(15,23):
  rows.append({'row':i,'label':cells['A'+str(i)],'count_or_mean':cells.get('AV'+str(i)),'reported_VI_percent':cells.get('AW'+str(i)),'share_percent':cells.get('AX'+str(i))})
 notes={str(i):cells['A'+str(i)] for i in [25,26,27,28,29,31,33]}
 report={'status':'pass','provider':'Swiss Federal Statistical Office','asset':'36351624','table':'T 11.4.4.3','sheet':'T 11.4.4.3','geography':'Switzerland (asset metadata Raumgliederung)','reference_year':2024,'selected_columns':{'count_or_mean':'AV','VI_percent':'AW','share_percent':'AX'},'rows':rows,'notes':notes,'primary_admissions':0,'actual_score_width_reduction':0,'decision':'National work-commuter survey; not Zurich CH002C incoming/internal work commuters or a matched city student distribution. Do not transfer national bins or mean to the retained city cell. Unknown-duration commuters are reported separately from known-duration shares; VI is not individual-duration support.'}
 print(json.dumps(report,ensure_ascii=False,indent=2))
