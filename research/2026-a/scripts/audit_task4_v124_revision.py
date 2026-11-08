"""Independently audit the V124 facility-only evidence update."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v121_revision import revised_bounds as previous_bounds
from task4_user_v124_revision import revised_bounds,OUT,MANIFEST
from task4_user_city_indicators import SOURCE
from task4_v123_revision_diagnostic import independent_intervals
from task4_v5_model import ROOT,NAMES,weights

def main():
    frame,lo0,hi0=previous_bounds();_,lo,hi=revised_bounds();cities=frame.city.tolist()
    keep=~((lo0==0)&(hi0==1));np.testing.assert_array_equal(np.stack([lo,hi])[:,keep],np.stack([lo0,hi0])[:,keep])
    changes=(lo!=lo0)|(hi!=hi0)
    keys={(cities[i],NAMES[j]) for i,j in zip(*np.where(changes))}
    assert keys=={('Madrid','public_transport_density'),('Tokyo','public_pool_density')}
    assert keep.sum()==139 and changes.sum()==2
    assert lo.shape==(16,10) and np.all(lo>=lo0) and np.all(hi<=hi0)
    prior=pd.read_csv(ROOT/'results/task4_user_v121_revision/current_ranks.csv');current=pd.read_csv(OUT/'all_ranks.csv');cases=0
    observed=json.loads(MANIFEST.read_text())['observations'];selected={(x['city'],x['indicator']) for x in observed}
    for name,g in current.groupby('scenario'):
        if name.startswith('only:'): s={tuple(name.split(':')[1:])}
        elif name.startswith('without:'):s=selected-{tuple(name.split(':')[1:])}
        elif name in {'before','withdraw_all_new','before_withdraw_historical_stage_proxy'}:s=set()
        else:s=selected
        _,a,b=revised_bounds(s)
        if 'historical_stage_proxy' in name:
            a[cities.index('Singapore'),NAMES.index('travel')]=0;b[cities.index('Singapore'),NAMES.index('travel')]=1
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            r=g[g.weight_reference.eq(ref)].set_index('city').loc[cities];d=independent_intervals(a,b,w)
            for col,v in d.items():np.testing.assert_allclose(r[col],v,atol=1e-12,rtol=0)
            if name=='before':
                saved=prior[prior.weight_reference.eq(ref)&prior.scenario.eq('after_conditional')].set_index('city').loc[cities]
                for col in d:np.testing.assert_allclose(r[col],saved[col],atol=1e-12,rtol=0)
            cases+=1
    # Reuse precisely the original weight stream; no sampled data completion.
    from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
    mc=pd.read_csv(OUT/'mc_city_summary.csv');oldmc=pd.read_csv(ROOT/'results/task4_user_v121_revision/mc_city_summary.csv')
    mc_cases=0
    for ref,center in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        for k in [20,100,500]:
            sampled=np.random.default_rng(np.random.SeedSequence([20261108,k])).dirichlet(k*center,10000)
            for name,a0,b0 in [('before',lo0,hi0),('after_conditional',lo,hi),('before_withdraw_historical_stage_proxy',lo0,hi0),('withdraw_historical_stage_proxy',lo,hi)]:
                a,b=a0.copy(),b0.copy()
                if 'historical_stage_proxy' in name:a[cities.index('Singapore'),7]=0;b[cities.index('Singapore'),7]=1
                # Independent broadcast weighted norms and explicit competitor sets.
                l=np.linalg.norm(a[None]*np.sqrt(sampled[:,None]),axis=-1);t=np.linalg.norm((1-a)[None]*np.sqrt(sampled[:,None]),axis=-1);l=100*l/(l+t)
                u=np.linalg.norm(b[None]*np.sqrt(sampled[:,None]),axis=-1);t=np.linalg.norm((1-b)[None]*np.sqrt(sampled[:,None]),axis=-1);u=100*u/(u+t)
                regret=np.stack([np.maximum(0,np.delete(u,i,axis=1).max(1)-l[:,i]) for i in range(16)],axis=1)
                rows=mc[mc.weight_reference.eq(ref)&mc.concentration.eq(k)&mc.scenario.eq(name)].set_index('city').loc[cities]
                for i in range(16):
                    ahead=(regret<regret[:,i,None]-1e-12).sum(1);tied=(abs(regret-regret[:,i,None])<=1e-12).sum(1)
                    expected=[np.clip((1-ahead)/tied,0,1).mean(),(1+ahead+(tied-1)/2).mean(),(u[:,i]>=np.delete(l,i,axis=1).max(1)-1e-12).mean()]
                    np.testing.assert_allclose(rows.iloc[i][['minimax_recommendation_frequency','mean_decision_rank','possible_champion_frequency']].to_numpy(float),expected,atol=1e-11,rtol=0)
                if name=='before':
                    old=oldmc[oldmc.weight_reference.eq(ref)&oldmc.concentration.eq(k)&oldmc.scenario.eq('after_conditional')].set_index('city').loc[cities]
                    for col in ['minimax_recommendation_frequency','mean_decision_rank','possible_champion_frequency']:np.testing.assert_allclose(rows[col],old[col],atol=1e-12,rtol=0)
                mc_cases+=1
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    result=dict(status='pass',shape=[16,10],changed_cells=2,unchanged_cells=158,protected_nonfullymissing_cells=139,all_original_and_V121_nonmissing_values_exactly_preserved=True,independent_static_cases=cases,independent_weight_MC_cases=mc_cases,draws_per_setting=10000,seed_stream_unchanged=True,before_matches_saved_V121=True,all_new_supplements_withdrawable=True,point_cells=int((lo==hi).sum()),partial_cells=int(((lo<hi)&((lo>0)|(hi<1))).sum()),fully_missing_cells=int(((lo==0)&(hi==1)).sum()),output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.csv'))})
    (OUT/'revision_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
