"""Same-year NCES state-ID linkage, source-byte checks and outcome reconstruction."""
import csv,hashlib,io,json,re,zipfile
from pathlib import Path
P=Path(__file__).resolve().parent;D=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
 with p.open(newline='') as f:return list(csv.DictReader(f))
def write(name,rs):
 with (P/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def main():
 for m in json.loads((P/'manifest.json').read_text()):
  assert 'sha256'in m and sha(P/m['file'])==m['sha256'] and (P/m['file']).stat().st_size==m['bytes']
 for name,h in json.loads((P/'reused_sources.json').read_text()).items():assert sha(D/name)==h
 archive=P/'ccd_sch_029_2425_w_1a_073025.zip';member='ccd_sch_029_2425_w_1a_073025.csv'
 with zipfile.ZipFile(archive) as z:
  assert z.testzip() is None
  raw=z.read(member);directory=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
 assert len({r['NCESSCH']for r in directory})==len(directory)
 byid={r['NCESSCH']:r for r in directory}
 roster=rows(D/'task4_v93_phoenix/roster_coverage.csv');targets=[r for r in roster if r['grade11_category']=='positive' and r['identity_verified']=='False']
 prior=rows(D/'task4_v92_phoenix/verified_grade11_observations.csv')+rows(D/'task4_v93_phoenix/grade11_observations.csv')
 controls={r['nces_id']:r['educationOrganizationId']for r in prior}
 assert len(controls)==100
 for n,eid in controls.items():assert byid[n]['ST_SCHID'].split('-')[-1]==eid
 links=[];new=[];extract=[]
 for r in targets:
  n=r['nces_id'];d=byid[n];assert d['SCHOOL_YEAR']=='2024-2025' and d['ST_LEAID'].startswith('AZ-')
  match=re.fullmatch(r'AZ-(\d+)-(\d+)',d['ST_SCHID']);assert match
  lea,eid=match.groups();assert d['ST_LEAID']=='AZ-'+lea
  data=json.loads((P/'responses'/f'{eid}_assessment.json').read_text());assert isinstance(data,list)
  assert all(x['educationOrganizationId']==int(eid) and x['fiscalYear']==2025 for x in data)
  selected=[x for x in data if x['subgroups']=='All' and str(x['grade'])=='11' and x['type']==1]
  assert all(x['fayType']=='ALL ENROLLED'for x in selected)
  assert len({x['subject']for x in selected})==len(selected)
  current=json.loads((P/'responses'/f'{eid}_entity.json').read_text());c=current[0] if len(current)==1 else {}
  current_nces=(str(c['leances'])+str(c['nces']).zfill(5))if c.get('leances')and c.get('nces')else ''
  links.append(dict(nces_id=n,school=d['SCH_NAME'],directory_year=d['SCHOOL_YEAR'],state_school_id=d['ST_SCHID'],entity_id=eid,ccd_school_type=d['SCH_TYPE_TEXT'],current_entity_rows=len(current),current_entity_year=c.get('fiscalYear',''),current_nces=current_nces,current_nces_matches=current_nces==n,assessment_rows=len(data),grade11_subject_rows=len(selected)))
  new.extend(dict(nces_id=n,school=d['SCH_NAME'],identity_rule='official_2024_25_NCES_state_school_ID',**x)for x in selected)
  extract.append(d)
 assert len(targets)==12 and len({x['nces_id']for x in links})==12
 assert not ({x['nces_id']for x in new}&set(controls))
 combined=prior+new;assert len({(r['nces_id'],r['subject'])for r in combined})==len(combined)
 write('identity_bridge.csv',links);write('directory_target_extract.csv',extract);write('grade11_observations.csv',new)
 # The previous ASDB rows were quarantined, so readmission adds them once.
 previously_raw=rows(D/'task4_v92_phoenix/grade11_observations.csv')
 asdb=[r for r in new if r['nces_id']=='040046302884'];old_asdb=[r for r in previously_raw if r['nces_id']=='040046302884']
 assert len(asdb)==len(old_asdb)==3
 for a in asdb:
  b=next(r for r in old_asdb if r['subject']==a['subject'])
  for k in ['numberTested','percentagePassed','fiscalYear','educationOrganizationId']:assert str(a[k])==b[k]
 subjects={}
 for s in sorted({r['subject']for r in combined}):
  rs=[r for r in combined if r['subject']==s];known=[r for r in rs if r['numberTested']!='' and float(r['numberTested'])>=0];n=sum(float(r['numberTested'])for r in known)
  valid=[r for r in known if r['percentagePassed']!='' and float(r['percentagePassed'])>=0];lower=sum(float(r['numberTested'])*float(r['percentagePassed'])for r in valid)/n
  missing=sum(float(r['numberTested'])for r in known if r not in valid)
  subjects[s]=dict(rows=len(rs),known_test_records=n,unknown_tested_count_rows=len(rs)-len(known),known_count_unknown_rate_mass=missing,published_percentage_descriptor_lower=lower,published_percentage_descriptor_upper=lower+100*missing/n)
 result=dict(main_admitted=False,directory_rows=len(directory),directory_member=member,directory_member_sha256=hashlib.sha256(raw).hexdigest(),directory_year='2024-2025',control_schools_exact_state_id_match=len(controls),new_identity_bridges=len(links),new_schools_with_grade11=len({r['nces_id']for r in new}),new_grade11_subject_rows=len(new),readmitted_prior_quarantined_rows=3,combined_schools_with_grade11=len({r['nces_id']for r in combined}),combined_subject_rows=len(combined),positive_grade11_roster=111,positive_grade11_identity_verified=111,positive_grade11_with_results=99+len({r['nces_id']for r in new}),cted_with_empty_assessment=[r['nces_id']for r in links if r['assessment_rows']==0],subjects=subjects,scope='Published-percentage descriptors for known tested counts in covered public school records; not city/resident pass rates, exact reconstructed pass counts or comparable international test scores.')
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
