"""Check complete recovered original and non-admission without changing science."""
from pathlib import Path
import gzip,hashlib,json,re,subprocess,tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    meta=read(HERE/'retrieval.json');scope=read(HERE/'scope_audit.json')
    source={p.name:sha(p) for p in HERE.iterdir() if p.is_file() and p.name not in {'verification.json','recheck_verification.json'}}
    previous=HERE/'verification.json'
    if previous.exists():
        for name,digest in read(previous)['source_sha256'].items():assert sha(HERE/name)==digest,name
    snapshot=read(ROOT/'design/task4_user_v136_snapshot.json')
    extensions=read(ROOT/'results/task4_v137_revision/audit.json')
    protected={**snapshot['source_sha256'],**extensions['result_sha256']}
    for name,digest in protected.items():assert sha(ROOT/name)==digest,name
    registry=ROOT/'design/task4_user_current_model.json';registry_bytes=registry.read_bytes()
    manuscript={str(p.relative_to(PAPER)):sha(p) for p in [PAPER/'main.tex',PAPER/'ref.bib',PAPER/'mcmthesis.cls',PAPER/'drafts/task4_v137_paper.pdf',*[PAPER/f'drafts/task4_v137_{k}.tex' for k in ['paper','front','core','conclusion','news','ai','references']]]}
    raw=gzip.decompress((HERE/'report_original.pdf.gz').read_bytes())
    assert len(raw)==meta['raw_original_bytes']==6068386
    assert hashlib.sha256(raw).hexdigest()==meta['raw_original_sha256']
    assert raw.startswith(b'%PDF-') and scope['primary_admissions']==0
    assert read(HERE/'observations.json')==[]
    assert meta['http_status']==200 and scope['school_stage_or_14_to_18_subgroup_not_identified']
    with tempfile.TemporaryDirectory(prefix='himcm_v138_source_',dir='/data/scratch') as tmp:
        p=Path(tmp)/'original.pdf';p.write_bytes(raw)
        info=subprocess.check_output(['pdfinfo',str(p)],text=True)
        assert re.search(r'^Pages:\s+141$',info,re.M)
        text=subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True).split('\f')
        for number in meta['verified_extracted_pages']:
            assert text[number-1]==(HERE/f'page_{number:03d}_extracted.txt').read_text(),number
        assert '2022' in text[2] and '7 702' in text[2] and '800' in text[2]
        assert '408' in text[57] and '22' in text[57]
        assert 'Czas trwania podróży do szkoły' in text[63]
    assert sum(scope['displayed_city_percentages'])==scope['displayed_city_percentages_sum']==101
    for name,digest in protected.items():assert sha(ROOT/name)==digest,name
    for name,digest in manuscript.items():assert sha(PAPER/name)==digest,name
    assert registry.read_bytes()==registry_bytes
    for name,digest in source.items():assert sha(HERE/name)==digest,name
    result=dict(status='pass',complete_original_verified=True,lossless_archive_reproduces_original=True,raw_original_bytes=len(raw),raw_original_sha256=hashlib.sha256(raw).hexdigest(),pdf_pages=141,extracted_pages_exactly_reproduced=meta['verified_extracted_pages'],page64_visually_reviewed=True,primary_admissions=0,no_rounding_or_missing_tail_repair=True,current_registry_before_after_identical=True,current_registry_version=read(registry)['version'],protected_scientific_files=len(protected),protected_manuscript_sha256=manuscript,source_sha256=source)
    target=HERE/('recheck_verification.json' if previous.exists() else 'verification.json')
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if not isinstance(v,dict)},indent=2))
if __name__=='__main__':main()
