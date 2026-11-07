"""Complete one-source mixture sensitivity for Sao Paulo's travel evidence.
The mixture share is an assumption, never an estimated error or source probability.
"""
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_v7_model import baseline, apply_bounds, collect
from task4_v5_model import ROOT, CITIES, weights, score, summarize


def mixture_bounds(lower,upper,share,mode='coverage'):
    if not (0<=lower<=upper<=1 and 0<=share<=1):raise ValueError('Invalid utility interval or mixture share')
    if mode=='coverage':return (1-share)*lower,(1-share)*upper+share
    if mode=='contamination':
        if share==1:return 0.,1.
        return max(0.,(lower-share)/(1-share)),min(1.,upper/(1-share))
    raise ValueError('Unknown mixture direction')


def analyze(scope,source,mode):
    low,high,_=apply_bounds(*baseline(),collect());i=CITIES.index('Sao Paulo');j=7;w=weights()
    source_l,source_h=source['utility_lower'],source['utility_upper']
    # This case returns to the actually missing baseline at share=1.
    assert low[i,j]==0 and high[i,j]==1
    def state(e):
        l=low.copy();h=high.copy();l[i,j],h[i,j]=mixture_bounds(source_l,source_h,e,mode)
        return summarize(l,h,w)[0]
    original=state(1);f0=state(0);mask=np.arange(len(CITIES))!=i
    upper=score(high,w)
    # Even when excluding any one rival, another rival outranks Sao Paulo's upper bound.
    assert upper[i]<np.sort(upper[mask])[-2]
    def regret(e):
        l=low.copy();l[i,j]=mixture_bounds(source_l,source_h,e,mode)[0]
        return float(np.max(upper[mask])-score(l,w)[i])
    roots=[]
    for k in np.flatnonzero(mask):
        target=float(original.iloc[k].max_regret)
        a,b=regret(0)-target,regret(1)-target
        if a*b<0:
            root=brentq(lambda e:regret(e)-target,0,1,xtol=1e-14)
            assert abs(regret(root)-target)<1e-10
            roots.append(dict(share=root,tied_with=CITIES[k],target_regret=target))
    roots.sort(key=lambda r:r['share'])
    cuts=sorted(set([0.,1.]+[r['share'] for r in roots]));segments=[]
    for a,b in zip(cuts,cuts[1:]):
        f=state((a+b)/2)
        segments.append(dict(share_lower=a,share_upper=b,boundary_convention='open interval; exact boundary is a competition-rank tie',sao_paulo_decision_rank=int(f.iloc[i].decision_rank),possible_champions=int(f.possible_champion.sum())))
    # Independent full-model grid checks challenge the constant-rival and complete-root arguments.
    for e in np.linspace(0,1,101):
        f=state(float(e))
        assert np.allclose(f.loc[mask,'max_regret'],original.loc[mask,'max_regret'],atol=1e-11,rtol=0)
        assert abs(float(f.iloc[i].max_regret)-regret(float(e)))<1e-11
        assert int(f.possible_champion.sum())==25
        if all(abs(e-c)>1e-9 for c in cuts):
            seg=next(s for s in segments if s['share_lower']<e<s['share_upper'])
            assert int(f.iloc[i].decision_rank)==seg['sao_paulo_decision_rank']
    snapshots=[]
    for e in [0,.1,.25,.5,1]:
        f=state(e);f['share']=e;f['scope']=scope;f['mode']=mode;snapshots.append(f)
    return dict(scope=scope,mode=mode,source_interval=[source_l,source_h],main_admitted=False,share_estimated=False,baseline_rank=int(original.iloc[i].decision_rank),rank_at_zero=int(f0.iloc[i].decision_rank),first_rank_loss_share=roots[0]['share'] if roots else None,breakpoints=roots,segments=segments,all_share_possible_champions=25),snapshots


def main():
    source=json.loads((ROOT/'data/task4_v10_saopaulo/sampling_sensitivity.json').read_text())
    results=[];frames=[]
    for scope,r in source['scopes'].items():
        for mode in ['coverage','contamination']:
            summary,fs=analyze(scope,r,mode);results.append(summary);frames.extend(fs)
    out=ROOT/'results/task4_v12_source_sensitivity';out.mkdir(parents=True,exist_ok=True)
    (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n')
    pd.concat(frames).to_csv(out/'rank_scenarios.csv',index=False)
    print(json.dumps([{k:r[k] for k in ['scope','mode','first_rank_loss_share','rank_at_zero','baseline_rank','all_share_possible_champions']} for r in results],indent=2))
if __name__=='__main__':main()
