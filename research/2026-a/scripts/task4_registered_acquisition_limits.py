"""Current-registry bounds on what perfect future measurements can resolve.

These are universally unavoidable candidates, not attainable joint minima.
No synthetic measurement is admitted to the model.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES
from task4_current_model import current_bounds,run as run_current
from task4_acquisition_limits import certificate
from task4_joint_uncertainty_stress import protect_output


ANALYSIS_KIND = 'current_acquisition_limits'


def protect_analysis(out,lo,hi,config):
    summary=out/'summary.json'
    if summary.exists() and json.loads(summary.read_text()).get('analysis_kind') != ANALYSIS_KIND:
        raise ValueError('Refusing to overwrite a different analysis kind')
    protect_output(out,lo,hi,config)


def run(out):
    lo,hi,config=current_bounds()
    protect_analysis(out,lo,hi,config)
    run_current(out/'baseline')
    saved=np.stack([lo,hi]).copy()
    education,travel=NAMES.index('upper_secondary_ptr'),NAMES.index('travel')
    scopes=[('all_education',[education],None),('all_travel',[travel],None),
            ('all_education_and_travel',[education,travel],None),
            ('phoenix_education_and_travel',[education,travel],CITIES.index('Phoenix'))]
    scopes += [('both_plus_'+name,[education,travel,j],None) for j,name in enumerate(NAMES) if j not in (education,travel)]
    rows=[];summaries=[]
    for label,indicators,city in scopes:
        mask=np.zeros_like(lo,bool)
        if city is None:mask[:,indicators]=True
        else:mask[city,indicators]=True
        result=certificate(lo,hi,mask,config['fixed_alpha'],config['alpha_range'])
        rows.extend(dict(scenario=label,city=CITIES[r['index']],**r) for r in result)
        fixed=[CITIES[r['index']] for r in result if r['fixed_unavoidable']]
        continuous=[CITIES[r['index']] for r in result if r['continuous_unavoidable']]
        summaries.append(dict(scenario=label,measured_indicators=[NAMES[j] for j in indicators],selected_cells=int(mask.sum()),currently_nonpoint_cells=int((mask & (lo<hi)).sum()),fixed_unavoidable_cities=fixed,continuous_unavoidable_cities=continuous,fixed_champion_count_lower_bound=max(1,len(fixed)),continuous_champion_count_lower_bound=max(1,len(continuous))))
    np.testing.assert_array_equal(np.stack([lo,hi]),saved)
    pd.DataFrame(rows).to_csv(out/'certificates.csv',index=False)
    summary=dict(analysis_kind=ANALYSIS_KIND,model_version=config['model_version'],fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],input_bounds_sha256=hashlib.sha256(saved.astype('<f8').tobytes()).hexdigest(),new_observations=0,main_admitted=False,scenario_only=True,count_bound_is_not_generally_joint_minimum=True,claim='Under every exact revelation of selected cells within their current intervals, named cities remain possible champions; all other bounds fixed. Different cities may have different preference witnesses.',scenarios=summaries)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps([dict(scenario=r['scenario'],fixed=r['fixed_champion_count_lower_bound'],continuous=r['continuous_champion_count_lower_bound']) for r in summaries],indent=2))
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args().output)
