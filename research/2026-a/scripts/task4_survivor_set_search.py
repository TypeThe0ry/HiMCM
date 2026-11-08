"""Exact subset reduction for shared revelations in a rectangular utility model.

For a proposed survivor superset K, raise measured cells in K to their upper
endpoints and lower measured cells outside K. This completion is sufficient
whenever any shared completion can exclude every outsider for all alpha.
Numerical uncertainty is retained; this is not formal interval arithmetic.
"""
import itertools,json,hashlib
from pathlib import Path
import numpy as np
from task4_current_model import current_bounds
from task4_v5_model import ROOT,CITIES,NAMES,score,weights
from task4_continuous_preferences import feasible_preferences


def endpoint_completion(lo,hi,mask,keep):
    lo,hi=np.asarray(lo,float),np.asarray(hi,float)
    mask=np.asarray(mask)
    if lo.shape!=hi.shape or mask.shape!=lo.shape or mask.dtype!=bool:
        raise ValueError('Matching bound matrices and Boolean mask required')
    if np.any(~np.isfinite([lo,hi])) or np.any((lo<0)|(hi>1)|(lo>hi)):
        raise ValueError('Valid finite utility intervals required')
    keep=tuple(keep)
    if not keep or len(set(keep))!=len(keep) or any(not isinstance(i,(int,np.integer)) or i<0 or i>=len(lo) for i in keep):
        raise ValueError('Nonempty distinct valid survivor indices required')
    rows=np.zeros(len(lo),bool);rows[list(keep)]=True
    point=np.where(rows[:,None],hi,lo)
    return np.where(mask,point,lo),np.where(mask,point,hi)


def evaluate(lo,hi,mask,keep,alpha_range=(.05,.2)):
    lower,upper=endpoint_completion(lo,hi,mask,keep)
    exclusions=[];uncertain=[]
    for i in range(len(lo)):
        if i in keep:continue
        result=feasible_preferences(upper[i],lower[list(keep)],*alpha_range)
        if result['possible']:
            a=result['witness_alpha'];values=score(np.vstack([upper[i],lower[list(keep)]]),weights(a))
            gap=float(values[0]-max(values[1:]))
            if gap>1e-8:
                return dict(status='excluded_by_strict_witness',outside_index=i,alpha=a,score_gap=gap)
            uncertain.append(dict(outside_index=i,alpha=a,score_gap=gap))
        else:exclusions.append(dict(outside_index=i,**result))
    if uncertain:return dict(status='unresolved_boundary',uncertain=uncertain)
    return dict(status='feasible_survivor_superset',exclusions=exclusions)


def search(lo,hi,mask,required,max_size,alpha_range=(.05,.2)):
    required=tuple(sorted(required));optional=[i for i in range(len(lo)) if i not in required]
    records=[];unresolved_smaller=False
    for size in range(max(1,len(required)),max_size+1):
        level=[]
        for extra in itertools.combinations(optional,size-len(required)):
            keep=tuple(sorted(required+extra));r=dict(keep_indices=list(keep),size=size,**evaluate(lo,hi,mask,keep,alpha_range));records.append(r);level.append(r)
        successes=[r for r in level if r['status']=='feasible_survivor_superset']
        if successes:
            return dict(certified_minimum=None if unresolved_smaller else size,
                        attained_upper_bound=size,minimum_proved=not unresolved_smaller,
                        successful_sets=[r['keep_indices'] for r in successes],records=records)
        unresolved_smaller |= any(r['status']=='unresolved_boundary' for r in level)
    return dict(certified_minimum=None,attained_upper_bound=None,minimum_proved=False,successful_sets=[],records=records)


def main():
    lo,hi,config=current_bounds();prior=ROOT/'results/task4_v103_joint_acquisition/summary.json';s=json.loads(prior.read_text())
    digest=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()
    assert digest==s['input_bounds_sha256'] and config['model_version']==s['model_version']
    case=next(r for r in s['scenarios'] if r['scenario']=='both_plus_homicide_rate' and r['mode']=='continuous')
    required=[CITIES.index(c) for c in case['unavoidable_cities']]
    mask=np.zeros_like(lo,bool);mask[:,[NAMES.index(n) for n in case['measured_indicators']]]=True
    result=search(lo,hi,mask,required,case['attained_count_upper_bound'],config['alpha_range'])
    result.update(model_version=config['model_version'],input_bounds_sha256=digest,
        source_summary_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),required_cities=case['unavoidable_cities'],
        scenario=case['scenario'],mode='continuous',alpha_range=config['alpha_range'],
        previous_bound=[case['universal_count_lower_bound'],case['attained_count_upper_bound']],
        measured_indicators=case['measured_indicators'],main_admitted=False,new_observations=0,
        successful_city_sets=[[CITIES[i] for i in k] for k in result['successful_sets']],
        scope='Shared hypothetical exact selected cells; independent closed utility box. Endpoint feasibility and subset minimality are numerical, not physical attainability or a forecast.')
    out=ROOT/'results/task4_v103_survivor_search'
    if (out/'summary.json').exists():
        old=json.loads((out/'summary.json').read_text())
        if old['model_version']!=config['model_version'] or old['input_bounds_sha256']!=digest:
            raise ValueError('Refusing to overwrite a different historical input')
    out.mkdir(exist_ok=True)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))

if __name__=='__main__':main()
