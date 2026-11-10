from pathlib import Path
import json,zipfile,hashlib,math,datetime,io,concurrent.futures
import numpy as np
from PIL import Image,ImageDraw
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import Normalize,LinearSegmentedColormap
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
P=Path(__file__).resolve().parent; ROOT=P.parents[3]; DATA=ROOT/'research/2026-a/data/task4_access'
URL='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi'; LAYER='HLS_S30_Nadir_BRDF_Adjusted_Reflectance'
CITIES={'Oslo':('6494',['2024-06-27','2024-06-22','2024-06-17']),'Zurich':('9808',['2024-06-27','2024-06-22','2024-06-17'])}
R=6378137
def project(lon,lat): return (R*math.radians(lon),R*math.log(math.tan(math.pi/4+math.radians(lat)/2)))
manifest=json.loads((DATA/'manifest.json').read_text()); records=[]; cities={}
for city,(id,dates) in CITIES.items():
 f=(DATA/f'{id}_hexes.zip') if city=='Zurich' else ROOT/'research/2026-a/data/current_oslo_spatial/6494_hexes.zip'; expected=next(x['sha256'] for x in manifest if x['file']==f.name) if city=='Zurich' else json.loads((f.parent/'download.json').read_text())['sha256']; actual=hashlib.sha256(f.read_bytes()).hexdigest(); assert actual==expected
 fs=json.loads(zipfile.ZipFile(f).read('hexes.geojson'))['features']; polys=[]; vals=[]; pops=[]; coords=[]
 for feature in fs:
  p=feature['properties']; pop=p['population']; t=p['c_f']; assert pop is not None and math.isfinite(pop) and pop>=0
  poly=[project(*xy[:2]) for xy in feature['geometry']['coordinates'][0]]; coords+=poly
  if pop>0: polys.append(poly); vals.append(t); pops.append(pop)
 if city=='Oslo':
  assert all(10.3 < x/(R*math.pi/180) < 11.1 and 59.5 < math.degrees(2*math.atan(math.exp(y/R))-math.pi/2) < 60.5 for x,y in coords)
  assert abs(sum(pops)-686862.09)<.02
 vals=np.array(vals); pops=np.array(pops); good=np.isfinite(vals)&(vals>0); xs,ys=np.array(coords).T; dx=xs.max()-xs.min();dy=ys.max()-ys.min(); pad=.06; bounds=[float(xs.min()-dx*pad),float(ys.min()-dy*pad),float(xs.max()+dx*pad),float(ys.max()+dy*pad)]
 cities[city]=dict(polys=polys,vals=vals,pops=pops,good=good,bounds=bounds)
 records.append(dict(city=city,zip=str(f.relative_to(ROOT)),sha256=actual,total_cells=len(fs),populated_cells=len(pops),retained_residents=float(pops.sum()),valid_residents=float(pops[good].sum()),unknown_residents=float(pops[~good].sum()),within_30_residents=float(pops[good & (vals<=30)].sum()),within_30_share_of_valid=float(pops[good & (vals<=30)].sum()/pops[good].sum()),max_valid_minutes=float(vals[good].max()),bounds_3857=bounds))
(P/'metrics.json').write_text(json.dumps(records,indent=2))
import csv
fields=['city','total_cells','populated_cells','retained_residents','valid_residents','unknown_residents','within_30_residents','within_30_share_of_valid','max_valid_minutes']
with (P/'metrics.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows({k:r[k] for k in fields} for r in records)
if __name__=='__main__':
 # Archive reuse is deliberately offline. New acquisitions require a new directory.
 manifest_path=P/'imagery_manifest.json'
 if not manifest_path.exists(): raise SystemExit('Missing archive manifest; acquire into a new directory, never overwrite this archive.')
 results=json.loads(manifest_path.read_text())
 for rec in results:
  if 'path' in rec:
   f=P/rec['path']
   if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=rec['sha256']:
    raise SystemExit(f'Archive missing or SHA-256 mismatch: {f}')
 for rec in json.loads((P/'oslo_imagery_manifest.json').read_text()):
  if 'path' in rec: assert hashlib.sha256((P/rec['path']).read_bytes()).hexdigest()==rec['sha256']
 print('Verified archived HLS responses; no network requests made.')
