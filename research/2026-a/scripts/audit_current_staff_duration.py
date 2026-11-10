"""Read-only source/scope checks for bounded staff-request and national-duration follow-up."""
from pathlib import Path
import hashlib,html,json,math,re,subprocess,sys
from task4_audit_output import audit_parser,check_output,emit_report
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf'
O=R/'results/current_staff_duration_review/verification.json'
a=audit_parser(__doc__).parse_args();check_output(a,O,G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def text(p):return ' '.join(html.unescape(re.sub('<[^>]+>',' ',p.read_text())).split())
science=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];v=read(R/'results/current_paper_review/current_verification.json');extra={}
for k,d in v.items():
 if k.startswith('additional_') and k.endswith('_sha256'):extra.update(d)
assert len(science)==548 and len(extra)==77
for n,h in {**science,**extra}.items():assert sha(R/n)==h,n
for n,h in v['current_files_sha256'].items():assert sha(P/n)==sha(G/'paper/current'/n)==h,n
sources=[];receipts=0
for directory,manifest in [('current_swiss_duration2024','retrievals.json'),('current_zurich_staff_request','retrieval.json')]:
 d=R/'data'/directory
 for row in read(d/manifest):
  b=(d/row['file']).read_bytes();assert row['status']==200 and row['bytes']==len(b) and row['sha256']==hashlib.sha256(b).hexdigest();receipts+=1
 sources.extend(sorted(p for p in d.iterdir() if p.is_file()))
d=R/'data/current_swiss_duration2024';q=read(d/'selected_2024.json');actual=json.loads(subprocess.check_output([sys.executable,str(d/'extract.py')],text=True));assert actual==q
assert q['reference_year']==2024 and q['primary_admissions']==0 and 'Schweiz' in text(d/'asset.html')
rows=q['rows'];total=rows[0]['count_or_mean'];bins=rows[1:6]
assert len(bins)==5 and math.isclose(sum(x['count_or_mean'] for x in bins),total,abs_tol=1e-7)
assert math.isclose(sum(x['share_percent'] for x in bins),100,abs_tol=1e-10)
for row in bins:assert math.isclose(row['share_percent'],row['count_or_mean']/total*100,abs_tol=1e-10)
assert rows[6]['count_or_mean']>0 and rows[6]['share_percent'] is None and rows[7]['share_percent'] is None
z=R/'data/current_zurich_staff_request';scope=read(z/'scope.json');assert scope['decision']=='not_admitted' and scope['requested_aggregate']['status']=='unsent and not received'
assert 'teacher_denominator' in scope['requested_aggregate'] and 'pupil_numerator' in scope['requested_aggregate']
assert 'massgeschneiderte Daten' in text(z/'request_page.html') and 'bista@bi.zh.ch' in text(z/'request_page.html')
pages=subprocess.check_output(['pdftotext','-layout',str(z/'ssp_activity_35956351.pdf'),'-'],text=True).split('\f')
for field in scope['sources']['ssp_activity_35956351.pdf']['page_1']['activity_fields']:assert field in pages[0],field
assert 'Regionalisierungsgrad' in pages[1] and 'Kantone' in pages[1]
assert 'Vollerhebung' in text(z/'survey_coverage.html') and '15. September' in text(z/'survey_coverage.html')
sources.extend([Path(__file__),R/'scripts/task4_audit_output.py',R/'design/task4_current_source_routes.csv'])
report=dict(status='pass',raw_receipts_checked=receipts,national_duration_bins_checked=5,unknown_duration_separate=True,SSP_activity_fields_checked=8,source_requests_sent=0,primary_admissions=0,actual_score_width_reduction=0,core_bindings_checked=len(science),supplemental_bindings_checked=len(extra),paper_dependencies_each_copy=7,source_sha256={str(p.relative_to(R)):sha(p) for p in sources},scope='Archived official source and scope checks; national work-duration bins are not a Zurich observation. A custom aggregate request specification is unsent and supplies no city teaching FTE. All primary and manuscript inputs remain unchanged.')
emit_report(report,a,O,G)
