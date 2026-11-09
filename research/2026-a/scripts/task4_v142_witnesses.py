"""Construct deterministic interior witnesses, not observed/imputed city data."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
from task4_user_v136_revision import revised_bounds
from task4_v5_model import ROOT,NAMES,score,weights
OUT=ROOT/'results/task4_v142_witnesses'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inputs():
    paths={}
    for name,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256')]:
        paths.update(json.loads((ROOT/name).read_text())[key]);paths[name]=sha(ROOT/name)
    for name in ['design/task4_user_current_model.json','design/task4_user_v137_extensions.json','scripts/task4_v142_witnesses.py','scripts/task4_v5_model.py']:
        paths[name]=sha(ROOT/name)
    return paths

def main():
    frozen=inputs()
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();uncertain=lo<hi
    assert lo.shape==(16,10) and int(uncertain.sum())==48 and int((~uncertain).sum())==112
    assert json.loads((ROOT/'design/task4_user_current_model.json').read_text())['version']=='V136'
    cells=[];ranks=[];cases=[]
    for i,target in enumerate(cities):
        u=lo+.05*(hi-lo);u[i]=lo[i]+.95*(hi[i]-lo[i])
        np.testing.assert_array_equal(u[~uncertain],lo[~uncertain])
        assert np.all(u[uncertain]>lo[uncertain]) and np.all(u[uncertain]<hi[uncertain])
        for k,city in enumerate(cities):
            for j,indicator in enumerate(NAMES):cells.append(dict(target=target,city=city,indicator=indicator,utility=float(u[k,j]),original_lower=float(lo[k,j]),original_upper=float(hi[k,j])))
        for reference,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            scores=score(u,w);order=np.argsort(-scores,kind='stable');assert order[0]==i
            gap=float(scores[i]-np.delete(scores,i).max());assert gap>0
            runner=int(order[1]);cases.append(dict(target=target,weight_reference=reference,winner=cities[order[0]],winner_score=float(scores[i]),runner_up=cities[runner],runner_up_score=float(scores[runner]),strict_margin=gap))
            for rank,k in enumerate(order,1):ranks.append(dict(target=target,weight_reference=reference,city=cities[k],rank=rank,score=float(scores[k])))
    OUT.mkdir(exist_ok=True)
    for name,rows in [('utility_completions',cells),('scores',ranks),('cases',cases)]:pd.DataFrame(rows).to_csv(OUT/(name+'.csv'),index=False)
    minima={r:min((x for x in cases if x['weight_reference']==r),key=lambda x:x['strict_margin']) for r in ['fixed','equal']}
    summary=dict(version='V142 constructive validation on V136 / V137 evidence',distinct_completions=16,weight_cases=32,utility_entries_per_completion=160,point_entries_preserved_per_completion=112,uncertain_entries_strictly_inside_per_completion=48,other_city_interval_fraction=.05,target_city_interval_fraction=.95,all16_targets_strictly_first_under_both_weights=True,minimum_strict_margin_by_weight={r:x['strict_margin'] for r,x in minima.items()},minimum_margin_target_by_weight={r:x['target'] for r,x in minima.items()},changes_primary_model=False,changes_primary_data=False,interpretation='Separate mathematical feasibility witnesses in the declared utility rectangle; not observations, imputations, probability draws, forecasts or proof of joint physical attainability',source_sha256=frozen)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    print(json.dumps({k:v for k,v in summary.items() if k!='source_sha256'},indent=2))
if __name__=='__main__':main()
