"""Read-only source-scope and unsent-request checks; no Helsinki teacher observation."""
from pathlib import Path
import hashlib,json,subprocess
from task4_audit_output import audit_parser,check_output,emit_report
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';D=R/'data/current_helsinki_staff_scope';O=R/'results/current_helsinki_staff_review/verification.json'
a=audit_parser(__doc__).parse_args();check_output(a,O,G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
r=read(D/'retrieval.json');scope=read(D/'scope.json');pdf=D/r['saved_as'];assert pdf.stat().st_size==r['bytes']==771089 and sha(pdf)==r['sha256']==scope['raw_pdf_sha256']
assert r['http_status'] is None and r['retrieval_utc'] is None and r['final_url'] is None
pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f');assert len(pages)==28 and not pages[-1].strip()
intro=' '.join(pages[2].replace('-\n','').split());assert 'Julkaisun raportit esitetään toimiala-, virasto- ja liikelaitostasolla.' in intro and '31.12.2024' in intro
assert scope['primary_admissions']==scope['actual_primary_width_reduction']==0 and scope['teaching_FTE_by_upper_secondary_school_obtained'] is False
request=R/'design/current_helsinki_teacher_request.md';assert '**not sent**' in request.read_text() and '091' in request.read_text()
core=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];v=read(R/'results/current_paper_review/current_verification.json');extra={}
for k,d in v.items():
 if k.startswith('additional_') and k.endswith('_sha256'):extra.update(d)
assert len(core)==548 and len(extra)==77
for n,h in {**core,**extra,**v['withdrawal_source_sha256']}.items():assert sha(R/n)==h,n
for n,h in v['current_files_sha256'].items():assert sha(P/n)==sha(G/'paper/current'/n)==h,n
f,l,h=revised_bounds();i=f.city.tolist().index('Helsinki');j=NAMES.index('upper_secondary_ptr');assert l[i,j]==0 and h[i,j]==1
sources=[*sorted(x for x in D.iterdir() if x.is_file()),request,Path(__file__),R/'scripts/task4_audit_output.py']
report={'status':'pass scoped source review','PDF_bytes_checked':771089,'PDF_pages_checked':27,'reporting_unit_page':3,'HTTP_status_and_exact_UTC_recorded':False,'requests_sent':0,'matched_teaching_FTE_obtained':False,'primary_admissions':0,'actual_primary_width_reduction':0,'core_bindings_checked':548,'supplemental_bindings_checked':77,'withdrawal_evidence_entries_checked':len(v['withdrawal_source_sha256']),'paper_dependencies_each_copy':7,'source_sha256':{str(x.relative_to(R)):sha(x) for x in sources},'scope':'Original appendix body and reporting scope verified; no inferred retrieval status/time, teacher ratio, city subset bound or claim that no other source exists. Unsent request supplies no observation.'}
emit_report(report,a,O,G)
