"""Independent staged V181 research audit; never activates registries or edits paper."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,NAMES,SPEC
from task4_user_v154_revision import revised_bounds as prior_bounds
from task4_user_v181_revision import revised_bounds,MANIFEST
from audit_task4_v180_amsterdam import independent_scores

O=ROOT/'results/task4_v181_transition'
P=ROOT.parents[2]/'HiMCM-Overleaf'
REFS={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.ones(10)/10}

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csv(p):return pd.read_csv(p,float_precision='round_trip')
def close(a,b,tol=1e-11):np.testing.assert_allclose(a,b,atol=tol,rtol=0)

def check_rows(cities,l,h,w,rows):
    saved=rows.set_index('city').loc[cities]
    for i,r in enumerate(independent_scores(l,h,w)):
        for key,value in r.items():
            if key in saved:close(saved.iloc[i][key],value)
    return len(saved)

def norms(u,w):
    # Independent explicit criterion reduction rather than production matrix product.
    z=np.asarray(u);ww=np.asarray(w)
    if z.ndim==2 and ww.ndim==2:z=z[None,:,:];ww=ww[:,None,:]
    positive=np.sqrt(np.sum(ww*z*z,axis=-1));negative=np.sqrt(np.sum(ww*(1-z)*(1-z),axis=-1))
    return 100*positive/(positive+negative)

def decisions(lower,upper,tol=1e-12,average=True):
    lower=np.atleast_2d(lower);upper=np.atleast_2d(upper)
    regrets=[];possible=[];necessary=[]
    for i in range(16):
        other=[j for j in range(16) if j!=i]
        regrets.append(np.maximum(0,upper[:,other].max(1)-lower[:,i]))
        possible.append(upper[:,i]>=lower[:,other].max(1)-tol)
        necessary.append(lower[:,i]>=upper[:,other].max(1)-tol)
    regret=np.stack(regrets,axis=1);possible=np.stack(possible,axis=1);necessary=np.stack(necessary,axis=1)
    rank=[];first=[];top3=[]
    for i in range(16):
        ahead=(regret<regret[:,i,None]-tol).sum(1)
        tied=(np.abs(regret-regret[:,i,None])<=tol).sum(1)
        rank.append(1+ahead+(tied-1)/2 if average else 1+ahead)
        first.append(np.clip((1-ahead)/tied,0,1));top3.append(np.clip((3-ahead)/tied,0,1))
    return dict(minimax_recommendation_frequency=np.array(first).mean(1),mean_decision_rank=np.array(rank).mean(1),top3_decision_frequency=np.array(top3).mean(1),possible_champion_frequency=possible.mean(0),necessary_champion_frequency=necessary.mean(0))

def check_mc(rows,expected,cities):
    saved=rows.set_index('city').loc[cities];assert len(saved)==16
    for key,values in expected.items():
        key='recommendation_frequency' if key=='minimax_recommendation_frequency' and key not in saved else key
        if key in saved:close(saved[key],values,1e-12)
    return len(saved)

def raw_map(l,h,factors,means):
    # Invert ordinary utility to raw values, scale raw values, then map back.
    factors=np.asarray(factors);a=np.broadcast_to(l,factors.shape).copy();b=np.broadcast_to(h,factors.shape).copy()
    for j,(name,benefit,anchor,_) in enumerate(SPEC):
        r=factors[...,j]
        for original,out in [(l,a),(h,b)]:
            if name=='travel':continue
            u=original[:,j];inner=(u>0)&(u<1)
            raw=anchor*u[inner]/(1-u[inner]) if benefit else anchor*(1/u[inner]-1)
            scaled=r[...,inner]*raw
            out[...,inner,j]=scaled/(anchor+scaled) if benefit else anchor/(anchor+scaled)
        if name=='travel':
            a[...,j]=np.where(r<1,l[:,j],l[:,j]**r)
            b[...,j]=np.where(r<1,h[:,j]**r,h[:,j])
            known=np.isfinite(means)
            a[...,known,j]=np.exp(-r[...,known]*means[known]/30)
    return a,b

def factors_for(shape,changes):
    f=np.ones(shape)
    for name,change in changes.items():f[...,NAMES.index(name)]=1+change
    return f

def precision_checks():
    folder=ROOT/'results/task4_v181_mc_precision';summary=read(folder/'summary.json');bands=csv(folder/'mean_bounds.csv')
    assert summary['base_means']==2064 and summary['settings']==37 and summary['familywise_alpha']==.05
    epsilon=math.sqrt(math.log(2*2064/.05)/(2*10000))
    close(summary['normalized_half_width'],epsilon,1e-16)
    sources={'preferences':('task4_v181_preferences/mc_city_summary.csv',['profile','concentration']),
             'future_shocks':('task4_v181_future/future_mc_city_summary.csv',['scenario','weight_reference','evidence_arm']),
             'weights_only':('task4_v181_future/weight_mc_city_summary.csv',['scenario','weight_reference','evidence_arm','concentration'])}
    for name,digest in summary['input_sha256'].items():assert sha(ROOT/name)==digest,name
    assert len(bands)==2064 and len(bands[['family','setting']].drop_duplicates())==37
    expected_lookup={}
    for family,(file,keys) in sources.items():
        for row in csv(ROOT/'results'/file).to_dict('records'):
            setting=json.dumps({key:str(row[key]) for key in keys},sort_keys=True)
            expected_lookup[family,setting,row['city']]=row
    groups={}
    for row in bands.itertuples():
        source=expected_lookup[row.family,row.setting,row.city]
        close(row.estimate,source[row.metric],1e-15)
        a,b=(1,16) if row.metric=='mean_decision_rank' else (0,1)
        assert row.draws==10000 and row.support_lower==a and row.support_upper==b
        close(row.half_width,(b-a)*epsilon,1e-15)
        close(row.lower,max(a,row.estimate-(b-a)*epsilon),1e-15);close(row.upper,min(b,row.estimate+(b-a)*epsilon),1e-15)
        if row.metric=='mean_decision_rank':groups[row.family,row.setting,row.city]=row
    folder=ROOT/'results/task4_v181_mean_rank_comparisons';pairs=csv(folder/'pairs.csv');settings=csv(folder/'settings.csv');report=read(folder/'summary.json')
    assert len(pairs)==4440 and len(pairs[['family','setting','city_a','city_b']].drop_duplicates())==4440
    certified=0
    for row in pairs.itertuples():
        a=groups[row.family,row.setting,row.city_a];b=groups[row.family,row.setting,row.city_b]
        low,high=a.lower-b.upper,a.upper-b.lower
        close(row.sample_mean_a,a.estimate);close(row.sample_mean_b,b.estimate);close(row.gap_a_minus_b,a.estimate-b.estimate)
        close(row.gap_lower,low);close(row.gap_upper,high)
        label='a_lower_expected_mean_rank' if high < -1e-12 else ('b_lower_expected_mean_rank' if low>1e-12 else 'unresolved')
        assert row.classification==label
        certified+=label!='unresolved'
    unique=0
    for setting in settings.itertuples():
        rows=pairs[(pairs.family==setting.family)&(pairs.setting==setting.setting)]
        assert len(rows)==120
        beaten=set(rows.loc[rows.classification=='a_lower_expected_mean_rank','city_b'])|set(rows.loc[rows.classification=='b_lower_expected_mean_rank','city_a'])
        cities={city for family,key,city in groups if family==setting.family and key==setting.setting}
        front=sorted(cities-beaten)
        assert json.loads(setting.unresolved_mean_rank_front)==front
        assert bool(setting.unique_smallest_expectation_certified)==(len(front)==1)
        unique+=len(front)==1
    assert report['certified_pairs']==certified and report['unresolved_pairs']==4440-certified
    assert report['settings_with_unique_smallest_expected_mean_rank']==unique
    return dict(base_means=2064,settings=37,familywise_alpha=.05,derived_pairs=4440,certified_pairs=certified,unresolved_pairs=4440-certified,unique_minimum_settings=unique)

def main():
    protected=read(O/'protected_files.json')
    for section,base in [('science',ROOT),('paper',P),('registries',ROOT/'design')]:
        for name,digest in protected[section].items():assert sha(base/name)==digest,name
    assert read(ROOT/'design/task4_user_current_model.json')['version']=='V154'
    assert read(ROOT/'design/task4_user_current_extensions.json')['extension_version']=='V154'
    assert read(ROOT/'design/task4_user_current_review.json')['version']=='V179'
    manifest=read(MANIFEST)
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    v180=read(ROOT/'results/task4_v180_amsterdam_candidate/verification.json')
    for name,digest in v180['audited_output_sha256'].items():assert sha(ROOT/name)==digest,name
    assert v180['status']=='pass' and v180['independently_retained_candidate_groups']==32
    assert len(manifest['source_hashes'])==14
    obs=manifest['observations'];assert len(obs)==1
    obs=obs[0];assert obs['raw_count']==32 and obs['inventory_metadata_year']==2026 and obs['population_year']==2025
    assert obs['screen_is_positional_error_bound'] is False and obs['exact_inventory_date'] is None
    f,l0,h0=prior_bounds();f1,l,h=revised_bounds();pd.testing.assert_frame_equal(f,f1,check_exact=True)
    cities=f.city.tolist();i=cities.index('Amsterdam');j=NAMES.index('public_transport_density')
    assert l.shape==h.shape==(16,10);assert np.count_nonzero(l!=l0)==1;np.testing.assert_array_equal(h,h0)
    exact=Fraction(32*100000,50*941927+32*100000);close(l[i,j],float(exact),2e-16)
    mask=np.ones((16,10),bool);mask[i,j]=False;np.testing.assert_array_equal(l[mask],l0[mask])
    assert [int((l==h).sum()),int(((l<h)&((l>0)|(h<1))).sum()),int(((l==0)&(h==1)).sum())]==[112,35,13]
    _,wl,wh=revised_bounds(False);np.testing.assert_array_equal(wl,l0);np.testing.assert_array_equal(wh,h0)
    stage_l=l.copy();stage_h=h.copy();stage_l[cities.index('Singapore'),NAMES.index('travel')]=0;stage_h[cities.index('Singapore'),NAMES.index('travel')]=1
    cases={'before_V154':(l0,h0),'after_conditional':(l,h),'withdraw_Amsterdam_mapped_inventory':(l0,h0),'withdraw_historical_stage_proxy':(stage_l,stage_h)}
    primary=ROOT/'results/task4_user_v181_revision';ranks=csv(primary/'all_ranks.csv');mc=csv(primary/'mc_city_summary.csv');city_cases=0;mc_rows=0
    assert set(ranks.scenario)==set(cases)
    for case,(a,b) in cases.items():
        for ref,w in REFS.items():city_cases+=check_rows(cities,a,b,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    for ref,w in REFS.items():
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            for case,(a,b) in cases.items():
                expected=decisions(norms(a,draws),norms(b,draws))
                mc_rows+=check_mc(mc[(mc.scenario==case)&(mc.weight_reference==ref)&(mc.concentration==concentration)],expected,cities)
    primary_summary=read(primary/'summary.json')
    assert primary_summary['admissions_sha256']==sha(MANIFEST) and primary_summary['point_cells']==112 and primary_summary['partial_cells']==35 and primary_summary['fully_missing_cells']==13
    assert primary_summary['protected_nonmissing_cells']==int(((l0>0)|(h0<1)).sum())==146
    assert primary_summary['mc_seed']==20261108 and primary_summary['mc_draws_per_setting']==10000
    for report in primary_summary['results']:
        rows=ranks[(ranks.scenario==report['scenario'])&(ranks.weight_reference==report['weight_reference'])]
        close(report['mean_width'],float((rows.score_upper-rows.score_lower).mean()))
        assert report['minimax_choices']==rows.loc[rows.decision_rank==1,'city'].tolist()
        assert report['possible_champions']==rows.loc[rows.possible_champion,'city'].tolist()
        assert report['necessary_champions']==rows.loc[rows.necessary_champion,'city'].tolist()
    before=mc[mc.scenario=='before_V154'].drop(columns='scenario').reset_index(drop=True)
    old=csv(ROOT/'results/task4_user_v154_revision/mc_city_summary.csv');old=old[old.scenario=='after_conditional'].drop(columns='scenario').reset_index(drop=True)
    pd.testing.assert_frame_equal(before,old,check_exact=True)
    p=ROOT/'results/task4_v181_preferences';pw=csv(p/'weights.csv');pr=csv(p/'ranks.csv');pm=csv(p/'mc_city_summary.csv')
    pd.testing.assert_frame_equal(pw,csv(ROOT/'results/task4_v154_preferences/weights.csv'),check_exact=True)
    assert read(p/'scenario_matrices.json')==read(ROOT/'results/task4_v154_preferences/scenario_matrices.json')
    pref_mc_rows=0
    for profile in pr.profile.unique():
        w=pw[pw.profile==profile].set_index('indicator').loc[NAMES].weight.to_numpy()
        city_cases+=check_rows(cities,l,h,w,pr[pr.profile==profile])
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            pref_mc_rows+=check_mc(pm[(pm.profile==profile)&(pm.concentration==concentration)],decisions(norms(l,draws),norms(h,draws)),cities)
    # The extension source is exactly the frozen V154 source with declared rebase substitutions.
    original=(ROOT/'scripts/task4_v154_extensions.py').read_text()
    expected=original.replace('task4_user_v154_revision','task4_user_v181_revision').replace("version='V154'","version='V181'").replace("primary='V154'","primary='V181'").replace("'V154'","'V181'").replace('results/task4_v154_','results/task4_v181_').replace('rebased to V154','rebased to V181')
    actual=(ROOT/'scripts/task4_v181_extensions.py').read_text()
    # Metadata counts can be updated separately; scientific code must stay identical.
    expected=expected.replace('uncertain_cells=48','uncertain_cells=48')
    assert actual==expected,'V181 extension differs beyond allowed rebase substitutions'
    from task4_v122_future import SCENARIOS,DRAWS,SEED,WEIGHT_SEED
    future=ROOT/'results/task4_v181_future';fr=csv(future/'ranks.csv');fb=csv(future/'utility_bounds.csv');fm=csv(future/'future_mc_city_summary.csv');wm=csv(future/'weight_mc_city_summary.csv')
    assert DRAWS==10000 and SEED==20261108122 and WEIGHT_SEED==[20261108,100]
    assert read(future/'summary.json')['scenario_definitions']==SCENARIOS
    means=f.commute_min.to_numpy(dtype=float);arms={'conditional':(l,h),'withdraw_historical_stage_proxy':(stage_l,stage_h)}
    future_mc_rows=0;future_weight_rows=0
    rng=np.random.default_rng(SEED);delta=.05*rng.uniform(0,1,(DRAWS,1))+.05*rng.uniform(0,1,(DRAWS,16))
    for arm,(base_l,base_h) in arms.items():
        for scenario,changes in SCENARIOS.items():
            factors=factors_for(l.shape,changes);a,b=raw_map(base_l,base_h,factors,means)
            saved=fb[(fb.evidence_arm==arm)&(fb.scenario==scenario)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
            close(saved.lower.to_numpy().reshape(16,10),a,3e-14);close(saved.upper.to_numpy().reshape(16,10),b,3e-14)
            for ref,w in REFS.items():
                city_cases+=check_rows(cities,a,b,w,fr[(fr.evidence_arm==arm)&(fr.scenario==scenario)&(fr.weight_reference==ref)])
                draws=np.random.default_rng(np.random.SeedSequence(WEIGHT_SEED)).dirichlet(100*w,DRAWS)
                future_weight_rows+=check_mc(wm[(wm.evidence_arm==arm)&(wm.scenario==scenario)&(wm.weight_reference==ref)],decisions(norms(a,draws),norms(b,draws),tol=1e-10,average=False),cities)
                if scenario=='baseline':continue
                factors=np.ones((DRAWS,16,10))
                for name,change in changes.items():factors[...,NAMES.index(name)]=1+np.sign(change)*delta
                aa,bb=raw_map(base_l,base_h,factors,means);low,high=norms(aa,w),norms(bb,w)
                rows=fm[(fm.evidence_arm==arm)&(fm.scenario==scenario)&(fm.weight_reference==ref)]
                future_mc_rows+=check_mc(rows,decisions(low,high,tol=1e-10,average=False),cities)
                saved=rows.set_index('city').loc[cities]
                for endpoint,values,baseline in [('lower',low,norms(base_l,w)),('upper',high,norms(base_h,w))]:
                    for suffix,q in [('05',.05),('50',.5),('95',.95)]:close(saved[f'score_{endpoint}_change_p{suffix}'],np.quantile(values-baseline,q,axis=0),1e-11)
    # Independently invert and evaluate every declared conditional threshold grid point.
    scans=csv(future/'threshold_scan.csv');thresholds=csv(future/'thresholds.csv');assert len(scans)==3232 and len(thresholds)==32
    for row in scans.itertuples():
        factors=np.ones((16,10));target=cities.index(row.city)
        factors[target,[NAMES.index(name) for name in ['upper_secondary_ptr','pm25','travel']]]=row.raw_multiplier
        aa,bb=raw_map(l,h,factors,means);values=independent_scores(aa,bb,REFS[row.weight_reference])
        regret=np.array([v['max_regret'] for v in values]);close(row.regret_gap_to_best_other,regret[target]-np.delete(regret,target).min())
    for row in thresholds.itertuples():
        if row.status!='crossing_found':continue
        for delta,sign in [(-1e-6,-1),(1e-6,1)]:
            factors=np.ones((16,10));target=cities.index(row.city)
            factors[target,[NAMES.index(name) for name in ['upper_secondary_ptr','pm25','travel']]]=row.threshold_raw_multiplier+delta
            aa,bb=raw_map(l,h,factors,means);values=independent_scores(aa,bb,REFS[row.weight_reference])
            regret=np.array([v['max_regret'] for v in values]);assert sign*(regret[target]-np.delete(regret,target).min())>1e-10
    from task4_v137_method_country import independent_method_check,CASE_FILES
    method=ROOT/'results/task4_v181_method';mr=csv(method/'method_ranks.csv');ms=read(method/'summary.json')
    for ref,w in REFS.items():independent_method_check(mr[mr.weight_reference==ref].set_index('city').loc[cities].reset_index(),next(v for v in ms['method_cases'] if v['weight_reference']==ref),l,h,w)
    for name in CASE_FILES:assert sha(method/name)==sha(ROOT/'results/task4_v154_method'/name)
    dg=ROOT/'results/task4_v181_diagnostics';dr=csv(dg/'vintage_ranks.csv');du=csv(dg/'witness_utilities.csv');dc=csv(dg/'witness_cases.csv');points=csv(ROOT/'results/task4_v143_vintage/submitted_points.csv')
    for (scenario,ref),rows in dr.groupby(['scenario','weight_reference']):
        a,b=l.copy(),h.copy()
        for point in points.itertuples():
            early,late,flag=point.submitted_year<2020,point.submitted_year>2025,point.submitted_flag!='ok'
            remove={'baseline':False,'pre2020_points':early,'after2025_points':late,'non_ok_points':flag,'union_points':early or late or flag,'withdraw_Zurich_homicide':point.city=='Zurich' and point.indicator==NAMES[0],'withdraw_Amsterdam_homicide':point.city=='Amsterdam' and point.indicator==NAMES[0]}[scenario]
            if remove:a[cities.index(point.city),NAMES.index(point.indicator)],b[cities.index(point.city),NAMES.index(point.indicator)]=0,1
        city_cases+=check_rows(cities,a,b,REFS[ref],rows)
    for target in cities:
        u=du[du.target==target].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])].utility.to_numpy().reshape(16,10)
        close(u[l==h],l[l==h]);assert np.all(u[l<h]>l[l<h]) and np.all(u[l<h]<h[l<h])
        for ref,w in REFS.items():
            scores=norms(u,w);k=cities.index(target);margin=scores[k]-np.delete(scores,k).max();assert margin>0
            close(dc[(dc.target==target)&(dc.weight_reference==ref)].iloc[0].strict_margin,margin)
    for section,base in [('science',ROOT),('paper',P),('registries',ROOT/'design')]:
        for name,digest in protected[section].items():assert sha(base/name)==digest,name
    precision=precision_checks()
    result=dict(precision_and_mean_rank_audit=precision,independent_future_threshold_scan_points=3232,threshold_crossing_sides_verified=True,version='V181 staged research',status='pass',activation_status='staged_not_active',current_primary='V154',current_paper='V179',one_lower_changed=True,other159_cells_and_all160_uppers_exact=True,withdrawal_exact_V154=True,exact_candidate_utility=str(exact),point_partial_unknown=[112,35,13],cumulative_supplements=23,independent_scalar_city_cases=city_cases,independent_primary_MC_rows=mc_rows,independent_preference_MC_rows=pref_mc_rows,independent_future_shock_MC_rows=future_mc_rows,independent_future_weight_MC_rows=future_weight_rows,draws_per_setting=10000,paired_seeds_profiles_and_scenarios_preserved=True,historical_csvs_byte_identical=len(CASE_FILES),interior_witness_weight_cases=32,scientific_files_unchanged=len(protected['science']),existing_paper_files_unchanged=len(protected['paper']),registries_unchanged=len(protected['registries']),manuscript_changed=False,independent_raw_future_transform=True,future_shock_quantiles_verified=True,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [MANIFEST,Path(__file__),ROOT/'scripts/task4_user_v181_revision.py',ROOT/'scripts/task4_v181_extensions.py',ROOT/'scripts/task4_v181_mc_precision.py',ROOT/'scripts/task4_v181_mean_rank_comparisons.py']},result_sha256={str(p.relative_to(ROOT)):sha(p) for folder in [primary,ROOT/'results/task4_v181_preferences',future,method,dg,ROOT/'results/task4_v181_mc_precision',ROOT/'results/task4_v181_mean_rank_comparisons'] for p in sorted(folder.iterdir()) if p.is_file()})
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['source_sha256','result_sha256']},indent=2))

if __name__=='__main__':main()
