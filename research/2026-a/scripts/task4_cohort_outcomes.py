"""Conditional four-year administrative diploma outcomes on the V16 matrix.
Separate criterion-design effects from real-data effects; preserve unknown outcomes.
No international equivalence or resident-wide coverage is asserted.
"""
import hashlib,json
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_combined_evidence import combined_bounds
from task4_continuous_preferences import terms,feasible_polynomials


def outcome_terms(u,beta):
    if not 0<=beta<1:raise ValueError('Outcome weight must be in [0,1)')
    u=np.asarray(u,float)
    if u.shape!=(11,) or not np.isfinite(u).all() or np.any((u<0)|(u>1)):raise ValueError('11 utilities in [0,1] required')
    a,b=terms(u[:10]);a=(1-beta)*a;b=(1-beta)*b
    a[0]+=beta*(1-u[-1])**2;b[0]+=beta*u[-1]**2
    return a,b


def outcome_feasible(candidate,rivals,beta,alpha_min=.05,alpha_max=.2):
    a,b=outcome_terms(candidate,beta);polys=[]
    for row in rivals:
        c,d=outcome_terms(row,beta)
        polys.append(np.polynomial.polynomial.polysub(np.polynomial.polynomial.polymul(b,c),np.polynomial.polynomial.polymul(d,a)))
    return feasible_polynomials(polys,alpha_min,alpha_max)


def scenario_bounds():
    lo,hi=combined_bounds();lo=np.column_stack([lo,np.zeros(len(lo))]);hi=np.column_stack([hi,np.ones(len(hi))])
    cases={'unknown_outcome':(lo,hi)}
    phoenix=json.loads((ROOT/'results/task4_v14_duplicate_budget/summary.json').read_text())['scenarios'][-1]
    nyc=json.loads((ROOT/'data/task4_v18_nyc_quality/graduation_summary.json').read_text())['scopes']
    for label,include_phoenix,year in [('phoenix_unrestricted',True,None),('nyc2024_only',False,'2024'),('phoenix_nyc2024',True,'2024'),('phoenix_nyc2025',True,'2025')]:
        l,h=lo.copy(),hi.copy()
        if include_phoenix:
            i=CITIES.index('Phoenix');l[i,-1]=phoenix['quality_lower'];h[i,-1]=phoenix['quality_upper']
        if year:
            i=CITIES.index('New York');l[i,-1]=nyc[year]['lower'];h[i,-1]=nyc[year]['upper']
        assert np.all(l<=h);cases[label]=(l,h)
    return cases


def main():
    cases=scenario_bounds();out=ROOT/'results/task4_v18_cohort_outcomes';out.mkdir(parents=True,exist_ok=True)
    base_lo,base_hi=cases['unknown_outcome'];archived=pd.read_csv(ROOT/'results/task4_v16_combined/utility_bounds.csv')
    archived=archived[archived.scenario=='combined_municipal'].set_index(['city','indicator'])
    for i,c in enumerate(CITIES):
        for j,n in enumerate(NAMES):
            assert abs(base_lo[i,j]-archived.loc[(c,n),'lower'])<1e-14
            assert abs(base_hi[i,j]-archived.loc[(c,n),'upper'])<1e-14
    matrix_hash=hashlib.sha256(np.stack([base_lo[:,:10],base_hi[:,:10]]).astype('<f8').tobytes()).hexdigest()
    frames=[];summary=[];bounds=[]
    for label,(l,h) in cases.items():
        bounds.extend(dict(scenario=label,city=c,lower=float(l[i,-1]),upper=float(h[i,-1])) for i,c in enumerate(CITIES))
        for beta in [0,.05,.1,.2]:
            w=np.r_[(1-beta)*weights(),beta];frame,decision=summarize(l,h,w)
            possible=[c for i,c in enumerate(CITIES) if outcome_feasible(h[i],l[np.arange(len(l))!=i],beta)['possible']]
            frame['scenario']=label;frame['outcome_weight']=beta;frames.append(frame)
            ny=frame.iloc[CITIES.index('New York')]
            summary.append(dict(scenario=label,outcome_weight=beta,nyc_decision_rank=int(ny.decision_rank),phoenix_decision_rank=int(frame.iloc[CITIES.index('Phoenix')].decision_rank),nyc_score_width=float(ny.score_upper-ny.score_lower),mean_score_width=float((frame.score_upper-frame.score_lower).mean()),fixed_possible_champions=int(frame.possible_champion.sum()),continuous_possible_champions=len(possible),minimax_regret=decision['minimax_regret'],minimax_choices=[CITIES[i] for i in decision['minimax_choices']]))
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'outcome_bounds.csv',index=False)
    sources=[]
    for name in ['data/task4_v18_nyc_quality/graduation_summary.json','results/task4_v14_duplicate_budget/summary.json','results/task4_v16_combined/utility_bounds.csv']:
        sources.append(dict(path=name,sha256=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()))
    (out/'summary.json').write_text(json.dumps(dict(main_admitted=False,baseline_matrix_sha256=matrix_hash,outcome_weight_grid=[0,.05,.1,.2],continuous_auxiliary_weight_range=[.05,.2],source_inputs=sources,scenarios=summary),indent=2)+'\n')
    print(pd.DataFrame(summary).to_string(index=False))
if __name__=='__main__':main()
