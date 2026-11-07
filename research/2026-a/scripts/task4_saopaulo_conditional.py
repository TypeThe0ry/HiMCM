"""Run OD2023 mirror evidence under explicit municipal and metro interpretations."""
import json, sys
import numpy as np
import pandas as pd
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_continuous_preferences import feasible_preferences

def main():
    sampling='--sampling' in sys.argv
    filename='sampling_sensitivity.json' if sampling else 'commute_summary.json'
    source=json.loads((ROOT/'data/task4_v10_saopaulo'/filename).read_text())
    l,h,_=apply_bounds(*baseline(),collect());i=CITIES.index('Sao Paulo')
    before,_=summarize(l,h,weights());frames=[];summaries=[]
    for scope,r in source['scopes'].items():
        ll=l.copy();hh=h.copy();ll[i,7]=r['utility_lower'];hh[i,7]=r['utility_upper']
        assert np.all(ll<=hh)
        f,_=summarize(ll,hh,weights());f['scenario']=scope;frames.append(f)
        continuous=[CITIES[k] for k in range(len(CITIES)) if feasible_preferences(hh[k],ll[np.arange(len(ll))!=k])['possible']]
        summaries.append(dict(scope=scope,main_admitted=False,possible_before=int(before.possible_champion.sum()),possible_after=int(f.possible_champion.sum()),continuous_possible=len(continuous),continuous_possible_cities=continuous,changed_ranks=int((before.decision_rank!=f.decision_rank).sum()),rank_before=int(before.iloc[i].decision_rank),rank_after=int(f.iloc[i].decision_rank),score_width_before=float(before.iloc[i].score_upper-before.iloc[i].score_lower),score_width_after=float(f.iloc[i].score_upper-f.iloc[i].score_lower)))
    out=ROOT/('results/task4_v10_saopaulo_sampling' if sampling else 'results/task4_v10_saopaulo');out.mkdir(parents=True,exist_ok=True)
    before.to_csv(out/'baseline_ranks.csv',index=False);pd.concat(frames).to_csv(out/'scenario_ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(summaries,indent=2)+'\n');print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
