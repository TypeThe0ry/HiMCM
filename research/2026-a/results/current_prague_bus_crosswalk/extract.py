#!/usr/bin/env python3
"""Exact archived-to-current PID cross-snapshot diagnostic; missing != false."""
import collections,csv,hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent
R=H.parent.parent
OLD=R/'results/current_prague_bus_node_candidate/all_link_occurrences.csv'
SEM=R/'data/current_prague_node_semantics'
METRO=R/'data/task4_v127_prague/station_complexes.csv'
files=[OLD,SEM/'pid_stops.json',SEM/'pid_stops_schema.xsd',SEM/'pid_buses.html',SEM/'manifest.json',METRO]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=json.loads((SEM/'pid_stops.json').read_text())
assert d['generatedAt']=='2026-11-10T04:12:17'
groups=collections.defaultdict(list)
for gi,g in enumerate(d['stopGroups']):groups[(str(g['node']),g['name'])].append((gi,g))
rows=list(csv.DictReader(OLD.open(encoding='utf8')))
out=[]; qualified=[]
for row in rows:
 k=(row['node'],row['stop_name']); gs=groups.get(k,[])
 status=''; hits=[]
 if not gs: status='no_exact_group'
 elif len(gs)!=1: status='ambiguous_group'
 else:
  gi,g=gs[0]
  for si,stop in enumerate(g.get('stops',[])):
   for li,line in enumerate(stop.get('lines',[])):
    if line.get('name')==row['display_route']:
     hits.append((si,li,stop,line))
  modes=sorted({x[3].get('type','') for x in hits})
  if not hits: status='no_exact_route'
  elif len(modes)!=1: status='ambiguous_mode'
  elif modes!=['bus']: status='non_bus'
  elif not row['display_route'].isdigit() or not 100<=int(row['display_route'])<=250: status='outside_100_250'
  elif row['inprague']!='1': status='not_prague'
  elif row['flags']: status='flagged_archived_link'
  else:
   nights={x[3].get('isNight','absent') for x in hits}
   if True in nights: status='explicit_night_or_mixed'
   else: status='qualifying'
 extra={'classification':status,'group_count':len(gs),'current_group_index':gs[0][0] if len(gs)==1 else '',
 'current_group_name':gs[0][1]['name'] if len(gs)==1 else '',
 'current_group_municipality':gs[0][1].get('municipality','') if len(gs)==1 else '',
 'current_types':';'.join(sorted({str(x[3].get('type','')) for x in hits})),
 'current_night_values':';'.join(sorted({str(x[3].get('isNight','absent')) for x in hits})),
 'current_pole_ids':';'.join(sorted({x[2].get('id','') for x in hits})),
 'current_line_locators':';'.join(f'stopGroups[{gs[0][0]}].stops[{x[0]}].lines[{x[1]}]' for x in hits) if len(gs)==1 else ''}
 out.append({**row,**extra})
 if status=='qualifying':qualified.append({**row,**extra})
# Stable ordering, one archived witness per native node.
qualified.sort(key=lambda x:(int(x['node']),x['stop_name'],x['display_route'],x['file'],x['locator']))
witness={}
for row in qualified:witness.setdefault(row['node'],row)
fields=list(out[0])
for name,data in [('link_diagnostics.csv',out),('witness.csv',list(witness.values()))]:
 with (H/name).open('w',encoding='utf8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(data)
counts=collections.Counter(x['classification'] for x in out)
metro=list(csv.DictReader(METRO.open(encoding='utf8')))
metro_overlap=sorted(set(witness)&{r['pid_node_id'] for r in metro},key=int)
receipt={'description':'Exact node + stop group name + displayed line name match, never internal line ID. JSON is newer than archived 2026-11-09 response.', 'current_generatedAt':d['generatedAt'],'source_sha256':{str(p.relative_to(R)):digest(p) for p in files}, 'classification_precedence':'no exact group; ambiguous group; no exact route; ambiguous mode; non-bus; outside 100–250; not Prague; flagged archive; explicit night/mixed; qualify', 'link_occurrences_by_first_exclusion':dict(counts),'conditional_candidate_distinct_nodes':len(witness),'candidate_night_values':dict(collections.Counter(x['current_night_values'] for x in witness.values())), 'candidate_current_municipality':dict(collections.Counter(x['current_group_municipality'] for x in witness.values())), 'overlap_existing_57_metro_by_node':len(metro_overlap), 'overlap_node_ids':metro_overlap,'note':'isNight absent stays unknown; explicitly true excluded conservatively. Distinct nodes do not establish distinct physical sites; no admission or day-service claim.'}
(H/'receipt.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n');print(json.dumps(receipt,indent=2,ensure_ascii=False))
