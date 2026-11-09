"""Protect primary science and compare the current age-contrast page to Git."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,tempfile
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v148_documentation';BASE='e900096'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=P)
def main():
 O.mkdir(exist_ok=True);a=read(R/'results/task4_v148_age_contrast/verification.json');s=read(R/'results/task4_v148_age_contrast/summary.json');assert a['status']=='pass' and a['finite_interior_witnesses']==2
 for n,h in {**a['protected_scientific_sha256'],**a['result_sha256'],**s['source_sha256']}.items():assert sha(R/n)==h,n
 assert sha(R/'scripts/audit_task4_v148_age_contrast.py')==a['verifier_sha256']
 assets='drafts/task4_v137_assets/';previous=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets,'drafts/task4_v147_source_review'],cwd=P,text=True).splitlines()
 retained=[n for n in previous if not n.startswith(assets) or Path(n).name not in {'manifest.json','qa.json','README.md'}]
 retained+=['drafts/task4_v137_generated.tex']+[f'drafts/task4_v137_{x}.tex' for x in ['paper','front','conclusion','news','ai','references']]
 for n in retained:assert (P/n).read_bytes()==old(n),n
 m=read(P/assets/'manifest.json');q=read(P/assets/'qa.json');pdf=P/'drafts/task4_v137_paper.pdf'
 assert m['documentation_revision']==q['documentation_revision']=='V148'
 for n,h in m['source_hashes'].items():assert sha(R/n)==h,n
 for n,h in m['protected_files'].items():assert sha(P/n)==h,n
 for n,h in m['manuscript_source_sha256'].items():assert sha(P/'drafts'/n)==h,n
 for dest,src in [('age_joint_summary.json','summary.json'),('age_joint_verification.json','verification.json'),('age_joint_witnesses.csv','witnesses.csv')]:assert (P/assets/dest).read_bytes()==(R/'results/task4_v148_age_contrast'/src).read_bytes(),dest
 assert sha(P/assets/'age_joint.tex')==m['generated_age_joint_sha256']
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);flat=' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',text).split())
 for claim in ['0.23330','0.26325','0.23842','0.20848','retained 2012 aggregate uncertainty set','not observed age effects','16.08933','14.47%']:assert claim in flat,claim
 assert q['technical_checks']=='pass' and q['all_pages_rendered_and_visually_reviewed'] and not q['submission_ready']
 assert (q['total_pages'],q['main_pages_including_news_and_references'],q['news_pages'],q['ai_report_pages'])==(24,22,[16,17],[23,24]) and sha(pdf)==q['pdf_sha256']
 with tempfile.TemporaryDirectory(prefix='himcm-v148-',dir='/data/scratch') as tmp:
  tmp=Path(tmp);(tmp/'previous.pdf').write_bytes(old('drafts/task4_v137_paper.pdf'))
  subprocess.run(['pdftoppm','-r','95','-png',str(tmp/'previous.pdf'),str(tmp/'old')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  subprocess.run(['pdftoppm','-r','95','-png',str(pdf),str(tmp/'new')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  changed=[]
  for page in range(1,25):
   left=Image.open(tmp/f'old-{page:02}.png').convert('RGB');right=Image.open(tmp/f'new-{page:02}.png').convert('RGB')
   if left.size!=right.size or ImageChops.difference(left,right).getbbox():changed.append(page)
 assert changed==[14],changed
 for n,dst in [('manifest.json','paper_manifest.json'),('qa.json','paper_qa.json')]:shutil.copyfile(P/assets/n,O/dst)
 for n,dst in [('himcm_v148_compile.txt','compiler_stdout_stderr.txt'),('himcm_v148_shared_main.txt','shared_main_compiler_stdout_stderr.txt')]:shutil.copyfile(Path('/data/scratch')/n,O/dst)
 assert 'framework.png' in (O/'shared_main_compiler_stdout_stderr.txt').read_text()
 result=dict(status='pass',documentation_revision='V148',primary_evidence='V136 user16',extensions='V137',primary_data_admissions=0,primary_score_interval_width_reduction=0,protected_scientific_files=len(a['protected_scientific_sha256']),unchanged_previous_assets_and_sections=len(retained),unchanged_owned_sections=['paper','front','conclusion','news','ai','references'],protected_historical_manuscript_files=len(m['protected_files']),selected_age_contrast_copies_verified=3,analytic_joint_bound_verified=True,allocation_grid_points=5151,finite_interior_witnesses=2,all_24_final_pages_rendered_and_visually_reviewed=True,render_dpi=95,full_page_inspection=14,previous_overleaf_commit=BASE,changed_PDF_pages_vs_git=changed,pixel_identical_PDF_pages=23,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),shared_main_build='failed at existing missing framework.png; sources unchanged',submission_ready=False,remaining_requirements=q['remaining_requirements'],public_github_push='held pending existing user choice',delivery_sha256={p.name:sha(p) for p in O.iterdir() if p.name not in ['audit.json','sync.json']},verifier_sha256=sha(Path(__file__)))
 (O/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not k.endswith('sha256')},indent=2))
if __name__=='__main__':main()
