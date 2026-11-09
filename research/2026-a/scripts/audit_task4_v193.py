"""Independently bind owned V193 review and delivery evidence to immutable V192 science."""
from pathlib import Path
from collections import Counter,defaultdict
import argparse,csv,hashlib,json,math,re,subprocess,unicodedata,xml.etree.ElementTree as E,zlib
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_user_v192_revision import revised_bounds
from task4_v5_model import NAMES,weights
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';D=P/'drafts';O=R/'results/task4_v193_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def table(p):return list(csv.DictReader(p.open()))
def frame(p):return pd.read_csv(p,float_precision='round_trip')
def norm(s):return ' '.join(unicodedata.normalize('NFKC',s).replace('\u00ad','').split())
def canon(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','').translate(str.maketrans({'–':'-','−':'-','—':'-'}))
    return re.sub(r'\s+',' ',re.sub(r'(?<=-)\s+(?=\w)','',s)).strip().casefold()
def phrase(marker,s):return re.search(r'(?<!\w)'+re.escape(canon(marker))+r'(?!\w)',canon(s)) is not None

def pdftext(p,mode='-layout'):return subprocess.check_output(['pdftotext',mode,str(p),'-'],text=True)
def graph(path,seen=None):
    seen=set() if seen is None else seen;path=path.resolve()
    if path in seen:return seen
    seen.add(path)
    for name in re.findall(r'\\input\{([^}]+)\}',path.read_text()):
        q=D/name
        if q.suffix!='.tex':q=q.with_suffix('.tex')
        assert q.exists(),q;graph(q,seen)
    return seen

def scores(a,w):
    result=[]
    for row in a:
        b=math.sqrt(math.fsum(float(v)*float(x)**2 for v,x in zip(w,row)))
        g=math.sqrt(math.fsum(float(v)*(1-float(x))**2 for v,x in zip(w,row)))
        result.append(100*b/(b+g))
    return np.array(result)
def values(l,h,w):
    a,b=scores(l,w),scores(h,w);r=np.array([max(0,float(np.delete(b,i).max()-a[i])) for i in range(len(a))])
    return a,b,r

def protect(active):
    saved=read(O/'protected_files.json');changed=[]
    for name,h in saved['science'].items():assert sha(R/name)==h,name
    for name,h in saved['paper'].items():
        if active and name in {'drafts/task4_current_review.json','drafts/task4_current_delivery.json'}:changed.append(name);continue
        if active and name=='AGENTS.md':
            s=(P/name).read_text()
            changes=[('Current primary evidence and controlled extensions are user16 V181','Current primary evidence and controlled extensions are user16 V192'),('(primary science V181; current version in the registry)','(primary science V192; current version in the registry)'),('V188 is the frozen preceding review.','V189 is the frozen preceding review.')]
            for old,new in changes:
                assert s.count(new)==1,(name,new);s=s.replace(new,old)
            assert hashlib.sha256(s.encode()).hexdigest()==h,'P AGENTS changed outside navigation'
            changed.append(name);continue
        assert sha(P/name)==h,name
    mutable={'task4_user_current_model.json','task4_user_current_extensions.json','task4_user_current_review.json','task4_user_current_delivery.json'}
    for name,h in saved['registries'].items():
        if active and name in mutable:continue
        assert sha(R/'design'/name)==h,name
    if active:
        model=read(R/'design/task4_user_current_model.json');ext=read(R/'design/task4_user_current_extensions.json')
        assert model['version']=='V192' and model['module']=='task4_user_v192_revision' and model['factory']=='revised_bounds'
        assert model['snapshot']=='design/task4_user_v192_snapshot.json'
        assert model['admissions']=='design/task4_user_v192_admissions.json' and model['results']=='results/task4_user_v192_revision'
        assert model['source_csv']=='data/task4_v117_team_intake/city_indicators.csv' and model['primary_dataset']=='user-provided16-city CSV'
        assert ext['extension_version']==ext['primary_evidence_version']=='V192'
        for part,v in ext['modules'].items():assert v['script']=='scripts/task4_v192_extensions.py '+part and v['results']=='results/task4_v192_'+part
    return saved,changed

def science():
    proof=read(R/'results/task4_v192_transition/verification.json');assert proof['status']=='pass'
    for group in ['source_sha256','result_sha256']:
        for name,h in proof[group].items():assert sha(R/name)==h,name
    snapshot=read(R/'design/task4_user_v192_snapshot.json')['source_sha256'];assert len(snapshot)==327
    for name,h in snapshot.items():assert sha(R/name)==h,name
    assert not any('current_' in Path(name).name and name.startswith('design/') for name in snapshot)
    f,l,h=revised_bounds();cities=f.city.tolist();assert l.shape==h.shape==(16,10)
    counts=[int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())];assert counts==[112,37,11]
    primary=frame(R/'results/task4_user_v192_revision/current_ranks.csv');refs={'fixed':weights(.1),'equal':np.full(10,.1)};widths={};historical=[]
    for ref,w in refs.items():
        a,b,r=values(l,h,w);v=primary[primary.weight_reference.eq(ref)].set_index('city').loc[cities]
        np.testing.assert_allclose(v.score_lower,a,atol=1e-11,rtol=0);np.testing.assert_allclose(v.score_upper,b,atol=1e-11,rtol=0);np.testing.assert_allclose(v.max_regret,r,atol=1e-11,rtol=0)
        assert v.index[v.decision_rank.eq(1)].tolist()==['Zurich'] and v.possible_champion.sum()==16 and v.necessary_champion.sum()==0
        if ref=='fixed':assert v.loc['Warsaw','decision_rank']==11 and v.loc['Vienna','decision_rank']==12
        widths[ref]=float(np.mean(b-a))
        for remove in [('Paris',),('Dublin',),('Paris','Dublin')]:
            ll=l.copy();hh=h.copy()
            for c in remove:ll[cities.index(c),NAMES.index('public_transport_density')]=0;hh[cities.index(c),NAMES.index('public_transport_density')]=1
            aa,bb,rr=values(ll,hh,w);choice=[cities[k] for k in range(16) if rr[k]<=rr.min()+1e-10];assert choice==['Zurich']
            historical.append(dict(removed=list(remove),weight_reference=ref,minimax=choice,mean_width=float(np.mean(bb-aa))))
    return f,l,h,widths,historical

