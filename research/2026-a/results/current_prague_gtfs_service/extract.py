#!/usr/bin/env python3
"""Offline reproducible PID GTFS qualification; stream stop_times directly from ZIP."""
import collections,csv,datetime,hashlib,io,json,zipfile
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parent.parent
PACKAGED=R/'data/current_prague_gtfs_service/PID_GTFS_20261110.zip'
EXTERNAL=Path('/data/datasets/HiMCM/source_archives/PID_GTFS_20261110.zip')
ARCH=PACKAGED if PACKAGED.exists() else EXTERNAL
EXPECTED='dfde0f0d8b662795bbce2adc185c676b5d1a0cc9c0a18f8373cc4a46374c111a'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
assert sha(ARCH)==EXPECTED, 'GTFS archive hash mismatch'
D=R/'results/current_prague_bus_crosswalk/link_diagnostics.csv'; J=R/'data/current_prague_node_semantics/pid_stops.json'
assert sha(D)=='575a1e02edab6fe7b7ebaee42b4b7a21b6122902925b4bab55399b5070c4c96c'
assert sha(J)=='f372f85b730fe86d5e12f09374cf14e0794857b96848e9b1ddcfbeaaef9849a0'
rows=[r for r in csv.DictReader(D.open(encoding='utf8')) if r['classification']=='qualifying']
groups=json.loads(J.read_text())['stopGroups']; pairs={}
for r in rows:
 g=groups[int(r['current_group_index'])]
 assert str(g['node'])==r['node'] and g['name']==r['stop_name']
 for si,s in enumerate(g['stops']):
  for li,l in enumerate(s.get('lines',[])):
   if l.get('name')==r['display_route'] and l.get('type')=='bus' and l.get('isNight') is not True:
    node,post=s['id'].split('/')
    assert node==r['node']
    key=(node,post,r['display_route'])
    rec={'node':node,'post':post,'route_short_name':r['display_route'],'group_name':g['name'],'json_pole_id':s['id'],'json_pole_locator':f"stopGroups[{r['current_group_index']}].stops[{si}]",'json_line_locator':f"stopGroups[{r['current_group_index']}].stops[{si}].lines[{li}]",'json_isNight':str(l.get('isNight','absent')),'list_file':r['file'],'list_locator':r['locator'],'list_url':r['timetable_url']}
    if key not in pairs or tuple(rec.values())<tuple(pairs[key].values()):pairs[key]=rec
assert len({x[0] for x in pairs})==942
z=zipfile.ZipFile(ARCH)
def member_sha(name):
 h=hashlib.sha256()
 with z.open(name) as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def records(name):
 with z.open(name) as f:
  yield from csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''))
info=list(records('feed_info.txt'))[0]; day='20261110'; assert info['feed_start_date']<=day<=info['feed_end_date']
calendar={x['service_id']:x for x in records('calendar.txt')}; exceptions={}
for x in records('calendar_dates.txt'):
 if x['date']==day:
  assert x['service_id'] not in exceptions
  exceptions[x['service_id']]=x['exception_type']
def active(s):
 c=calendar.get(s); base=bool(c and c['start_date']<=day<=c['end_date'] and c['tuesday']=='1'); ex=exceptions.get(s,'')
 assert ex in ('','1','2')
 return (ex=='1' or (base and ex!='2')),base,ex
