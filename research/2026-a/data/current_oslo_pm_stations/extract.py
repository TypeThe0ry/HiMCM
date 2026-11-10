"""Read-only extraction of Oslo's reported 2024 station annual PM2.5 cells."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
for r in json.loads((P/'retrievals.json').read_text()):
 raw=(P/r['file']).read_bytes();assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
 if r.get('request_body_file'):assert hashlib.sha256((P/r['request_body_file']).read_bytes()).hexdigest()==r['request_sha256']
m=json.loads((P/'metadata.json').read_text());q=json.loads((P/'query.json').read_text());assert q==json.loads((P/'request_body.json').read_text())
v=json.loads((P/'annual_2024.json').read_text());assert v['id']==['ContentsCode','lokalitet','år','statistikkvariabel'] and v['size']==[1,20,1,1]
assert list(v['dimension']['år']['category']['label'].values())==['2024'] and list(v['dimension']['statistikkvariabel']['category']['label'].values())==['µg/m3']
station=v['dimension']['lokalitet']['category'];rows=[]
for code,i in sorted(station['index'].items(),key=lambda x:x[1]):
 rows.append({'station_code':code,'station_name':station['label'][code],'year':2024,'reported_annual_pm25_ugm3':v['value'][i],'source_status':v.get('status',{}).get(str(i))})
assert len(rows)==20 and sum(r['reported_annual_pm25_ugm3'] is not None for r in rows)==12
notes=v['note'];assert any('75 %' in s for s in notes)
out={'status':'pass','table':'MIL032','source':v['source'],'updated':v['updated'],'stations_selected':20,'reported_values':12,'missing_values':8,'rows':rows,'source_notes':notes,'primary_admissions':0,'actual_primary_width_reduction':0,'scope':'Reported station-specific 2024 annual means, not a population-weighted city exposure. Missing cells are not zero: the source lists inactive station, no data or less than75%coverage. No station average or city exposure is manufactured; original modelled7.9 remains unlinked.'}
print(json.dumps(out,ensure_ascii=False,indent=2))
