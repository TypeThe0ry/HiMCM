"""Refresh shared survivor sets and finite-width precision for registered inputs."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import protect_output
from task4_survivor_set_search import search
from task4_survivor_precision import frontier,evaluate
from task4_v5_model import ROOT,CITIES,NAMES


def run(out,prior):
    lo,hi,config=current_bounds();protect_output(out,lo,hi,config)
    source=json.loads(prior.read_text())
    digest=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()
    if source['model_version']!=config['model_version'] or source['input_bounds_sha256']!=digest:
        raise ValueError('Joint-acquisition input does not match registered model')
    if any(source.get(k)!=config[k] for k in ('fixed_alpha','alpha_range')):
        raise ValueError('Joint-acquisition preference parameters do not match registered model')
    case=next(r for r in source['scenarios'] if r['scenario']=='both_plus_homicide_rate' and r['mode']=='continuous')
    required=[CITIES.index(c) for c in case['unavoidable_cities']]
    mask=np.zeros_like(lo,bool);mask[:,[NAMES.index(n) for n in case['measured_indicators']]]=True
    result=search(lo,hi,mask,required,case['attained_count_upper_bound'],config['alpha_range'])
    precision=[]
    for keep in result['successful_sets']:
        grid=[evaluate(lo,hi,mask,keep,d,config['alpha_range']) for d in [0,.001,.005,.01,.02,.05,.1,.2,1]]
        # The inherited evaluator uses legacy four-set status names for arbitrary K.
        # Preserve these raw diagnostics and report the actual size separately.
        precision.append(dict(keep_indices=keep,keep_cities=[CITIES[i] for i in keep],keep_size=len(keep),
            frontier=frontier(lo,hi,mask,keep,config['alpha_range']),grid=grid))
    # Search enumerates all minimum-cardinality sets containing unavoidable cities.
    # Larger residual widths only weaken exclusion, so sets failing at width zero
    # cannot become feasible later. Max of all per-set thresholds is global.
    bracketed=bool(precision) and result['minimum_proved'] and all(p['frontier']['status']=='bracketed' for p in precision)
    global_frontier=None
    if bracketed:
        global_frontier=dict(feasible_width=max(p['frontier']['feasible']['delta'] for p in precision),
            infeasible_width=max(p['frontier']['infeasible']['delta'] for p in precision),
            minimum_set_size=result['certified_minimum'],all_minimum_sets_enumerated=True)
    result.update(model_version=config['model_version'],input_bounds_sha256=digest,
        source_summary_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
        required_cities=case['unavoidable_cities'],measured_indicators=case['measured_indicators'],
        alpha_range=config['alpha_range'],fixed_alpha=config['fixed_alpha'],main_admitted=False,new_observations=0,
        successful_city_sets=[[CITIES[i] for i in k] for k in result['successful_sets']],
        precision=precision,global_minimum_size_frontier=global_frontier,width_rule='min(delta, original width)',
        scope='Hypothetical shared endpoint revelations, not observed improvements or forecast. Precision frontier is per successful minimum set; no claim of larger-set optimum without separate witness. Legacy precision status names contain four_set regardless of actual keep_size.')
    out.mkdir(parents=True,exist_ok=True);(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['model_version','certified_minimum','successful_city_sets','required_cities']},indent=2))
    print(json.dumps([dict(keep=p['keep_cities'],frontier=[p['frontier']['feasible']['delta'],p['frontier']['infeasible']['delta']]) for p in precision],indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--joint-summary',type=Path,required=True)
    a=p.parse_args();run(a.output,a.joint_summary)
