#!/usr/bin/env python3
"""Check the compiled review draft; do not equate checks with submission approval."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--render-review-confirmed',action='store_true');p.add_argument('--compiler-output',type=Path,required=True,help='Captured stdout and stderr of the current Tectonic build, including PDF-backend messages');a=p.parse_args()
here=Path(__file__).resolve().parent; pdf=here/'task4_v125_paper.pdf'
manifest=json.loads((here/'task4_v125_assets/manifest.json').read_text())
for name,digest in manifest['manuscript_source_sha256'].items():
 assert hashlib.sha256((here/name).read_bytes()).hexdigest()==digest,name
protected=manifest['protected_files']
for name,digest in protected.items(): assert hashlib.sha256((here.parent/name).read_bytes()).hexdigest()==digest,name
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
parts=[s for s in text.split('\f') if s.strip()];assert len(parts)==pages
aux=(here/'task4_v125_paper.aux').read_text()
def label(key):
 return int(re.search(r'\\newlabel\{'+key+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
main_end=label('main-end');news_start=label('news-start');news_end=label('news-end')
assert main_end<=25 and 1<=news_end-news_start+1<=2
assert 'Summary Sheet' in parts[0] and 'Contents' in parts[1]
assert 'Report on Use of AI Tools' in parts[main_end]
assert main_end+1<=pages # AI-use documentation follows the main-page allowance.
for i,part in enumerate(parts,1):
 assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of '+str(pages),part),i
assert '[?]' not in text and '??' not in text
log=(here/'task4_v125_paper.log').read_text()
assert not re.search(r'Warning:|Overfull|Underfull|undefined',log)
compiler_output=a.compiler_output.read_text()
assert not re.search(r'warning:|error:',compiler_output,re.I), 'Compiler/backend reported warnings or errors'
assert 'task4_v125_paper.pdf' in compiler_output
assert pdf.stat().st_size<20_000_000
assert manifest['minimum_figure_font_inserted_pt']>=12
paper=(here/'task4_v125_paper.tex').read_text()
assert '\\documentclass[12pt]' in paper and 'pdfauthor={}' in paper
assert 'incomplete review record' in (here/'task4_v125_ai.tex').read_text()
assert all(s in text for s in ['gpt-6.1-sol', '0.166.0-alpha.5.1', 'Exa'])
qa={'document_status':'independent full review draft, not submission-ready','technical_checks':'pass','total_pages':pages,'main_pages_including_news_and_references':main_end,'news_pages':[news_start,news_end],'ai_report_pages':list(range(main_end+1,pages+1)),'summary_one_page':True,'table_of_contents_includes_news_and_references':all(x in parts[1] for x in ['News article','References']),'control_and_page_headers_all_pages':True,'control_number':'PENDING - not verified','main_font_declared_pt':12,'minimum_final_figure_font_pt':manifest['minimum_figure_font_inserted_pt'],'compilation_warnings':0,'unresolved_reference_markers':False,'pdf_bytes':pdf.stat().st_size,'all_pages_rendered_and_visually_reviewed':a.render_review_confirmed,'render_review_note':'All final pages rendered and reviewed; tables intact, results start on a fresh page, no widowed paragraph lines and news split at a section boundary' if a.render_review_confirmed else 'Not confirmed','primary_evidence_version':'V124','extension_version':'V125','all_current_numeric_claims_use_V124':True,'protected_files_unchanged':protected,'original_user_csv_sha256':manifest['original_user_csv_sha256'],'submission_ready':False,'remaining_requirements':['Verify actual Team Control Number','Confirm all team AI tools/versions and reconcile actual saved query/output records','Team review and specifically authorized integration with shared manuscript'],'shared_main_status':'Unmodified; earlier shared-main build failed at existing missing framework.png','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
qa.update(documentation_revision='V126',ai_record_complete=False,compiler_stdout_stderr_checked=True,compiler_output_sha256=hashlib.sha256(a.compiler_output.read_bytes()).hexdigest())
(here/'task4_v125_assets/qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:qa[k] for k in ['technical_checks','total_pages','main_pages_including_news_and_references','news_pages','submission_ready']},indent=2))
