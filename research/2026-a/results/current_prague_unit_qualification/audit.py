#!/usr/bin/env python3
"""Inventory exact PID identity collisions involving the 942 candidate nodes."""
import collections,csv,hashlib,json,unicodedata
from pathlib import Path
H=Path(__file__).resolve().parent; R=H.parent.parent
paths=['results/current_prague_bus_crosswalk/witness.csv','results/current_prague_bus_crosswalk/link_diagnostics.csv','results/current_prague_bus_node_candidate/all_link_occurrences.csv','data/current_prague_node_semantics/pid_stops.json','data/current_prague_node_semantics/pid_stops_schema.xsd','data/current_prague_node_semantics/pid_opendata.html','data/current_prague_node_semantics/manifest.json','results/current_transport_identity/bus_subset_audit.json']
w=list(csv.DictReader((R/paths[0]).open())); candidates={int(x['node']) for x in w};assert len(w)==len(candidates)==942
d=json.loads((R/paths[3]).read_text()); groups=d['stopGroups']; assert d['generatedAt']=='2026-11-10T04:12:17'
by_node=collections.defaultdict(list)
for i,g in enumerate(groups):by_node[g['node']].append((i,g))
# Confirm exact join to current group and archived records for each witness.
old=list(csv.DictReader((R/paths[2]).open()));oldkeys={(x['node'],x['stop_name'],x['display_route'],x['file'],x['locator']) for x in old}
for x in w:
 assert (x['node'],x['stop_name'],x['display_route'],x['file'],x['locator']) in oldkeys
 assert len([g for _,g in by_node[int(x['node'])] if g['name']==x['stop_name']])==1
 assert groups[int(x['current_group_index'])]['name']==x['stop_name']

def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).casefold().split())
def write(name, rows, fields):
 with (H/name).open('w',encoding='utf8',newline='') as f:
  dw=csv.DictWriter(f,fieldnames=fields);dw.writeheader();dw.writerows(rows)
# Record all groups belonging to candidate nodes, not only the chosen witness group.
inv=[]
for n in sorted(candidates):
 for i,g in by_node[n]:
  inv.append({'node':n,'group_index':i,'name':g['name'],'idosName':g['idosName'],'uniqueName':g['uniqueName'],'cis':g['cis'],'municipality':g['municipality'],'poles':len(g['stops']),'pole_ids':';'.join(s['id'] for s in g['stops'])})
write('candidate_groups.csv',inv,list(inv[0]))
# index group fields and pole fields across entire source; ignore null/zero CIS and coordinates.
indexes={k:collections.defaultdict(list) for k in ['name_exact','name_normalized','idosName','uniqueName','cis','pole_id','gtfs_id','coordinates']}
for i,g in enumerate(groups):
 rec=(g['node'],i,g['name'],g['municipality'])
 for kind,val in [('name_exact',g['name']),('name_normalized',norm(g['name'])),('idosName',g['idosName']),('uniqueName',g['uniqueName']),('cis',g.get('cis'))]:
  if val not in (None,'',0):indexes[kind][str(val)].append((rec,''))
 for s in g['stops']:
  for kind,val in [('pole_id',s['id'])]+[('gtfs_id',x) for x in s['gtfsIds']]+[('coordinates',f"{s['lat']},{s['lon']}" if s['lat'] and s['lon'] else '')]:
   if val:indexes[kind][str(val)].append((rec,s['id']))
coll=[];summary={}
for kind,idx in indexes.items():
 stats=collections.Counter()
 for key,records in idx.items():
  nodes={r[0][0] for r in records}; cand=nodes&candidates
  if len(nodes)<2 or not cand:continue
  stats['keys_involving_candidate']+=1
  if len(cand)>=2:stats['keys_two_or_more_candidate_nodes']+=1
  for (n,i,name,muni),pole in records:
   coll.append({'kind':kind,'key':key,'node':n,'candidate':int(n in candidates),'group_index':i,'group_name':name,'municipality':muni,'pole_id':pole,'candidate_nodes_in_key':len(cand),'all_nodes_in_key':len(nodes)})
 summary[kind]=dict(stats)
write('cross_node_collisions.csv',coll,['kind','key','node','candidate','group_index','group_name','municipality','pole_id','candidate_nodes_in_key','all_nodes_in_key'])
counts=collections.Counter(len(by_node[n]) for n in candidates)
mun=collections.Counter(g['municipality'] for n in candidates for _,g in by_node[n]); witnessmun=collections.Counter(x['current_group_municipality'] for x in w)
receipt={'input_sha256':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},'current_generatedAt':d['generatedAt'],'candidate_nodes':len(candidates),'witness_exact_archive_and_current_group_matches':len(w),'candidate_groups':len(inv),'candidate_poles':sum(len(g['stops']) for n in candidates for _,g in by_node[n]),'candidate_poles_with_node_prefix_mismatch':sum(s['id'].split('/')[0]!=str(n) for n in candidates for _,g in by_node[n] for s in g['stops']),'candidate_groups_with_missing_or_zero_cis':sum(g.get('cis') in (None,'',0) for n in candidates for _,g in by_node[n]),'groups_per_candidate_node':dict(sorted(counts.items())),'candidate_node_group_municipalities':dict(mun),'witness_municipalities':dict(witnessmun),'cross_node_keys':summary,'definitions':'Collisions compare exact field values across all source records and report keys involving >=1 candidate node; normalized names use Unicode NFKC, casefold and whitespace normalization. Coordinates compare exact numeric lat/lon of poles. CIS zero or missing is excluded. None of these alone authorizes a merge.'}
(H/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps(receipt,ensure_ascii=False,indent=2))
