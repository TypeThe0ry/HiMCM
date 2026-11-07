"""Verify new evidence packages and recheck the unchanged V38 city ranking."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_singapore_coverage_revision import singapore_bounds


def main():
    sources=[]
    for folder in ['task4_v40_toronto','task4_v40_education','task4_v40_mumbai']:
        path=ROOT/'data'/folder
        for r in json.loads((path/'manifest.json').read_text()):
            filename=r.get('file',r.get('existing_source_file'))
            if filename is None:continue
            b=(path/filename).read_bytes()
            assert hashlib.sha256(b).hexdigest()==r['sha256']
            if 'bytes' in r:assert len(b)==r['bytes']
        sources.append(dict(folder=folder,manifest_sha256=hashlib.sha256((path/'manifest.json').read_bytes()).hexdigest()))
    lo,hi=singapore_bounds();rank,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v38_singapore/ranks.csv')
    prior=prior[prior.scenario=='expanded_coverage_allocation'].reset_index(drop=True)
    assert prior.city.tolist()==rank.city.tolist()
    for key in ['score_lower','score_upper','decision_rank','max_regret','possible_champion']:
        np.testing.assert_allclose(rank[key],prior[key],rtol=0,atol=1e-12)
    summary=dict(baseline='V38 singapore_bounds',new_admitted_city_cells=0,changed_ranks=0,
        possible_champions=int(rank.possible_champion.sum()),choice=[CITIES[k] for k in decision['minimax_choices']],
        input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),sources=sources,
        distinction='New school-level achievement and district enrollment evidence; missing denominators, grade coverage or spatial scope block city scoring. No hypothetical values written into main inputs.')
    out=ROOT/'results/task4_v40_intake';out.mkdir(parents=True,exist_ok=True)
    rank.to_csv(out/'ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
