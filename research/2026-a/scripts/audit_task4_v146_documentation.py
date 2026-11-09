"""Verify citation repair, frozen science and current owned manuscript delivery."""
from pathlib import Path
import hashlib,json,re,subprocess,shutil
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf';OUT=ROOT/'results/task4_v146_documentation';BASE='024f9b6'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=PAPER)
def main():
 OUT.mkdir(exist_ok=True);frozen={}
 for n,k in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(ROOT/n)[k])
 for n,h in frozen.items():assert sha(ROOT/n)==h,n
 coverage=read(ROOT/'results/task4_v146_source_coverage/verification.json');assert coverage['status']=='pass' and coverage['explicit_admitted_citations']==21
 for n,h in {**coverage['source_sha256'],**coverage['result_sha256']}.items():assert sha(ROOT/n)==h,n
 assets='drafts/task4_v137_assets/';previous=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets],cwd=PAPER,text=True).splitlines()
 retained=[n for n in previous if Path(n).name not in {'manifest.json','qa.json','README.md'}]
 retained+=['drafts/task4_v137_generated.tex']+[f'drafts/task4_v137_{x}.tex' for x in ['paper','front','conclusion','news','ai']]
 for n in retained:assert (PAPER/n).read_bytes()==old(n),n
 m=read(PAPER/assets/'manifest.json');q=read(PAPER/assets/'qa.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
 assert m['documentation_revision']==q['documentation_revision']=='V146'
 for n,h in m['source_hashes'].items():assert sha(ROOT/n)==h,n
 for n,h in m['protected_files'].items():assert sha(PAPER/n)==h,n
 for n,h in m['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/n)==h,n
 for n in ['summary.json','admitted_sources.csv','indicator_coverage.csv','cell_coverage.csv','verification.json']:assert (PAPER/assets/('source_coverage_'+n)).read_bytes()==(ROOT/'results/task4_v146_source_coverage'/n).read_bytes(),n
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);flat=' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',text).split())
 for claim in ['5,205','119,740','2,487','8,148','eight teacher-ratio, four transport and three travel','0.23002','0.90473','16.08933','4.966','5.306']:assert claim in flat,claim
 assert q['technical_checks']=='pass' and q['all_pages_rendered_and_visually_reviewed'] and not q['submission_ready']
 assert (q['total_pages'],q['main_pages_including_news_and_references'],q['news_pages'],q['ai_report_pages'])==(24,22,[16,17],[23,24])
 assert sha(pdf)==q['pdf_sha256'] and pdf.stat().st_size==q['pdf_bytes']
 for src,dst in [('manifest.json','paper_manifest.json'),('qa.json','paper_qa.json')]:shutil.copyfile(PAPER/assets/src,OUT/dst)
 for src,dst in [('himcm_v146_compile.txt','compiler_stdout_stderr.txt'),('himcm_v146_shared_main.txt','shared_main_compiler_stdout_stderr.txt')]:shutil.copyfile(Path('/data/scratch')/src,OUT/dst)
 assert 'framework.png' in (OUT/'shared_main_compiler_stdout_stderr.txt').read_text()
 result=dict(status='pass',documentation_revision='V146',primary_evidence='V136 user16',extensions='V137',primary_data_admissions=0,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),unchanged_owned_sections=['paper','front','conclusion','news','ai'],protected_historical_manuscript_files=len(m['protected_files']),selected_coverage_copies_verified=5,explicit_admitted_citations_before=15,explicit_admitted_citations_after=21,independent_cells=160,independent_bounds=320,all_24_final_pages_rendered_and_visually_reviewed=True,render_dpi=95,full_page_inspections=[7,22],previous_overleaf_commit=BASE,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),shared_main_build='failed at existing missing framework.png; team sources unchanged',submission_ready=False,remaining_requirements=q['remaining_requirements'],public_github_push='held pending existing user choice',source_sha256={n:sha(ROOT/n) for n in ['scripts/audit_task4_v146_documentation.py','results/task4_v146_source_coverage/verification.json']},delivery_sha256={p.name:sha(p) for p in OUT.iterdir() if p.name not in {'audit.json','sync.json'}})
 (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not k.endswith('sha256')},indent=2))
if __name__=='__main__':main()
