"""Independent bbox-word audit of scoped V190 delivery anchors on frozen V189."""
import csv,hashlib,json,re,subprocess,unicodedata,xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v190_delivery'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):return list(csv.DictReader(p.open()))
def canonical(s):
    value=unicodedata.normalize('NFKC',s).replace('\u00ad','')
    value=value.translate(str.maketrans({'–':'-','—':'-','−':'-'}))
    # bbox words preserve physical word gaps; a line-broken hyphenated token
    # is represented by two word nodes and must be rejoined for this comparison.
    value=re.sub(r'(?<=-)\s+(?=\w)','',value)
    return re.sub(r'\s+',' ',value).strip().lower()
def phrase(needle,text):
    return re.search(r'(?<!\w)'+re.escape(canonical(needle))+r'(?!\w)',canonical(text)) is not None

def main():
    protected=read(O/'protected_files.json')
    for name,h in protected['paper'].items():assert sha(P/name)==h,name
    for name,h in protected['science'].items():assert sha(R/name)==h,name
    for name,h in protected['registries'].items():assert sha(R/'design'/name)==h,name
    model=read(R/'design/task4_user_current_model.json');assert model['version']=='V181' and model['module']=='task4_user_v181_revision'
    review=read(R/'design/task4_user_current_review.json');assert review['version']=='V189' and review['primary_model']=='V181'
    assert review==read(P/'drafts/task4_current_review.json')
    delivery=read(R/'design/task4_user_current_delivery.json')
    assert delivery==read(P/'drafts/task4_current_delivery.json')
    assert delivery['version']=='V190' and delivery['review_version']=='V189' and delivery['primary_model']=='V181'
    assert delivery['pdf']==review['pdf'] and delivery['pdf_sha256']==review['pdf_sha256']
    assert delivery['requirements']==47 and delivery['pending_count']==13 and delivery['main_page_margin']==0
    assert not delivery['submission_ready'] and not delivery['server_compile_verified']
    pdf=P/review['pdf'];assert sha(pdf)==review['pdf_sha256']
    xml=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-']))
    nodes=xml.findall('.//{*}page');assert len(nodes)==27
    assert all((float(p.get('width')),float(p.get('height')))==(612,792) for p in nodes)
    pages=[' '.join(w.text or '' for w in page.findall('.//{*}word')) for page in nodes]
    raw=subprocess.check_output(['pdftotext','-raw',str(pdf),'-'],text=True).split('\f')
    assert len(raw)==28 and not raw[-1].strip();raw=raw[:-1]
    requirements=table(O/'requirements.csv');prior=table(R/'results/task4_v189_review/requirements.csv');anchors=table(O/'anchor_hits.csv')
    assert len(requirements)==len(prior)==47 and len(anchors)==58
    assert [x['id'] for x in requirements]==[x['id'] for x in prior]
    assert {x['id']:x['status'] for x in requirements}=={x['id']:x['status'] for x in prior}
    pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}]
    assert len(pending)==13
    old={x['id']:x for x in prior};new={x['id']:x for x in requirements}
    page_changes=[x['id'] for x in requirements if x['pdf_pages']!=old[x['id']]['pdf_pages']];assert len(page_changes)==12
    grouped=defaultdict(list);recomputed=[]
    for item in anchors:
        key=item['id'];assert key in new
        first,last=int(item['allowed_page_start']),int(item['allowed_page_end']);assert 1<=first<=last<=27
        mode=item['match_mode'];assert mode in {'phrase','line'}
        if mode=='line':
            hits=[n for n in range(first,last+1) if any(canonical(line)==canonical(item['marker']) for line in raw[n-1].splitlines())]
        else:hits=[n for n in range(first,last+1) if phrase(item['marker'],pages[n-1])]
        assert hits and item['hit_pages']==','.join(map(str,hits)),(key,item['marker'],hits,item['hit_pages'])
        grouped[key].append((item['marker'],hits));recomputed.append(dict(id=key,marker=item['marker'],pages=hits,independent_extractor='Poppler bbox word nodes; raw lines for headings'))
    for item in requirements:
        key=item['id'];markers=json.loads(item['passage_markers'])
        assert [m for m,_ in grouped[key]]==markers,key
        expected=sorted({n for _,hits in grouped[key] for n in hits})
        if key=='PA-references':
            assert expected==[20] and phrase('Report on Use of AI Tools',pages[25]);expected=list(range(20,26))
        elif key=='U-template-format':
            assert not markers and item['pdf_pages']=='1-27';continue
        assert item['pdf_pages']==','.join(map(str,expected)),key
        if markers:assert 'page_basis' in item and item['page_basis']
    assert new['PA-toc']['pdf_pages']=='2'
    assert new['AI-tool-disclosure']['pdf_pages']=='26,27'
    assert new['U-fairness-error']['pdf_pages']=='16'
    assert new['U-MC-precision']['pdf_pages']=='15'
    assert '64 are dated 2026' not in json.loads(new['U-vintage']['passage_markers'])
    assert not any(phrase('64 are dated 2026',page) for page in pages)
    assert 'Zero main-page margin' in new['CI-budget']['scope_or_remaining_action']
    assert 'One main page remains' not in json.dumps(requirements)
    for value in ['example','examination','extra','exabyte','Exa2','myExa']:
        assert not phrase('Exa',value),value
    assert phrase('Exa','Exa, used by the team') and phrase('Exa','EXA search')
    assert phrase('fixed','ﬁxed') and phrase('unknown','un\u00adknown')
    assert phrase('64 post-2025 points','64 post-\n2025 points')
    summary=read(O/'summary.json');verification=read(R/'results/task4_v189_review/verification.json')
    assert verification['status']=='pass' and verification['pdf_sha256']==sha(pdf)
    assert summary['pdf_sha256']==sha(pdf) and summary['paper_version']=='V189 unchanged'
    assert summary['requirements']==47 and summary['anchor_count']==58 and summary['all_scoped_anchors_found']
    assert summary['total_pages']==27 and summary['main_and_reference_pages']==verification['main_and_references_pages']==25
    assert summary['main_page_margin']==25-verification['main_and_references_pages']==0
    assert summary['statuses_unchanged'] and summary['pending_count']==13 and not summary['submission_ready']
    assert 'do not validate all measurements' in summary['scope']
    for name,h in summary['source_sha256'].items():assert sha(R/name)==h,name
    for name,h in summary['paper_sha256'].items():assert sha(P/name)==h,name
    for change in summary['changes']:
        key=change['id'];expected={k:dict(before=old[key].get(k),after=v) for k,v in new[key].items() if old[key].get(k)!=v}
        assert change['changed_fields']==expected,key
    assert len(summary['changes'])==47
    sources=[Path(__file__),O/'protected_files.json',R/'design/task4_user_current_delivery.json',R/'design/task4_user_current_review.json',R/'results/task4_v189_review/verification.json']
    outputs=[O/name for name in ['requirements.csv','anchor_hits.csv','summary.json','content_review.md']]
    result=dict(version='V190 independent delivery audit',status='pass',review_version='V189 unchanged',primary_model='V181 unchanged',pdf_sha256=sha(pdf),total_pages=27,main_and_reference_pages=25,main_page_margin=0,requirements=47,scoped_anchor_rows=58,independent_bbox_anchor_hits_match=True,raw_heading_lines_checked=True,page_mapping_rows_corrected=12,all47_statuses_preserved=True,pending_count=13,pending_gates=pending,whole_word_negative_cases_checked=['example','examination','extra','exabyte','Exa2','myExa'],unicode_and_hyphen_wrap_checks=True,paper_files_unchanged=len(protected['paper']),science_files_unchanged=len(protected['science']),existing_research_registries_unchanged=len(protected['registries']),delivery_registries_equal=True,submission_ready=False,server_compile_verified=False,scope='Locates the specified passages and verifies frozen inputs/status preservation. Does not certify every original measurement, all paper reasoning, source validity, full-team AI records, registration or final contest readiness.',source_sha256={str(p.relative_to(R)):sha(p) for p in sources},audited_output_sha256={str(p.relative_to(R)):sha(p) for p in outputs})
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','scoped_anchor_rows','page_mapping_rows_corrected','paper_files_unchanged','science_files_unchanged','pending_count']},indent=2))
if __name__=='__main__':main()
