"""Official murder-rate alternatives; not an intentional-homicide series update."""
import hashlib,importlib.util,json
import numpy as np
import pandas as pd
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import protect_output
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize


def run():
    source=ROOT/'data/task4_v100_singapore'
    spec=importlib.util.spec_from_file_location('sg100_source',source/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    evidence=module.extract()
    assert evidence==json.loads((source/'summary.json').read_text())
    lo,hi,config=current_bounds();i,j=CITIES.index('Singapore'),NAMES.index('homicide_rate')
    mask=np.ones(lo.shape,bool);mask[i,j]=False
    out=ROOT/'results/task4_v100_singapore_source';protect_output(out,lo,hi,config)
    source_hash=hashlib.sha256((source/'summary.json').read_bytes()).hexdigest()
    if (out/'summary.json').exists():assert json.loads((out/'summary.json').read_text())['source_summary_sha256']==source_hash
    scenarios=[('v96_current',lo.copy(),hi.copy())]
    for r in evidence['local_murder_scenarios']:
        l,h=lo.copy(),hi.copy();rate=r['murder_victims_per_100000'];assert rate>=0
        l[i,j]=h[i,j]=2/(2+rate)
        scenarios.append(('murder_'+str(r['year']),l,h))
    base,_=summarize(lo,hi,weights(config['fixed_alpha']));frames=[];bounds=[];reports=[];certs=[]
    for label,l,h in scenarios:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        f,d=summarize(l,h,weights(config['fixed_alpha']));frames.append(f.assign(scenario=label))
        cert=certify(l,h,*config['alpha_range']);certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,singapore_risk_utility=[l[i,j],h[i,j]],
            singapore=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            changed_ranks_vs_current=int((f.decision_rank!=base.decision_rank).sum()),
            choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=f.loc[f.possible_champion,'city'].tolist(),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k],*config['alpha_range'])['possible']],
            continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version=config['model_version'],fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],
        input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),source_summary_sha256=source_hash,
        main_admitted=False,admitted_cells_changed=0,unchanged_other_cells=249,scenarios=reports,
        interpretation='Murder victims and official annual population define alternate local rate scenarios; no verified ICCS crosswalk to current WDI intentional homicide. 2023 source contrast is not pure temporal change; three local years share definition. No risk confidence interval or high-school-specific victimization claim.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ['scenario','singapore','changed_ranks_vs_current','choice','continuous_recommendation']} for r in reports],indent=2))

if __name__=='__main__':run()
