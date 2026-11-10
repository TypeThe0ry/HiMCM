import pathlib,urllib.parse,urllib.request,urllib.error,json,hashlib,datetime,io
import numpy as np
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2];p=root/'visuals/current_spatial';out=p/'oslo_imagery_manifest.json'
if out.exists():raise SystemExit('Immutable archive already exists')
bb=next(x['bounds_3857'] for x in json.loads((p/'metrics.json').read_text()) if x['city']=='Oslo');results=[]
for date in ['2024-06-27','2024-06-22','2024-06-17']:
 q={'SERVICE':'WMS','VERSION':'1.1.1','REQUEST':'GetMap','LAYERS':'HLS_S30_Nadir_BRDF_Adjusted_Reflectance','STYLES':'','SRS':'EPSG:3857','BBOX':','.join(map(str,bb)),'WIDTH':1000,'HEIGHT':800,'FORMAT':'image/png','TIME':date,'TRANSPARENT':'TRUE'};url='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi?'+urllib.parse.urlencode(q);rec={'city':'Oslo','requested_date':date,'product_date':'WMS request date; actual granule acquisition not verified','url':url,'bounds_3857':bb,'retrieval_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-research'}),timeout=35);b=r.read();im=Image.open(io.BytesIO(b)).convert('RGBA');a=np.asarray(im);path=p/'imagery'/f'oslo_{date}.png';path.write_bytes(b);rec.update(http_status=r.status,headers=dict(r.headers),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),path=str(path.relative_to(p)),alpha_coverage=float((a[:,:,3]>0).mean()),pixels=list(im.size))
 except (urllib.error.URLError,TimeoutError,OSError) as e:rec['error']=repr(e)
 results.append(rec)
 if rec.get('alpha_coverage',0)>.9:break
out.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
