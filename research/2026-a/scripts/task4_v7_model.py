"""V7: verified microdata travel and direction-aware partial coverage bounds."""
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,build,weights,summarize
from task4_v6_model import inputs,admit_observations,admit_travel
from task4_champion_acquisition import certificates,elimination_threshold
OUT=ROOT/'results/task4_v7'


def baseline():
    l,h,_=build();l,h,_=admit_observations(l,h,inputs());l,h,_=admit_travel(l,h)
    return l,h


def collect():
    frames=[]
    for source in ['core','istanbul','mexico']:
        p=ROOT/f'data/task4_v7_{source}/bounds.csv'
        if p.exists():
            f=pd.read_csv(p);f['source_package']=source;frames.append(f)
    return pd.concat(frames,ignore_index=True) if frames else pd.DataFrame()


def apply_bounds(l,h,rows,mode='all'):
    l=l.copy();h=h.copy();audit=[]
    accepted={'conditional_manual_primary_homicide_rate','conditional_partial_jurisdiction_risk_bound',
              'conditional_official_complete_he_aggregate','observed_official_microdata_school_travel_bound'}
    for r in rows.to_dict('records'):
        status=str(r.get('status','')); ok=status in accepted
        if mode=='no_manual' and ('manual' in status or 'manual' in str(r.get('extraction','')).lower()):ok=False
        if r.get('indicator')=='travel' and not all(str(r.get(key,False)).strip().lower()=='true' for key in ['mapping_robust','raw_data_archived']):ok=False
        if mode=='travel_only' and r.get('indicator')!='travel':ok=False
        if mode=='no_travel' and r.get('indicator')=='travel':ok=False
        if not ok:
            audit.append(dict(r,admitted=False));continue
        i=CITIES.index(r['city']);j=NAMES.index(r['indicator'])
        a=float(r['utility_lower']);b=float(r['utility_upper'])
        if not (np.isfinite(a) and np.isfinite(b) and 0<=a<=b<=1):raise ValueError('Invalid evidence endpoints')
        if max(l[i,j],a)>min(h[i,j],b)+1e-12:raise ValueError('Conflicting evidence requires reconciliation')
        l[i,j]=max(l[i,j],a);h[i,j]=min(h[i,j],b)
        audit.append(dict(r,admitted=True))
    return l,h,audit


def main():
    OUT.mkdir(parents=True,exist_ok=True);l0,h0=baseline();l,h,audit=apply_bounds(l0,h0,collect())
    w=weights();before,d0=summarize(l0,h0,w);after,d1=summarize(l,h,w)
    assert np.all(l>=l0-1e-12) and np.all(h<=h0+1e-12)
    before.to_csv(OUT/'before_v6.csv',index=False);after.to_csv(OUT/'after_v7.csv',index=False)
    pd.DataFrame(audit).to_csv(OUT/'source_admission.csv',index=False)
    comparison=before[['city','decision_rank','score_lower','score_upper']].merge(after,on='city',suffixes=('_before','_after'))
    comparison['decision_rank_change']=comparison.decision_rank_before-comparison.decision_rank_after
    comparison.to_csv(OUT/'rank_changes.csv',index=False)
    pd.DataFrame([dict(city=c,indicator=n,before_lower=l0[i,j],before_upper=h0[i,j],after_lower=l[i,j],after_upper=h[i,j])
                  for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)]).to_csv(OUT/'utility_bounds.csv',index=False)
    for label,ll,hh in [('before',l0,h0),('after',l,h)]:
        r,b=certificates(ll,hh,w,NAMES,CITIES)
        pd.DataFrame(r).to_csv(OUT/f'acquisition_certificate_{label}.csv',index=False)
        pd.DataFrame(b).to_csv(OUT/f'minimal_bundles_{label}.csv',index=False)
    thresholds=[]
    for i,c in enumerate(CITIES):
        for j,n in enumerate(NAMES):
            if h[i,j]>l[i,j]+1e-12:
                t=elimination_threshold(l,h,w,i,j)
                thresholds.append(dict(city=c,indicator=n,utility_strict_cutoff=t,single_cell_can_eliminate=t is not None))
    pd.DataFrame(thresholds).to_csv(OUT/'single_cell_elimination_thresholds.csv',index=False)
    sensitivity=[]
    for aux in [.05,.1,.2]:
        for mode in ['all','no_manual','travel_only','no_travel']:
            ll,hh,_=apply_bounds(l0,h0,collect(),mode);f,d=summarize(ll,hh,weights(aux))
            sensitivity.append(dict(auxiliary_weight=aux,evidence_mode=mode,possible_champions=int(d['possible_champion'].sum()),
                                    minimax_regret=d['minimax_regret'],choices='|'.join(CITIES[k] for k in d['minimax_choices'])))
    pd.DataFrame(sensitivity).to_csv(OUT/'sensitivity.csv',index=False)
    s=dict(before_possible=int(d0['possible_champion'].sum()),after_possible=int(d1['possible_champion'].sum()),
           before_mean_width=float((before.score_upper-before.score_lower).mean()),after_mean_width=float((after.score_upper-after.score_lower).mean()),
           before_minimax=d0['minimax_regret'],after_minimax=d1['minimax_regret'],
           before_choices=[CITIES[i] for i in d0['minimax_choices']],after_choices=[CITIES[i] for i in d1['minimax_choices']],
           kendall_decision_rank=float(kendalltau(before.decision_rank,after.decision_rank).statistic),
           changed_cells=int(np.sum((l>l0+1e-12)|(h<h0-1e-12))),
           informative_after=int(np.sum(h-l<1-1e-12)))
    (OUT/'summary.json').write_text(json.dumps(s,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    selected=['Phoenix','Istanbul','Mexico City','Singapore'];fig,axes=plt.subplots(1,2,figsize=(11,4.5))
    for off,f,color,label in [(-.14,before,'#aaa','V6'),(.14,after,'#197d91','V7')]:
        f=f.set_index('city').loc[selected];axes[0].hlines(np.arange(4)+off,f.score_lower,f.score_upper,color=color,lw=5,label=label)
    axes[0].set_yticks(range(4),selected);axes[0].invert_yaxis();axes[0].set_xlim(0,100);axes[0].set_xlabel('TOPSIS score interval');axes[0].legend(loc='lower right')
    i=CITIES.index('Mexico City');axes[1].hlines([0,1],[l0[i,7],l[i,7]],[h0[i,7],h[i,7]],lw=7,color=['#aaa','#197d91'])
    axes[1].set_yticks([0,1],['V6 chart bounds','V7 microdata bounds']);axes[1].set_xlim(0,1);axes[1].set_xlabel('Student travel utility interval');axes[1].set_ylim(-.6,1.6)
    fig.suptitle('Measured evidence updates; weights and missing cells preserved');fig.tight_layout();fig.savefig(OUT/'evidence_updates.png',dpi=170);plt.close(fig)
    print(json.dumps(s,indent=2))
if __name__=='__main__':main()
