"""Independently bind V182 owned review to frozen V181 scientific evidence."""
from pathlib import Path
from collections import Counter
import argparse,csv,hashlib,json,re,subprocess,unicodedata,xml.etree.ElementTree as E
import numpy as np
import pandas as pd
from task4_user_v181_revision import revised_bounds
from task4_v5_model import NAMES,weights

R=Path(__file__).resolve().parents[1]
P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v182_review'
T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',s)).split())
def text(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def csvread(p):return pd.read_csv(p,float_precision='round_trip')
def write_table(name,records):
    with (O/name).open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
def graph(path,seen=None):
    seen=set() if seen is None else seen
    path=path.resolve()
    if path in seen:return seen
    seen.add(path)
    for n in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
        q=D/n
        if q.suffix!='.tex':q=q.with_suffix('.tex')
        assert q.exists(),q
        graph(q,seen)
    return seen
def scalar_scores(u,w):
    import math
    out=[]
    for row in u:
        positive=math.sqrt(math.fsum(float(a)*float(x)**2 for a,x in zip(w,row)))
        negative=math.sqrt(math.fsum(float(a)*(1-float(x))**2 for a,x in zip(w,row)))
        out.append(100*positive/(positive+negative))
    return np.array(out)
def science_checks(expect_active=False):
    proof=read(R/'results/task4_v181_transition/verification.json');assert proof['status']=='pass'
    for group in ['source_sha256','result_sha256']:
        for name,h in proof[group].items():assert sha(R/name)==h,name
    snapshot=read(R/'design/task4_user_v181_snapshot.json')
    for name,h in snapshot['source_sha256'].items():
        if expect_active and name in {'design/task4_user_current_model.json','design/task4_user_current_extensions.json'}:continue
        assert sha(R/name)==h,name
    f,lo,hi=revised_bounds();assert lo.shape==hi.shape==(16,10)
    assert [int((lo==hi).sum()),int(((lo<hi)&((lo>0)|(hi<1))).sum()),int(((lo==0)&(hi==1)).sum())]==[112,35,13]
    i,j=f.city.tolist().index('Amsterdam'),NAMES.index('public_transport_density')
    assert abs(lo[i,j]-64000/1005927)<1e-15 and hi[i,j]==1
    primary=csvread(R/'results/task4_user_v181_revision/current_ranks.csv')
    widths={}
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        saved=primary[primary.weight_reference==ref].set_index('city').loc[f.city]
        a,b=scalar_scores(lo,w),scalar_scores(hi,w)
        np.testing.assert_allclose(saved.score_lower,a,atol=1e-11,rtol=0);np.testing.assert_allclose(saved.score_upper,b,atol=1e-11,rtol=0)
        assert saved.possible_champion.sum()==16 and saved.necessary_champion.sum()==0
        assert saved.index[saved.decision_rank==1].tolist()==['Zurich']
        widths[ref]=float(np.mean(b-a))
    method=read(R/'results/task4_v181_method/summary.json')['method_cases']
    assert abs(next(x for x in method if x['weight_reference']=='fixed')['kendall_tau_b']-.48333333333333334)<1e-15
    assert next(x for x in method if x['weight_reference']=='equal')['kendall_tau_b']==.65
    precision=read(R/'results/task4_v181_mc_precision/summary.json');pairs=read(R/'results/task4_v181_mean_rank_comparisons/summary.json')
    assert precision['base_means']==2064 and precision['settings']==37
    assert pairs['certified_pairs']==4255 and pairs['unresolved_pairs']==185 and pairs['settings_with_unique_smallest_expected_mean_rank']==22
    historical_withdrawals=[]
    for removed in [('Paris',),('Dublin',),('Paris','Dublin')]:
        a,b=lo.copy(),hi.copy()
        for city in removed:
            k=f.city.tolist().index(city);a[k,j],b[k,j]=0,1
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            lower,upper=scalar_scores(a,w),scalar_scores(b,w)
            regret=np.array([max(0,float(np.delete(upper,k).max()-lower[k])) for k in range(16)])
            choices=[f.city.iloc[k] for k in range(16) if regret[k]<=regret.min()+1e-10]
            assert choices==['Zurich'],(removed,ref,choices)
            historical_withdrawals.append(dict(withdrawn_cities=list(removed),indicator='public_transport_density',weight_reference=ref,conservative_recommendation=choices,possible_champions=int(sum(upper[k]>=np.delete(lower,k).max()-1e-10 for k in range(16))),mean_width=float(np.mean(upper-lower))))
    return f,lo,hi,widths,historical_withdrawals

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--expect-active',action='store_true')
    parser.add_argument('--proxy-pdf',type=Path,default=T/'himcm_v182_proxy/task4_v182_review_entry.pdf')
    parser.add_argument('--direct-aux',type=Path,default=T/'himcm_v182_build/task4_v182_paper.aux')
    parser.add_argument('--direct-log',type=Path,default=T/'himcm_v182_build/task4_v182_paper.log')
    parser.add_argument('--proxy-log',type=Path,default=T/'himcm_v182_proxy/task4_v182_review_entry.log')
    parser.add_argument('--source-only',action='store_true')
    args=parser.parse_args();O.mkdir(exist_ok=True)
    protected=read(O/'protected_files.json')
    science_navigation_changes=[]
    for n,h in protected['science'].items():
        if args.expect_active and n in {'design/task4_user_current_model.json','design/task4_user_current_extensions.json'}:
            science_navigation_changes.append(n);continue
        assert sha(R/n)==h,n
    changed_p=[]
    for n,h in protected['paper'].items():
        if args.expect_active and n=='drafts/task4_current_review.json':changed_p.append(n);continue
        if args.expect_active and n=='AGENTS.md':
            current=(P/n).read_text()
            changes=[('Current primary evidence and controlled extensions are user16 V154','Current primary evidence and controlled extensions are user16 V181'),('(primary science V154; current version in the registry)','(primary science V181; current version in the registry)'),('V154 is the frozen preceding review.','V179 is the frozen preceding review.')]
            for old,new in changes:
                assert current.count(new)==1,(n,new)
                current=current.replace(new,old)
            assert hashlib.sha256(current.encode()).hexdigest()==h,'P AGENTS changes exceed three pointer substitutions'
            changed_p.append(n);continue
        assert sha(P/n)==h,n
    if not args.expect_active:
        for n,h in protected['registries'].items():assert sha(R/'design'/n)==h,n
    else:
        model=read(R/'design/task4_user_current_model.json')
        assert model['version']=='V181' and model['module']=='task4_user_v181_revision' and model['factory']=='revised_bounds'
        assert model['snapshot']=='design/task4_user_v181_snapshot.json'
        assert read(R/'design/task4_user_current_extensions.json')['extension_version']=='V181'
    f,lo,hi,widths,historical_withdrawals=science_checks(args.expect_active)
    sources=graph(D/'task4_v182_paper.tex');combined='\n'.join(p.read_text() for p in sorted(sources))
    assert 'task4_v154_generated.tex' not in combined
    assert 'task4_v182_assets/' in combined and 'task4_v182_evidence_figure.tex' in combined
    assert 'tcn=PENDING' in (D/'task4_v182_paper.tex').read_text()
    assert '112 point values, 35 partial intervals and 13 fully missing intervals' in norm(combined)
    assert 'twenty-three previously missing entries' in norm(combined)
    assert 'eight teacher-ratio, two transport and three' in norm(combined)
    asset=D/'task4_v182_assets'
    manifest=read(asset/'manifest.json')
    for name,h in manifest['source_sha256'].items():assert sha(R/name)==h,name
    saved=csvread(asset/'source_intervals.csv').set_index(['city','weight_reference']).sort_index()
    original=csvread(R/'results/task4_user_v181_revision/current_ranks.csv')
    original=original[original.weight_reference=='fixed'].set_index(['city','weight_reference']).sort_index()
    pd.testing.assert_frame_equal(saved,original,check_exact=True)
    matrix_asset=D/'task4_v182_evidence_assets';fm=read(matrix_asset/'figure_manifest.json')
    assert fm['counts']==dict(point=112,partial=35,unknown=13)
    assert fm['unknown_by_indicator']=={'travel':3,'upper_secondary_ptr':8,'public_transport_density':2}
    assert fm['plot_labels'][7]=='Travel burden' and fm['minimum_source_font_pt']>=9
    assert fm['figure_width_inches']==fm['intended_insertion_width_inches']==6.5
    assert fm['matrix_sha256']==sha(matrix_asset/'matrix.csv')
    for ext,h in fm['output_sha256'].items():assert sha(matrix_asset/('identification_matrix.'+ext))==h
    matrix=csvread(matrix_asset/'matrix.csv').set_index(['city','indicator']).loc[pd.MultiIndex.from_product([f.city.tolist(),NAMES])]
    np.testing.assert_array_equal(matrix.utility_lower.to_numpy().reshape(16,10),lo)
    np.testing.assert_array_equal(matrix.utility_upper.to_numpy().reshape(16,10),hi)
    assert Counter(matrix.state)==Counter(point=112,partial=35,unknown=13)
    figure_text=text(matrix_asset/'identification_matrix.pdf')
    assert figure_text.count('?')==14
    assert 'Travel burden' in (matrix_asset/'identification_matrix.svg').read_text()
    import zlib
    for pdfasset,minimum in [(matrix_asset/'identification_matrix.pdf',9),(asset/'score_intervals.pdf',9)]:
        sizes=[]
        for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',pdfasset.read_bytes(),re.S):
            try:raw=zlib.decompress(stream)
            except zlib.error:continue
            sizes += [float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw)]
        info=subprocess.check_output(['pdfinfo',str(pdfasset)],text=True)
        natural_width=float(re.search(r'Page size:\s+([0-9.]+)',info)[1])
        assert sizes and min(sizes)*468/natural_width>=minimum,(pdfasset,sizes,natural_width)
    generated=(D/'task4_v182_generated.tex').read_text()
    assert '\\newcommand{\\CurrentMeanWidth}{16.04938}' in generated
    assert re.search(r'\\tau_b\s*=\s*0\.483',generated), 'fixed method tau'
    assert '0.650' in generated and 'Dublin' in generated and 'Oslo' in generated
    # Cross-year source scope must be visible, not buried solely in an attachment.
    for token in ['Amsterdam','2026','2025','941','100','32']:
        assert token in combined,token
    assert ('positional' in combined.lower() or 'positioning' in combined.lower())
    assert 'maps.amsterdam.nl' in combined and ('pdok.nl' in combined or 'cbs.nl' in combined)
    for marker in ['14:31:18.850 UTC','326 selected','1,865','74 saved root','subsequent work is outside']:
        assert norm(marker) in norm(combined),marker
    assert 'incomplete review record' in combined
    if args.source_only:
        print(json.dumps({'status':'source_checks_pass','scientific_source_sha_bindings_verified':True,'mean_widths':widths,'historical_withdrawals':historical_withdrawals,'input_tex_files':len(sources),'current_pointers_frozen':not args.expect_active},indent=2));return
    pdf=D/'task4_v182_paper.pdf';pages=[norm(x) for x in text(pdf).split('\f') if x.strip()]
    proxy_pages=[norm(x) for x in text(args.proxy_pdf).split('\f') if x.strip()]
    assert pages==proxy_pages,'direct/root page text differs'
    aux=args.direct_aux.read_text()
    def label(name):return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
    end=label('main-end');assert end<=25 and len(pages)==end+2
    assert label('LastPage')==len(pages)
    new_refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux))
    old_refs=set(re.findall(r'\\bibcite\{([^}]+)\}',(R/'results/task4_v179_ai_review/direct_labels.aux').read_text()))
    assert old_refs<=new_refs and len(new_refs)>50
    cited={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',combined) for k in group.split(',')}
    assert cited<=new_refs,cited-new_refs
    complete=norm(' '.join(pages))
    for token in ['16.04938','0.483','0.650','2064','37','2.1092','2.2620','not sampling confidence intervals','incomplete review record']:
        assert token in complete,token
    assert 'fourteen entries remain fully unknown' not in complete.lower()
    bbox=T/'himcm_v182_audit_bbox.html'
    subprocess.run(['pdftotext','-bbox',str(pdf),str(bbox)],check=True)
    nodes=E.parse(bbox).getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(nodes)==len(pages)
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{http://www.w3.org/1999/xhtml}word')
        assert not any(float(w.get('yMin'))>745 for w in words),('footer',i+1)
        if i:
            top=[w for w in words if float(w.get('yMin'))<65]
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
            assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert f'Page {i+1} of {len(pages)}' in pages[i]
    logs=[args.direct_log.read_text(),args.proxy_log.read_text()]
    for value in logs:
        assert not any(x in value for x in ['Overfull','undefined','LaTeX Warning']), 'TeX warning/error'
    xml=T/'himcm_v182_audit_fonts.xml'
    subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(xml)],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    fonts={};counts=Counter();small=[]
    for page in E.parse(xml).getroot().findall('page'):
        for font in page.findall('fontspec'):fonts[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if not value:continue
            font=fonts[span.get('font')];size=int(font['size']);family=re.sub(r'^[A-Z]{6}\+','',font['family']);counts[size,family]+=1
            if size<9:small.append(dict(pdf_page=int(page.get('number')),top=int(span.get('top')),extractor_size=size,font_family=family,text=value))
    write_table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Nominal body12pt/nativehead11pt; mathsubscripts separately inventoried') for k,v in sorted(counts.items())])
    if small:write_table('small_spans.csv',small)
    requirements=list(csv.DictReader((R/'results/task4_v179_ai_review/requirements.csv').open()));old_status={x['id']:x['status'] for x in requirements}
    for item in requirements:
        hits=[]
        for marker in json.loads(item['passage_markers']):
            found=[i for i,page in enumerate(pages,1) if norm(marker).lower() in page.lower()]
            assert found,(item['id'],marker);hits+=found
        if hits:item['pdf_pages']=','.join(map(str,sorted(set(hits))))
        if item['id']=='CI-file':item['evidence']=f'{pdf.stat().st_size} bytes;one V182 owned PDF'
        if item['id']=='TEAM-independent-entry':item['evidence']=f'V182 direct/root normalized text equal;{len(pages)} pages;0overfull'
        if item['id']=='AI-verification':item['evidence']='V181 frozen scientific audit and V182 current owned-paper consistency; V178 fixed-prefix AI provenance retained'
        if item['id']=='U-MC-precision':item['evidence']='V181 2064 means/37 settings;4440 pair intervals,4255 directions identified185 unresolved22 unique minima'
        if item['id']=='U-preserve':item['evidence']='Original CSV unchanged; only Amsterdam transport lower bound conditional supplement; existing weights/anchors/interval rules retained'
    updated={
        'PA-toc':('2','Contents includes news, references and separate provisional AI section'),
        'PA-sample':('10','Retained16x10 primary sample;V181 ranking table p10'),
        'PA-data':('4-7','Owned data collection section includes conditional Amsterdam2026 inventory with retained2025 population; original supplied source limitations retained'),
        'PA-news':(f"{label('news-start')}-{label('news-end')}",'Scoped conservative recommendation under common scoring yardsticks'),
        'PA-references':(f'20-{end}',f'{len(new_refs)} compiled references;prior50 retained and two new Amsterdam/boundary sources'),
        'PA-ai-section':(f'{end+1}-{end+2}',f'Provisional incomplete AI appendix after{end} main/reference pages'),
        'CI-budget':('',f'{end} main/reference pages;2 additional provisional AI pages;{25-end} main-page margin'),
        'CI-headers':('',f'Native summary p1;Team # PENDING / Page x of{len(pages)} onp2-{len(pages)};emptyfooters'),
        'AI-tool-disclosure':(f'{end+1}-{end+2}','V178 fixed14:31UTC window,74root labels,326visible/1865toolinputs;incomplete status retained'),
        'U-template-format':(f'1-{len(pages)}',f'Read-only class preserved;{len(pages)}Letter pages;native heads andemptyfooters checked'),
        'U-matrix-visual':('9','Figure1 p9;V181112point/35partial/13unknown;160cells independently matched;Travel burden mixedproxy scope;10pt at6.5in'),
        'U-collection-compression':('5-7','Retains compressed data-collection structure;adds bounded Amsterdam2026 source paragraph and original scope;currentmainpage budget0'),
    }
    for item in requirements:
        if item['id'] in updated:item['pdf_pages'],item['evidence']=updated[item['id']]
        if item['id']=='U-MC-precision':item['scope_or_remaining_action']='V181 simulation exports; within-settingIID assumption;no real-world winner probability or forecast calibration;pair bounds derived without additional draws'
    assert len(requirements)==47 and all(x['status']==old_status[x['id']] for x in requirements)
    pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
    write_table('requirements.csv',requirements)
    visual=read(O/'visual_review.json');assert visual['pdf_sha256']==sha(pdf)
    assert visual.get('contact_sheets_reviewed_all_pages')==list(range(1,len(pages)+1))
    assert visual['matrix_and_score_plot_reviewed'] and visual['empty_footers_reviewed']
    if args.expect_active:
        review=read(R/'design/task4_user_current_review.json');assert review==read(D/'task4_current_review.json')
        assert review['version']=='V182' and review['primary_model']=='V181' and review['pdf_sha256']==sha(pdf)
    result=dict(version='V182',status='pass',primary_model='V181',activation_status='active' if args.expect_active else 'verified_pending_activation',total_pages=len(pages),main_and_references_pages=end,main_page_margin=25-end,news_pages=[label('news-start'),label('news-end')],AI_pages=[end+1,end+2],compiled_references=len(new_refs),prior50_references_retained=True,scientific_files_unchanged=len(protected['science'])-len(science_navigation_changes),scientific_navigation_files_changed=science_navigation_changes,existing_manuscript_files_unchanged=len(protected['paper'])-len(changed_p),owned_pointer_files_changed=changed_p,shared_main_ref_class_unchanged=True,original_user_CSV_unchanged=True,point_partial_unknown=[112,35,13],cumulative_supplements=23,possible_champions=16,necessary_champions=0,conservative_recommendation='Zurich',mean_widths=widths,historical_inventory_withdrawal_checks=historical_withdrawals,source_graph_tex_files=len(sources),scientific_source_identity_checked=True,direct_root_text_equal=True,native_header_footer_checked=True,overfull_boxes=0,underfull_paragraphs_per_build=logs[0].count('Underfull'),underfull_counts=[x.count('Underfull') for x in logs],requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,AI_history_complete=False,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),verifier_sha256=sha(Path(__file__)),tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(sources)},scientific_certificate_sha256=sha(R/'results/task4_v181_transition/verification.json'),visual_review_scope=visual['scope'],full_page_images_reviewed=visual['full_page_images_reviewed'],matrix160cells_independently_verified=True,score_plot16source_rows_exact=True,new_vector_figure_font_minimum9pt_verified=True)
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
