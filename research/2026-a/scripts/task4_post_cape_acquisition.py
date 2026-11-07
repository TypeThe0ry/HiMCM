"""Update acquisition diagnostics against V30 actual high-school evidence, without imputation."""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize,score
from task4_cape_town_revision import cape_bounds
from task4_robust_acquisition import bundles
from task4_champion_acquisition import certificates
from task4_continuous_preferences import feasible_preferences


def main():
    lo,hi=cape_bounds();saved=(lo.copy(),hi.copy())
    fixed,_=certificates(lo,hi,weights(),NAMES,CITIES)
    robust,details=bundles(lo,hi)
    collapsed,_=bundles(lo,hi,.1,.1)
    diagnostics=[]
    for i,city in enumerate(CITIES):
        n=fixed[i]['minimum_city_local_exact_measurements']
        assert n==collapsed[i]['minimum_measurements']
        assert robust[i]['minimum_measurements'] is None or robust[i]['minimum_measurements']>=n
        robust[i]['fixed_weight_minimum']=n
        rivals=np.arange(len(lo))!=i
        for label,names in [('travel_only',['travel']),('education_only',['upper_secondary_ptr']),('education_and_travel',['upper_secondary_ptr','travel'])]:
            js=[NAMES.index(x) for x in names]
            favorable=hi[i].copy();favorable[js]=lo[i,js]
            upper=float(score(favorable[None,:],weights())[0]);threshold=float(score(lo[rivals],weights()).max())
            possible=feasible_preferences(favorable,lo[rivals])['possible']
            diagnostics.append(dict(city=city,measurement_bundle=label,hypothetical_upper_score=upper,rival_lower_threshold=threshold,
                can_exclude_fixed=upper<threshold-1e-12,can_exclude_all_preferences=not possible))
    np.testing.assert_array_equal(lo,saved[0]);np.testing.assert_array_equal(hi,saved[1])
    # Quantify how strong adverse measurements must be, rather than reporting
    # only feasibility at exact lower endpoints. These are planning scenarios.
    thresholds=[]
    i=CITIES.index('Phoenix');rivals=lo[np.arange(len(lo))!=i]
    for bundle in details:
        if bundle['city']!='Phoenix':continue
        js=[NAMES.index(n) for n in bundle['indicators'].split('|')]
        def remains_possible(fraction):
            hypothetical=hi[i].copy()
            hypothetical[js]-=fraction*(hi[i,js]-lo[i,js])
            return feasible_preferences(hypothetical,rivals)['possible']
        assert remains_possible(0) and not remains_possible(1)
        left,right=0.,1.
        for _ in range(40):
            middle=(left+right)/2
            if remains_possible(middle):left=middle
            else:right=middle
        assert remains_possible(left) and not remains_possible(right)
        thresholds.append(dict(city='Phoenix',indicators=bundle['indicators'],
            still_possible_fraction=left,excluded_fraction=right,
            bracket_width=right-left))
    rank,d=summarize(lo,hi,weights())
    old=pd.read_csv(ROOT/'results/task4_v30_cape_town/ranks.csv');old=old[old.scenario=='age14_18_sampling'].reset_index(drop=True)
    assert old.city.tolist()==rank.city.tolist()
    for c in ['score_lower','score_upper','decision_rank','max_regret']:np.testing.assert_allclose(rank[c],old[c],rtol=0,atol=1e-12)
    out=ROOT/'results/task4_v31_acquisition';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(robust).to_csv(out/'minimum_measurements.csv',index=False)
    pd.DataFrame(details).to_csv(out/'minimal_bundles.csv',index=False)
    pd.DataFrame(diagnostics).to_csv(out/'education_travel_diagnostics.csv',index=False)
    rank.to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(thresholds).to_csv(out/'phoenix_resolution_thresholds.csv',index=False)
    prior=pd.read_csv(ROOT/'results/task4_v27_current_acquisition/minimum_measurements.csv')
    previous_minimum={r['city']:(None if pd.isna(r['minimum_measurements']) else int(r['minimum_measurements'])) for r in prior.to_dict('records')}
    summary=dict(new_observations=0,baseline='V30 cape_bounds; actual age14-18 high-school travel with sampling envelope',alpha_range=[.05,.2],
        possible_champions=int(rank.possible_champion.sum()),choice=[CITIES[i] for i in d['minimax_choices']],
        rank_changes_vs_v30=0,phoenix=robust[CITIES.index('Phoenix')],
        education_travel_excludable_fixed=[r['city'] for r in diagnostics if r['measurement_bundle']=='education_and_travel' and r['can_exclude_fixed']],
        education_travel_excludable_all_preferences=[r['city'] for r in diagnostics if r['measurement_bundle']=='education_and_travel' and r['can_exclude_all_preferences']],
        changed_minimum_vs_v27=[dict(city=r['city'],before=previous_minimum[r['city']],after=r['minimum_measurements']) for r in robust if r['minimum_measurements']!=previous_minimum[r['city']]],
        input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),
        interpretation='Favorable lower-endpoint exact outcomes are hypothetical feasibility certificates, not observations or guaranteed acquisition benefits. Education here is the existing pupil-teacher-ratio criterion, not a new graduation-rate criterion.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
