"""V23: restore roster/attendance uncertainty; preserve V21 historical scenarios."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_combined_evidence import combined_bounds
from task4_cohort_outcomes import scenario_bounds,outcome_feasible
from task4_continuous_preferences import feasible_preferences



def current_bounds(nyc_scope='under19', include_outcome=False, sampling=True):
    """V23 conditional analysis entry point; historical builders remain frozen.

    Melbourne remains Greater Melbourne Secondary age 15--19, not exact upper
    secondary. Mexico remains conditional completed-grade progression. Sampling
    envelopes across cities are not a joint confidence region.
    """
    if nyc_scope not in ('all_age','under19'):
        raise ValueError('Unknown NYC age scope')
    l,h = (scenario_bounds()['phoenix_nyc2024'] if include_outcome else combined_bounds())
    l,h=l.copy(),h.copy();j=NAMES.index('travel')
    nyc=json.loads((ROOT/'data/task4_v21_nyc_chains/summary.json').read_text())['scopes'][nyc_scope]
    mexico=json.loads((ROOT/'data/task4_v23_mexico_membership/summary.json').read_text())['scopes']['age3_17']
    melbourne=json.loads((ROOT/'data/task4_v23_melbourne_roster/summary.json').read_text())['scopes']['secondary_15_19']
    for city,row,prefix in [('New York',nyc,'sampling'),('Mexico City',mexico,'utility'),
                           ('Melbourne',melbourne,'sampling' if sampling else 'utility')]:
        i=CITIES.index(city);l[i,j]=row[prefix+'_lower'];h[i,j]=row[prefix+'_upper']
    return l,h


def main():
    paths={
        'nyc':'data/task4_v21_nyc_chains/summary.json',
        'mexico':'data/task4_v23_mexico_membership/summary.json',
        'melbourne':'data/task4_v23_melbourne_roster/summary.json',
    }
    data={k:json.loads((ROOT/p).read_text()) for k,p in paths.items()}
    mexico=data['mexico']['scopes']['age3_17']
    melbourne=data['melbourne']['scopes']['secondary_15_19']
    previous=pd.read_csv(ROOT/'results/task4_v22_optimism/ranks.csv')
    frames=[];summaries=[];bounds=[]
    j=NAMES.index('travel');mi=CITIES.index('Mexico City');vi=CITIES.index('Melbourne')
    for model,base_l,base_h,beta in [('v16_ten_criteria',*combined_bounds(),0),
            ('v18_cohort_beta10',*scenario_bounds()['phoenix_nyc2024'],.1)]:
        w=weights() if not beta else np.r_[(1-beta)*weights(),beta]
        for scope in ['all_age','under19']:
            lo,hi=base_l.copy(),base_h.copy();ny=CITIES.index('New York')
            lo[ny,j]=data['nyc']['scopes'][scope]['sampling_lower']
            hi[ny,j]=data['nyc']['scopes'][scope]['sampling_upper']
            np.testing.assert_allclose([lo[mi,j],hi[mi,j]],[mexico['before_lower'],mexico['before_upper']],atol=1e-14,rtol=0)
            baseline=None
            for name,mex,melb in [('v21_reference',False,None),('mexico_membership_only',True,None),
                    ('melbourne_roster_identification_only',False,'utility'),
                    ('both_identification',True,'utility'),('both_sampling_envelope',True,'sampling')]:
                l,h=lo.copy(),hi.copy();expected=set()
                if mex:
                    l[mi,j]=mexico['utility_lower'];h[mi,j]=mexico['utility_upper'];expected.add((mi,j))
                if melb:
                    l[vi,j]=melbourne[melb+'_lower'];h[vi,j]=melbourne[melb+'_upper'];expected.add((vi,j))
                assert set(zip(*np.where((l!=lo)|(h!=hi))))==expected
                assert np.all((0<=l)&(l<=h)&(h<=1))
                if name in ('both_identification','both_sampling_envelope'):
                    active=current_bounds(scope,bool(beta),name=='both_sampling_envelope')
                    np.testing.assert_array_equal(l,active[0]);np.testing.assert_array_equal(h,active[1])
                f,d=summarize(l,h,w);f['model']=model;f['nyc_age_scope']=scope;f['scenario']=name
                frames.append(f)
                if baseline is None:
                    baseline=f.copy()
                    ref=previous[(previous.model==model)&(previous.age_scope==scope)]
                    assert ref.city.tolist()==CITIES
                    np.testing.assert_allclose(f[['score_lower','score_upper','decision_rank']],ref[['score_lower','score_upper','decision_rank']],atol=1e-11,rtol=0)
                possible=[]
                for k,c in enumerate(CITIES):
                    rivals=l[np.arange(len(l))!=k]
                    yes=(outcome_feasible(h[k],rivals,beta) if beta else feasible_preferences(h[k],rivals))['possible']
                    if yes:possible.append(c)
                selected={c:dict(rank=int(f.iloc[CITIES.index(c)].decision_rank),
                    score_width=float(f.iloc[CITIES.index(c)].score_upper-f.iloc[CITIES.index(c)].score_lower))
                    for c in ['Phoenix','Mexico City','Melbourne','New York','Singapore']}
                summaries.append(dict(model=model,nyc_age_scope=scope,scenario=name,selected=selected,
                    fixed_possible_champions=f.loc[f.possible_champion,'city'].tolist(),
                    continuous_possible_champions=possible,
                    mean_score_width=float((f.score_upper-f.score_lower).mean()),
                    changed_ranks=int((f.decision_rank!=baseline.decision_rank).sum()),
                    kendall_tau=float(kendalltau(f.decision_rank,baseline.decision_rank).statistic),
                    minimax_regret=d['minimax_regret'],minimax_choices=[CITIES[k] for k in d['minimax_choices']],
                    matrix_sha256=hashlib.sha256(np.stack([l,h]).astype('<f8').tobytes()).hexdigest()))
                names=NAMES+(['graduation_outcome'] if beta else [])
                bounds.extend(dict(model=model,nyc_age_scope=scope,scenario=name,city=c,indicator=n,
                    lower=float(l[k,t]),upper=float(h[k,t])) for k,c in enumerate(CITIES) for t,n in enumerate(names))
    out=ROOT/'results/task4_v23_roster_coverage';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False)
    sources=[dict(path=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in paths.values()]
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,source_inputs=sources,
        alpha_range=[.05,.2],outcome_weights=[0,.1],new_phoenix_observations=0,
        scenarios=summaries),indent=2)+'\n')
    for s in summaries:
        if s['nyc_age_scope']=='under19':
            print(s['model'],s['scenario'],'ranks', {c:r['rank'] for c,r in s['selected'].items()},
                  'possible',len(s['continuous_possible_champions']),'meanwidth',s['mean_score_width'])

if __name__=='__main__':main()
