"""Independently audit V184 source scope, conditional withdrawals and owned review."""
from pathlib import Path
from collections import Counter
import argparse,csv,hashlib,json,math,re,subprocess,unicodedata,xml.etree.ElementTree as E
import numpy as np
import pandas as pd
from task4_user_v181_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v184_source_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',s)).split())
def pdftext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def write_table(name,rows):
    with (O/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def decode(data,selectors):
    offset=0;labels={}
    for key,size in zip(data['id'],data['size']):
        cat=data['dimension'][key]['category'];index=cat['index'];index={v:i for i,v in enumerate(index)} if isinstance(index,list) else index
        code=selectors.get(key)
        if code is None:assert size==1;code=next(iter(index))
        assert code in index,(key,code);offset=offset*size+index[code];labels[key]=cat.get('label',{}).get(code,code)
    value=data['value'];value=value[str(offset)] if isinstance(value,dict) else value[offset]
    status=data.get('status',{});flag=status.get(str(offset)) if isinstance(status,dict) else status[offset]
    return value,flag,labels,offset

def source_checks():
    bindings={};responses=0
    for folder in ['dublin_commute','zurich_commute','helsinki_teacher']:
        base=R/('data/task4_v184_'+folder)
        for receipt in read(base/'retrievals.json'):
            assert receipt['http_status']==200
            path=base/receipt['file'];assert len(path.read_bytes())==receipt['bytes'] and sha(path)==receipt['sha256'],path
            bindings[str(path.relative_to(R))]=sha(path);responses+=1
        for name in ['retrievals.json','findings.json']:
            path=base/name;bindings[str(path.relative_to(R))]=sha(path)
    assert responses==8
    dub=R/'data/task4_v184_dublin_commute';zur=R/'data/task4_v184_zurich_commute'
    dv,ds,dl,di=decode(read(dub/'eurostat_dublin2011_original.json'),dict(freq='A',indic_ur='TT1019V',cities='IE001C',time='2011'))
    zv,zs,zl,zi=decode(read(zur/'zurich_CH002C2024_urb_ctran_original.json'),dict(freq='A',indic_ur='TT1019V',cities='CH002C',time='2024'))
    bv,bs,bl,_=decode(read(zur/'initial_CH001C2024_urb_ctran_original.json'),dict(freq='A',indic_ur='TT1019V',cities='CH001C',time='2024'))
    av,ass,al,_=decode(read(zur/'all_cities2024_worktime_original.json'),dict(freq='A',indic_ur='TT1019V',cities='CH002C',time='2024'))
    transit,transitstatus,_,_=decode(read(zur/'zurich_CH002C2024_urb_ctran_original.json'),dict(freq='A',indic_ur='TT1010V',cities='CH002C',time='2024'))
    assert dv==28.8 and ds is None and di==6 and dl['cities']=='Dublin (greater city)'
    assert zv==39.9 and zs=='e' and zi==6 and zl['cities']=='Zurich (greater city)'
    assert av==zv and ass==zs and al['cities']==zl['cities']
    assert bv==37.69 and bs=='e' and bl['cities']=='Bern (greater city)'
    assert transit==60.41 and transitstatus=='e'
    assert dl['indic_ur']==zl['indic_ur']=='Average time of journey to work - minutes'
    original=read(zur/'zurich_CH002C2024_urb_ctran_original.json');assert original['extension']['status']['label']['e']=='estimated'
    findings=read(zur/'findings.json');assert not findings['interpretation']['proven_original_CSV_lineage'] and not findings['interpretation']['compatible_duration_bins_obtained']
    h=read(R/'data/task4_v184_helsinki_teacher/findings.json');assert h['primary_admissions']==0
    assert h['city_annual']['combined_personnel_headcount']==684+103==787 and not h['city_annual']['teaching_FTE_located']
    f,l,u=revised_bounds()
    for name,x,year,flag in [('Dublin',28.8,2011,'STALE'),('Zurich',39.9,2024,'ok')]:
        row=f[f.city==name].iloc[0];assert row.commute_min==x and row.commute_min_year==year and row.commute_min_flag==flag
    return dict(successful_original_responses=responses,matching_Dublin_value=dv,matching_Zurich_value=zv,Dublin_status=None,Zurich_status='e (estimated)',both_current_labels_greater_city=True,CH001C_verified_Bern=True,user_source_lineage_proven=False,historical_boundary_verified=False,school_travel_distribution_obtained=False,source_sha256=bindings)

def scalar_scores(u,w):
    result=[]
    for row in u:
        a=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)));b=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
        result.append(100*a/(a+b))
    return np.array(result)
