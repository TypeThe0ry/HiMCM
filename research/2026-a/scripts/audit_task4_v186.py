"""Audit the single-paragraph V186 sensitivity insertion and preserved V181 science."""
from pathlib import Path
from collections import Counter
import argparse,csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as E
import numpy as np
from scipy.optimize import brentq
from task4_user_v181_revision import revised_bounds
from task4_v5_model import NAMES
from audit_task4_v184 import norm,pdftext,graph,diagnostic_checks
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v186_review';T=Path('/data/scratch')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write_table(name,records):
    with (O/name).open('w') as stream:
        w=csv.DictWriter(stream,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
def scores(u,w):
    return np.array([100*(a:=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row))))/(a+math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))) for row in u])
def protection(active):
    saved=read(O/'protected_files.json');changed=[]
    for name,h in saved['science'].items():assert sha(R/name)==h,name
    for name,h in saved['paper'].items():
        if active and name=='drafts/task4_current_review.json':changed.append(name);continue
        if active and name=='AGENTS.md':
            value=(P/name).read_text();new='V184 is the frozen preceding review.';old='V182 is the frozen preceding review.'
            assert value.count(new)==1 and hashlib.sha256(value.replace(new,old).encode()).hexdigest()==h
            changed.append(name);continue
        assert sha(P/name)==h,name
    for name,h in saved['registries'].items():
        if active and name=='task4_user_current_review.json':continue
        assert sha(R/'design'/name)==h,name
    f,l,h=revised_bounds()
    assert f.city.tolist()==saved['cities'];np.testing.assert_array_equal(l,saved['lower']);np.testing.assert_array_equal(h,saved['upper'])
    return saved,changed
def threshold_checks():
    prior=R/'results/task4_v185_commute_candidate';cert=read(prior/'verification.json');assert cert['status']=='pass'
    for section in ['source_sha256','audited_output_sha256']:
        for name,h in cert[section].items():assert sha(R/name)==h,name
    f,l,h=revised_bounds();city=f.city.tolist();z=city.index('Zurich');j=NAMES.index('travel');records=[]
    rows=read(prior/'mean_thresholds.json')
    for ref,w in [('fixed',np.array([.1125]*6+[.05,.1125,.1125,.05])),('equal',np.full(10,.1))]:
        upper=scores(h,w)
        other_reference=None
        def values(u):
            a=l.copy();a[z,j]=u;lower=scores(a,w)
            regret=np.array([max(0.,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)])
            selected=[city[i] for i in range(16) if regret[i]<=regret.min()+1e-12]
            return regret,selected
        def gap(u):
            v,_=values(u);return float(v[z]-np.delete(v,z).min())
        r0,_=values(0);r1,_=values(1);np.testing.assert_array_equal(np.delete(r0,z),np.delete(r1,z))
        supplied=next(v for v in rows if v['weight_reference']==ref)
        np.testing.assert_allclose([gap(0),gap(1)],[supplied['gap_at_lower_utility0'],supplied['gap_at_lower_utility1']],rtol=0,atol=3e-13)
        if ref=='fixed':
            root=float(brentq(gap,0,1,xtol=1e-14));mean=-30*math.log(root)
            np.testing.assert_allclose(mean,supplied['tie_mean_minutes'],rtol=0,atol=1e-10)
            assert f'{mean:.2f}'=='46.59'
            for shift,choice in [(-1e-4,['Zurich']),(1e-4,['Singapore'])]:
                assert values(math.exp(-(mean+shift)/30))[1]==choice
            assert set(values(root)[1])=={'Zurich','Singapore'}
            records.append(dict(weight_reference=ref,tie_mean_minutes=mean,tie_lower_utility=root,below='Zurich',above='Singapore',both_sides_verified=True))
        else:
            assert gap(0)<0 and gap(1)<0
            for u in np.linspace(0,1,101):assert values(float(u))[1]==['Zurich']
            # Score increases with u, upper scores/other regrets are constant;
            # maximum focal gap is at u=0 and is strictly below zero.
            records.append(dict(weight_reference=ref,no_finite_mean_crossing=True,maximum_gap=gap(0),monotone_score_and_constant_competitor_regrets=True))
    withdrawn=diagnostic_checks();assert len(withdrawn)==10 and all(x['possible_champions']==16 for x in withdrawn)
    return records
