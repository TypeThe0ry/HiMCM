"""Independent, scoped V198 paper-to-V197 audit; run before activation.

This checks numerical artifacts, key prose and page geometry. It does not certify
source quality, all prose claims, visual appearance, or final team readiness.
"""
from pathlib import Path
import csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET,zlib
import numpy as np
import pandas as pd
from task4_user_v197_revision import revised_bounds
from task4_v5_model import NAMES,weights
from audit_task4_v193 import graph,norm,values
R=Path(__file__).resolve().parents[1]; P=R.parents[2]/'HiMCM-Overleaf'; D=P/'drafts'; O=R/'results/task4_v198_review'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frame(p):return pd.read_csv(p,float_precision='round_trip')
def check_protection():
    frozen=read(R/'results/task4_v197_transition/baseline_protection.json')
    for group,base in [('science',R),('paper',P),('registries',R)]:
        for name,digest in frozen[group].items():assert sha(base/name)==digest,(group,name)
    snapshot=read(R/'design/task4_user_v197_snapshot.json')['source_sha256'];assert len(snapshot)==361
    for name,digest in snapshot.items():assert sha(R/name)==digest,name
    proof=read(R/'results/task4_v197_transition/verification.json');assert proof['status']=='pass'
    for group in ('source_sha256','result_sha256'):
        for name,digest in proof[group].items():assert sha(R/name)==digest,name
    return {k:len(frozen[k]) for k in ('science','paper','registries')}
def check_science():
    f,l,h=revised_bounds(); assert l.shape==h.shape==(16,10)
    assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,37,11]
    src=frame(R/'results/task4_user_v197_revision/current_ranks.csv');out={}
    for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
        a,b,r=values(l,h,w);v=src[src.weight_reference.eq(ref)].set_index('city').loc[f.city.tolist()]
        for col,arr in [('score_lower',a),('score_upper',b),('max_regret',r)]:np.testing.assert_allclose(v[col],arr,atol=1e-11,rtol=0)
        assert v.index[v.decision_rank.eq(1)].tolist()==['Zurich'];out[ref]=float(np.mean(b-a))
    pairs=frame(R/'results/task4_v197_mean_rank_comparisons/pairs.csv')
    pair=pairs[(pairs.family=='preferences')&(pairs.city_a=='Oslo')&(pairs.city_b=='Zurich')&pairs.setting.str.contains('baseline')&pairs.setting.str.contains('100')].iloc[0]
    assert pair.sample_mean_a==2.1779 and pair.sample_mean_b==2.0269 and pair.gap_lower<0<pair.gap_upper and pair.classification=='unresolved'
    return f,l,h,out,dict(lower=float(pair.gap_lower),upper=float(pair.gap_upper))
