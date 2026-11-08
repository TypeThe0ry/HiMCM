"""Evidence-only revision of V118, with explicit withdrawal of historical stage proxy."""
import json, hashlib
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,NAMES,weights
from task4_user_city_indicators import SOURCE,evaluate
from task4_user_v118_revision import revised_bounds as previous_bounds
from task4_ahp_mc_baseline import score_many,interval_metrics,rank_metrics
MANIFEST=ROOT/'design/task4_user_v120_admissions.json'
OUT=ROOT/'results/task4_user_v120_revision'
def revised_bounds(selected=None):
    f,l,h=previous_bounds();before=np.stack([l,h]).copy()
    m=json.loads(MANIFEST.read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==m['input_sha256']
    for p,digest in m['source_hashes'].items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest,p
    for r in m['observations']:
        if selected is not None and r['city'] not in selected:continue
        i=f.city.tolist().index(r['city']);j=NAMES.index(r['indicator'])
        np.testing.assert_array_equal([l[i,j],h[i,j]],[0,1])
        if r.get('kind')=='teacher_interval':
            low,high=r['teacher_fte_bounds']
            computed=[15/(15+r['students']/low),15/(15+r['students']/high)]
        elif r['indicator']=='public_transport_density':
            assert float(f.iloc[i].population)==r['population']
            density=r['raw_count']*100000/r['population'];computed=[density/(50+density),1]
        else:
            assert r['city']=='Singapore' and r['indicator']=='travel'
            computed=json.loads((ROOT/'data/task4_v120_singapore/derived_bounds.json').read_text())['stage_hull']
        np.testing.assert_allclose(computed,r['utility_after'],atol=1e-12,rtol=0)
        l[i,j],h[i,j]=computed
    protected=~((before[0]==0)&(before[1]==1))
    np.testing.assert_array_equal(np.stack([l,h])[:,protected],before[:,protected])
    assert np.all(l>=before[0]) and np.all(h<=before[1]) and np.all(l<=h)
    return f,l,h

def main():
    f,lo0,hi0=previous_bounds();_,lo,hi=revised_bounds();cities=f.city.tolist()
    cases=[('before',lo0,hi0)]
    for c in ('Zurich','Helsinki','Singapore','Prague'):
        _,l,h=revised_bounds({c});cases.append(('only_'+c,l,h))
    cases.append(('after_conditional',lo,hi))
    _,l,h=revised_bounds({'Zurich','Helsinki','Prague'});cases.append(('withdraw_historical_stage_proxy',l,h))
    rr=[];bb=[];ss=[]
    for name,l,h in cases:
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            old=evaluate(cities,lo0,hi0,w);out=evaluate(cities,l,h,w)
            out['previous_decision_rank']=old.decision_rank
            out['rank_change_positive_improves']=old.decision_rank-out.decision_rank
            rr.append(out.assign(scenario=name,weight_reference=ref))
            ss.append(dict(scenario=name,weight_reference=ref,possible_champions=out.loc[out.possible_champion,'city'].tolist(),minimax_choices=out.loc[out.decision_rank==1,'city'].tolist(),mean_width=float((out.score_upper-out.score_lower).mean()),kendall_tau=float(kendalltau(old.decision_rank,out.decision_rank).statistic)))
        for i,c in enumerate(cities):
            for j,n in enumerate(NAMES):bb.append(dict(scenario=name,city=c,indicator=n,lower=l[i,j],upper=h[i,j]))
    OUT.mkdir(exist_ok=True,parents=True)
    allr=pd.concat(rr,ignore_index=True);allr.to_csv(OUT/'all_ranks.csv',index=False)
    allr[allr.scenario=='after_conditional'].to_csv(OUT/'current_ranks.csv',index=False)
    pd.DataFrame(bb).to_csv(OUT/'utility_bounds.csv',index=False)
    # Identical random weights before/after, not resampling the missing values.
    mc=[]
    for ref,center in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        for k in (20,100,500):
            w=np.random.default_rng(np.random.SeedSequence([20261108,k])).dirichlet(k*center,10000)
            for case,l,h in [cases[0],cases[-2],cases[-1]]:
                lower,upper=score_many(l,w),score_many(h,w)
                regret,possible,necessary,_,_=interval_metrics(lower,upper)
                ranks,recommended,_=rank_metrics(regret,descending=False)
                assert np.allclose(recommended.sum(axis=1),1)
                for i,c in enumerate(cities):mc.append(dict(scenario=case,weight_reference=ref,concentration=k,city=c,minimax_recommendation_frequency=float(recommended[:,i].mean()),mean_decision_rank=float(ranks[:,i].mean()),possible_champion_frequency=float(possible[:,i].mean())))
    pd.DataFrame(mc).to_csv(OUT/'mc_city_summary.csv',index=False)
    summary=dict(results=ss,changed_cells=int(np.sum((lo!=lo0)|(hi!=hi0))),unchanged_cells=int(np.sum((lo==lo0)&(hi==hi0))),point_cells=int(np.sum(lo==hi)),partial_cells=int(np.sum((lo<hi)&((lo>0)|(hi<1)))),fully_missing_cells=int(np.sum((lo==0)&(hi==1))),input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),mc_seed=20261108,mc_draws_per_setting=10000,scope='Conditional mixed-year school-stage proxy arm and its explicit withdrawal; no claim of identified ages14-18 or2025 travel.')
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
