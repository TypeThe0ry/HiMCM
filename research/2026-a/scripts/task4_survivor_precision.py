"""Residual-width sensitivity of the V103 minimum-survivor construction.

Delta is absolute width in utility units, not a probability or a raw-data error.
Measured interval width is min(delta, original width); all other bounds remain.
"""
import hashlib,json
import numpy as np
from task4_current_model import current_bounds
from task4_survivor_set_search import endpoint_completion
from task4_continuous_preferences import feasible_preferences
from task4_v5_model import ROOT,CITIES,NAMES,score,weights


def finite_completion(lo,hi,mask,keep,delta):
    if not np.isscalar(delta) or not np.isfinite(delta) or not 0<=delta<=1:
        raise ValueError('Residual width must be finite and within [0,1]')
    lower,upper=endpoint_completion(lo,hi,mask,keep)
    width=np.minimum(delta,np.asarray(hi)-np.asarray(lo));inside=np.zeros(len(lo),bool);inside[list(keep)]=True
    lower=np.where(mask&inside[:,None],upper-width,lower)
    upper=np.where(mask&~inside[:,None],lower+width,upper)
    return lower,upper


def evaluate(lo,hi,mask,keep,delta,alpha_range=(.05,.2)):
    lower,upper=finite_completion(lo,hi,mask,keep,delta);excluded=[];uncertain=[]
    for i in range(len(lo)):
        if i in keep:continue
        r=feasible_preferences(upper[i],lower[list(keep)],*alpha_range)
        if r['possible']:
            a=r['witness_alpha'];v=score(np.vstack([upper[i],lower[list(keep)]]),weights(a));gap=float(v[0]-max(v[1:]))
            if gap>1e-8:
                return dict(delta=float(delta),status='impossible_four_set',outside_index=i,outside_city=CITIES[i],witness_alpha=a,strict_score_gap=gap)
            uncertain.append(dict(outside_index=i,witness_alpha=a,score_gap=gap))
        else:excluded.append(dict(outside_index=i,**r))
    return dict(delta=float(delta),status='unresolved_boundary' if uncertain else 'four_set_feasible',exclusions=excluded,uncertain=uncertain)


def frontier(lo,hi,mask,keep,alpha_range=(.05,.2),precision=1e-4):
    if not 0<precision<1:raise ValueError('Search precision must be inside (0,1)')
    left,right=evaluate(lo,hi,mask,keep,0,alpha_range),evaluate(lo,hi,mask,keep,1,alpha_range)
    if left['status']!='four_set_feasible' or right['status']!='impossible_four_set':
        return dict(status='not_bracketed',feasible=left,infeasible=right,steps=[])
    steps=[]
    while right['delta']-left['delta']>precision:
        r=evaluate(lo,hi,mask,keep,(left['delta']+right['delta'])/2,alpha_range);steps.append(r)
        if r['status']=='four_set_feasible':left=r
        elif r['status']=='impossible_four_set':right=r
        else:break
    return dict(status='bracketed_with_unresolved_boundary' if steps and steps[-1]['status']=='unresolved_boundary' else 'bracketed',
                feasible=left,infeasible=right,bracket_width=right['delta']-left['delta'],steps=steps)


def main():
    lo,hi,config=current_bounds();prior=ROOT/'results/task4_v103_survivor_search/summary.json';s=json.loads(prior.read_text())
    digest=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()
    assert s['input_bounds_sha256']==digest and s['model_version']==config['model_version']
    assert s['minimum_proved'] and s['certified_minimum']==4 and len(s['successful_sets'])==1
    # All other <=4 sets have strict failure witnesses at zero width and remain
    # infeasible as widths increase; the mandatory set remains unavoidable.
    assert len(s['records'])==23 and all(r['status'] in ['excluded_by_strict_witness','feasible_survivor_superset'] for r in s['records'])
    keep=s['successful_sets'][0];mask=np.zeros_like(lo,bool);mask[:,[NAMES.index(n) for n in s['measured_indicators']]]=True
    before=np.stack([lo,hi]).copy();boundary=frontier(lo,hi,mask,keep,config['alpha_range'])
    grid=[evaluate(lo,hi,mask,keep,d,config['alpha_range']) for d in [0,.001,.005,.01,.02,.05,.1,.2,1]]
    # At delta=.01 the unique four-set fails. Adding its strict outsider gives
    # a constructive five-set witness; verify it rather than infer attainment.
    four_at_one_percent=next(r for r in grid if r['delta']==.01)
    assert four_at_one_percent['status']=='impossible_four_set'
    five=sorted(keep+[four_at_one_percent['outside_index']])
    five_result=evaluate(lo,hi,mask,five,.01,config['alpha_range'])
    assert five_result['status']=='four_set_feasible'  # legacy status means K feasible
    five_result['status']='five_set_feasible'
    five_result.update(keep_indices=five,keep_cities=[CITIES[i] for i in five],certified_minimum=5)
    np.testing.assert_array_equal(before,np.stack([lo,hi]))
    out=ROOT/'results/task4_v104_survivor_precision'
    if (out/'summary.json').exists():
        old=json.loads((out/'summary.json').read_text())
        if old['input_bounds_sha256']!=digest:raise ValueError('Historical inputs cannot be overwritten')
    out.mkdir(exist_ok=True)
    result=dict(model_version=config['model_version'],input_bounds_sha256=digest,prior_summary_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
        measured_indicators=s['measured_indicators'],keep_indices=keep,keep_cities=[CITIES[i] for i in keep],
        alpha_range=config['alpha_range'],absolute_width_units='dimensionless utility [0,1]',width_rule='min(delta, original width)',
        main_admitted=False,new_observations=0,grid=grid,frontier=boundary,five_set_at_delta_001=five_result,
        interpretation='Best-case shared measurement intervals with specified residual width. Feasible means four remains the model minimum; impossible means at least five; delta .01 additionally has a verified five-set witness. Not actual observations or attainable raw-data precision.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(grid=[{k:v for k,v in r.items() if k not in ['exclusions','uncertain']} for r in grid],boundary=[boundary['feasible']['delta'],boundary['infeasible']['delta']],status=boundary['status']),indent=2))

if __name__=='__main__':main()
