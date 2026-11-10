"""Inspect six public-school pool pages, preserving access restrictions."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json
P=Path(__file__).resolve().parent
class Page(HTMLParser):
 def __init__(self):super().__init__();self.contacts=[];self.text=[];self.skip=0
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
  if t=='stzh-contact':self.contacts.append(dict(a))
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip and d.strip():self.text.append(' '.join(d.split()))
rows=[]
for r in json.loads((P/'school_retrievals.json').read_text()):
 assert r['status']==200 and r['file']
 b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 q=Page();q.feed(b.decode('utf-8'));text=' '.join(q.text)
 assert len(q.contacts)==1
 c=q.contacts[0]
 assert c['location']=='Zürich' and c['heading'].startswith('Schulschwimmanlage ')
 streets=json.loads(c['street']);assert len(streets)==1
 lead=next(t for t in q.text if t.startswith('Die Schulschwimmanlage liegt'))
 assert 'öffentliches Schwimmen' in lead
 assert 'Schulferien und an schulfreien Tagen' in text and 'geschlossen' in text
 rows.append(dict(slug=r['slug'],name=c['heading'],street=streets[0],postal_code=c['postal-code'],city=c['location'],public_swimming_statement=lead,adult_only_explicit=('für Erwachsene' in lead),partial_women_girls_sessions=('teilweise nur für Frauen und Mädchen' in lead),school_holidays_and_non_school_days_closed=True,individual_teen_access_verified=False,source_url=r['url'],source_file=r['file'],source_sha256=r['sha256'],contact_locator='stzh-contact#kontakt attributes; introductory lead and opening-hours text'))
assert len(rows)==6 and len({r['street'] for r in rows})==6
assert [r['slug'] for r in rows if r['adult_only_explicit']]==['kuegeliloo']
assert {r['slug'] for r in rows if r['partial_women_girls_sessions']}=={'aemtler','riedtli'}
existing=[]
for r in json.loads((P/'existing_retrievals.json').read_text()):
 assert r['status']==200 and r['file']
 b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 q=Page();q.feed(b.decode('utf-8'));assert len(q.contacts)==1
 c=q.contacts[0];streets=json.loads(c['street']);assert len(streets)==1 and c['location']=='Zürich'
 notices=[t for t in q.text if any(v in t.lower() for v in ['geschlossen','defekt'])]
 existing.append(dict(slug=r['slug'],name=c['heading'],street=streets[0],postal_code=c['postal-code'],city=c['location'],source_url=r['url'],source_file=r['file'],source_sha256=r['sha256'],operational_notices=notices,continuous_operation_certified=False))
old=json.loads((P.parents[1]/'data/task4_v118_pools/observations.json').read_text())[0]
assert {r['name'] for r in existing}==set(old['venues']) and len(existing)==7
assert len({r['street'] for r in existing+rows})==13
included=[r for r in rows if not r['adult_only_explicit']]
assert len(included)==5
result=dict(status='pass',six_distinct_school_addresses=True,additional_school_facility_cards=6,rows=rows,existing_seven_addresses=existing,old_seven_address_crosscheck_completed=True,all_thirteen_addresses_unique=True,descriptive_combined_public_facility_directory_targets=13,conservative_candidate=dict(retained_original_names=old['venues'],new_school_names=[r['name'] for r in included],excluded_new_name='Schulschwimmanlage Kügeliloo',exclusion_reason='Publicswimming explicitly adults-only; preserve14–18student-scope caution.',proposed_count=12,previous_count=7,population=440935,population_year=2025,population_source='Originaluserinputunchanged,notindependentlyrevalidated',source_observation='2026-11-10currentdirectorycapture; inventoryreferencedateunstated',interpretation='Conditionalfacilitysupplysubsetwithsomepublicsessions; notallteenagersaccessorcontinuousopening'),candidate_count_not_admitted=True,remaining_checks=['IndependentcandidateandmodelvalidationbeforeanyV192inputchange.','Retainpartialwomen/girlssessionsandschoolholiday/non-schooldayclosures; neitherabsenceofadult-onlylabelnorpubliclabelprovesall14–18access.'],primary_admissions=0,actual_score_width_reduction=0)
(P/'school_candidates.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS:13originaldetailpages/uniqueZurichaddresses;5newcandidatevenues,1adult-onlyexcluded;noadmission')
