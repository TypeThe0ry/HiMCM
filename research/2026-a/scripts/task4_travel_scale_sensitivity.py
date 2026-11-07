"""Simple conservative sensitivity to the travel time scale, without imputation.

Input [L,H] bounds E[exp(-T/30)]. Jensen plus X^p<=X (or >=X)
propagates those bounds to another scale. This deliberately uses only the mean
interval; it is not an exact re-extraction of every available individual diary.
"""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_roster_coverage_comparison import current_bounds
from task4_continuous_preferences import feasible_preferences


def mean_utility_bounds(lower,upper,tau,base_tau=30.):
    lower,upper=np.asarray(lower,float),np.asarray(upper,float)
    if (lower.shape!=upper.shape or not np.isfinite(lower).all() or not np.isfinite(upper).all()
            or np.any(lower<0) or np.any(upper>1) or np.any(lower>upper)
            or not np.isfinite(tau) or not np.isfinite(base_tau) or tau<=0 or base_tau<=0):
        raise ValueError('Finite ordered utility bounds and positive time scales required')
    p=base_tau/tau
    return (lower**p,upper.copy()) if p>=1 else (lower.copy(),upper**p)


def main():
    lo,hi=current_bounds();j=NAMES.index('travel');base,_=summarize(lo,hi,weights())
    reference=pd.read_csv(ROOT/'results/task4_v23_roster_coverage/ranks.csv')
    reference=reference[(reference.model=='v16_ten_criteria')&(reference.nyc_age_scope=='under19')&(reference.scenario=='both_sampling_envelope')]
    assert reference.city.tolist()==CITIES
    np.testing.assert_allclose(base[['score_lower','score_upper','decision_rank']],reference[['score_lower','score_upper','decision_rank']],rtol=0,atol=1e-11)
    frames=[];rows=[];travel=[]
    for tau in [15,20,30,45,60]:
        l,h=lo.copy(),hi.copy();l[:,j],h[:,j]=mean_utility_bounds(lo[:,j],hi[:,j],tau)
        np.testing.assert_array_equal(l[:,np.arange(len(NAMES))!=j],lo[:,np.arange(len(NAMES))!=j])
        np.testing.assert_array_equal(h[:,np.arange(len(NAMES))!=j],hi[:,np.arange(len(NAMES))!=j])
        unknown=(lo[:,j]==0)&(hi[:,j]==1)
        assert np.all(l[unknown,j]==0) and np.all(h[unknown,j]==1)
        f,d=summarize(l,h,weights());f['tau_minutes']=tau;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        rows.append(dict(tau_minutes=tau,minimax_choices=[CITIES[k] for k in d['minimax_choices']],
            minimax_regret=d['minimax_regret'],fixed_possible_champions=int(f.possible_champion.sum()),
            continuous_alpha_possible_champions=possible,changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),
            kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            mean_score_width=float((f.score_upper-f.score_lower).mean()),
            selected_ranks={c:int(f.iloc[CITIES.index(c)].decision_rank) for c in ['Singapore','Melbourne','Sao Paulo','New York','Mexico City','Phoenix']}))
        travel.extend(dict(city=c,tau_minutes=tau,lower=float(l[k,j]),upper=float(h[k,j])) for k,c in enumerate(CITIES))
    out=ROOT/'results/task4_v25_travel_scale';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(travel).to_csv(out/'travel_bounds.csv',index=False)
    source=ROOT/'results/task4_v23_roster_coverage/utility_bounds.csv'
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,new_observations=0,
        baseline='V23 ten criteria, NYC under19, Melbourne person-weight sampling envelope',
        alpha_fixed_for_ranks=.1,alpha_range_for_possible_champions=[.05,.2],base_tau_minutes=30,
        method='Conservative mean-interval propagation; not exact diary re-estimation or new data. Sampling and source conditions inherited.',
        source_path=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        matrix_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),scenarios=rows),indent=2)+'\n')
    print(pd.DataFrame([{k:v for k,v in r.items() if k!='continuous_alpha_possible_champions'} for r in rows]).to_string(index=False))

if __name__=='__main__':main()
