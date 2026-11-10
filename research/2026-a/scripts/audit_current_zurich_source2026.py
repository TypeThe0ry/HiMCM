"""Independently audit Zurich source captures, without changing the model.

From the repository root, run:
  UV_CACHE_DIR=/data/scratch/uv-cache uv run --with openpyxl==3.1.5 python research/2026-a/scripts/audit_current_zurich_source2026.py

Requires uv, openpyxl (provided by uv in its ephemeral environment), and
pdftotext; uv may need network access if the package is not cached.
"""
import csv,hashlib,json,pathlib,re,subprocess,sys,xml.etree.ElementTree as ET
from datetime import datetime
import openpyxl
R=pathlib.Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';B=R/'data/current_zurich_boundary2024';D=R/'data/current_zurich_source2026'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def require(v,label):
 if not v:raise RuntimeError(label)
# Verify protected model bindings and both copies of current paper dependencies.
snapshot=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];v=read(R/'results/current_paper_review/current_verification.json');extra={}
for k,n in [('additional_source_scope_sha256',22),('additional_figure_inputs_sha256',27),('additional_student_inputs_sha256',12),('additional_ai_inputs_sha256',6)]:
 require(len(v[k])==n,'supplementary binding count');extra.update(v[k])
require(len(snapshot)==548 and len(extra)==67 and len(v['current_files_sha256'])==7,'binding counts')
for p,h in {**snapshot,**extra}.items():require(sha(R/p)==h,'protected scientific input mismatch')
for p,h in v['current_files_sha256'].items():require(sha(P/p)==h and sha(G/'paper/current'/p)==h,'paper dependency mismatch')
# Verify all archived boundary bodies and extraction artifacts. No header values are emitted.
body_files=[]
for row in (B/'SHA256SUMS').read_text().splitlines():
 h,n=row.split(maxsplit=1);n=n.strip();require(sha(B/n)==h,'boundary digest mismatch');body_files.append(n)
for n in body_files:
 if (B/(n+'.headers')).exists():
  text=(B/(n+'.headers')).read_text(errors='replace');statuses=re.findall(r'^HTTP/\S+\s+(\d{3})',text,re.M);require(statuses and statuses[-1]=='200','boundary HTTP status');datetime.fromisoformat((B/(n+'.utc')).read_text().strip().replace('Z','+00:00'))
metadata=subprocess.check_output(['pdftotext','-layout',str(B/'metadata.raw'),'-'],text=True)
for phrase in ['2025-12','revisions up to the 1st January 2024','EuroBoundaryMap Version 2025','reference date of 01.01.2024']:require(phrase in metadata,'boundary metadata')
for code,category,name,geom in [('CH002C','C','Zurich (greater city)','Polygon'),('CH002F','F','Zurich','MultiPolygon')]:
 for shape in ['region-100k','label']:
  f=read(B/f'{code}-{shape}-4326-2024.geojson');require(f['crs']['properties']['name'].endswith('4326') and len(f['features'])==1,'geojson shape/crs');item=f['features'][0];p=item['properties'];require((p['URAU_CODE'],p['URAU_CATG'],p['URAU_NAME'])==(code,category,name),'geojson identity');require(item['geometry']['type']==('Point' if shape=='label' else geom),'geojson geometry')
  if code=='CH002C':require(p['FUA_CODE']=='CH002F','city/fua relationship')
w=openpyxl.load_workbook(B/'city-lau-2021.xlsx',read_only=True,data_only=True);rows=list(w['CITY_LAU2021'].iter_rows(values_only=True));sel=[r for r in rows[1:] if r[2]=='CH002C'];require(len(sel)==22 and any('CH_CH0261' in r for r in sel),'2021 city municipalities');require(any('CH007C' in r and 'CH002F' in r for r in rows[1:]),'Winterthur FUA association')
with (B/'city-lau-2021-CH002C.csv').open(newline='',encoding='utf-8') as f:actual=list(csv.reader(f))
normal=lambda r:['' if c is None else str(c) for c in r]
require(actual==[normal(r) for r in [rows[0],*sel]],'2021 CSV extraction')
# Verify current official FSO response bodies and independently extract workbook rows.
receipts=read(D/'retrievals.json');require(len(receipts)==5,'FSO receipt count')
for r in receipts:require(r['status']==200 and (D/r['file']).stat().st_size==r['bytes'] and sha(D/r['file'])==r['sha256'],'FSO response receipt')
workbook=openpyxl.load_workbook(D/'variable_list.xlsx',read_only=True,data_only=True);sheet=workbook['DE'];found=[]
for r in sheet.iter_rows(values_only=False):
 if r[0].value in ('TT1019V_zb','TT1020V_zb'):
  values=[c.value if c.value is not None else '' for c in r];
  while values and values[-1]=='':values.pop()
  found.append({'sheet':'DE','excel_row':str(r[0].row),'values':values})
