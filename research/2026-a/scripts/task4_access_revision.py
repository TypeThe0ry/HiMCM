"""Population-aware learning accessibility revision using archived source grids.
This measures generic learning-POI proximity, NOT verified high-school admission,
teaching quality, child-specific travel, or after-school opening hours.
"""
from pathlib import Path
import json,zipfile
import numpy as np
import pandas as pd
from scipy.stats import rankdata,kendalltau
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from task4_real_analysis import scores,grid
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data/task4_access';OUT=ROOT/'results/task4_access_revision'
OUT.mkdir(parents=True,exist_ok=True)


def lower_tail(u,p,fraction=.2):
    order=np.argsort(u);v=u[order];mass=p[order]
    target=fraction*mass.sum();before=np.cumsum(mass)-mass
    included=np.clip(target-before,0,mass)
    return float(np.dot(v,included)/target)

def access(t,p,tau=30,lam=.3):
    valid=np.isfinite(t)&(t>0)
    lo=np.where(valid,np.exp(-np.maximum(t,0)/tau),0.)
    hi=np.where(valid,lo,1.)
    mu=float(np.average(lo,weights=p));tail=lower_tail(lo,p)
    qlo=(1-lam)*mu+lam*tail
    qhi=(1-lam)*float(np.average(hi,weights=p))+lam*lower_tail(hi,p)
    return {'mean_utility_lower':mu,'lower_quintile_utility':tail,'q_low':qlo,'q_high':qhi,
            'invalid_population_share':float(p[~valid].sum()/p.sum()),
            'learning_15min_population_share_lower':float(p[valid&(t<=15)].sum()/p.sum()),
            'learning_30min_population_share_lower':float(p[valid&(t<=30)].sum()/p.sum()),
            'mean_minutes_valid_only':float(np.average(t[valid],weights=p[valid])) if valid.any() else None}

def cscore(A,B,unknown_weight=0,y=0):
    dm=np.sqrt(A+unknown_weight*np.asarray(y)**2)
    dp=np.sqrt(B+unknown_weight*(1-np.asarray(y))**2)
    return dm/(dm+dp)

def bounds_rows(names,lo,hi,stage):
    out=[]
    for i,n in enumerate(names):
        others=np.arange(len(names))!=i
        out.append({'city':n,'stage':stage,'score_lower':100*lo[i],'score_upper':100*hi[i],
                    'best_rank':1+int(np.sum(lo[others]>hi[i]+1e-12)),
                    'worst_rank':1+int(np.sum(hi[others]>lo[i]+1e-12)),
                    'possible_champion':bool(hi[i]>=lo[others].max()-1e-12),
                    'necessary_champion':bool(lo[i]>=hi[others].max()-1e-12)})
    return out

