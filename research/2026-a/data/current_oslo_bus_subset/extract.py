"""Derive the Oslo single-mode bus stop-place candidate from the archived NSR export."""
import csv,datetime,hashlib,json,pathlib,zipfile,xml.etree.ElementTree as ET
from collections import Counter,defaultdict
R=pathlib.Path(__file__).resolve().parents[2];D=pathlib.Path(__file__).resolve().parent
source=R/'data/current_oslo_transport/03_Oslo_latest.zip';meta=json.loads((source.parent/'download.json').read_text()); assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['sha256']
with zipfile.ZipFile(source) as z: assert len(z.namelist())==1;doc=ET.fromstring(z.read(z.namelist()[0]))
n={'n':'http://www.netex.org.uk/netex'};nodes=doc.findall('.//n:StopPlace',n); entries={}
def text(e,k):return e.findtext('n:'+k,default='',namespaces=n)
def attr(e,k,a='ref'):
 x=e.find('n:'+k,n);return x.get(a,'') if x is not None else ''
for x in nodes:
 i=x.get('id');assert i not in entries
 entries[i]={'id':i,'name':text(x,'Name'),'city':attr(x,'TopographicPlaceRef'),'parent':attr(x,'ParentSiteRef'),'mode':text(x,'TransportMode'),'type':text(x,'StopPlaceType'),'submode':text(x,'BusSubmode'),'lon':x.findtext('n:Centroid/n:Location/n:Longitude',default='',namespaces=n),'lat':x.findtext('n:Centroid/n:Location/n:Latitude',default='',namespaces=n),'quays':[q.get('id') for q in x.findall('n:quays/n:Quay',n)],'validity':[{'from':text(v,'FromDate'),'to':text(v,'ToDate')} for v in x.findall('n:ValidBetween',n)],'element':x}
city={k:v for k,v in entries.items() if v['city']=='KVE:TopographicPlace:0301'}; assert len(city)==1256
# Entire source hierarchy: do not accidentally admit a group with an out-of-city or non-bus member.
groups=defaultdict(list)
for i,v in entries.items():
 if v['parent']: assert v['parent'] in entries and not entries[v['parent']]['parent']
 groups[v['parent'] or i].append(v)
modes={'bus','tram','metro','rail','water'};selected=[]
for root,members in groups.items():
 if root not in city:continue
 bearing=[v for v in members if v['mode']]
 if not bearing or not all(v['mode']=='bus' and v['type']=='onstreetBus' for v in bearing):continue
 if any(v['city']!='KVE:TopographicPlace:0301' for v in members):continue
 selected.append((root,members,bearing))
assert len(selected)==627
assert sum(any(v['id']=='NSR:StopPlace:6109' for v in m) for _,m,_ in selected)==1
selected=[item for item in selected if all(v['id']!='NSR:StopPlace:6109' for v in item[1])]
assert len(selected)==626
# Independent polygon test over group roots and every member centroid.
b=json.loads((R/'data/task4_v118_transit/oslo_boundary_raw.json').read_text());assert b['kommunenummer']=='0301'; polys=b['omrade']['coordinates']; boxes=[(min(q[0] for q in p[0]),min(q[1] for q in p[0]),max(q[0] for q in p[0]),max(q[1] for q in p[0])) for p in polys]
def ring(x,y,p):
 inside=False;x0,y0=p[-1]
 for x1,y1 in p:
  if (y1>y)!=(y0>y) and x<(x0-x1)*(y-y1)/(y0-y1)+x1:inside=not inside
  x0,y0=x1,y1
 return inside
