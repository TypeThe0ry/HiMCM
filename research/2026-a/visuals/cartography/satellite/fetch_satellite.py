from pathlib import Path
import requests,json,hashlib,concurrent.futures
from PIL import Image,ImageDraw
from io import BytesIO
H=Path(__file__).resolve().parent
(H/'cache').mkdir(exist_ok=True)
plans=[p for p in json.loads((H.parent/'map_viewports.json').read_text()) if p['kind']=='full']
URL='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi'
def fetch(p,date):
 city=p['city'];q={'SERVICE':'WMS','VERSION':'1.1.1','REQUEST':'GetMap','LAYERS':'MODIS_Terra_CorrectedReflectance_TrueColor','STYLES':'','SRS':'EPSG:3857','BBOX':','.join(map(str,p['bounds'])),'WIDTH':768,'HEIGHT':724,'FORMAT':'image/png','TIME':date}
 f=H/'cache'/f'{city.lower()}_{date}.png'
 r=requests.get(URL,params=q,timeout=90);r.raise_for_status();im=Image.open(BytesIO(r.content));im.load();f.write_bytes(r.content)
 return {'city':city,'date':date,'path':str(f.relative_to(H)),'layer':q['LAYERS'],'request_url':r.url,'bounds':p['bounds'],'crs':'EPSG:3857','native_visualization_resolution_m':250,'sha256':hashlib.sha256(r.content).hexdigest(),'size':im.size}
if __name__=='__main__':
 tasks=[(p,d) for p in plans for d in ['2024-07-18','2024-08-12','2024-09-07']]
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex: records=list(ex.map(lambda x:fetch(*x),tasks))
 (H/'candidate_manifest.json').write_text(json.dumps(records,indent=2))
 out=Image.new('RGB',(3*384,4*386),'white');dr=ImageDraw.Draw(out)
 for i,r in enumerate(records):
  x=i%3*384;y=i//3*386;im=Image.open(H/r['path']).convert('RGB');im.thumbnail((384,362));out.paste(im,(x,y+24));dr.text((x+8,y+5),r['city']+' '+r['date'],fill='black')
 out.save(H/'cache/candidate_contact.jpg')
 print('Downloaded',len(records))
