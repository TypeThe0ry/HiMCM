"""Archive actual school-level Grade 11 results; no city aggregation or imputation."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv,datetime,hashlib,json,requests
P=Path(__file__).resolve().parent
SCHOOLS={5439:'Central High School',5437:'Trevor Browne High School',969999:'Hope College and Career Readiness Academy'}
SECTIONS=['Assessment DetailsFAY','Assessment Participation Rates']
def get(job):
 eid,section=job
 filename=f'{eid}_'+('assessment' if section==SECTIONS[0] else 'participation')+'.json'
 params=dict(reportSection=section,fiscalYear=2025,educationOrganizationId=eid)
 r=requests.get('https://azreportcards.azed.gov/api/DataApi/'+section,params=params,timeout=30)
 r.raise_for_status();data=r.json();assert isinstance(data,list)
 assert all(x['educationOrganizationId']==eid and x['fiscalYear']==2025 for x in data)
 (P/filename).write_bytes(r.content)
 return dict(file=filename,url=r.url,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
def main():
 with ThreadPoolExecutor(max_workers=3) as ex:manifest=list(ex.map(get,[(i,s) for i in SCHOOLS for s in SECTIONS]))
 for eid in SCHOOLS:
  if eid==5439:
   r=requests.get('https://azreportcards.azed.gov/api/Entity/GetEntity',params=dict(id=eid,fiscalYear=2025),timeout=30);r.raise_for_status()
   q=P/f'{eid}_entity.json';q.write_bytes(r.content)
   manifest.append(dict(file=q.name,url=r.url,bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest()))
  else:
   q=P.parent/'task4_v9_phoenix'/'recovered'/f'{eid}_entity.json'
   manifest.append(dict(file=str(q.relative_to(P.parent)),base='parent_data_directory',bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest(),note='Reused ADE entity response; returned FY2026, identifiers only'))
 (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 rows=[]
 for eid,name in SCHOOLS.items():
  data=json.loads((P/f'{eid}_assessment.json').read_text())
  for row in data:
   if row['subgroups']=='All' and row['grade']=='11' and row['type']==1:
    assert row['fayType']=='ALL ENROLLED'
    rows.append(dict(school=name,**row))
 with (P/'grade11_observations.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
