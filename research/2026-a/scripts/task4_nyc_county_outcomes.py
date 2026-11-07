"""Current-input completion diagnostic; county coverage is distinct from DOE scope."""
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds
from task4_cohort_outcomes import outcome_feasible
from task4_v52_intake import verify_manifest


def main():
    folder=ROOT/'data/task4_v52_nyc_outcomes';verify_manifest(folder)
    evidence=json.loads((folder/'summary.json').read_text())
    observed=evidence.get('nyc_counties',evidence)
    counties=pd.read_csv(folder/'county_outcomes.csv')
    selected=counties[counties.period=='august2025']
    assert len(selected)==5 and selected.county_code.nunique()==5
    for column,target in [('cohort','cohort'),('graduates','graduates'),('unclassified_residual','unknown_outcomes')]:
        assert selected[column].sum()==observed[target]
    assert observed['cohort']==78918 and observed['graduates']==63878
    assert observed['unknown_outcomes']==56
    assert abs(observed['lower']-63878/78918)<1e-12
    assert abs(observed['upper']-(63878+56)/78918)<1e-12
    lo,hi=saopaulo_age_bounds()
    l=np.column_stack([lo,np.zeros(len(lo))]);h=np.column_stack([hi,np.ones(len(hi))])
    phoenix=json.loads((ROOT/'results/task4_v14_duplicate_budget/summary.json').read_text())['scenarios'][-1]
    p=CITIES.index('Phoenix');i=CITIES.index('New York')
    l[p,-1],h[p,-1]=phoenix['quality_lower'],phoenix['quality_upper']
    old=json.loads((ROOT/'data/task4_v18_nyc_quality/graduation_summary.json').read_text())['scopes']['2025']
    frames=[];stats=[]
    for beta in [0,.05,.1,.2]:
        baseline=None
        for label,row in [('county_target_outcome_unknown',None),('nyc_counties_observed',observed),('doe_charter_excluded_reference',old)]:
            a,b=l.copy(),h.copy()
            if row is not None:a[i,-1],b[i,-1]=row['lower'],row['upper']
            np.testing.assert_array_equal(a[:,:10],lo);np.testing.assert_array_equal(b[:,:10],hi)
            w=np.r_[(1-beta)*weights(),beta]
            f,d=summarize(a,b,w)
            if baseline is None:baseline=f.copy()
            f['scenario']=label;f['outcome_weight']=beta;frames.append(f)
            stats.append(dict(scenario=label,outcome_weight=beta,
                nyc=f.iloc[i][['score_lower','score_upper','decision_rank','max_regret']].to_dict(),
                changed_ranks_vs_unknown=int((f.decision_rank!=baseline.decision_rank).sum()),
                choice=[CITIES[k] for k in d['minimax_choices']],
                possible_champions=int(f.possible_champion.sum()),
                continuous_possible=sum(outcome_feasible(b[k],a[np.arange(len(a))!=k],beta)['possible'] for k in range(len(a)))))
            if beta==0:
                original,_=summarize(lo,hi,weights())
                for c in ['score_lower','score_upper','decision_rank','max_regret']:
                    np.testing.assert_allclose(f[c],original[c],rtol=0,atol=1e-12)
    out=ROOT/'results/task4_v52_nyc_county_outcomes';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_model_changed=False,main_admitted=False,baseline_ten_criteria='V48 current bounds',
        interpretation='Separate administrative diploma completion criterion; local credentials and accountability geography remain conditional',
        new_nyc_outcome=[observed['lower'],observed['upper']],scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([r for r in stats if r['outcome_weight']==.1],indent=2))


if __name__=='__main__':main()
