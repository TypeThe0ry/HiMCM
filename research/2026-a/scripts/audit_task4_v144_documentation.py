"""Verify source-specific paper claims and preserve existing scientific inputs."""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf';OUT=ROOT/'results/task4_v144_documentation';BASE='39b6a35'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=PAPER)
def main():
    frozen={}
    for file,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(ROOT/file)[key])
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    report=read(ROOT/'results/task4_v144_homicide_sensitivity/verification.json');summary=read(ROOT/'results/task4_v144_homicide_sensitivity/summary.json')
    assert report['status']=='pass' and report['independent_city_cases']==128 and report['primary_admissions']==0
    for name,digest in {**summary['source_sha256'],**report['result_sha256']}.items():assert sha(ROOT/name)==digest,name
    assert sha(ROOT/'scripts/audit_task4_v144_homicide.py')==report['verifier_sha256']
    assets='drafts/task4_v137_assets/'
    previous=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets],cwd=PAPER,text=True).splitlines()
    retained=[name for name in previous if Path(name).name not in {'manifest.json','qa.json','README.md','vintage.tex'}]
    retained+=['drafts/task4_v137_generated.tex','drafts/task4_v137_paper.tex','drafts/task4_v137_ai.tex']
    for name in retained:assert (PAPER/name).read_bytes()==old(name),name
    manifest=read(PAPER/assets/'manifest.json');qa=read(PAPER/assets/'qa.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert manifest['documentation_revision']==qa['documentation_revision']=='V144'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['protected_files'].items():assert sha(PAPER/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    for name,digest in manifest['generated_vintage_sha256'].items():assert sha(PAPER/assets/name)==digest,name
    assert sha(PAPER/assets/'revision.tex')==manifest['generated_revision_sha256']
    selected={'homicide_scope.json':'data/task4_v144_homicide/scope_audit.json','homicide_source_verification.json':'data/task4_v144_homicide/verification.json','homicide_summary.json':'results/task4_v144_homicide_sensitivity/summary.json','homicide_verification.json':'results/task4_v144_homicide_sensitivity/verification.json','homicide_cbs_annual_table.json':'data/task4_v144_homicide/cbs_annual_table_extracted.json','homicide_cbs_cells.json':'data/task4_v144_homicide/cbs_cells_extracted.json','homicide_zurich_page117.txt':'data/task4_v144_homicide/zurich_page_117_extracted.txt','homicide_zurich_page118.txt':'data/task4_v144_homicide/zurich_page_118_extracted.txt'}
    for dest,src in selected.items():assert (PAPER/assets/dest).read_bytes()==(ROOT/src).read_bytes(),dest
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);flat=' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',text).split())
    for claim in ['ten provisional homicide victims','totals 68 over 2018','numerator 340','one completed offence in 2024','two in 2025','0.14 still lacks a verified denominator','other 159 entries fixed','16.08933','4.966','5.306']:assert claim in flat,claim
    assert 'no official count is inserted as an assumed replacement rate' in flat.replace('oﬀicial','official')
    assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
    assert qa['total_pages']==23 and qa['main_pages_including_news_and_references']==21 and qa['news_pages']==[16,17] and qa['ai_report_pages']==[22,23]
    assert qa['pdf_sha256']==sha(pdf) and qa['pdf_bytes']==pdf.stat().st_size and qa['compilation_warnings']==0
    assert not qa['submission_ready'] and not qa['ai_record_complete'] and qa['control_number']=='PENDING - not verified'
    assert sha(OUT/'compiler_stdout_stderr.txt')==qa['compiler_output_sha256']
    main_log=(OUT/'shared_main_compiler_stdout_stderr.txt').read_text();assert 'framework.png' in main_log and 'error:' in main_log
    oldpdf=old('drafts/task4_v137_paper.pdf');assert hashlib.sha256(oldpdf).hexdigest()=='f1385f15ea5648fa9ada1d24d54ccab94ad25fe7ba0e3b6c9b324510f2d247b9'
    with tempfile.TemporaryDirectory(prefix='himcm_v144_compare_',dir='/data/scratch') as t:
        p=Path(t);(p/'before.pdf').write_bytes(oldpdf)
        for name,path in [('before',p/'before.pdf'),('after',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(path),str(p/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        before=sorted(p.glob('before-*.png'));after=sorted(p.glob('after-*.png'));assert len(before)==len(after)==23
        changed=[i for i,(a,b) in enumerate(zip(before,after),1) if ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()]
    assert changed==[1,7,8,11,12,13,15,16,17,21],changed
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    for name in ['manifest.json','qa.json']:(OUT/('paper_'+name)).write_bytes((PAPER/assets/name).read_bytes())
    result=dict(status='pass',documentation_revision='V144',primary_evidence='V136',controlled_extensions='V137',primary_data_admissions=0,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),protected_historical_manuscript_files=len(manifest['protected_files']),selected_source_and_check_copies_verified=len(selected),all_23_final_pages_rendered_and_visually_reviewed=True,source_specific_city_cases=128,source_specific_score_bounds=256,previous_overleaf_commit=BASE,changed_PDF_pages_vs_git=changed,pixel_identical_PDF_pages=23-len(changed),pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),paper_qa_sha256=sha(OUT/'paper_qa.json'),shared_main_build='failed at pre-existing missing framework.png; sources unchanged',submission_ready=False)
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
