"""Prepare authoritative candidate matches and vector-map viewports.
CARTO raster placeholders were rejected; final maps use vector_data/ only.
"""
from pathlib import Path
import json,math,hashlib,zipfile
import numpy as np
import pandas as pd
import requests
from pyproj import Transformer
H=Path(__file__).resolve().parent;B=H.parents[1];DATA=B/'data/task4_access';CACHE=H/'basemap_cache';CACHE.mkdir(exist_ok=True)
manifest=json.loads((DATA/'manifest.json').read_text());index={str(r['id']):r for r in json.loads((DATA/'city_index.json').read_text())};team=pd.read_csv(B/'data/city_candidates_team_25.csv');matches={r['city']:r for r in manifest};rows=[]
for _,r in team.iterrows():
 source=matches[r.city];loc=index[str(source['source_id'])];rows.append({'city':r.city,'country':r.country,'region':r.region,'source_id':source['source_id'],'source_city':loc['city'],'latitude':float(loc['lat']),'longitude':float(loc['lon']),'coordinate_source':'Archived author city_index.json','source_grid_zip':source['file']})
assert len(rows)==25 and len({r['city'] for r in rows})==25
pd.DataFrame(rows).to_csv(H/'candidate_city_locations.csv',index=False)
provenance=[]
for layer in ['ne_110m_admin_0_countries','ne_50m_admin_0_countries']:
 scale=layer.split('_')[1];url=f'https://naturalearth.s3.amazonaws.com/{scale}_cultural/{layer}.zip';dest=CACHE/(layer+'.zip')
 if not dest.exists():
  response=requests.get(url,timeout=45,headers={'User-Agent':'HiMCM-Research-Cartography/1.0'});response.raise_for_status();dest.write_bytes(response.content)
 with zipfile.ZipFile(dest) as z:z.extractall(CACHE/layer)
 provenance.append({'type':'vector_basemap','url':url,'path':str(dest.relative_to(H)),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'retrieved_local_date':'2026-11-07','credit':'Made with Natural Earth','license':'Public domain'})
T=Transformer.from_crs(4326,3857,always_xy=True);plans=[]
for city in ['Copenhagen','Toronto','Dubai','Shanghai']:
 row=next(r for r in rows if r['city']==city)
 with zipfile.ZipFile(DATA/row['source_grid_zip']) as z:fs=json.loads(z.read('hexes.geojson'))['features']
 fs=[f for f in fs if f['properties'].get('population',0)>0];xy=np.concatenate([np.array(f['geometry']['coordinates'][0]) for f in fs]);xx,yy=T.transform(xy[:,0],xy[:,1]);lo=np.array([min(xx),min(yy)]);hi=np.array([max(xx),max(yy)]);center=(lo+hi)/2;span=(hi-lo)*1.12;aspect=1.06
 if span[0]/span[1]<aspect:span[0]=span[1]*aspect
 else:span[1]=span[0]/aspect
 bounds=[*(center-span/2),*(center+span/2)];cx,cy=T.transform(row['longitude'],row['latitude']);half=(2000 if city=='Copenhagen' else 10000)/math.cos(math.radians(row['latitude']));detail=[cx-half,cy-half,cx+half,cy+half]
 for kind,bb in [('full',bounds),('detail',detail)]:plans.append({'city':city,'kind':kind,'bounds':list(map(float,bb)),'center_lonlat':[row['longitude'],row['latitude']],'grid_zip':row['source_grid_zip'],'projection':'EPSG:3857','basemap':'OpenStreetMap vector_data and Natural Earth'})
(H/'basemap_manifest.json').write_text(json.dumps(provenance,indent=2));(H/'map_viewports.json').write_text(json.dumps(plans,indent=2))
print('25 coordinate matches, 8 vector viewports, Natural Earth basemaps prepared.')
