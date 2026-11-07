"""Cumulative real-data comparisons with source conditions kept explicit.
This composes year-specific alternatives; it never intersects historical years.
"""
import json,hashlib
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v7_model import baseline,apply_bounds,collect
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_champion_acquisition import certificates
from task4_robust_acquisition import bundles


def combined_bounds(mexico_scope='age3_17',use_saopaulo=True):
    l,h,_=apply_bounds(*baseline(),collect())
    mexico=json.loads((ROOT/'data/task4_v15_mexico2020/commute_summary.json').read_text())['scopes'][mexico_scope]
    i=CITIES.index('Mexico City');j=NAMES.index('travel')
    l[i,j]=mexico['membership_utility_lower'];h[i,j]=mexico['membership_utility_upper']
    if use_saopaulo:
        sao=json.loads((ROOT/'data/task4_v10_saopaulo/sampling_sensitivity.json').read_text())['scopes']['municipality_sao_paulo']
        i=CITIES.index('Sao Paulo');l[i,j]=sao['utility_lower'];h[i,j]=sao['utility_upper']
    assert np.all(l<=h)
    return l,h


def main():
    out=ROOT/'results/task4_v16_combined';out.mkdir(parents=True,exist_ok=True)
    l0,h0,_=apply_bounds(*baseline(),collect());base,d0=summarize(l0,h0,weights());frames=[];summary=[];all_bounds=[]
    scenarios=[('baseline_v7',l0,h0),('mexico2020_only',*combined_bounds(use_saopaulo=False)),('combined_municipal',*combined_bounds()),('combined_mexico_all_age',*combined_bounds('all_age3plus'))]
    for name,l,h in scenarios:
        frame,d=summarize(l,h,weights());frame['scenario']=name;frames.append(frame)
        possible=[CITIES[k] for k in range(len(CITIES)) if feasible_preferences(h[k],l[np.arange(len(l))!=k])['possible']]
        summary.append(dict(scenario=name,possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=len(possible),changed_decision_ranks=int((frame.decision_rank!=base.decision_rank).sum()),mean_score_width=float((frame.score_upper-frame.score_lower).mean()),minimax_regret=d['minimax_regret'],minimax_choices=[CITIES[k] for k in d['minimax_choices']],selected_ranks={c:int(frame.iloc[CITIES.index(c)].decision_rank) for c in ['Phoenix','Mexico City','Sao Paulo','Singapore']}))
        summary[-1]['kendall_tau_vs_baseline']=float(kendalltau(base.decision_rank,frame.decision_rank).statistic)
        all_bounds.extend(dict(scenario=name,city=c,indicator=n,lower=float(l[i,j]),upper=float(h[i,j])) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES))
    l,h=combined_bounds();changed=(l!=l0)|(h!=h0)
    assert set(zip(*np.where(changed)))=={(CITIES.index('Mexico City'),NAMES.index('travel')),(CITIES.index('Sao Paulo'),NAMES.index('travel'))}
    old,_=certificates(l0,h0,weights(),NAMES,CITIES);new,_=certificates(l,h,weights(),NAMES,CITIES)
    robust,details=bundles(l,h)
    old_robust=pd.read_csv(ROOT/'results/task4_v8_robust_acquisition/minimum_measurements.csv').set_index('city')
    acquisition=[]
    for before,after,r in zip(old,new,robust):
        assert before['city']==after['city']==r['city']
        assert r['minimum_measurements'] is None or (after['minimum_city_local_exact_measurements'] is not None and r['minimum_measurements']>=after['minimum_city_local_exact_measurements'])
        prior=old_robust.loc[r['city'],'minimum_measurements'];prior=None if pd.isna(prior) else int(prior)
        acquisition.append(dict(city=r['city'],fixed_minimum_before=before['minimum_city_local_exact_measurements'],fixed_minimum_after=after['minimum_city_local_exact_measurements'],continuous_minimum_before=prior,continuous_minimum_after=r['minimum_measurements'],new_minimal_bundle_count=r['minimal_bundle_count']))
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(all_bounds).to_csv(out/'utility_bounds.csv',index=False)
    pd.DataFrame(acquisition).to_csv(out/'acquisition_comparison.csv',index=False);pd.DataFrame(details).to_csv(out/'minimal_bundles.csv',index=False)
    sources=[]
    for path in ['data/task4_v15_mexico2020/commute_summary.json','data/task4_v10_saopaulo/sampling_sensitivity.json']:
        sources.append(dict(path=path,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()))
    (out/'source_inputs.json').write_text(json.dumps(dict(sources=sources,global_main_admission_changed=False,joint_confidence_interval=False,conditions=['Mexico2020 school-stage progression reconstruction; uncertain stage retained; unknown attendance not included','SaoPaulo2023 direct current-high-school variable; public mirror official identity unverified; exploratory household resampling','Separate city years, population scopes and age limits remain explicit; no implicit trend inference'],alpha_range=[.05,.2]),indent=2)+'\n')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