def check_assets(f,l,h,widths):
    A=D/'task4_v198_assets'; source=frame(A/'source_intervals.csv').set_index(['city','weight_reference']).sort_index()
    expected=frame(R/'results/task4_user_v197_revision/current_ranks.csv');expected=expected[expected.weight_reference.eq('fixed')].set_index(['city','weight_reference']).sort_index()
    pd.testing.assert_frame_equal(source,expected,check_exact=True)
    baseline=(A/'baseline.tex').read_text()
    for r in expected.sort_values('decision_rank').itertuples():
        assert f'{r.decision_rank} & {r.Index[0]} & {r.score_lower:.2f}--{r.score_upper:.2f} & {r.max_regret:.2f}' in baseline
    candidates=list(A.rglob('matrix.csv'))+list((D/'task4_v198_evidence_assets').glob('matrix.csv'));assert len(candidates)==1,candidates
    matrix=frame(candidates[0]).set_index(['city','indicator']).loc[pd.MultiIndex.from_product([f.city.tolist(),NAMES])]
    np.testing.assert_array_equal(matrix.utility_lower.to_numpy().reshape(16,10),l);np.testing.assert_array_equal(matrix.utility_upper.to_numpy().reshape(16,10),h)
    assert matrix.state.value_counts().to_dict()=={'point':112,'partial':37,'unknown':11}
    fm=read(candidates[0].parent/'figure_manifest.json');assert fm['matrix_sha256']==sha(candidates[0])
    for ext,digest in fm['output_sha256'].items():assert sha(candidates[0].parent/('identification_matrix.'+ext))==digest
    fonts=[]
    for pdf in [candidates[0].parent/'identification_matrix.pdf',A/'score_intervals.pdf']:
        sizes=[]
        for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',pdf.read_bytes(),re.S):
            try:raw=zlib.decompress(stream)
            except zlib.error:continue
            sizes.extend(float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw))
        width=float(re.search(r'Page size:\s+([0-9.]+)',subprocess.check_output(['pdfinfo',str(pdf)],text=True))[1]);assert sizes and min(sizes)*468/width>=9,(pdf,sizes,width)
        fonts.append(dict(asset=str(pdf.relative_to(P)),minimum_inserted_font_pt=min(sizes)*468/width))
    macros={m[1]:m[2] for line in (D/'task4_v198_generated.tex').read_text().splitlines() if (m:=re.match(r'\\newcommand\{\\(\w+)\}\{(.*)\}$',line))}
    assert macros['CurrentMeanWidth']==f"{widths['fixed']:.5f}"
    for city in ['Zurich','Oslo','Singapore']:
        row=frame(R/'results/task4_v197_preferences/mc_city_summary.csv');row=row[(row.concentration==100)&(row.profile=='baseline')&(row.city==city)].iloc[0]
        assert f'{100*row.minimax_recommendation_frequency:.2f}' in macros['SummaryWeightMC']
    for text in ['2.0269','2.1779']:assert text in macros['MonteCarloInterpretation']
    for k,v in [('MCBaseMeans','2064'),('MCSettings','37'),('MCCertifiedPairs','4265'),('MCUnresolvedPairs','175'),('MCUniqueMinSettings','24')]:assert macros[k].strip()==v,(k,macros[k])
    manifest=read(A/'manifest.json')
    for group,base in [('source_sha256',R),('paper_input_sha256',P),('output_sha256',P)]:
        for name,digest in manifest.get(group,{}).items():assert sha(base/name)==digest,(group,name)
    pref=frame(R/'results/task4_v197_preferences/mc_city_summary.csv');k=pref[pref.concentration.eq(100)]
    pt=(A/'preferences.tex').read_text()
    for profile,label in [('baseline','Baseline'),('education_priority','Education priority'),('independent_living_priority','Independent living')]:
        cells=[f"{100*float(k[k.profile.eq(profile)&k.city.eq(city)].iloc[0].minimax_recommendation_frequency):.2f}" for city in ['Zurich','Oslo','Singapore']]
        assert label+' & '+' & '.join(cells) in pt
    future=read(R/'results/task4_v197_future/summary.json');thresholds={x['city']:x for x in future['thresholds'] if x['weight_reference']=='fixed'}
    for city in ['Oslo','Singapore','Stockholm']:assert f"{100*thresholds[city]['required_cost_reduction_fraction']:.3f}" in macros['FutureThresholds']
    assert f"{100*thresholds['Berlin']['required_cost_reduction_fraction']:.3f}" in macros['EvidenceThresholdCheck']
    mc=frame(R/'results/task4_v197_future/future_mc_city_summary.csv')
    for arm,macro in [('conditional','FutureMonteCarlo'),('withdraw_historical_stage_proxy','ProxyWithdrawalMC')]:
        for scenario in ['resource_expansion','living_pressure','balanced_improvement']:
            row=mc[mc.weight_reference.eq('fixed')&mc.city.eq('Zurich')&mc.evidence_arm.eq(arm)&mc.scenario.eq(scenario)].iloc[0]
            assert f'{100*row.recommendation_frequency:.2f}' in macros[macro]
    vintage=read(R/'results/task4_v197_diagnostics/summary.json')['vintage_cases'];vintage={(x['scenario'],x['weight_reference']):x for x in vintage};vt=(A/'vintage_table.tex').read_text()
    for sc,label in [('baseline','Retained input'),('pre2020_points','Before 2020'),('after2025_points','After 2025'),('non_ok_points','Non-ok flags'),('union_points','Union')]:
        assert f"{label} & {vintage[sc,'fixed']['withdrawn_point_cells']} & {'/'.join(vintage[sc,'fixed']['minimax_choices'])} & {'/'.join(vintage[sc,'equal']['minimax_choices'])} & {vintage[sc,'fixed']['mean_interval_width']:.2f}" in vt
    return fonts
def check_content():
    sources=graph(D/'task4_v198_paper.tex');text='\n'.join(p.read_text() for p in sorted(sources));n=norm(text)
    assert 'tcn=18213' in (D/'task4_v198_paper.tex').read_text()
    for x in ['112 points, 37 partial intervals and 11 fully unknown','2.0269','2.1779','13.01105','63.44548','54.05','counterexample','326 selected','1,865','74 saved root','14:31:18.850 UTC']:
        assert x in n,x
    core=norm((D/'task4_v198_core.tex').read_text());v=norm((D/'task4_v198_vintage.tex').read_text());m=(D/'task4_v198_generated.tex').read_text()
    fixed=frame(R/'results/task4_user_v197_revision/current_ranks.csv');fixed=fixed[fixed.weight_reference.eq('fixed')].set_index('city')
    for city in ['Zurich','Oslo']:
        assert f"{fixed.loc[city,'score_lower']:.5f}" in core and f"{fixed.loc[city,'max_regret']:.5f}" in core,(city,'baseline arithmetic')
    assert 'evidence for twenty-five distinct city--indicator cells' in core
    for x in ['twelve Zurich venues','five distinct school pools','women/girls-only','school holidays','non-school days','adult-only','expected mean-rank order unresolved']:assert x in core,x
    for x in ['Below each boundary','at it Oslo can tie','above it a counterexample exists','not measured errors or future probabilities']:assert x in v,x
    assert not any(x in n for x in ['7.14733','51.42357','46.59','twenty-six admitted supplements'])
    assert (D/'task4_v198_ai.tex').read_text()==(D/'task4_v193_ai.tex').read_text().replace('V192','V197')
    old=(D/'task4_v196_references.tex').read_text();new=(D/'task4_v198_references.tex').read_text()
    oldpart=old.split('\\bibitem{zurichpool}',1)[1].split('\\bibitem{milanpool2025}',1)[0]
    newpart=new.split('\\bibitem{zurichpool}',1)[1].split('\\bibitem{milanpool2025}',1)[0]
    assert old.replace(oldpart,newpart)==new and 'updated 9 September 2025' in new
    assert set(re.findall(r'\\bibitem\{([^}]+)\}',old))==set(re.findall(r'\\bibitem\{([^}]+)\}',new))
    return sources,text
