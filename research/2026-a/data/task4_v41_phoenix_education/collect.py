"""Collect actual ADE teacher counts, retaining exact NCES ID verification and scope."""
from pathlib import Path
import csv,json,subprocess,hashlib
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode
P=Path(__file__).resolve().parent

def main():
 schools={r['NCESSCH']:r for r in csv.DictReader((P.parent/'task4_v6_phoenix/school_audit.csv').open())}
 matches=json.loads((P.parent/'task4_v9_phoenix/school_matches.json').read_text())
 candidates=[m for m in matches if schools[m['nces_id']]['pure_9_12']=='True']
 (P/'responses').mkdir(exist_ok=True)
 def get(eid,kind):
  path=P/'responses'/f'{eid}_{kind}.json'
  if kind=='teacher':url='https://azreportcards.azed.gov/api/DataApi/Teacher%20Qualification?'+urlencode(dict(reportSection='Teacher Qualification',fiscalYear=2025,educationOrganizationId=eid))
  else:url='https://azreportcards.azed.gov/api/Entity/GetEntity?'+urlencode(dict(id=eid,fiscalYear=2025))
  if not path.exists():
   r=subprocess.run(['curl','--fail','--silent','--show-error','--location','--max-time','25',url],capture_output=True)
   if r.returncode:return None,dict(url=url,status='failed',error=r.stderr.decode()[:150])
   try:data=json.loads(r.stdout)
   except ValueError:return None,dict(url=url,status='invalid_json')
   path.write_bytes(r.stdout)
  else:data=json.loads(path.read_text())
  return data,dict(url=url,file=str(path.relative_to(P)),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),bytes=path.stat().st_size,status='downloaded')
 def fetch(m):
  s=schools[m['nces_id']];eid=m['entity_id'];t,tm=get(eid,'teacher');e,em=get(eid,'entity')
  row=dict(**m,grade_total=s['grade_total'],ccd_member=s['MEMBER'],ccd_fte=s['FTE'],grade_counts_complete=s['valid_grade_counts'],grade_total_matches_membership=s['grade_total_matches_membership'],admitted_main=False)
  ed=e[0] if isinstance(e,list) and len(e)==1 else {}
  row.update(official_nces_id=str(ed.get('leances',''))+str(ed.get('nces','')).zfill(5),entity_returned_year=ed.get('fiscalYear'))
  row['id_verified']=row['official_nces_id']==m['nces_id']
  row['teacher_response_rows']=len(t) if isinstance(t,list) else -1
  if isinstance(t,list) and len(t)==1:
   row.update({k:t[0].get(k) for k in ['teacherCount','teacherAndSchoolLeadersCount','fiscalYear','educationOrganizationId']})
  row['matched_diagnostic']=bool(row['id_verified'] and row.get('teacherCount',-1)>0 and row.get('fiscalYear')==2025 and row.get('educationOrganizationId')==eid and row['grade_counts_complete']=='True' and row['grade_total_matches_membership']=='True')
  return row,[tm,em]
 with ThreadPoolExecutor(max_workers=6) as ex:out=list(ex.map(fetch,candidates))
 rows=[r for r,_ in out];fields=list(dict.fromkeys(k for r in rows for k in r))
 with (P/'school_teacher_audit.csv').open('w') as f:
  w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
 good=[r for r in rows if r['matched_diagnostic']];students=sum(float(r['grade_total']) for r in good);teachers=sum(r['teacherCount'] for r in good);ftes=sum(float(r['ccd_fte']) for r in good if float(r['ccd_fte'])>=0)
 summary=dict(candidate_pure_9_12_schools=len(candidates),exact_official_id_matches=sum(r['id_verified'] for r in rows),matched_diagnostic_schools=len(good),matched_grade_9_12_students=students,reported_teacher_count=teachers,students_per_reported_teacher=students/teachers if teachers else None,ccd_fte_same_subset=ftes,main_model_admission=False,scope='Matched available nonvirtual operational public schools located within current Phoenix boundary, pure grades9-12; not all residents or private schools; year alignment and unique shared-teacher semantics unresolved')
 (P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');(P/'manifest.json').write_text(json.dumps([m for _,ms in out for m in ms],indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
