"""Check current evidence and pending gates without certifying prose quality."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v156_readiness'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def rows(p):return list(csv.DictReader(p.open()))
def normal(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',s).split())
def main():
 s=read(O/'summary.json');items=rows(O/'requirements.csv');assert len(items)==len({r['id'] for r in items})==s['requirements']==40
 assert Counter(r['status'] for r in items)==s['status_counts']
 pdf=P/'drafts/task4_v154_paper.pdf';assert sha(pdf)==s['pdf_sha256'] and pdf.stat().st_size==s['pdf_bytes']<20_000_000
 info=subprocess.check_output(['pdfinfo',str(pdf)],text=True);author=re.search(r'^Author:[ \t]*(.*)$',info,re.M);assert author is None or not author.group(1).strip()
 pages=[normal(x) for x in subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f') if x.strip()];assert len(pages)==s['total_pages']==24
 assert 'Summary Sheet' in pages[0] and 'Contents' in pages[1] and 'Report on Use of AI Tools' in pages[22]
 for i,p in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 24',p),i
 assert (s['main_pages'],s['news_pages'],s['ai_pages'])==(22,[16,17],[23,24]) and s['main_remaining_page_allowance']==3
 # These checks locate the passage evidence; they do not validate the meaning.
 for r in items:
  selected=[int(p)-1 for p in r['pdf_pages'].split(',') if p]
  for marker in json.loads(r['passage_markers']):assert any(normal(marker).lower() in pages[p].lower() for p in selected),(r['id'],marker)
 pending={r['id']:r for r in items};required={'CI-control':'unverified','CI-headers':'partial','CI-anonymity':'unverified','AI-complete-record':'unverified','AI-tool-disclosure':'partial','PA-ai-section':'partial','U-source-quality':'partial','TEAM-integration':'awaiting_team','TEAM-shared-build':'not_ready','REG-eligibility':'unverified','SUB-filename':'awaiting_team','SUB-upload':'not_performed','SUB-confirmation':'unverified','PUB-sharing':'awaiting_team'}
 for key,state in required.items():assert pending[key]['status']==state,(key,pending[key]['status'])
 assert not s['submission_ready'] and 'incomplete review record' in pages[22]
 assert pending['TEAM-independent-entry']['status']=='technical_pass'
 proof=read(R/'results/task4_v154_transition/verification.json')
 assert proof['root_local_build_pages']==24 and proof['root_local_text_matches'] and not proof['online_compile_verified']
 assert sha(pdf)==proof['pdf_sha256']
 # No all-glyph 12pt certificate: all smaller math spans remain in the report.
 small=rows(O/'math_script_spans.csv');inventory=rows(O/'font_inventory.csv');assert len(small)==167
 assert sum(int(r['text_spans']) for r in inventory if int(r['rounded_size'])<12)==167
 assert all(r['rounded_size']=='8' and r['font_family'] in {'CMR8','CMMI8','CMSY8'} for r in small)
 assert s['font_inventory']['not_a_blanket_all_glyph_size_certificate']
 assert (P/'drafts/task4_v154_paper.aux').read_text().count(chr(92)+'bibcite{')==47
 citations={key.strip() for block in (P/'drafts/task4_v154_core.tex').read_text().split(chr(92)+'cite{')[1:] for key in block.split('}',1)[0].split(',')}
 supplements=rows(O/'supplement_citation_bridge.csv');assert len(supplements)==22 and all(r['bibkey'] in citations for r in supplements)
 for n,h in s['admission_source_hashes'].items():assert sha(R/n)==h,n
 refresh=read(R/'data/task4_v156_requirements_refresh/retrieval.json');assert len(refresh['responses'])==4
 for x in refresh['responses']:assert x['status']==200 and x['same_bytes_as_v123'] and sha(R/x['archived_original'])==x['sha256']
 for n,h in s['authority_source_sha256'].items():assert sha(R/n)==h,n
 for n,h in s['manuscript_files_unchanged_sha256'].items():assert sha(P/n)==h,n
 frozen=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in frozen.items():assert sha(R/n)==h,n
 assert sha(R/'scripts/task4_v156_readiness.py')==s['generator_sha256']
 for n,h in s['result_sha256'].items():assert sha(R/n)==h,n
 ranks=rows(R/'results/task4_user_v154_revision/current_ranks.csv')
 for ref in ['fixed','equal']:
  selected=[r for r in ranks if r['weight_reference']==ref];assert len(selected)==16 and all(r['possible_champion']=='True' and r['necessary_champion']=='False' for r in selected)
  assert [r['city'] for r in selected if float(r['decision_rank'])==1]==['Zurich']
 shared=R/'results/task4_v154_transition/shared_main_compiler_stdout_stderr.txt';assert 'framework.png' in shared.read_text() and not (P/'framework.png').exists()
 assert s['deadlines_asia_singapore']=={'stop_work':'2026-11-18T09:00:00+08:00','upload_by':'2026-11-18T10:00:00+08:00','recommended_portal_receipt_check':'2026-11-19T09:00:00+08:00'}
 old_items={r['id']:r for r in rows(R/'results/task4_v149_readiness/requirements.csv')}
 assert len(old_items)==39 and set(pending)-set(old_items)=={'TEAM-independent-entry'}
 assert all(pending[k]['status']==v['status'] for k,v in old_items.items())
 result=dict(status='pass',iteration='V156',paper_documentation_revision='V154',requirements_checked=40,hard_pending_states_preserved=len(required),protected_scientific_files=len(frozen),unchanged_manuscript_files=len(s['manuscript_files_unchanged_sha256']),paper_pdf_sha256=s['pdf_sha256'],official_responses_refreshed_and_unchanged=4,reference_count=47,admitted_supplements_with_core_citations=22,small_math_script_spans_reported=167,primary_data_admissions=0,manuscript_changed=False,PDF_authored=False,submission_ready=False,scope='Integrity, dimensions, passage locations, preserved pending gates and selected current claims checked. Not an independent semantic, all-source, full-team-identity or COMAP compliance certificate.',source_sha256={str(p.relative_to(R)):sha(p) for p in [R/'scripts/task4_v156_readiness.py',R/'data/task4_v156_requirements_refresh/retrieval.json']},result_sha256={str(p.relative_to(R)):sha(p) for p in [O/'summary.json',O/'requirements.csv',O/'font_inventory.csv',O/'math_script_spans.csv',O/'supplement_citation_bridge.csv']},verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','requirements_checked','hard_pending_states_preserved','protected_scientific_files','unchanged_manuscript_files','submission_ready']},indent=2))
if __name__=='__main__':main()
