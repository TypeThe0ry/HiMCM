"""Match annual under19 participation to annual teacher-main-role records by UKPRN."""
import csv,gzip,hashlib,json,subprocess
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parent
for m in json.loads((P/'reuse_manifest.json').read_text()):
 b=(P/m['path']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
for m in json.loads((P/'manifest.json').read_text()):
 b=(P/m['file']).read_bytes();assert len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256']
 original=gzip.decompress(b) if m['gzip_lossless'] else b
 assert len(original)==m['original_bytes'] and hashlib.sha256(original).hexdigest()==m['original_sha256']
with (P/'../task4_v62_london_colleges/london_provider_matches.csv').open() as f: teachers=list(csv.DictReader(f))
ids={r['provider_ukprn'] for r in teachers};assert len(ids)==9
with gzip.open(P/'under19_participation.csv.gz','rt',encoding='utf-8-sig') as f:
 allrows=list(csv.DictReader(f))
rows=[r for r in allrows if r['year']=='202425' and r['ukprn'] in ids]
assert len(rows)==531 and {r['snapshot'] for r in rows}=={'14'}
# Check each geography tuple is a single row, not repeated geography subtotal.
key=['ukprn','learner_home_region','learner_home_pcon','learner_home_la','learner_home_lad','learner_home_devolved_administration']
assert len({tuple(r[k] for k in key) for r in rows})==len(rows)
with gzip.open(P/'provider_participation.csv.gz','rt',encoding='utf-8-sig') as f:
 summary=[r for r in csv.DictReader(f) if r['academic_year']=='202425' and r['ukprn'] in ids and r['characteristic']=='Total' and r['age_youth_adult']=='Under 19']
assert len(summary)==9
summaries={r['ukprn']:r for r in summary};joined=[]
for r in teachers:
 a=[x for x in rows if x['ukprn']==r['provider_ukprn']]
 total=sum(int(x['et_part_u19']) for x in a)
 london=sum(int(x['et_part_u19']) for x in a if x['learner_home_region_name']=='London')
 rounded=int(summaries[r['provider_ukprn']]['education_and_training'])
 assert abs(total-rounded)<=5
 joined.append(dict(r,academic_year='2024/25',under19_et_participation_reported_sum=total,under19_london_resident_et_reported_sum=london,under19_et_rounded_summary=rounded,geography_rows=len(a)))
with (P/'matched_provider_counts.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(joined[0]),lineterminator='\n');w.writeheader();w.writerows(joined)
with (P/'matched_under19_source_rows.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
text=subprocess.check_output(['pdftotext','-layout',str(P/'metadata.pdf'),'-'],text=True)
(P/'metadata_extract.txt').write_text(text)
assert '2024/25' in text and 'full year' in text and 'Under 19 education and training learner participation' in text
result=dict(academic_year='2024/25',matched_providers=9,source_geography_rows=531,
 reported_under19_et_provider_count_sum=sum(x['under19_et_participation_reported_sum'] for x in joined),
 reported_under19_london_resident_et_provider_count_sum=sum(x['under19_london_resident_et_reported_sum'] for x in joined),
 reported_teacher_main_role_provider_count_sum=sum(int(x['number_staff_hc']) for x in joined),
 same_academic_year=True,same_point_in_time_census=False,full_year_flow_not_point_stock=True,
 under19_is_not_current_upper_secondary_stage=True,main_role_is_not_all_instructional_roles=True,
 city_deduplicated_student_total_identified=False,city_deduplicated_teacher_total_identified=False,
 main_admitted=False,changed_model_cells=0,
 interpretation='Annual provider-level participation and teacher-main-role counts are now matched by UKPRN, but do not establish city upper-secondary enrollment or instructional teacher headcount.',
 under19_status='Statistics in development; published for transparency',
 rounding_check='Each underlying provider sum agrees with rounded provider summary within5; published counts retained without interpreting low/z as0')
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
