"""Fixed-criterion, evidence-bounded TOPSIS. Offline, no imputation prior."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_interval_decision import interval_decision, voi_1d
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results/task4_v5'
# name, benefit, anchor, main/auxiliary
SPEC = [('homicide_rate',False,2,True),('pm25',False,15,True),
 ('cost_living_index',False,100,True),('price_income_ratio',False,10,True),
 ('upper_secondary_ptr',False,15,True),('research_he_density',True,1,True),
 ('public_transport_density',True,50,False),('travel',True,1,True),
 ('fixed_broadband_mbps',True,100,True),('public_pool_density',True,1,False)]
CITIES = pd.read_csv(ROOT/'data/city_candidates_team_25.csv').city.tolist()
NAMES = [s[0] for s in SPEC]

def weights(aux=.1):
    return np.array([(1-aux)/8 if s[3] else aux/2 for s in SPEC])

def score(z,w):
    good = np.sqrt(((1-z)**2*w).sum(axis=1))
    bad = np.sqrt((z*z*w).sum(axis=1))
    return 100*bad/(good+bad)

def build(after=True, scale=1, strict='conditional'):
    lo=np.zeros((25,10)); hi=np.ones((25,10)); audit=[]
    for directory in ['core','air','education','resources']:
        frame=pd.read_csv(ROOT/f'data/task4_v5_{directory}/observations.csv')
        for r in frame.to_dict('records'):
            name=r['indicator']; city=r['city']
            if name not in NAMES or city not in CITIES: continue
            if not after and name!='price_income_ratio': continue
            status=str(r['status'])
            if status.startswith(('missing','scope_mismatch')) or not np.isfinite(float(r['value'])): continue
            if strict=='no_homicide' and name=='homicide_rate': continue
            if strict in ('no_air','strict_scope') and name=='pm25': continue
            if strict in ('no_education','strict_scope') and name=='upper_secondary_ptr': continue
            if strict=='strict_scope' and name in ('public_transport_density','research_he_density'): continue
            if strict=='recent_air' and name=='pm25':
                if float(r['year'])<2023 or not float(r.get('temporal_coverage_percent',np.nan))>=75: continue
            i=CITIES.index(city); j=NAMES.index(name); _,benefit,a,_=SPEC[j]
            x=float(r['value']); assert x>=0
            u=x/(scale*a+x) if benefit else scale*a/(scale*a+x)
            partial=str(r.get('lower_bound_only',False)).lower()=='true'
            assert not partial or benefit
            lo[i,j]=u; hi[i,j]=1 if partial else u
            audit.append(dict(r,utility_lower=lo[i,j],utility_upper=hi[i,j]))
    travel=pd.read_csv(ROOT/'results/task4_school_revision/admitted_bounds.csv').set_index('city')
    for i,c in enumerate(CITIES):
        lo[i,7]=travel.loc[c,'travel_lower']; hi[i,7]=travel.loc[c,'travel_upper']
    # Exploratory uncertainty, NOT a design-based CI; same interval in both arms.
    boot=pd.read_csv(ROOT/'data/task4_school_commute_extra/melbourne_exploratory_bootstrap.csv')
    r=boot[(boot.group=='secondary_15_19')&(boot.statistic=='mean_exp_utility_tau30')].iloc[0]
    i=CITIES.index('Melbourne'); lo[i,7]=r.exploratory_cluster_bootstrap_p025; hi[i,7]=r.exploratory_cluster_bootstrap_p975
    for c in ['New York','Singapore','Melbourne']:
        i=CITIES.index(c)
        audit.append(dict(city=c,indicator='travel',value=np.nan,year={'New York':'2013–14','Singapore':'2020','Melbourne':'2024–25'}[c],
            source_url='See results/task4_school_revision/admitted_bounds.csv and data/task4_school_commute_extra/',
            scope={'New York':'Grade 9; Jensen bound from reported mean; old school geography',
                   'Singapore':'Student strata; unknown mixture weights; census travel intervals',
                   'Melbourne':'VISTA secondary age15–19; household bootstrap; NOT design-based CI'}[c],
            status='inherited_actual_student_travel_conditional',utility_lower=lo[i,7],utility_upper=hi[i,7]))
    return lo,hi,audit

def summarize(lo,hi,w):
    a,b=score(lo,w),score(hi,w); d=interval_decision(a,b)
    frame=pd.DataFrame(dict(city=CITIES,score_lower=a,score_upper=b,
        best_rank=d['best_rank'],worst_rank=d['worst_rank'],possible_champion=d['possible_champion'],
        necessary_champion=d['necessary_champion'],max_regret=d['max_regret']))
    # This ranks decisions by worst-case regret, not identified city performance.
    frame['decision_rank']=frame.max_regret.rank(method='min').astype(int)
    return frame,d

def main():
    OUT.mkdir(parents=True,exist_ok=True); w=weights()
    l0,h0,_=build(False); l1,h1,audit=build()
    assert np.all(l1>=l0-1e-12) and np.all(h1<=h0+1e-12)
    assert np.isclose(w.sum(),1) and np.all(l1<=h1)
    before,d0=summarize(l0,h0,w); after,d1=summarize(l1,h1,w)
    before.to_csv(OUT/'before.csv',index=False); after.to_csv(OUT/'after.csv',index=False)
    pd.DataFrame(audit).to_csv(OUT/'source_admission.csv',index=False)
    rows=[]
    for i,c in enumerate(CITIES):
        for j,n in enumerate(NAMES): rows.append(dict(city=c,indicator=n,before_lower=l0[i,j],before_upper=h0[i,j],after_lower=l1[i,j],after_upper=h1[i,j],weight=w[j]))
    pd.DataFrame(rows).to_csv(OUT/'utility_bounds.csv',index=False)
    comparison=before[['city','decision_rank','best_rank','worst_rank']].merge(after,on='city',suffixes=('_before','_after'))
    comparison['decision_rank_change']=comparison.decision_rank_before-comparison.decision_rank_after
    comparison.to_csv(OUT/'rank_changes.csv',index=False)
    sensitivity=[]
    for scale in [.5,1,2]:
        for aux in [.05,.1,.2]:
            for strict in ['conditional','no_air','recent_air','no_education','strict_scope','no_homicide']:
                l,h,_=build(scale=scale,strict=strict); f,d=summarize(l,h,weights(aux))
                sensitivity.append(dict(anchor_scale=scale,aux_weight=aux,scope=strict,possible_champions=int(d['possible_champion'].sum()),minimax_regret=d['minimax_regret'],choices='|'.join(CITIES[i] for i in d['minimax_choices'])))
    pd.DataFrame(sensitivity).to_csv(OUT/'sensitivity.csv',index=False)
    voi=[]
    for i,c in enumerate(CITIES):
        for j,n in enumerate(NAMES):
            if h1[i,j]-l1[i,j]<1e-10: continue
            def callback(x):
                l=l1.copy();h=h1.copy(); l[i,j]=h[i,j]=x
                return score(l,w),score(h,w)
            v=voi_1d(callback,i,l1[i,j],h1[i,j],baseline=(score(l1,w),score(h1,w)))
            voi.append(dict(city=c,indicator=n,**v))
    pd.DataFrame(voi).sort_values(['guaranteed_gain','best_possible_gain'],ascending=False).to_csv(OUT/'acquisition_priority.csv',index=False)
    summary=dict(before_possible=int(d0['possible_champion'].sum()),after_possible=int(d1['possible_champion'].sum()),
        before_mean_width=float((before.score_upper-before.score_lower).mean()),after_mean_width=float((after.score_upper-after.score_lower).mean()),
        before_minimax=d0['minimax_regret'],after_minimax=d1['minimax_regret'],
        before_choices=[CITIES[i] for i in d0['minimax_choices']],after_choices=[CITIES[i] for i in d1['minimax_choices']],
        kendall_decision_rank=float(kendalltau(before.decision_rank,after.decision_rank).statistic),
        informative_before=int(np.sum(h0-l0<1-1e-12)),informative_after=int(np.sum(h1-l1<1-1e-12)),
        conditional_point_cells=int(np.sum(h1-l1<1e-12)))
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    order=np.argsort(after.decision_rank.to_numpy()); y=np.arange(25)
    fig,ax=plt.subplots(figsize=(10,9))
    for frame,offset,color,label in [(before,-.15,'#aaa','Before additional evidence'),(after,.15,'#1679a4','After additional evidence')]:
        a=frame.score_lower.to_numpy()[order];b=frame.score_upper.to_numpy()[order]
        ax.hlines(y+offset,a,b,color=color,lw=3,label=label)
    ax.set_yticks(y,[CITIES[i] for i in order]);ax.invert_yaxis();ax.set_xlim(0,100)
    ax.set_xlabel('Conditional TOPSIS score interval (0–100)');ax.legend(loc='lower right')
    ax.set_title('Same ten criteria, same weights; unknown evidence stays bounded')
    fig.tight_layout();fig.savefig(OUT/'score_intervals.png',dpi=170);plt.close(fig)
    print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
