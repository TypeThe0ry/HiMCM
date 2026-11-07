"""Optimistic city-local acquisition across a continuous preference interval.

Upper-endpoint observations maximize the target's recommendation margin at
EVERY alpha. Success is a certificate in the rectangular outer model, not a
forecast of attainable observations. Unresolved intervals remain unresolved.
"""
from itertools import combinations
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,score,weights,summarize
from task4_cape_2025_revision import cape_2025_bounds
from task4_evidence_withdrawal import regrets
from task4_recommendation_acquisition import minimum_recommendation_bundles
from task4_continuous_recommendation import certify
from task4_continuous_preferences import feasible_preferences
TOL=1e-8


def margin(lo,hi,i,alpha):
    r=regrets(score(lo,weights(alpha)),score(hi,weights(alpha)))
    return float(np.delete(r,i).min()-r[i])


def check_bundle(lo,hi,i,subset,max_depth=10):
    l=lo.copy();l[i,list(subset)]=hi[i,list(subset)]
    for alpha in [.05,.1,.2]:
        gap=margin(l,hi,i,alpha)
        if gap < -TOL:
            return dict(status='excluded_by_witness',witness_alpha=alpha,witness_margin=gap),[]
    leaves=certify(l,hi,max_depth=max_depth)
    # A certified rival on any nonempty interval disproves target uniqueness.
    for leaf in leaves:
        if leaf['certified'] and leaf['winner']!=i:
            alpha=(leaf['alpha_lower']+leaf['alpha_upper'])/2
            gap=margin(l,hi,i,alpha)
            assert gap < -TOL
            return dict(status='excluded_by_witness',witness_alpha=alpha,witness_margin=gap),leaves
    if all(c['certified'] and c['winner']==i for c in leaves):
        return dict(status='certified_outer_box',minimum_margin_bound=min(c['regret_gap_lower'] for c in leaves)),leaves
    return dict(status='unresolved'),leaves


def search(lo,hi,i):
    unknown=np.flatnonzero(hi[i]-lo[i]>1e-12).tolist()
    evaluated=[];certificates=[];minimum=None
    for size in range(len(unknown)+1):
        successes=0
        for subset in combinations(unknown,size):
            result,leaves=check_bundle(lo,hi,i,subset)
            name='|'.join(NAMES[j] for j in subset)
            evaluated.append(dict(city=CITIES[i],size=size,indicators=name,**result))
            if result['status']=='certified_outer_box':
                successes+=1
                certificates.extend(dict(city=CITIES[i],indicators=name,**c) for c in leaves)
        if successes:
            minimum=size;break
    lower_unresolved=[r for r in evaluated if r['status']=='unresolved' and (minimum is None or r['size']<minimum)]
    fixed,options=minimum_recommendation_bundles(lo,hi,weights(),i)
    summary=dict(city=CITIES[i],fixed_alpha_minimum=fixed,fixed_alpha_minimal_bundles=len(options),
                 smallest_certified_continuous_bundle=minimum,minimum_proved_in_outer_model=minimum is not None and not lower_unresolved,
                 unresolved_smaller_bundles=len(lower_unresolved),
                 certified_minimal_bundles=sum(r['status']=='certified_outer_box' for r in evaluated),
                 unresolved_at_smallest_certified_size=sum(r['status']=='unresolved' and r['size']==minimum for r in evaluated))
    return summary,evaluated,certificates


def checks():
    a=np.full((2,10),.4);b=a.copy();b[0]=.8
    assert check_bundle(a,b,0,range(10))[0]['status']=='certified_outer_box'
    tied=np.full((2,10),.5)
    assert check_bundle(tied,tied,0,[],max_depth=2)[0]['status']=='unresolved'
    rng=np.random.default_rng(6401)
    for _ in range(12):
        l=rng.uniform(0,.5,(4,10));h=l+rng.uniform(0,.5,(4,10));js=[0,4,7]
        upper=l.copy();upper[0,js]=h[0,js]
        for alpha in [.05,.073,.1,.147,.2]:
            best=margin(upper,h,0,alpha)
            for _ in range(10):
                ll,hh=l.copy(),h.copy();v=rng.uniform(l[0,js],h[0,js]);ll[0,js]=hh[0,js]=v
                assert margin(ll,hh,0,alpha)<=best+1e-10


def main():
    checks();lo,hi=cape_2025_bounds();saved=np.stack([lo,hi]).copy()
    summaries=[];evaluations=[];certificates=[]
    for i in range(len(CITIES)):
        s,e,c=search(lo,hi,i);summaries.append(s);evaluations+=e;certificates+=c
    np.testing.assert_array_equal(np.stack([lo,hi]),saved)
    rank,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v63_cape_2025/ranks.csv')
    prior=prior[prior.scenario=='v63_ghs2025_age14_18'].reset_index(drop=True)
    assert rank.city.tolist()==prior.city.tolist()
    for col in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(rank[col],prior[col],rtol=0,atol=1e-12)
    continuous=[c for i,c in enumerate(CITIES) if feasible_preferences(hi[i],lo[np.arange(len(lo))!=i])['possible']]
    out=ROOT/'results/task4_v64_continuous_acquisition';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(summaries).to_csv(out/'minimum_bundles.csv',index=False)
    pd.DataFrame(evaluations).to_csv(out/'bundle_evaluations.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'bundle_certificates.csv',index=False)
    rank.to_csv(out/'ranks.csv',index=False)
    result=dict(baseline='V63',changed_cells=0,changed_ranks=0,alpha_range=[.05,.2],fixed_alpha=.1,
        possible_champions=int(rank.possible_champion.sum()),continuous_possible_champions=continuous,
        choice=[CITIES[i] for i in decision['minimax_choices']],main_admitted=False,
        focal_cities=[r for r in summaries if r['city'] in ['Phoenix','Tokyo','Cape Town','Shanghai','London','New York']],
        unresolved_bundles=sum(r['status']=='unresolved' for r in evaluations),
        scope='City-local favorable exact observations in rectangular utility outer box; not guaranteed outcomes, physically joint attainability, or necessary performance champions.',
        proof='Upper endpoint maximizes target lower score and preserves target upper score. Target regret is minimized and each rival regret maximized for every alpha; one common endpoint vector is simultaneously optimal.',
        tolerances=dict(witness_negative_margin=TOL,score_padding=1e-9,certificate_positive_gap=TOL,max_depth=10,numerical_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['focal_cities'],indent=2));print('unresolved',result['unresolved_bundles'])

if __name__=='__main__':main()
