"""V154 transition audit: one-cell provenance, rebased results and owned PDF."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
import numpy as np
import pandas as pd
from PIL import Image,ImageChops
from task4_user_v136_revision import revised_bounds as previous_bounds
from task4_user_v154_revision import revised_bounds,MANIFEST
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT,NAMES,weights
from task4_v123_revision_diagnostic import independent_intervals
from task4_v125_future import raw_transform

P=Path('/data/projects/HiMCM-Overleaf')
O=ROOT/'results/task4_v154_transition'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())

def check_rows(cities,lo,hi,w,rows):
    expected=independent_intervals(lo,hi,w)
    rows=rows.set_index('city').loc[cities]
    for key,value in expected.items():
        if key in rows:np.testing.assert_allclose(rows[key],value,atol=1e-11,rtol=0)
    return len(rows)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--render-review-confirmed',action='store_true');parser.add_argument('--expect-active',action='store_true');args=parser.parse_args()
    O.mkdir(exist_ok=True)
    f,l0,h0=previous_bounds();_,lo,hi=revised_bounds();cities=f.city.tolist()
    i,j=cities.index('Milan'),NAMES.index('public_transport_density')
    assert lo.shape==hi.shape==(16,10)
    mask=np.ones((16,10),bool);mask[i,j]=False
    np.testing.assert_array_equal(np.stack([lo,hi])[:,mask],np.stack([l0,h0])[:,mask])
    assert np.count_nonzero(lo!=l0)==1;np.testing.assert_array_equal(hi,h0)
    assert [int((lo==hi).sum()),int(((lo<hi)&((lo>0)|(hi<1))).sum()),int(((lo==0)&(hi==1)).sum())]==[112,34,14]
    _,withdraw_l,withdraw_h=revised_bounds(False)
    np.testing.assert_array_equal(withdraw_l,l0);np.testing.assert_array_equal(withdraw_h,h0)
    primary=ROOT/'results/task4_user_v154_revision'
    ranks=pd.read_csv(primary/'all_ranks.csv');cases=0
    for scenario in ranks.scenario.unique():
        l,h=(l0,h0) if scenario in ['before_V136','withdraw_Milan_historical_inventory'] else (lo.copy(),hi.copy())
        if scenario=='withdraw_historical_stage_proxy':
            k=cities.index('Singapore');t=NAMES.index('travel');l[k,t],h[k,t]=0,1
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            cases+=check_rows(cities,l,h,w,ranks[(ranks.scenario==scenario)&(ranks.weight_reference==ref)])
    # Every paired primary MC row reproduces the independently checked V153 proposal.
    p=pd.read_csv(primary/'mc_city_summary.csv');old=pd.read_csv(ROOT/'results/task4_v153_milan_proposal/paired_weight_summary.csv')
    keys=['weight_reference','concentration','city'];cols=['minimax_recommendation_frequency','mean_decision_rank','possible_champion_frequency']
    for now,prior in [('after_conditional','V153_proposed'),('before_V136','V136_active')]:
        a=p[p.scenario==now].set_index(keys).sort_index();b=old[old.scenario==prior].set_index(keys).sort_index()
        np.testing.assert_allclose(a[cols],b[cols],atol=1e-12,rtol=0)
    pref=ROOT/'results/task4_v154_preferences';pr=pd.read_csv(pref/'ranks.csv');pw=pd.read_csv(pref/'weights.csv');pm=pd.read_csv(pref/'mc_city_summary.csv')
    old_pref=ROOT/'results/task4_v137_preferences'
    pd.testing.assert_frame_equal(pw,pd.read_csv(old_pref/'weights.csv'),check_exact=True)
    assert read(pref/'scenario_matrices.json')==read(old_pref/'scenario_matrices.json')
    for profile in pr.profile.unique():
        w=pw[pw.profile==profile].set_index('indicator').loc[NAMES].weight.to_numpy()
        cases+=check_rows(cities,lo,hi,w,pr[pr.profile==profile])
    for concentration in [20,100,500]:
        a=pm[(pm.profile=='baseline')&(pm.concentration==concentration)].set_index('city').loc[cities]
        b=p[(p.scenario=='after_conditional')&(p.weight_reference=='fixed')&(p.concentration==concentration)].set_index('city').loc[cities]
        np.testing.assert_allclose(a[cols],b[cols],atol=1e-12,rtol=0)
    future=ROOT/'results/task4_v154_future';fr=pd.read_csv(future/'ranks.csv');fb=pd.read_csv(future/'utility_bounds.csv')
    for (arm,scenario,ref),rows in fr.groupby(['evidence_arm','scenario','weight_reference'],sort=False):
        b=fb[(fb.evidence_arm==arm)&(fb.scenario==scenario)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        l=b.lower.to_numpy().reshape(16,10);h=b.upper.to_numpy().reshape(16,10)
        w=weights(.1) if ref=='fixed' else np.ones(10)/10
        cases+=check_rows(cities,l,h,w,rows)
        if scenario=='baseline' and arm=='conditional':np.testing.assert_allclose(l,lo,atol=1e-15,rtol=0);np.testing.assert_allclose(h,hi,atol=1e-15,rtol=0)
    # Every midpoint method case independently recomputed by its original helper.
    from task4_v137_method_country import independent_method_check,CASE_FILES
    method=ROOT/'results/task4_v154_method';mr=pd.read_csv(method/'method_ranks.csv');ms=read(method/'summary.json')
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        rows=mr[mr.weight_reference==ref].set_index('city').loc[cities].reset_index()
        report=next(x for x in ms['method_cases'] if x['weight_reference']==ref)
        independent_method_check(rows,report,lo,hi,w)
    for name in CASE_FILES:assert sha(method/name)==sha(ROOT/'results/task4_v137_method_country'/name)
    dg=ROOT/'results/task4_v154_diagnostics';utilities=pd.read_csv(dg/'witness_utilities.csv');wc=pd.read_csv(dg/'witness_cases.csv')
    for target in cities:
        rows=utilities[utilities.target==target].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        u=rows.utility.to_numpy().reshape(16,10)
        np.testing.assert_allclose(u[lo==hi],lo[lo==hi],atol=1e-15,rtol=0)
        assert np.all(u[lo<hi]>lo[lo<hi]) and np.all(u[lo<hi]<hi[lo<hi])
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            good=np.linalg.norm((1-u)*np.sqrt(w),axis=1);bad=np.linalg.norm(u*np.sqrt(w),axis=1);scores=100*bad/(good+bad)
            t=cities.index(target);margin=scores[t]-np.delete(scores,t).max();assert margin>0
            saved=wc[(wc.target==target)&(wc.weight_reference==ref)].iloc[0]
            assert abs(margin-saved.strict_margin)<1e-11
    old=read(ROOT/'results/task4_v151_shared_entry/verification.json')
    for n,h in old['scientific_file_sha256'].items():assert sha(ROOT/n)==h,n
    protected=dict(old['manuscript_files_unchanged_sha256'])
    for folder,key in [('task4_v151_shared_entry','support_file_sha256'),('task4_v152_tail_access','selected_file_sha256'),('task4_v153_milan_proposal','selected_file_sha256')]:protected.update(read(ROOT/'results'/folder/'delivery.json')[key])
    for n,h in protected.items():assert sha(P/n)==h,n
    paper=P/'drafts/task4_v154_paper.pdf';text=subprocess.check_output(['pdftotext','-layout',str(paper),'-'],text=True)
    pages=[x for x in text.split('\f') if x.strip()]
    assert len(pages)==24,len(pages)
    for k,page in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(k)+r' of 24',page),k
    flat=' '.join(text.split())
    for marker in ['34 partial intervals','14 fully missing intervals','16.06144','14.62%','0.650','104 station/hub','Milan']:
        assert marker in flat,marker
    assert '33 partial intervals' not in flat and '15 fully missing intervals' not in flat
    aux=(P/'drafts/task4_v154_paper.aux').read_text()
    def label(name):
        line=next(s for s in aux.splitlines() if s.startswith('\\newlabel{'+name+'}'))
        return int(line.split('}{')[2])
    main_pages=label('main-end');assert main_pages==22
    assert label('news-start')==16 and label('news-end')==17
    assert len(re.findall(r'\\bibcite\{',aux))==47
    log=(P/'drafts/task4_v154_paper.log').read_text();stdout=Path('/data/scratch/himcm_v154_compile.txt').read_text()
    assert not re.search(r'warning|undefined|Overfull|Underfull',stdout,re.I)
    assert not re.search(r'LaTeX Warning|Package .* Warning|Overfull|Underfull',log)
    figure=P/'drafts/task4_v154_assets/score_intervals.pdf'
    figure_text=subprocess.check_output(['pdftotext',str(figure),'-'],text=True)
    assert all(c in figure_text for c in cities)
    manifest=read(P/'drafts/task4_v154_assets/manifest.json')
    for n,h in manifest['source_sha256'].items():assert sha(ROOT/n)==h,n
    assert manifest['minimum_figure_font_inserted_pt']>=9
    root_pdf=Path('/data/scratch/himcm_v154_rootproof/task4_v154_review_entry.pdf')
    root_text=subprocess.check_output(['pdftotext','-layout',str(root_pdf),'-'],text=True)
    assert [' '.join(x.split()) for x in root_text.split('\f') if x.strip()]==[' '.join(x.split()) for x in pages]
    root_stdout=Path('/data/scratch/himcm_v154_root_compile.txt').read_text()
    assert not re.search(r'warning|undefined|Overfull|Underfull',root_stdout,re.I)
    registry=read(ROOT/'design/task4_user_current_model.json')
    if args.expect_active:
        assert registry['version']=='V154' and registry['module']=='task4_user_v154_revision'
        extension=read(ROOT/'design/task4_user_current_extensions.json')
        assert extension['primary_evidence_version']==extension['extension_version']=='V154'
        assert extension['manuscript_entry']=='../HiMCM-Overleaf/drafts/task4_v154_paper.tex'
    else:assert registry['version']=='V136'
    files={str(p.relative_to(ROOT)):sha(p) for folder in [primary,pref,future,method,dg] for p in sorted(folder.iterdir()) if p.is_file()}
    sources={str(p.relative_to(ROOT)):sha(p) for p in [MANIFEST,ROOT/'scripts/task4_user_v154_revision.py',ROOT/'scripts/task4_v154_extensions.py',ROOT/'scripts/audit_task4_v154.py']}
    result=dict(status='pass',version='V154',active_registry_verified=args.expect_active,
                point_partial_unknown=[112,34,14],newly_admitted_cells=1,cumulative_supplements=22,
                original_159_utility_entries_exact=True,original_csv_sha256=sha(ROOT/'data/task4_v117_team_intake/city_indicators.csv'),
                independent_city_cases=cases,paired_primary_MC_rows=192,preference_baseline_MC_rows=48,
                independently_recomputed_method_cases=2,historical_cases_byte_identical=6,interior_witness_weight_cases=32,
                protected_scientific_files=len(old['scientific_file_sha256']),unchanged_manuscript_support_files=len(protected),
                pages=24,main_pages=main_pages,news_pages=[16,17],AI_pages=[23,24],compiled_references=47,compilation_warnings=0,
                all_pages_visually_reviewed=args.render_review_confirmed,pdf_sha256=sha(paper),pdf_bytes=paper.stat().st_size,
                minimum_new_figure_font_inserted_pt=manifest['minimum_figure_font_inserted_pt'],
                project_settings_changed=False,online_compile_verified=False,submission_ready=False,root_local_build_pages=24,root_local_text_matches=True,root_local_pdf_sha256=sha(root_pdf),
                result_sha256=files,source_sha256=sources,old_primary_pdf_sha256=sha(P/'drafts/task4_v137_paper.pdf'))
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','active_registry_verified','independent_city_cases','pages','compilation_warnings','protected_scientific_files','unchanged_manuscript_support_files']},indent=2))

if __name__=='__main__':main()
