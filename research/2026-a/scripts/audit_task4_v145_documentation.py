"""Verify the added point-rate interpretation without altering primary evidence."""
from pathlib import Path
import hashlib,json,re,subprocess,tempfile
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf';OUT=ROOT/'results/task4_v145_documentation';BASE='41a91e7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=PAPER)
def main():
    frozen={}
    for name,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(ROOT/name)[key])
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    report=read(ROOT/'results/task4_v145_rate_threshold/verification.json');summary=read(ROOT/'results/task4_v145_rate_threshold/summary.json')
    assert report['status']=='pass' and report['independent_city_cases']==224
    for name,digest in {**summary['source_sha256'],**report['result_sha256']}.items():assert sha(ROOT/name)==digest,name
    assert sha(ROOT/'scripts/audit_task4_v145_rate_threshold.py')==report['verifier_sha256']
    assets='drafts/task4_v137_assets/'
    previous=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets],cwd=PAPER,text=True).splitlines()
    retained=[name for name in previous if Path(name).name not in {'manifest.json','qa.json','README.md','vintage.tex'}]
    retained+=['drafts/task4_v137_generated.tex']+[f'drafts/task4_v137_{x}.tex' for x in ['paper','front','core','conclusion','news','ai','references']]
    for name in retained:assert (PAPER/name).read_bytes()==old(name),name
    manifest=read(PAPER/assets/'manifest.json');qa=read(PAPER/assets/'qa.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert manifest['documentation_revision']==qa['documentation_revision']=='V145'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['protected_files'].items():assert sha(PAPER/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    for name,digest in manifest['generated_vintage_sha256'].items():assert sha(PAPER/assets/name)==digest,name
    assert sha(PAPER/assets/'revision.tex')==manifest['generated_revision_sha256']
    for dest,src in [('rate_threshold_summary.json','summary.json'),('rate_threshold_verification.json','verification.json')]:assert (PAPER/assets/dest).read_bytes()==(ROOT/'results/task4_v145_rate_threshold'/src).read_bytes(),dest
    tex=(PAPER/assets/'vintage.tex').read_text()
    for t in summary['thresholds']:assert f"{t['rate_per100000']:.5f}" in tex
    assert 'point rate $x_Z$' in tex and 'point rate $r$' not in tex
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);flat=' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',text).split())
    for claim in ['0.23002','0.90473','hypothetical point-rate cutoffs','not observed rates or confidence limits','other 159 entries fixed','16.08933','4.966','5.306']:assert claim in flat,claim
    assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
    assert qa['total_pages']==23 and qa['main_pages_including_news_and_references']==21 and qa['news_pages']==[16,17] and qa['ai_report_pages']==[22,23]
    assert qa['pdf_sha256']==sha(pdf) and qa['pdf_bytes']==pdf.stat().st_size and qa['compilation_warnings']==0
    assert not qa['submission_ready'] and not qa['ai_record_complete'] and qa['control_number']=='PENDING - not verified'
    assert sha(OUT/'compiler_stdout_stderr.txt')==qa['compiler_output_sha256']
    main=(OUT/'shared_main_compiler_stdout_stderr.txt').read_text();assert 'framework.png' in main and 'error:' in main
    before_pdf=old('drafts/task4_v137_paper.pdf');assert hashlib.sha256(before_pdf).hexdigest()=='3caf1fa59d423c99bd78082899149de8adc686d9d635ae48751e3e1adcd94580'
    with tempfile.TemporaryDirectory(prefix='himcm_v145_compare_',dir='/data/scratch') as t:
        p=Path(t);(p/'before.pdf').write_bytes(before_pdf)
        for name,path in [('before',p/'before.pdf'),('after',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(path),str(p/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        before=sorted(p.glob('before-*.png'));after=sorted(p.glob('after-*.png'));assert len(before)==len(after)==23
        changed=[i for i,(a,b) in enumerate(zip(before,after),1) if ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()]
    assert changed==[11,12,13],changed
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    for name in ['manifest.json','qa.json']:(OUT/('paper_'+name)).write_bytes((PAPER/assets/name).read_bytes())
    result=dict(status='pass',documentation_revision='V145',primary_evidence='V136',controlled_extensions='V137',primary_data_admissions=0,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),all_seven_owned_sections_unchanged=True,protected_historical_manuscript_files=len(manifest['protected_files']),selected_threshold_copies_verified=2,independent_city_cases=224,independent_score_bounds=448,all_23_final_pages_rendered_and_visually_reviewed=True,previous_overleaf_commit=BASE,changed_PDF_pages_vs_git=changed,pixel_identical_PDF_pages=20,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),paper_qa_sha256=sha(OUT/'paper_qa.json'),shared_main_build='failed at pre-existing missing framework.png; sources unchanged',submission_ready=False)
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
