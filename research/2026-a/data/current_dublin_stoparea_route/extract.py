#!/usr/bin/env python3
"""Verify archived responses and extract source facts without network access."""
import hashlib, json
from pathlib import Path
P=Path(__file__).resolve().parent
m=json.loads((P/'manifest.json').read_text())
for r in m:
 if r.get('file'):
  body=(P/r['file']).read_bytes()
  assert len(body)==r['bytes'] and hashlib.sha256(body).hexdigest()==r['sha256'],r['file']
cat=json.loads((P/'nta_gtfs_catalogue.json').read_text())['result']
resources={x['name']:x['url'] for x in cat['resources']}
assert resources['GTFS'].endswith('/GTFS_All.zip')
assert resources['GTFS for Realtime Operators'].endswith('/GTFS_Realtime.zip')
assert all(next(x for x in m if x.get('file')==n)['status']==403 for n in ('gtfs_all_response.bin','gtfs_realtime_response.bin'))
examples=(P/'irish_netex_examples.html').read_text(encoding='windows-1252')
assert 'StopArea' in examples and 'STOP PLACE' in examples and 'QUAY' in examples
out={'catalogue_publisher':cat['organization']['title'],'catalogue_resources':{'GTFS':resources['GTFS'],'GTFS for Realtime Operators':resources['GTFS for Realtime Operators']},'download_statuses':{x['file']:x['status'] for x in m if x.get('file') in ('gtfs_all_response.bin','gtfs_realtime_response.bin')},'netex_example_terms_present':['StopArea','STOP PLACE','QUAY'],'hierarchy_observed':False,'city_boundary_checked':False,'service_dates_checked':False,'admitted_stop_count':None}
(P/'extract.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
