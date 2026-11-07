"""Recompute the unchanged V23 model after V28 source-scope audits.

The new sources supply no admitted city observations. Keep their audit trail
separate from utility bounds and verify against the preceding actual ranking.
"""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_roster_coverage_comparison import current_bounds


def main():
    lo,hi=current_bounds()
    rank,d=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v27_current_acquisition/ranks.csv')
    assert rank.city.tolist()==prior.city.tolist()
    for col in ['score_lower','score_upper','decision_rank','max_regret']:
        np.testing.assert_allclose(rank[col],prior[col],rtol=0,atol=1e-12)
    for city in ['Cape Town','Istanbul','Jakarta']:
        i=CITIES.index(city)
        assert lo[i,7]==0 and hi[i,7]==1,city
    out=ROOT/'results/task4_v28_source_scope';out.mkdir(parents=True,exist_ok=True)
    rank.to_csv(out/'ranks.csv',index=False)
    paths=sorted(p for folder in ['task4_v28_cape_town','task4_v28_istanbul','task4_v28_jakarta'] for p in (ROOT/'data'/folder).rglob('*') if p.is_file())
    summary=dict(new_admitted_observations=0,rank_changes=0,possible_champions=int(rank.possible_champion.sum()),
        minimax_choice=[CITIES[k] for k in d['minimax_choices']],phoenix_rank=int(rank.loc[rank.city=='Phoenix','decision_rank'].iloc[0]),
        input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        validation='Recomputed current_bounds; V27 scores and ranks match at absolute tolerance1e-12. Three audited cities retain travel [0,1].',
        source_audits=[dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths])
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print({k:v for k,v in summary.items() if k!='source_audits'})

if __name__=='__main__':main()
