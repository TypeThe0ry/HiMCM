"""Historical/conditional Santiago commute scenarios, never main observations."""
import json,sys
import pandas as pd
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,weights,summarize

def main():
    chain='--chain' in sys.argv
    filename='trip_chain_summary.json' if chain else 'conditional_commute_bounds.json'
    rows=json.loads((ROOT/'data/task4_v10_santiago'/filename).read_text())
    l,h,_=apply_bounds(*baseline(),collect());i=CITIES.index('Santiago');before,_=summarize(l,h,weights());result=[];frames=[]
    for r in rows:
        ll=l.copy();hh=h.copy();ll[i,7]=r['utility_lower'];hh[i,7]=r['utility_upper'];f,_=summarize(ll,hh,weights());f['scenario']=r['scope'];frames.append(f)
        result.append(dict(scope=r['scope'],possible_champions=int(f.possible_champion.sum()),changed_ranks=int((before.decision_rank!=f.decision_rank).sum()),santiago_rank_before=int(before.iloc[i].decision_rank),santiago_rank_after=int(f.iloc[i].decision_rank),score_width_before=float(before.iloc[i].score_upper-before.iloc[i].score_lower),score_width_after=float(f.iloc[i].score_upper-f.iloc[i].score_lower),main_admitted=False))
    out=ROOT/('results/task4_v10_santiago_chain' if chain else 'results/task4_v10_santiago');out.mkdir(parents=True,exist_ok=True);pd.concat(frames).to_csv(out/'scenario_ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
