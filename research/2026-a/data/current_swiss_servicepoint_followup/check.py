#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
from bs4 import BeautifulSoup
D=Path(__file__).resolve().parent
R=D.parents[1]/'results/current_swiss_servicepoint_followup'
old=D.parent/'current_zurich_transport'
files=[D/'catalogue.json',D/'catalogue.json.receipt.json',D/'cookbook.html',D/'cookbook.html.receipt.json',D/'fot_stop_points.json',D/'fot_stop_points.json.receipt.json',old/'README.md',old/'provenance.json',old/'kanton_zh_wfs.geojson',D/'check.py',D/'fot_description.html',D/'fot_description.html.receipt.json']
for name in ['catalogue.json','cookbook.html','fot_stop_points.json','fot_description.html']:
 b=(D/name).read_bytes(); receipt=json.loads((D/(name+'.receipt.json')).read_text());assert hashlib.sha256(b).hexdigest()==receipt['sha256'] and len(b)==receipt['bytes']
assert json.loads((D/'catalogue.json.receipt.json').read_text())['http_status']==403
for name in ['cookbook.html','fot_stop_points.json','fot_description.html']: assert json.loads((D/(name+'.receipt.json')).read_text())['http_status']==200
fot_text=BeautifulSoup((D/'fot_description.html').read_text(),'html.parser').get_text(' ',strip=True)
assert 'additional operating points relevant for timetable planning' in fot_text and 'not suitable for regular, automatic data retrieval' in fot_text
j=json.loads((D/'fot_stop_points.json').read_text()); assert len(j['results'])==5
s=BeautifulSoup((D/'cookbook.html').read_text(),'html.parser').get_text(' ',strip=True)
for word in ('parentSloidServicePoint','stopPointType','freightServicePoint','operatingPointTrafficPointType','REVOKED','Europaplatz','validTo'): assert word in s,word
assert hashlib.sha256((old/'kanton_zh_wfs.geojson').read_bytes()).hexdigest()==json.loads((old/'provenance.json').read_text())['sha256']
root=D.parents[1]
out={'status':'pass bounded semantic and sample check','source_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'checks':{'receipts_match':True,'cookbook_terms_present':True,'fot_sample_rows':len(j['results']),'old_wfs_receipt_matches':True},'admitted_increase':0,'admitted_records':0,'interpretation':'bounded semantic and sample check; no city census or acceptance decision'}
R.mkdir(parents=True,exist_ok=True);(R/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out['checks']))
