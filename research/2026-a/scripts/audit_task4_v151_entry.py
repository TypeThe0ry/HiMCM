"""Verify root proxy build equivalence while preserving the existing paper."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,tempfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v151_shared_entry';SUP=P/'drafts/task4_v151_entry_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--render-review-confirmed',action='store_true');args=ap.parse_args();O.mkdir(exist_ok=True)
 inventory=read(O/'inventory.json');assert inventory['graphics_references']==inventory['missing_graphics']==17 and inventory['available_name_matches']==[]
 for n,h in inventory['source_sha256'].items():assert sha(P/n)==h,n
 assert sha(O/'shared_dependencies.csv')==inventory['inventory_sha256'] and sha(R/'scripts/task4_v151_entry_inventory.py')==inventory['generator_sha256']
 src=P/'task4_review_entry.tex';pdf=SUP/'task4_review_entry.pdf';log=SUP/'task4_review_entry.log';stdout=Path('/data/scratch/himcm_v151_entry_compile.txt')
 assert src.read_text().count('\\RequirePackage{import}')==1 and src.read_text().count('\\import{drafts/}{task4_v137_paper.tex}')==1
 assert not re.search(r'warning:|error:',stdout.read_text(),re.I) and not re.search(r'Warning:|Overfull|Underfull|undefined',log.read_text())
 assert '\\documentclass' not in src.read_text() # Document class comes from the imported real paper, as in the official proxy example.
 qa=read(P/'drafts/task4_v137_assets/qa.json');manifest=read(P/'drafts/task4_v137_assets/manifest.json');assert qa['documentation_revision']==manifest['documentation_revision']=='V148'
 primary=P/'drafts/task4_v137_paper.pdf';assert sha(primary)==qa['pdf_sha256']=='f4e50119defd735828ca34d4427ff54f9bc8b58750ae9f3a87a3c3dca76eb6a8'
 protected={**manifest['protected_files'],**{str(Path('drafts')/n):h for n,h in manifest['manuscript_source_sha256'].items()},'drafts/task4_v137_paper.pdf':qa['pdf_sha256']}
 for n,h in protected.items():assert sha(P/n)==h,n
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);parts=[x for x in text.split('\f') if x.strip()];assert len(parts)==24
 for i,page in enumerate(parts,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 24',page),i
 flat=' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',text).split());assert all(x in flat for x in ['112 point values, 33 partial intervals and 15 fully missing intervals','0.23330','0.26325','16.08933','14.47%'])
 assert 'Super Bowl' not in text and 'Singapore is the conservative recommendation in our current comparison of' not in flat
 end_label=next(line for line in (SUP/'task4_review_entry.aux').read_text().splitlines() if line.startswith(chr(92)+'newlabel{main-end}'));assert end_label.split('}{')[2]=='22'
 with tempfile.TemporaryDirectory(prefix='himcm-v151-compare-',dir='/data/scratch') as td:
  td=Path(td)
  for name,file in [('primary',primary),('proxy',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(file),str(td/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  a=sorted(td.glob('primary-*.png'));b=sorted(td.glob('proxy-*.png'));assert len(a)==len(b)==24
  different=[]
  for i,(x,y) in enumerate(zip(a,b),1):
   left=Image.open(x).convert('RGB');right=Image.open(y).convert('RGB')
   if left.size!=right.size or ImageChops.difference(left,right).getbbox():different.append(i)
 assert different==[8,14],different
 normalize=lambda value:' '.join(value.split())
 old_parts=[x for x in subprocess.check_output(['pdftotext','-layout',str(primary),'-'],text=True).split('\f') if x.strip()]
 assert [normalize(x) for x in old_parts]==[normalize(x) for x in parts]
 fresh=Path('/data/scratch/himcm_v151_probe/project/drafts/task4_v137_paper.pdf')
 with tempfile.TemporaryDirectory(prefix='himcm-v151-fresh-',dir='/data/scratch') as td:
  td=Path(td)
  for name,file in [('direct',fresh),('proxy',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(file),str(td/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  aa=sorted(td.glob('direct-*.png'));bb=sorted(td.glob('proxy-*.png'));assert len(aa)==len(bb)==24
  assert all(ImageChops.difference(Image.open(x).convert('RGB'),Image.open(y).convert('RGB')).getbbox() is None for x,y in zip(aa,bb))
 probe=Path('/data/scratch/himcm_v151_probe/project');probe_log=(probe/'direct_root_probe_stdout.txt').read_text();assert "File `task4_v137_generated.tex' not found" in probe_log and 'No pages of output' in probe_log
 assert (probe/'drafts/task4_v137_paper.tex').read_bytes()==(P/'drafts/task4_v137_paper.tex').read_bytes()
 assert (probe/'drafts/task4_v137_generated.tex').read_bytes()==(P/'drafts/task4_v137_generated.tex').read_bytes()
 frozen={}
 for n,k in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(R/n)[k])
 for n,h in frozen.items():assert sha(R/n)==h,n
 for file,dest in [(stdout,'proxy_compiler_stdout_stderr.txt'),(probe/'direct_root_probe_stdout.txt','direct_root_probe_stdout_stderr.txt')]:shutil.copyfile(file,O/dest)
 result=dict(status='pass',iteration='V151',paper_documentation_revision='V148',primary_evidence='V136 user16',extensions='V137',root_proxy='task4_review_entry.tex',root_proxy_sha256=sha(src),root_proxy_pdf='drafts/task4_v151_entry_review/task4_review_entry.pdf',root_proxy_pdf_sha256=sha(pdf),root_proxy_pdf_bytes=pdf.stat().st_size,primary_pdf_sha256=sha(primary),pages=24,main_pages=22,news_pages=[16,17],ai_pages=[23,24],compilation_warnings=0,compiler='Local Tectonic root-file build; not a verified Overleaf UI compile',proxy_matches_all_24_fresh_direct_pages=True,archived_primary_pixel_identical_pages=22,archived_primary_different_pages=different,all_page_text_matches_archived_primary=True,fresh_direct_build_pdf_sha256=sha(fresh),comparison_dpi=95,all_pages_visually_reviewed=args.render_review_confirmed,missing_shared_graphics=17,original_asset_replacements=0,negative_probe='Direct input from project-root layout fails at missing unqualified task4_v137_generated.tex; no output pages',positive_probe='Official import-package root proxy resolves unchanged owned paper and relative assets',archived_spacing_difference='Two pages have small spacing differences also reproduced by the fresh direct build; no claim of pixel identity to the archived primary PDF',protected_scientific_files=len(frozen),unchanged_manuscript_files=len(protected),scientific_file_sha256=frozen,manuscript_files_unchanged_sha256=protected,primary_data_admissions=0,primary_score_interval_width_reduction=0,shared_team_files_modified=False,project_main_setting_inspected=False,project_main_setting_changed_by_this_iteration=False,submission_ready=False,remaining_gates=['Actual registered control number and identity review','Complete actual team AI history','Specific final-manuscript selection/integration authorization','Unverified Overleaf main-document setting and server compiler state','Final registration/upload/receipt evidence'],source_sha256={str(p.relative_to(R)):sha(p) for p in [O/'inventory.json',O/'shared_dependencies.csv',O/'proxy_compiler_stdout_stderr.txt',O/'direct_root_probe_stdout_stderr.txt']},verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');small={k:v for k,v in result.items() if k not in ['scientific_file_sha256','manuscript_files_unchanged_sha256','source_sha256']};(SUP/'verification.json').write_text(json.dumps(small,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','pages','compilation_warnings','proxy_matches_all_24_fresh_direct_pages','all_pages_visually_reviewed','missing_shared_graphics','submission_ready']},indent=2))
if __name__=='__main__':main()
