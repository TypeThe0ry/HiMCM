"""Recover omitted Phoenix roster schools using official NCES IDs, never name alone."""
import csv,json,re,hashlib,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
P=Path(__file__).resolve().parent;D=P.parent
sources=[D/'task4_v9_phoenix/phoenix_search.json',D/'task4_v42_phoenix_coverage/phoenix_secondary_roster.csv',D/'task4_v92_phoenix/school_audit.csv',D/'task4_v92_phoenix/verified_grade11_observations.csv']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open()))
def main():
 directory=P/'entity_list_2025.json';directory_url='https://azreportcards.azed.gov/api/Entity/GetEntityList?fiscalYear=2025'
 if not directory.exists():
  r=subprocess.run(['curl','--fail','--silent','--show-error','--max-time','35',directory_url],capture_output=True,check=True);json.loads(r.stdout);directory.write_bytes(r.stdout)
 (P/'directory_source.json').write_text(json.dumps(dict(file=directory.name,url=directory_url,sha256=sha(directory),requested_year=2025,returned_years=sorted({r['fiscalYear'] for r in json.loads(directory.read_text())})),indent=2)+'\n')
 roster=rows(sources[1]);prior={x['nces_id'] for x in rows(sources[2])};missing=[x for x in roster if x['NCESSCH'] not in prior]
 entities={e['educationOrganizationId']:e for e in json.loads(sources[0].read_text()) if e['educationOrganizationId'] and 'School' in str(e['type'])}
 norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
 candidates={i:e for i,e in entities.items() if any(norm(x['SCH_NAME'])==norm(e['searchTermDescription']) for x in missing)}
 # Name changes only nominate candidates. Official NCES equality is still mandatory.
 for i in [6250,91304,92248,92984,1002102]:candidates[i]=entities[i]
 manifest=[]
 def get(job):
  eid,kind=job;f=P/'responses'/f'{eid}_{kind}.json'
  if kind=='entity':url='https://azreportcards.azed.gov/api/Entity/GetEntity?'+urlencode(dict(id=eid,fiscalYear=2025))
  else:url='https://azreportcards.azed.gov/api/DataApi/Assessment%20DetailsFAY?'+urlencode(dict(reportSection='Assessment DetailsFAY',fiscalYear=2025,educationOrganizationId=eid))
  if not f.exists():
   z=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','35',url],capture_output=True)
   if z.returncode:return None,dict(entity_id=eid,kind=kind,url=url,error=z.stderr.decode()[:160])
   json.loads(z.stdout);f.write_bytes(z.stdout)
  return json.loads(f.read_text()),dict(entity_id=eid,kind=kind,url=url,file=str(f.relative_to(P)),sha256=sha(f),bytes=f.stat().st_size)
 with ThreadPoolExecutor(max_workers=6) as pool:out=list(pool.map(get,[(i,'entity') for i in candidates]))
 matching={};audit=[];missingids={x['NCESSCH']:x for x in missing}
 for data,meta in out:
  manifest.append(meta);e=data[0] if isinstance(data,list) and len(data)==1 else {};n=(str(e['leances'])+str(e['nces']).zfill(5)) if e.get('leances') is not None and e.get('nces') is not None else None
  r=dict(entity_id=meta['entity_id'],candidate_name=candidates[meta['entity_id']]['searchTermDescription'],official_nces_id=n,returned_year=e.get('fiscalYear'),matches_uncovered_roster=n in missingids)
  if n in missingids:matching[meta['entity_id']]=missingids[n]
  audit.append(r)
 assert len({x['NCESSCH'] for x in matching.values()})==len(matching)
 with ThreadPoolExecutor(max_workers=6) as pool:out=list(pool.map(get,[(i,'assessment') for i in matching]))
 observations=[];coverage=[]
 for data,meta in out:
  manifest.append(meta);eid=meta['entity_id'];s=matching[eid];selected=[]
  if isinstance(data,list):
   assert all(x['educationOrganizationId']==eid and x['fiscalYear']==2025 for x in data)
   selected=[x for x in data if x['subgroups']=='All' and str(x['grade'])=='11' and x['type']==1]
   assert all(x['fayType']=='ALL ENROLLED' for x in selected)
   assert len({x['subject'] for x in selected})==len(selected)
  observations.extend(dict(nces_id=s['NCESSCH'],school=s['SCH_NAME'],**x) for x in selected)
  coverage.append(dict(nces_id=s['NCESSCH'],school=s['SCH_NAME'],entity_id=eid,ccd_grade11=s['G11'],grade11_subject_rows=len(selected),response_rows=None if data is None else len(data)))
 for name,rs in [('candidate_audit.csv',audit),('new_school_coverage.csv',coverage),('grade11_observations.csv',observations),('remaining_roster.csv',[x for x in missing if x['NCESSCH'] not in {s['NCESSCH'] for s in matching.values()}])]:
  with (P/name).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (P/'reused_sources.json').write_text(json.dumps({str(p.relative_to(D)):sha(p) for p in sources},indent=2)+'\n')
 print(json.dumps(dict(candidates=len(candidates),matched=len(matching),schools_with_grade11=sum(x['grade11_subject_rows']>0 for x in coverage),new_subject_rows=len(observations),failed=sum('error' in m for m in manifest)),indent=2))
if __name__=='__main__':main()
