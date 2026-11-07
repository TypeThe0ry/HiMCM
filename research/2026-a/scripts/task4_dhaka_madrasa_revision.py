"""Expand HSC coverage to Alim using subset count caps, without imputation."""
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_dhaka_stage_bounds import dhaka_stage_bounds,evidence
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def madrasa_evidence():
    evidence()  # Verify shared original PDF hash and general HSC counts.
    r=json.loads((ROOT/'data/task4_v60_dhaka_madrasa/audit.json').read_text())
    assert sum(x['alim_upper'] for x in r['rows'])==42393
    assert sum(x['city_teachers'] for x in r['rows'])==1944
    for x in r['rows']:
        upper=min(x['city_girls'],x['national_alim_girls'])+min(x['city_students']-x['city_girls'],x['national_alim']-x['national_alim_girls'])
        assert upper==x['alim_upper']
    return r


def dhaka_madrasa_bounds(student_cap=42393):
    madrasa_evidence();r=evidence();lo,hi=dhaka_stage_bounds()
    i,j=CITIES.index('Dhaka'),NAMES.index('upper_secondary_ptr')
    lo[i,j]=15*r['teachers_lower']/(r['students_upper']+student_cap+15*r['teachers_lower'])
    hi[i,j]=15*(r['teachers_upper']+1944)/(r['students_lower']+15*(r['teachers_upper']+1944))
    return lo,hi


def main():
    r=madrasa_evidence();lo,hi=dhaka_stage_bounds();i,j=CITIES.index('Dhaka'),NAMES.index('upper_secondary_ptr')
    mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
    broadlo,broadh=lo.copy(),hi.copy();broadlo[i,j],broadh[i,j]=0,1
    cases=[('v59_general_hsc',(lo,hi)),('expanded_scope_unknown',(broadlo,broadh)),
           ('expanded_no_stage_caps',dhaka_madrasa_bounds(50440)),
           ('expanded_without_gender_cap',dhaka_madrasa_bounds(42550)),
           ('v60_general_hsc_and_alim',dhaka_madrasa_bounds())]
    base,_=summarize(lo,hi,weights());frames=[];reports=[];bounds=[]
    for label,(l,h) in cases:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        assert np.all((0<=l)&(l<=h)&(h<=1))
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        reports.append(dict(scenario=label,dhaka_education_utility=[float(l[i,j]),float(h[i,j])],
            dhaka=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v59=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            possible_champions=int(f.possible_champion.sum()),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(l[k,m]),upper=float(h[k,m])) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    # Conservative monotone corners contain all count allocations in the box.
    a,b=dhaka_madrasa_bounds()
    for n in [140342,426900,469293]:
        for t in [965,12016,13960]:
            assert a[i,j]<=15*t/(n+15*t)<=b[i,j]
    cert=certify(a,b)
    for leaf in cert:leaf['city']=None if leaf['winner'] is None else CITIES[leaf['winner']]
    out=ROOT/'results/task4_v60_dhaka_madrasa';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(cert).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(current_scenario=cases[-1][0],baseline='V59',main_admitted=False,other_unchanged_cells=int(mask.sum()),
        students_interval=[140342,469293],teachers_interval=[965,13960],national_share_imputation=False,
        target='Source-defined general HSC plus Alim; technical/vocational coverage unresolved',
        date_caveat=r['date_caveat'],geography=r['geography'],scenarios=reports,
        continuous_recommendation=dict(alpha_range=[.05,.2],unresolved_leaves=sum(not c['certified'] for c in cert),
            certified_winners=sorted({c['city'] for c in cert if c['certified']}),numerical_certificate_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k!='continuous_possible_champions'} for x in reports],indent=2))

if __name__=='__main__':main()
