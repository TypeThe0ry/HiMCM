"""Potential data acquisition for champion exclusion, never admitted observations.

Fix the current evidence rectangle and weights. A city's upper score after
learning one utility is monotone, so its smallest possible upper score occurs
at the existing lower endpoint. Enumerate lower-endpoint bundles to determine
minimum cell count that COULD exclude a city; no assertion of likely observations.
"""
import argparse, hashlib, itertools, json
from pathlib import Path
import numpy as np
import pandas as pd
from task4_mexico_sampling_revision import mexico_sampling_bounds
from task4_v5_model import ROOT, CITIES, NAMES, weights, score

TOL=1e-12

def upper_after(row, indices, values, w):
    z=row.copy(); z[list(indices)]=values
    return float(score(z[None,:],w)[0])


def run(out):
    lo,hi=mexico_sampling_bounds(); config={'model_version':'V108','fixed_alpha':0.1}
    cells=[]; cities=[]; bundles=[]; checks=0; benchmark=[]
    for scenario,w in [('inherited',weights(config['fixed_alpha'])),('equal',np.ones(len(NAMES))/len(NAMES))]:
        lower=score(lo,w); upper=score(hi,w)
        for i,city in enumerate(CITIES):
            threshold=float(np.max(np.delete(lower,i)))
            unknown=np.flatnonzero(hi[i]-lo[i]>TOL)
            cityrow=dict(scenario=scenario,city=city,score_lower=lower[i],score_upper=upper[i],other_best_lower=threshold,
                uncertain_cells=len(unknown),all_uncertain_at_lower_excludes=bool(lower[i]<threshold-TOL))
            for j in unknown:
                new_lower=upper_after(lo[i],[j],[hi[i,j]],w)
                excluded=[c for q,c in enumerate(CITIES) if q!=i and upper[q]<new_lower-TOL]
                benchmark.append(dict(scenario=scenario,city=city,indicator=NAMES[j],hypothetical_new_lower=new_lower,excluded_other_count=len(excluded),excluded_others="|".join(excluded),closest_other_upper=float(np.min(np.delete(upper,i))),remaining_margin=float(np.min(np.delete(upper,i)))-new_lower))
                minimum=upper_after(hi[i],[j],[lo[i,j]],w)
                can=minimum<threshold-TOL
                left=right=None
                if can:
                    left,right=float(lo[i,j]),float(hi[i,j])
                    for _ in range(60):
                        mid=(left+right)/2
                        if upper_after(hi[i],[j],[mid],w)<threshold: left=mid
                        else:right=mid
                    # Finite probes verify monotonic implementation, not a formal proof.
                    vals=[upper_after(hi[i],[j],[x],w) for x in np.linspace(lo[i,j],hi[i,j],21)]
                    assert np.all(np.diff(vals)>=-TOL);checks+=1
                    assert upper_after(hi[i],[j],[lo[i,j]],w)<threshold-TOL
                cells.append(dict(scenario=scenario,city=city,indicator=NAMES[j],current_lower=lo[i,j],current_upper=hi[i,j],
                    original_upper_score=upper[i],minimum_post_upper=minimum,other_best_lower=threshold,
                    best_case_upper_score_reduction=upper[i]-minimum,remaining_exclusion_margin=minimum-threshold,
                    can_exclude_alone=can,threshold_lower=left,threshold_upper=right))
            minimum_size=None; successful=[]
            for count in range(1,len(unknown)+1):
                for comb in itertools.combinations(unknown,count):
                    post=upper_after(hi[i],comb,lo[i,list(comb)],w)
                    if post<threshold-TOL:
                        successful.append(dict(scenario=scenario,city=city,cell_count=count,indicators='|'.join(NAMES[j] for j in comb),
                            hypothetical_upper=post,other_best_lower=threshold,exclusion_margin=threshold-post))
                if successful:minimum_size=count;break
            cityrow['minimum_hypothetical_cells']=minimum_size
            cityrow['minimal_bundle_count']=len(successful)
            cities.append(cityrow);bundles.extend(successful)
    out.mkdir(parents=True,exist_ok=True)
    cell=pd.DataFrame(cells).sort_values(['scenario','remaining_exclusion_margin'])
    cf=pd.DataFrame(cities);bf=pd.DataFrame(bundles)
    pd.DataFrame(benchmark).sort_values(['scenario','remaining_margin']).to_csv(out/'single_cell_benchmark_raise.csv',index=False)
    cell.to_csv(out/'single_cell_thresholds.csv',index=False);cf.to_csv(out/'city_requirements.csv',index=False);bf.to_csv(out/'minimum_bundles.csv',index=False)
    summary=dict(evidence_model=config['model_version'],input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        scenarios=['inherited','equal'],actual_admitted_cells=0,actual_changed_bounds=0,
        single_cell_exclusions={s:int(g.can_exclude_alone.sum()) for s,g in cell.groupby('scenario')},
        single_cell_max_other_exclusions={s:int(g.excluded_other_count.max()) for s,g in pd.DataFrame(benchmark).groupby('scenario')},
        minimum_bundle_distribution={s:{str(k):int(v) for k,v in g.minimum_hypothetical_cells.value_counts(dropna=False).items()} for s,g in cf.groupby('scenario')},
        threshold_monotonic_probe_checks=checks,
        interpretation='Optimistic information acquisition for exclusion: hypothetical observed utilities at existing lower endpoints. Values are NOT data, probabilities or newly admitted bounds. Exact point observation is stronger than interval-valued evidence. Real observation may fail to exclude.',
        exclusion_rule='post_upper < max_other_existing_lower - 1e-12; endpoint equality retains a possible tied champion',
        invariant='All original data intervals, weights, transforms and registry remain unchanged.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2));return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'results/task4_v113_exclusion_priority');args=p.parse_args();run(args.output)