routes={x['route_id']:x for x in records('routes.txt')}
stops={x['stop_id']:x for x in records('stops.txt') if x['location_type'] in ('','0') and x['zone_region_type']=='1' and x['asw_node_id'] and x['asw_stop_id']}
by_pole=collections.defaultdict(list)
for sid,s in stops.items():by_pole[(s['asw_node_id'],s['asw_stop_id'])].append(sid)
trips={x['trip_id']:x for x in records('trips.txt') if x['route_id'] in routes and routes[x['route_id']]['route_short_name'].isdigit() and 100<=int(routes[x['route_id']]['route_short_name'])<=250}
# Track all date and mode mismatches as stage counters, and store a deterministic witness.
flags=collections.defaultdict(collections.Counter); witnesses={}; conditional_witnesses={}; phone_witnesses={}; counts=collections.Counter()
for st in records('stop_times.txt'):
 t=trips.get(st['trip_id']); s=stops.get(st['stop_id'])
 if not t or not s:continue
 route=routes[t['route_id']]; k=(s['asw_node_id'],s['asw_stop_id'],route['route_short_name'])
 if k not in pairs:continue
 f=flags[k]; f['matching_stop_times']+=1
 if route['route_type']!='3':f['non_bus']+=1;continue
 if route['is_night']!='0':f['night_or_unknown']+=1;continue
 if route['is_substitute_transport']!='0':f['substitute_or_unknown']+=1;continue
 on,base,ex=active(t['service_id'])
 if not on:f['inactive_service']+=1;continue
 f['active_service']+=1
 pickup=st['pickup_type']; drop=st['drop_off_type']
 regular=pickup in ('','0') or drop in ('','0')
 driver='3' in (pickup,drop)
 phone='2' in (pickup,drop)
 if not regular:
  f['no_regular_public_access']+=1
  if not driver and not phone:
   f['both_forbidden']+=1
   continue
  if driver:f['driver_arrangement']+=1
  elif phone:f['phone_arrangement']+=1
 else:f['public_regular']+=1
 w={**pairs[k], 'gtfs_stop_id':st['stop_id'],'gtfs_stop_name':s['stop_name'],'gtfs_location_type':s['location_type'],'gtfs_zone_region_type':s['zone_region_type'],'route_id':t['route_id'],'route_type':route['route_type'],'route_is_night':route['is_night'],'route_is_substitute_transport':route['is_substitute_transport'],'trip_id':st['trip_id'],'service_id':t['service_id'],'calendar_tuesday':calendar.get(t['service_id'],{}).get('tuesday',''),'calendar_start_date':calendar.get(t['service_id'],{}).get('start_date',''),'calendar_end_date':calendar.get(t['service_id'],{}).get('end_date',''),'calendar_base_active':int(base),'calendar_exception_type':ex,'arrival_time':st['arrival_time'],'departure_time':st['departure_time'],'stop_sequence':st['stop_sequence'],'pickup_type':pickup,'drop_off_type':drop,'trip_operation_type':st['trip_operation_type']}
 rank=(w['route_short_name'],w['post'],w['gtfs_stop_id'],w['trip_id'],int(w['stop_sequence']),w['list_file'],w['list_locator'])
 target=witnesses if regular else conditional_witnesses if driver else phone_witnesses
 if k not in target or rank<target[k][0]:target[k]=(rank,w)
nodew={}
for k,(rank,w) in witnesses.items():
 if k[0] not in nodew or rank<nodew[k[0]][0]:nodew[k[0]]=(rank,w)
