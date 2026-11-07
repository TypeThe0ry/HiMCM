"""Single explicit entry point for the currently selected evidence model.

Historical model scripts remain frozen. The registry names both the selected
factory and its expected baseline, so changing one without the other fails.
"""
import argparse,hashlib,importlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify
REGISTRY=ROOT/'design/task4_current_model.json'


def current_bounds():
    config=json.loads(REGISTRY.read_text())
    amin,amax=config['alpha_range']
    if not 0<amin<=config['fixed_alpha']<=amax<1:
        raise ValueError('Fixed alpha must lie within the interior preference range')
    module=importlib.import_module(config['module'])
    lo,hi=getattr(module,config['factory'])()
    lo,hi=np.asarray(lo,float),np.asarray(hi,float)
    if lo.shape!=(len(CITIES),len(NAMES)) or hi.shape!=lo.shape:
        raise ValueError('Registry factory must return current city-by-indicator dimensions')
    if not np.isfinite([lo,hi]).all() or not np.all((0<=lo)&(lo<=hi)&(hi<=1)):
        raise ValueError('Registry returned invalid evidence intervals')
    return lo,hi,config


def verify_baseline(frame,baseline):
    if baseline.city.tolist()!=CITIES:
        raise ValueError('Selected baseline does not contain each current city in its canonical order')
    for col in ['score_lower','score_upper','max_regret','decision_rank','possible_champion','necessary_champion','best_rank','worst_rank']:
        np.testing.assert_allclose(frame[col],baseline[col],rtol=0,atol=1e-12,
            err_msg='Current model differs from registry baseline: '+col)


def verify_bounds(lo,hi,baseline):
    if baseline.city.tolist()!=[c for c in CITIES for _ in NAMES] or baseline.indicator.tolist()!=NAMES*len(CITIES):
        raise ValueError('Baseline cell identities or ordering differ from current model')
    np.testing.assert_allclose(lo.ravel(),baseline.lower,rtol=0,atol=1e-15)
    np.testing.assert_allclose(hi.ravel(),baseline.upper,rtol=0,atol=1e-15)


def run(out):
    lo,hi,config=current_bounds()
    frame,decision=summarize(lo,hi,weights(config['fixed_alpha']))
    baseline_file=ROOT/config['baseline_ranks'];baseline=pd.read_csv(baseline_file)
    baseline=baseline[baseline.scenario==config['baseline_scenario']].reset_index(drop=True)
    verify_baseline(frame,baseline)
    bounds_file=ROOT/config['baseline_bounds'];old_bounds=pd.read_csv(bounds_file)
    old_bounds=old_bounds[old_bounds.scenario==config['baseline_scenario']].reset_index(drop=True)
    verify_bounds(lo,hi,old_bounds)
    amin,amax=config['alpha_range']
    continuous=[c for i,c in enumerate(CITIES) if feasible_preferences(hi[i],lo[np.arange(len(lo))!=i],amin,amax)['possible']]
    certificate=certify(lo,hi,amin,amax)
    for c in certificate:c['city']=None if c['winner'] is None else CITIES[c['winner']]
    bounds=pd.DataFrame([dict(city=c,indicator=n,lower=float(lo[i,j]),upper=float(hi[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)])
    out.mkdir(parents=True,exist_ok=True)
    frame.to_csv(out/'ranks.csv',index=False);bounds.to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificate).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(registry=config,registry_sha256=hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
        baseline_ranks_sha256=hashlib.sha256(baseline_file.read_bytes()).hexdigest(),
        baseline_bounds_sha256=hashlib.sha256(bounds_file.read_bytes()).hexdigest(),
        utility_bounds_sha256=hashlib.sha256((out/'utility_bounds.csv').read_bytes()).hexdigest(),
        verified_cells=int(lo.size),baseline_matches=True,possible_champions=int(frame.possible_champion.sum()),
        continuous_possible_champions=continuous,choice=[CITIES[i] for i in decision['minimax_choices']],
        continuous_recommendation=dict(unresolved_leaves=sum(not c['certified'] for c in certificate),
            winners=sorted({c['city'] for c in certificate if c['certified']})),
        main_admitted=config['main_admitted'])
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['verified_cells','baseline_matches','possible_champions','choice','continuous_recommendation','main_admitted']},indent=2))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'results/task4_current')
    run(parser.parse_args().output)
