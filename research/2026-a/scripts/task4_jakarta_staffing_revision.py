"""Broaden Jakarta's formal-school staffing evidence, retaining role uncertainty.

Induk means home-school assignment, not FTE. The target excludes noninduk
attachments by definition; it is not a census of everybody teaching in Jakarta.
"""
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_istanbul_coverage_revision import istanbul_coverage_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def observations():
    data=json.loads((ROOT/'data/task4_v58_jakarta_education/observation.json').read_text())
    rows={r['program']:r for r in data['observations']}
    assert set(rows)=={'SMA','SMK'}
    assert all(r['academic_year']=='2025/2026' and r['snapshot']=='2025-11-30' for r in rows.values())
    assert [(rows[k]['students'],rows[k]['induk_teachers'],rows[k]['headmasters']) for k in ['SMA','SMK']]==[(186461,11530,453),(194178,10994,525)]
    ma=pd.read_csv(ROOT/'data/task4_v58_jakarta_ma/ma_municipal_transcription.csv')
    total=ma[ma.area=='DKI Jakarta'].iloc[0];parts=ma[ma.area!='DKI Jakarta']
    assert len(parts)==6
    for key in ['schools','staff','students']:
        assert (ma[key+'_public']+ma[key+'_private']==ma[key+'_total']).all()
        assert parts[key+'_total'].sum()==total[key+'_total']
    assert (total.students_total,total.staff_total)==(24672,2008)
    return rows,total


def staffing_utility(students,teachers):
    assert students>0 and teachers>=0
    return 15*teachers/(students+15*teachers)


def jakarta_coverage_bounds(strict_ma_source=False):
    rows,ma=observations()
    students=sum(r['students'] for r in rows.values())+int(ma.students_total)
    teachers=sum(r['induk_teachers'] for r in rows.values())
    pool=sum(r['headmasters'] for r in rows.values())+int(ma.staff_total)
    lo,hi=istanbul_coverage_bounds();i=CITIES.index('Jakarta');j=NAMES.index('upper_secondary_ptr')
    lo[i,j],hi[i,j]=(0.,1.) if strict_ma_source else (staffing_utility(students,teachers),staffing_utility(students,teachers+pool))
    return lo,hi


def checks():
    # Endpoint bounds cover every staff allocation in the actual two pools.
    n=405311;t=22524
    low=staffing_utility(n,t);high=staffing_utility(n,t+978+2008)
    for h in [0,1,489,977,978]:
        for m in [0,1,1004,2007,2008]:
            assert low<=staffing_utility(n,t+h+m)<=high
    # Same student population and staff pool: reallocating staff cannot change
    # the full-staff upper bound or alter the source's enrollment denominator.
    assert staffing_utility(186461,11530)<staffing_utility(186461,11983)
    assert staffing_utility(380639,22524)<staffing_utility(380639,23502)


def main():
    checks();rows,ma=observations()
    lo,hi=istanbul_coverage_bounds();i=CITIES.index('Jakarta');j=NAMES.index('upper_secondary_ptr')
    old=staffing_utility(186461,11983)
    np.testing.assert_allclose([lo[i,j],hi[i,j]],[old,old],atol=1e-12,rtol=0)
    def cell(a,b=None):
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=a,a if b is None else b
        return l,h
    cases=[('v53_sma_headmaster_and_teacher',(lo,hi)),
           ('sma_teacher_role_only',cell(staffing_utility(186461,11530))),
           ('sma_smk_headmaster_and_teacher',cell(staffing_utility(380639,23502))),
           ('sma_smk_teacher_role_only',cell(staffing_utility(380639,22524))),
           ('sma_smk_headmaster_allocation',cell(staffing_utility(380639,22524),staffing_utility(380639,23502))),
           ('v58_three_stream_home_assignment',jakarta_coverage_bounds()),
           ('ma_indexed_source_withdrawn',jakarta_coverage_bounds(True))]
    frames=[];bounds=[];reports=[];base,_=summarize(lo,hi,weights())
    mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
    for label,(l,h) in cases:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        assert np.all((0<=l)&(l<=h)&(h<=1))
        frame,decision=summarize(l,h,weights());frame['scenario']=label;frames.append(frame)
        champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        reports.append(dict(scenario=label,jakarta_education_utility=[float(l[i,j]),float(h[i,j])],
            jakarta=frame.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in decision['minimax_choices']],
            changed_ranks_vs_v53=int((frame.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v53=float(kendalltau(frame.decision_rank,base.decision_rank).statistic),
            possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=champions))
        bounds.extend(dict(scenario=label,city=c,indicator=name,lower=float(l[k,m]),upper=float(h[k,m])) for k,c in enumerate(CITIES) for m,name in enumerate(NAMES))
    out=ROOT/'results/task4_v58_jakarta_staffing';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    certificate=certify(*jakarta_coverage_bounds())
    for leaf in certificate:leaf['city']=None if leaf['winner'] is None else CITIES[leaf['winner']]
    pd.DataFrame(certificate).to_csv(out/'recommendation_certificate.csv',index=False)
    report=dict(current_scenario='v58_three_stream_home_assignment',changed_input_cells=1,
        unchanged_other_cells=int(mask.sum()),main_admitted=False,
        student_count=405311,identified_home_assigned_teachers=22524,
        headmaster_pool=978,unallocated_ma_staff_pool=2008,teacher_bounds=[22524,25510],
        scope='Published SMA, SMK and MA home-assigned instructional resource counts, public+private; not all teaching providers or FTE',
        ma_original_source_archived=False,same_day_census=False,academic_year='2025/2026',
        remaining_coverage='Special education and nonformal/equivalency programs not established; MA/MAK labels alone do not prove MAK coverage',
        phoenix_bounds_changed=False,travel_bounds_changed=False,scenarios=reports)
    report['continuous_recommendation']=dict(alpha_range=[.05,.2],
        certified_winners=sorted({r['city'] for r in certificate if r['certified']}),
        unresolved_leaves=sum(not r['certified'] for r in certificate),
        numerical_certificate_not_formal_interval_arithmetic=True)
    (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='continuous_possible_champions'} for r in reports],indent=2))


if __name__=='__main__':main()
