"""Independently verify source grid statistics and current spatial illustration."""
import datetime,hashlib,json,math,pathlib,re,zipfile,xml.etree.ElementTree as E
from urllib.parse import urlparse,parse_qs
from PIL import Image
R=pathlib.Path(__file__).resolve().parents[1]; V=R/'visuals/current_spatial';P=R.parents[1];D=R/'data/current_oslo_spatial'; O=R/'results/current_oslo_spatial_review'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];assert len(old)==548
commute=read(R/'results/current_oslo_commute_scope/summary.json')['source_sha256'];cv=read(R/'results/current_oslo_commute_scope/verification.json')['source_sha256'];extra={**commute,**cv};vpath=R/'results/current_oslo_commute_scope/verification.json';extra[str(vpath.relative_to(R))]=sha(vpath);assert len(extra)==22
for p,h in {**old,**extra}.items():assert sha(R/p)==h,p
index=read(R/'data/task4_access/city_index.json');ix=next(x for x in index if str(x['id'])=='6494');assert ix['city'].casefold()=='oslo' and abs(float(ix['lat'])-59.9816)<1e-8 and abs(float(ix['lon'])-10.73864)<1e-8
meta=read(D/'download.json');raw=D/'6494_hexes.zip';assert meta['status']==200 and raw.stat().st_size==meta['bytes'] and sha(raw)==meta['sha256'] and datetime.datetime.fromisoformat(meta['retrieval_utc']).utcoffset()==datetime.timedelta(0)
metrics=read(V/'metrics.json');assert {x['city'] for x in metrics}=={'Oslo','Zurich'}
computed={}
for city,path in [('Oslo',raw),('Zurich',R/'data/task4_access/9808_hexes.zip')]:
 m=next(a for a in metrics if a['city']==city);assert sha(path)==m['sha256']
 with zipfile.ZipFile(path) as z:fs=json.loads(z.read('hexes.geojson'))['features']
 populations=[]; valid=[];invalid=[];below=[];times=[];coordinates=[]
 for f in fs:
  v=f['properties'];pop=v['population'];t=v['c_f'];assert isinstance(pop,(int,float)) and math.isfinite(pop) and pop>=0
  for ring in f['geometry']['coordinates']:
   for xy in ring:coordinates.append(xy[:2])
  if pop>0:
   populations.append(pop)
   if isinstance(t,(int,float)) and math.isfinite(t) and t>0:
    valid.append(pop);times.append(t)
    if t<=30:below.append(pop)
   else:invalid.append(pop)
 total=math.fsum(populations);good=math.fsum(valid);unknown=math.fsum(invalid);numerator=math.fsum(below)
 assert len(fs)==m['total_cells'] and len(populations)==m['populated_cells']
 for key,value in [('retained_residents',total),('valid_residents',good),('unknown_residents',unknown),('within_30_residents',numerator),('within_30_share_of_valid',numerator/good),('max_valid_minutes',max(times))]:assert math.isclose(m[key],value,rel_tol=1e-12,abs_tol=1e-7),(city,key,m[key],value)
 assert math.isclose(total,good+unknown,abs_tol=1e-7)
 lons=[p[0] for p in coordinates];lats=[p[1] for p in coordinates]
 if city=='Oslo':assert min(lons)<float(ix['lon'])<max(lons) and min(lats)<float(ix['lat'])<max(lats) and abs(total-float(ix['pop']))<.01
 computed[city]={'total_cells':len(fs),'positive_population_cells':len(populations),'retained':total,'valid':good,'unknown':unknown,'within30':numerator,'share_valid':numerator/good,'source_index_population':ix['pop'] if city=='Oslo' else '401551.57','geography_scope':'source grid extent; no independent complete municipal boundary or population census claim'}
# Check all archived original PNGs, including pre-existing six HLS and one MODIS.
archive=read(V/'imagery_manifest.json')+[read(V/'fallback_manifest.json')];assert len(archive)==7
for x in archive:
 p=V/x['path'];assert sha(p)==x['sha256'];assert p.stat().st_size==x['bytes']
withheld=read(V/'oslo_imagery_manifest.json');assert len(withheld)<=3 and len(withheld)>0
for x in withheld:
 p=V/x['path'];assert x['city']=='Oslo' and x['http_status']==200 and sha(p)==x['sha256'] and p.stat().st_size==x['bytes']
 url=urlparse(x['url']);args=parse_qs(url.query);assert url.hostname=='gibs.earthdata.nasa.gov' and args['TIME']==[x['requested_date']] and 'HLS_S30' in args['LAYERS'][0]
 im=Image.open(p).convert('RGBA');alpha=im.getchannel('A');coverage=1-alpha.histogram()[0]/(im.width*im.height);assert abs(coverage-x['alpha_coverage'])<1e-12
 assert 'not verified' in x['product_date'].lower()
svg=E.parse(V/'city_walktime.svg').getroot(); assert svg.attrib['width']=='468pt' and svg.attrib['height']=='460.8pt'
ns={'s':'http://www.w3.org/2000/svg'}; text_nodes=svg.findall('.//s:text',ns);sizes=[]
for node in text_nodes:
 style=node.get('style','');match=re.search(r'font:\s*(?:\d+\s+)?([\d.]+)px',style)
 assert match,style;sizes.append(float(match.group(1)))
assert sizes and min(sizes)>=9
visible=' '.join(''.join(n.itertext()) for n in text_nodes);assert 'Oslo' in visible and 'Zurich' in visible and 'Height = walking time' in visible and 'residents' in visible.lower()
render=(V/'render.py').read_text();assert "Normalize(0,150)" in render and 'set_zlim(0,150)' in render and "(x,y,t)" in render and "if city=='Zurich'" in render
for p,h in {**old,**extra}.items():assert sha(R/p)==h,p
O.mkdir(exist_ok=True);out={'status':'PASS numerical/source, font and independent figure inspection','grid_source':computed,'oslo_source_index':ix,'author_indicator':'c_f is modelled mean walking time to 20 generic Learning POIs; source grids represent residents, not students or school access.','unknown_policy':'Positive resident weight with missing/nonfinite/nonpositive c_f is unknown; excluded from valid denominator and stated separately. Unknown=0 for both snapshots.','old_seven_pngs_hash_verified':len(archive),'oslo_nasa_requests':len(withheld),'oslo_nasa_alpha_coverages':[x['alpha_coverage'] for x in withheld],'imagery_scope':'Raw NASA GIBS browse responses; request dates are not verified granule dates. Clouds remain; no AI-generated observations.','figure_svg_width_pt':468,'min_text_size_at_6_5_in_pt':min(sizes),'visual_inspection':'Full exported figure inspected: labels and legends are legible with no visible clipping or overlap; Zurich cloud remains visible, Oslo uses unbacked grids. Final paper insertion size must remain 6.5 inches or larger.', 'figure_interpretation':'Colour and extrusion height represent mean walking time on shared 0–150 minute scale; not terrain or buildings.','preserved_v203_bindings':len(old),'commute_bound_files_checked':len(extra),'sha256':{str(p.relative_to(R)):sha(p) for p in [pathlib.Path(__file__),raw,V/'metrics.json',V/'city_walktime.pdf',V/'city_walktime.svg',V/'city_walktime.png',V/'render.py',V/'oslo_imagery_manifest.json']}}
(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
