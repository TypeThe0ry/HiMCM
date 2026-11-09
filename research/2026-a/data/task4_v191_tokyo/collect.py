"""Save actual Toei provider responses; no inferred status or body for failures."""
from pathlib import Path
import urllib.request,datetime,hashlib,json
D=Path(__file__).resolve().parent
URLS=[('oedo_original.html','https://www.kotsu.metro.tokyo.jp/subway/oedo/'),('stationlist_original.csv','https://www.opendata.metro.tokyo.lg.jp/kotsu/subway/subway_branch_o_stationlist.csv'),('catalog_original.json','https://catalog.data.metro.tokyo.lg.jp/api/3/action/package_show?id=t000018d0000000027'),('media_guide2026_response_original.html','https://www.kotsu.metro.tokyo.jp/other/kanren/ad/pdf/media_guide_2026_02.pdf'),('api_catalog_original.html','https://spec.api.metro.tokyo.lg.jp/spec/t000018d0000000027-2911e010ab42b6f8fad459fc7dc10e83-0?lang=en')]
def fetch(name,url):
 rec=dict(file=name,url=url,requested_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25) as response:
   body=response.read();rec.update(http_status=response.status,final_url=response.url,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),content_type=response.headers.get('Content-Type'));(D/name).write_bytes(body)
   if b'/_Incapsula_Resource?' in body:rec['payload_classification']='Incapsula JavaScript access shell; not requested source content; no numerical use'
 except Exception as error:rec.update(http_status=getattr(error,'code',None),error=str(error),file=None)
 return rec
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=D);args=parser.parse_args();D=args.output_dir.resolve();D.mkdir(parents=True,exist_ok=True)
 if (D/'retrievals.json').exists() or any((D/name).exists() for name,_ in URLS):raise SystemExit('Refusing to overwrite a source snapshot; select an empty --output-dir')
 rows=[fetch(*x) for x in URLS];(D/'retrievals.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
