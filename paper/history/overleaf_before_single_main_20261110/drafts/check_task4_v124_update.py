#!/usr/bin/env python3
"""Verify the compiled V124 companion and preservation of frozen manuscripts."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
p=argparse.ArgumentParser();p.add_argument('--render-review-confirmed',action='store_true');a=p.parse_args();here=Path(__file__).resolve().parent
pdf=here/'task4_v124_update.pdf';m=json.loads((here/'task4_v124_assets/manifest.json').read_text())
for name,h in m['protected_manuscript_files'].items():assert hashlib.sha256((here.parent/name).read_bytes()).hexdigest()==h,name
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);pages=[x for x in text.split('\f') if x.strip()]
assert len(pages)==3 and '[?]' not in text and '??' not in text
for i,t in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 3',t)
log=(here/'task4_v124_update.log').read_text();assert not re.search(r'Warning|Overfull|Underfull|undefined',log)
assert all(x in text for x in ['16.18302','16.15002','0.204%','191','V121','V123'])
assert 'not a final submission' in text.replace('\n',' ')
qa=dict(status='pass',artifact='V124 independent evidence companion',pages=3,compiler_warnings=0,unresolved_citations=False,all_pages_rendered_and_visually_reviewed=a.render_review_confirmed,main_font_declared_pt=12,figures='none; no resized text',frozen_V123_and_shared_manuscript_unchanged=True,shared_main_compile={'status':'failed_existing_missing_asset','asset':'framework.png','line':143},source_result_sha256=m['research_sources'],pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),submission_ready=False,scope='New baseline evidence only; V123 complete review and V122 extensions remain explicitly frozen on V121')
(here/'task4_v124_assets/qa.json').write_text(json.dumps(qa,indent=2)+'\n');print(json.dumps({k:qa[k] for k in ['status','pages','all_pages_rendered_and_visually_reviewed','submission_ready']},indent=2))
