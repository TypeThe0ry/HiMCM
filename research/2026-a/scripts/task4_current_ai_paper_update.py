"""Integrate a reviewed AI-only appendix update; preserve V204 scientific proof."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess
import task4_v198_reproduce as base
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';O=R/'results/current_ai_continuation2_paper';C=R/'results/current_paper_review';B=Path('/data/scratch/himcm-ai-continuation2-build')
BASE='e325aed443f3426463801ebe08d52ce342adbfb3'
sha=base.sha;read=base.read
write=lambda p,d:p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 previous=O/'prior_current_verification.json'
 if not previous.exists():shutil.copyfile(C/'current_verification.json',previous)
 old=read(previous);text=(P/'main.tex').read_bytes();before=subprocess.check_output(['git','show',BASE+':main.tex'],cwd=P)
 marker=b'\\section*{Report on Use of AI Tools}';assert text.count(marker)==before.count(marker)==1 and text.split(marker)[0]==before.split(marker)[0]
 for n,h in old['current_files_sha256'].items():
  if n!='main.tex':assert sha(P/n)==h and (P/n).read_bytes()==subprocess.check_output(['git','show',BASE+':'+n],cwd=P)
 peer=read(O/'peer_review.json');assert peer['status']=='PASS' and peer['paper_main_sha256']==sha(P/'main.tex') and peer['candidate_pdf_sha256']==sha(B/'main.pdf')
 pixels=read(O/'pixel_comparison.json');assert pixels['equal_pages']==list(range(1,26)) and pixels['baseline_pdf_sha256']==old['pdf_sha256'] and pixels['candidate_pdf_sha256']==sha(B/'main.pdf')
 pages=base.text_pages(B/'main.pdf');assert len(pages)==27
 aux=(B/'main.aux').read_text();label=lambda n:int(re.search(r'\\newlabel\{'+n+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1]);assert label('main-end')==25 and label('LastPage')==27 and len(re.findall(r'\\bibcite\{',aux))==63
 layout=base.layout(B/'main.pdf',O,pages)
 log=(B/'main.log').read_text();assert 'Overfull' not in log and 'undefined' not in log and 'LaTeX Warning' not in log
 snapshot=read(R/'design/task4_user_v204_snapshot.json');science={**snapshot['upstream_source_sha256'],**snapshot['source_sha256']};assert len(science)==658
 for n,h in science.items():assert sha(R/n)==h,n
 # Selected public evidence only; exact root log and selected-text exports stay outside Git.
 inputs=[Path(__file__),R/'data/current_ai_continuation2/session_manifest.json',R/'data/current_ai_continuation2/coverage_summary.json',R/'data/current_ai_continuation2/README.md',R/'scripts/task4_current_ai_coverage_summary.py',R/'results/current_ai_continuation2/verification.json',R/'results/current_ai_continuation2/negative_controls.json',R/'scripts/test_current_ai_continuation2_integrity.py',R/'scripts/task4_v204_ai_delivery.py',O/'peer_review.json',O/'pixel_comparison.json',previous]
 source={str(p.relative_to(R)):sha(p) for p in inputs}
 report=dict(status='pass AI-only integration',source_sha256=source,primary_model='V204 unchanged',paper_baseline=BASE,pre_ai_source_byte_equal=True,unchanged_resource_files=6,unchanged_first25page_pixels_at72dpi=True,total_pages=27,main_and_references_pages=25,reference_keys=63,pdf_sha256=sha(B/'main.pdf'),main_source_sha256=sha(P/'main.tex'),science_bindings_unchanged=658,main_page_margin=0,server_compile_verified=False,submission_ready=False,complete_team_ai_history=False,private_exports_published=False,**layout)
 write(O/'verification.json',report)
 for n in old['current_files_sha256']:shutil.copyfile(P/n,G/'paper/current'/n)
 shutil.copyfile(B/'main.pdf',G/'paper/current/main.pdf')
 proof=read(C/'current_verification.json');proof.update(pdf_sha256=sha(B/'main.pdf'),main_source_sha256=sha(P/'main.tex'),current_files_sha256={n:sha(P/n) for n in old['current_files_sha256']},total_pages=27,main_and_references_pages=25,underfull_counts=[log.count('Underfull')]*2,visual_review_sha256=sha(O/'peer_review.json'),latest_ai_inputs_sha256={n:h for n,h in source.items() if n.startswith(('data/current_ai_continuation2/','results/current_ai_continuation2/','scripts/test_current_ai_continuation2'))},latest_ai_paper_verification='results/current_ai_continuation2_paper/verification.json',latest_ai_paper_verification_sha256=sha(O/'verification.json'),scope='V204 science and first25 rendered pages unchanged from e325aed. Owned AI appendix adds a third authenticated root-log window; 27pages63references, private exports outside Git and incomplete team disclosure retained. Clean-HEAD reproduction recorded separately.')
 delivery=read(C/'delivery_verification.json')
 if delivery['pdf_sha256']==sha(B/'main.pdf'):proof['delivery_audit_sha256']=sha(C/'delivery_verification.json')
 write(C/'current_verification.json',proof)
 p=R/'design/task4_user_current_review.json';review=read(p);review.update(pdf_sha256=sha(B/'main.pdf'),revision='AI-only third-window disclosure; pre-AI source and6resources byte-identical to e325aed; first25 raster pages unchanged.',latest_ai_paper_verification='research/2026-a/results/current_ai_continuation2_paper/verification.json',latest_ai_paper_verification_sha256=sha(O/'verification.json'));write(p,review)
 print(json.dumps(dict(status='pass',pages=27,main_pages=25,first25pages_unchanged=True)))
if __name__=='__main__':main()
