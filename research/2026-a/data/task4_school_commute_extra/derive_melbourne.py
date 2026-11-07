"""Reproduce actual-school VISTA teen commute summaries from archived public files.
Not a city census, design-based CI, or exact 14--18 sample. No private records used.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

P=Path(__file__).resolve().parent

def tail(u,w,f=.2):
    o=np.argsort(u); u=u[o];w=w[o];target=f*w.sum()
    m=np.clip(target-(np.cumsum(w)-w),0,w)
    return float(u@m/target)

def stats(t,w):
    u=np.exp(-t/30)
    return np.array([np.average(t,weights=w),np.average(u,weights=w),tail(u,w),
                     .7*np.average(u,weights=w)+.3*tail(u,w),np.average(t<=45,weights=w)])

def main():
    j=pd.read_csv(P/'journey_to_education_vista_2024_2025.csv')
    p=pd.read_csv(P/'person_vista_2024_2025.csv')
    assert p.persid.is_unique and j.jteid.is_unique
    d=j.merge(p[['persid','agegroup','studying']],on='persid',validate='many_to_one')
    assert len(d)==len(j)
    eligible=d[(d.homeregion_ASGS=='Greater Melbourne')&(d.dayType=='Weekday')&(d.studying=='Secondary')]
    assert (eligible.start_loc=='FROM_HOME').all() and (eligible.end_loc=='TO_EDUCATION').all()
    groups={'secondary_15_19':eligible[eligible.agegroup=='15->19'],
            'secondary_all_ages':eligible,
            'secondary_15_19_first_journey':eligible[eligible.agegroup=='15->19'].sort_values('start_time').drop_duplicates('persid')}
    summaries=[];hist=[];boot=[]
    fields=['mean_elapsed_minutes','mean_exp_utility_tau30','lower20_exp_utility_tau30','equity_q_lambda03','share_le45']
    for group,a in groups.items():
        t=a.journey_elapsed_time.to_numpy(float);w=a.journey_weight.to_numpy(float)*7/5
        assert np.isfinite(t).all() and (t>=0).all() and np.isfinite(w).all() and (w>0).all()
        s=stats(t,w)
        row=dict(group=group,city='Melbourne',source_year='2024-25',geography='Greater Melbourne GCCSA',
                 sample_journeys=len(a),sample_persons=a.persid.nunique(),sample_households=a.hhid.nunique(),
                 expanded_weekday_journeys=w.sum(),kish_effective_n=w.sum()**2/(w@w))
        row.update(zip(fields,s));summaries.append(row)
        for tm in sorted(set(t)):
            take=t==tm;hist.append(dict(group=group,elapsed_minutes=tm,unweighted_journeys=int(take.sum()),
                                       expanded_weekday_journeys=float(w[take].sum()),weight_share=float(w[take].sum()/w.sum())))
        # Household-cluster, fixed-weight resampling is exploratory, NOT the
        # provider's replicate-weight design CI. Publish separately, never label official.
        hh,inv=np.unique(a.hhid.to_numpy(),return_inverse=True);rng=np.random.default_rng(20261107)
        reps=[]
        for _ in range(2000):
            counts=np.bincount(rng.integers(0,len(hh),len(hh)),minlength=len(hh))
            ww=w*counts[inv]
            reps.append(stats(t,ww))
        for k,f in enumerate(fields):
            lo,hi=np.quantile(np.asarray(reps)[:,k],[.025,.975])
            boot.append(dict(group=group,statistic=f,estimate=s[k],exploratory_cluster_bootstrap_p025=lo,
                             exploratory_cluster_bootstrap_p975=hi,replicates=2000,
                             method='household resampling; fixed survey weights; NOT design-based confidence interval'))
    pd.DataFrame(summaries).to_csv(P/'melbourne_summary.csv',index=False)
    pd.DataFrame(hist).to_csv(P/'melbourne_elapsed_histogram.csv',index=False)
    pd.DataFrame(boot).to_csv(P/'melbourne_exploratory_bootstrap.csv',index=False)
    print(pd.DataFrame(summaries).to_string(index=False))
    print(pd.DataFrame(boot).query("group=='secondary_15_19'").to_string(index=False))

if __name__=='__main__':main()
