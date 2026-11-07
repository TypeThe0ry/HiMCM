from pathlib import Path
import json,hashlib,time,zipfile
from concurrent.futures import ThreadPoolExecutor
import requests
from pyproj import Transformer
H=Path(__file__).resolve().parent;v=json.loads((H.parent/'map_viewports.json').read_text());tr=Transformer.from_crs(3857,4326,always_xy=True)
UA={'User-Agent':'HiMCM-Research-Cartography/1.0 (bounded static research map extracts)'}
entries=[]
def fetch_ne(layer):
 url=f'https://naturalearth.s3.amazonaws.com/10m_physical/{layer}.zip';dest=H/(layer+'.zip')
 if not dest.exists():
  r=requests.get(url,headers=UA,timeout=60);r.raise_for_status();dest.write_bytes(r.content)
 with zipfile.ZipFile(dest) as z:z.extractall(H/layer)
 return dict(type='natural_earth',url=url,file=dest.name,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),retrieved_local_date='2026-11-07',license='public domain')
for layer in ['ne_10m_land','ne_10m_lakes']:
 entries.append(fetch_ne(layer));print('downloaded',layer,flush=True)
def bbox(b):
 x0,y0,x1,y1=b;w,s=tr.transform(x0,y0);e,n=tr.transform(x1,y1);return f'{s:.6f},{w:.6f},{n:.6f},{e:.6f}'
for city in ['Copenhagen','Toronto','Dubai','Shanghai']:
 full=next(r for r in v if r['city']==city and r['kind']=='full');detail=next(r for r in v if r['city']==city and r['kind']=='detail');bb=bbox(full['bounds']);dd=bbox(detail['bounds'])
 query=f'''[out:json][timeout:90];(
way["highway"~"^(motorway|trunk|primary|secondary)(_link)?$"]({bb});
way["waterway"~"^(river|canal)$"]({bb});
way["natural"="coastline"]({bb});
way["highway"~"^(tertiary|residential)(_link)?$"]({dd});
);out geom;'''
 qfile=H/(city.lower()+'.overpassql');qfile.write_text(query);dest=H/(city.lower()+'.json');errors=[]
 if dest.exists():d=json.loads(dest.read_text());url='cached'
 else:
  for url in ['https://overpass-api.de/api/interpreter','https://overpass.kumi.systems/api/interpreter']:
   try:
    r=requests.post(url,data={'data':query},headers=UA,timeout=110);r.raise_for_status();d=r.json()
    if d.get('remark'):raise ValueError(d['remark'])
    if not d.get('elements'):raise ValueError('empty response')
    dest.write_bytes(r.content);break
   except Exception as e:errors.append(str(e));print(city,url,type(e).__name__,str(e)[:140],flush=True)
  else:
   entries.append(dict(city=city,status='failed',errors=errors,query=qfile.name));(H/'manifest.json').write_text(json.dumps(entries,indent=2));continue
 counts={}
 for e in d['elements']:
  t=e.get('tags',{});kind=t.get('highway') or t.get('waterway') or t.get('natural','other');counts[kind]=counts.get(kind,0)+1
 entry=dict(type='osm_overpass',city=city,status='complete',file=dest.name,query=qfile.name,url=url,full_bbox=bb,detail_bbox=dd,sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),osm_timestamp=d.get('osm3s',{}).get('timestamp_osm_base'),elements=len(d['elements']),counts=counts,retrieved_local_date='2026-11-07',credit='© OpenStreetMap contributors',license='ODbL 1.0',errors_before_success=errors)
 entries.append(entry);(H/'manifest.json').write_text(json.dumps(entries,indent=2));print(city,entry['elements'],counts,flush=True)
(H/'manifest.json').write_text(json.dumps(entries,indent=2));print('DONE',flush=True)