def inside(x,y):return any(a<=x<=c and b<=y<=d and ring(x,y,p[0]) and not any(ring(x,y,q) for q in p[1:]) for p,(a,b,c,d) in zip(polys,boxes))
rows=[]; suspicious=[];field_flags=[];allquays=[];validity=[];submodes=Counter();mode_without_quays=[];words=('garage','garasje','depot','test','nedlagt','flytt','dummy')
for root,members,bearing in sorted(selected):
 r=entries[root];assert r['name'].strip() and r['lon'] and r['lat']
 for v in members:
  assert v['lon'] and v['lat'] and inside(float(v['lon']),float(v['lat']))
  assert v['name'].strip()
  if any(w in v['name'].casefold() for w in words):suspicious.append([v['id'],v['name']])
  for dt in v['element'].findall('.//n:ValidBetween',n):
   start=text(dt,'FromDate');end=text(dt,'ToDate');validity.append((v['id'],start,end))
  allquays.extend(v['quays'])
  if v['mode'] and not v['quays']:mode_without_quays.append(v['id'])
  for kv in v['element'].findall('n:keyList/n:KeyValue',n):
   key=text(kv,'Key');value=text(kv,'Value')
   if key not in ('imported-id','merged-id') and any(w in (key+' '+value).casefold() for w in ('garage','garasje','depot','dummy','test','future','private','nedlagt','flytt','planned','planlagt','stengt')):field_flags.append({'id':v['id'],'field':key,'value':value})
  for key in ('Description','ShortName','PublicCode','PrivateCode'):
   value=text(v['element'],key)
   if any(w in value.casefold() for w in ('garage','garasje','depot','dummy','test','future','private','nedlagt','flytt','planned','planlagt','stengt')):field_flags.append({'id':v['id'],'field':key,'value':value})
 for v in bearing:submodes[v['submode']]+=1
 rows.append({'root_id':root,'root_name':r['name'],'root_longitude':r['lon'],'root_latitude':r['lat'],'member_ids':'|'.join(sorted(v['id'] for v in members)),'mode_bearing_ids':'|'.join(sorted(v['id'] for v in bearing)),'member_names':json.dumps({v['id']:v['name'] for v in members},ensure_ascii=False,sort_keys=True),'member_modes_types':json.dumps({v['id']:[v['mode'],v['type'],v['submode']] for v in members},ensure_ascii=False,sort_keys=True),'quay_ids':'|'.join(sorted(q for v in members for q in v['quays'])),'member_quay_ids':json.dumps({v['id']:v['quays'] for v in members},sort_keys=True),'validity':json.dumps({v['id']:v['validity'] for v in members},sort_keys=True)})
assert len({r['root_name'].strip().casefold() for r in rows})==626 and not suspicious and not mode_without_quays
assert len(allquays)==len(set(allquays))
# Check all nested validity intervals, including quays; absence is not a service guarantee.
cut=datetime.date.fromisoformat('2026-11-09')
for i,start,end in validity:
 if start:assert datetime.date.fromisoformat(start[:10])<=cut,(i,start)
 if end:assert datetime.date.fromisoformat(end[:10])>=cut,(i,end)
with (D/'bus_stop_groups.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
pop=727797; density=626*100000/pop;util=density/(50+density)
out={'status':'candidate_not_admitted','count':626,'excluded_unresolved_discontinuation_tag':{'id':'NSR:StopPlace:6109','name':'Tveten bru','note':'Tag asks whether discontinued or may be deactivated; exclusion is precautionary and does not assert closure.'},'source_export_date':'2026-11-09','source_capture_utc':meta['retrieved_utc'],'population':pop,'population_year':2025,'density_per_100000':density,'utility_lower':util,'utility_upper':1,'group_definition':'NSR parent-collapsed group; every mode-bearing member bus/onstreetBus; all members municipality 0301 and centroid inside archived polygon; root names unique after strip/casefold; no proximity merge; all quay IDs supporting metadata, not units','scope':'Conditional administrative stop-place inventory, not a claim that all are served or public/private access; 2026 source and fixed 2025 population. Do not add 89 metro stations; no admission to V202.','unique_quays':len(allquays),'groups_without_quays':sum(not r['quay_ids'] for r in rows),'nested_validity_intervals':len(validity),'mode_bearing_members_without_quays':mode_without_quays,'keyword_flagged_source_fields':field_flags,'rail_replacement_bus_member_ids':['NSR:StopPlace:317','NSR:StopPlace:668'],'bus_submodes':dict(submodes),'suspicious_name_keyword_matches':suspicious,'sha256':{'source':meta['sha256'],'boundary':hashlib.sha256((R/'data/task4_v118_transit/oslo_boundary_raw.json').read_bytes()).hexdigest(),'derived_csv':hashlib.sha256((D/'bus_stop_groups.csv').read_bytes()).hexdigest(),'extract_script':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()}}
(D/'observations.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');print(json.dumps(out,indent=2,ensure_ascii=False))
