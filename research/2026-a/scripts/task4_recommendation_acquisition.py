"""Minimum city-local exact measurements that could change the recommendation.

Favorable upper-endpoint observations minimize the selected city's regret and
maximize all rivals' regrets among possible outcomes of the same measurements.
They are acquisition feasibility bounds, never replacement observations.
"""
from itertools import combinations
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,score,weights,summarize
from task4_istanbul_coverage_revision import istanbul_coverage_bounds
from task4_evidence_withdrawal import regrets


def minimum_recommendation_bundles(lo,hi,w,i,tol=1e-9):
    ls,us=score(lo,w),score(hi,w)
    base=regrets(ls,us)
    others=np.arange(len(lo))!=i
    rival_regret=float(base[others].min())
    rival_upper=float(us[others].max())
    unknown=np.flatnonzero(hi[i]-lo[i]>1e-12).tolist()
    for size in range(len(unknown)+1):
        found=[]
        for subset in combinations(unknown,size):
            row=lo[i].copy();row[list(subset)]=hi[i,list(subset)]
            own=max(0.,rival_upper-float(score(row[None,:],w)[0]))
            if own<rival_regret-tol:found.append((subset,rival_regret-own))
        if found:return size,found
    return None,[]


def main():
    lo,hi=istanbul_coverage_bounds();saved=np.stack([lo,hi]).copy();w=weights()
    rows=[];details=[];education_travel=[]
    for i,city in enumerate(CITIES):
        minimum,options=minimum_recommendation_bundles(lo,hi,w,i)
        rows.append(dict(city=city,minimum_city_local_measurements=minimum,minimal_bundle_count=len(options)))
        for subset,margin in options:
            l=lo.copy();l[i,list(subset)]=hi[i,list(subset)]
            actual=regrets(score(l,w),score(hi,w))
            assert actual[i]<np.delete(actual,i).min()-1e-9
            details.append(dict(city=city,indicators='|'.join(NAMES[j] for j in subset),size=minimum,
                                favorable_regret_margin=margin))
        l=lo.copy();l[i,[4,7]]=hi[i,[4,7]]
        actual=regrets(score(l,w),score(hi,w));margin=float(np.delete(actual,i).min()-actual[i])
        education_travel.append(dict(city=city,education_travel_can_make_unique_recommendation=margin>1e-9,
                                     favorable_regret_margin=margin))
    # Independent finite grids verify endpoint dominance on nonlinear examples.
    rng=np.random.default_rng(5501)
    for _ in range(30):
        a=rng.uniform(0,.5,(4,10));b=a+rng.uniform(0,.5,(4,10));i=0;js=[4,7]
        best=a.copy();best[i,js]=b[i,js]
        rbest=regrets(score(best,w),score(b,w));mbest=np.delete(rbest,i).min()-rbest[i]
        for x in np.linspace(0,1,7):
            for y in np.linspace(0,1,7):
                l,h=a.copy(),b.copy();v=a[i,js]+np.array([x,y])*(b[i,js]-a[i,js])
                l[i,js]=h[i,js]=v
                rr=regrets(score(l,w),score(h,w))
                assert np.delete(rr,i).min()-rr[i]<=mbest+1e-10
    tied=np.full((3,10),.5)
    assert minimum_recommendation_bundles(tied,tied,w,0)==(None,[])
    rank,d=summarize(lo,hi,w)
    old=pd.read_csv(ROOT/'results/task4_v54_scope_intake/ranks.csv')
    for key in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(rank[key],old[key],rtol=0,atol=1e-12)
    np.testing.assert_array_equal(np.stack([lo,hi]),saved)
    out=ROOT/'results/task4_v55_recommendation_acquisition';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'minimum_measurements.csv',index=False)
    pd.DataFrame(details).to_csv(out/'minimal_bundles.csv',index=False)
    pd.DataFrame(education_travel).to_csv(out/'education_travel.csv',index=False)
    rank.to_csv(out/'ranks.csv',index=False)
    result=dict(baseline='V53 current bounds',fixed_alpha=.1,new_admitted_cells=0,
        possible_champions=int(rank.possible_champion.sum()),choice=[CITIES[k] for k in d['minimax_choices']],
        phoenix=rows[CITIES.index('Phoenix')],tokyo=rows[CITIES.index('Tokyo')],
        cities_education_travel_can_recommend=[r['city'] for r in education_travel if r['education_travel_can_make_unique_recommendation']],
        interpretation='Optimistic city-local exact-observation feasibility in the existing utility box, not a measurement forecast, probability, or all-city minimum.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
