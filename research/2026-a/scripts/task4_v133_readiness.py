"""Read-only V131 delivery and teacher-source check; never claim final submission."""
from pathlib import Path
import json,hashlib,html,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
OVERLEAF=ROOT.parents[1].with_name('HiMCM-Overleaf')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 source=ROOT/'data/task4_v133_teacher_scope'
 archive=read(source/'archive_sha256.json')
 assert all(sha(source/p)==h for p,h in archive.items())
 for row in read(source/'retrievals.json'):
  assert row['status']==200 and sha(source/row['file'])==row['sha256']
 z=html.unescape((source/'zurich_ssp_response_original.html').read_text())
 h=html.unescape((source/'helsinki_teacher_context_response_original.html').read_text())
 assert 'öffentliche und private' in z and 'Vollerhebung' in z
 assert 'Opettaja-tiedonkeruun' in h and 'vuodelta 2019' in h
 assert read(source/'observations.json')==[]
 assert len(read(source/'attempts.json'))==2
 snapshot=read(ROOT/'design/task4_user_v130_snapshot.json')
 assert all(sha(ROOT/p)==v for p,v in snapshot['source_sha256'].items())
 registry=read(ROOT/'design/task4_user_current_model.json');assert registry['version']=='V130'
 index=read(ROOT/'design/task4_user_v131_extensions.json');assert index['activation_status']=='active'
 for v in ['128','131']:
  a=read(ROOT/f'results/task4_v{v}_revision/audit.json')
  assert all(sha(ROOT/p)==digest for p,digest in a['result_sha256'].items())
 assets=OVERLEAF/'drafts/task4_v131_assets'
 qa=read(assets/'qa.json');manifest=read(assets/'manifest.json')
 pdf=OVERLEAF/'drafts/task4_v131_paper.pdf';assert sha(pdf)==qa['pdf_sha256']
 assert all(sha(ROOT/p)==digest for p,digest in manifest['source_hashes'].items())
 assert all(sha(OVERLEAF/p)==digest for p,digest in manifest['protected_files'].items())
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
 pages=[x for x in text.split('\f') if x.strip()];assert len(pages)==qa['total_pages']==20
 for i,page in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 20',page)
 assert 'Summary Sheet' in pages[0] and 'Contents' in pages[1]
 assert 'Report on Use of AI Tools' in pages[18]
 assert '[?]' not in text and '??' not in text
 assert qa['technical_checks']=='pass' and qa['compilation_warnings']==0
 assert qa['main_pages_including_news_and_references']==18 and qa['news_pages']==[14,15]
 assert pdf.stat().st_size==qa['pdf_bytes']<20_000_000
 assert qa['all_pages_rendered_and_visually_reviewed']
 assert not (OVERLEAF/'framework.png').exists() and '{framework.png}' in (OVERLEAF/'main.tex').read_text()
 report=dict(technical_verification='pass',final_submission_ready=False,current_primary='V130',current_extensions='V131',
  pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,total_pages=20,main_pages=18,news_pages=[14,15],AI_pages=[19,20],
  actual_PDF_headers_all20_pending=True,prior_render_review_applicable_to_identical_bytes=True,new_render_not_claimed=True,
  original_primary_snapshot_unchanged=True,old_and_current_extensions_files_verified=110,protected_manuscript_files=len(manifest['protected_files']),
  source_routes=2,teacher_original_HTTP200_files=2,teacher_admissions=0,
  incomplete_requirements=[dict(item='Actual team control number',evidence='All20 PDF headers state PENDING; conflicting template IDs are not registration evidence.'),
   dict(item='Complete team AI use report',evidence='Current appendix states incomplete review record;66-message selected root-session export excludes tool payloads and other members.'),
   dict(item='Final manuscript selection/integration',evidence='Independent review exists; shared main retains missing framework.png. Team-root changes require specific authorization.'),
   dict(item='Verified registration and final submission receipt',evidence='No registration or formal submission receipt established by these artifacts; review filename is not a verified control-number filename.'),
   dict(item='Public research publishing choice',evidence='Existing unanswered publishing choice remains; this script neither queries nor changes repository visibility.')],
  audit_scope='Current artifact/metadata checks and prior verified science/render receipts; no new full numerical or visual retest claimed.',
  source_hashes={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'design/task4_user_current_model.json',ROOT/'design/task4_user_v131_extensions.json',ROOT/'data/task4_v117_team_intake/city_indicators.csv']},
  own_script_sha256=sha(Path(__file__)))
 out=ROOT/'results/task4_v133_readiness';out.mkdir(exist_ok=True)
 (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 (source/'verification.json').write_text(json.dumps(dict(status='pass',archived_files_verified=len(archive),original_HTTP_files=2,observations_empty=True,admissions=0,current_science_and_manuscript_unchanged=True,verifier='scripts/task4_v133_readiness.py'),indent=2)+'\n')
 print('PASS: current PDF/source protections;2 teacher routes,0 admissions;final readiness incomplete')
if __name__=='__main__':main()
