"""V8 preference audit: fixed evidence, continuous group-weight feasibility."""
import json
import numpy as np
import pandas as pd
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences,robust_exclusion_cutoff,selfcheck


def main():
    selfcheck()
    l,h,_=apply_bounds(*baseline(),collect())
    out=ROOT/'results/task4_v8_preferences';out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for i,c in enumerate(CITIES):
        r=feasible_preferences(h[i],l[np.arange(len(l))!=i])
        rows.append(dict(city=c,**r))
    (out/'continuous_champions.json').write_text(json.dumps(rows,indent=2)+'\n')
    ranks=[]
    for a in [.05,.1,.15,.2]:
        f,_=summarize(l,h,weights(a));f['auxiliary_weight']=a;ranks.append(f)
    pd.concat(ranks).to_csv(out/'rank_sensitivity.csv',index=False)
    i=CITIES.index('Istanbul');j=NAMES.index('travel');u=h[i].copy();u[j]=0
    stress=feasible_preferences(u,l[np.arange(len(l))!=i])
    cutoffs={str(a):robust_exclusion_cutoff(l,h,i,j,a,a) for a in [.05,.1,.15,.2]}
    robust=robust_exclusion_cutoff(l,h,i,j)
    summary=dict(evidence_version='V7 unchanged',new_admitted_cells=0,alpha_range=[.05,.2],
                 continuous_possible=sum(r['possible'] for r in rows),
                 istanbul_travel_zero_hypothetical=stress,istanbul_fixed_alpha_cutoffs=cutoffs,
                 istanbul_robust_travel_cutoff=robust,
                 interpretation='Hypothetical zero is a diagnostic only, never an observed travel value. Weight range is an explicit sensitivity assumption, not estimated preferences.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
