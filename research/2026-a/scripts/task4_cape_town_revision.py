"""Add actual Cape Town Grade10--12 school travel to the V29 conditional model."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_education_year_update import updated_bounds
from task4_continuous_preferences import feasible_preferences

SOURCE=ROOT/'data/task4_v30_cape_town'


def cape_bounds(scope='age14_18',sampling=True):
    if scope not in ('age14_18','all_age'):raise ValueError('Unknown student scope')
    for item in json.loads((SOURCE/'manifest.json').read_text()):
        assert hashlib.sha256((SOURCE/item['file']).read_bytes()).hexdigest()==item['sha256']
    extraction=json.loads((SOURCE/'summary.json').read_text())
    raw=extraction['ages14_18' if scope=='age14_18' else 'all_ages']
    inference=json.loads((SOURCE/'inference_summary.json').read_text())[scope]
    assert raw['optional']['n']==0,'New unresolved eligibility requires inference review'
    assert raw['definite']['n']==inference['n']
    np.testing.assert_allclose(inference['point_bounds'],[raw['utility_lower'],raw['utility_upper']],rtol=0,atol=1e-12)
    a,b=inference['joint_95_percent_approximate_envelope'] if sampling else inference['point_bounds']
    assert 0<=a<=b<=1
    assert a<=raw['utility_lower']+1e-12 and raw['utility_upper']<=b+1e-12
    lo,hi=updated_bounds();i=CITIES.index('Cape Town');j=NAMES.index('travel')
    assert lo[i,j]==0 and hi[i,j]==1
    lo[i,j],hi[i,j]=a,b
    return lo,hi


def main():
    lo,hi=updated_bounds();base,_=summarize(lo,hi,weights());frames=[];bounds=[];summaries=[]
    scenarios=[('v29_before',(lo,hi)),('age14_18_point',cape_bounds(sampling=False)),('age14_18_sampling',cape_bounds()),('all_age_sampling',cape_bounds('all_age'))]
    for name,(l,h) in scenarios:
        keep=np.ones(l.shape,dtype=bool);keep[CITIES.index('Cape Town'),NAMES.index('travel')]=False
        np.testing.assert_array_equal(l[keep],lo[keep]);np.testing.assert_array_equal(h[keep],hi[keep])
        assert np.all(l>=lo-1e-12) and np.all(h<=hi+1e-12) and np.all(l<=h)
        f,d=summarize(l,h,weights());f['scenario']=name;frames.append(f)
        possible=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        summaries.append(dict(scenario=name,minimax_choice=[CITIES[k] for k in d['minimax_choices']],minimax_regret=d['minimax_regret'],
            possible_champions=int(f.possible_champion.sum()),continuous_alpha_possible_champions=possible,
            changed_ranks=int((f.decision_rank!=base.decision_rank).sum()),kendall_tau=float(kendalltau(f.decision_rank,base.decision_rank).statistic),
            mean_score_width=float((f.score_upper-f.score_lower).mean()),
            cape_town={k:float(f.loc[f.city=='Cape Town',k].iloc[0]) for k in ['score_lower','score_upper','max_regret','decision_rank']},
            phoenix_rank=int(f.loc[f.city=='Phoenix','decision_rank'].iloc[0])))
        bounds.extend(dict(scenario=name,city=c,indicator=n,lower=float(l[i,j]),upper=float(h[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    out=ROOT/'results/task4_v30_cape_town';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    files=['manifest.json','summary.json','inference_summary.json','extract.py','inference.py']
    result=dict(main_admitted=False,new_city_indicator_cells=1,primary_scenario='age14_18_sampling',alpha_fixed=.1,alpha_range=[.05,.2],
        scope='Cape Town household-resident formal Grade10-12 students age14-18, in-person; GHS2023. Excludes student hostels and other collective quarters. Approximate released-design inference, not a simultaneous confidence region across cities.',
        sources=[dict(path=str((SOURCE/p).relative_to(ROOT)),sha256=hashlib.sha256((SOURCE/p).read_bytes()).hexdigest()) for p in files],scenarios=summaries)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k!='continuous_alpha_possible_champions'} for r in summaries],indent=2))

if __name__=='__main__':main()
