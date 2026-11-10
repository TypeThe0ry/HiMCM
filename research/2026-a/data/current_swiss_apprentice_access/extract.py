"""Offline, source-bound extraction of EHB pathway/access context; no model writes."""
from pathlib import Path
import csv, hashlib, json, re, subprocess
D=Path(__file__).resolve().parent;R=D.parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';O=R/'results/current_swiss_apprentice_access'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def norm(s):return ' '.join(re.sub(r'(\w)-[ \t]*\n[ \t]*(\w)',r'\1\2',s).replace('’',"'").split())
def main():
 snapshot=read(R/'design/task4_user_v204_snapshot.json')
 frozen={**snapshot['upstream_source_sha256'],**snapshot['source_sha256']}
 protected={R/n:h for n,h in frozen.items()}
 proof=read(R/'results/current_paper_review/current_verification.json')
 protected.update({P/n:h for n,h in proof['current_files_sha256'].items()})
 for p,h in protected.items():assert sha(p)==h,str(p)
 receipts=read(D/'retrievals.json');assert len(receipts)==4
 for rec in receipts:
  p=D/rec['file'];assert rec['status']==200 and p.stat().st_size==rec['bytes'] and sha(p)==rec['sha256']
 pages={}
 for year in [2024,2026]:
  name='mobility2024.pdf' if year==2024 else 'access2026.pdf';p=D/name;assert p.read_bytes().startswith(b'%PDF-')
  text=subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
  pages[year]=[norm(t) for t in text.split('\f') if t.strip()]
 a,b=pages[2024],pages[2026]
 assert len(a)==12 and len(b)==16
 # Explicit population and approximate travel construction, not diary observations.
 assert all(v in a[2] for v in ["188'284","184'964","174'868",'höchstens 25','ab 25 Jahren'])
 assert all(v in a[4] for v in ['tatsächlich besuchte Berufsfachschule nicht','Wohnkanton','am schnellsten erreichbaren Gemeinde'])
 m=re.search(r'beträgt rund (\d+) Minuten, zur Berufsfachschule rund (\d+) Minuten',a[5]);assert m and m.groups()==('39','46')
 s=re.search(r'rund (\d+)% bei den Pendelzeiten zum Betrieb sowie rund (\d+)% bei den Pendelzeiten zur Berufsfachschule',a[6]);assert s and s.groups()==('85','77')
 assert 'nur 1,4%' in a[6] and 'Berufsfachschule 2,1%' in a[6] and 'länger als 120 Minuten' in a[6]
 assert all(v in b[3] for v in ["174'868",'nicht älter als 25','keinerlei Informationen','nicht besetzt werden konnten'])
 assert 'eine Person unter 25 wohnt' in b[4] and 'maximale Pendelzeit von 60' in b[3]
 olten=re.search(r'(\d+) Gemeinden mit ([\d\']+) Ausbildungsbetrieben und ([\d\']+) Lehrstellen in (\d+) Berufen',b[6]);assert olten
 brusio=re.search(r'Hier bilden (\d+) Gemeinden mit (\d+) Ausbildungsbetrieben und (\d+) Lehrstellen in (\d+) Berufen',b[6]);assert brusio
 nums=lambda match:[int(v.replace("'",'')) for v in match.groups()]
 assert nums(olten)==[242,12704,49484,227] and nums(brusio)==[2,24,38,18]
 assert '84% der Suchräume' in b[6] and '4,4% der Jugendlichen' in b[6]
 observations=[]
 def row(source,page,group,metric,value,unit,qualification):observations.append(dict(source=source,physical_page=page,group=group,metric=metric,value=value,unit=unit,qualification=qualification))
 for group,mean,share,tail in [('training_employer',int(m[1]),int(s[1]),1.4),('assigned_vocational_school',int(m[2]),int(s[2]),2.1)]:
  row('mobility2024.pdf',6,group,'approximate_mean_one_way',mean,'minutes','SBG-BUR 2021/22 and intermunicipal public-transport times; school assignment estimated')
  row('mobility2024.pdf',7,group,'approximate_share_under_60_minutes',share,'percent','Published rounded share, not a Zurich-specific distribution or exact 14/18 age cohort')
  row('mobility2024.pdf',7,group,'approximate_share_over_120_minutes',tail,'percent','Figure truncation is not a finite support maximum')
 for group,match in [('Olten',olten),('Brusio',brusio)]:
  for metric,value,unit in zip(['reachable_municipalities','training_employers','filled_training_contracts','occupations'],nums(match),['municipalities','employers','contracts','occupations']):
   row('access2026.pdf',7,group,metric,value,unit,'60-minute assumed public-transport search space; 2021/22 filled dual contracts, not current vacancies')
 row('access2026.pdf',7,'origin_search_spaces','share_over_100_occupations',84,'percent','Origin/search-space denominator, not student-weighted')
 row('access2026.pdf',7,'young_apprentices','share_below_100_occupations',4.4,'percent','Young-apprentice denominator; do not equate with origin-weighted 84 percent')
 O.mkdir(exist_ok=True)
 with (O/'observations.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(observations[0]),lineterminator='\n');w.writeheader();w.writerows(observations)
 summary=dict(primary_admissions=0,actual_primary_width_reduction=0,model='V204 unchanged',reference_school_year='2021/22',report_publication_years=[2024,2026],retained_contracts=174868,not_a_zurich_city_travel_distribution=True,not_exact_14_or_18_age_groups=True,age_definition_note='2024 p3 says entry age at most25 and adult from25; 2026 p4 says entry not older25, p5 origin rule says person under25. Preserve these nonidentical boundaries; no silent harmonization.',school_assignment_note='Fastest eligible school municipality with home-canton preference, not linked actual school attended',travel_note='Intermunicipal average public-transport times, approximate individual commutes',search_space_note='Assumed60-minute reachability over occupied dual training contracts; no unfilled vacancy information',denominator_note='84 percent of search spaces with over100 occupations differs from4.4 percent of young apprentices with below100',original_39_9_minutes_unchanged=True)
 (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 files=[*sorted(p for p in D.iterdir() if p.is_file()),R/'design/task4_user_v204_snapshot.json',R/'data/task4_v117_team_intake/city_indicators.csv']
 assert all(sha(p)==h for p,h in protected.items())
 result=dict(status='pass bounded source extraction',source_sha256={str(p.relative_to(R)):sha(p) for p in files},source_responses=4,PDF_pages={'2024':len(a),'2026':len(b)},extracted_observations=len(observations),output_sha256={n:sha(O/n) for n in ['observations.csv','summary.json']},protected_science_files=len(frozen),protected_paper_dependencies=7,protected_inputs_changed=[],primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,scope='Checks local source integrity, specified passages and numeric selections; does not reproduce underlying confidential SBG-BUR linkage or author travel matrix.')
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','extracted_observations','protected_science_files','primary_admissions']}))
if __name__=='__main__':main()
