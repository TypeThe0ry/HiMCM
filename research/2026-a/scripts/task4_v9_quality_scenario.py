"""Conditional graduation outcome scenario; does not modify main evidence."""
import json
import numpy as np
import pandas as pd
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,weights,summarize

def main():
    p=ROOT/'data/task4_v9_phoenix';s=json.loads((p/'expanded_bounds_summary.json').read_text())
    state=[r for r in json.loads((p/'state_graduation_2025.json').read_text()) if r['studentGroupDescription']=='All'][0]
    n=s['known_cohort'];gl=s['graduates_lower'];gh=s['graduates_upper'];gs=state['numGraduated'];fs=state['numInCohort']-gs
    ql=gl/(gl+fs);qh=gs/(gs+n-gh)
    assert 0<=ql<=qh<=1 and gh<=gs and n-gl<=fs
    l,h,_=apply_bounds(*baseline(),collect());i=CITIES.index('Phoenix')
    out=ROOT/'results/task4_v9_quality_scenario';out.mkdir(exist_ok=True,parents=True)
    records=[];frames=[]
    for beta in [.05,.1,.2]:
        w=np.r_[(1-beta)*weights(),beta]
        lo=np.column_stack([l,np.zeros(len(l))]);hi=np.column_stack([h,np.ones(len(l))])
        before,d0=summarize(lo,hi,w);lo[i,-1]=ql;hi[i,-1]=qh;after,d1=summarize(lo,hi,w)
        assert np.all(after.score_lower>=before.score_lower-1e-10) and np.all(after.score_upper<=before.score_upper+1e-10)
        for label,f in [('unknown_outcome',before),('conditional_margin_bounds',after)]:
            f['scenario']=label;f['outcome_weight']=beta;frames.append(f)
        records.append(dict(outcome_weight=beta,before_champions=int(before.possible_champion.sum()),after_champions=int(after.possible_champion.sum()),phoenix_width_before=float(before.iloc[i].score_upper-before.iloc[i].score_lower),phoenix_width_after=float(after.iloc[i].score_upper-after.iloc[i].score_lower),phoenix_rank_before=int(before.iloc[i].decision_rank),phoenix_rank_after=int(after.iloc[i].decision_rank),changed_ranks=int((before.decision_rank!=after.decision_rank).sum())))
    pd.concat(frames).to_csv(out/'rank_comparison.csv',index=False)
    summary=dict(main_admission=False,assumption='Observed school cohorts are disjoint subsets of the same statewide adjusted cohort; historical location/type alignment remains unverified',quality_lower=ql,quality_upper=qh,comparisons=records)
    (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
