"""Update actual high-school travel to GHS2025, keeping survey uncertainty."""
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_dhaka_role_revision import dhaka_role_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def travel_evidence():
    p=ROOT/'data/task4_v63_cape_travel'
    for item in json.loads((p/'manifest.json').read_text()):
        b=(p/item['file']).read_bytes()
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
    r=json.loads((p/'inference_summary.json').read_text())
    assert r['age14_18']['n']==182 and r['age14_18']['psus_all_relevant_strata']==216
    return r


def cape_2025_bounds():
    r=travel_evidence();lo,hi=dhaka_role_bounds()
    i,j=CITIES.index('Cape Town'),NAMES.index('travel')
    lo[i,j],hi[i,j]=r['age14_18']['joint_95_percent_approximate_envelope']
    return lo,hi


def main():
    r=travel_evidence();lo,hi=dhaka_role_bounds();i,j=CITIES.index('Cape Town'),NAMES.index('travel')
    mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False;base,_=summarize(lo,hi,weights())
    def cell(v):
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=v;return l,h
    cases=[('v61_ghs2023',(lo,hi)),('ghs2025_sample_only',cell(r['age14_18']['point_bounds'])),
           ('v63_ghs2025_age14_18',cape_2025_bounds()),
           ('ghs2025_all_age_sensitivity',cell(r['all_age']['joint_95_percent_approximate_envelope'])),
           ('travel_source_withdrawn',cell([0,1]))]
    frames=[];reports=[];bounds=[]
    for label,(l,h) in cases:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        assert np.all((0<=l)&(l<=h)&(h<=1))
        f,d=summarize(l,h,weights());f['scenario']=label;frames.append(f)
        reports.append(dict(scenario=label,cape_travel_utility=[float(l[i,j]),float(h[i,j])],
            cape=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),
            kendall_tau_vs_v61=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            possible_champions=int(f.possible_champion.sum()),
            continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=float(l[k,m]),upper=float(h[k,m])) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    certificate=certify(*cape_2025_bounds())
    for leaf in certificate:leaf['city']=None if leaf['winner'] is None else CITIES[leaf['winner']]
    out=ROOT/'results/task4_v63_cape_2025';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(certificate).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(current_scenario='v63_ghs2025_age14_18',baseline='V61 used in V62',main_admitted=False,
        updated_cells=1,other_unchanged_cells=int(mask.sum()),source_year=2025,scenarios=reports,
        inferential_scope='Approximate endpoint sampling envelope, not an exact joint confidence set for 250 cells; no causal or panel comparison across years.',
        continuous_recommendation=dict(alpha_range=[.05,.2],unresolved_leaves=sum(not c['certified'] for c in certificate),
            certified_winners=sorted({c['city'] for c in certificate if c['certified']}),numerical_certificate_not_formal_interval_arithmetic=True))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k!='continuous_possible_champions'} for x in reports],indent=2))

if __name__=='__main__':main()
