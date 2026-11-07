"""Conditional demographic union lower bounds with cross-record label budgets."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_cohort_outcomes import scenario_bounds,outcome_feasible


def partition_union_lower(all_lower,group_lowers,excess_labels=0):
    """Excess labels = sum over persons max(number of distinct labels - 1,0)."""
    values=np.asarray([all_lower,*group_lowers,excess_labels],float)
    if not np.isfinite(values).all() or np.any(values<0) or np.any(values!=np.floor(values)):
        raise ValueError('Finite nonnegative integer counts and budget required')
    return max(int(all_lower),sum(int(x) for x in group_lowers)-int(excess_labels))


def main():
    source=ROOT/'data/task4_v19_phoenix_partitions';s=json.loads((source/'summary.json').read_text())
    witnesses=pd.read_csv(source/'witnesses.csv');race=witnesses[witnesses.partition=='race_ethnicity']
    g=race[race.metric=='graduates_lower'].lower.tolist();f=race[race.metric=='nongraduates_lower'].lower.tolist()
    lo,hi=scenario_bounds()['phoenix_nyc2024'];i=CITIES.index('Phoenix')
    assert abs(lo[i,-1]-s['previous_quality_lower'])<1e-14 and abs(hi[i,-1]-s['previous_quality_upper'])<1e-14
    scenarios=[('previous_unrestricted',None),('stable_labels',0),('label_budget_16',16),('label_budget_100',100),('label_budget_401',401)]
    frames=[];rows=[]
    for label,budget in scenarios:
        l,h=lo.copy(),hi.copy()
        gl=s['previous_unique_graduates_lower'];fl=s['previous_unique_nongraduates_lower']
        if budget is not None:
            gl=partition_union_lower(gl,g,budget);fl=partition_union_lower(fl,f,budget)
        l[i,-1]=gl/(gl+s['state_nongraduates']);h[i,-1]=s['state_graduates']/(s['state_graduates']+fl)
        assert np.all(l>=lo) and np.all(h<=hi)
        if budget==401:np.testing.assert_array_equal(l,lo);np.testing.assert_array_equal(h,hi)
        for beta in [0,.05,.1,.2]:
            frame,d=summarize(l,h,np.r_[(1-beta)*weights(),beta]);frame['scenario']=label;frame['outcome_weight']=beta;frames.append(frame)
            possible=sum(outcome_feasible(h[k],l[np.arange(len(l))!=k],beta)['possible'] for k in range(len(l)))
            r=frame.iloc[i];rows.append(dict(scenario=label,excess_label_budget_each_status=budget,outcome_weight=beta,graduates_lower=gl,nongraduates_lower=fl,quality_lower=l[i,-1],quality_upper=h[i,-1],phoenix_decision_rank=int(r.decision_rank),phoenix_score_width=float(r.score_upper-r.score_lower),mean_score_width=float((frame.score_upper-frame.score_lower).mean()),possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=possible,minimax_regret=d['minimax_regret']))
    out=ROOT/'results/task4_v19_partition_outcomes';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    hashes=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [source/'summary.json',source/'witnesses.csv',ROOT/'results/task4_v18_cohort_outcomes/summary.json']]
    payload=dict(main_admitted=False,label_consistency_observed=False,baseline_matrix_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),sources=hashes,scenarios=rows)
    (out/'summary.json').write_text(json.dumps(payload,indent=2)+'\n');print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
