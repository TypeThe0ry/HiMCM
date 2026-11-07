"""Bound a city accountability cohort from disjoint, verified school subsets.

The administrative last-school rule supplies disjointness. Unknown schools
remain in the statewide outcome caps; this is not a complete-city point rate.
"""
import hashlib,json,itertools
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_istanbul_coverage_revision import istanbul_coverage_bounds
from task4_cohort_outcomes import outcome_feasible


def rate_bounds(g,f,state_g,state_f):
    assert 0<=g<=state_g and 0<=f<=state_f and state_g>0 and state_f>0
    return g/(g+state_f),state_g/(state_g+f)


def partition_compatible(known_school_cohorts,district_cohort):
    """Necessary accounting check only: passing does not prove a partition."""
    assert all(n>=0 and n==int(n) for n in known_school_cohorts)
    return sum(known_school_cohorts)<=district_cohort


def checks():
    assert not partition_compatible([5802,485],6285)
    assert partition_compatible([5800,485],6285)
    # Every completion of a small partial school union stays within its bounds.
    for g,f,other_g,other_f in itertools.product(range(5),repeat=4):
        if g+f+other_g+other_f==0:continue
        low,high=rate_bounds(g,f,max(1,g+other_g),max(1,f+other_f))
        actual=(g+other_g)/(g+f+other_g+other_f)
        assert low-1e-12<=actual<=high+1e-12


def main():
    checks();folder=ROOT/'data/task4_v57_school_union'
    for item in json.loads((folder/'manifest.json').read_text())+json.loads((folder/'refresh_manifest.json').read_text()):
        raw=(folder/item['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        assert len(raw)==item['bytes']
    join=pd.read_csv(folder/'identity_join.csv',dtype={'nces_id':str})
    assert join.entity_id.is_unique and join.nces_id.is_unique
    unresolved_identity=join.loc[~join.identity_verified,'entity_id'].tolist()
    join=join[join.identity_verified]
    assert join.catalog_city_verified.all()
    assert not (join.entity_id==875776).any()
    rows=[]
    for r in join.to_dict('records'):
        entity=json.loads((folder/r['entity_file']).read_text())[0]
        assert str(entity['leances'])+str(entity['nces']).zfill(5)==r['nces_id']
        assert entity['leaEducationOrganizationId']==4286
        source=ROOT/'data'/r['cohort_source']
        records=[a for a in json.loads(source.read_text()) if a.get('studentGroupDescription')=='All']
        refreshed=[a for a in json.loads((folder/f"refreshed/{r['entity_id']}.json").read_text()) if a.get('studentGroupDescription')=='All']
        assert records==refreshed,'Snapshot changed; review before using cached observations'
        assert len(records)==r['all_rows']<=1
        row=dict(entity_id=r['entity_id'],nces_id=r['nces_id'],name=r['catalog_name'],
                 graduates_lower=0,nongraduates_lower=0,cohort=None,graduates_upper=None,status='no_All_row')
        if records:
            a=records[0]
            assert a['fiscalYear']==2025 and a['educationOrganizationId']==r['entity_id']
            n=a['numInCohort'];g=a['numGraduated']
            if n>=0:
                assert n==int(n)
                if g>=0:
                    assert g==int(g) and g<=n
                    gl=gu=int(g);status='observed_count'
                else:gl,gu,status=0,int(n),'suppressed_outcome_0_to_n'
                row.update(cohort=int(n),graduates_lower=gl,graduates_upper=gu,
                           nongraduates_lower=int(n)-gu,status=status)
            else:row['status']='suppressed_cohort_no_lower_contribution'
        rows.append(row)
    school=pd.DataFrame(rows);school.to_csv(folder/'school_bounds.csv',index=False)
    g=int(school.graduates_lower.sum());f=int(school.nongraduates_lower.sum())
    def all_row(eid):
        a=[r for r in json.loads((folder/f'refreshed/{eid}.json').read_text()) if r.get('studentGroupDescription')=='All']
        assert len(a)==1 and a[0]['fiscalYear']==2025
        return a[0]
    district=all_row(4286);digital=all_row(875776)
    school_n=int(school.cohort.sum())
    compatible=partition_compatible([school_n,digital['numInCohort']],district['numInCohort'])
    state=next(a for a in json.loads((ROOT/'data/task4_v9_phoenix/state_graduation_2025.json').read_text()) if a['studentGroupDescription']=='All')
    assert state['fiscalYear']==2025
    sg=state['numGraduated'];sf=state['numInCohort']-sg
    ql,qu=rate_bounds(g,f,sg,sf)
    lo,hi=istanbul_coverage_bounds();core,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v56_pxu_exclusion/main_ranks.csv')
    assert core.city.tolist()==prior.city.tolist()
    for col in ['score_lower','score_upper','max_regret','decision_rank']:
        np.testing.assert_allclose(core[col],prior[col],atol=1e-12,rtol=0)
    l=np.c_[lo,np.zeros(len(lo))];h=np.c_[hi,np.ones(len(hi))]
    ny=json.loads((ROOT/'data/task4_v52_nyc_outcomes/summary.json').read_text())
    ni=CITIES.index('New York');l[ni,-1],h[ni,-1]=ny['lower'],ny['upper']
    p=CITIES.index('Phoenix');frames=[];summaries=[]
    for beta in [.05,.1,.2]:
        for label,interval in [('retained_unrestricted_overlap',rate_bounds(655,263,sg,sf)),('unreconciled_union_candidate',(ql,qu))]:
            ll,hh=l.copy(),h.copy();ll[p,-1],hh[p,-1]=interval
            rank,d=summarize(ll,hh,np.r_[(1-beta)*weights(),beta])
            rank['scenario']=label;rank['outcome_weight']=beta;frames.append(rank)
            summaries.append(dict(scenario=label,outcome_weight=beta,
                phoenix=rank.iloc[p][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
                choice=[CITIES[k] for k in d['minimax_choices']],
                possible_champions=int(rank.possible_champion.sum()),
                continuous_possible_champions=sum(outcome_feasible(hh[k],ll[np.arange(len(ll))!=k],beta)['possible'] for k in range(len(ll)))))
    out=ROOT/'results/task4_v57_school_union';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);core.to_csv(out/'main_ranks.csv',index=False)
    summary=dict(core_version='V53',core_changed_cells=0,core_changed_ranks=0,
        core_choice=[CITIES[k] for k in decision['minimax_choices']],core_possible_champions=int(core.possible_champion.sum()),
        target='Public non-fully-virtual school-location administrative cohort2024; not residents or private schools',
        unresolved_identity_entities=unresolved_identity,unique_school_entities=len(school),schools_with_known_cohort=int(school.cohort.notna().sum()),
        known_subset_cohort=int(school.cohort.sum()),graduates_lower=g,nongraduates_lower=f,
        state_graduates=sg,state_nongraduates=sf,outcome_lower=ql,outcome_upper=qu,
        old_lower=rate_bounds(655,263,sg,sf)[0],old_upper=rate_bounds(655,263,sg,sf)[1],
        city_bound_upgraded=False,union_admitted=False,
        partition_check=dict(known_physical_school_cohort=school_n,digital_cohort=digital['numInCohort'],
                             district_cohort=district['numInCohort'],school_sum_minus_district=school_n+digital['numInCohort']-district['numInCohort'],
                             necessary_condition_passed=compatible,refresh_all_rows_unchanged=True),
        administrative_last_school_rule_assumed=True,complete_city_coverage_assumed=False,
        additional_exclusion_budget_assumed=False,all_city_quality_comparability_established=False,
        scenarios=summaries)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
