"""Read-only extraction of archived FSO source metadata and selected SDMX data."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as E,zipfile
O=Path(__file__).resolve().parent;ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for r in json.loads((O/'retrievals.json').read_text()):
 if r.get('file'):assert r['status']==200 and sha(O/r['file'])==r['sha256'] and (O/r['file']).stat().st_size==r['bytes']
selected=[]
with zipfile.ZipFile(O/'variable_list.xlsx') as z:
 strings=[''.join(n.itertext()) for n in E.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si',ns)]
 sheets=E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns);sheet_name=sheets[1].get('name')
 for r in E.fromstring(z.read('xl/worksheets/sheet2.xml')).findall('.//s:row',ns):
  vals=[]
  for c in r.findall('s:c',ns):
   v=c.find('s:v',ns);txt='' if v is None else v.text
   if c.get('t')=='s':txt=strings[int(txt)]
   vals.append(txt or '')
  if vals and vals[0] in ['TT1019V_zb','TT1020V_zb']:selected.append(dict(sheet=sheet_name,excel_row=r.get('r'),values=vals))
assert len(selected)==2 and selected[0]['values'][0]=='TT1019V_zb'
(O/'selected_variable_metadata.json').write_text(json.dumps(selected,ensure_ascii=False,indent=2)+'\n')
root=E.parse(O/'current_structure.xml').getroot();codes=[]
for c in root.findall('.//{*}Code'):
 if c.get('id') in ['261901','261910','261920','TT1019V_zb','CI']:
  codes.append(dict(id=c.get('id'),names=[dict(lang=n.get('{http://www.w3.org/XML/1998/namespace}lang'),text=n.text) for n in c.findall('{*}Name')]))
(O/'selected_structure.json').write_text(json.dumps(codes,ensure_ascii=False,indent=2)+'\n')
rows=[]
for obs in E.parse(O/'zurich_worktime.xml').getroot().findall('.//{*}Obs'):
 row={}
 for x in obs.iter():
  if x.tag.endswith('ObsValue'):row['value']=x.get('value')
  elif x.tag.endswith('ObsDimension'):row['time']=x.get('value')
  elif x.tag.endswith('Value') and x.get('id'):row[x.get('id')]=x.get('value')
 rows.append(row)
assert len(rows)==12 and {r['ID_RAUM'] for r in rows}=={'261901','261910','261920'} and {r['TIME_PERIOD'] for r in rows}=={'2023','2024'}
assert all(r['ID_INDIC_DISPR']=='TT1019V_zb' for r in rows)
(O/'selected_observations.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps({'metadata_rows':len(selected),'SDMX_observations':len(rows),'primary_admissions':0}))
