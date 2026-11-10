#!/usr/bin/env python3
"""Acquire small primary-source receipts; reject unexpectedly large downloads."""
import datetime, hashlib, json
from pathlib import Path
import requests
P = Path(__file__).resolve().parent
SOURCES = [
 ('nta_gtfs_catalogue.json','https://data.gov.ie/api/3/action/package_show?id=nta-gtfs'),
 ('nta_developer_gtfs.html','https://developer.nationaltransport.ie/GTFS'),
 ('irish_netex_examples.html','https://netex.ie/examplesStop.htm'),
 ('irish_netex_spec.pdf','https://netex.ie/doc/EIRE_NP/NTA-NeTEx-1-Spec-2021.10.20-v1.0.pdf'),
 ('gtfs_all_response.bin','https://www.transportforireland.ie/transitData/Data/GTFS_All.zip'),
 ('gtfs_realtime_response.bin','https://www.transportforireland.ie/transitData/Data/GTFS_Realtime.zip'),
]
def main():
 records=[]
 for name,url in SOURCES:
  started=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:
   with requests.get(url,timeout=(10,30),stream=True) as r:
    size=int(r.headers.get('Content-Length') or 0)
    if size>5000000: raise ValueError(f'Content-Length {size} exceeds 5 MB acquisition cap')
    parts=[]; total=0
    for chunk in r.iter_content(65536):
     total+=len(chunk)
     if total>5000000: raise ValueError('Body exceeds 5 MB acquisition cap')
     parts.append(chunk)
    body=b''.join(parts); (P/name).write_bytes(body)
    records.append({'file':name,'url':url,'final_url':r.url,'utc':started,'status':r.status_code,'content_type':r.headers.get('Content-Type'),'content_length_header':r.headers.get('Content-Length'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()})
  except (requests.RequestException,ValueError) as e:
   records.append({'file':None,'url':url,'utc':started,'error':str(e)})
 (P/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__': main()
