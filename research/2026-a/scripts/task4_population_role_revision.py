"""Separate subgroup identification and teacher-role corrections with a factorial audit."""
import importlib.util
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_tokyo_special_revision import tokyo_special_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify
from task4_subgroup_bounds import subgroup_bounds


def observation(folder):
    path=ROOT/'data'/folder
    spec=importlib.util.spec_from_file_location(folder+'_extract',path/'extract.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    r=module.extract()
    assert r==json.loads((path/'summary.json').read_text()),'Refresh '+folder
    return r


def revised_bounds(travel=True,roles=True,role_mode="main"):
    lo,hi=tokyo_special_bounds()
    if travel:
        r=observation('task4_v70_singapore')
        # Unknown target subgroup mass does not inherit the whole-group mean.
        counts=r['secondary_counts']
        lower=np.exp(-np.array([15,30,45,60,np.inf])/30)
        upper=np.exp(-np.array([0,15,30,45,60])/30)
        bound=subgroup_bounds(counts,lower,upper,r['target_mass_interval'])
        np.testing.assert_allclose(bound,r['revised_travel_interval'],rtol=0,atol=1e-15)
        counter=r['counterexample_mass80000']
        np.testing.assert_allclose(subgroup_bounds(counts,lower,upper,[counter['mass'],counter['mass']]),[counter['lower'],counter['upper']],rtol=0,atol=1e-12)
        i,j=CITIES.index('Singapore'),NAMES.index('travel')
        np.testing.assert_allclose([lo[i,j],hi[i,j]],r['previous_mixed_stage_envelope'],rtol=0,atol=1e-12)
        lo[i,j],hi[i,j]=bound
    if roles:
        r=observation('task4_v70_tokyo')
        n0,n1=r['students_interval'];t0,t1=r['teachers_interval']
        np.testing.assert_allclose(r['utility_interval'],[15*t0/(n1+15*t0),15*t1/(n0+15*t1)],rtol=0,atol=1e-15)
        key={'main':'utility_interval','coarse':'coarse_utility_interval','role_only':'role_only_utility_interval'}[role_mode]
        i,j=CITIES.index('Tokyo'),NAMES.index('upper_secondary_ptr')
        np.testing.assert_allclose([lo[i,j],hi[i,j]],r['prior_utility_interval'],rtol=0,atol=1e-12)
        lo[i,j],hi[i,j]=r[key]
    return lo,hi


def main():
    old=tokyo_special_bounds();base,_=summarize(*old,weights())
    mask=np.ones(old[0].shape,bool)
    mask[CITIES.index('Singapore'),NAMES.index('travel')]=False
    mask[CITIES.index('Tokyo'),NAMES.index('upper_secondary_ptr')]=False
    frames=[];bounds=[];reports=[];certificates=[]
    for label,travel,roles,mode in [('v69_before',False,False,'main'),('subgroup_only',True,False,'main'),('roles_only',False,True,'main'),('v70_both',True,True,'main'),('all_private_allocation_unknown',True,True,'coarse'),('ignore_advanced_course_allocation',True,True,'role_only')]:
        lo,hi=revised_bounds(travel,roles,mode)
        np.testing.assert_array_equal(lo[mask],old[0][mask]);np.testing.assert_array_equal(hi[mask],old[1][mask])
        assert np.all((0<=lo)&(lo<=hi)&(hi<=1))
        f,d=summarize(lo,hi,weights());f['scenario']=label;frames.append(f)
        cert=certify(lo,hi)
        for r in cert:r.update(scenario=label,city=None if r['winner'] is None else CITIES[r['winner']])
        certificates.extend(cert)
        reports.append(dict(scenario=label,changed_cells=int(((lo!=old[0])|(hi!=old[1])).sum()),
            choice=[CITIES[k] for k in d['minimax_choices']],changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v69=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            selected_cities=f[f.city.isin(['Singapore','Tokyo','Phoenix'])][['city','decision_rank','score_lower','score_upper','max_regret']].to_dict('records'),
            possible_champions=f.loc[f.possible_champion,'city'].tolist(),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible']],
            continuous_recommendation=dict(unresolved_leaves=sum(not r['certified'] for r in cert),winners=sorted({r['city'] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(lo[i,j]),upper=float(hi[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v70_population_roles';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificates).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version='V70',main_admitted=False,current_scenario='v70_both',baseline='V69',
        other_unchanged_cells=int(mask.sum()),alpha_fixed=.1,alpha_range=[.05,.2],scenarios=reports)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
