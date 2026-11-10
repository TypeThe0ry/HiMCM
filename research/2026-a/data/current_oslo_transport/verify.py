"""Offline conservative consolidation of Entur's current Oslo NeTEx export."""
import csv, hashlib, json, math, pathlib, zipfile, xml.etree.ElementTree as ET
P=pathlib.Path(__file__).resolve().parent
z=zipfile.ZipFile(P/'03_Oslo_latest.zip'); assert len(z.namelist())==1
r=ET.fromstring(z.read(z.namelist()[0])); ns={'n':'http://www.netex.org.uk/netex'}
ss=r.findall('.//n:StopPlace',ns); records={}
for x in ss:
    ref=x.find('n:TopographicPlaceRef',ns)
    if ref is None or ref.get('ref')!='KVE:TopographicPlace:0301': continue
    lon=x.findtext('n:Centroid/n:Location/n:Longitude',namespaces=ns); lat=x.findtext('n:Centroid/n:Location/n:Latitude',namespaces=ns)
    parent=x.find('n:ParentSiteRef',ns)
    records[x.get('id')]={'id':x.get('id'),'name':x.findtext('n:Name',default='',namespaces=ns),'municipality':'0301','lon':float(lon) if lon else None,'lat':float(lat) if lat else None,'parent':parent.get('ref') if parent is not None else '', 'mode':x.findtext('n:TransportMode',default='',namespaces=ns),'type':x.findtext('n:StopPlaceType',default='',namespaces=ns)}
# Only parent groups with at least one transport-mode child or independent mode-bearing stop.
root=lambda q: records[q]['parent'] if records[q]['parent'] else q
groups={}
for q,a in records.items():
    if a['mode'] not in {'bus','tram','metro','rail','water'}: continue
    if a['parent'] and a['parent'] not in records: continue
    k=root(q); groups.setdefault(k,[]).append(q)
# Exclude missing coordinates, including children; prevent unresolved spatial overlaps.
groups={k:v for k,v in groups.items() if all(records[q]['lon'] is not None and records[q]['lat'] is not None for q in [k]+v)}
keys=sorted(groups); p=list(range(len(keys)))
def find(i):
    while p[i]!=i: p[i]=p[p[i]]; i=p[i]
    return i
def union(i,j):
    a,b=find(i),find(j)
    if a!=b:p[b]=a
def dist(a,b):
    return math.hypot((a['lon']-b['lon'])*111320*math.cos(math.radians((a['lat']+b['lat'])/2)),(a['lat']-b['lat'])*111320)
# Merge any roots with member centroids within 250 m, or identical casefolded names.
# Transitive merging intentionally coalesces many genuinely distinct nearby stops.
for i,k in enumerate(keys):
 for j in range(i):
    l=keys[j]; aa=[records[x] for x in [k]+groups[k]]; bb=[records[x] for x in [l]+groups[l]]
    if any(a['name'].strip().casefold() and a['name'].strip().casefold()==b['name'].strip().casefold() or dist(a,b)<=250 for a in aa for b in bb): union(i,j)
clusters={}
for i,k in enumerate(keys): clusters.setdefault(find(i),[]).append(k)
rows=[]
for no,ks in enumerate(sorted(clusters.values(),key=lambda a:a[0]),1):
 for k in ks:
  a=records[k]
  rows.append({'basin':no,'id':k,'name':a['name'],'municipality':'0301','longitude':a['lon'],'latitude':a['lat'],'member_stopplace_ids':'|'.join(sorted(set(groups[k]))),'modes':'|'.join(sorted({records[q]['mode'] for q in groups[k]}))})
with (P/'conservative_basins.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
n=len(clusters); d=n*100000/727797; u=d/(50+d)
out={'stopplace_records':len(ss),'municipality_0301_records':len(records),'eligible_root_groups':len(keys),'conservative_basin_count':n,'population':727797,'density_per_100000':d,'utility_interval':[u,1],'policy':'parent-child collapse; union distinct roots if any member centroids within 250 m or exact casefolded name; transitive closure; public transport modes only; exclude missing coordinates or missing parent; not a full inventory','zip_sha256':hashlib.sha256((P/'03_Oslo_latest.zip').read_bytes()).hexdigest()}
(P/'summary.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
