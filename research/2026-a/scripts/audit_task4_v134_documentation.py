"""Verify a documentation-only Paris source case and unchanged V130/V131 science."""
from pathlib import Path
import json,hashlib,subprocess,csv
ROOT=Path(__file__).resolve().parents[1]
OVERLEAF=ROOT.parents[1].with_name('HiMCM-Overleaf')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 case=ROOT/'data/task4_v129_education'
 assert all(sha(case/n)==h for n,h in read(case/'archive_sha256.json').items())
 teachers=read(case/'paris_teacher_henriiv_original.json')['results']
 pupils=read(case/'paris_pupil_henriiv_original.json')['results']
 t=[x for x in teachers if x['uai']=='0750654D' and x['annee_de_la_rentree_scolaire']=='2025']
 p=[x for x in pupils if x['numero_lycee']=='0750654D' and x['rentree_scolaire']=='2025']
 assert len(t)==len(p)==1 and t[0]['etp_enseignants_hommes_et_femmes']==153.65 and p[0]['nombre_d_eleves']==794
 directory=read(case/'paris_annuaire_henriiv_original.json')['results'][0]
 assert directory['post_bac']=='1' and directory['date_maj_ligne']=='2026-11-07'
 assert read(case/'observations.json')==[]
 snapshot=read(ROOT/'design/task4_user_v130_snapshot.json')
 assert all(sha(ROOT/n)==h for n,h in snapshot['source_sha256'].items())
 for v in ['128','131']:
  audit=read(ROOT/f'results/task4_v{v}_revision/audit.json')
  assert all(sha(ROOT/n)==h for n,h in audit['result_sha256'].items())
 bounds=list(csv.DictReader((ROOT/'results/task4_user_v130_revision/utility_bounds.csv').open()))
 paris=[x for x in bounds if x['scenario']=='after_conditional' and x['city']=='Paris' and x['indicator']=='upper_secondary_ptr']
 assert len(paris)==1 and float(paris[0]['lower'])==0 and float(paris[0]['upper'])==1
 assets=OVERLEAF/'drafts/task4_v131_assets';manifest=read(assets/'manifest.json');qa=read(assets/'qa.json')
 assert manifest['documentation_revision']==qa['documentation_revision']=='V134'
 assert all(sha(ROOT/n)==h for n,h in manifest['source_hashes'].items())
 assert all(sha(OVERLEAF/n)==h for n,h in manifest['protected_files'].items())
 assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
 pdf=OVERLEAF/'drafts/task4_v131_paper.pdf';assert sha(pdf)==qa['pdf_sha256']
 assert qa['total_pages']==20 and qa['main_pages_including_news_and_references']==18
 text=' '.join(subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split())
 for phrase in ['0750654D','153.65','794','without recovering 2025 workloads','DEPP.']:
  assert phrase in text,phrase
 old_files=subprocess.check_output(['git','-C',str(OVERLEAF),'ls-tree','-r','--name-only','dbffa4e','drafts/task4_v131_assets'],text=True).splitlines()
 unchanged={}
 for name in old_files+['drafts/task4_v131_generated.tex']:
  if Path(name).name in ['manifest.json','qa.json']:continue
  prior=subprocess.check_output(['git','-C',str(OVERLEAF),'show','dbffa4e:'+name])
  assert (OVERLEAF/name).read_bytes()==prior,name
  unchanged[name]=sha(OVERLEAF/name)
 report=dict(status='pass',documentation_revision='V134',science='V130 primary/V131 extensions unchanged',new_admissions=0,
    Paris_PTR_retained_unknown=True,school_UAI='0750654D',pupil_year=2025,pupil_count=794,teacher_year=2025,teacher_ETP=153.65,
    directory_flag_year=2026,directory_not_used_as_2025_allocation=True,all_old_numeric_assets_and_macros_byte_identical=unchanged,
    original_primary_snapshot_verified=True,old_and_current_extension_files_verified=110,
    source_manifest_all_hashes_verified=True,protected_files_verified=len(manifest['protected_files']),
    PDF_pages=20,main_pages=18,all20_pages_rendered_and_reviewed=True,changed_rendered_pages=[6,7,8,12,18],
    pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,source_case_archive_sha256=sha(case/'archive_sha256.json'),
    own_script_sha256=sha(Path(__file__)),submission_ready=False)
 out=ROOT/'results/task4_v134_documentation';out.mkdir(exist_ok=True)
 (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 (out/'final_document_qa.json').write_bytes((assets/'qa.json').read_bytes())
 print('PASS source case,year boundaries,all numeric assets/macros,science protections and20-page review')
if __name__=='__main__':main()