def asset_checks(f,l,h,widths):
    A=D/'task4_v193_assets';manifest=read(A/'manifest.json')
    for field,base in [('source_sha256',R),('paper_input_sha256',P),('output_sha256',P)]:
        for name,digest in manifest.get(field,{}).items():assert sha(base/name)==digest,(field,name)
    source=frame(A/'source_intervals.csv').set_index(['city','weight_reference']).sort_index()
    original=frame(R/'results/task4_user_v192_revision/current_ranks.csv');original=original[original.weight_reference.eq('fixed')].set_index(['city','weight_reference']).sort_index();pd.testing.assert_frame_equal(source,original,check_exact=True)
    baseline=(A/'baseline.tex').read_text()
    for r in original.sort_values('decision_rank').itertuples():
        expected=f'{r.decision_rank} & {r.Index[0]} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f}'
        assert expected in baseline,expected
    matrixfiles=list(A.rglob('matrix.csv'))+list((D/'task4_v193_evidence_assets').glob('matrix.csv'));assert len(matrixfiles)==1,matrixfiles
    matrix=frame(matrixfiles[0]).set_index(['city','indicator']).loc[pd.MultiIndex.from_product([f.city.tolist(),NAMES])]
    np.testing.assert_array_equal(matrix.utility_lower.to_numpy().reshape(16,10),l);np.testing.assert_array_equal(matrix.utility_upper.to_numpy().reshape(16,10),h)
    assert Counter(matrix.state)==Counter(point=112,partial=37,unknown=11)
    unknown=Counter(matrix.reset_index().loc[matrix.reset_index().state.eq('unknown'),'indicator']);assert unknown==Counter(upper_secondary_ptr=8,travel=3)
    fm=read(matrixfiles[0].parent/'figure_manifest.json')
    assert fm['iteration']=='V193' and fm['model']=='V192' and fm['counts']==dict(point=112,partial=37,unknown=11)
    assert fm['unknown_by_indicator']==dict(travel=3,upper_secondary_ptr=8) and fm['plot_labels'][7]=='Travel burden'
    assert fm['city_order']==f.city.tolist() and fm['indicator_order']==NAMES and fm['matrix_sha256']==sha(matrixfiles[0])
    assert fm['admissions_sha256']==sha(R/'design/task4_user_v192_admissions.json')
    for ext,digest in fm['output_sha256'].items():assert sha(matrixfiles[0].parent/('identification_matrix.'+ext))==digest
    matrixpdf=next(matrixfiles[0].parent.glob('identification_matrix.pdf'));assert 'Travel burden' in matrixpdf.with_suffix('.svg').read_text()
    fonts=[]
    for p in [matrixpdf,A/'score_intervals.pdf']:
        sizes=[]
        for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',p.read_bytes(),re.S):
            try:raw=zlib.decompress(stream)
            except zlib.error:continue
            sizes.extend(float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw))
        info=subprocess.check_output(['pdfinfo',str(p)],text=True);width=float(re.search(r'Page size:\s+([0-9.]+)',info)[1]);assert sizes and min(sizes)*468/width>=9,(p,sizes,width)
        fonts.append(dict(asset=str(p.relative_to(P)),minimum_inserted_font_pt=min(sizes)*468/width))
    generated=(D/'task4_v193_generated.tex').read_text();macros={}
    for line in generated.splitlines():
        m=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line)
        if m:macros[m[1]]=m[2]
    assert macros['CurrentMeanWidth']==f"{widths['fixed']:.5f}" and macros['TotalWidthReduction']=='14.73' and macros['RevisionRankChanges']=='13'
    for marker in ['0.483','0.650','Dublin','Oslo']:assert marker in macros['MethodComparison']
    for marker in ['0.717','0.883','Oslo','Zurich']:assert marker in macros['PreferenceResults']
    assert '0.733' not in macros['PreferenceResults']
    pref=frame(R/'results/task4_v192_preferences/mc_city_summary.csv');k=pref[pref.concentration.eq(100)]
    pt=(A/'preferences.tex').read_text()
    for profile,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]:
        cells=[f"{100*float(k[k.profile.eq(profile)&k.city.eq(city)].iloc[0].minimax_recommendation_frequency):.2f}" for city in ['Zurich','Oslo','Singapore']]
        assert label+' & '+' & '.join(cells) in pt
    for city in ['Zurich','Oslo','Singapore']:
        row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{100*row.minimax_recommendation_frequency:.2f}' in macros['SummaryWeightMC']
    for city in ['Oslo','Zurich']:
        row=k[k.profile.eq('baseline')&k.city.eq(city)].iloc[0];assert f'{row.mean_decision_rank:.4f}' in macros['MonteCarloInterpretation']
    future=read(R/'results/task4_v192_future/summary.json');thresholds={x['city']:x for x in future['thresholds'] if x['weight_reference']=='fixed'}
    for city in ['Oslo','Singapore','Stockholm']:assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}" in macros['FutureThresholds']
    assert f"{100*thresholds['Berlin']['required_cost_reduction_fraction']:.3f}" in macros['EvidenceThresholdCheck']
    mc=frame(R/'results/task4_v192_future/future_mc_city_summary.csv')
    for arm,macro in [('conditional','FutureMonteCarlo'),('withdraw_historical_stage_proxy','ProxyWithdrawalMC')]:
        for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
            row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Zurich')&mc.evidence_arm.eq(arm)&mc.scenario.eq(scenario)].iloc[0]
            assert f'{100*row.recommendation_frequency:.2f}' in macros[macro]
    for key in ['EquityCase','AgeCase','CountryInterpretation','CaseReferences']:
        old=(D/'task4_v182_generated.tex').read_text();m=re.search(r'\\newcommand\{\\'+key+r'\}\{(.*)\}$',old,re.M);assert m and macros[key]==m[1],key
    revision=(A/'revision.tex').read_text();assert r'\tau_b=0.600' in revision and r'\tau_b=0.650' in revision
    assert '48 non-point' in revision and 'All 112 point' in revision and 'all 48 uncertain' in revision
    v=read(R/'results/task4_v192_diagnostics/summary.json')['vintage_cases'];v={(x['scenario'],x['weight_reference']):x for x in v};vt=(A/'vintage_table.tex').read_text()
    for sc,label in [('baseline','Retained input'),('pre2020_points','Before 2020'),('after2025_points','After 2025'),('non_ok_points','Non-ok flags'),('union_points','Union')]:
        assert f"{label} & {v[sc,'fixed']['withdrawn_point_cells']} & {'/'.join(v[sc,'fixed']['minimax_choices'])} & {'/'.join(v[sc,'equal']['minimax_choices'])} & {v[sc,'fixed']['mean_interval_width']:.2f}" in vt
    return fonts,matrixfiles[0],manifest


