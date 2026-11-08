"""Phoenix incorporated-city monitor envelope, conditional on network comparison.

The quantity is a convex weighting of complete observed monitor annual means,
not a bound on resident or high-school exposure. Strict scope withdrawal restores
[0,1]. Other249 indicator cells and all student travel intervals are unchanged.
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_delhi_allocation_revision import delhi_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def source():
    folder=ROOT/'data/task4_v91_phoenix_air'
    saved=json.loads((folder/'summary.json').read_text())
    spec=importlib.util.spec_from_file_location('phoenix91_air',folder/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    with contextlib.redirect_stdout(io.StringIO()):
        actual=module.main()
    if actual != saved:
        raise ValueError('Phoenix monitor summary does not reproduce from original sources')
    return actual


def phoenix_monitor_bounds():
    lo,hi=delhi_bounds()
    result=source();i,j=CITIES.index('Phoenix'),NAMES.index('pm25')
    assert lo[i,j]==0 and hi[i,j]==1
    a,b=result['concentration_convex_hull']
    assert 0<=a<=b and result['all_complete_and_certified']
    lo[i,j],hi[i,j]=15/(15+b),15/(15+a)
    np.testing.assert_allclose([lo[i,j],hi[i,j]],result['utility_convex_hull'],rtol=0,atol=1e-15)
    return lo,hi


def main():
    before=delhi_bounds();after=phoenix_monitor_bounds()
    i,j=CITIES.index('Phoenix'),NAMES.index('pm25')
    mask=np.ones(before[0].shape,bool);mask[i,j]=False
    for old,new in zip(before,after):
        np.testing.assert_array_equal(old[mask],new[mask])
    strict=tuple(a.copy() for a in after);strict[0][i,j]=0;strict[1][i,j]=1
    for a,b in zip(strict,before):np.testing.assert_array_equal(a,b)
    baseline,_=summarize(*before,weights())
    frames=[];bounds=[];reports=[];certificates=[]
    for label,(lo,hi) in [('v79_before',before),('v91_monitor_envelope',after),('strict_scope_withdrawal',strict)]:
        frame,decision=summarize(lo,hi,weights());frame['scenario']=label;frames.append(frame)
        cert=certify(lo,hi)
        for row in cert:
            row.update(scenario=label,city=None if row['winner'] is None else CITIES[row['winner']])
        certificates.extend(cert)
        continuous=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(CITIES))!=k])['possible']]
        reports.append(dict(scenario=label,changed_cells=int(((lo!=before[0])|(hi!=before[1])).sum()),
            changed_ranks=int((frame.decision_rank!=baseline.decision_rank).sum()),
            kendall_tau_vs_before=float(kendalltau(frame.decision_rank,baseline.decision_rank).statistic),
            possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=continuous,
            minimax_choices=[CITIES[k] for k in decision['minimax_choices']],
            continuous_recommendation=sorted({c['city'] for c in cert if c['certified']}),
            unresolved_leaves=sum(not c['certified'] for c in cert),phoenix=frame.iloc[i].to_dict()))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[k,h],upper=hi[k,h])
            for k,c in enumerate(CITIES) for h,n in enumerate(NAMES))
    out=ROOT/'results/task4_v91_phoenix_monitor';out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    pd.concat(frames).pivot(index='city',columns='scenario',values='decision_rank').to_csv(out/'rank_comparison.csv')
    result=dict(model_version='V91',previous_model_version='V79',main_admitted=True,
        admission='Conditional incorporated-city observed-monitor mean comparison. Not population or high-school exposure.',
        source_summary_sha256=hashlib.sha256((ROOT/'data/task4_v91_phoenix_air/summary.json').read_bytes()).hexdigest(),
        changed_indicator='Phoenix/pm25 only',unchanged_cells=249,student_travel_unchanged=True,
        strict_scope_restores_previous_model=True,scenarios=reports)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(reports,indent=2))


if __name__=='__main__':main()
