"""Verify a source-documentation edit without regenerating scientific results."""
from pathlib import Path
import gzip,hashlib,json,subprocess,tempfile
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1]
PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
OUT=ROOT/'results/task4_v139_documentation'
BASE='d8ba697'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=PAPER)
def main():
    snapshot=read(ROOT/'design/task4_user_v136_snapshot.json')
    extension=read(ROOT/'results/task4_v137_revision/audit.json')
    priority=read(ROOT/'results/task4_v138_priority/summary.json')
    frozen={**snapshot['source_sha256'],**extension['result_sha256'],**priority['source_sha256']}
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    assets='drafts/task4_v137_assets/'
    tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--',assets],cwd=PAPER,text=True).splitlines()
    retained=[name for name in tracked if Path(name).name not in {'manifest.json','qa.json','README.md'}]
    retained+=['drafts/task4_v137_generated.tex']
    retained += [f'drafts/task4_v137_{k}.tex' for k in ['paper','front','conclusion','news','ai']]
    for name in retained:assert (PAPER/name).read_bytes()==old(name),name
    manifest=read(PAPER/assets/'manifest.json')
    assert manifest['documentation_revision']=='V139'
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['protected_files'].items():assert sha(PAPER/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    source=ROOT/'data/task4_v138_warsaw';receipt=read(source/'verification.json')
    for name,digest in receipt['source_sha256'].items():assert sha(source/name)==digest,name
    original=gzip.decompress((source/'report_original.pdf.gz').read_bytes())
    assert hashlib.sha256(original).hexdigest()==receipt['raw_original_sha256']
    assert read(source/'observations.json')==[]
    qa=read(PAPER/assets/'qa.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert qa['documentation_revision']=='V139' and qa['technical_checks']=='pass'
    assert qa['all_pages_rendered_and_visually_reviewed'] and qa['total_pages']==22
    assert qa['pdf_sha256']==sha(pdf) and not qa['submission_ready']
    assert sha(OUT/'compiler_stdout_stderr.txt')==qa['compiler_output_sha256']
    text=' '.join(subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split())
    for claim in ['27 minutes','sample base of 22','2022','upper-secondary','denominator','112 point values, 33 partial intervals and 15 fully missing intervals']:assert claim in text,claim
    old_pdf=old('drafts/task4_v137_paper.pdf')
    assert hashlib.sha256(old_pdf).hexdigest()=='fd0d8de50b6dc15e7878a62f1263dbee724874a6e04151e3a43a845a91cfcecb'
    with tempfile.TemporaryDirectory(prefix='himcm_v139_compare_',dir='/data/scratch') as tmp:
        p=Path(tmp);(p/'original.pdf').write_bytes(old_pdf)
        for name,path in [('before',p/'original.pdf'),('after',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(path),str(p/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        before=sorted(p.glob('before-*.png'));after=sorted(p.glob('after-*.png'));assert len(before)==len(after)==22
        changed=[i for i,(a,b) in enumerate(zip(before,after),1) if ImageChops.difference(Image.open(a).convert('RGB'),Image.open(b).convert('RGB')).getbbox()]
    assert changed==[7,8,20],changed
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    for name in ['qa.json','manifest.json']:(OUT/('paper_'+name)).write_bytes((PAPER/assets/name).read_bytes())
    result=dict(status='pass',documentation_revision='V139',science='V136 primary / V137 extensions',primary_admissions=0,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),protected_historical_manuscript_files=len(manifest['protected_files']),all_22_final_pages_rendered_and_visually_reviewed=True,changed_PDF_pages_vs_git=changed,pixel_identical_PDF_pages=19,previous_overleaf_commit=BASE,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),paper_qa_sha256=sha(OUT/'paper_qa.json'),submission_ready=False)
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
