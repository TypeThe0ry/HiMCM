"""Archive FY2025 Grade11 results for the existing matched and recovered Phoenix public schools."""
import csv,datetime,hashlib,json,subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'task4_v9_phoenix/school_matches.json'
ROSTER=HERE.parent/'task4_v42_phoenix_coverage/phoenix_secondary_roster.csv'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 matches=json.loads(SOURCE.read_text());roster={r['NCESSCH']:r for r in csv.DictReader(ROSTER.open())}
 assert len(matches)==64 and len({m['entity_id'] for m in matches})==64
 reused=[SOURCE,ROSTER]
 known={m['entity_id'] for m in matches}
 for f in sorted((HERE.parent/'task4_v9_phoenix/recovered').glob('*_entity.json')):
  data=json.loads(f.read_text());e=data[0] if isinstance(data,list) and len(data)==1 else {}
  if e.get('leances') is None or e.get('nces') is None:continue
  n=str(e['leances'])+str(e['nces']).zfill(5);eid=e['educationOrganizationId']
  if n in roster and eid not in known:
   matches.append(dict(nces_id=n,name=roster[n]['SCH_NAME'],entity_id=eid));known.add(eid);reused.append(f)
 assert len(matches)==71
 assert all(m['nces_id'] in roster for m in matches)
 (HERE/'responses').mkdir(exist_ok=True)
 def request(m,kind):
  eid=m['entity_id'];file=HERE/'responses'/f'{eid}_{kind}.json'
  if kind=='entity':url='https://azreportcards.azed.gov/api/Entity/GetEntity?'+urlencode(dict(id=eid,fiscalYear=2025))
  else:
   section='Assessment DetailsFAY';url='https://azreportcards.azed.gov/api/DataApi/'+section.replace(' ','%20')+'?'+urlencode(dict(reportSection=section,fiscalYear=2025,educationOrganizationId=eid))
  if not file.exists():
   process=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','30',url],capture_output=True)
   if process.returncode:return None,dict(entity_id=eid,kind=kind,url=url,status='failed',error=process.stderr.decode()[:180])
   try:json.loads(process.stdout)
   except ValueError:return None,dict(entity_id=eid,kind=kind,url=url,status='invalid_json')
   file.write_bytes(process.stdout)
  data=json.loads(file.read_text())
  return data,dict(entity_id=eid,kind=kind,file=str(file.relative_to(HERE)),url=url,status='acquired',sha256=sha(file),bytes=file.stat().st_size)
 jobs=[(m,k) for m in matches for k in ['entity','assessment']]
 with ThreadPoolExecutor(max_workers=6) as pool:result=list(pool.map(lambda x:request(*x),jobs))
 manifest=[meta for data,meta in result];responses={(meta['entity_id'],meta['kind']):data for data,meta in result}
 audit=[];observations=[]
 for m in matches:
  eid=m['entity_id'];e=responses[eid,'entity'];a=responses[eid,'assessment'];s=roster[m['nces_id']]
  entity=e[0] if isinstance(e,list) and len(e)==1 else {}
  actual=(str(entity['leances'])+str(entity['nces']).zfill(5)) if entity.get('leances') is not None and entity.get('nces') is not None else None
  verified=actual==m['nces_id']
  rows=[]
  if isinstance(a,list):
   assert all(r['educationOrganizationId']==eid and r['fiscalYear']==2025 for r in a)
   rows=[r for r in a if r['subgroups']=='All' and str(r['grade'])=='11' and r['type']==1]
   assert all(r['fayType']=='ALL ENROLLED' for r in rows)
   assert len({r['subject'] for r in rows})==len(rows)
  for r in rows:
   observations.append(dict(nces_id=m['nces_id'],school=m['name'],identity_verified=verified,**r))
  audit.append(dict(nces_id=m['nces_id'],entity_id=eid,school=m['name'],official_nces_id=actual,identity_verified=verified,
    entity_returned_year=entity.get('fiscalYear'),source_school_year=s['SURVYEAR'],source_grade11=s['G11'],
    response_rows=None if a is None else len(a),grade11_subject_rows=len(rows),subjects='|'.join(r['subject'] for r in rows)))
 for name,rows in [('school_audit.csv',audit),('grade11_observations.csv',observations)]:
  with (HERE/name).open('w') as f:
   writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
 (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 (HERE/'reused_sources.json').write_text(json.dumps({str(p.relative_to(HERE.parent)):sha(p) for p in reused},indent=2)+'\n')
 print(json.dumps(dict(schools=len(audit),verified=sum(r['identity_verified'] for r in audit),grade11_rows=len(observations),failed_requests=sum(r['status']!='acquired' for r in manifest)),indent=2))
if __name__=='__main__':main()
