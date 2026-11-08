"""Offline hash, identifier and grade-filter audit; no network or ranking mutation."""
import csv,json,hashlib,math
from pathlib import Path
P=Path(__file__).resolve().parent;D=P.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return list(csv.DictReader(p.open()))
def main():
 for f,h in json.loads((P/'reused_sources.json').read_text()).items():assert sha(D/f)==h,f
 manifest=json.loads((P/'manifest.json').read_text())
 for m in manifest:assert sha(P/m['file'])==m['sha256']
 directory=json.loads((P/'directory_source.json').read_text());assert sha(P/directory['file'])==directory['sha256']
 old=read(D/'task4_v92_phoenix/verified_grade11_observations.csv');new=read(P/'grade11_observations.csv');coverage=read(P/'new_school_coverage.csv');roster=read(D/'task4_v42_phoenix_coverage/phoenix_secondary_roster.csv');prior=read(D/'task4_v92_phoenix/school_audit.csv')
 for s in coverage:
  eid=s['entity_id'];e=json.loads((P/'responses'/f'{eid}_entity.json').read_text())[0]
  assert str(e['leances'])+str(e['nces']).zfill(5)==s['nces_id']
  raw=json.loads((P/'responses'/f'{eid}_assessment.json').read_text());select=[r for r in raw if r['subgroups']=='All' and str(r['grade'])=='11' and r['type']==1]
  extracted=[r for r in new if r['educationOrganizationId']==eid]
  assert len(select)==len(extracted)==int(s['grade11_subject_rows'])
  for r in select:
   assert r['fiscalYear']==2025 and r['fayType']=='ALL ENROLLED'
   q=[x for x in extracted if x['subject']==r['subject']];assert len(q)==1
   for k,v in r.items():assert q[0][k]==('' if v is None else str(v)),(eid,k)
 assert not ({x['nces_id'] for x in old}&{x['nces_id'] for x in new})
 combined=old+new;assert len({(x['nces_id'],x['subject']) for x in combined})==len(combined)
 verified={s['nces_id'] for s in prior if s['identity_verified']=='True'}|{s['nces_id'] for s in coverage}
 observed={s['nces_id'] for s in combined};cs=[]
 for r in roster:
  g=int(r['G11']);cs.append(dict(nces_id=r['NCESSCH'],school=r['SCH_NAME'],ccd_grade11=g,grade11_category='positive' if g>0 else ('zero' if g==0 else 'not_positive_or_unknown_code'),identity_verified=r['NCESSCH'] in verified,grade11_results_observed=r['NCESSCH'] in observed))
 with (P/'roster_coverage.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(cs[0]));w.writeheader();w.writerows(cs)
 result=dict(main_admitted=False,new_identity_verified_schools=len(coverage),new_schools_with_grade11=len({x['nces_id'] for x in new}),new_subject_rows=len(new),combined_schools_with_grade11=len(observed),combined_subject_rows=len(combined),roster_schools=len(roster),verified_roster_schools=len(verified),coverage_by_grade11={},subjects={})
 for category in sorted({x['grade11_category'] for x in cs}):
  subset=[x for x in cs if x['grade11_category']==category];result['coverage_by_grade11'][category]=dict(roster=len(subset),identity_verified=sum(x['identity_verified'] for x in subset),with_results=sum(x['grade11_results_observed'] for x in subset))
 for subj in sorted({x['subject'] for x in combined}):
  rs=[r for r in combined if r['subject']==subj]
  known=[r for r in rs if r['numberTested'] and float(r['numberTested'])>=0];n=sum(float(r['numberTested']) for r in known)
  unknown_rate=[r for r in known if not r['percentagePassed'] or float(r['percentagePassed'])<0]
  lower=sum(float(r['numberTested'])*float(r['percentagePassed']) for r in known if r not in unknown_rate)/n
  mass=sum(float(r['numberTested']) for r in unknown_rate)
  result['subjects'][subj]=dict(rows=len(rs),known_tested_count_rows=len(known),known_test_record_count=n,unknown_tested_count_rows=len(rs)-len(known),unknown_rate_rows=sum(not r['percentagePassed'] or float(r['percentagePassed'])<0 for r in rs),known_count_unknown_rate_mass=mass,published_percentage_descriptor_lower=lower,published_percentage_descriptor_upper=lower+100*mass/n)
 result['scope']='Current NCES-identifier linkage to 2024-25 Phoenix-boundary CCD roster; FY2025 grade11 assessment records; not resident/citywide pass rate, no cross-city assessment calibration.'
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
