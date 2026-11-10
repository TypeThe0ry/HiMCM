#!/usr/bin/env python3
"""Check the compiled review draft; do not equate checks with submission approval."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--render-review-confirmed',action='store_true');a=p.parse_args()
here=Path(__file__).resolve().parent; pdf=here/'task4_v123_paper.pdf'
manifest=json.loads((here/'task4_v123_assets/manifest.json').read_text())
protected=manifest['protected_files']
for name,digest in protected.items(): assert hashlib.sha256((here.parent/name).read_bytes()).hexdigest()==digest,name
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
pages=int(re.search(r'^Pages:\s*(\d+)',info,re.M).group(1))
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
parts=[s for s in text.split('\f') if s.strip()];assert len(parts)==pages
aux=(here/'task4_v123_paper.aux').read_text()
def label(key):
 return int(re.search(r'\\newlabel\{'+key+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
main_end=label('main-end');news_start=label('news-start');news_end=label('news-end')
assert main_end<=25 and 1<=news_end-news_start+1<=2
assert 'Summary Sheet' in parts[0] and 'Contents' in parts[1]
assert 'Report on Use of AI Tools' in parts[main_end]
assert main_end+1==pages # Current one-page documentation appendix.
for i,part in enumerate(parts,1):
 assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of '+str(pages),part),i
assert '[?]' not in text and '??' not in text
log=(here/'task4_v123_paper.log').read_text()
assert not re.search(r'Warning:|Overfull|Underfull|undefined',log)
assert pdf.stat().st_size<20_000_000
assert manifest['minimum_figure_font_inserted_pt']>=12
paper=(here/'task4_v123_paper.tex').read_text()
assert '\\documentclass[12pt]' in paper and 'pdfauthor={}' in paper
assert 'incomplete review record' in (here/'task4_v123_ai.tex').read_text()
qa={'document_status':'independent full review draft, not submission-ready','technical_checks':'pass','total_pages':pages,'main_pages_including_news_and_references':main_end,'news_pages':[news_start,news_end],'ai_report_pages':list(range(main_end+1,pages+1)),'summary_one_page':True,'table_of_contents_includes_news_and_references':all(x in parts[1] for x in ['News article','References']),'control_and_page_headers_all_pages':True,'control_number':'PENDING - not verified','main_font_declared_pt':12,'minimum_final_figure_font_pt':manifest['minimum_figure_font_inserted_pt'],'compilation_warnings':0,'unresolved_reference_markers':False,'pdf_bytes':pdf.stat().st_size,'all_pages_rendered_and_visually_reviewed':a.render_review_confirmed,'render_review_note':'18-page contact sheets and full-size summary, plot and revision pages reviewed; tables kept intact and news split at a section boundary' if a.render_review_confirmed else 'Not confirmed','protected_files_unchanged':protected,'original_user_csv_sha256':manifest['sources']['data/task4_v117_team_intake/city_indicators.csv'],'submission_ready':False,'remaining_requirements':['Verify actual Team Control Number','Confirm all team AI tools/versions and reconcile actual saved query/output records','Team review and specifically authorized integration with shared manuscript'],'shared_main_status':'Unmodified; earlier shared-main build failed at existing missing framework.png','pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest()}
(here/'task4_v123_assets/qa.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:qa[k] for k in ['technical_checks','total_pages','main_pages_including_news_and_references','news_pages','submission_ready']},indent=2))
