"""Independent staged V203 research audit; never activates registries or edits paper."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,math,html,re
from html.parser import HTMLParser
from urllib.parse import urlparse
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,NAMES,SPEC
from task4_user_v202_revision import revised_bounds as prior_bounds
from task4_user_v203_revision import revised_bounds,MANIFEST
from audit_task4_v180_amsterdam import independent_scores

O=ROOT/'results/task4_v203_transition'
P=ROOT.parents[2]/'HiMCM-Overleaf'
REFS={'fixed':np.array([.1125]*6+[.05,.1125,.1125,.05]),'equal':np.ones(10)/10}

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csv(p):return pd.read_csv(p,float_precision='round_trip')
def close(a,b,tol=1e-11):np.testing.assert_allclose(a,b,atol=tol,rtol=0)

def check_rows(cities,l,h,w,rows,allow_near_tie_ranks=False):
    saved=rows.set_index('city').loc[cities]
    independent=independent_scores(l,h,w)
    regrets=np.array([v['max_regret'] for v in independent])
    for i,r in enumerate(independent):
        for key,value in r.items():
            if key not in saved:continue
            if allow_near_tie_ranks and key=='decision_rank':
                low=1+sum(regrets<regrets[i]-1e-12);high=sum(regrets<=regrets[i]+1e-12)
                assert low<=saved.iloc[i][key]<=high
            else:close(saved.iloc[i][key],value)
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
    folder=ROOT/'results/task4_v203_mc_precision';summary=read(folder/'summary.json');bands=csv(folder/'mean_bounds.csv')
    m=len(bands);group_count=len(bands[['family','setting']].drop_duplicates())
    assert summary['base_means']==m and summary['settings']==group_count and summary['familywise_alpha']==.05
    epsilon=math.sqrt(math.log(2*m/.05)/(2*10000))
    close(summary['normalized_half_width'],epsilon,1e-16)
    sources={'preferences':('task4_v203_preferences/mc_city_summary.csv',['profile','concentration']),
             'future_shocks':('task4_v203_future/future_mc_city_summary.csv',['scenario','weight_reference','evidence_arm']),
             'weights_only':('task4_v203_future/weight_mc_city_summary.csv',['scenario','weight_reference','evidence_arm','concentration'])}
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
    folder=ROOT/'results/task4_v203_mean_rank_comparisons';pairs=csv(folder/'pairs.csv');settings=csv(folder/'settings.csv');report=read(folder/'summary.json')
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


def source_diagnostic_checks(frame,l,h):
    from scipy.optimize import brentq
    folder=ROOT/'results/task4_v203_source_diagnostics';report=read(folder/'summary.json')
    for p,digest in report['source_sha256'].items():assert sha(ROOT/p)==digest,p
    cities=frame.city.tolist();j=NAMES.index('travel');z=cities.index('Zurich');means=frame.commute_min.to_numpy(float);idx=np.flatnonzero(np.isfinite(means));assert len(idx)==12
    withdrawals={'retained_input':[],'withdraw_Zurich_work_commute':['Zurich'],'withdraw_Dublin_work_commute':['Dublin'],'withdraw_both_work_commute':['Zurich','Dublin'],'withdraw_all_submitted_commute_means':[cities[i] for i in idx]}
    ranks=csv(folder/'commute_withdrawal_ranks.csv');bounds=csv(folder/'commute_withdrawal_bounds.csv')
    for case,removed in withdrawals.items():
        a=l.copy()
        for city in removed:a[cities.index(city),j]=0
        b=bounds[bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(b.lower.to_numpy().reshape(16,10),a,1e-15);close(b.upper.to_numpy().reshape(16,10),h,1e-15)
        for ref,w in REFS.items():check_rows(cities,a,h,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    singles=read(folder/'mean_thresholds.json');joints=read(folder/'joint_thresholds.json');probes=csv(folder/'single_mean_probes.csv');pairs=csv(folder/'joint_pairwise_crossings.csv');cases=csv(folder/'joint_cases.csv');ncorner=0;results=[]
    for ref,w in REFS.items():
        def regrets(a):return np.array([x['max_regret'] for x in independent_scores(a,h,w)])
        def zg(u):
            a=l.copy();a[z,j]=u;r=regrets(a);return r[z]-np.delete(r,z).min()
        single=next(x for x in singles if x['weight_reference']==ref)
        for row in probes[probes.weight_reference==ref].itertuples():close(row.zurich_regret_minus_best_other,zg(row.lower_utility))
        close(single['gap_at_utility_0'],zg(0));close(single['gap_at_utility_1'],zg(1))
        if zg(0)>0>zg(1):
            u=brentq(zg,0,1,xtol=5e-16,rtol=1e-15);close(single['tie_mean_minutes'],-30*math.log(u),1e-10);assert single['status']=='finite_tie'
        else:assert single['tie_mean_minutes'] is None
        item=next(x for x in joints if x['weight_reference']==ref);target=cities.index(item['target']);assert item['target']==('Oslo' if ref=='fixed' else 'Zurich')
        def corner(delta):
            a=l.copy();a[idx,j]=np.exp(-means[idx]*(1-delta)/30)
            if target in idx:a[target,j]=math.exp(-means[target]*(1+delta)/30)
            return a
        def gap(d):
            r=regrets(corner(d));return r[target]-np.delete(r,target).min()
        close(item['gap_at_zero'],gap(0));close(item['gap_at_one'],gap(1));grid=[gap(d) for d in np.linspace(0,1,101)];assert all(b>=a-1e-10 for a,b in zip(grid,grid[1:]))
        if gap(0)<0<gap(1):
            root=brentq(gap,0,1,xtol=5e-16,rtol=1e-15);close(root,item['sharp_radius'],1e-12);assert gap(root-1e-7)<0<gap(root+1e-7)
        else:root=1;assert item['sharp_radius'] is None
        for row in pairs[pairs.weight_reference==ref].itertuples():
            k=cities.index(row.rival)
            def pg(d):r=regrets(corner(d));return r[target]-r[k]
            close(row.gap_at_zero,pg(0));close(row.gap_at_one,pg(1))
            if pd.notna(row.crossing_radius):close(row.crossing_radius,brentq(pg,0,1),1e-10)
        for row in cases[cases.weight_reference==ref].itertuples():close(row.gap,gap(row.radius))
        for delta in [.05,root]:
            bits=(np.arange(4096)[:,None]>>np.arange(12))&1;a=np.broadcast_to(l,(4096,16,10)).copy();a[:,idx,j]=np.exp(-means[idx][None,:]*(1+delta*(2*bits-1))/30)
            low=norms(a,w);upper=norms(h,w);C=np.array([np.delete(upper,i).max() for i in range(16)]);rg=np.maximum(0,C[None,:]-low);allg=rg[:,target]-np.delete(rg,target,axis=1).min(axis=1);close(allg.max(),gap(delta),1e-11);ncorner+=4096
        results.append({'reference':ref,'target':item['target'],'radius':root,'zurich_mean_tie':single['tie_mean_minutes']})
    return {'corners':ncorner,'targets':results,'withdrawal_cases':len(withdrawals)}

def main():
    protected=read(O/'protection_snapshot.json')
    def protection():
        assert not protected['v202_binding_issues_at_capture']
        assert sha(ROOT/'design/task4_user_v202_snapshot.json')==protected['v202_snapshot_sha256']
        for name,digest in protected['v202_bindings'].items():assert sha(ROOT/name)==digest,name
        for name,digest in protected['protected_files'].items():assert sha(Path(name))==digest,name
    protection()
    snapshot_path=ROOT/'design/task4_user_v202_snapshot.json';snapshot=read(snapshot_path)
    assert len(snapshot['source_sha256'])==476
    manifest=read(MANIFEST)
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    f,l0,h0=prior_bounds();f1,l,h=revised_bounds();pd.testing.assert_frame_equal(f,f1,check_exact=True)
    cities=f.city.tolist();z=cities.index('Oslo');j=NAMES.index('public_transport_density');transport=j
    assert l.shape==h.shape==(16,10) and np.count_nonzero(l!=l0)==1
    mask=np.ones((16,10),bool);mask[z,j]=False
    np.testing.assert_array_equal(l[mask],l0[mask]);np.testing.assert_array_equal(h,h0)
    row=manifest['observations'][0];assert row['raw_count']==626 and row['raw_count_before']==89 and row['population']==727797
    for count,arr in [(626,l),(89,l0)]:close(arr[z,j],float(Fraction(count*100000,727797*50+count*100000)),2e-16)
    import itertools
    for flags in itertools.product([False,True],repeat=5):
        old=prior_bounds(*flags);new=revised_bounds(False,*flags)
        pd.testing.assert_frame_equal(old[0],new[0],check_exact=True);np.testing.assert_array_equal(old[1],new[1]);np.testing.assert_array_equal(old[2],new[2])
    for n,kwargs in [(626,{}),(624,{'withhold_rail_replacement':True}),(625,{'withhold_no_calls_bus':True}),(623,{'withhold_rail_replacement':True,'withhold_no_calls_bus':True}),(627,{'include_questioned_stop':True})]:
        _,a,b=revised_bounds(**kwargs);expected=l.copy();expected[z,j]=float(Fraction(n*100000,727797*50+n*100000));close(a,expected,2e-16);np.testing.assert_array_equal(b,h)
    def lower(**kw):return revised_bounds(**kw)[1]
    stage_l=l.copy();stage_h=h.copy();stage_l[cities.index('Singapore'),NAMES.index('travel')]=0;stage_h[cities.index('Singapore'),NAMES.index('travel')]=1
    amsterdam=l.copy();amsterdam[cities.index('Amsterdam'),transport]=0
    cases={'before_V202':(l0,h0),'after_conditional':(l,h),'withdraw_Oslo_bus_refinement':(revised_bounds(False)[1],h),'withdraw_OCBC_venue':(lower(include_sportshub=False),h),'withdraw_Singapore_directory_refinement':(lower(include_sg_pool=False),h),'withdraw_all_Singapore_pool_supplements':(lower(include_sportshub=False,include_sg_pool=False),h),'withhold_existing_three_notice_venues':(lower(withhold_existing_notice_venues=True),h),'withhold_all_four_notice_venues':(lower(withhold_notice_venues=True),h),'withdraw_Zurich_pool_refinement':(lower(include_zurich_pool=False),h),'withdraw_Tokyo_inventory':(lower(include_tokyo=False),h),'withdraw_Warsaw_inventory':(lower(include_warsaw=False),h),'withdraw_both_inventory':(lower(include_tokyo=False,include_warsaw=False),h),'withdraw_historical_stage_proxy':(stage_l,stage_h),'withdraw_Amsterdam_mapped_inventory':(amsterdam,h),'withhold_two_rail_replacement_stops':(lower(withhold_rail_replacement=True),h),'withhold_no_calls_Midtstuen_bus':(lower(withhold_no_calls_bus=True),h),'withhold_all_three_service_flags':(lower(withhold_rail_replacement=True,withhold_no_calls_bus=True),h),'include_questioned_Tveten_bru':(lower(include_questioned_stop=True),h)}
    primary=ROOT/'results/task4_user_v203_revision';ranks=csv(primary/'all_ranks.csv');mc=csv(primary/'mc_city_summary.csv');bounds=csv(primary/'utility_bounds.csv');city_cases=0;mc_rows=0
    assert set(ranks.scenario)==set(cases) and len(ranks)==576 and len(bounds)==2880 and len(mc)==1728
    for case,(a,b) in cases.items():
        saved=bounds[bounds.scenario==case].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])]
        close(saved.lower.to_numpy().reshape(16,10),a,1e-15);close(saved.upper.to_numpy().reshape(16,10),b,1e-15)
        for ref,w in REFS.items():city_cases+=check_rows(cities,a,b,w,ranks[(ranks.scenario==case)&(ranks.weight_reference==ref)])
    for ref,w in REFS.items():
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            for case,(a,b) in cases.items():
                expected=decisions(norms(a,draws),norms(b,draws))
                mc_rows+=check_mc(mc[(mc.scenario==case)&(mc.weight_reference==ref)&(mc.concentration==concentration)],expected,cities)
    primary_summary=read(primary/'summary.json')
    assert primary_summary['admissions_sha256']==sha(MANIFEST) and primary_summary['point_cells']==112 and primary_summary['partial_cells']==37 and primary_summary['fully_missing_cells']==11
    assert primary_summary['mc_seed']==20261108 and primary_summary['mc_draws_per_setting']==10000 and primary_summary['primary_mc_settings']==108
    for report in primary_summary['results']:
        rows=ranks[(ranks.scenario==report['scenario'])&(ranks.weight_reference==report['weight_reference'])]
        close(report['mean_width'],float((rows.score_upper-rows.score_lower).mean()))
        assert report['minimax_choices']==rows.loc[rows.decision_rank==1,'city'].tolist()
        assert report['possible_champions']==rows.loc[rows.possible_champion,'city'].tolist()
        assert report['necessary_champions']==rows.loc[rows.necessary_champion,'city'].tolist()
    before=mc[mc.scenario=='before_V202'].drop(columns='scenario').reset_index(drop=True)
    old=csv(ROOT/'results/task4_user_v202_revision/mc_city_summary.csv');old=old[old.scenario=='after_conditional'].drop(columns='scenario').reset_index(drop=True)
    pd.testing.assert_frame_equal(before,old,check_exact=True)
    extension_structure_tables=0
    for part in ['preferences','future','method','diagnostics']:
        old_folder=ROOT/('results/task4_v202_'+part);new_folder=ROOT/('results/task4_v203_'+part)
        assert {p.name for p in old_folder.glob('*.csv')}=={p.name for p in new_folder.glob('*.csv')}
        for path in new_folder.glob('*.csv'):
            old_table=csv(old_folder/path.name);new_table=csv(path)
            assert list(old_table.columns)==list(new_table.columns) and old_table.shape==new_table.shape
            for column in ['city','indicator','profile','scenario','weight_reference','evidence_arm','concentration','target']:
                if column in old_table:
                    pd.testing.assert_series_equal(old_table[column],new_table[column],check_exact=True)
            extension_structure_tables+=1
    p=ROOT/'results/task4_v203_preferences';pw=csv(p/'weights.csv');pr=csv(p/'ranks.csv');pm=csv(p/'mc_city_summary.csv')
    pd.testing.assert_frame_equal(pw,csv(ROOT/'results/task4_v202_preferences/weights.csv'),check_exact=True)
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
    compare_matrices(read(p/'scenario_matrices.json'),read(ROOT/'results/task4_v202_preferences/scenario_matrices.json'))
    assert len(diagnostic_changes)==3
    pref_mc_rows=0
    for profile in pr.profile.unique():
        w=pw[pw.profile==profile].set_index('indicator').loc[NAMES].weight.to_numpy()
        city_cases+=check_rows(cities,l,h,w,pr[pr.profile==profile])
        for concentration in [20,100,500]:
            draws=np.random.default_rng(np.random.SeedSequence([20261108,concentration])).dirichlet(concentration*w,10000)
            pref_mc_rows+=check_mc(pm[(pm.profile==profile)&(pm.concentration==concentration)],decisions(norms(l,draws),norms(h,draws)),cities)
    from task4_v122_future import SCENARIOS,DRAWS,SEED,WEIGHT_SEED
    future=ROOT/'results/task4_v203_future';fr=csv(future/'ranks.csv');fb=csv(future/'utility_bounds.csv');fm=csv(future/'future_mc_city_summary.csv');wm=csv(future/'weight_mc_city_summary.csv')
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
    method=ROOT/'results/task4_v203_method';mr=csv(method/'method_ranks.csv');ms=read(method/'summary.json')
    for ref,w in REFS.items():independent_method_check(mr[mr.weight_reference==ref].set_index('city').loc[cities].reset_index(),next(v for v in ms['method_cases'] if v['weight_reference']==ref),l,h,w)
    for name in CASE_FILES:assert sha(method/name)==sha(ROOT/'results/task4_v202_method'/name)
    dg=ROOT/'results/task4_v203_diagnostics';dr=csv(dg/'vintage_ranks.csv');du=csv(dg/'witness_utilities.csv');dc=csv(dg/'witness_cases.csv');points=csv(ROOT/'results/task4_v143_vintage/submitted_points.csv')
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
    roots=csv(ROOT/'data/current_oslo_bus_subset/bus_stop_groups.csv');assert len(roots)==626 and set(roots.root_id)==set(manifest['observations'][0]['native_root_ids'])
    source_diagnostics=source_diagnostic_checks(f,l,h)
    protection();precision=precision_checks()
    result=dict(version='V203 staged research',status='pass',activation_status='staged_not_active',current_primary='V202',changed_lower_cells=1,other159_cells_and_all160_uppers_exact=True,withdrawals_exact=True,independent_scalar_city_cases=city_cases,independent_primary_MC_rows=mc_rows,primary_MC_settings_replayed=108,independent_preference_MC_rows=pref_mc_rows,independent_future_shock_MC_rows=future_mc_rows,independent_future_weight_MC_rows=future_weight_rows,draws_per_setting=10000,independent_future_threshold_scan_points=len(scans),historical_csvs_byte_identical=len(CASE_FILES),interior_witness_weight_cases=32,scientific_files_unchanged=len(protected['v202_bindings']),protected_files_unchanged=len(protected['protected_files']),precision_and_mean_rank_audit=precision,source_diagnostics=source_diagnostics,hypothetical_homicide_checks=homicide_checks,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [MANIFEST,Path(__file__),snapshot_path]},result_sha256={str(p.relative_to(ROOT)):sha(p) for folder in [primary,ROOT/'results/task4_v203_preferences',future,method,dg,ROOT/'results/task4_v203_mc_precision',ROOT/'results/task4_v203_mean_rank_comparisons',ROOT/'results/task4_v203_source_diagnostics'] for p in sorted(folder.iterdir()) if p.is_file()})
    (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
