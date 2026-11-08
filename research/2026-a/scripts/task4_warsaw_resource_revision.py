"""Warsaw complete youth-stage school resources with adult allocation retained.

Conditional on school-location, source-stage scope and unit rounding.
A year-only comparison separates the new school coverage from the year update.
Rollback restores the prior general-school bounds; strict withdrawal uses [0,1].
"""
import contextlib
import hashlib
import importlib.util
import io
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_phoenix_monitor_revision import phoenix_monitor_bounds
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def source():
    folder=ROOT/'data/task4_v96_warsaw'
    saved=json.loads((folder/'summary.json').read_text())
    spec=importlib.util.spec_from_file_location('warsaw96_education',folder/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    with contextlib.redirect_stdout(io.StringIO()):
        actual=module.extract()
    if actual != saved:
        raise ValueError('Warsaw resource summary does not reproduce from original sources')
    return actual


def warsaw_bounds():
    lo,hi=phoenix_monitor_bounds()
    result=source();i,j=CITIES.index('Warsaw'),NAMES.index('upper_secondary_ptr')
    assert lo[i,j]==0
    np.testing.assert_allclose(hi[i,j],0.5089314114476085,rtol=0,atol=1e-15)
    total=result['students_total'];a,b=result['teacher_fte_bounds']
    assert total==119740 and 0<=a<=b
    lo[i,j],hi[i,j]=15*a/(total+15*a),15*b/(total+15*b)
    np.testing.assert_allclose([lo[i,j],hi[i,j]],result['utility_bounds'],rtol=0,atol=1e-15)
    return lo,hi


def main():
    before=phoenix_monitor_bounds();after=warsaw_bounds()
    i,j=CITIES.index('Warsaw'),NAMES.index('upper_secondary_ptr')
    mask=np.ones(before[0].shape,bool);mask[i,j]=False
    for old,new in zip(before,after):
        np.testing.assert_array_equal(old[mask],new[mask])
    rollback=tuple(a.copy() for a in after)
    for a,b in zip(rollback,before):a[i,j]=b[i,j]
    for a,b in zip(rollback,before):np.testing.assert_array_equal(a,b)
    strict=tuple(a.copy() for a in after);strict[0][i,j]=0;strict[1][i,j]=1
    general=tuple(a.copy() for a in before);r=source()
    n=r['students_by_route']['general_youth'];t=r['teacher_fte_published']['general_including_adults']+r['rounding_guard_per_cell']
    general[0][i,j]=0;general[1][i,j]=15*t/(n+15*t)
    baseline,_=summarize(*before,weights())
    frames=[];bounds=[];reports=[];certificates=[]
    for label,(lo,hi) in [('v91_before',before),('v96_general_year_only',general),('v96_warsaw_resources',after),('strict_scope_withdrawal',strict)]:
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
            unresolved_leaves=sum(not c['certified'] for c in cert),warsaw=frame.iloc[i].to_dict()))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=lo[k,h],upper=hi[k,h])
            for k,c in enumerate(CITIES) for h,n in enumerate(NAMES))
    out=ROOT/'results/task4_v96_warsaw_revision';out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    pd.concat(frames).pivot(index='city',columns='scenario',values='decision_rank').to_csv(out/'rank_comparison.csv')
    result=dict(model_version='V96',previous_model_version='V91',main_admitted=True,
        admission='Conditional complete source-defined youth-stage school resources, all ownership. Adult general teacher allocation remains unknown; one-FTE outward unit-rounding guard. Not exact age14-18 resident learning quality.',
        source_summary_sha256=hashlib.sha256((ROOT/'data/task4_v96_warsaw/summary.json').read_bytes()).hexdigest(),
        changed_indicator='Warsaw/upper_secondary_ptr only',unchanged_cells=249,student_travel_unchanged=True,
        prior_scope_rollback_verified=True,strict_scope_uses_unidentified_interval=True,scenarios=reports)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(reports,indent=2))


if __name__=='__main__':main()
