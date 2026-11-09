from pathlib import Path
import urllib.request,datetime,hashlib,json
D=Path(__file__).resolve().parent
SOURCES=[('m1_original.html','https://metro.waw.pl/metro-warszawskie/linia-m1/przebieg/'),('m2_original.html','https://metro.waw.pl/metro-warszawskie/linia-m2/przebieg/'),('network_plan_original.pdf','https://metro.waw.pl/wp-content/uploads/2026/02/PLAN-METRA_2.pdf'),('fire_service_2025_original.pdf','https://www.gov.pl/attachment/2b7775c0-aa52-487e-809a-66df1b991b59')]
def main():
 if (D/'retrievals.json').exists():raise SystemExit('Frozen originals already exist; acquire a new dated package instead of overwriting')
 rows=[]
 for name,url in SOURCES:
  started=datetime.datetime.now(datetime.timezone.utc).isoformat()
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 HiMCM research source verification'}),timeout=35) as r:
    body=r.read();(D/name).write_bytes(body);rows.append(dict(url=url,final_url=r.url,file=name,http_status=r.status,accessed_utc=started,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),response_headers=dict(r.headers)))
  except Exception as e:rows.append(dict(url=url,file=None,accessed_utc=started,error=repr(e)))
 (D/'retrievals.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n');print(json.dumps([{k:v for k,v in x.items() if k!='response_headers'} for x in rows],indent=2,ensure_ascii=False))
if __name__=='__main__':main()
