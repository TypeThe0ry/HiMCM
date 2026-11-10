"""Read-only extraction of archived OECD Oslo CITY/FUA PM2.5 model records."""
from pathlib import Path
import csv,hashlib,json,decimal,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
for name,r in json.loads((P/'receipts.json').read_text()).items():
 raw=(P/name).read_bytes();assert r['status']==200 and len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
with (P/'oslo_exposure.csv').open(newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==6 and {r['REF_AREA'] for r in rows}=={'NO001C','NO001F'} and {r['TIME_PERIOD'] for r in rows}=={'2021','2022','2023'}
for r in rows:assert r['FREQ']=='A' and r['MEASURE']=='PM25_POP_EXP' and r['UNIT_MEASURE']=='MCG_M3' and r['UNIT_MULT']=='0' and r['DECIMALS']=='1'
selected=[]
for r in sorted(rows,key=lambda x:(x['REF_AREA'],x['TIME_PERIOD'])):
 selected.append({'area':r['REF_AREA'],'territorial_level':r['TERRITORIAL_LEVEL'],'year':int(r['TIME_PERIOD']),'source_obs_value':r['OBS_VALUE'],'display_decimals':int(r['DECIMALS']),'rounded_one_decimal':str(decimal.Decimal(r['OBS_VALUE']).quantize(decimal.Decimal('.1'))),'status':r['OBS_STATUS']})
root=E.parse(P/'structure.xml').getroot();names={}
for c in root.findall('.//{*}Code'):
 if c.get('id') in ['NO001C','NO001F']:names[c.get('id')]=[x.text for x in c.findall('{*}Name') if x.get('{http://www.w3.org/XML/1998/namespace}lang')=='en']
assert names=={'NO001C':['Oslo'],'NO001F':['Oslo']}
xml=(P/'structure.xml').read_text();assert 'Plume Labs' in xml and 'GHS-POP' in xml
out={'status':'pass','dataflow':'OECD.CFE.EDS:DSD_FUA_ENV@DF_POLLUTION(1.2)','units':'micrograms per cubic metre','rows':selected,'source_area_labels':names,'latest_returned_year':2023,'returned_2024_rows':0,'primary_admissions':0,'actual_primary_width_reduction':0,'scope':'Targeted API result only: annual CITY/FUA model exposure has no2024row here. Matching rounded2023FUA7.9 is not proof of the original2024 point source. Plume Labs grids/GHS-POP weights are publisher metadata; Oslo boundary and population-grid vintages unverified.'}
print(json.dumps(out,ensure_ascii=False,indent=2))
