"""Illustrative midpoint method comparison and separate 25-city country cases."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau

from task4_v5_model import ROOT, NAMES, weights, score

OUT=ROOT/'results/task4_v119_method_country'


def normalize(values):
    span=float(np.max(values)-np.min(values))
    return np.zeros_like(values) if span <= 1e-14 else (values-np.min(values))/span


def vikor(z,w,v=.5):
    """Classic sample best/worst VIKOR; constant criteria contribute zero loss."""
    best=z.max(axis=0);worst=z.min(axis=0);span=best-worst
    loss=np.divide(best-z,span,out=np.zeros_like(z),where=span>1e-14)
    weighted=loss*w
    S=weighted.sum(axis=1);R=weighted.max(axis=1)
    Q=v*normalize(S)+(1-v)*normalize(R)
    return S,R,Q,best,worst


def main():
    paths=[ROOT/'data/task4_v117_team_intake/city_indicators.csv',
           ROOT/'results/task4_user_v118_revision/utility_bounds.csv',
           ROOT/'results/task4_v117_city_revision/utility_bounds.csv',
           ROOT/'data/city_candidates_team_25.csv']
    source=pd.read_csv(paths[0]);u=pd.read_csv(paths[1]);u=u[u.scenario=='after']
    cities=source.city.tolist();assert len(cities)==16
    lower=u.pivot(index='city',columns='indicator',values='lower').loc[cities,NAMES]
    upper=u.pivot(index='city',columns='indicator',values='upper').loc[cities,NAMES]
    z=((lower+upper)/2).to_numpy();w=weights(.1)
    S,R,Q,best,worst=vikor(z,w)
    topsis=score(z,w)
    result=pd.DataFrame(dict(city=cities,topsis_midpoint_score=topsis,
        topsis_rank=pd.Series(topsis).rank(ascending=False,method='min'),
        vikor_S=S,vikor_R=R,vikor_Q=Q,vikor_rank=pd.Series(Q).rank(method='min')))
    tau=kendalltau(result.topsis_rank,result.vikor_rank,variant='b')
    order=np.argsort(Q,kind='stable');a,b=order[:2];threshold=1/(len(cities)-1)
    advantage=bool(Q[b]-Q[a]>=threshold-1e-12)
    stability=bool(S[a]<=S.min()+1e-12 or R[a]<=R.min()+1e-12)
    q_winners=[cities[k] for k in np.flatnonzero(Q<=Q.min()+1e-12)]
    # Degenerate input has zero S/R/Q and no numerical failure.
    for x in [np.ones((3,10))*.4,np.tile(z[0],(3,1))]:
        ds,dr,dq,_,_=vikor(x,w);assert np.all(ds==0) and np.all(dr==0) and np.all(dq==0)
    assert np.all((Q>=-1e-12)&(Q<=1+1e-12))
    country_counts=source.groupby('country').size()
    assert country_counts.max()==1
    # Use the independent 25-city V117 matrices, never merge these into user16.
    legacy=pd.read_csv(paths[2]);legacy=legacy[legacy.scenario=='v117']
    meta=pd.read_csv(paths[3]).set_index('city')
    lc=legacy.city.drop_duplicates().tolist();assert len(lc)==25
    ll=legacy.pivot(index='city',columns='indicator',values='lower').loc[lc,NAMES]
    hh=legacy.pivot(index='city',columns='indicator',values='upper').loc[lc,NAMES]
    sl=pd.Series(score(ll.to_numpy(),w),index=lc);sh=pd.Series(score(hh.to_numpy(),w),index=lc)
    pairs=[('Phoenix','New York'),('Mumbai','Delhi')];pair_reports=[];pair_rows=[]
    for a,b in pairs:
        assert meta.loc[a,'country']==meta.loc[b,'country']
        strict_ab=bool(sl[a]>sh[b]+1e-12);strict_ba=bool(sl[b]>sh[a]+1e-12)
        pair_reports.append(dict(country=meta.loc[a,'country'],city_a=a,city_b=b,
            a_score_interval=[sl[a],sh[a]],b_score_interval=[sl[b],sh[b]],
            a_necessarily_strictly_better=strict_ab,b_necessarily_strictly_better=strict_ba,
            a_possible_pairwise_winner=bool(sh[a]>=sl[b]-1e-12),
            b_possible_pairwise_winner=bool(sh[b]>=sl[a]-1e-12),
            decision='A necessarily better' if strict_ab else 'B necessarily better' if strict_ba else 'No necessary winner identified'))
        for n in NAMES:
            pair_rows.append(dict(country=meta.loc[a,'country'],city_a=a,city_b=b,indicator=n,
                a_lower=ll.loc[a,n],a_upper=hh.loc[a,n],b_lower=ll.loc[b,n],b_upper=hh.loc[b,n],
                a_necessarily_above=bool(ll.loc[a,n]>hh.loc[b,n]+1e-12),
                b_necessarily_above=bool(ll.loc[b,n]>hh.loc[a,n]+1e-12)))
    OUT.mkdir(exist_ok=True)
    result.to_csv(OUT/'method_ranks.csv',index=False)
    pd.DataFrame(dict(indicator=NAMES,weight=w,vikor_sample_best=best,vikor_sample_worst=worst)).to_csv(OUT/'weights_and_ideals.csv',index=False)
    pd.DataFrame(pair_rows).to_csv(OUT/'country_indicator_bounds.csv',index=False)
    pd.DataFrame(pair_reports).to_csv(OUT/'country_score_comparison.csv',index=False)
    source[['city','country']].to_csv(OUT/'user16_country_coverage.csv',index=False)
    summary=dict(method_dataset='user16 V118',country_dataset='separate25 V117',
        midpoint_role='Illustration only; neither imputation nor main recommendation. Main TOPSIS interval/minimax unchanged.',
        comparison_scope='Same midpoint utilities and weights. TOPSIS retains fixed0/1 ideals; classic VIKOR uses sample best/worst. Agreement does not validate missing values or establish truth.',
        kendall_tau_b=float(tau.statistic),kendall_pvalue_descriptive=float(tau.pvalue),
        topsis_winners=result.loc[result.topsis_rank==1,'city'].tolist(),vikor_q_winners=q_winners,
        vikor_v=.5,vikor_advantage_threshold=threshold,
        vikor_first_second_Q_gap=float(Q[order[1]]-Q[order[0]]),
        acceptable_advantage=advantage,acceptable_stability=stability,
        single_compromise_accepted=bool(advantage and stability and len(q_winners)==1),
        vikor_zero_denominator_rule='Constant criteria and zero S/R range contribute zero normalized loss; ties retained.',
        user16_country_counts=country_counts.to_dict(),same_country_comparison_possible_in_user16=False,
        country_pairs=pair_reports,
        limits='One city per country in user16 prevents within-country comparisons or separating city and country effects. Separate25 pairs are illustrative cases, not pooled rankings or estimates of all national cities.',
        input_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths})
    (OUT/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
