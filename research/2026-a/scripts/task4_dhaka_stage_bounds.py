"""Use national contamination caps to bound city HSC counts, not impute means."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_jakarta_staffing_revision import jakarta_coverage_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def evidence():
    p=ROOT/'data/task4_v59_dhaka'
    r=json.loads((p/'observation.json').read_text())
    raw=(p/'../task4_v59_secondary_sources/bangladesh_education2025.pdf').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==r['source_sha256']
    assert (r['students_lower'],r['students_upper'],r['teachers_lower'],r['teachers_upper'])==(140342,426900,965,12016)
    return r


def dhaka_stage_bounds():
    r=evidence();lo,hi=jakarta_coverage_bounds()
    i=CITIES.index('Dhaka');j=NAMES.index('upper_secondary_ptr')
    lo[i,j]=15*r['teachers_lower']/(r['students_upper']+15*r['teachers_lower'])
    hi[i,j]=15*r['teachers_upper']/(r['students_lower']+15*r['teachers_upper'])
    return lo,hi


def checks():
    # Local contamination cannot exceed the whole-country same-category count.
    for local_total in range(8):
        for national_cap in range(8):
            for local_other in range(min(local_total,national_cap)+1):
                assert max(0,local_total-national_cap)<=local_total-local_other
    # Independent allocation of additional stage students and teacher roles.
    for n in [140342,200000,300000,426900]:
        for t in [965,2238,7075,12016]:
            u=15*t/(n+15*t)
            assert 15*965/(426900+15*965)<=u<=15*12016/(140342+15*12016)


def main():
    checks();r=evidence();lo,hi=jakarta_coverage_bounds();i=CITIES.index('Dhaka');j=NAMES.index('upper_secondary_ptr')
    assert lo[i,j]==0 and hi[i,j]==1
    base,_=summarize(lo,hi,weights());mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
    def cell(a,b):
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=a,b;return l,h
    primary=dhaka_stage_bounds()
    cases=[('v58_unknown_dhaka_education',(lo,hi)),
           ('pure_hsc_college_subset_only',cell(15*2238/(37191+15*2238),15*2238/(37191+15*2238))),
           ('reported_roles_no_head_exclusion',cell(r['reported_role_lower'],r['education_upper'])),
           ('v59_role_and_stage_bounds',primary),
           ('date_or_geography_not_accepted',(lo,hi))]
    frames=[];bounds=[];reports=[]
    for label,(l,h) in cases:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        assert np.all((0<=l)&(l<=h)&(h<=1))
        frame,d=summarize(l,h,weights());frame['scenario']=label;frames.append(frame)
        reports.append(dict(scenario=label,dhaka_education_utility=[float(l[i,j]),float(h[i,j])],
            dhaka=frame.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],
            changed_ranks=int((frame.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v58=float(kendalltau(frame.decision_rank,base.decision_rank).statistic),
            possible_champions=int(frame.possible_champion.sum()),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]))
        bounds.extend(dict(scenario=label,city=c,indicator=name,lower=float(l[k,m]),upper=float(h[k,m])) for k,c in enumerate(CITIES) for m,name in enumerate(NAMES))
    certificate=certify(*primary)
    for leaf in certificate:leaf['city']=None if leaf['winner'] is None else CITIES[leaf['winner']]
    out=ROOT/'results/task4_v59_dhaka_stage';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificate).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(current_scenario='v59_role_and_stage_bounds',baseline='V58',main_admitted=False,
        newly_bounded_cells=1,other_unchanged_cells=int(mask.sum()),
        date_caveat=r['date_caveat'],geography=r['geography'],target=r['target'],
        national_values_used_as_city_estimates=False,scenarios=reports,
        continuous_recommendation=dict(alpha_range=[.05,.2],unresolved_leaves=sum(not c['certified'] for c in certificate),
            certified_winners=sorted({c['city'] for c in certificate if c['certified']}),
            numerical_certificate_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in row.items() if k!='continuous_possible_champions'} for row in reports],indent=2))


if __name__=='__main__':main()
