"""Archive the published 15min-City current-scenario files; never ideal-city simulations."""
from pathlib import Path
import requests,json,hashlib,concurrent.futures,zipfile,io
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/task4_access';OUT.mkdir(exist_ok=True)
BASE='https://whatif.sonycsl.it/15mincity/'
CITY_IDS={'Toronto':'8814','Phoenix':'6835','New York':'6245','Mexico City':'5707',
'Bogota':'1272','Sao Paulo':'7739','Santiago':'7724','Copenhagen':'1958','London':'5076',
'Barcelona':'859','Warsaw':'9248','Athens':'550','Nairobi':'6047','Lagos':'4800',
'Cape Town':'1559','Dubai':'2406','Istanbul':'3639','Mumbai':'5927','Dhaka':'2238',
'Tokyo':'8774','Shanghai':'7912','Singapore':'8133','Jakarta':'3725','Melbourne':'5662',
'Delhi':'10043','Zurich':'9808','Vienna':'9127','Wuhan':'9340','Detroit':'2226'}

def get(item):
 city,cid=item;url=BASE+f'data/{cid}/hexes.zip';path=OUT/f'{cid}_hexes.zip'
 try:
  if not path.exists():
   r=requests.get(url,timeout=90);r.raise_for_status()
   with zipfile.ZipFile(io.BytesIO(r.content)) as z:json.loads(z.read('hexes.geojson'))
   path.write_bytes(r.content)
  raw=path.read_bytes()
  with zipfile.ZipFile(io.BytesIO(raw)) as z:d=json.loads(z.read('hexes.geojson'))
  record={'city':city,'source_id':cid,'url':url,'file':path.name,'bytes':len(raw),
          'sha256':hashlib.sha256(raw).hexdigest(),'cells':len(d['features']),
          'retrieved_local_date':'2026-11-07','status':'downloaded'}
 except Exception as e:record={'city':city,'source_id':cid,'url':url,'status':'failed','error':str(e)}
 print(city,record['status'],record.get('cells'),flush=True)
 return record

def main():
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:records=list(ex.map(get,CITY_IDS.items()))
 (OUT/'manifest.json').write_text(json.dumps(records,indent=2)+'\n')
 for name,url in [('platform_page.html',BASE+'15min.php?idcity=1958'),
                  ('paper_methods.html','https://arxiv.org/html/2408.03794v1')]:
  r=requests.get(url,timeout=40)
  if r.ok:(OUT/name).write_bytes(r.content)

if __name__=='__main__':main()