def source_scope():
    old=(D/'task4_v184_vintage.tex').read_text();new=(D/'task4_v186_vintage.tex').read_text();cut=old.index('Separately withdraw commute proxies')
    assert new.startswith(old[:cut])
    prefix=old[:cut];addition=new[len(prefix):];text=norm(addition)
    assert '46.59 minutes' in text and 'Separately vary only Zurich' in text and 'Jensen bounds' in text
    assert 'all withdrawals retain sixteen possible champions' in text
    assert 'for all nonnegative means' in text and 'with other data fixed' in text
    assert not any(s in text.lower() for s in ['confidence level','forecast','95%','all changes retain sixteen'])
    assert (D/'task4_v186_core.tex').read_text()==(D/'task4_v184_core.tex').read_text().replace('task4_v184_vintage.tex','task4_v186_vintage.tex')
    assert (D/'task4_v186_paper.tex').read_text()==(D/'task4_v184_paper.tex').read_text().replace('% V184 owned review;','% V186 owned review;').replace('task4_v184_core.tex','task4_v186_core.tex')
    m=read(D/'task4_v186_manifest.json')
    for name,h in m['source_sha256'].items():assert sha(R/name)==h,name
    for name,h in m['paper_input_sha256'].items():assert sha(P/name)==h,name
    assert m['rounded_threshold_minutes']=='46.59' and not m['baseline_data_changed'] and not m['figures_references_AI_changed']
    return dict(edit_scope='Only final5.5paragraph and two inputpaths/versioncomment',original_vintage_prefix_byte_preserved=True,threshold_scope='OneZurichmean, Jensenlower,allotherdataandweightsfixed',sixteen_possible_scope='Withdrawalchecks only;notwholemeanparameterdomain')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expect-active',action='store_true');parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    O.mkdir(exist_ok=True);protected,changed=protection(args.expect_active);math_checks=threshold_checks();scope=source_scope()
    if args.source_only:print(json.dumps(dict(status='pass',math=math_checks,scope=scope),indent=2));return
    pdf=D/'task4_v186_paper.pdf';proxy=T/'himcm_v186_proxy/task4_v186_review_entry.pdf';tex=D/'task4_v186_paper.tex'
    pages=[norm(x) for x in pdftext(pdf).split('\f') if x.strip()]
    assert pages==[norm(x) for x in pdftext(proxy).split('\f') if x.strip()]
    aux=(T/'himcm_v186_build/task4_v186_paper.aux').read_text()
    def label(name):return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
    end=label('main-end');assert end<=25 and len(pages)==end+2 and label('LastPage')==len(pages)
    references=set(re.findall(r'\\bibcite\{([^}]+)\}',aux));oldrefs=set(re.findall(r'\\bibcite\{([^}]+)\}',(R/'results/task4_v184_source_review/direct_labels.aux').read_text()))
    assert references==oldrefs and len(references)==53
    files=graph(tex);combined='\n'.join(p.read_text() for p in sorted(files))
    assert 'tcn=PENDING' in tex.read_text() and 'task4_v182_generated.tex' in combined
    for marker in ['46.59','Jensen bounds','other data fixed','nonnegative means','incomplete review record','14:31:18.850 UTC','326 selected','1,865']:
        assert norm(marker) in norm(combined),marker
    bbox=T/'himcm_v186_bbox.html';subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    nodes=E.parse(bbox).getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(nodes)==len(pages)
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{http://www.w3.org/1999/xhtml}word');assert not any(float(w.get('yMin'))>745 for w in words)
        if i:
            top=[w for w in words if float(w.get('yMin'))<65]
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert f'Page {i+1} of {len(pages)}' in pages[i]
    logs=[(T/'himcm_v186_build/task4_v186_paper.log').read_text(),(T/'himcm_v186_proxy/task4_v186_review_entry.log').read_text()]
    for log in logs:assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
    assert [log.count('Underfull') for log in logs]==[2,2]
    fontxml=T/'himcm_v186_fonts.xml';subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(fontxml)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    fonts={};counts=Counter();small=[];threshold_font=[]
    for page in E.parse(fontxml).getroot().findall('page'):
        for font in page.findall('fontspec'):fonts[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if not value:continue
            font=fonts[span.get('font')];size=int(font['size']);family=re.sub(r'^[A-Z]{6}\+','',font['family']);counts[size,family]+=1
            if '46.59' in value:threshold_font.append(size)
            if size<9:small.append(dict(pdf_page=int(page.get('number')),top=int(span.get('top')),extractor_size=size,font_family=family,text=value))
    assert threshold_font and min(threshold_font)>=11
    write_table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Nominal12ptbody/11ptnativeheads retained;legacy math subscripts separately listed') for k,v in sorted(counts.items())])
    if small:write_table('small_spans.csv',small)
    requirements=list(csv.DictReader((R/'results/task4_v184_source_review/requirements.csv').open()));statuses={x['id']:x['status'] for x in requirements}
    for item in requirements:
        hits=[]
        for marker in json.loads(item['passage_markers']):
            found=[i for i,page in enumerate(pages,1) if norm(marker).lower() in page.lower()]
            assert found,(item['id'],marker);hits+=found
        if hits:item['pdf_pages']=','.join(map(str,sorted(set(hits))))
        updates={'CI-file':f'{pdf.stat().st_size} bytes;oneV186ownedPDF','TEAM-independent-entry':f'V186direct/root per-page textequal;{len(pages)}pages;0overfull/2underfull','CI-budget':f'{end}main/reference+2provisionalAI;{25-end}page margin','PA-references':'53compiledreferences;exactsame53keysasV184','U-source-quality':'V184provenance/withdrawal findingretained;V185one-mean46.59threshold insertedwithJensen/allotherdatafixed scope;noCIorforecastclaim','AI-verification':'V181scienceandV185thresholdproof retained;V186limitedparagraph/paperaudit;frozencaptureunchanged'}
        if item['id'] in updates:item['evidence']=updates[item['id']]
    assert len(requirements)==47 and all(x['status']==statuses[x['id']] for x in requirements)
    pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
    write_table('requirements.csv',requirements)
    visual=read(O/'visual_review.json');assert visual['pdf_sha256']==sha(pdf)
    overview=visual.get('contact_overview_all_pages',visual.get('contact_sheets_reviewed_all_pages'));assert overview==list(range(1,len(pages)+1))
    if args.expect_active:
        review=read(R/'design/task4_user_current_review.json');assert review==read(D/'task4_current_review.json')
        assert review['version']=='V186' and review['primary_model']=='V181' and review['pdf_sha256']==sha(pdf)
    result=dict(version='V186',status='pass',primary_model='V181',activation_status='active' if args.expect_active else 'verified_pending_activation',total_pages=len(pages),main_and_references_pages=end,main_page_margin=25-end,news_pages=[label('news-start'),label('news-end')],AI_pages=[end+1,end+2],compiled_references=53,prior53_reference_keys_exact=True,scientific_files_unchanged=len(protected['science']),existing_manuscript_files_unchanged=len(protected['paper'])-len(changed),owned_pointer_files_changed=changed,original_user_CSV_and_all160bounds_unchanged=True,current_model_extensions_unchanged=True,shared_main_ref_class_unchanged=True,figures_numerical_assets_references_AI_byte_unchanged=True,primary_admissions=0,actual_baseline_width_change=0,threshold_checks=math_checks,edit_scope_checks=scope,direct_root_text_equal=True,native_header_footer_checked=True,new_threshold_font_extractor_size_min=min(threshold_font),overfull_boxes=0,underfull_paragraphs_per_build=2,requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,AI_history_complete=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),threshold_certificate_sha256=sha(R/'results/task4_v185_commute_candidate/verification.json'),verifier_sha256=sha(Path(__file__)),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(files)},visual_review_scope=visual.get('scope'))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='tex_source_sha256'},indent=2))
if __name__=='__main__':main()
