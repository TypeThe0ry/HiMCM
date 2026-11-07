"""Minimum city-local acquisition bundles over continuous group preferences.

Hypothetical lower-endpoint outcomes diagnose feasibility, never update evidence.
"""
import itertools
import json
import numpy as np
import pandas as pd
from task4_continuous_preferences import feasible_preferences
from task4_champion_acquisition import certificates
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,NAMES,weights


def bundles(lower,upper,alpha_min=.05,alpha_max=.2):
    lo=np.asarray(lower);hi=np.asarray(upper);rows=[];details=[]
    for i,city in enumerate(CITIES):
        rivals=lo[np.arange(len(lo))!=i]
        unknown=np.flatnonzero(hi[i]-lo[i]>1e-12)
        winners=[];minimum=None
        for n in range(len(unknown)+1):
            for subset in itertools.combinations(unknown,n):
                hypothetical=hi[i].copy();hypothetical[list(subset)]=lo[i,list(subset)]
                if not feasible_preferences(hypothetical,rivals,alpha_min,alpha_max)['possible']:
                    winners.append(subset)
                    details.append(dict(city=city,size=n,indicators='|'.join(NAMES[j] for j in subset)))
            if winners:minimum=n;break
        rows.append(dict(city=city,minimum_measurements=minimum,minimal_bundle_count=len(winners)))
    return rows,details


def main():
    lo,hi,_=apply_bounds(*baseline(),collect());saved=(lo.copy(),hi.copy())
    fixed,_=certificates(lo,hi,weights(),NAMES,CITIES)
    rows,details=bundles(lo,hi)
    # Collapsed preference range must reproduce the existing fixed-weight result.
    collapsed,_=bundles(lo,hi,.1,.1)
    for f,c,r in zip(fixed,collapsed,rows):
        n=f['minimum_city_local_exact_measurements']
        assert n==c['minimum_measurements'],(f,c)
        assert r['minimum_measurements'] is None or (n is not None and r['minimum_measurements']>=n)
        r['fixed_weight_minimum']=n
    assert np.array_equal(lo,saved[0]) and np.array_equal(hi,saved[1])
    out=ROOT/'results/task4_v8_robust_acquisition';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(rows).to_csv(out/'minimum_measurements.csv',index=False)
    pd.DataFrame(details).to_csv(out/'minimal_bundles.csv',index=False)
    summary=dict(new_observations=0,alpha_range=[.05,.2],changed_minimum=[r for r in rows if r['minimum_measurements']!=r['fixed_weight_minimum']],
                 validation='25 collapsed-range comparisons match fixed-weight method; robust count cannot decrease; evidence arrays unchanged',
                 caveat='Minimum counts assume favorable exact measurements of this city only. Outcomes are hypothetical, not guaranteed; field acquisition may yield intervals, and evidence costs are not estimated.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