def main():
    manifest=json.loads((DATA/'manifest.json').read_text());records=[];arrays={}
    index={r['id']:r for r in json.loads((DATA/'city_index.json').read_text())}
    for row in manifest:
        if row['status']!='downloaded':continue
        with zipfile.ZipFile(DATA/row['file']) as f:d=json.loads(f.read('hexes.geojson'))
        a=np.array([[h['properties'].get(k,np.nan) for k in ['population','c_f','c_b']] for h in d['features']],float)
        assert np.isfinite(a[:,0]).all() and (a[:,0]>=0).all()
        a=a[a[:,0]>0];p=a[:,0];assert p.sum()>0
        arrays[row['city']]=(p,a[:,1],a[:,2]);r=access(a[:,1],p)
        r.update(city=row['city'],source_id=row['source_id'],populated_cells=len(a),
                 retained_population=float(p.sum()),source_index_population=float(index[row['source_id']]['pop']),
                 source_city=index[row['source_id']]['city'])
        records.append(r)
    measures=pd.DataFrame(records).set_index('city')
    measures.to_csv(OUT/'learning_access_measures.csv')
    pilot=pd.read_csv(ROOT/'inputs/team/task4_attachments/pilot_sheet0_table0.csv')
    pilot_access=pilot[['city','country']].join(measures,on='city',how='left',rsuffix='_source')
    assert len(pilot_access)==10 and pilot_access.q_low.notna().all()
    pilot_access['access_only_rank']=rankdata(-pilot_access.q_low,method='min').astype(int)
    pilot_access.sort_values('access_only_rank').to_csv(OUT/'pilot10_access_only.csv',index=False)
    old=pd.read_csv(ROOT/'results/task4_real/normalized_indicators.csv',index_col=0)
    common=old.index.intersection(measures.index,sort=False);z=old.loc[common].to_numpy()
    # All mapped cities retain intervals for invalid cells; no mean imputation.
    point_names=common;zp=old.loc[point_names].to_numpy()
    q=measures.loc[point_names,'q_low'].to_numpy();mean=measures.loc[point_names,'mean_utility_lower'].to_numpy()
    base=scores(zp,np.ones((1,4))*.25)[0]
    def augmented(qq):
        return scores(np.column_stack([zp,qq]),np.array([[.2,.2,.2,.2,.2]]))[0]
    revised=augmented(q);mean_only=augmented(mean)
    q_upper=measures.loc[point_names,'q_high'].to_numpy()
    revised_upper=augmented(q_upper)
    access_bounds=pd.DataFrame(bounds_rows(point_names,revised,revised_upper,'five_proxy_model'))
    access_bounds.to_csv(OUT/'five_proxy_rank_bounds.csv',index=False)
    # Same design weight set and alpha for V1 versus V3 decision-rule comparison.
    w=grid();base_sc=scores(zp,w)
    wr=np.column_stack([.8*w,np.full(len(w),.2)])
    rev_sc=scores(np.column_stack([zp,q]),wr)
    R0=(base_sc.max(axis=1,keepdims=True)-base_sc).max(axis=0)
    upper_sc=scores(np.column_stack([zp,q_upper]),wr)
    R3=np.array([max(0.,float((upper_sc[:,np.arange(len(point_names))!=i].max(axis=1)-rev_sc[:,i]).max())) for i in range(len(point_names))])
    rank=lambda x:rankdata(-x,method='min').astype(int)
    table=pd.DataFrame({'city':point_names,'V0_score':100*base,'V0_rank_common_sample':rank(base),
                        'access_mean_only_score':100*mean_only,'access_mean_only_rank':rank(mean_only),
                        'V3_score_lower':100*revised,'V3_score_upper':100*revised_upper,'V3_rank':rank(revised),'access_q_lower':q,
                        'V1_regret_rank_common_sample':rank(-R0),'V3_regret_rank':rank(-R3),
                        'V1_regret_points':100*R0,'V3_regret_points':100*R3})
    table.sort_values('V3_rank').to_csv(OUT/'point_rankings.csv',index=False)
    # Matched information experiment: 80% old dimensions, 10% observed access,
    # 10% still-unknown school quality/eligibility. Same equation before/after.
    names=old.index.to_numpy();zz=old.to_numpy();A=.8*(zz**2).mean(axis=1);B=.8*((1-zz)**2).mean(axis=1)
    before_lo=cscore(A,B,.2,0);before_hi=cscore(A,B,.2,1)
    qlo=np.array([measures.loc[n,'q_low'] if n in measures.index else 0 for n in names])
    qhi=np.array([measures.loc[n,'q_high'] if n in measures.index else 1 for n in names])
    after_lo=cscore(A+.1*qlo**2,B+.1*(1-qlo)**2,.1,0)
    after_hi=cscore(A+.1*qhi**2,B+.1*(1-qhi)**2,.1,1)
    assert np.all(after_lo>=before_lo-1e-12) and np.all(after_hi<=before_hi+1e-12)
    ranges=pd.DataFrame(bounds_rows(names,before_lo,before_hi,'before_two_unknown')+
                        bounds_rows(names,after_lo,after_hi,'after_access_observed_quality_unknown'))
    ranges.to_csv(OUT/'matched_information_rank_bounds.csv',index=False)
    # Retained uncertainty is varied without claiming a real statistical error model.
    sensitivity=[]
    for tau in [15,30,45]:
      for lam in [0,.3,.6]:
       for mode in ['walk','bike']:
        qq=np.array([access(arrays[n][1 if mode=='walk' else 2],arrays[n][0],tau,lam)['q_low'] for n in point_names])
        ss=augmented(qq)
        sensitivity.append({'tau_minutes':tau,'tail_weight':lam,'mode':mode,'winner':point_names[ss.argmax()],
                            'kendall_vs_main':float(kendalltau(rank(ss),rank(revised)).statistic)})
    pd.DataFrame(sensitivity).to_csv(OUT/'parameter_sensitivity.csv',index=False)
    # Distinguish adding measurement from counting adult commute twice.
    no_commute=scores(np.column_stack([zp[:,:3],q]),np.full((1,4),.25))[0]
    pd.DataFrame({'city':point_names,'rank_without_adult_commute':rank(no_commute),
                  'score_without_adult_commute':100*no_commute}).to_csv(OUT/'commute_ablation.csv',index=False)
    # Assumed proxy error bands, not empirically estimated CIs.
    proxy=[]
    for eps in [0,.1,.2,.3]:
        l=np.maximum(0,qlo-eps);h=np.minimum(1,qhi+eps)
        ll=cscore(A+.1*l*l,B+.1*(1-l)**2,.1,0)
        hh=cscore(A+.1*h*h,B+.1*(1-h)**2,.1,1)
        rr=bounds_rows(names,ll,hh,'stress')
        proxy.append({'assumed_access_utility_error':eps,'possible_champions':[r['city'] for r in rr if r['possible_champion']]})
    (OUT/'proxy_error_stress.json').write_text(json.dumps(proxy,indent=2)+'\n')
    # Mechanism checks: partial population mass at lower-tail cutoff and transfer.
    assert abs(lower_tail(np.array([0.,1.]),np.array([1.,9.]))-.5)<1e-12
    u=np.array([.2,.8]);v=np.array([.3,.7]);p=np.ones(2)
    assert np.mean(u)==np.mean(v) and lower_tail(v,p)>lower_tail(u,p)
    assert np.allclose(scores(zp,np.full((1,4),.25))[0],base)
    summary={'ranked_city_count':len(point_names),'rank_identified_count':int((access_bounds.best_rank==access_bounds.worst_rank).sum()),'point_excluded':list(old.index.difference(point_names)),
             'V0_winner_same_sample':str(point_names[base.argmax()]),'V3_winner':str(point_names[revised.argmax()]),
             'V1_regret_winner':str(point_names[R0.argmin()]),'V3_regret_winner':str(point_names[R3.argmin()]),
             'kendall_V0_V3':float(kendalltau(rank(base),rank(revised)).statistic),
             'ranks_changed':int(np.sum(rank(base)!=rank(revised))),
             'before_possible_champions':ranges[(ranges.stage=='before_two_unknown')&ranges.possible_champion].city.tolist(),
             'after_possible_champions':ranges[(ranges.stage=='after_access_observed_quality_unknown')&ranges.possible_champion].city.tolist(),
             'after_necessary_champions':ranges[(ranges.stage=='after_access_observed_quality_unknown')&ranges.necessary_champion].city.tolist(),
             'mean_score_interval_width_before':float(np.mean(before_hi-before_lo)*100),
             'mean_score_interval_width_after':float(np.mean(after_hi-after_lo)*100),
             'scope':'Modeled generic learning accessibility; all-age retained population, NOT observed high-school travel or education quality',
             'checks':'tail fractional mass, mean-preserving equity transfer, interval nesting, source population validity passed'}
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    fig,ax=plt.subplots(1,2,figsize=(14,7))
    ordered=table.sort_values('V3_rank').head(12)
    yy=np.arange(len(ordered))
    ax[0].barh(yy-.18,ordered.V0_score,height=.35,label='V0: four proxies',color='#a9b9c3')
    ax[0].barh(yy+.18,ordered.V3_score_lower,height=.35,label='V3: learning-access + lower tail',color='#087e8b')
    ax[0].set_yticks(yy,ordered.city);ax[0].invert_yaxis();ax[0].legend(fontsize=8)
    ax[0].set(xlabel='Conditional TOPSIS score',title='Same available-city sample')
    contenders=summary['before_possible_champions']
    for k,n in enumerate(contenders):
        i=int(np.where(names==n)[0][0])
        ax[1].plot([100*before_lo[i],100*before_hi[i]],[k-.13,k-.13],lw=5,color='#a9b9c3')
        ax[1].plot([100*after_lo[i],100*after_hi[i]],[k+.13,k+.13],lw=5,color='#087e8b')
    ax[1].set_yticks(np.arange(len(contenders)),contenders);ax[1].invert_yaxis()
    ax[1].set(xlabel='Score bounds: gray before, teal after',title='School quality still unknown (10% weight)')
    fig.suptitle('Real spatial data, conditional model revision\nLearning POIs are not identified high schools; access is modeled, not student-observed')
    fig.tight_layout();fig.savefig(OUT/'access_revision.png',dpi=180);plt.close(fig)
    print(json.dumps(summary,indent=2));print(table.sort_values('V3_rank').to_string(index=False))

if __name__=='__main__':main()
