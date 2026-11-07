from fetch_satellite import *
import numpy as np
D={'Copenhagen':['2024-06-24','2024-06-25','2024-06-26','2024-06-27','2024-06-28'],'Toronto':['2024-10-16','2024-10-17','2024-10-18'],'Dubai':['2024-09-06','2024-09-07','2024-09-08'],'Shanghai':['2025-04-06','2025-04-07','2025-04-08']}
def get(t):
 p,d=t;q={'SERVICE':'WMS','VERSION':'1.1.1','REQUEST':'GetMap','LAYERS':'HLS_S30_Nadir_BRDF_Adjusted_Reflectance','STYLES':'','SRS':'EPSG:3857','BBOX':','.join(map(str,p['bounds'])),'WIDTH':768,'HEIGHT':724,'FORMAT':'image/png','TIME':d,'TRANSPARENT':'TRUE'}
 r=requests.get(URL,params=q,timeout=120);r.raise_for_status();im=Image.open(BytesIO(r.content));im.load();f=H/'cache'/f"hls_{p['city'].lower()}_{d}.png";f.write_bytes(r.content)
 return {'city':p['city'],'date':d,'path':str(f.relative_to(H)),'layer':q['LAYERS'],'request_url':r.url,'bounds':p['bounds'],'crs':'EPSG:3857','native_visualization_resolution_m':30,'sha256':hashlib.sha256(r.content).hexdigest(),'size':im.size,'mode':im.mode}
tasks=[(p,d) for p in plans for d in D[p['city']]]
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as ex:r=list(ex.map(get,tasks))
(H/'hls_candidates.json').write_text(json.dumps(r,indent=2));out=Image.new('RGB',(5*256,3*266),'#bbb');dr=ImageDraw.Draw(out)
for i,q in enumerate(r):
 x=i%5*256;y=i//5*266;im=Image.open(H/q['path']).convert('RGBA');im.thumbnail((256,242));out.paste(im,(x,y+24),im);dr.text((x+4,y+5),q['city']+' '+q['date'],fill='black')
out.save(H/'cache/hls_contact.jpg')
