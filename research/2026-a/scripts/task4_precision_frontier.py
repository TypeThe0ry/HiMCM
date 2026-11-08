"""Continuous precision thresholds for adverse-outcome acquisition scenarios.

For selected cells upper endpoints are lo+rho*(hi-lo). Monotonicity in rho
permits bisection; all preference comparisons retain their continuous roots.
These are hypothetical lower-anchored outcomes, never observations.
"""
import argparse,hashlib,itertools,json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES
from task4_current_model import current_bounds,run as run_current
from task4_continuous_preferences import feasible_preferences
from task4_joint_uncertainty_stress import protect_output
KIND='adverse_acquisition_precision_frontier'


def threshold(lo,hi,city,subset,alpha_range=(.05,.2),iterations=40):
    lo,hi=np.asarray(lo,float),np.asarray(hi,float)
    subset=tuple(subset);amin,amax=alpha_range
    if (lo.ndim!=2 or lo.shape!=hi.shape or lo.shape[1]!=10 or len(lo)<2
        or not np.isfinite([lo,hi]).all() or not np.all((0<=lo)&(lo<=hi)&(hi<=1))):
        raise ValueError('Finite ordered city-by-ten bounds required')
    if (not isinstance(city,(int,np.integer)) or not 0<=city<len(lo) or len(set(subset))!=len(subset)
        or any(not isinstance(j,(int,np.integer)) or j not in range(10) for j in subset)):
        raise ValueError('Invalid city or distinct criterion indices')
    if not 0<amin<=amax<1 or not 1<=iterations<=60:raise ValueError('Invalid preference range or bisection count')
    rivals=lo[np.arange(len(lo))!=city]
    js=list(subset)
    def possible(rho):
        row=hi[city].copy();row[js]=lo[city,js]+rho*(hi[city,js]-lo[city,js])
        return feasible_preferences(row,rivals,amin,amax)
    zero=possible(0.)
    if zero['possible']:
        return dict(status='cannot_exclude_even_exact',excluded_rho=None,possible_rho=0.,witness_alpha=zero['witness_alpha'])
    one=possible(1.)
    if not one['possible']:
        return dict(status='already_excluded',excluded_rho=1.,possible_rho=None,witness_alpha=None)
    left,right=0.,1.
    for _ in range(iterations):
        mid=(left+right)/2
        if possible(mid)['possible']:right=mid
        else:left=mid
    assert not possible(left)['possible']
    witness=possible(right);assert witness['possible']
    return dict(status='bracketed',excluded_rho=left,possible_rho=right,witness_alpha=witness['witness_alpha'])


def run(out,city_name='Phoenix'):
    lo,hi,config=current_bounds();city=CITIES.index(city_name)
    path=out/'summary.json'
    if path.exists():
        previous=json.loads(path.read_text())
        if previous.get('analysis_kind')!=KIND or previous.get('city')!=city_name:
            raise ValueError('Refusing to overwrite different analysis or city')
    protect_output(out,lo,hi,config)
    run_current(out/'baseline')
    saved=np.stack([lo,hi]).copy()
    unknown=np.flatnonzero(hi[city]-lo[city]>1e-12).tolist()
    records=[];frontier=[]
    for size in range(len(unknown)+1):
        rows=[]
        for subset in itertools.combinations(unknown,size):
            result=threshold(lo,hi,city,subset,config['alpha_range'])
            row=dict(city=city_name,size=size,indicators='|'.join(NAMES[j] for j in subset),**result)
            rows.append(row);records.append(row)
        feasible=[r for r in rows if r['excluded_rho'] is not None]
        if feasible:
            best=max(feasible,key=lambda r:r['excluded_rho'])
            frontier.append(dict(size=size,exclusion_possible=True,largest_certified_rho=best['excluded_rho'],best_bundle=best['indicators'],indistinguishable_best_bundles=[r['indicators'] for r in feasible if r['possible_rho'] is None or r['possible_rho']>=best['excluded_rho']],possible_rho_for_best_bundle=best['possible_rho'],all_bundles_possible_from_rho=max(r['possible_rho'] for r in feasible if r['possible_rho'] is not None) if all(r['possible_rho'] is not None for r in feasible) else None,number_excludable_exact_bundles=len(feasible)))
        else:frontier.append(dict(size=size,exclusion_possible=False,largest_certified_rho=None,best_bundle=None,indistinguishable_best_bundles=[],possible_rho_for_best_bundle=None,all_bundles_possible_from_rho=0.,number_excludable_exact_bundles=0))
    # Same-input reproduction of the earlier coarse precision grid.
    grid=[]
    for rho in [0.,.01,.025,.05,.1,.2,.5,1.]:
        successful=[]
        for row in records:
            js=[NAMES.index(n) for n in row['indicators'].split('|') if n]
            candidate=hi[city].copy();candidate[js]=lo[city,js]+rho*(hi[city,js]-lo[city,js])
            if not feasible_preferences(candidate,lo[np.arange(len(lo))!=city],*config['alpha_range'])['possible']:
                successful.append(row)
        minimum=min((r['size'] for r in successful),default=None)
        grid.append(dict(residual_fraction=rho,minimum_criteria=minimum,minimal_bundle_count=sum(r['size']==minimum for r in successful)))
    pd.DataFrame(grid).to_csv(out/'same_input_coarse_grid.csv',index=False)
    np.testing.assert_array_equal(saved,np.stack([lo,hi]))
    pd.DataFrame(records).to_csv(out/'bundle_thresholds.csv',index=False)
    pd.DataFrame(frontier).to_csv(out/'frontier.csv',index=False)
    result=dict(analysis_kind=KIND,model_version=config['model_version'],city=city_name,fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],input_bounds_sha256=hashlib.sha256(saved.astype('<f8').tobytes()).hexdigest(),new_observations=0,admitted_cells_changed=0,scenario_only=True,main_admitted=False,unknown_criteria=[NAMES[j] for j in unknown],evaluated_bundles=len(records),same_input_coarse_grid=grid,bisection_iterations=40,polynomial_tolerance=1e-12,formal_interval_arithmetic=False,interpretation='Hypothetical intervals anchored at existing lower endpoints. Precision alone does not ensure exclusion; favorable outcomes retain champion possibility. Counts are model criteria, not source files or acquisition costs.',frontier=frontier)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(frontier,indent=2));return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);parser.add_argument('--city',default='Phoenix',choices=CITIES)
    args=parser.parse_args();run(args.output,args.city)
