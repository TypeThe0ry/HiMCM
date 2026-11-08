"""Refresh optimistic recommendation-acquisition search from the model registry.

Historical V64 remains unchanged. Current source bounds and baseline ranks are
verified before search; the search is conditional on favorable exact endpoints,
not a promise that collecting the named data changes a city's recommendation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_current_model import current_bounds, verify_baseline, verify_bounds
from task4_continuous_acquisition import search, TOL
from task4_v5_model import ROOT, CITIES, NAMES, weights, summarize


def run(out, prior_results=None, prior_model="V63"):
    lo, hi, config = current_bounds()
    if config['fixed_alpha'] != .1 or config['alpha_range'] != [.05, .2]:
        raise ValueError('Reused continuous search is certified only for alpha [.05,.2] and fixed .1')
    frame, decision = summarize(lo, hi, weights(config['fixed_alpha']))
    old = pd.read_csv(ROOT/config['baseline_ranks'])
    verify_baseline(frame, old.loc[old.scenario.eq(config['baseline_scenario'])].reset_index(drop=True))
    bounds = pd.read_csv(ROOT/config['baseline_bounds'])
    verify_bounds(lo, hi, bounds.loc[bounds.scenario.eq(config['baseline_scenario'])].reset_index(drop=True))
    saved = np.stack([lo, hi]).copy()
    summaries, evaluations, certificates = [], [], []
    for i, city in enumerate(CITIES):
        summary, rows, leaves = search(lo, hi, i)
        summaries.append(summary); evaluations.extend(rows); certificates.extend(leaves)
        print(city, summary['smallest_certified_continuous_bundle'], flush=True)
    np.testing.assert_array_equal(saved, np.stack([lo, hi]))
    previous_path = (prior_results or ROOT/'results/task4_v64_continuous_acquisition')/'minimum_bundles.csv'
    previous = pd.read_csv(previous_path)
    current = pd.DataFrame(summaries)
    compared = previous.merge(current, on='city', suffixes=('_prior', '_current'), validate='one_to_one')
    fields = ['fixed_alpha_minimum', 'smallest_certified_continuous_bundle', 'certified_minimal_bundles']
    changed = compared.loc[np.logical_or.reduce([compared[f'{c}_prior'].ne(compared[f'{c}_current']) for c in fields])]
    out.mkdir(parents=True, exist_ok=True)
    current.to_csv(out/'minimum_bundles.csv', index=False)
    pd.DataFrame(evaluations).to_csv(out/'bundle_evaluations.csv', index=False)
    pd.DataFrame(certificates).to_csv(out/'bundle_certificates.csv', index=False)
    compared.to_csv(out/'comparison_prior.csv', index=False)
    frame.to_csv(out/'ranks.csv', index=False)
    pd.DataFrame([dict(city=c, indicator=n, lower=lo[i,j], upper=hi[i,j])
        for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)]).to_csv(out/'utility_bounds.csv',index=False)
    result = dict(model_version=config['model_version'], previous_model_version=prior_model,
        input_bounds_sha256=hashlib.sha256(saved.astype('<f8').tobytes()).hexdigest(),
        previous_minimum_bundles_sha256=hashlib.sha256(previous_path.read_bytes()).hexdigest(),
        actual_changed_cells=0, actual_changed_ranks=0, main_admitted=False,
        baseline_matches=True, alpha_range=config['alpha_range'], fixed_alpha=config['fixed_alpha'],
        possible_champions=int(frame.possible_champion.sum()), choice=[CITIES[i] for i in decision['minimax_choices']],
        evaluated_bundles=len(evaluations), unresolved_bundles=sum(r['status']=='unresolved' for r in evaluations),
        changed_acquisition_diagnostics=changed[['city']+[c+s for c in fields for s in ['_prior','_current']]].to_dict('records'),
        focal_cities=[r for r in summaries if r['city'] in ['Phoenix','Delhi','Mumbai','Tokyo','Cape Town','Shanghai']],
        scope='Optimistic city-local exact revelation at current upper endpoints in the rectangular outer model. Not guaranteed observations, joint physical attainability, city quality, or a necessary performance champion.',
        proof='The upper endpoints maximize target lower score while retaining its upper score; target regret decreases and rivals regret increases for every alpha. The same endpoint vector is favorable throughout the preference interval.',
        tolerances=dict(witness_negative_margin=TOL, score_padding=1e-9, certificate_positive_gap=TOL,
            max_depth=10, numerical_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['changed_acquisition_diagnostics'],indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'results/task4_current_acquisition')
    parser.add_argument("--prior-results",type=Path)
    parser.add_argument("--prior-model",default="V63")
    args=parser.parse_args()
    run(args.output,args.prior_results,args.prior_model)
