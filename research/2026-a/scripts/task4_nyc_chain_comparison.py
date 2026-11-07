"""Same-population V20 to V21 actual-journey recovery comparison."""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_combined_evidence import combined_bounds
from task4_cohort_outcomes import scenario_bounds,outcome_feasible
from task4_continuous_preferences import feasible_preferences


def main():
    old_path=ROOT/'data/task4_v20_nyc_travel/commute_summary.json';new_path=ROOT/'data/task4_v21_nyc_chains/summary.json'
    old=json.loads(old_path.read_text());new=json.loads(new_path.read_text());i=CITIES.index('New York');j=NAMES.index('travel')
    frames=[];rows=[]
    archived=pd.read_csv(ROOT/'results/task4_v20_nyc_reported_travel/ranks.csv')
    for model,lo,hi,w,beta in [('v16_ten_criteria',*combined_bounds(),weights(),0),('v18_cohort_beta10',*scenario_bounds()['phoenix_nyc2024'],np.r_[.9*weights(),.1],.1)]:
        for scope in ['all_age','under19']:
            prior=old if scope=='all_age' else old['under19_alternative'];after=new['scopes'][scope]
            baseline_rank=None
            for version,lvalue,hvalue in [('v20_direct_plus_unknown',prior['sampling_envelope_lower'],prior['sampling_envelope_upper']),('v21_transport_chain_recovery',after['sampling_lower'],after['sampling_upper'])]:
                l,h=lo.copy(),hi.copy();l[i,j]=lvalue;h[i,j]=hvalue
                f,d=summarize(l,h,w);f['model']=model;f['age_scope']=scope;f['version']=version;frames.append(f)
                if baseline_rank is None:
                    baseline_rank=f.decision_rank.copy()
                    scenario='reported_sampling_envelope' if scope=='all_age' else 'under19_sampling_envelope'
                    reference=archived[(archived.model==model)&(archived.scenario==scenario)]
                    assert reference.city.tolist()==CITIES
                    np.testing.assert_allclose(f[['score_lower','score_upper']],reference[['score_lower','score_upper']],rtol=0,atol=1e-11)
                possible=[]
                for k,c in enumerate(CITIES):
                    others=l[np.arange(len(l))!=k]
                    yes=outcome_feasible(h[k],others,beta)['possible'] if beta else feasible_preferences(h[k],others)['possible']
                    if yes:possible.append(c)
                r=f.iloc[i];rows.append(dict(model=model,age_scope=scope,version=version,travel_lower=lvalue,travel_upper=hvalue,nyc_decision_rank=int(r.decision_rank),nyc_score_width=float(r.score_upper-r.score_lower),mean_score_width=float((f.score_upper-f.score_lower).mean()),changed_decision_ranks=int((f.decision_rank!=baseline_rank).sum()),possible_champions=int(f.possible_champion.sum()),continuous_possible_champions=len(possible),minimax_regret=d['minimax_regret'],minimax_choices=[CITIES[k] for k in d['minimax_choices']]))
    out=ROOT/'results/task4_v21_nyc_chains';out.mkdir(parents=True,exist_ok=True);pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    sources=[dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in [old_path,new_path]]
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,sources=sources,scenarios=rows),indent=2)+'\n');print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
