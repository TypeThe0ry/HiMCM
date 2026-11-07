"""Cohort-count exclusion bounds; unknown historical exclusions stay unrestricted."""
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_istanbul_coverage_revision import istanbul_coverage_bounds
from task4_cohort_outcomes import outcome_feasible
from task4_v52_intake import verify_manifest


def bounded_counts(g,f,excluded_cap,extra_cap,known_g,known_f):
    vals=[g,f,excluded_cap,extra_cap,known_g,known_f]
    if not all(np.isfinite(x) and x>=0 and x==int(x) for x in vals):
        raise ValueError('Nonnegative integer counts required')
    return max(known_g,g-excluded_cap-extra_cap),max(known_f,f-excluded_cap-extra_cap)


def checks():
    # Enumerate every possible excluded outcome composition, not only one label match.
    for g in range(7):
        for f in range(7):
            for cap in range(g+f+1):
                low_g,low_f=bounded_counts(g,f,cap,0,0,0)
                for eg in range(g+1):
                    for ef in range(f+1):
                        if eg+ef<=cap:
                            assert low_g<=g-eg and low_f<=f-ef
    # More unbounded historical exclusions cannot improve either lower count.
    assert bounded_counts(4813,1472,485,6285,655,263)==(655,263)
    assert bounded_counts(4813,1472,485,0,655,263)==(4328,987)


def main():
    checks()
    source=ROOT/'data/task4_v55_phoenix_outcomes'
    verify_manifest(source)
    data=json.loads((source/'pxu_graduation_fy2025.json').read_text())
    district=next(r for r in data if r['studentGroupDescription']=='All')
    digital=next(r for r in json.loads((ROOT/'data/task4_v9_phoenix/spatial_responses/875776.json').read_text()) if r['studentGroupDescription']=='All')
    assert district['numInCohort']==6285 and district['numGraduated']==4813
    assert digital['numInCohort']==485 and digital['numGraduated']==286
    state=next(r for r in json.loads((ROOT/'data/task4_v9_phoenix/state_graduation_2025.json').read_text()) if r['studentGroupDescription']=='All')
    gs=state['numGraduated'];fs=state['numInCohort']-gs
    assert (gs,fs)==(74261,20240)
    schools=pd.read_csv(ROOT/'data/task4_v9_phoenix/expanded_known_cohort_bounds.csv')
    known_g=int(schools.graduates_lower.max());known_f=int((schools.cohort-schools.graduates_upper).max())
    assert (known_g,known_f)==(655,263)
    lo,hi=istanbul_coverage_bounds();lo=np.c_[lo,np.zeros(25)];hi=np.c_[hi,np.ones(25)]
    ny=json.loads((ROOT/'data/task4_v52_nyc_outcomes/summary.json').read_text())
    ni=CITIES.index('New York');lo[ni,-1],hi[ni,-1]=ny['lower'],ny['upper']
    p=CITIES.index('Phoenix');w=np.r_[.9*weights(),.1]
    cases=[('unresolved_historical_exclusions',6285),('no_extra_exclusions_assumed',0),
           ('nongraduate_gain_boundary',724),('graduate_gain_boundary',3673)]
    rows=[];frames=[];baseline=None
    for label,budget in cases+[('status_compatibility_also_assumed',0)]:
        g,f=bounded_counts(4813,1472,485,budget,known_g,known_f)
        if label=='status_compatibility_also_assumed':g,f=4527,1273
        ql,qu=g/(g+fs),gs/(gs+f)
        l,h=lo.copy(),hi.copy();l[p,-1],h[p,-1]=ql,qu
        rank,d=summarize(l,h,w)
        if baseline is None:baseline=rank.copy()
        rank['scenario']=label;frames.append(rank)
        rows.append(dict(scenario=label,additional_excluded_cohort_cap=budget,
            unique_graduates_lower=g,unique_nongraduates_lower=f,outcome_lower=ql,outcome_upper=qu,
            phoenix=rank.iloc[p][['score_lower','score_upper','decision_rank','max_regret']].to_dict(),
            changed_ranks_vs_unresolved=int((rank.decision_rank!=baseline.decision_rank).sum()),
            possible_champions=int(rank.possible_champion.sum()),
            continuous_possible=sum(outcome_feasible(h[k],l[np.arange(25)!=k],.1)['possible'] for k in range(25))))
    old=json.loads((ROOT/'results/task4_v14_duplicate_budget/summary.json').read_text())['scenarios'][-1]
    np.testing.assert_allclose([rows[0]['outcome_lower'],rows[0]['outcome_upper']],
                               [old['quality_lower'],old['quality_upper']],rtol=0,atol=1e-12)
    out=ROOT/'results/task4_v56_pxu_exclusion';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    main_rank,main_decision=summarize(lo[:,:10],hi[:,:10],weights())
    previous=pd.read_csv(ROOT/'results/task4_v55_recommendation_acquisition/ranks.csv')
    for key in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(main_rank[key],previous[key],rtol=0,atol=1e-12)
    main_rank.to_csv(out/'main_ranks.csv',index=False)
    report=dict(main_choice=[CITIES[k] for k in main_decision['minimax_choices']],
        main_possible_champions=int(main_rank.possible_champion.sum()),main_model_changed=False,city_bound_upgraded=False,main_admitted=False,
        baseline_ten_criteria='V53',outcome_weight=.1,extra_exclusion_cap_observed=False,
        conditional_pxu_scenarios_require_unique_compatible_membership=True,
        fallback_does_not_require_pxu_compatibility=True,scenarios=rows)
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(rows,indent=2))


if __name__=='__main__':main()
