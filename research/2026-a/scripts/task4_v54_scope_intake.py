"""Verify new source packages; retain current bounds when scopes do not match."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_istanbul_coverage_revision import istanbul_coverage_bounds
from task4_continuous_preferences import feasible_preferences


def main():
    sources=[]
    for name in ['task4_v54_istanbul_allocation','task4_v54_phoenix_travel','task4_v54_shanghai_coverage']:
        folder=ROOT/'data'/name
        for item in json.loads((folder/'manifest.json').read_text()):
            raw=(folder/item['file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==item['sha256']
            if 'bytes' in item:assert len(raw)==item['bytes']
        sources.append(dict(package=name,manifest_sha256=hashlib.sha256((folder/'manifest.json').read_bytes()).hexdigest()))
    lo,hi=istanbul_coverage_bounds();frame,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v53_istanbul_coverage/ranks.csv')
    prior=prior[prior.scenario=='v53_broader_teacher_allocation'].reset_index(drop=True)
    assert frame.city.tolist()==prior.city.tolist()
    for key in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(frame[key],prior[key],rtol=0,atol=1e-12)
    continuous=[c for i,c in enumerate(CITIES) if feasible_preferences(hi[i],lo[np.arange(len(lo))!=i])['possible']]
    out=ROOT/'results/task4_v54_scope_intake';out.mkdir(parents=True,exist_ok=True)
    frame.to_csv(out/'ranks.csv',index=False)
    result=dict(baseline='V53 istanbul_coverage_bounds',source_packages=sources,changed_cells=0,
                changed_ranks=0,possible_champions=int(frame.possible_champion.sum()),
                continuous_possible_champions=continuous,
                choice=[CITIES[i] for i in decision['minimax_choices']],main_admitted=False)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['source_packages','continuous_possible_champions']},indent=2))


if __name__=='__main__':main()
