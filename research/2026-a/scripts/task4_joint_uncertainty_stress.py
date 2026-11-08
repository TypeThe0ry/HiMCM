"""Continuous preference/interval-expansion stress, with targeted counterexamples.

Uniform expansion is a specified scenario, not a guarantee against arbitrary
source errors. Unresolved rectangles are preserved; no monotone-gap assumption.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_current_model import current_bounds,run as run_current
from task4_v5_model import ROOT,CITIES,NAMES,score,weights,summarize
from task4_continuous_recommendation import certify


def expand(lo,hi,epsilon,target=None):
    if not 0<=epsilon<=1:raise ValueError('epsilon must be in [0,1]')
    l,h=np.array(lo,dtype=float,copy=True),np.array(hi,dtype=float,copy=True)
    if (l.ndim!=2 or h.shape!=l.shape or l.shape[1]!=10 or len(l)<2
        or not np.isfinite([l,h]).all() or not np.all((0<=l)&(l<=h)&(h<=1))):
        raise ValueError('Ordered finite city-by-ten bounds required')
    rows=slice(None) if target is None else target
    l[rows]=np.maximum(0,l[rows]-epsilon);h[rows]=np.minimum(1,h[rows]+epsilon)
    return l,h


def rectangle_enclosure(lo,hi,e0,e1,a0,a1,target=None,padding=1e-9):
    # Lower scores fall and upper scores rise with epsilon. For fixed epsilon,
    # each score is monotone or constant in alpha: squared distances are affine.
    small_l,small_h=expand(lo,hi,e0,target)
    large_l,large_h=expand(lo,hi,e1,target)
    lmin=np.minimum(score(large_l,weights(a0)),score(large_l,weights(a1)))-padding
    lmax=np.maximum(score(small_l,weights(a0)),score(small_l,weights(a1)))+padding
    umin=np.minimum(score(small_h,weights(a0)),score(small_h,weights(a1)))-padding
    umax=np.maximum(score(large_h,weights(a0)),score(large_h,weights(a1)))+padding
    rmin=np.array([max(0,np.delete(umin,i).max()-lmax[i]) for i in range(len(lo))])
    rmax=np.array([max(0,np.delete(umax,i).max()-lmin[i]) for i in range(len(lo))])
    return rmin,rmax


def certify_prefix(lo,hi,choice,emax=.2,amin=.05,amax=.2,max_depth=14,target=None):
    if not 0<=emax<=1 or not 0<amin<=amax<1 or not 0<=max_depth<=18:
        raise ValueError('Invalid stress domain or recursion depth')
    pending=[(0.,emax,amin,amax,0)];leaves=[]
    while pending:
        e0,e1,a0,a1,depth=pending.pop()
        low,high=rectangle_enclosure(lo,hi,e0,e1,a0,a1,target)
        gap=float(np.delete(low,choice).min()-high[choice])
        certified=gap>1e-8
        if certified or depth==max_depth or (e0==e1 and a0==a1):
            leaves.append(dict(epsilon_lower=e0,epsilon_upper=e1,alpha_lower=a0,alpha_upper=a1,
                certified=certified,gap_lower=gap,depth=depth))
        elif (e1-e0)/max(emax,1e-15)>=(a1-a0)/max(amax-amin,1e-15):
            m=(e0+e1)/2;pending.extend([(e0,m,a0,a1,depth+1),(m,e1,a0,a1,depth+1)])
        else:
            m=(a0+a1)/2;pending.extend([(e0,e1,a0,m,depth+1),(e0,e1,m,a1,depth+1)])
    return sorted(leaves,key=lambda x:(x['epsilon_lower'],x['alpha_lower']))


def protect_output(out,lo,hi,config):
    """Reject baseline changes before creating or writing any output files."""
    out=Path(out)
    if not out.exists() or not any(out.iterdir()):return
    summary=out/'summary.json'
    if not summary.exists():raise ValueError('Existing output has no verifiable baseline; choose a new directory')
    previous=json.loads(summary.read_text())
    digest=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()
    if previous.get('model_version')!=config['model_version']:
        raise ValueError('Refusing to overwrite a different model baseline')
    if 'fixed_alpha' in previous:
        previous_weights=previous
    else:
        baseline_summary=out/'baseline/summary.json'
        if not baseline_summary.exists():raise ValueError('Existing output has no verifiable weight baseline')
        previous_weights=json.loads(baseline_summary.read_text())['registry']
    if any(previous_weights.get(k)!=config[k] for k in ('fixed_alpha','alpha_range')):
        raise ValueError('Refusing to overwrite changed baseline weights')
    if 'input_bounds_sha256' in previous:
        if previous['input_bounds_sha256']!=digest:
            raise ValueError('Refusing to overwrite changed input bounds')
    else:
        # Legacy results predate the explicit input digest.
        saved=pd.read_csv(out/'baseline/utility_bounds.csv')
        if (saved.city.tolist()!=[c for c in CITIES for _ in range(10)]
            or saved.indicator.tolist()!=NAMES*len(CITIES)
            or not np.allclose(saved.lower,lo.ravel(),rtol=0,atol=1e-15)
            or not np.allclose(saved.upper,hi.ravel(),rtol=0,atol=1e-15)):
            raise ValueError('Refusing to overwrite changed legacy baseline')


def run(out=None,targeted_prefix_max=.05,extra_epsilons=()):
    if not 0<=targeted_prefix_max<=.2:raise ValueError('Targeted prefix must lie in [0,.2]')
    extra_epsilons=tuple(extra_epsilons)
    if any(not np.isfinite(e) or not 0<=e<=.2 for e in extra_epsilons):
        raise ValueError('Extra epsilon values must be finite and in [0,.2]')
    lo,hi,config=current_bounds();amin,amax=config['alpha_range']
    out=Path(out) if out is not None else ROOT/('results/task4_'+config['model_version'].lower()+'_joint_stress')
    protect_output(out,lo,hi,config)
    base,decision=summarize(lo,hi,weights(config['fixed_alpha']))
    assert len(decision['minimax_choices'])==1
    choice=decision['minimax_choices'][0]
    out.mkdir(parents=True,exist_ok=True)
    run_current(out/'baseline')
    leaves=certify_prefix(lo,hi,choice,amin=amin,amax=amax)
    pd.DataFrame(leaves).to_csv(out/'uniform_prefix_certificate.csv',index=False)
    targeted_prefix=certify_prefix(lo,hi,choice,emax=targeted_prefix_max,amin=amin,amax=amax,target=choice)
    pd.DataFrame(targeted_prefix).to_csv(out/'targeted_prefix_certificate.csv',index=False)
    targeted_fixed=certify(*expand(lo,hi,.2,choice),amin,amax)
    for row in targeted_fixed:row['city']=None if row['winner'] is None else CITIES[row['winner']]
    pd.DataFrame(targeted_fixed).to_csv(out/'targeted_epsilon02_certificate.csv',index=False)
    frames=[];cases=[]
    for structure,target in [('uniform',None),('recommendation_city_only',choice)]:
        for epsilon in sorted(set([0,.025,.05,.075,.1,.15,.2,targeted_prefix_max,*extra_epsilons])):
            l,h=expand(lo,hi,epsilon,target)
            for alpha in sorted(set([amin,config['fixed_alpha'],amax])):
                f,d=summarize(l,h,weights(alpha))
                same_alpha,_=summarize(lo,hi,weights(alpha))
                gap=float(np.delete(f.max_regret.to_numpy(),choice).min()-f.max_regret.iloc[choice])
                cases.append(dict(structure=structure,epsilon=epsilon,alpha=alpha,
                    baseline_choice_gap=gap,choices=[CITIES[k] for k in d['minimax_choices']],
                    possible_champions=int(f.possible_champion.sum()),changed_ranks_same_alpha=int((f.decision_rank!=same_alpha.decision_rank).sum()),
                    changed_ranks_fixed_baseline=int((f.decision_rank!=base.decision_rank).sum())))
                f=f.assign(structure=structure,epsilon=epsilon,alpha=alpha);frames.append(f)
    pd.concat(frames).to_csv(out/'scenario_ranks.csv',index=False)
    failures=[x for x in cases if x['structure']=='recommendation_city_only' and x['baseline_choice_gap'] < -1e-8]
    witness=min(failures,key=lambda x:(x['epsilon'],x['alpha'])) if failures else None
    result=dict(model_version=config['model_version'],input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),scenario_only=True,admitted_cells_changed=0,
        baseline_choice=CITIES[choice],fixed_alpha=config['fixed_alpha'],alpha_range=[amin,amax],epsilon_range=[0,.2],
        uniform_certificate=dict(leaves=len(leaves),unresolved=sum(not x['certified'] for x in leaves),
            minimum_gap_lower=min(x['gap_lower'] for x in leaves),padding=1e-9,strict_tolerance=1e-8,
            formal_interval_arithmetic=False),
        targeted_prefix_certificate=dict(epsilon_range=[0,targeted_prefix_max],leaves=len(targeted_prefix),
            unresolved=sum(not x['certified'] for x in targeted_prefix),
            minimum_gap_lower=min(x['gap_lower'] for x in targeted_prefix)),
        targeted_fixed_certificate=dict(epsilon=.2,leaves=len(targeted_fixed),
            unresolved=sum(not x['certified'] for x in targeted_fixed),
            winners=sorted({x['city'] for x in targeted_fixed if x['certified']})),
        targeted_failure_witness=witness,
        scenarios=cases,
        interpretation='Uniform expansion is not arbitrary-error robustness; targeted cases are hypothetical counterexamples, not measured source bias.',main_admitted=False)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='scenarios'},indent=2))
    return result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,help='Output directory; defaults to current model version')
    parser.add_argument('--targeted-prefix-max',type=float,default=.05)
    parser.add_argument('--extra-epsilon',type=float,action='append',default=[],help='Additional explicitly sampled expansion, repeatable; not a continuous certificate')
    args=parser.parse_args()
    run(args.output,args.targeted_prefix_max,args.extra_epsilon)


if __name__=='__main__':main()
