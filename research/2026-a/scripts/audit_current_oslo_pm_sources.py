"""Read-only source and scope audit of Oslo PM2.5 follow-up."""
from pathlib import Path
import csv,hashlib,json,subprocess,sys,xml.etree.ElementTree as E
from decimal import Decimal
from task4_audit_output import audit_parser,check_output,emit_report
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';D=R/'data';O=R/'results/current_oslo_pm_source_review/verification.json'
a=audit_parser(__doc__).parse_args();check_output(a,O,G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
core=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];v=read(R/'results/current_paper_review/current_verification.json');extra={}
for k,d in v.items():
 if k.startswith('additional_') and k.endswith('_sha256'):extra.update(d)
assert len(core)==548 and len(extra)==77
for n,h in {**core,**extra,**v['withdrawal_source_sha256']}.items():assert sha(R/n)==h,n
for n,h in v['current_files_sha256'].items():assert sha(P/n)==sha(G/'paper/current'/n)==h,n
sources=[];success=failed=0
for name,manifest in [('current_oslo_pm_stations','retrievals.json'),('current_oslo_pm_model','receipts.json')]:
 p=D/name;r=read(p/manifest);items=r.items() if isinstance(r,dict) else [(x['file'],x) for x in r]
 for file,row in items:
  raw=(p/file).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
  success+=row['status']==200;failed+=row['status']!=200
 sources.extend(sorted(x for x in p.iterdir() if x.is_file()))
p=D/'current_oslo_pm_stations';j=read(p/'annual_2024.json');assert j['id']==['ContentsCode','lokalitet','år','statistikkvariabel'] and j['size']==[1,20,1,1]
assert list(j['dimension']['år']['category']['label'].values())==['2024'] and list(j['dimension']['statistikkvariabel']['category']['label'].values())==['µg/m3']
valid=sum(x is not None for x in j['value']);assert len(j['value'])==20 and valid==12
assert {str(i) for i,x in enumerate(j['value']) if x is None}==set(j['status']) and set(j['status'].values())=={'.'}
assert 'mindre enn 75 % datadekning' in '\n'.join(j['note'])
selected=read(p/'selected_2024.json');assert json.loads(subprocess.check_output([sys.executable,str(p/'extract.py')],text=True))==selected
for row in selected['rows']:
 i=j['dimension']['lokalitet']['category']['index'][row['station_code']]
 assert row['station_name']==j['dimension']['lokalitet']['category']['label'][row['station_code']] and row['reported_annual_pm25_ugm3']==j['value'][i]
p=D/'current_oslo_pm_model'
with (p/'oslo_exposure.csv').open(newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==6 and {r['TIME_PERIOD'] for r in rows}=={'2021','2022','2023'}
lookup={(r['REF_AREA'],r['TIME_PERIOD']):r for r in rows};assert len(lookup)==6
assert lookup['NO001C','2023']['OBS_VALUE']=='8.506857989031039' and lookup['NO001F','2023']['OBS_VALUE']=='7.934470167063854'
for row in rows:assert row['MEASURE']=='PM25_POP_EXP' and row['UNIT_MEASURE']=='MCG_M3' and row['UNIT_MULT']=='0' and row['DECIMALS']=='1' and row['FREQ']=='A' and row['TERRITORIAL_LEVEL']==('CITY' if row['REF_AREA']=='NO001C' else 'FUA')
assert Decimal(lookup['NO001F','2023']['OBS_VALUE']).quantize(Decimal('.1'))==Decimal('7.9')
xml=E.parse(p/'structure.xml').getroot();metadata=' '.join(x.text or '' for x in xml.iter());assert 'Plume Labs' in metadata and 'GHS-POP' in metadata
assert json.loads(subprocess.check_output([sys.executable,str(p/'extract.py')],text=True))==read(p/'selected.json')
with (D/'task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig',newline='') as f:original=next(r for r in csv.DictReader(f) if r['city']=='Oslo')
assert original['pm25_ugm3']=='7.9' and original['pm25_ugm3_year']=='2024' and original['pm25_ugm3_flag']=='MODELLED'
assert success==5 and failed==2
sources.extend([Path(__file__),R/'scripts/task4_audit_output.py'])
report={'status':'pass','successful_archived_responses':success,'failed_endpoint_responses':failed,'station_cells':20,'reported_station_values':12,'missing_station_values':8,'OECD_rows':6,'OECD_latest_returned_year':2023,'original2024source_lineage_verified':False,'primary_admissions':0,'actual_primary_width_reduction':0,'core_bindings_checked':548,'supplemental_bindings_checked':77,'manuscript_withdrawal_binding_entries':len(v['withdrawal_source_sha256']),'paper_dependencies_each_copy':7,'source_sha256':{str(p.relative_to(R)):sha(p) for p in sources},'scope':'Station annual means and OECD city/FUA model estimates have different statistical units. A rounded2023FUA match does not identify the original2024point; neither station averages nor a replacement model input are created.'}
emit_report(report,a,O,G)
