#!/usr/bin/env python3
"""Inventory archived PID stop-list links; no mode classification or new retrieval."""
import collections, csv, hashlib, json
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
HERE=Path(__file__).resolve().parent
R=HERE.parent
SRC=R/'task4_v127_prague'
OUT=R.parent/'results/current_prague_bus_node_candidate'
OUT.mkdir(parents=True, exist_ok=True)
requests=json.loads((SRC/'retrieval_requests.json').read_text())
manifest=json.loads((SRC/'manifest.json').read_text())
assert hashlib.sha256((SRC/'retrieval_requests.json').read_bytes()).hexdigest()==manifest['source_hashes']['retrieval_requests.json']
records=[]; hashes={}
for req in requests:
 p=SRC/req['file']; hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
 assert hashes[p.name]==manifest['source_hashes'][p.name]
 data=json.loads(p.read_text()); assert data['success'] is True
 soup=BeautifulSoup(data['html'],'html.parser')
 for i,li in enumerate(soup.select('li.links-col-stop'),1):
  title=li.select_one('a.is-stop'); assert title
  name=title.get_text(' ',strip=True)
  for j,a in enumerate(li.select('span.links-col-stop-hover > a'),1):
   url=a.get('href',''); q=parse_qs(urlparse(url).query)
   if 'node' not in q: raise ValueError((p.name,i,j,url))
   label=a.select_one('span'); assert label
   records.append({'file':p.name,'request_char':req['form']['char'],'locator':f'html li.links-col-stop[{i}] hover a[{j}]','stop_name':name,'node':q['node'][0],'query_name':q.get('nm',[''])[0],'inprague':q.get('inprague',[''])[0],'display_route':label.get_text(' ',strip=True),'timetable_url':url,'flags':'; '.join(img.get('title','') for img in a.select('img'))})
assert len(requests)==21
OUT.joinpath('all_link_occurrences.csv').write_text('',encoding='utf8')
with (OUT/'all_link_occurrences.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=records[0].keys());w.writeheader();w.writerows(records)
byname=collections.defaultdict(set); bynode=collections.defaultdict(set); bykey=collections.defaultdict(set)
for row in records:
 byname[row['stop_name']].add(row['node']); bynode[row['node']].add(row['stop_name'])
 # Exact URL and label/flags, across responses; locator deliberately excluded.
 key=tuple(row[k] for k in ('stop_name','node','query_name','inprague','display_route','timetable_url','flags'))
 bykey[key].add(row['file'])
conflicts={'same_name_different_nodes':{k:sorted(v) for k,v in sorted(byname.items()) if len(v)>1},'same_node_different_names':{k:sorted(v) for k,v in sorted(bynode.items()) if len(v)>1}}
(OUT/'name_node_conflicts.json').write_text(json.dumps(conflicts,ensure_ascii=False,indent=2)+'\n')
receipt={'source':'Archived PID POST responses previously captured 2026-11-09; no new retrieval.', 'request_file_sha256':hashlib.sha256((SRC/'retrieval_requests.json').read_bytes()).hexdigest(),'sha256':hashes,'prior_manifest_hashes_match':True,'responses':len(requests),'link_occurrences':len(records),'distinct_nodes_any_mode':len(bynode),'distinct_stop_names_any_mode':len(byname),'exact_link_records_in_multiple_responses':sum(len(v)>1 for v in bykey.values()),'same_name_different_nodes':len(conflicts['same_name_different_nodes']),'same_node_different_names':len(conflicts['same_node_different_names']),'inprague_not_1':sum(row['inprague']!='1' for row in records),'candidate_bus_node_count':None,'reason':'No archived link-level transport-mode classification located. Any-mode node totals are not a bus subset.'}
(OUT/'receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
