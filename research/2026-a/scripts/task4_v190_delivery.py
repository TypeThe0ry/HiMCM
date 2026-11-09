"""Bind the current owned paper's delivery map to scoped, whole-word PDF anchors."""
import csv,hashlib,json,re,subprocess,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v190_delivery'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','')
    s=s.replace('–','-').replace('−','-').replace('—','-')
    s=re.sub(r'-[ \t]*\n[ \t]*','-',s)
    return ' '.join(s.split()).casefold()
def matches(marker,page,mode='phrase'):
    m=norm(marker)
    if mode=='line':return any(norm(line)==m for line in page.splitlines())
    return re.search(r'(?<!\w)'+re.escape(m)+r'(?!\w)',norm(page)) is not None

def main():
    O.mkdir(exist_ok=True)
    registry=R/'design/task4_user_current_review.json';review=json.loads(registry.read_text());assert review['version']=='V189' and review['primary_model']=='V181'
    pdf=P/review['pdf'];assert sha(pdf)==review['pdf_sha256']
    pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f');assert not pages[-1].strip();pages=pages[:-1];assert len(pages)==27
    prior=R/'results/task4_v189_review/requirements.csv';rows=list(csv.DictReader(prior.open()));assert len(rows)==47
    hits=[];changes=[];missing=[]
    for row in rows:
        old=dict(row);key=row['id'];mode='phrase';lo,hi=3,17
        if key=='PA-summary':lo=hi=1
        if key=='PA-toc':lo=hi=2;mode='line'
        if key=='PA-news':lo,hi=18,19
        if key=='PA-references':lo=hi=20;mode='line'
        if key in ['PA-ai-section','AI-tool-disclosure']:lo,hi=26,27
        if key=='U-MC-precision':lo=hi=15
        if key=='U-vintage':row['passage_markers']=json.dumps(['nominal reference year is 2025','64 post-2025 points'])
        if key=='U-perturbation':row['passage_markers']=json.dumps(['Dirichlet','conditional stress frequencies','critical radii'])
        if key=='AI-tool-disclosure':row['passage_markers']=json.dumps(['gpt-6.1-sol','Exa'])
        if key=='CI-budget':row['scope_or_remaining_action']='Zero main-page margin under the retained25-page limit; final integration can change pagination; not submission certification'
        if key=='U-source-quality':row['evidence']='V184provenance/withdrawals,V185one-meanthresholdandV187jointboxintegratedinV189;retainedpopulation/Jensen/otherinputscope;noCIorforecastclaim'
        if key=='U-perturbation':row['evidence']='Dirichletpreferenceandboundedfuture-shockexperiments;V187twelve-meanboxboundaryinV189;historicalutility-onlyfractional-massbudgets5%/20%'
        markers=json.loads(row['passage_markers']);found=set()
        for marker in markers:
            where=[n for n in range(lo,hi+1) if matches(marker,pages[n-1],mode)]
            if not where:missing.append((key,marker))
            found.update(where);hits.append(dict(id=key,marker=marker,match_mode=mode,allowed_page_start=lo,allowed_page_end=hi,hit_pages=','.join(map(str,where))))
        if markers:
            row['pdf_pages']=','.join(map(str,sorted(found)))
            row['page_basis']=f'Scoped {mode} anchors; pages{lo}-{hi}; whole-word boundaries'
        else:
            row['page_basis']='Artifact/source evidence; no PDF passage asserted'
            if row['pdf_pages']:
                assert key=='U-template-format' and row['pdf_pages']=='1-27'
                row['page_basis']='All27pages; geometry verified by frozenV189verification, not text anchors'
        if key=='PA-references':
            row['pdf_pages']='20,21,22,23,24,25';row['page_basis']='References heading p20; span ends before AI heading p26'
        if key=='PA-ai-section':row['page_basis']='AI section heading and incomplete-record statement onp26; appendix extends throughp27'
        if row!=old:changes.append(dict(id=key,changed_fields={k:dict(before=old.get(k),after=v) for k,v in row.items() if old.get(k)!=v}))
    assert not missing,missing
    assert not matches('Exa','example') and not matches('Exa','examination') and matches('Exa','Exa search')
    assert next(x for x in rows if x['id']=='U-fairness-error')['pdf_pages']=='16'
    assert next(x for x in rows if x['id']=='PA-toc')['pdf_pages']=='2'
    assert next(x for x in rows if x['id']=='AI-tool-disclosure')['pdf_pages']=='26,27'
    for name,values in [('requirements.csv',rows),('anchor_hits.csv',hits)]:
        with (O/name).open('w') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(values[0]),lineterminator='\n');writer.writeheader();writer.writerows(values)
    summary=dict(version='V190 delivery map',paper_version='V189 unchanged',primary='V181 unchanged',pdf_sha256=sha(pdf),total_pages=27,main_and_reference_pages=25,main_page_margin=0,requirements=47,statuses_unchanged=True,pending_count=13,anchor_count=len(hits),all_scoped_anchors_found=True,changes=changes,source_sha256={str(p.relative_to(R)):sha(p) for p in [prior,registry,Path(__file__),R/'results/task4_v189_review/verification.json']},paper_sha256={str(pdf.relative_to(P)):sha(pdf)},scope='Page anchors locate passages; they do not validate all measurements, certify content sufficiency, close team/registration/AI gaps, or establish server compile or final submission readiness.',submission_ready=False)
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(dict(requirements=47,anchors=len(hits),all_found=True,main_page_margin=0,changed_rows=len(changes)),indent=2))
if __name__=='__main__':main()