def check_pdf(sources,combined):
    pdf=D/'task4_v198_paper.pdf';proxy=Path('/data/scratch/himcm_v198_proxy/task4_v198_review_entry.pdf');build=Path('/data/scratch/himcm_v198_build')
    def pdftext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True).split('\f')[:-1]
    pages=pdftext(pdf);assert pages==pdftext(proxy) and len(pages)==27
    aux=(build/'task4_v198_paper.aux').read_text()
    def label(name):return int(re.search(r'\\newlabel\{'+re.escape(name)+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
    assert label('main-end')==25 and label('LastPage')==27
    refs=set(re.findall(r'\\bibcite\{([^}]+)\}',aux)); old=set(re.findall(r'\\bibcite\{([^}]+)\}',Path('/data/scratch/himcm_v196_build/task4_v196_paper.aux').read_text()))
    assert refs==old and len(refs)==56
    cited={k.strip() for g in re.findall(r'\\cite\{([^}]+)\}',combined) for k in g.split(',')};assert cited<=refs,cited-refs
    nodes=ET.fromstring(subprocess.check_output(['pdftotext','-bbox',str(pdf),'-'])).findall('.//{*}page');assert len(nodes)==27
    for i,node in enumerate(nodes):
        assert (float(node.get('width')),float(node.get('height')))==(612,792)
        words=node.findall('.//{*}word');assert not any(float(w.get('yMin'))>745 for w in words),('footer',i+1)
        if i:
            top=[w for w in words if float(w.get('yMin'))<65]
            assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top) and any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
            assert any(w.text=='18213' for w in top) and f'Page {i+1} of 27' in norm(pages[i])
        else:assert '18213' in pages[0]
    logs=[]
    for file in [build/'task4_v198_paper.log',Path('/data/scratch/himcm_v198_proxy/task4_v198_review_entry.log')]:
        log=file.read_text();assert not any(x in log for x in ['Overfull','undefined','LaTeX Warning']),file;logs.append(log.count('Underfull'))
    xml=Path('/data/scratch/himcm_v198_font_audit.xml');subprocess.run(['pdftohtml','-xml','-hidden','-zoom','1.0',str(pdf),str(xml)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    fontmap={};spans=[]
    for page in ET.parse(xml).getroot().findall('page'):
        for font in page.findall('fontspec'):fontmap[font.get('id')]=font.attrib
        for span in page.findall('text'):
            value=''.join(span.itertext()).strip()
            if any(x in value for x in ['13.01105','63.44548','16.01221']):spans.append((value,int(fontmap[span.get('font')]['size'])))
    assert spans and min(x[1] for x in spans)>=12,spans
    return dict(total_pages=27,main_and_references_pages=25,AI_pages=[26,27],reference_keys=56,direct_proxy_text_equal=True,empty_footers_and_running_headers=True,display_control_number='18213 provisional',underfull_counts=logs,new_numeric_prose_minimum_pt=min(x[1] for x in spans),pdf_sha256=sha(pdf))
def main():
    protection=check_protection();f,l,h,widths,pair=check_science();fonts=check_assets(f,l,h,widths);sources,combined=check_content();pdf=check_pdf(sources,combined)
    result=dict(version='V198',status='pass',scope='Independent selected numeric, content, protected-file and PDF geometry audit; not an exhaustive prose/source-quality audit, raster review, or final team acceptance.',activation_status='staged',protected_counts=protection,immutable_science_bindings=361,point_partial_unknown=[112,37,11],mean_score_interval_widths=widths,baseline_Oslo_minus_Zurich_mean_rank_bound=pair,figure_minimum_inserted_fonts=fonts,AI_window_and_counts_frozen=True,reference_changes_limited_to_Zurich=True,actual_registration_verified=False,submission_ready=False,server_compile_verified=False,**pdf,tex_source_sha256={str(p.relative_to(P)):sha(p) for p in sorted(sources)})
    O.mkdir(exist_ok=True);(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
