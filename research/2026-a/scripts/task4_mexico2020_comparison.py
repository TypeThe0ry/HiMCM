"""Separate source-year, age-scope and unknown-stage effects; never intersect years."""
import json
import numpy as np
import pandas as pd
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_continuous_preferences import feasible_preferences

def main():
    source=json.loads((ROOT/'data/task4_v15_mexico2020/commute_summary.json').read_text())
    low,high,_=apply_bounds(*baseline(),collect());i=CITIES.index('Mexico City');w=weights()
    before,_=summarize(low,high,w);results=[];frames=[]
    for scope,r in source['scopes'].items():
        for membership in [False,True]:
            prefix='membership_' if membership else ''
            l,h=low.copy(),high.copy();l[i,7]=r[prefix+'utility_lower'];h[i,7]=r[prefix+'utility_upper']
            # Replacement is intentional:2015 and2020 measure different populations in time.
            frame,_=summarize(l,h,w);name=scope+('_unknown_stage_retained' if membership else '_classified_stage')
            frame['scenario']=name;frames.append(frame)
            continuous=sum(feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible'] for k in range(len(l)))
            results.append(dict(scenario=name,year=2020,stage_reconstruction_conditional=True,age_scope=scope,unknown_stage_retained=membership,old_interval=[float(low[i,7]),float(high[i,7])],new_interval=[float(l[i,7]),float(h[i,7])],interval_nested_in_old=bool(l[i,7]>=low[i,7] and h[i,7]<=high[i,7]),changed_decision_ranks=int((frame.decision_rank!=before.decision_rank).sum()),mexico_rank_before=int(before.iloc[i].decision_rank),mexico_rank_after=int(frame.iloc[i].decision_rank),score_width_before=float(before.iloc[i].score_upper-before.iloc[i].score_lower),score_width_after=float(frame.iloc[i].score_upper-frame.iloc[i].score_lower),possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=int(continuous)))
    out=ROOT/'results/task4_v15_mexico2020';out.mkdir(parents=True,exist_ok=True)
    before.to_csv(out/'baseline_2015_ranks.csv',index=False);pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
if __name__=='__main__':main()
