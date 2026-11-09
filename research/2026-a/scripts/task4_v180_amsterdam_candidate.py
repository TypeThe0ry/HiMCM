"""Preview one declared Amsterdam inventory lower bound; leave V154 active."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import numpy as np
import pandas as pd
from task4_user_v154_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import ROOT, NAMES, weights

O = ROOT / 'results/task4_v180_amsterdam_candidate'
D = ROOT / 'data/task4_v180_amsterdam'
P = ROOT.parents[2] / 'HiMCM-Overleaf'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    O.mkdir(exist_ok=True)
    protected_path = O / 'protected_files.json'
    if protected_path.exists():
        protected = json.loads(protected_path.read_text())
    else:
        names = subprocess.check_output(['git', '-C', str(P), 'ls-files', '-z']).decode().split('\0')[:-1]
        protected = dict(science=json.loads((ROOT/'design/task4_user_v154_snapshot.json').read_text())['source_sha256'],
                         paper={n:sha(P/n) for n in names},
                         registries={n:sha(ROOT/'design'/n) for n in ['task4_user_current_model.json','task4_user_current_extensions.json','task4_user_current_review.json']})
    for base, mapping in [(ROOT,protected['science']), (P,protected['paper']), (ROOT/'design',protected['registries'])]:
        for n,h in mapping.items(): assert sha(base/n)==h,n
    spec = importlib.util.spec_from_file_location('amsterdam180_source', D/'extract.py')
    extractor = importlib.util.module_from_spec(spec);spec.loader.exec_module(extractor)
    extraction = extractor.main()
    frame, lo, hi = revised_bounds()
    assert lo.shape == hi.shape == (16,10)
    i, j = frame.city.tolist().index('Amsterdam'), NAMES.index('public_transport_density')
    assert lo[i,j] == 0 and hi[i,j] == 1
    pop = int(frame.iloc[i].population)
    assert pop == 941927
    tables, summaries, bounds = [], [], []
    for scenario, count in [('V154_baseline',0),('candidate_screened32',extraction['retained_candidate_count']),('nominal35_diagnostic',extraction['nominal_inside_both_boundaries'])]:
        rate = count*100000/pop
        lower = rate/(50+rate)
        current = lo.copy();current[i,j] = lower
        assert np.array_equal(np.delete(current.ravel(),i*10+j),np.delete(lo.ravel(),i*10+j))
        assert np.array_equal(hi,revised_bounds()[2])
        bounds.append(dict(scenario=scenario,city='Amsterdam',indicator=NAMES[j],count='not_observed' if scenario=='V154_baseline' else str(count),count_interpretation='Unknown transport inventory,not observed zero' if scenario=='V154_baseline' else 'Declared mapped Metro subset only',population=pop,population_year=int(frame.iloc[i].population_year),inventory_metadata_year=2026,lower=lower,upper=1.0,primary_admitted=False))
        for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
            result=evaluate(frame.city.tolist(),current,hi,w)
            tables.append(result.assign(scenario=scenario,weight_reference=ref))
            summaries.append(dict(scenario=scenario,weight_reference=ref,mean_score_interval_width=float((result.score_upper-result.score_lower).mean()),conservative_recommendation=result.loc[result.decision_rank==1,'city'].tolist(),possible_champions=int(result.possible_champion.sum()),necessary_champions=int(result.necessary_champion.sum())))
    pd.concat(tables,ignore_index=True).to_csv(O/'preview_ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(O/'candidate_bounds.csv',index=False)
    summary=dict(version='V180 candidate preview',current_primary='V154 unchanged',current_paper='V179 unchanged',
                 primary_admissions=0,candidate_count=32,nominal_inside_count=35,declared_screen_metres=100,
                 utility_scope='Conditional2026 mapped-inventory lower bound with retained2025 population;not a backdated2025 count or measured positional-error guarantee',
                 upper_bounds_160_unchanged=True,other_159_utility_cells_unchanged=True,city_weight_scenario_rows=96,
                 scenarios=summaries,source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [*sorted(D.iterdir()),Path(__file__)] if p.is_file()},
                 next_gate='Independent source/geometry/preview audit;formal admission,full extension migration and manuscript consistency before activation',MC_rerun=False)
    (O/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    protected_path.write_text(json.dumps(protected,indent=2)+'\n')
    for base,mapping in [(ROOT,protected['science']),(P,protected['paper']),(ROOT/'design',protected['registries'])]:
        for n,h in mapping.items():assert sha(base/n)==h,n
    print(json.dumps({k:summary[k] for k in ['candidate_count','primary_admissions','scenarios']},indent=2))


if __name__=='__main__':
    main()
