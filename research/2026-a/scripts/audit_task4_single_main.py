"""Verify current single-entry manuscript against the independently audited migration."""
from pathlib import Path
import json,re,shutil,sys,tempfile
import task4_v198_reproduce as b
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';C=G/'paper/current';A=G/'paper/history/overleaf_before_single_main_20261110';O=R/'results/task4_v201_review';B=Path('/data/scratch/himcm-single-overleaf-actual')
def main():
 archived=json.loads((G/'paper/history/overleaf_before_single_main_20261110_manifest.json').read_text())
 for n,h in archived['file_sha256'].items():assert b.sha(A/n)==h,n
 ref=A/'drafts/task4_v201_paper.pdf';actual=B/'main.pdf';assert b.sha(ref)=='18d5e8d535dfed46d81fc4017f0aa09e14c7134200981defc1abcdb8014f96e5'
 pages=b.text_pages(actual);assert len(pages)==27 and pages==b.text_pages(ref)
 with tempfile.TemporaryDirectory(prefix='single-main-proof-',dir='/data/scratch') as t:
  t=Path(t);assert b.pixels(ref,t/'ref')==b.pixels(actual,t/'actual')
 b.layout(actual,B,pages)
 text=(P/'main.tex').read_text();assert not re.search(r'\\input\{',text)
 assert [str(x.relative_to(P)) for x in P.rglob('*.tex') if '.git' not in x.parts]==['main.tex']
 assert not (P/'drafts').exists() and not (P/'archive').exists()
 deps=['main.tex','mcmthesis.cls','ref.bib','figures/identification_matrix.pdf','figures/score_intervals.pdf','figures/country_contrasts.pdf']
 for n in deps:assert (P/n).read_bytes()==(C/n).read_bytes(),n
 for n in ['mcmthesis.cls','ref.bib']:assert (P/n).read_bytes()==(A/n).read_bytes(),n
 for n,h in json.loads((R/'design/task4_user_v200_snapshot.json').read_text())['source_sha256'].items():assert b.sha(R/n)==h,n
 protected=json.loads((O/'protection_snapshot.json').read_text())
 for n,h in protected.items():assert b.sha(A/n)==h,n
 log=(B/'main.log').read_text();assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning']);assert log.count('Underfull')==2
 shutil.copy2(actual,C/'main.pdf');shutil.copy2(B/'main.log',O/'single_main_build.log')
 d=dict(status='pass',version='V201 single current main',primary_model='V200',pdf_sha256=b.sha(C/'main.pdf'),reference_pdf_sha256=b.sha(ref),main_entry='main.tex',main_source_sha256=b.sha(P/'main.tex'),all_pages_text_equal=True,all_pages_render_equal=True,total_pages=27,main_and_references_pages=25,render_dpi=72,underfull_counts=[2,2],reference_keys=57,single_current_tex_entry=True,source_mirror_files=len(deps),current_files_sha256={n:b.sha(P/n) for n in deps},archived_files_checked=len(archived['file_sha256']),team_original_preserved_byte_for_byte=True,team_original_archive='paper/history/overleaf_before_single_main_20261110/archive/team_main_before_owned_entry_20261110/main.tex',ref_class_unchanged=True,server_compile_verified=False,submission_ready=False,scope='Actual single main locally compiled and matched all27text/rendered pages to independently audited V201; original archive and current source mirror checked; no online preview or final acceptance claim')
 (O/'current_verification.json').write_text(json.dumps(d,indent=2)+'\n')
 delivery=json.loads((O/'delivery_verification.json').read_text());delivery.update(pdf_sha256=d['pdf_sha256'],single_main_verification_sha256=b.sha(O/'current_verification.json'),source_layout='Single current main.tex plus three figures; historical V201 sources archived in GitHub',anchor_identity_basis='All27per-page text identities imply same58scoped anchor hits; requirements unchanged')
 (O/'current_delivery_verification.json').write_text(json.dumps(delivery,indent=2)+'\n')
 visual=dict(status='pass',pdf_sha256=d['pdf_sha256'],all27pages_contact_sheets_viewed=True,full_page_visual_checks=[1,6,13,14,15],basis='Reviewed final V201 reference at96dpi; single main matches all27grayscale rendered pages exactly',new_figure_minimum_inserted_pt=[10,12.596899224806203],native_letter_headers_empty_footers=True,display_control_number='18213 provisional',server_compile_verified=False)
 (O/'visual_review.json').write_text(json.dumps(visual,indent=2)+'\n')
 print(json.dumps(dict(status='pass',pdf_sha256=d['pdf_sha256'],archive_files=d['archived_files_checked'],current_source_files=len(deps),pages=27)))
if __name__=='__main__':main()
