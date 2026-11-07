"""Withdraw an unsupported instructional-headcount floor; retain evidence upper bound."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_dhaka_madrasa_revision import dhaka_madrasa_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def dhaka_role_bounds():
    audit=json.loads((ROOT/'data/task4_v61_dhaka_definition/audit.json').read_text())
    raw=ROOT/'data/task4_v59_secondary_sources/bangladesh_education2025.pdf'
    assert hashlib.sha256(raw.read_bytes()).hexdigest()==audit['source_sha256']
    assert audit['conditional_role_lower']==230
    assert not audit['person_deduplication_verified']
    lo,hi=dhaka_madrasa_bounds()
    lo[CITIES.index('Dhaka'),NAMES.index('upper_secondary_ptr')]=0
    return lo,hi


def main():
    lo,hi=dhaka_madrasa_bounds();i,j=CITIES.index('Dhaka'),NAMES.index('upper_secondary_ptr')
    base,_=summarize(lo,hi,weights());new=dhaka_role_bounds()
    mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
    # Sex-consistent designation allocation refutes the old 965 role floor.
    # This is a feasible hypothetical allocation, never a city observation.
    male=[1060,59,149,0,0,0]
    female=[135,19,416,165,5,230]
    assert sum(male)==2238-970 and sum(female)==970
    assert all(a<=b for a,b in zip(male,[1060,59,1262,275,29,12585]))
    assert all(a<=b for a,b in zip(female,[135,19,416,165,5,5345]))
    assert male[-1]+female[-1]==230<965
    # The zero endpoint is a conservative outer bound; not a sharp identified
    # zero-teacher realization. Teaching roles and distinct people differ.
    assert 13960==12016+1944
    frames=[];reports=[];bounds=[]
    unknownlo,unknownhi=lo.copy(),hi.copy();unknownlo[i,j],unknownhi[i,j]=0,1
    cases=[('v60_role_floor',(lo,hi)),('v61_instructional_headcount_floor_unknown',new),
           ('source_scope_withdrawn',(unknownlo,unknownhi))]
    for label,(l,h) in cases:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        assert np.all((0<=l)&(l<=h)&(h<=1))
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        reports.append(dict(scenario=label,dhaka_education_utility=[float(l[i,j]),float(h[i,j])],
            dhaka=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v60=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            possible_champions=int(f.possible_champion.sum()),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(l[k,m]),upper=float(h[k,m])) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    cert=certify(*new)
    for leaf in cert:leaf['city']=None if leaf['winner'] is None else CITIES[leaf['winner']]
    out=ROOT/'results/task4_v61_dhaka_roles';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(cert).to_csv(out/'recommendation_certificate.csv',index=False)
    r=dict(current_scenario=cases[1][0],baseline='V60',main_admitted=False,other_unchanged_cells=int(mask.sum()),
        students_interval=[140342,469293],teachers_interval=[0,13960],sharp_headcount_bounds=False,
        reason='Unidentified teaching duties and cross-institution uniqueness; 965 non-head roles are not a guaranteed count of distinct instructional teachers.',
        target='Source-defined general HSC plus Alim; technical/vocational coverage unresolved',
        scenarios=reports,continuous_recommendation=dict(alpha_range=[.05,.2],unresolved_leaves=sum(not c['certified'] for c in cert),
            certified_winners=sorted({c['city'] for c in cert if c['certified']}),numerical_certificate_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k!='continuous_possible_champions'} for x in reports],indent=2))

if __name__=='__main__':main()