def write(name,data,fields):
 with (H/name).open('w',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(data)
ws=[nodew[n][1] for n in sorted(nodew,key=int)]; assert ws
write('witness.csv',ws,list(ws[0]))
conditional_nodew={}
for k,(rank,w) in conditional_witnesses.items():
 if k[0] not in conditional_nodew or rank<conditional_nodew[k[0]][0]:conditional_nodew[k[0]]=(rank,w)
cws=[conditional_nodew[n][1] for n in sorted(conditional_nodew,key=int)]
write('conditional_witness.csv',cws,list(ws[0]))
phone_nodew={}
for k,(rank,w) in phone_witnesses.items():
 if k[0] not in phone_nodew or rank<phone_nodew[k[0]][0]:phone_nodew[k[0]]=(rank,w)
write('phone_witness.csv',[phone_nodew[n][1] for n in sorted(phone_nodew,key=int)],list(ws[0]))
union_nodes=set(nodew)|set(conditional_nodew)
write('public_witness.csv',[(nodew.get(n) or conditional_nodew[n])[1] for n in sorted(union_nodes,key=int)],list(ws[0]))
pairrows=[]
for k,p in sorted(pairs.items(),key=lambda x:(int(x[0][0]),x[0][1],x[0][2])):
 f=flags[k]; ids=by_pole[(k[0],k[1])]
 status=('ordinary_0' if k in witnesses else 'driver_3' if k in conditional_witnesses else 'phone_2_only' if k in phone_witnesses else 'no_public_prague_gtfs_pole' if not ids else 'no_matching_route_stop_time' if not f['matching_stop_times'] else 'no_eligible_active_public_stop_time')
 pairrows.append({**p,'gtfs_prague_stop_ids':';'.join(sorted(ids)),'status':status,**{x:f[x] for x in ['matching_stop_times','non_bus','night_or_unknown','substitute_or_unknown','inactive_service','active_service','no_regular_public_access','driver_arrangement','phone_arrangement','both_forbidden','public_regular']}})
write('pair_diagnostics.csv',pairrows,list(pairrows[0]))
nodepairs=collections.defaultdict(list)
for r in pairrows:nodepairs[r['node']].append(r)
node_rows=[{'node':n,'status':'ordinary_0' if n in nodew else 'driver_3' if n in conditional_nodew else 'phone_2_only' if n in phone_nodew else 'no_evidence','pair_count':len(ps),'pair_statuses':json.dumps(dict(collections.Counter(p['status'] for p in ps)),sort_keys=True)} for n,ps in sorted(nodepairs.items(),key=lambda x:int(x[0]))]
write('node_diagnostics.csv',node_rows,list(node_rows[0]))
receipt={'source_url':'https://data.pid.cz/PID_GTFS.zip','archive_path':str(ARCH.relative_to(R)) if ARCH==PACKAGED else str(ARCH),'external_archive_path':str(EXTERNAL),'member_crc32':{i.filename:f'{i.CRC:08x}' for i in z.infolist()},'archive_bytes':ARCH.stat().st_size,'archive_sha256':EXPECTED,'archive_http_status':200,'archive_etag':'"2c62389-65fe36f03d140"','last_modified':'Tue, 10 Nov 2026 03:11:25 GMT','http_date_utc':'Tue, 10 Nov 2026 21:41:23 GMT','feed_info':info,'service_date':day,'weekday':'Tuesday','input_sha256':{str(p.relative_to(R)):sha(p) for p in (D,J)},'gtfs_member_sha256':{n:member_sha(n) for n in ['feed_info.txt','stops.txt','routes.txt','trips.txt','calendar.txt','calendar_dates.txt','stop_times.txt']},'candidate_nodes':len(nodepairs),'ordinary_0_nodes':len(ws),'driver_3_nodes':len(cws),'driver_3_only_nodes':len(set(conditional_nodew)-set(nodew)),'ordinary_or_driver_nodes':len(union_nodes),'phone_2_nodes':len(phone_nodew),'no_ordinary_or_driver_nodes':len(nodepairs)-len(union_nodes),'candidate_pole_route_pairs':len(pairs),'pair_status_counts':dict(collections.Counter(x['status'] for x in pairrows)),'stop_time_diagnostics':dict(sum((collections.Counter({k:int(v) for k,v in f.items()}) for f in flags.values()),collections.Counter())),'public_witness_exception_types':dict(collections.Counter((nodew.get(n) or conditional_nodew[n])[1]['calendar_exception_type'] or 'none' for n in union_nodes)),'output_sha256':{n:sha(H/n) for n in ['witness.csv','conditional_witness.csv','phone_witness.csv','public_witness.csv','pair_diagnostics.csv','node_diagnostics.csv']}}
(H/'receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print(json.dumps(receipt,indent=2,ensure_ascii=False))
