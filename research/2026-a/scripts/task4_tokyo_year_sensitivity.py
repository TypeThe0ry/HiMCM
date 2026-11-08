"""Matched narrow 2025/2026 source comparison; never replaces V96 coverage."""
import hashlib
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import protect_output
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def run():
    source=ROOT/'data/task4_v99_tokyo'
    spec=importlib.util.spec_from_file_location('tokyo99_source',source/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    data=module.extract()
    assert data==json.loads((source/'summary.json').read_text())
    lo,hi,config=current_bounds();i,j=CITIES.index('Tokyo'),NAMES.index('upper_secondary_ptr')
    mask=np.ones(lo.shape,bool);mask[i,j]=False
    scenarios=[('v96_current',lo.copy(),hi.copy())]
    for r in data['scenarios']:
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=r['utility_bounds']
        assert 0<=l[i,j]<=h[i,j]<=1
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        scenarios.append(('matched_narrow_'+str(r['year']),l,h))
    out=ROOT/'results/task4_v99_tokyo_year'
    protect_output(out,lo,hi,config);out.mkdir(parents=True,exist_ok=True)
    frames=[];bounds=[];reports=[];certificates=[]
    for label,l,h in scenarios:
        f,d=summarize(l,h,weights(config['fixed_alpha']))
        frames.append(f.assign(scenario=label))
        cert=certify(l,h,*config['alpha_range'])
        certificates.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,tokyo_utility=[l[i,j],h[i,j]],
            tokyo=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],
            possible_champions=f.loc[f.possible_champion,'city'].tolist(),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k],*config['alpha_range'])['possible']],
            continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    old,new=frames[1],frames[2]
    result=dict(model_version=config['model_version'],fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],main_admitted=False,admitted_cells_changed=0,
        input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        source_summary_sha256=hashlib.sha256((source/'summary.json').read_bytes()).hexdigest(),
        paired_year_changed_ranks=int((old.decision_rank!=new.decision_rank).sum()),
        paired_year_kendall_tau=float(kendalltau(old.decision_rank,new.decision_rank).statistic),
        paired_year_tokyo_lower_change=float(new.iloc[i].score_lower-old.iloc[i].score_lower),
        paired_year_tokyo_upper_change=float(new.iloc[i].score_upper-old.iloc[i].score_upper),
        unchanged_other_cells=249,scenarios=reports,
        interpretation='Only the matched narrow pair isolates calendar year. Both use school main-duty persons and omit special-needs coverage; V96 instead uses selected teaching roles and wider coverage. Neither scenario is an improvement or replacement of V96. 2026 is provisional.')
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
