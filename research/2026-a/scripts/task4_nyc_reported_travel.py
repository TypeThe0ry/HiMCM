"""Historical actual school-trip alternatives to historical modeled NYC routes.
Only NYC travel changes; years and measurement concepts are never intersected.
"""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_combined_evidence import combined_bounds
from task4_cohort_outcomes import scenario_bounds,outcome_feasible
from task4_continuous_preferences import feasible_preferences


def main():
    source=ROOT/'data/task4_v20_nyc_travel/commute_summary.json';data=json.loads(source.read_text());i=CITIES.index('New York');j=NAMES.index('travel')
    cases=[('previous_modeled_routes',None),('reported_known_stage',(data['known_stage_utility_lower'],data['known_stage_utility_upper'])),('reported_optional_membership',(data['membership_utility_lower'],data['membership_utility_upper'])),('reported_sampling_envelope',(data['sampling_envelope_lower'],data['sampling_envelope_upper'])),('under19_sampling_envelope',(data['under19_alternative']['sampling_envelope_lower'],data['under19_alternative']['sampling_envelope_upper']))]
    frames=[];summary=[];matrices=[]
    baselines=[('v16_ten_criteria',*combined_bounds(),weights(),0),('v18_cohort_beta10',*scenario_bounds()['phoenix_nyc2024'],np.r_[.9*weights(),.1],.1)]
    for model,lo,hi,w,beta in baselines:
        before,_=summarize(lo,hi,w);matrices.append(dict(model=model,sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest()))
        for name,endpoints in cases:
            l,h=lo.copy(),hi.copy()
            if endpoints is not None:
                l[i,j],h[i,j]=endpoints
                assert set(zip(*np.where((l!=lo)|(h!=hi))))=={(i,j)}
            frame,d=summarize(l,h,w);frame['model']=model;frame['scenario']=name;frames.append(frame)
            possible=[]
            for k,c in enumerate(CITIES):
                rivals=l[np.arange(len(l))!=k]
                yes=outcome_feasible(h[k],rivals,beta)['possible'] if beta else feasible_preferences(h[k],rivals)['possible']
                if yes:possible.append(c)
            row=frame.iloc[i]
            summary.append(dict(model=model,scenario=name,travel_lower=float(l[i,j]),travel_upper=float(h[i,j]),nyc_decision_rank=int(row.decision_rank),phoenix_decision_rank=int(frame.iloc[CITIES.index('Phoenix')].decision_rank),nyc_score_lower=float(row.score_lower),nyc_score_upper=float(row.score_upper),nyc_score_width=float(row.score_upper-row.score_lower),mean_score_width=float((frame.score_upper-frame.score_lower).mean()),changed_decision_ranks=int((frame.decision_rank!=before.decision_rank).sum()),kendall_tau=float(kendalltau(frame.decision_rank,before.decision_rank).statistic),fixed_possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=len(possible),minimax_regret=d['minimax_regret'],minimax_choices=[CITIES[k] for k in d['minimax_choices']]))
    out=ROOT/'results/task4_v20_nyc_reported_travel';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,source=str(source.relative_to(ROOT)),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),baseline_matrices=matrices,alpha_range=[.05,.2],sampling_interval_is_official_confidence=False,scenarios=summary),indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False))
if __name__=='__main__':main()