def content_checks():
    tex=D/'task4_v193_paper.tex';sources=graph(tex);combined='\n'.join(p.read_text() for p in sorted(sources));n=norm(combined)
    assert 'tcn=18213' in tex.read_text() and 'task4_v193_generated.tex' in tex.read_text()
    assert not any(old in combined for old in ['task4_v182_generated.tex','task4_v182_assets/','task4_v182_evidence_figure.tex'])
    assert '112 point values, 37 partial intervals and 11 fully missing intervals' in n
    assert 'twenty-five' in n and 'eight teacher-ratio' in n
    assert not any(x in n for x in ['35 partial intervals','13 fully missing intervals','twenty-three admitted supplements','twenty-three previously missing entries'])
    for marker in ['Tokyo','Warsaw','38','21','18','39','2024','2025','2026','unknown','directory','Świętokrzyska']:
        # TeX may encode accents in the Polish interchange name.
        if marker=='Świętokrzyska':assert ('Świętokrzyska' in combined or 'wi' in combined and 'tokrzyska' in combined)
        else:assert marker in combined,marker
    for marker in ['14:31:18.850 UTC','326 selected','1,865','74 saved root','incomplete review record','subsequent work is outside']:assert norm(marker) in n,marker
    vintage=(D/'task4_v193_vintage.tex').read_text();v=norm(vintage)
    for marker in ['7.14733','51.42357','46.59','Oslo','Jensen','twelve','unknown travel','Singapore','below','counterexample','not measured errors or future probabilities']:
        assert marker.casefold() in v.casefold(),marker
    assert '\\delta' in vintage and '(1-' in vintage and '(1+' in vintage
    assert '7.15\\%' not in vintage and '51.42\\%' not in vintage
    # Existing factual/conditional case material must survive the new source insertion.
    for marker in ['0.200134','0.129091','0.226686','499950','681503','not observed age effects','Every primary city belongs to a different country','legacy25 V117','not representative student opinion']:
        assert norm(marker) in n,marker
    oldcore=(D/'task4_v189_core.tex').read_text();core=(D/'task4_v193_core.tex').read_text()
    section=r'\section{Model revision and extension}'
    assert core.split(section,1)[1].replace('task4_v193_assets/','task4_v182_assets/')==oldcore.split(section,1)[1],'Existing future/preference/fairness/age/country text changed'
    start=r'\section{Establishing the baseline evaluation model}';stop=r'\subsection{Scoring results and interpretation}'
    assert core.split(start,1)[1].split(stop,1)[0]==oldcore.split(start,1)[1].split(stop,1)[0],'Scoring/weight definitions changed'
    manifest=read(D/'task4_v193_manifest.json')
    for field,base in [('source_sha256',R),('paper_input_sha256',P)]:
        for name,digest in manifest[field].items():assert sha(base/name)==digest,name
    ai=D/'task4_v193_ai.tex'
    if ai.exists():
        old=(D/'task4_v184_ai.tex').read_text();assert ai.read_text()==old.replace('V181','V192'),'AI changed beyond scientific version rebinding'
    return sources,combined


