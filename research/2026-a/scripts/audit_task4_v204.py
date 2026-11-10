"""Independent scientific audit of staged V204; default is read-only stdout."""
from pathlib import Path
from fractions import Fraction
from itertools import product
import json,math,hashlib
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,NAMES,SPEC
from task4_user_v203_revision import revised_bounds as prior_bounds
from task4_user_v204_revision import revised_bounds,MANIFEST
from audit_task4_v203 import read,sha,csv,close,check_rows,norms,decisions,check_mc,raw_map,factors_for,REFS,independent_scores
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_audit_output import audit_parser,check_output,emit_report
O=ROOT/'results/task4_v204_transition'; G=ROOT.parents[1]

def precision_checks():
    folder=ROOT/'results/task4_user_v204_extensions/mc_precision';summary=read(folder/'summary.json');bands=csv(folder/'mean_bounds.csv')
    m=len(bands);group_count=len(bands[['family','setting']].drop_duplicates())
    assert summary['base_means']==m and summary['settings']==group_count and summary['familywise_alpha']==.05
    epsilon=math.sqrt(math.log(2*m/.05)/(2*10000))
    close(summary['normalized_half_width'],epsilon,1e-16)
    sources={'preferences':('task4_user_v204_extensions/preferences/mc_city_summary.csv',['profile','concentration']),
             'future_shocks':('task4_user_v204_extensions/future/future_mc_city_summary.csv',['scenario','weight_reference','evidence_arm']),
             'weights_only':('task4_user_v204_extensions/future/weight_mc_city_summary.csv',['scenario','weight_reference','evidence_arm','concentration'])}
    for name,digest in summary['input_sha256'].items():assert sha(ROOT/name)==digest,name
    assert m>0 and group_count>0
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
    folder=ROOT/'results/task4_user_v204_extensions/mean_rank_comparisons';pairs=csv(folder/'pairs.csv');settings=csv(folder/'settings.csv');report=read(folder/'summary.json')
    from collections import Counter
    family_sizes=Counter((family,key) for family,key,city in groups)
    pair_count=sum(n*(n-1)//2 for n in family_sizes.values())
    assert len(pairs)==pair_count and len(pairs[['family','setting','city_a','city_b']].drop_duplicates())==pair_count
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
    assert report['certified_pairs']==certified and report['unresolved_pairs']==pair_count-certified
    assert report['settings_with_unique_smallest_expected_mean_rank']==unique
    return dict(base_means=m,settings=group_count,familywise_alpha=.05,derived_pairs=pair_count,certified_pairs=certified,unresolved_pairs=pair_count-certified,unique_minimum_settings=unique)



def main():
    args=audit_parser(__doc__).parse_args(); canonical=O/'verification.json';check_output(args,canonical,G)
    protection=protected_inputs();old_current=read(ROOT/'results/current_paper_review/current_verification.json')
    for name,digest in old_current['edition_source_sha256'].items():assert sha(ROOT/name)==digest,name
    edition_count=len(old_current['edition_source_sha256']);assert edition_count==24
    navigation=[ROOT/'design/task4_user_current_review.json',ROOT/'design/task4_user_current_extensions.json',ROOT/'design/task4_user_current_delivery.json']
    nav={str(p.relative_to(ROOT)):sha(p) for p in navigation}
    manifest=read(MANIFEST);assert manifest['version']=='V204' and manifest['activation_status']=='staged_not_active'
    assert len(manifest['source_hashes'])==68
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    obs=manifest['observations'][0];assert obs['raw_count']==378 and obs['raw_count_before']==99 and obs['population']==2028399 and obs['anchor']==50 and obs['service_day']=='20261110'
    assert obs['public_passenger_nature_supported'] and obs['source_defined_scheduled_supply_supported'] and not obs['trip_level_PDF_conditions_verified'] and not obs['actual_operation_verified'] and obs['counts_not_added']
    witness=csv(ROOT/'results/current_vienna_gtfs_candidate/station_witnesses.csv');witness.DIVA=witness.DIVA.astype(str)
    assert len(witness)==witness.DIVA.nunique()==378 and set(witness.DIVA)==set(obs['native_root_ids'])
    routes=set(manifest['condition_routes']);assert routes=={'41A','43A','56A','58A','73A','74A','86A','89A','92A'}
    for route in routes:assert set(witness.loc[witness.route_short_name==route,'DIVA'])==set(manifest['condition_route_DIVA_ids'][route])
    selected=set(witness.loc[witness.route_short_name.isin(routes),'DIVA']);assert len(selected)==36 and selected==set(manifest['condition_selected_DIVA_ids'])
    qual=read(ROOT/manifest['qualification_verification']);assert sha(ROOT/manifest['qualification_verification'])==manifest['qualification_verification_sha256'] and qual['witness_routes_matched']==88 and qual['public_passenger_nature_supported'] and not qual['actual_operation_verified'] and not qual['trip_level_PDF_conditions_verified']
    f,l0,h0=prior_bounds(); f1,l,h=revised_bounds();pd.testing.assert_frame_equal(f,f1,check_exact=True)
    cities=f.city.tolist();z=cities.index('Vienna');j=NAMES.index('public_transport_density');mask=np.ones(l.shape,bool);mask[z,j]=False
    np.testing.assert_array_equal(l[mask],l0[mask]);np.testing.assert_array_equal(h,h0);assert np.count_nonzero(l!=l0)==1
    def value(n):return float(Fraction(n*100000,2028399*50+n*100000))
    close(l0[z,j],value(99),2e-16);close(l[z,j],value(378),2e-16)
    # Exhaustive former basic withdrawal switches, comparing actual off to V203.
    for flags in product([False,True],repeat=5):
        kw=dict(zip(["include_oslo_bus","include_sportshub","include_sg_pool","include_zurich_pool","include_tokyo"],flags));old=prior_bounds(**kw);new=revised_bounds(include_vienna_bus=False,**kw)
        pd.testing.assert_frame_equal(old[0],new[0],check_exact=True);np.testing.assert_array_equal(old[1],new[1]);np.testing.assert_array_equal(old[2],new[2])
    oldbounds=csv(ROOT/'results/task4_user_v203_revision/utility_bounds.csv')
    def oldcase(case):
        v=oldbounds[oldbounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        return v.lower.to_numpy().reshape(16,10),v.upper.to_numpy().reshape(16,10)
    cases={}
    for name in oldbounds.scenario.unique():
        a,b=oldcase(name);a=a.copy();b=b.copy()
        if name=='before_V202':continue
        if name!='after_conditional':a[z,j]=value(378)
        else:a=l.copy();b=h.copy()
        cases[name]=(a,b)
    cases['before_V203']=(l0,h0);cases['withdraw_Vienna_bus_refinement']=(l0,h0)
    a=l.copy();a[z,j]=value(342);cases['conservative_withhold_selected_nine_route_witnesses']=(a,h)
    for route in routes:
        a=l.copy();a[z,j]=value(378-int(witness.route_short_name.eq(route).sum()));cases[f'conservative_withhold_selected_{route}_witnesses']=(a,h)
    assert len(cases)==29
    stage_l,stage_h=cases['withdraw_historical_stage_proxy']
    primary=ROOT/'results/task4_user_v204_revision';ranks=csv(primary/'all_ranks.csv');mc=csv(primary/'mc_city_summary.csv');bounds=csv(primary/'utility_bounds.csv');city_cases=0;mc_rows=0
    assert set(ranks.scenario)==set(cases) and len(ranks)==928 and len(bounds)==4640 and len(mc)==2784
    for case,(a,b) in cases.items():
        saved=bounds[bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(saved.lower.to_numpy().reshape(16,10),a,1e-15);close(saved.upper.to_numpy().reshape(16,10),b,1e-15)
        for ref,w in REFS.items():city_cases+=check_rows(cities,a,b,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    for ref,w in REFS.items():
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            for case,(a,b) in cases.items():mc_rows+=check_mc(mc[(mc.scenario==case)&(mc.weight_reference==ref)&(mc.concentration==concentration)],decisions(norms(a,draws),norms(b,draws)),cities)
    primary_summary=read(primary/'summary.json');assert primary_summary['primary_mc_settings']==174 and primary_summary['mc_seed']==20261108 and primary_summary['mc_draws_per_setting']==10000 and primary_summary['activation_status']=='staged_not_active'
    for report in primary_summary['results']:
        rows=ranks[(ranks.scenario==report['scenario'])&(ranks.weight_reference==report['weight_reference'])]
        close(report['mean_width'],float((rows.score_upper-rows.score_lower).mean()))
        assert report['minimax_choices']==rows.loc[rows.decision_rank==1,'city'].tolist()
        assert report['possible_champions']==rows.loc[rows.possible_champion,'city'].tolist()
        assert report['necessary_champions']==rows.loc[rows.necessary_champion,'city'].tolist()
    print('Primary: 29 bound cases and 174 MC settings passed',flush=True)
    extension_structure_tables=0
    for part in ['preferences','future','method','diagnostics']:
        old_folder=ROOT/('results/task4_v203_'+part);new_folder=ROOT/('results/task4_user_v204_extensions/'+part)
        assert {p.name for p in old_folder.glob('*.csv')}=={p.name for p in new_folder.glob('*.csv')}
        for path in new_folder.glob('*.csv'):
            old_table=csv(old_folder/path.name);new_table=csv(path)
            assert list(old_table.columns)==list(new_table.columns) and old_table.shape==new_table.shape
            for column in ['city','indicator','profile','scenario','weight_reference','evidence_arm','concentration','target']:
                if column in old_table:
                    pd.testing.assert_series_equal(old_table[column],new_table[column],check_exact=True)
            extension_structure_tables+=1
    p=ROOT/'results/task4_user_v204_extensions/preferences';pw=csv(p/'weights.csv');pr=csv(p/'ranks.csv');pm=csv(p/'mc_city_summary.csv')
    pd.testing.assert_frame_equal(pw,csv(ROOT/'results/task4_v203_preferences/weights.csv'),check_exact=True)
    diagnostic_changes=[]
    def compare_matrices(a,b,path=()):
        if isinstance(a,dict):
            assert isinstance(b,dict) and a.keys()==b.keys()
            for key in a:compare_matrices(a[key],b[key],path+(key,))
        elif isinstance(a,list):
            assert isinstance(b,list) and len(a)==len(b)
            for i,(x,y) in enumerate(zip(a,b)):compare_matrices(x,y,path+(i,))
        elif path[:2]==('independent_living_priority','diagnostic') and len(path)==3 and path[2] in {'lambda_max','CI','CR'}:
            assert isinstance(a,(int,float)) and isinstance(b,(int,float))
            close(a,b,1e-12);diagnostic_changes.append(abs(a-b))
        else:assert type(a)==type(b) and a==b,path
    compare_matrices(read(p/'scenario_matrices.json'),read(ROOT/'results/task4_v203_preferences/scenario_matrices.json'))
    assert len(diagnostic_changes)==3
    pref_mc_rows=0
    for profile in pr.profile.unique():
        w=pw[pw.profile==profile].set_index('indicator').loc[NAMES].weight.to_numpy()
        city_cases+=check_rows(cities,l,h,w,pr[pr.profile==profile])
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            pref_mc_rows+=check_mc(pm[(pm.profile==profile)&(pm.concentration==concentration)],decisions(norms(l,draws),norms(h,draws)),cities)
    from task4_v122_future import SCENARIOS,DRAWS,SEED,WEIGHT_SEED
    future=ROOT/'results/task4_user_v204_extensions/future';fr=csv(future/'ranks.csv');fb=csv(future/'utility_bounds.csv');fm=csv(future/'future_mc_city_summary.csv');wm=csv(future/'weight_mc_city_summary.csv')
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
        bracket=json.loads(row.threshold_bracket);assert bracket[0]-2e-15<=row.threshold_raw_multiplier<=bracket[1]+2e-15
        for delta,sign in [(-1e-6,-1),(1e-6,1)]:
            factors=np.ones((16,10));target=cities.index(row.city)
            factors[target,[NAMES.index(name) for name in ['upper_secondary_ptr','pm25','travel']]]=row.threshold_raw_multiplier+delta
            aa,bb=raw_map(l,h,factors,means);values=independent_scores(aa,bb,REFS[row.weight_reference])
            regret=np.array([v['max_regret'] for v in values]);assert sign*(regret[target]-np.delete(regret,target).min())>1e-10
    from task4_v137_method_country import independent_method_check,CASE_FILES
    method=ROOT/'results/task4_user_v204_extensions/method';mr=csv(method/'method_ranks.csv');ms=read(method/'summary.json')
    for ref,w in REFS.items():independent_method_check(mr[mr.weight_reference==ref].set_index('city').loc[cities].reset_index(),next(v for v in ms['method_cases'] if v['weight_reference']==ref),l,h,w)
    for name in CASE_FILES:assert sha(method/name)==sha(ROOT/'results/task4_v203_method'/name)
    dg=ROOT/'results/task4_user_v204_extensions/diagnostics';dr=csv(dg/'vintage_ranks.csv');du=csv(dg/'witness_utilities.csv');dc=csv(dg/'witness_cases.csv');points=csv(ROOT/'results/task4_v143_vintage/submitted_points.csv')
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
    from scipy.optimize import brentq
    homicide_checks=[];zurich=cities.index('Zurich')
    for record in read(dg/'summary.json')['hypothetical_rate_thresholds']:
        w=REFS[record['weight_reference']]
        def homicide_gap(rate):
            a,b=l.copy(),h.copy();a[zurich,0]=b[zurich,0]=2/(2+rate)
            rr=np.array([x['max_regret'] for x in independent_scores(a,b,w)])
            return rr[zurich]-np.delete(rr,zurich).min()
        left,right=homicide_gap(0),homicide_gap(5);close(record['endpoint_gaps'],[left,right]);assert left<=right
        if left<0<right:
            value=brentq(homicide_gap,0,5,xtol=1e-14);assert record['status']=='crossing_found';close(value,record['rate_per100000'],1e-12)
        else:assert record['status']=='no_crossing_in_interval' and record['rate_per100000'] is None
        homicide_checks.append({'reference':record['weight_reference'],'status':record['status'],'endpoint_gaps':[left,right]})

    protection_after=protected_inputs();assert protection_after==protection
    assert nav=={str(p.relative_to(ROOT)):sha(p) for p in navigation}
    for name,digest in old_current['edition_source_sha256'].items():assert sha(ROOT/name)==digest,name
    precision=precision_checks();assert precision['base_means']==2064 and precision['derived_pairs']==4440
    folders=[primary,ROOT/'results/task4_user_v204_extensions']
    files=[p for folder in folders for p in folder.rglob('*') if p.is_file()]
    files += [MANIFEST,Path(__file__),ROOT/'scripts/task4_user_v204_revision.py',ROOT/'scripts/task4_v204_extensions.py']
    files += [ROOT/name for name in manifest['source_hashes']]
    source_map={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(files))}
    snapshot_path=ROOT/'design/task4_user_v204_snapshot.json'
    snapshot={'version':'V204 staged immutable science snapshot','activation_status':'staged_not_active','previous':'V203','upstream_v203_snapshot_sha256':sha(ROOT/'design/task4_user_v203_snapshot.json'),'upstream_bindings':548,'upstream_source_sha256':read(ROOT/'design/task4_user_v203_snapshot.json')['source_sha256'],'source_sha256':source_map,'scope':'Staged source-defined scheduled public facility supply; no observed operation or universal access claim.'}
    if args.output is not None:
        if snapshot_path.exists():assert read(snapshot_path)==snapshot
        else:snapshot_path.write_text(json.dumps(snapshot,indent=2)+'\n')
    result={'version':'V204 staged research','status':'pass','activation_status':'staged_not_active','current_primary':'V203','changed_lower_cells':1,'other159_cells_and_all160_uppers_exact':True,'off_switch_exhaustive_basic_combinations':32,'independent_scalar_city_cases':city_cases,'primary_bound_cases':29,'independent_primary_MC_rows':mc_rows,'primary_MC_settings_replayed':174,'independent_preference_MC_rows':pref_mc_rows,'independent_future_shock_MC_rows':future_mc_rows,'independent_future_weight_MC_rows':future_weight_rows,'draws_per_setting':10000,'independent_future_threshold_scan_points':len(scans),'precision_and_mean_rank_audit':precision,'protected':protection,'edition_entries_checked':edition_count,'navigation_sha256':nav,'source_bindings':len(source_map),'snapshot_sha256':sha(snapshot_path) if args.output is not None else None,'public_passenger_nature_supported':True,'trip_level_PDF_conditions_verified':False,'actual_operation_verified':False,'scope':'Source-defined scheduled public facility supply. Simulation results are conditional, not observed operation or real-world win probabilities.'}
    emit_report(result,args,canonical,G)
if __name__=='__main__':main()