require(found==read(D/'selected_variable_metadata.json'),'variable workbook extraction');description=found[0]['values'][3]
for phrase in ['ein Hinweg','ohne die Ausbildungspendlerinnen','Zu- und Binnenpendlerinnen','Stichprobe','15. Altersjahr','Privathaushalten']:require(phrase in description,'survey description')
# Parse all selected XML dimensions, attributes and values independently.
observations=[]
for obs in ET.parse(D/'zurich_worktime.xml').getroot().findall('.//{*}Obs'):
 out={}
 for node in obs.iter():
  tag=node.tag.rsplit('}',1)[-1]
  if tag=='Value' and node.get('id') is not None:out[node.get('id')]=node.get('value')
  elif tag=='ObsValue':out['value']=node.get('value')
  elif tag=='ObsDimension':out['time']=node.get('value')
 observations.append(out)
require(observations==read(D/'selected_observations.json') and len(observations)==12,'SDMX observations');require(all('null' not in r and r['ID_INDIC_DISPR']=='TT1019V_zb' and r['FREQ']=='A' for r in observations),'SDMX fields')
require({(r['ID_RAUM'],r['TIME_PERIOD'],r['STATISTICAL_OPERATION']) for r in observations}=={(g,t,o) for g in ['261901','261910','261920'] for t in ['2023','2024'] for o in ['OBS','CI']},'SDMX grid')
expected={'261901':('41.0244504880056','41.0491469488717'),'261910':('32.0986553841307','32.397798355318'),'261920':('36.5967153593001','36.7440821537823')}
for g,values in expected.items():
 for year,value in zip(('2023','2024'),values):require(next(r['value'] for r in observations if r['ID_RAUM']==g and r['TIME_PERIOD']==year and r['STATISTICAL_OPERATION']=='OBS')==value,'observation value')
ids={'261901','261910','261920','TT1019V_zb','CI'};codes=[]
for node in ET.parse(D/'current_structure.xml').getroot().findall('.//{*}Code'):
 if node.get('id') in ids:codes.append({'id':node.get('id'),'names':[{'lang':n.get('{http://www.w3.org/XML/1998/namespace}lang'),'text':n.text} for n in node.findall('{*}Name')]})
require(codes==read(D/'selected_structure.json') and len(codes)==5,'code labels')
labels={c['id']:{x['lang']:x['text'] for x in c['names']} for c in codes}
require(labels['261901']['en']=='Zurich: core city' and labels['261910']['en']=='Zurich: other agglomeration municipalities' and labels['261920']['en']=='Zurich: agglomeration','geographic labels')
portal=(D/'fso_city_portal.html').read_text();asset=(D/'data_asset.html').read_text();require(all(x in portal for x in ['STATPOP','STATENT','December 31','previous year']) and 'Agglomerationen 2020' in asset,'portal period/geography description')
# Verify protected bindings again after reading sources.
for p,h in {**snapshot,**extra}.items():require(sha(R/p)==h,'protected binding changed during audit')
for p,h in v['current_files_sha256'].items():require(sha(P/p)==h and sha(G/'paper/current'/p)==h,'paper changed during audit')
out={'status':'PASS','audit_script_sha256':sha(pathlib.Path(__file__)),'environment':{'python':sys.version.split()[0],'openpyxl':openpyxl.__version__},'boundary_hashes_checked':len(body_files),'FSO_receipts_checked':len(receipts),'selected_2021_city_laus':len(sel),'selected_FSO_workbook_rows':len(found),'SDMX_observations':len(observations),'core_bindings_checked':len(snapshot),'supplemental_bindings_checked':len(extra),'paper_compile_dependencies_each_copy':7,'primary_model_admissions':0,'scope':'2021 LAU association is not a verified 2024 membership. FSO current Swiss agglomerations are not automatically GISCO CH002C. General period shift and related indicator metadata do not establish the exact 39.9-minute observation join. CI operation values have no assumed unit, confidence level, or duration-bin interpretation.','source_hashes':{str(p.relative_to(R)):sha(p) for p in [B/'SHA256SUMS',D/'retrievals.json',D/'extract.py',D/'selected_observations.json',D/'selected_variable_metadata.json',D/'selected_structure.json']}}
O=R/'results/current_zurich_source_review';O.mkdir(exist_ok=True);(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':pass
