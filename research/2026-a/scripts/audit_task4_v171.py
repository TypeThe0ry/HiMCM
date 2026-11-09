"""Verify source claims, old-data identity and protected scientific/manuscript state."""
from pathlib import Path
import hashlib,json,subprocess,zipfile,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];O=R/'results/task4_v171_envelope_gate';P=R.parents[2]/'HiMCM-Overleaf'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipts=read(O/'source_manifest.json');success=0;failures=0
for x in receipts:
 if x.get('status')==200:
  f=R/x['research_directory']/x['file'];assert sha(f)==x['sha256'] and f.stat().st_size==x['bytes'];success+=1
 else:assert '404' in x.get('error','');failures+=1
assert (success,failures)==(8,1)
g=read(O/'admission_gate.json')
assert g['admitted_cells']==0 and not g['city_PTR_computed'] and not g['raw_indicator_replaced']
assert g['utility_interval_before']==g['utility_interval_after']==[0,1]
for n,h in g['source_sha256'].items():assert sha(R/n)==h
s=read(R/'data/task4_v171_student_scope/student_scope.json');source=R/'data/task4_v171_student_scope/city_students_original.xlsx'
assert sha(source)==sha(R/'data/task4_v120_education/zurich_students2024.xlsx')==s['source_sha256']
old=read(R/'data/task4_v157_zurich_school/scope_audit.json')['student_workbook']
assert old['upper_secondary']==s['public_upper_secondary']+s['private_upper_secondary']==8581
assert s['public_upper_secondary']==6582 and s['private_upper_secondary']==1999 and not s['new_city_observation']
assert s['extractor_sha256']==sha(R/'data/task4_v171_student_scope/extract.py')
manual=R/'data/task4_v171_bfs_scope/bfs_SSP_2024_25_manual_original.pdf'
pages=subprocess.check_output(['pdftotext','-layout',str(manual),'-'],text=True).split('\f')
# Independent locators for the operative algebra and timing, not only the source summary.
assert 'C.7/C.8' in pages[18] and 'C.7/C.8' in pages[19]
assert 'Gymnas' in pages[20] and 'getrennt codiert' in ' '.join(pages[20].split())
assert 'koordiniert' in pages[9] and '31. Dezember' in pages[9]
assert 'Fernstudien' in pages[33]
assert 'einschliesslich der Privatschulen' in pages[5]
method_ver=read(R/'data/task4_v171_bfs_scope/verification.json')
assert method_ver['source_scope_sha256']==sha(R/'data/task4_v171_bfs_scope/source_scope.json')
assert method_ver['extractor_sha256']==sha(R/'data/task4_v171_bfs_scope/extract.py')
science=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
for n,h in science.items():assert sha(R/n)==h,n
protected=read(O/'protected_files.json')['manuscript']
for n,h in protected.items():assert sha(P/n)==h,n
ref=read(O/'model_comparison_reference.json');assert sha(R/ref['referenced_file'])==ref['sha256']
assert all(c['mean_width_reduction']==0 and c['possible_champions']==16 for c in ref['comparison'])
result=dict(version='V171',passed=True,successful_HTTP_responses=success,failed_HTTP_attempts=failures,
 dataset_catalogue_response='HTTP200 application shell only; no new pupil metadata inferred',
 scientific_files_unchanged=len(science),existing_overleaf_files_unchanged=len(protected),
 student_workbook_identical_to_V120=True,existing_V157_stage_counts_reused=True,
 SSP_formula_and_stage_dates_independently_located=True,
 rendered_source_review='Manual PDF20 reviewed at full-page size',
 source_independent_review='education reviewed SSP manual/profile; root independently checked formula, timing and source hashes',
 primary_data_admissions=0,primary_score_width_reduction=0,
 model_recomputed_this_iteration=False,comparison='Frozen V170 comparison reused under unchanged science hashes',
 primary_science='V154 unchanged',current_paper='V168 unchanged',new_paper_PDF=False,goal='active')
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