def delivery_checks(pdf,pages,nodes,end,news,refcount,active):
    requirements=table(O/'requirements.csv');prior=table(R/'results/task4_v190_delivery/requirements.csv');assert len(requirements)==len(prior)==47
    assert {r['id']:r['status'] for r in requirements}=={r['id']:r['status'] for r in prior}
    pending=[r['id'] for r in requirements if r['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
    # Scope-aware anchor evidence is supplied by the parent delivery builder.
    anchorfile=O/'anchor_hits.csv';assert anchorfile.exists(),'Current delivery requires independently checkable scoped anchors'
    anchors=table(anchorfile);grouped=defaultdict(list);raw=pdftext(pdf,'-raw').split('\f')[:-1];wordpages=[' '.join(w.text or '' for w in node.findall('.//{*}word')) for node in nodes]
    for row in anchors:
        lo,hi=int(row['allowed_page_start']),int(row['allowed_page_end']);assert 1<=lo<=hi<=len(pages)
        if row['match_mode']=='line':hits=[i for i in range(lo,hi+1) if any(canon(x)==canon(row['marker']) for x in raw[i-1].splitlines())]
        else:hits=[i for i in range(lo,hi+1) if phrase(row['marker'],wordpages[i-1])]
        assert hits and ','.join(map(str,hits))==row['hit_pages'],(row['id'],row['marker'],hits,row['hit_pages'])
        grouped[row['id']].append((row['marker'],hits))
    for row in requirements:
        markers=json.loads(row['passage_markers']);assert markers==[m for m,_ in grouped[row['id']]],row['id']
        expected=sorted({p for _,hits in grouped[row['id']] for p in hits})
        if row['id']=='PA-references':expected=list(range(news[-1]+1,end+1))
        elif row['id']=='U-template-format':assert not markers and row['pdf_pages']==f'1-{len(pages)}';continue
        assert row['pdf_pages']==','.join(map(str,expected)),row['id']
    assert not phrase('Exa','example examination extra') and phrase('Exa','Exa search')
    byid={x['id']:x for x in requirements};assert byid['PA-toc']['pdf_pages']=='2'
    assert all(int(p)>=end+1 for p in byid['AI-tool-disclosure']['pdf_pages'].split(','))
    assert '4260' in byid['U-MC-precision']['evidence'] and '180' in byid['U-MC-precision']['evidence']
    assert 'V192' in byid['U-preserve']['evidence'] or 'Tokyo' in byid['U-preserve']['evidence']
    assert '0page' in norm(byid['CI-budget']['evidence']).replace(' ','') or '0 main-page' in byid['CI-budget']['scope_or_remaining_action'] or 'Zero main-page' in byid['CI-budget']['scope_or_remaining_action']
    if active:
        review=read(R/'design/task4_user_current_review.json');delivery=read(R/'design/task4_user_current_delivery.json')
        assert review==read(D/'task4_current_review.json') and delivery==read(D/'task4_current_delivery.json')
        assert review['version']=='V193' and review['primary_model']=='V192' and review['pdf_sha256']==sha(pdf)
        assert review['tex']=='drafts/task4_v193_paper.tex' and review['pdf']=='drafts/task4_v193_paper.pdf' and review['root_entry']=='task4_v193_review_entry.tex'
        assert delivery['version']=='V193' and delivery['review_version']=='V193' and delivery['primary_model']=='V192'
        assert delivery['pdf_sha256']==sha(pdf) and delivery['pdf']==review['pdf'] and delivery['requirements']==47 and delivery['pending_count']==13
        assert not review['submission_ready'] and not delivery['submission_ready']
    return requirements,pending,len(anchors)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--expect-active',action='store_true');parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    saved,changed=protect(args.expect_active);f,l,h,widths,historical=science();fonts,matrixfile,assetmanifest=asset_checks(f,l,h,widths);sources,combined=content_checks()
    precision=read(R/'results/task4_v192_mc_precision/summary.json');pairs=read(R/'results/task4_v192_mean_rank_comparisons/summary.json')
    assert precision['base_means']==2064 and precision['settings']==37 and pairs['certified_pairs']==4260 and pairs['unresolved_pairs']==180 and pairs['settings_with_unique_smallest_expected_mean_rank']==22
    if args.source_only:print(json.dumps(dict(status='pass',mean_widths=widths,assets=fonts,historical_inventory_withdrawals=historical),indent=2));return
    pdf=D/'task4_v193_paper.pdf';proxy=T/'himcm_v193_proxy/task4_v193_review_entry.pdf';aux=(T/'himcm_v193_build/task4_v193_paper.aux').read_text()
    pages=[norm(s) for s in pdftext(pdf).split('\f') if s.strip()];assert pages==[norm(s) for s in pdftext(proxy).split('\f') if s.strip()]
    label=lambda name:int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1]);end=label('main-end');news=[label('news-start'),label('news-end')]
    assert end<=25 and len(pages)==end+2==label('LastPage');assert len(pages)==27 and end==25
    refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux));oldrefs=set(re.findall(r'\\bibitem\{([^}]+)\}',(D/'task4_v184_references.tex').read_text()))
    assert oldrefs<=refs and len(refs)>53
    cited={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',combined) for k in group.split(',')};assert cited<=refs,cited-refs
    # The inherited CaseReferences macro contributes some historical bibliography keys.
    oldcompiled=set(re.findall(r'\\bibcite\{([^}]+)\}',(R/'results/task4_v186_review/direct_labels.aux').read_text()));assert oldcompiled<=refs and len(oldcompiled)==53
    nodes=E.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{*}page');assert len(nodes)==len(pages)
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{*}word');assert not any(float(w.get('yMin'))>745 for w in words),('footer',i+1)
        if i:
            top=[w for w in words if float(w.get('yMin'))<65]
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top);assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert any(w.text=='18213' for w in top) and f'Page {i+1} of {len(pages)}' in pages[i]
        else:assert '18213' in pages[0] and 'PENDING' not in pages[0]
    logs=[]
    for folder,name in [('himcm_v193_build','task4_v193_paper'),('himcm_v193_proxy','task4_v193_review_entry')]:
        log=(T/folder/(name+'.log')).read_text();assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning']);logs.append(log)
    complete=norm(' '.join(pages))
    for marker in ['16.03907','0.717','0.600','2064','37','2.1092','2.2620','14.73','not sampling confidence intervals','incomplete review record']:assert marker in complete,marker
    # Enumerate body font evidence for new numerical/source prose; no all-glyph claim.
    xml=T/'himcm_v193_audit_fonts.xml';subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(xml)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    fontmap={};spans=[]
    for page in E.parse(xml).getroot().findall('page'):
        for font in page.findall('fontspec'):fontmap[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if any(x in value for x in ['7.14733','51.42357','16.03907']):spans.append((value,int(fontmap[span.get('font')]['size'])))
    assert spans and min(v for _,v in spans)>=12,spans
    requirements,pending,anchors=delivery_checks(pdf,pages,nodes,end,news,len(refs),args.expect_active)
    value=read(R/'design/task4_user_format_reference.json');assert value['actual_control_number']=='PENDING' and value['actual_registered_number_verified'] is False and value['display_control_number']=='18213' and value['display_number_provisional'] is True
    result=dict(version='V193',status='pass',primary_model='V192',activation_status='active' if args.expect_active else 'verified_pending_activation',total_pages=len(pages),main_and_references_pages=end,main_page_margin=25-end,news_pages=news,AI_pages=[end+1,end+2],compiled_references=len(refs),prior53_references_retained=True,scientific_files_unchanged=len(saved['science']),existing_manuscript_files_unchanged=len(saved['paper'])-len(changed),owned_pointer_files_changed=changed,shared_main_ref_class_unchanged=True,original_user_CSV_unchanged=True,point_partial_unknown=[112,37,11],cumulative_supplements=25,possible_champions=16,necessary_champions=0,conservative_recommendation='Zurich',mean_widths=widths,historical_inventory_withdrawal_checks=historical,source_graph_tex_files=len(sources),scientific_source_identity_checked=True,direct_root_text_equal=True,native_header_footer_checked=True,display_control_number='18213',actual_registered_number_verified=False,figure_fonts_checked=fonts,new_numeric_body_font_min=min(v for _,v in spans),overfull_boxes=0,underfull_paragraphs_per_build=[x.count('Underfull') for x in logs],requirements=47,prior47_statuses_preserved=True,pending_gates_preserved=pending,scoped_delivery_anchors_verified=anchors,submission_ready=False,server_compile_verified=False,default_main_setting_changed=False,AI_history_complete=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),source_sha256={str(p.relative_to(R)):sha(p) for p in [Path(__file__),O/'protected_files.json',R/'design/task4_user_v192_snapshot.json',R/'results/task4_v192_transition/verification.json',R/'results/task4_v192_source_diagnostics/summary.json']},tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(sources)},delivery_sha256={n:sha(O/n) for n in ['requirements.csv','anchor_hits.csv']},visual_review_scope='Separate parent raster review; this audit checks numeric assets, source scope, fonts, page geometry and scoped anchors, not raster appearance.')
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','tex_source_sha256','delivery_sha256']},indent=2))
if __name__=='__main__':main()
