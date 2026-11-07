"""Minimum common interval interpolation needed for a possible champion.

Diagnostic scenario only: opponents at lower bounds, candidate at l+t(h-l).
No probabilistic interpretation or narrowing of observed intervals.
"""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT, CITIES, NAMES, weights, score, summarize
from task4_combined_evidence import combined_bounds
from task4_cohort_outcomes import scenario_bounds, outcome_terms
from task4_continuous_preferences import terms, feasible_polynomials


def threshold(lower, upper, rivals, beta=0, iterations=45):
    lower, upper, rivals = map(lambda x: np.asarray(x, float), (lower, upper, rivals))
    if np.any(lower > upper):
        raise ValueError('Reversed bounds')
    def feasible(t):
        row = lower + t * (upper-lower)
        term = (lambda x: outcome_terms(x, beta)) if len(row)==11 else terms
        a,b = term(row)
        polys=[]
        for rival in rivals:
            c,d = term(rival)
            polys.append(np.polynomial.polynomial.polysub(
                np.polynomial.polynomial.polymul(b,c),
                np.polynomial.polynomial.polymul(d,a)))
        # A fixed polynomial slack biases thresholds near ideal endpoints.
        return feasible_polynomials(polys, tol=0.)
    if feasible(0)['possible']:
        return dict(possible=True, threshold_lower=0., threshold_upper=0., **{'witness_alpha': feasible(0)['witness_alpha']})
    if not feasible(1)['possible']:
        return dict(possible=False, threshold_lower=None, threshold_upper=None, witness_alpha=None)
    low, high = 0., 1.
    for _ in range(iterations):
        middle = (low+high)/2
        if feasible(middle)['possible']: high = middle
        else: low = middle
    assert not feasible(low)['possible'] and feasible(high)['possible']
    return dict(possible=True, threshold_lower=low, threshold_upper=high,
                witness_alpha=feasible(high)['witness_alpha'])


def main():
    source = ROOT/'data/task4_v21_nyc_chains/summary.json'
    data = json.loads(source.read_text())
    archived = pd.read_csv(ROOT/'results/task4_v21_nyc_chains/ranks.csv')
    records, ranks, matrices = [], [], []
    for model, base_l, base_h, beta in [('v16_ten_criteria', *combined_bounds(), 0),
            ('v18_cohort_beta10', *scenario_bounds()['phoenix_nyc2024'], .1)]:
        for age in ['all_age', 'under19']:
            l,h=base_l.copy(),base_h.copy();i=CITIES.index('New York');j=NAMES.index('travel')
            l[i,j]=data['scopes'][age]['sampling_lower'];h[i,j]=data['scopes'][age]['sampling_upper']
            matrices.append(dict(model=model,age_scope=age,sha256=hashlib.sha256(np.stack([l,h]).astype('<f8').tobytes()).hexdigest()))
            w=weights() if beta==0 else np.r_[.9*weights(),.1]
            frame,_=summarize(l,h,w)
            previous=archived[(archived.model==model)&(archived.age_scope==age)&(archived.version=='v21_transport_chain_recovery')]
            assert previous.city.tolist()==CITIES
            np.testing.assert_allclose(frame[['score_lower','score_upper','decision_rank']],previous[['score_lower','score_upper','decision_rank']],rtol=0,atol=1e-11)
            frame['model']=model;frame['age_scope']=age;ranks.append(frame)
            for k,city in enumerate(CITIES):
                rivals=l[np.arange(len(l))!=k]
                r=threshold(l[k],h[k],rivals,beta)
                if r['possible']:
                    a=r['witness_alpha'];ww=weights(a) if beta==0 else np.r_[(1-beta)*weights(a),beta]
                    witness=l[k]+r['threshold_upper']*(h[k]-l[k])
                    margin=float(score(witness[None,:],ww)[0]-max(score(rivals,ww)))
                    assert margin>=-1e-7
                else:margin=None
                records.append(dict(model=model,age_scope=age,city=city,**r,witness_score_margin=margin))
    out=ROOT/'results/task4_v22_optimism';out.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(records).to_csv(out/'thresholds.csv',index=False)
    pd.concat(ranks).to_csv(out/'ranks.csv',index=False)
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,new_phoenix_observations=0,
        ranking_changes=0,alpha_range=[.05,.2],polynomial_tolerance=0.,bisection_iterations=45,
        interpretation='Common interpolation of candidate uncertainty only; rivals at lower bounds. Not probability or prediction.',
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),matrices=matrices,
        possible_counts=pd.DataFrame(records).groupby(['model','age_scope'],as_index=False).possible.sum().to_dict('records')),indent=2)+'\n')
    print(pd.DataFrame(records).groupby(['model','age_scope']).threshold_upper.agg(['min','max']).to_string())
    print(pd.DataFrame(records).query("city == 'Phoenix'").to_string(index=False))

if __name__=='__main__':main()
