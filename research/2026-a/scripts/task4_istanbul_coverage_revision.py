"""Extend Istanbul upper-secondary coverage with unidentified teacher allocation."""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_saopaulo_age_revision import saopaulo_age_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify

SOURCE=ROOT/'data/task4_v53_istanbul_coverage'


def education_bounds(students,general,vocational,imam,vocational_all_upper=False):
    if not all(np.isfinite(x) and x>=0 for x in [students,general,vocational,imam]) or students==0:
        raise ValueError('Positive students and finite nonnegative teacher pools required')
    low=general+(vocational if vocational_all_upper else 0)
    high=general+vocational+imam
    return np.array([15*low/(students+15*low),15*high/(students+15*high)])


def observation():
    for item in json.loads((SOURCE/'manifest.json').read_text()):
        raw=(SOURCE/item['file']).read_bytes()
        assert len(raw)==item['bytes'] and hashlib.sha256(raw).hexdigest()==item['sha256']
    row=json.loads((SOURCE/'observation.json').read_text())
    assert sum(r['non_open_students'] for r in row['programs'].values())==row['students_upper_nonopen']
    for r in row['programs'].values():
        assert r['total_including_open']-r['open_students']==r['non_open_students']==r['public_students']+r['private_students']
        assert r['reported_teacher_pool']==r['public_teachers']+r['private_teachers']
    for key,value in [('students_upper_nonopen',751598),('general_teachers',28436),
                      ('vocational_teacher_pool',20156),('imam_teacher_pool',9871)]:
        assert row[key]==value
    return row


def istanbul_coverage_bounds(vocational_all_upper=False,withdraw=False):
    row=observation();lo,hi=saopaulo_age_bounds();i=CITIES.index('Istanbul');j=NAMES.index('upper_secondary_ptr')
    assert abs(lo[i,j]-15*28436/(408480+15*28436))<1e-12 and lo[i,j]==hi[i,j]
    lo[i,j],hi[i,j]=[0,1] if withdraw else education_bounds(row['students_upper_nonopen'],row['general_teachers'],
        row['vocational_teacher_pool'],row['imam_teacher_pool'],vocational_all_upper)
    return lo,hi


def main():
    before=saopaulo_age_bounds();baseline,_=summarize(*before,weights())
    i,j=CITIES.index('Istanbul'),NAMES.index('upper_secondary_ptr')
    keep=np.ones(before[0].shape,bool);keep[i,j]=False
    frames=[];stats=[]
    unknown,_=summarize(*istanbul_coverage_bounds(withdraw=True),weights())
    cases=[('v48_general_only_reference',before),('broader_target_unknown',istanbul_coverage_bounds(withdraw=True)),
           ('v53_broader_teacher_allocation',istanbul_coverage_bounds()),
           ('vocational_teachers_all_upper_assumed',istanbul_coverage_bounds(vocational_all_upper=True))]
    for label,(lo,hi) in cases:
        for actual,expected in zip((lo,hi),before):np.testing.assert_array_equal(actual[keep],expected[keep])
        assert np.all((0<=lo)&(lo<=hi)&(hi<=1))
        f,d=summarize(lo,hi,weights());f['scenario']=label;frames.append(f)
        stats.append(dict(scenario=label,education_bounds=[float(lo[i,j]),float(hi[i,j])],
            istanbul=f.iloc[i][['score_lower','score_upper','max_regret','decision_rank']].to_dict(),
            changed_ranks_vs_general_only=int((f.decision_rank!=baseline.decision_rank).sum()),
            changed_ranks_vs_broader_unknown=int((f.decision_rank!=unknown.decision_rank).sum()),
            possible_champions=int(f.possible_champion.sum()),
            continuous_possible=sum(feasible_preferences(hi[k],lo[np.arange(len(lo))!=k])['possible'] for k in range(len(lo))),
            choice=[CITIES[k] for k in d['minimax_choices']]))
    certified=certify(*istanbul_coverage_bounds())
    assert all(r['certified'] and CITIES[r['winner']]=='Singapore' for r in certified)
    out=ROOT/'results/task4_v53_istanbul_coverage';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_admitted=False,primary_scenario='v53_broader_teacher_allocation',
                changed_city_indicator_cells=1,other_cells_unchanged=249,
                coverage_revision_not_same_population_precision_gain=True,
                continuous_recommendation_certificate=certified,scenarios=stats)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(stats,indent=2))


if __name__=='__main__':main()
