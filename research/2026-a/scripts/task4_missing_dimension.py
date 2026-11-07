"""Exact interval sensitivity to omitted criteria at fixed observed weights.
Unknown youth utilities are NOT observations or imputed city data.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results/task4_missing_dimension'
OUT.mkdir(parents=True,exist_ok=True)

def utility(A,B,alpha,y):
    minus=np.sqrt((1-alpha)*A+alpha*np.asarray(y)**2)
    plus=np.sqrt((1-alpha)*B+alpha*(1-np.asarray(y))**2)
    return minus/(minus+plus)

def intervals(A,B,alpha,lo=0.,hi=1.):
    return utility(A,B,alpha,lo),utility(A,B,alpha,hi)

def main():
    df=pd.read_csv(ROOT/'results/task4_real/normalized_indicators.csv',index_col=0)
    z=df.to_numpy();names=df.index.to_numpy();w=np.ones(4)/4
    A=(z*z)@w;B=((1-z)**2)@w
    base=utility(A,B,0,0);a=int(base.argmax())
    # Analytic equality threshold for incumbent unknown utility 0, challenger 1.
    thresholds=[]
    for h in range(len(names)):
        if h==a:continue
        t=(-(B[a]+A[h])+np.sqrt((B[a]-A[h])**2+4*A[a]*B[h]))/2
        alpha=max(0.,float(t/(1+t)))
        gap=lambda x:utility(A[h],B[h],x,1)-utility(A[a],B[a],x,0)
        numeric=brentq(gap,0,1)
        assert abs(alpha-numeric)<1e-10
        assert abs(gap(alpha))<1e-10
        assert gap(max(0,alpha-1e-5))<0 and gap(min(1,alpha+1e-5))>0
        thresholds.append({'incumbent':names[a],'challenger':names[h],
                           'tie_alpha':alpha,'scope':'fixed equal observed weights; incumbent y=0, challenger y=1'})
    th=pd.DataFrame(thresholds).sort_values('tie_alpha')
    th.to_csv(OUT/'exact_overturn_thresholds.csv',index=False)
    rows=[];diagnostics=[]
    for alpha in np.round(np.linspace(0,.4,81),8):
        low,high=intervals(A,B,alpha)
        possible=[];necessary=[]
        for i in range(25):
            others=np.arange(25)!=i
            # Competition ranks; only strictly higher scores count as ahead.
            best=1+int(np.sum(low[others]>high[i]+1e-12))
            worst=1+int(np.sum(high[others]>low[i]+1e-12))
            # A weak champion may tie; thresholds explicitly report equalities.
            pc=bool(high[i]>=low[others].max()-1e-12)
            nc=bool(low[i]>=high[others].max()-1e-12)
            if pc:possible.append(names[i])
            if nc:necessary.append(names[i])
            rows.append({'alpha':alpha,'city':names[i],'score_low':low[i]*100,
                         'score_high':high[i]*100,'best_attainable_rank':best,
                         'worst_attainable_rank':worst,'possible_weak_champion':pc,
                         'necessary_weak_champion':nc})
        diagnostics.append({'alpha':alpha,'possible_champions':possible,'necessary_champions':necessary})
    ranges=pd.DataFrame(rows);ranges.to_csv(OUT/'rank_bounds.csv',index=False)
    # Sensitivity to the allowed missing-utility range, an assumption not measured evidence.
    bound_checks=[]
    first=int(np.where(names==th.iloc[0].challenger)[0][0])
    for lo,hi in [(0.,1.),(.1,.9),(.25,.75),(.4,.6)]:
        gap=lambda x:utility(A[first],B[first],x,hi)-utility(A[a],B[a],x,lo)
        root=brentq(gap,0,1)
        bound_checks.append({'lower_unknown_utility':lo,'upper_unknown_utility':hi,
                             'challenger':names[first],'tie_alpha':root})
    pd.DataFrame(bound_checks).to_csv(OUT/'unknown_range_sensitivity.csv',index=False)
    # Evidence target: lower bound on incumbent's unknown utility sufficient for
    # it to remain a weak champion even if every competitor has utility one.
    targets=[]
    for alpha in [.05,.1,.2,.3]:
        competitor=float(np.max(utility(A[np.arange(25)!=a],B[np.arange(25)!=a],alpha,1)))
        f=lambda y:float(utility(A[a],B[a],alpha,y)-competitor)
        needed=0. if f(0)>=0 else (float(brentq(f,0,1)) if f(1)>=0 else None)
        targets.append({'alpha':alpha,'city':names[a],
                        'sufficient_lower_bound_on_missing_utility':needed,
                        'competitors_upper_bound_assumed':1.})
    pd.DataFrame(targets).to_csv(OUT/'evidence_targets.csv',index=False)
    # Analyst-declared profiles; never presented as sampled demographic groups.
    profile_weights={'equal':[.25,.25,.25,.25], 'safety_priority':[.55,.15,.15,.15],
                     'environment_priority':[.15,.55,.15,.15],
                     'housing_priority':[.15,.15,.55,.15], 'commute_priority':[.15,.15,.15,.55]}
    profiles=[]
    for name,weights in profile_weights.items():
        aa=z*z@np.array(weights);bb=(1-z)**2@np.array(weights)
        bbscore=utility(aa,bb,0,0);i=int(bbscore.argmax())
        choices=[]
        for j in range(25):
            if j==i:continue
            tt=(-(bb[i]+aa[j])+np.sqrt((bb[i]-aa[j])**2+4*aa[i]*bb[j]))/2
            choices.append((max(0,float(tt/(1+tt))),j))
        val,j=min(choices)
        profiles.append({'profile':name,'baseline_winner':names[i],
                         'first_potential_challenger':names[j],'tie_alpha':val})
    pd.DataFrame(profiles).to_csv(OUT/'declared_preference_profiles.csv',index=False)
    # Endpoint checks on random admissible completions: no draw can exceed its bounds.
    rng=np.random.default_rng(44)
    for alpha in [.01,.05,.1,.2,.4]:
        low,high=intervals(A,B,alpha)
        realized=utility(A,B,alpha,rng.uniform(0,1,(1000,25)))
        assert (realized>=low-1e-12).all() and (realized<=high+1e-12).all()
        assert np.all(utility(A,B,alpha,.6)>=utility(A,B,alpha,.4))
    # At alpha=0, intervals recover exactly the prior implementation's V0.
    old=pd.read_csv(ROOT/'results/task4_real/rankings.csv').set_index('city')
    assert np.allclose(base*100,old.loc[names,'V0_score'])
    summary={'scope':'analytic omitted-dimension sensitivity, NOT observed education or youth scores',
             'baseline_winner':names[a],'observed_weights':w.tolist(),
             'first_tie_alpha':float(th.iloc[0].tie_alpha),'first_challenger':th.iloc[0].challenger,
             'unknown_utility_assumptions':'independent city-wise intervals [0,1]; no population probabilities',
             'selected_alpha_results':[d for d in diagnostics if d['alpha'] in [0,.05,.1,.2,.3,.4]],
             'checks':'all 24 analytic roots matched numerical roots; crossing directions, endpoint containment, monotonicity and V0 recovery passed'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(13,6))
    xx=np.linspace(0,.4,401)
    low=np.array([utility(A[a],B[a],x,0) for x in xx])*100
    high=np.array([utility(A[a],B[a],x,1) for x in xx])*100
    axes[0].fill_between(xx*100,low,high,alpha=.2,color='#087e8b',label='Copenhagen admissible range')
    axes[0].plot(xx*100,low,color='#087e8b',label='Copenhagen lower bound')
    axes[0].plot(xx*100,[utility(A[first],B[first],x,1)*100 for x in xx],color='#d1495b',label='Dubai upper bound')
    root=summary['first_tie_alpha'];axes[0].axvline(root*100,color='black',ls='--')
    axes[0].set(xlabel='Total weight of missing criteria (%)',ylabel='TOPSIS score',title=f'First possible reversal: {root*100:.2f}%')
    axes[0].legend(fontsize=8)
    chosen=ranges[np.isclose(ranges.alpha,.2)].sort_values(['best_attainable_rank','worst_attainable_rank']).head(12)
    for k,(_,r) in enumerate(chosen.iterrows()):
        axes[1].plot([r.best_attainable_rank,r.worst_attainable_rank],[k,k],color='#087e8b',lw=3,marker='o')
    axes[1].set_yticks(range(len(chosen)),chosen.city);axes[1].invert_yaxis()
    axes[1].set(xlabel='Attainable rank (individual city bounds)',title='Missing criteria weight = 20%')
    fig.suptitle('Stable preferences do not certify omitted criteria\nReal observed proxies; missing youth utilities are unknown bounds, not data')
    fig.tight_layout();fig.savefig(OUT/'missing_dimension_bounds.png',dpi=180);plt.close(fig)
    print(json.dumps(summary,indent=2));print(pd.DataFrame(bound_checks).to_string(index=False))

if __name__=='__main__':main()