def graph(path,seen=None):
    seen=set() if seen is None else seen;path=path.resolve()
    if path in seen:return seen
    seen.add(path)
    for name in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
        q=D/name
        if q.suffix!='.tex':q=q.with_suffix('.tex')
        assert q.exists(),q;graph(q,seen)
    return seen

def protection(expect_active):
    protected=read(O/'protected_files.json');changed=[]
    for n,h in protected['science'].items():assert sha(R/n)==h,n
    for n,h in protected['paper'].items():
        if expect_active and n=='drafts/task4_current_review.json':changed.append(n);continue
        if expect_active and n=='AGENTS.md':
            current=(P/n).read_text();new='V182 is the frozen preceding review.';old='V179 is the frozen preceding review.'
            assert current.count(new)==1;assert hashlib.sha256(current.replace(new,old).encode()).hexdigest()==h;changed.append(n);continue
        assert sha(P/n)==h,n
    for n,h in protected['registries'].items():
        if expect_active and n=='task4_user_current_review.json':continue
        assert sha(R/'design'/n)==h,n
    return protected,changed

def diagnostic_checks():
    folder=O;ranks=pd.read_csv(folder/'commute_withdrawal_ranks.csv',float_precision='round_trip');saved_bounds=pd.read_csv(folder/'commute_withdrawal_bounds.csv',float_precision='round_trip');summary=read(folder/'summary.json')
    for n,h in summary['source_sha256'].items():assert sha(R/n)==h,n
    f,lo,hi=revised_bounds();cities=f.city.tolist();j=NAMES.index('travel');count=0;reports=[]
    assert lo.shape==hi.shape==(16,10)
    cases={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':f.loc[f.commute_min.notna(),'city'].tolist()}
    assert len(cases['withdraw_all_submitted_commute_means'])==12 and 'Singapore' not in cases['withdraw_all_submitted_commute_means']
    assert set(ranks.scenario)==set(cases) and len(ranks)==160
    for case,removed in cases.items():
        a,b=lo.copy(),hi.copy()
        for city in removed:a[cities.index(city),j],b[cities.index(city),j]=0,1
        if case=='withdraw_all_submitted_commute_means':
            sg=cities.index('Singapore');np.testing.assert_array_equal([a[sg,j],b[sg,j]],[lo[sg,j],hi[sg,j]])
        saved=saved_bounds[saved_bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        np.testing.assert_array_equal(saved.lower.to_numpy().reshape(16,10),a);np.testing.assert_array_equal(saved.upper.to_numpy().reshape(16,10),b)
        for ref,w in [('fixed',np.array([.1125]*6+[.05,.1125,.1125,.05])),('equal',np.full(10,.1))]:
            lower,upper=scalar_scores(a,w),scalar_scores(b,w)
            regret=np.array([max(0.,max(upper[k] for k in range(16) if k!=i)-lower[i]) for i in range(16)])
            rank=np.array([1+sum(regret[k]<regret[i]-1e-12 for k in range(16)) for i in range(16)])
            possible=[upper[i]>=max(lower[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
            necessary=[lower[i]>=max(upper[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
            saved=ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)].set_index('city').loc[cities]
            for col,x in [('score_lower',lower),('score_upper',upper),('max_regret',regret),('decision_rank',rank)]:np.testing.assert_allclose(saved[col],x,atol=1e-11,rtol=0)
            assert possible==saved.possible_champion.tolist() and necessary==saved.necessary_champion.tolist()
            assert all(possible) and not any(necessary)
            best=[1+sum(lower[k]>upper[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
            worst=[1+sum(upper[k]>lower[i]+1e-12 for k in range(16) if k!=i) for i in range(16)]
            assert best==saved.best_rank.tolist() and worst==saved.worst_rank.tolist()
            mid=scalar_scores((a+b)/2,w);np.testing.assert_allclose(saved.midpoint_illustrative_score,mid,atol=1e-11,rtol=0)
            midrank=[1+sum(mid[k]>mid[i]+1e-12 for k in range(16)) for i in range(16)];assert midrank==saved.midpoint_illustrative_rank.tolist()
            choices=[cities[i] for i in range(16) if rank[i]==1];expected=['Singapore'] if ref=='fixed' and 'Zurich' in removed else ['Zurich'];assert choices==expected
            reports.append(dict(scenario=case,weight_reference=ref,conservative_recommendation=choices,possible_champions=int(sum(possible)),necessary_champions=int(sum(necessary)),mean_score_interval_width=float(np.mean(upper-lower))))
            count+=16
    assert count==160
    return reports

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');parser.add_argument('--expect-active',action='store_true');parser.add_argument('--proxy-pdf',type=Path,default=T/'himcm_v184_proxy/task4_v184_review_entry.pdf');parser.add_argument('--direct-aux',type=Path,default=T/'himcm_v184_build/task4_v184_paper.aux');parser.add_argument('--direct-log',type=Path,default=T/'himcm_v184_build/task4_v184_paper.log');parser.add_argument('--proxy-log',type=Path,default=T/'himcm_v184_proxy/task4_v184_review_entry.log');args=parser.parse_args()
    O.mkdir(exist_ok=True);protected,changed=protection(args.expect_active);source=source_checks();reports=diagnostic_checks()
    if args.source_only:
        print(json.dumps(dict(status='pass',scope='sources and160scalarcases',sources=source,diagnostics=reports),indent=2));return
    paper_checks(args,protected,changed,source,reports)


def paper_checks(args,protected,changed,source,reports):
    tex=D/'task4_v184_paper.tex';pdf=D/'task4_v184_paper.pdf';sources=graph(tex);combined='\n'.join(p.read_text() for p in sorted(sources));normalized=norm(combined)
    assert 'tcn=PENDING' in tex.read_text()
    assert 'task4_v182_generated.tex' in combined and 'task4_v182_evidence_figure.tex' in combined
    assert '112 point values, 35 partial intervals and 13 fully missing intervals' in normalized
    assert 'twenty-three previously missing entries' in normalized
    for marker in ['28.8','39.9','2011','2024','greater city','estimated','Eurostat','Singapore']:
        assert marker in normalized,marker
    assert '14:31:18.850 UTC' in normalized and '326 selected' in normalized and '1,865' in normalized and '74 saved root' in normalized
    assert 'subsequent work is outside' in normalized and 'incomplete review record' in normalized
    # Wrapper must preserve native style and every old preamble command; input/comment changes only.
    old=(D/'task4_v182_paper.tex').read_text().split('\\begin{document}')[0]
    new=tex.read_text().split('\\begin{document}')[0]
    old='\n'.join(x for x in old.splitlines() if not x.startswith('%'))
    new='\n'.join(x for x in new.splitlines() if not x.startswith('%'))
    assert old==new,'Preamble changes exceed owned input/comment migration'
    pages=[norm(x) for x in pdftext(pdf).split('\f') if x.strip()];proxy=[norm(x) for x in pdftext(args.proxy_pdf).split('\f') if x.strip()]
    assert pages==proxy,'Direct/root normalized pages differ'
    aux=args.direct_aux.read_text()
    def label(n):return int(re.search(r'\\newlabel\{'+re.escape(n)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
    end=label('main-end');assert end<=25 and len(pages)==end+2 and label('LastPage')==len(pages)
    refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux));oldrefs=set(re.findall(r'\\bibcite\{([^}]+)\}',(R/'results/task4_v182_review/direct_labels.aux').read_text()))
    assert len(oldrefs)==52 and oldrefs<=refs and len(refs) in {53,54}
    cited={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',combined) for k in group.split(',')};assert cited<=refs,cited-refs
    body=norm(' '.join(pages))
    for marker in ['16.04938','0.483','2064','2.1092','2.2620','greater city','estimated','28.8','39.9','Singapore']:
        assert marker in body,marker
    bbox=T/'himcm_v184_audit_bbox.html';subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    nodes=E.parse(bbox).getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(nodes)==len(pages)
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{http://www.w3.org/1999/xhtml}word');assert not any(float(w.get('yMin'))>745 for w in words)
        if i:
            top=[w for w in words if float(w.get('yMin'))<65]
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert f'Page {i+1} of {len(pages)}' in pages[i]
    logs=[args.direct_log.read_text(),args.proxy_log.read_text()]
    for log in logs:assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning'])
    xml=T/'himcm_v184_audit_fonts.xml';subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(xml)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    fonts={};counts=Counter();small=[]
    for page in E.parse(xml).getroot().findall('page'):
        for font in page.findall('fontspec'):fonts[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if not value:continue
            font=fonts[span.get('font')];size=int(font['size']);family=re.sub(r'^[A-Z]{6}\+','',font['family']);counts[size,family]+=1
            if size<9:small.append(dict(pdf_page=int(page.get('number')),top=int(span.get('top')),extractor_size=size,font_family=family,text=value))
    write_table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Nominal12pt body/11pt native heads;mathsubscripts separately listed;all prior figures unchanged') for k,v in sorted(counts.items())])
    if small:write_table('small_spans.csv',small)
    requirements=list(csv.DictReader((R/'results/task4_v182_review/requirements.csv').open()));oldstatus={x['id']:x['status'] for x in requirements}
    points=pd.read_csv(R/'results/task4_v143_vintage/submitted_points.csv');assert len(points)==112 and int((points.submitted_year==2026).sum())==64
    for row in requirements:
        if row['id']=='U-vintage':
            markers=json.loads(row['passage_markers']);markers=['64 are dated 2026' if x=='64 are labelled 2026' else x for x in markers];row['passage_markers']=json.dumps(markers)
        hits=[]
        for marker in json.loads(row['passage_markers']):
            found=[i for i,page in enumerate(pages,1) if norm(marker).lower() in page.lower()];assert found,(row['id'],marker);hits+=found
        if hits:row['pdf_pages']=','.join(map(str,sorted(set(hits))))
        updates={
          'CI-file':f'{pdf.stat().st_size} bytes;one V184 owned PDF',
          'TEAM-independent-entry':f'V184 direct/root normalized text equal;{len(pages)}pages;0overfull',
          'PA-references':f'{len(refs)} compiled references;all prior52 retained plus official commute source evidence',
          'CI-budget':f'{end}main/reference pages;2additional provisionalAI pages;{25-end}mainpage margin',
          'CI-headers':f'Native summaryp1;Team #PENDING / Page x of{len(pages)} onp2-{len(pages)};emptyfooters',
          'U-template-format':f'Read-only class retained;{len(pages)}Letterpages;native heads/emptyfooters checked',
          'U-source-quality':'Original homicide source limitations retained; matching official greater-city work-journey means and Zurich estimatedflag disclosed;160scalar withdrawal cases;no source-lineage or historical-boundary proof',
          'AI-verification':'V181 frozen science,V184source/withdrawal/paper audit;V178fixedcapture retained',
          'U-collection-compression':'Existing compressed collection structure retained;sourceparagraph replaced with verified commute scope;no new uncertain-cell or data-admission claim',
          'AI-tool-disclosure':'Known Codexuse through10Nov;fixed V178prefix 74root labels326visible1865toolinputs remains incomplete',
        }
        if row['id'] in updates:row['evidence']=updates[row['id']]
        if row['id']=='PA-news':row['pdf_pages']=f"{label('news-start')}-{label('news-end')}"
        if row['id']=='PA-references':row['pdf_pages']=f"{label('news-end')+1}-{end}"
        if row['id'] in ['PA-ai-section','AI-tool-disclosure']:row['pdf_pages']=f'{end+1}-{end+2}'
        if row['id']=='U-template-format':row['pdf_pages']=f'1-{len(pages)}'
        if row['id']=='PA-ai-section':row['evidence']=f'Provisional incomplete AI appendix after{end}main/reference pages'
    assert len(requirements)==47 and all(x['status']==oldstatus[x['id']] for x in requirements)
    pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
    write_table('requirements.csv',requirements)
    visual=read(O/'visual_review.json');assert visual['pdf_sha256']==sha(pdf)
    assert visual.get('contact_sheets_reviewed_all_pages',visual.get('contact_overview_all_pages'))==list(range(1,len(pages)+1));assert visual.get('empty_footers_reviewed',visual.get('native_summary_headers_empty_footers_reviewed'))
    if args.expect_active:
        review=read(R/'design/task4_user_current_review.json');assert review==read(D/'task4_current_review.json')
        assert review['version']=='V184' and review['primary_model']=='V181' and review['pdf_sha256']==sha(pdf)
    result=dict(version='V184',status='pass',primary_model='V181',activation_status='active' if args.expect_active else 'verified_pending_activation',total_pages=len(pages),main_and_references_pages=end,main_page_margin=25-end,news_pages=[label('news-start'),label('news-end')],AI_pages=[end+1,end+2],compiled_references=len(refs),prior52_references_retained=True,scientific_files_unchanged=len(protected['science']),existing_manuscript_files_unchanged=len(protected['paper'])-len(changed),owned_pointer_files_changed=changed,shared_main_ref_class_unchanged=True,current_model_extensions_unchanged=True,existing_figures_and_numerical_assets_byte_unchanged=True,original_user_CSV_unchanged=True,primary_admissions=0,actual_primary_width_change=0,possible_champions=16,necessary_champions=0,conservative_recommendation='Zurich under retained baseline',independent_scalar_withdrawal_rows=160,withdrawal_reports=reports,source_review=source,diagnostic_sha256={str(p.relative_to(R)):sha(p) for p in [R/'scripts/task4_v184_commute_withdrawal.py',O/'summary.json',O/'commute_withdrawal_ranks.csv',O/'commute_withdrawal_bounds.csv']},source_graph_tex_files=len(sources),direct_root_text_equal=True,native_header_footer_checked=True,overfull_boxes=0,underfull_paragraphs_per_build=logs[0].count('Underfull'),underfull_counts=[x.count('Underfull') for x in logs],requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,AI_history_complete=False,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),verifier_sha256=sha(Path(__file__)),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(sources)},visual_review_scope=visual.get('scope'),full_page_images_reviewed=visual.get('full_page_images_reviewed'))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_review','tex_source_sha256']},indent=2))

if __name__=='__main__':main()
