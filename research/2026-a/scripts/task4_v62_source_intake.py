"""Recompute current ranking while keeping unmatched new source counts separate."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_dhaka_role_revision import dhaka_role_bounds
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def main():
    sources=[]
    for package in ['task4_v62_london_colleges','task4_v62_copenhagen_education','task4_v62_cape_school_roster']:
        folder=ROOT/'data'/package
        manifest=json.loads((folder/'manifest.json').read_text())
        if isinstance(manifest,dict):manifest=[dict(manifest,file='western_cape_q3_2025.xlsx')]
        for item in manifest:
            b=(folder/item['file']).read_bytes()
            assert hashlib.sha256(b).hexdigest()==item['sha256']
            assert len(b)==item['bytes']
        sources.append(dict(package=package,verified_raw_files=len(manifest)))
    gap=json.loads((ROOT/'data/task4_v62_pxu_gap/audit.json').read_text())
    assert not gap['gap_resolved'] and gap['new_admitted_observations']==0
    lo,hi=dhaka_role_bounds();frame,decision=summarize(lo,hi,weights())
    prior=pd.read_csv(ROOT/'results/task4_v61_dhaka_roles/ranks.csv')
    prior=prior[prior.scenario=='v61_instructional_headcount_floor_unknown'].reset_index(drop=True)
    assert frame.city.tolist()==prior.city.tolist()
    for k in ['score_lower','score_upper','decision_rank','max_regret','possible_champion']:
        np.testing.assert_allclose(frame[k],prior[k],rtol=0,atol=1e-12)
    old=pd.read_csv(ROOT/'results/task4_v61_dhaka_roles/utility_bounds.csv')
    old=old[old.scenario=='v61_instructional_headcount_floor_unknown']
    assert old.city.tolist()==[c for c in CITIES for _ in NAMES]
    assert old.indicator.tolist()==NAMES*len(CITIES)
    np.testing.assert_allclose(lo.ravel(),old.lower,rtol=0,atol=1e-15)
    np.testing.assert_allclose(hi.ravel(),old.upper,rtol=0,atol=1e-15)
    continuous=[c for i,c in enumerate(CITIES) if feasible_preferences(hi[i],lo[np.arange(len(lo))!=i])['possible']]
    cert=certify(lo,hi)
    for c in cert:c['city']=None if c['winner'] is None else CITIES[c['winner']]
    out=ROOT/'results/task4_v62_source_intake';out.mkdir(parents=True,exist_ok=True)
    frame.to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(cert).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model='V61 dhaka_role_bounds',new_source_packages=sources,changed_cells=0,verified_unchanged_cells=int(lo.size),changed_ranks=0,
                possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=continuous,
                choice=[CITIES[i] for i in decision['minimax_choices']],main_admitted=False,
                continuous_recommendation=dict(unresolved_leaves=sum(not c['certified'] for c in cert),winners=sorted({c['city'] for c in cert if c['certified']}),alpha_range=[.05,.2]))
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='continuous_possible_champions'},indent=2))

if __name__=='__main__':main()
