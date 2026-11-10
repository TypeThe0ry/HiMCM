"""Independent offline descriptive audit; does not admit a new transport indicator."""
import csv, datetime, hashlib, json, math, pathlib, zipfile, xml.etree.ElementTree as ET
from collections import Counter, defaultdict
R=pathlib.Path(__file__).resolve().parents[1]
O=R/'data/current_oslo_transport'; Z=R/'data/current_zurich_transport'
def read(p): return json.loads(p.read_text())
def check_capture(p,meta):
 b=p.read_bytes(); assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256']; assert meta['http_status']==200
 assert datetime.datetime.fromisoformat(meta['retrieved_utc']).utcoffset()==datetime.timedelta(0)
 return meta['sha256']
om=read(O/'download.json'); zm=read(Z/'provenance.json'); oh=check_capture(O/'03_Oslo_latest.zip',om); zh=check_capture(Z/'kanton_zh_wfs.geojson',zm)
with zipfile.ZipFile(O/'03_Oslo_latest.zip') as z:
 assert len(z.namelist())==1
 x=ET.fromstring(z.read(z.namelist()[0]))
n={'n':'http://www.netex.org.uk/netex'}; stops=x.findall('.//n:StopPlace',n); a={}
for s in stops:
 id=s.get('id'); assert id not in a
 ref=s.find('n:TopographicPlaceRef',n); par=s.find('n:ParentSiteRef',n)
 lo=s.findtext('n:Centroid/n:Location/n:Longitude',namespaces=n); la=s.findtext('n:Centroid/n:Location/n:Latitude',namespaces=n)
 a[id]={'city':ref.get('ref') if ref is not None else None,'parent':par.get('ref') if par is not None else None,'lon':float(lo) if lo else None,'lat':float(la) if la else None,'mode':s.findtext('n:TransportMode',default='',namespaces=n),'name':s.findtext('n:Name',default='',namespaces=n)}
city={i:v for i,v in a.items() if v['city']=='KVE:TopographicPlace:0301'}
g=defaultdict(set); missing_parent=0
for i,v in city.items():
 if v['mode'] not in {'bus','tram','metro','rail','water'}: continue
 if v['parent'] and v['parent'] not in city: missing_parent+=1; continue
 g[v['parent'] or i].add(i)
g={k:v for k,v in g.items() if all(city[j]['lon'] is not None and city[j]['lat'] is not None for j in v|{k})}
assert (len(stops),len(city),len(g))==(1257,1256,829)
assert not any(city[k]['parent'] for k in g), 'nested parent hierarchy requires review'
keys=sorted(g); par=list(range(len(keys)))
def root(i):
 while par[i]!=i: par[i]=par[par[i]]; i=par[i]
 return i
def near(a,b):
 return math.hypot((a['lon']-b['lon'])*111320*math.cos(math.radians((a['lat']+b['lat'])/2)),(a['lat']-b['lat'])*111320)<=250
for i,k in enumerate(keys):
 for j in range(i):
  if any((a['name'].strip().casefold() and a['name'].strip().casefold()==b['name'].strip().casefold()) or near(a,b) for a in (city[t] for t in g[k]|{k}) for b in (city[t] for t in g[keys[j]]|{keys[j]})):
   par[root(i)]=root(j)
components=defaultdict(set)
for i,k in enumerate(keys): components[root(i)].add(k)
assert len(components)==517
with (O/'conservative_basins.csv').open() as f: rows=list(csv.DictReader(f))
assert len(rows)==829 and {r['id'] for r in rows}==set(g)
by=defaultdict(set)
for r in rows:
 by[r['basin']].add(r['id']); assert set(r['member_stopplace_ids'].split('|'))==g[r['id']]
assert {frozenset(v) for v in by.values()}=={frozenset(v) for v in components.values()}
# Existing Kartverket boundary archive: ray casting and holes, with per-part bounding boxes.
bound=read(R/'data/task4_v118_transit/oslo_boundary_raw.json'); assert bound['kommunenummer']=='0301' and bound['omrade']['type']=='MultiPolygon'
polys=bound['omrade']['coordinates']; bounds=[(min(p[0] for p in v[0]),min(p[1] for p in v[0]),max(p[0] for p in v[0]),max(p[1] for p in v[0])) for v in polys]
def inring(x,y,r):
 inside=False; x0,y0=r[-1]
 for x1,y1 in r:
  if (y1>y)!=(y0>y) and x<(x0-x1)*(y-y1)/(y0-y1)+x1: inside=not inside
  x0,y0=x1,y1
 return inside
def contains(x,y):
 return any(lo<=x<=hi and bot<=y<=top and inring(x,y,p[0]) and not any(inring(x,y,h) for h in p[1:]) for p,(lo,bot,hi,top) in zip(polys,bounds))
spatial={i:contains(v['lon'],v['lat']) for i,v in city.items() if v['lon'] is not None and v['lat'] is not None}
outside=[i for i,v in spatial.items() if not v]
z=read(Z/'kanton_zh_wfs.geojson'); fs=z['features']; assert len(fs)==z['numberMatched']==zm['feature_count']==3004
zz=[v['properties'] for v in fs if v['properties']['cname']=='Zürich']; assert len(zz)==479
no_lines=sum(not v['linien'] for v in zz); assert no_lines==17
# Check the reported ambiguity examples against original fields rather than labels alone.
for name, ids in {'Trosterud':['NSR:StopPlace:5677','NSR:StopPlace:6197'], 'Midtstuen':['NSR:StopPlace:6302','NSR:StopPlace:6313']}.items():
 assert all(city[i]['name']==name and i in g and not city[i]['parent'] for i in ids)
 assert {city[i]['mode'] for i in ids}=={'bus','metro'}
 assert near(city[ids[0]],city[ids[1]])
D=lambda n,p:n*100000/p
result={'status':'source_and_computation_audit_complete; no admission','oslo':{'source_sha256':oh,'http_status_and_utc_are_recorded_metadata_not_independently_replayed':True,'records':len(stops),'municipality_reference_records':len(city),'native_mode_bearing_parent_collapsed_roots':len(g),'missing_parent_excluded':missing_parent,'polygon_checked_centroids':len(spatial),'outside_polygon_centroids':len(outside),'outside_polygon_ids':outside,'same_name_cross_mode_separate_roots':{'Trosterud':['NSR:StopPlace:5677','NSR:StopPlace:6197'],'Midtstuen':['NSR:StopPlace:6302','NSR:StopPlace:6313']},'native_density_per_100000':D(829,727797),'heuristic_clusters':len(components),'heuristic_density_per_100000':D(517,727797),'population':727797,'decision':'517 is diagnostic only; proximity/name clusters lack a validated physical-stop definition and polygon findings require review. Native parent-collapsed count is a conditional administrative StopPlace count, not platform count or a proven one-to-one physical facility count. No addition to existing 89.','native_semantics_source':'https://enturas.atlassian.net/wiki/plugins/viewsource/viewpagesrc.action?pageId=3846668311','registry_source':'https://developer.entur.org/pages-nsr-nsr/'},'zurich':{'source_sha256':zh,'http_status_and_utc_are_recorded_metadata_not_independently_replayed':True,'total_features':len(fs),'cname_exact_Zürich':len(zz),'no_listed_lines':no_lines,'population':440935,'existing_vbz_count':446,'existing_density_per_100000':D(446,440935),'decision':'Reject substitution or addition: cname is not a validated city polygon and raw identifiers do not establish comparable unique physical stops or active service; no proven increase over 446.'}}
out=R/'results/current_transport_candidate/source_verification.json'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps(result,indent=2,ensure_ascii=False))
