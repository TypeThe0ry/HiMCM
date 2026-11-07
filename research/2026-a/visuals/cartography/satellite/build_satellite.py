"""Fetch selected NASA HLS browse imagery and draw registered city context panels."""
from pathlib import Path
import requests,json,hashlib,concurrent.futures,datetime
from io import BytesIO
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pyproj import Transformer,Geod
H=Path(__file__).resolve().parent
URL='https://gibs.earthdata.nasa.gov/wms/epsg3857/best/wms.cgi'
LAYER='HLS_S30_Nadir_BRDF_Adjusted_Reflectance'
DATES={'Copenhagen':'2024-06-27','Toronto':'2024-10-17','Dubai':'2024-09-04','Shanghai':'2025-04-07'}
PLANS=[p for p in json.loads((H.parent/'map_viewports.json').read_text()) if p['kind']=='full']
T=Transformer.from_crs(3857,4326,always_xy=True);F=Transformer.from_crs(4326,3857,always_xy=True);G=Geod(ellps='WGS84')

def fetch(p):
 city=p['city'];date=DATES[city];q={'SERVICE':'WMS','VERSION':'1.1.1','REQUEST':'GetMap','LAYERS':LAYER,'STYLES':'','SRS':'EPSG:3857','BBOX':','.join(map(str,p['bounds'])),'WIDTH':1200,'HEIGHT':1132,'FORMAT':'image/png','TIME':date,'TRANSPARENT':'TRUE'}
 f=H/'imagery'/f'{city.lower()}_{date}.png';f.parent.mkdir(exist_ok=True)
 req=requests.Request('GET',URL,params=q).prepare()
 if not f.exists():
  r=requests.get(URL,params=q,timeout=120);r.raise_for_status();Image.open(BytesIO(r.content)).verify();f.write_bytes(r.content)
 im=Image.open(f).convert('RGBA');a=np.asarray(im)
 assert a[:,:,3].mean()>250, f'Incomplete coverage: {city}'
 assert a[:,:,:3].std()>15, f'Blank image: {city}'
 x0,y0,x1,y1=p['bounds'];cx=(x0+x1)/2;cy=(y0+y1)/2;lon,lat=T.transform(cx,cy);lon2,lat2=T.transform(cx+(x1-x0)/1200,cy)
 return {'city':city,'date':date,'path':str(f.relative_to(H)),'layer':LAYER,'request_url':req.url,'bounds':p['bounds'],'crs':'EPSG:3857','source_product_pixel_m':30,'output_pixels':[1200,1132],'output_pixel_ground_m_at_center':G.inv(lon,lat,lon2,lat2)[2],'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'alpha_coverage_fraction':float((a[:,:,3]>0).mean()),'interpretation':'NASA GIBS rendered RGB browse image of HLS S30; visual geographical context','retrieval_date_utc':datetime.datetime.now(datetime.UTC).isoformat()}

def bar(ax,bb,km):
 x0,y0,x1,y1=bb;xx=x0+.07*(x1-x0);yy=y0+.08*(y1-y0);lon,lat=T.transform(xx,yy);lo2,la2,_=G.fwd(lon,lat,90,km*1000);end=F.transform(lo2,la2)[0]
 ax.plot([xx,end],[yy,yy],color='white',lw=3,solid_capstyle='butt');ax.text((xx+end)/2,yy+.025*(y1-y0),f'{km} km',ha='center',color='white',fontsize=12,bbox=dict(fc='#182b32',ec='none',alpha=.8,pad=2))

def render(records):
 plt.rcParams.update({'font.family':'Times New Roman','font.size':12,'pdf.fonttype':42,'svg.fonttype':'none'})
 fig,axs=plt.subplots(2,2,figsize=(8.3,9.4));fig.subplots_adjust(left=.035,right=.98,bottom=.08,top=.87,wspace=.08,hspace=.21)
 for ax,r,letter,km in zip(axs.flat,records,'abcd',[2,20,10,10]):
  bb=r['bounds'];im=Image.open(H/r['path']);ax.imshow(im,extent=[bb[0],bb[2],bb[1],bb[3]],interpolation='none');ax.set(xticks=[],yticks=[]);ax.set_title(f'({letter}) {r["city"]}  |  {r["date"]}',fontsize=12.5,loc='left',pad=9)
  for spine in ax.spines.values():spine.set_color('#81919a');spine.set_linewidth(.6)
  bar(ax,bb,km);ax.annotate('N',xy=(.94,.91),xytext=(.94,.77),xycoords='axes fraction',ha='center',color='white',fontsize=12,arrowprops=dict(arrowstyle='-|>',color='white',lw=1.2))
 fig.text(.035,.962,'Satellite context for city accessibility',fontsize=19,color='#263f4c')
 fig.text(.035,.922,'Sentinel-2 / HLS S30 · matched map extents · dated observations',fontsize=12,color='#526b76')
 fig.text(.035,.039,'NASA HLS / GIBS · 30 m source product · EPSG:3857 · city-specific scales',fontsize=11,color='#526b76')
 for ext in ['png','pdf','svg']:fig.savefig(H/f'07_satellite_city_context.{ext}',dpi=300,facecolor='white')
 plt.close(fig)

if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:records=list(ex.map(fetch,PLANS))
 (H/'manifest.json').write_text(json.dumps(records,indent=2));render(records);print('4 HLS scenes verified and rendered.')
