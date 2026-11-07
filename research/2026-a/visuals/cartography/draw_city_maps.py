from pathlib import Path
import json,zipfile,math,gzip
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection,LineCollection
from matplotlib.patches import PathPatch,Rectangle,ConnectionPatch
from matplotlib.path import Path as MPath
from matplotlib.colors import ListedColormap,BoundaryNorm
from PIL import Image
from pyproj import Transformer,Geod
from shapely.geometry import box as sbox, LineString
from shapely.ops import transform
from shapely.geometry.polygon import orient
from cartopy.io.shapereader import Reader
H=Path(__file__).resolve().parent;B=H.parents[1];O=H/'figures';O.mkdir(exist_ok=True);V=H/'vector_data';DATA=B/'data/task4_access'
plt.rcParams.update({'font.family':['Times New Roman','Arial Unicode MS'],'font.size':10,'axes.linewidth':.65,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
T=Transformer.from_crs(4326,3857,always_xy=True);INV=Transformer.from_crs(3857,4326,always_xy=True);GEOD=Geod(ellps='WGS84')
plans=json.loads((H/'map_viewports.json').read_text());locations=pd.read_csv(H/'candidate_city_locations.csv').set_index('city');existing=pd.read_csv(B/'results/task4_access_revision/learning_access_measures.csv').set_index('city')
PALETTE=['#416C83','#78A9A5','#BFCCAE','#E3C58D','#C58670'];C=ListedColormap(PALETTE);N=BoundaryNorm([0,1,2,3,4,5],5)
water='#E8F0F3';land='#F3F1EB';road='#8D9695';ink='#2B414E'
landshapes=list(Reader(V/'ne_10m_land/ne_10m_land.shp').geometries());lakeshapes=list(Reader(V/'ne_10m_lakes/ne_10m_lakes.shp').geometries());cache={};audit=[]

def projected_polys(geo):
 if geo.is_empty:return []
 if geo.geom_type=='Polygon':
  p=orient(geo,sign=1);rings=[np.asarray(p.exterior.coords)]+[np.asarray(q.coords) for q in p.interiors];paths=[]
  for xy in rings:
   codes=np.full(len(xy),MPath.LINETO,dtype=np.uint8);codes[0]=MPath.MOVETO;codes[-1]=MPath.CLOSEPOLY;paths.append(MPath(xy,codes))
  return [MPath.make_compound_path(*paths)]
 if hasattr(geo,'geoms'):
  return sum((projected_polys(g) for g in geo.geoms),[])
 return []
def load(city):
 if city in cache:return cache[city]
 pfull=next(p for p in plans if p['city']==city and p['kind']=='full');pdetail=next(p for p in plans if p['city']==city and p['kind']=='detail');bb=pfull['bounds']
 lon0,lat0=INV.transform(bb[0],bb[1]);lon1,lat1=INV.transform(bb[2],bb[3]);clip=sbox(lon0-.05,lat0-.05,lon1+.05,lat1+.05)
 natural={}
 for key,shapes in [('land',landshapes),('lakes',lakeshapes)]:
  out=[]
  for g in shapes:
   if not g.intersects(clip):continue
   clipped=g.intersection(clip);pg=transform(T.transform,clipped);out.extend(projected_polys(pg))
  natural[key]=out
 with zipfile.ZipFile(DATA/pfull['grid_zip']) as z:fs=json.loads(z.read('hexes.geojson'))['features']
 fs=[f for f in fs if f['properties']['population']>0];pop=np.array([f['properties']['population'] for f in fs]);time=np.array([f['properties']['c_f'] for f in fs]);valid=np.isfinite(time)&(time>0)
 assert valid.all(), 'Handle uncertain grid times before drawing'
 polygons=[]
 for f in fs:
  xy=np.array(f['geometry']['coordinates'][0]);xx,yy=T.transform(xy[:,0],xy[:,1]);polygons.append(np.column_stack([xx,yy]))
 classes=np.searchsorted([15,30,60,90],time,side='left');within30=float(pop[time<=30].sum()/pop.sum());over60=float(pop[time>60].sum()/pop.sum());assert np.isclose(within30,existing.loc[city,'learning_30min_population_share_lower'])
 raw=V/(city.lower()+'.json');osm=json.loads(raw.read_text() if raw.exists() else gzip.decompress(Path(str(raw)+'.gz').read_bytes()));assert 'remark' not in osm
 roads=[];minor=[];rivers=[];coasts=[]
 for e in osm['elements']:
  coords=e.get('geometry',[])
  if len(coords)<2:continue
  xy=np.array([[p['lon'],p['lat']] for p in coords if 'lat' in p and 'lon' in p]);
  if len(xy)<2:continue
  xx,yy=T.transform(xy[:,0],xy[:,1]);path=np.column_stack([xx,yy]);tags=e.get('tags',{});hw=tags.get('highway','')
  if hw:
   if hw in ['motorway','trunk','primary','secondary','motorway_link','trunk_link','primary_link','secondary_link']:roads.append(path)
   else:minor.append(path)
  if 'waterway' in tags:rivers.append(path)
  if tags.get('natural')=='coastline':coasts.append(path)
 stats={'city':city,'retained_populated_grids':len(fs),'retained_population':float(pop.sum()),'within_30_minutes_population_share':within30,'over_60_minutes_population_share':over60,'time_field':'c_f','thresholds_minutes':[15,30,60,90],'major_osm_ways':len(roads),'detail_minor_osm_ways':len(minor),'river_ways':len(rivers),'coastline_ways':len(coasts),'grid_times_all_positive_and_finite':bool(valid.all()),'source_osm_timestamp':osm.get('osm3s',{}).get('timestamp_osm_base')};audit.append(stats)
 cache[city]=dict(full=pfull,detail=pdetail,natural=natural,polygons=polygons,classes=classes,roads=roads,minor=minor,rivers=rivers,coasts=coasts,stats=stats)
 return cache[city]
def scale(ax,bb,city,detail=False,small=False):
 x0,y0,x1,y1=bb;xx=x0+(x1-x0)*.07;yy=y0+(y1-y0)*.075;lon,lat=INV.transform(xx,yy)
 target=(x1-x0)*math.cos(math.radians(lat))/1000*.18
 length=max(v for v in [.5,1,2,5,10,20,50] if v<=max(target,.5))
 elon,elat,_=GEOD.fwd(lon,lat,90,length*1000);ex,_=T.transform(elon,elat);dx=ex-xx
 ax.plot([xx,xx+dx],[yy,yy],color=ink,lw=1.3,zorder=9);dy=(y1-y0)*.008
 ax.plot([xx,xx],[yy-dy,yy+dy],color=ink,lw=.7,zorder=9);ax.plot([xx+dx,xx+dx],[yy-dy,yy+dy],color=ink,lw=.7,zorder=9)
 ax.text(xx+dx/2,yy+(y1-y0)*.018,f'{length:g} km',ha='center',va='bottom',fontsize=11,color=ink,zorder=10,bbox=dict(fc='white',ec='none',alpha=.8,pad=.5))
 ax.annotate('N',xy=(.94,.94),xytext=(.94,.82),xycoords='axes fraction',ha='center',va='center',fontsize=11,color=ink,arrowprops=dict(arrowstyle='-|>',lw=.75,color=ink),zorder=10,bbox=dict(fc='white',ec='none',alpha=.8,pad=.5))
def visible_lines(lines,bb,kind):
 clip=sbox(*bb);tol=(bb[2]-bb[0])/1600*.25
 out=[]
 for p in lines:
  if p[:,0].max()<bb[0] or p[:,0].min()>bb[2] or p[:,1].max()<bb[1] or p[:,1].min()>bb[3]:continue
  g=LineString(p).intersection(clip).simplify(tol,preserve_topology=False)
  if g.is_empty:continue
  parts=list(g.geoms) if hasattr(g,'geoms') else [g]
  for q in parts:
   if q.geom_type=='LineString' and len(q.coords)>1:out.append(np.asarray(q.coords))
 return out
def draw(ax,city,kind='full',small=False):
 data=load(city).copy();bb=data[kind]['bounds'];ax.set_facecolor(water)
 # Clip and simplify context roads at sub-pixel tolerance; keep raw sources unchanged.
 for field in ['roads','minor','rivers','coasts']:data[field]=visible_lines(data[field],bb,kind)
 for p in data['natural']['land']:ax.add_patch(PathPatch(p,facecolor=land,edgecolor='#BDC7C8',lw=.35,zorder=0))
 for p in data['natural']['lakes']:ax.add_patch(PathPatch(p,facecolor=water,edgecolor='#B8C8CE',lw=.4,zorder=1))
 if data['coasts']:ax.add_collection(LineCollection(data['coasts'],colors='#A9BEC6',linewidths=.38,zorder=1.3))
 if data['rivers']:ax.add_collection(LineCollection(data['rivers'],colors='#ADC6D1',linewidths=.6 if kind=='detail' else .4,zorder=1.4))
 if data['roads']:ax.add_collection(LineCollection(data['roads'],colors='#BBC1BE',linewidths=.35,zorder=1.5))
 poly=data['polygons'];mask=np.array([p[:,0].max()>=bb[0] and p[:,0].min()<=bb[2] and p[:,1].max()>=bb[1] and p[:,1].min()<=bb[3] for p in poly]);pc=PolyCollection([p for p,m in zip(poly,mask) if m],array=np.asarray(data['classes'],float)[mask]+.5,cmap=C,norm=N,edgecolors='none',linewidths=0,alpha=.68 if kind=='full' else .48,zorder=3);ax.add_collection(pc)
 # Authentic roads remain visible over the overlay, with deliberately subordinate linework.
 if data['roads']:ax.add_collection(LineCollection(data['roads'],colors='#778A8A',linewidths=.30 if kind=='detail' else .18,alpha=.85,zorder=4))
 if kind=='detail' and data['minor']:ax.add_collection(LineCollection(data['minor'],colors='#81948F',linewidths=.23,alpha=.75,zorder=4))
 ax.set(xlim=(bb[0],bb[2]),ylim=(bb[1],bb[3]),aspect='equal',xticks=[],yticks=[])
 for sp in ax.spines.values():sp.set_edgecolor('#9EADB2');sp.set_linewidth(.65)
 scale(ax,bb,city,kind=='detail',small)
 return data,pc

def save(fig,name):
 for ext in ['pdf','svg','png']:fig.savefig(O/f'{name}.{ext}',bbox_inches='tight',pad_inches=.06,facecolor='white')
 plt.close(fig)
names=['Copenhagen','Toronto','Dubai','Shanghai'];captions=[]
for k,city in enumerate(names,2):
 if not (V/(city.lower()+'.json')).exists() and not (V/(city.lower()+'.json.gz')).exists():raise FileNotFoundError(city+' OSM data not ready')
 fig=plt.figure(figsize=(10.5,7.35));ax=fig.add_axes([.035,.12,.635,.78]);data,pc=draw(ax,city)
 detail=fig.add_axes([.705,.48,.27,.39]);draw(detail,city,'detail');detail.set_title('Selected neighbourhood detail',fontsize=11,pad=7,loc='left')
 bb=data['detail']['bounds'];ax.add_patch(Rectangle((bb[0],bb[1]),bb[2]-bb[0],bb[3]-bb[1],fill=False,ec='#3F515E',lw=1.0,zorder=8))
 # Connect the actual zoom rectangle to its geographical enlargement.
 fig.add_artist(ConnectionPatch(xyA=(bb[2],bb[3]),coordsA=ax.transData,xyB=(0,1),coordsB=detail.transAxes,color='#8B9DA5',lw=.6,zorder=0))
 fig.add_artist(ConnectionPatch(xyA=(bb[2],bb[1]),coordsA=ax.transData,xyB=(0,0),coordsB=detail.transAxes,color='#8B9DA5',lw=.6,zorder=0))
 fig.text(.035,.962,city,fontsize=21,color=ink);fig.text(.035,.924,'Learning-facility accessibility across retained populated grids',fontsize=11,color='#647982',fontstyle='italic')
 leg=fig.add_axes([.71,.115,.27,.265]);leg.axis('off');leg.set(xlim=(0,1),ylim=(0,1));leg.text(0,1,'Modelled walking time (min)',fontsize=11,color=ink,va='top')
 labels=['0–15','>15–30','>30–60','>60–90','>90']
 for j,(co,lab) in enumerate(zip(PALETTE,labels)):
  yy=.79-j*.125;leg.add_patch(Rectangle((0,yy),.10,.075,fc=co,ec='none'));leg.text(.15,yy+.036,lab,va='center',fontsize=11,color=ink)
 leg.plot([0,.10],[.12,.12],color='#81948F',lw=.7);leg.text(.15,.12,'Selected OSM roads',va='center',fontsize=11,color='#536871')
 s=data['stats'];fig.text(.71,.445,f"Within 30 min: {s['within_30_minutes_population_share']:.1%} population",fontsize=11,color=ink);fig.text(.71,.422,f"Over 60 min: {s['over_60_minutes_population_share']:.1%} population",fontsize=11,color=ink)
 fig.text(.035,.073,'Mean walking time to 20 nearby learning POIs · Population-weighted summaries',fontsize=11,color='#5B6D74')
 fig.text(.035,.050,'Five time classes · Urban population grids · Independent inset scale',fontsize=11,color='#5B6D74')
 fig.text(.98,.018,'© OpenStreetMap contributors · Natural Earth · Bruno et al. / SONY CSL',ha='right',fontsize=11,color='#61757D')
 name=f'{k:02d}_{city.lower()}_access';save(fig,name)
 captions.append({'file':name,'city':city,'caption':f'Learning-facility walking accessibility in {city}, using archived modelled mean travel times to the nearest 20 Learning POIs and retained all-age population grids. Grey roads provide current OpenStreetMap geographical context for the archived accessibility estimates. The full populated-grid footprint and selected detail use separate scales. Coverage follows the source urban-area dataset.','basemap':'OpenStreetMap selected road/water features and Natural Earth 10m land/lakes','projection':'EPSG:3857','source_style':'2023 Team 13904, PDF pp.11,20–22: muted geographical context, coloured network/coverage and enlarged detail.'})
 print('Rendered',city,flush=True)
# Consistent cross-city colour legend, with independent geographical scales explicitly shown.
fig,axs=plt.subplots(2,2,figsize=(10.3,9.8));fig.subplots_adjust(left=.03,right=.98,top=.92,bottom=.12,hspace=.14,wspace=.08)
for j,(ax,city) in enumerate(zip(axs.ravel(),names)):
 draw(ax,city,small=True);ax.set_title(f'({chr(97+j)})  {city}',loc='left',fontsize=12,pad=6)
fig.text(.035,.967,'City-scale patterns of learning-facility access',fontsize=17,color=ink)
handles=[Rectangle((0,0),1,1,fc=c,ec='none') for c in PALETTE];fig.legend(handles,['0–15','>15–30','>30–60','>60–90','>90'],title='Modelled walking time (min)',ncol=5,loc='lower center',bbox_to_anchor=(.5,.045),frameon=False,fontsize=11,title_fontsize=11,handlelength=1.4,columnspacing=1.7)
fig.text(.035,.028,'Shared time classes · City-specific scales · Populated urban grids',fontsize=11,color='#61757D')
fig.text(.98,.009,'© OpenStreetMap contributors · Natural Earth · Bruno et al. / SONY CSL',fontsize=11,ha='right',color='#61757D');save(fig,'06_city_access_comparison')
(H/'city_map_audit.json').write_text(json.dumps(audit,indent=2));(H/'city_map_captions.json').write_text(json.dumps(captions,indent=2))
print('All four city maps and comparison exported; population-share checks passed.')
