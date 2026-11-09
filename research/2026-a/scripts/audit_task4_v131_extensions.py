"""Independent V131 migration audit using separate norm/odds/competitor formulas."""
from pathlib import Path
import hashlib,importlib.util,json,subprocess
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_user_v130_revision import revised_bounds
from task4_user_v121_revision import revised_bounds as control_bounds
from task4_v5_model import ROOT

# Reuse already-reviewed independent audit utilities, never migration functions.
spec=importlib.util.spec_from_file_location('independent_v122_audit',ROOT/'results/task4_v122_revision/audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
score,decisions,transformed,factor=audit.score,audit.decisions,audit.transformed,audit.factor
city_rows,array_rows,close,check_static=audit.city_rows,audit.array_rows,audit.close,audit.check_static
WEIGHTS,CHANGES,NAMES=audit.WEIGHTS,audit.CHANGES,audit.NAMES
OUT=ROOT/'results/task4_v131_revision'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    repo=ROOT.parents[1]
    protected=[ROOT/'data/task4_v117_team_intake/city_indicators.csv',ROOT/'design/task4_user_current_model.json',ROOT/'design/task4_user_v130_admissions.json',*sorted((ROOT/'results/task4_user_v130_revision').glob('*.csv')),ROOT/'results/task4_user_v130_revision/summary.json']
    frozen={str(p.relative_to(ROOT)):sha(p) for p in protected}
    snapshot=json.loads((ROOT/'design/task4_user_v130_snapshot.json').read_text())
    for name,digest in snapshot['source_sha256'].items():assert sha(ROOT/name)==digest,name
    assert sha(ROOT/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    # Older primary evidence remains an immutable historical control.
    for name in ['design/task4_user_v124_admissions.json', 'results/task4_user_v124_revision/current_ranks.csv', 'results/task4_user_v124_revision/utility_bounds.csv', 'results/task4_user_v124_revision/summary.json']:
        p=ROOT/name
        assert p.read_bytes()==subprocess.check_output(['git','-C',str(repo),'show','8565a65:'+str(p.relative_to(repo))]),p
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();means=frame.commute_min.to_numpy(float);original=np.stack([lo,hi]).copy()
    assert lo.shape==(16,10) and frame.country.nunique()==16
    assert json.loads((ROOT/'design/task4_user_current_model.json').read_text())['version'] in {'V127','V130'}
    sl,su=array_rows(ROOT/'results/task4_user_v130_revision/utility_bounds.csv',cities,scenario='after_conditional');close(sl,lo,atol=1e-15);close(su,hi,atol=1e-15)
    pref=ROOT/'results/task4_v131_preferences';pr=pd.read_csv(pref/'ranks.csv');pmc=pd.read_csv(pref/'mc_city_summary.csv');pw=pd.read_csv(pref/'weights.csv');ps=json.loads((pref/'summary.json').read_text());matrices=json.loads((pref/'scenario_matrices.json').read_text())
    pbase=city_rows(pr,cities,profile='baseline');checks=[]
    for name,js in {'baseline':[],'education_priority':[4,5],'independent_living_priority':[6,7]}.items():
        w=WEIGHTS['fixed'].copy();w[js]*=2;w/=w.sum()
        close(pw[pw.profile==name].set_index('indicator').loc[NAMES].weight,w,atol=1e-15)
        A=np.asarray(matrices[name]['matrix']);close(A,w[:,None]/w[None,:]);close(A@w,10*w);assert abs(matrices[name]['diagnostic']['CR'])<1e-10
        d=decisions(lo,hi,w);rows=city_rows(pr,cities,profile=name);check_static(rows,d,score((lo+hi)/2,w))
        summary=next(x for x in ps['profiles'] if x['profile']==name);close(summary['kendall_tau_b_vs_baseline'],kendalltau(pbase.decision_rank,rows.decision_rank).statistic)
        for k in [20,100,500]:
            sampled=np.random.default_rng(np.random.SeedSequence([20261108,k])).dirichlet(k*w,10000);md=decisions(lo,hi,sampled,average=True);rows=city_rows(pmc,cities,profile=name,concentration=k)
            for col,x in [('minimax_recommendation_frequency',md['credit'].mean(0)),('mean_decision_rank',md['decision_rank'].mean(0)),('top3_decision_frequency',md['top3'].mean(0)),('possible_champion_frequency',md['possible_champion'].mean(0)),('necessary_champion_frequency',md['necessary_champion'].mean(0))]:close(rows[col],x)
            close(rows.minimax_recommendation_frequency.sum(),1);close(rows.top3_decision_frequency.sum(),3);checks.append([name,k])
    future=ROOT/'results/task4_v131_future';fs=json.loads((future/'summary.json').read_text());fr=pd.read_csv(future/'ranks.csv');bounds={};inputs={}
    arms=['conditional','withdraw_historical_stage_proxy']
    for arm in arms:
        l,u=lo.copy(),hi.copy()
        if arm!='conditional':l[cities.index('Singapore'),7],u[cities.index('Singapore'),7]=0,1
        inputs[arm]=(l,u)
        for name,changes in CHANGES.items():
            a,b=transformed(l,u,factor(l.shape,changes),means);bounds[arm,name]=(a,b)
            al,au=array_rows(future/'utility_bounds.csv',cities,evidence_arm=arm,scenario=name);close(al,a,atol=1e-14);close(au,b,atol=1e-14)
            unknown=(l==0)&(u==1);np.testing.assert_array_equal(a[unknown],0);np.testing.assert_array_equal(b[unknown],1)
            for ref,w in WEIGHTS.items():
                rows=city_rows(fr,cities,evidence_arm=arm,scenario=name,weight_reference=ref);d=decisions(a,b,w);check_static(rows,d,score((a+b)/2,w))
                ss=next(x for x in fs['scenarios'] if x['evidence_arm']==arm and x['scenario']==name and x['weight_reference']==ref);close(ss['mean_score_interval_width'],np.mean(d['score_upper']-d['score_lower']))
    thresholds=pd.read_csv(future/'thresholds.csv');scan=pd.read_csv(future/'threshold_scan.csv')
    for row in thresholds.to_dict('records'):
        i=cities.index(row['city']);w=WEIGHTS[row['weight_reference']];others=[j for j in range(16) if j!=i]
        def gap(r):
            a,b=transformed(lo,hi,factor(lo.shape,{1:r-1,4:r-1,7:r-1},i),means);d=decisions(a,b,w);return d['max_regret'][i]-d['max_regret'][others].min()
        points=scan[(scan.city==row['city'])&(scan.weight_reference==row['weight_reference'])];assert len(points)==101
        for point in points.itertuples():close(point.regret_gap_to_best_other,gap(point.raw_multiplier))
        close(row['baseline_gap_to_best_other'],gap(1));close(row['gap_at_50pct_cost_reduction'],gap(.5))
        if row['status']=='crossing_found':
            r=row['threshold_raw_multiplier'];assert abs(gap(r))<1e-8 and gap(r-1e-6)<-1e-10 and gap(r+1e-6)>1e-10;close(row['required_cost_reduction_fraction'],1-r)
        elif row['status']=='already_strict_minimax':assert gap(1)<-1e-10
        elif row['status']=='not_reached':assert gap(.5)>0
        else:assert row['status']=='tie_only_at_endpoint' and abs(gap(.5))<=1e-10
    fmc=pd.read_csv(future/'future_mc_city_summary.csv');rng=np.random.default_rng(20261108122);common=rng.uniform(0,1,(10000,1));local=rng.uniform(0,1,(10000,16));delta=.05*common+.05*local
    fchecks=[]
    for arm in arms:
        l,u=inputs[arm]
        for ref,w in WEIGHTS.items():
            l0,u0=score(l,w),score(u,w)
            for name,changes in CHANGES.items():
                if name=='baseline':continue
                m=np.ones((10000,16,10))
                for j,change in changes.items():m[...,j]=1+np.sign(change)*delta
                a,b=transformed(l,u,m,means);md=decisions(a,b,w,tol=1e-10,future_credit=True);rows=city_rows(fmc,cities,evidence_arm=arm,scenario=name,weight_reference=ref)
                for col,x in [('recommendation_frequency',md['credit'].mean(0)),('possible_champion_frequency',md['possible_champion'].mean(0)),('mean_decision_rank',md['decision_rank'].mean(0))]:close(rows[col],x)
                for side,base in [('lower',l0),('upper',u0)]:
                    for q,suffix in [(.05,'p05'),(.5,'p50'),(.95,'p95')]:close(rows[f'score_{side}_change_{suffix}'],np.quantile(md[f'score_{side}']-base,q,axis=0))
                fchecks.append([arm,ref,name])
    wmc=pd.read_csv(future/'weight_mc_city_summary.csv');savedmc=pd.read_csv(ROOT/'results/task4_user_v130_revision/mc_city_summary.csv');wchecks=[]
    for arm in arms:
        for ref,w in WEIGHTS.items():
            sampled=np.random.default_rng(np.random.SeedSequence([20261108,100])).dirichlet(100*w,10000)
            for name in CHANGES:
                a,b=bounds[arm,name];md=decisions(a,b,sampled,tol=1e-10,future_credit=True);rows=city_rows(wmc,cities,evidence_arm=arm,weight_reference=ref,scenario=name)
                for col,x in [('recommendation_frequency',md['credit'].mean(0)),('mean_decision_rank',md['decision_rank'].mean(0)),('possible_champion_frequency',md['possible_champion'].mean(0))]:close(rows[col],x)
                if name=='baseline':
                    base_scenario='after_conditional' if arm=='conditional' else 'withdraw_historical_stage_proxy';old=city_rows(savedmc,cities,scenario=base_scenario,weight_reference=ref,concentration=100);close(rows.recommendation_frequency,old.minimax_recommendation_frequency);close(rows.mean_decision_rank,old.mean_decision_rank)
                wchecks.append([arm,ref,name])
    method=ROOT/'results/task4_v131_method_country';ms=json.loads((method/'summary.json').read_text());mr=pd.read_csv(method/'method_ranks.csv');mchecks=[]
    for version,fn in [('V121',control_bounds),('V130',revised_bounds)]:
        _,a,b=fn();saved_a,saved_b=array_rows(method/'method_utility_inputs.csv',cities,evidence_version=version);close(saved_a,a,atol=1e-15);close(saved_b,b,atol=1e-15);z=(a+b)/2
        for ref,w in WEIGHTS.items():
            rows=city_rows(mr,cities,evidence_version=version,weight_reference=ref);best,worst=z.max(0),z.min(0);loss=np.divide(best-z,best-worst,out=np.zeros_like(z),where=best-worst>1e-14)*w;S,R=loss.sum(1),loss.max(1)
            qs=(S-S.min())/(S.max()-S.min()) if S.max()-S.min()>1e-14 else np.zeros(16);qr=(R-R.min())/(R.max()-R.min()) if R.max()-R.min()>1e-14 else np.zeros(16);Q=.5*(qs+qr);t=score(z,w);tr=[1+sum(t>x) for x in t];vr=[1+sum(Q<x) for x in Q]
            for col,x in [('topsis_midpoint_score',t),('topsis_rank',tr),('vikor_S',S),('vikor_R',R),('vikor_Q',Q),('vikor_rank',vr)]:close(rows[col],x)
            ss=next(x for x in ms['method_cases'] if x['evidence_version']==version and x['weight_reference']==ref);close(ss['kendall_tau_b'],kendalltau(tr,vr).statistic);o=np.argsort(Q,kind='stable');first,second=o[:2];adv=bool(Q[second]-Q[first]>=1/15-1e-12);stab=bool(S[first]<=S.min()+1e-12 or R[first]<=R.min()+1e-12);assert ss['acceptable_advantage']==adv and ss['acceptable_stability']==stab
            if version=='V121':
                old=city_rows(pd.read_csv(ROOT/'results/task4_v122_method_country/method_ranks.csv'),cities,evidence_version=version,weight_reference=ref)
                for col in ['topsis_midpoint_score','topsis_rank','vikor_S','vikor_R','vikor_Q','vikor_rank']:close(rows[col],old[col],atol=1e-14)
            mchecks.append([version,ref,adv,stab])
    historical=['country_score_comparison.csv','country_indicator_bounds.csv','user16_country_coverage.csv','shanghai_district_resources.csv','istanbul_historical_age_groups.csv','singapore2020_secondary_exact_age_counts.csv']
    for name in historical:assert (method/name).read_bytes()==(ROOT/'results/task4_v122_method_country'/name).read_bytes(),name
    # Current-data diagnostic completions: membership, strict interiors and scores.
    diag=ROOT/'results/task4_v131_revision_diagnostic';ds=json.loads((diag/'summary.json').read_text());wu=pd.read_csv(diag/'witness_utilities.csv',float_precision='round_trip');ws=pd.read_csv(diag/'witness_scores.csv',float_precision='round_trip');rc=pd.read_csv(diag/'rank_comparison.csv',float_precision='round_trip')
    diagnostic_checks=[]
    for ref,w in WEIGHTS.items():
        d=decisions(lo,hi,w);rows=city_rows(rc,cities,weight_reference=ref);z=(lo+hi)/2;t=score(z,w);tr=[1+sum(t>x) for x in t];ir=[1+sum(d['max_regret']<x) for x in d['max_regret']]
        close(rows.midpoint_scenario_score,t);close(rows.midpoint_scenario_rank,tr);close(rows.interval_decision_rank,ir)
        report=next(x for x in ds['results'] if x['weight_reference']==ref);close(report['kendall_tau_b'],kendalltau(tr,ir).statistic);assert report['changed_city_decision_ranks']==int(np.sum(np.asarray(tr)!=ir))
        for name in wu.scenario.unique():
            f=wu[(wu.weight_reference==ref)&(wu.scenario==name)].set_index(['city','indicator']).loc[pd.MultiIndex.from_product([cities,NAMES])];z=f.utility.to_numpy().reshape(16,10);assert np.all(z>=lo) and np.all(z<=hi);np.testing.assert_array_equal(z[lo==hi],lo[lo==hi])
            if name=='interior_counterexample':assert np.all(z[lo<hi]>lo[lo<hi]) and np.all(z[lo<hi]<hi[lo<hi])
            values=score(z,w);rows=city_rows(ws,cities,weight_reference=ref,scenario=name);close(rows.score,values);close(rows.scenario_rank,[1+sum(values>x) for x in values])
            if name!='midpoint_diagnostic':assert cities[int(np.argmax(values))]=='Dublin' and values[cities.index('Dublin')]>values[cities.index('Zurich')]
            if name=='adversarial_endpoint_Dublin':close(values[cities.index('Dublin')]-values[cities.index('Zurich')],d['max_regret'][cities.index('Zurich')])
        assert d['possible_champion'].all() and not d['necessary_champion'].any();diagnostic_checks.append(ref)
    # Explicit legacy-inventory withdrawal on current evidence: new facilities stay.
    l,u=lo.copy(),hi.copy()
    for city in ['Paris','Dublin']:l[cities.index(city),6],u[cities.index(city),6]=0,1
    for w in WEIGHTS.values():assert cities[int(np.argmin(decisions(l,u,w)['max_regret']))]=='Zurich'
    for p,expected in frozen.items():assert sha(ROOT/p)==expected,p
    for name,digest in snapshot['source_sha256'].items():assert sha(ROOT/name)==digest,name
    _,a,b=revised_bounds();np.testing.assert_array_equal(original,np.stack([a,b]))
    OUT.mkdir(exist_ok=True,parents=True)
    result=dict(status='pass',primary_snapshot='design/task4_user_v130_snapshot.json',older_V124_control_commit='8565a65',V130_snapshot_all160_bounds_CSV_registry_and_primary_outputs_unchanged=True,input_sha256=frozen,preferences_independent_MC_settings=checks,future_deterministic_arms=16,future_threshold_scan_points=len(scan),future_threshold_cases=len(thresholds),future_shock_independent_settings=fchecks,future_weight_independent_settings=wchecks,draws_per_setting=10000,method_independent_cases=mchecks,historical_cases_identical_to_audited_V122=historical,diagnostic_completion_independent_references=diagnostic_checks,current_prior_historical_inventory_withdrawal_recommends_Zurich=True,result_sha256={str(p.relative_to(ROOT)):sha(p) for directory in [pref,future,method,diag] for p in sorted(directory.iterdir()) if p.suffix in ['.csv','.json']})
    (OUT/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS V131: independent preferences, both-arm future MC, thresholds, VIKOR, legacy separation and V130 protection')
if __name__=='__main__':main()
