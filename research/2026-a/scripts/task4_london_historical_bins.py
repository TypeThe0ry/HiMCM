"""Historical Year10 rounded-bin diagnostic, never current-city evidence."""
import hashlib,json
import numpy as np
import pandas as pd
from scipy.optimize import linprog
from task4_current_model import current_bounds
from task4_joint_uncertainty_stress import protect_output
from task4_v5_model import ROOT,CITIES,NAMES,weights,summarize
from task4_continuous_preferences import feasible_preferences
from task4_continuous_recommendation import certify


def rounded_bin_bounds(percent,lower,upper,rounding_points=.5):
    p=np.asarray(percent,float);l=np.asarray(lower,float);h=np.asarray(upper,float)
    if p.ndim!=1 or p.size==0 or p.shape!=l.shape or p.shape!=h.shape or not np.isfinite([p,l,h]).all():raise ValueError('Matching finite one-dimensional bin arrays required')
    if np.any((p<0)|(p>100)|(l<0)|(h>1)|(l>h)) or not np.isfinite(rounding_points) or rounding_points<0:raise ValueError('Invalid bin or rounding bounds')
    bounds=np.column_stack([np.maximum(0,p-rounding_points)/100,np.minimum(100,p+rounding_points)/100])
    results=[]
    for c in [l,-h]:
        r=linprog(c,A_eq=np.ones((1,len(p))),b_eq=[1.],bounds=bounds,method='highs')
        if not r.success:raise ValueError('Rounded bins have no common probability vector; do not renormalize')
        assert abs(r.x.sum()-1)<1e-10 and np.all(r.x>=bounds[:,0]-1e-10) and np.all(r.x<=bounds[:,1]+1e-10)
        results.append(r)
    return dict(utility_lower=float(results[0].fun),utility_upper=float(-results[1].fun),
                lower_probability_witness=results[0].x.tolist(),upper_probability_witness=results[1].x.tolist(),
                percentage_bounds=(bounds*100).tolist(),rounding_points=rounding_points)


def main():
    source=ROOT/'data/task4_v106_london';src=json.loads((source/'historical_year10_aggregates.json').read_text())
    p=[r['London_Year10_published_percent'] for r in src['published_percentages']]
    assert p==[30,36,15,7,3,8] and src['London_Year10_respondents']==22451
    # Conservative contiguous closures, no midpoints, missing values [0,1].
    lower=np.r_[np.exp(-np.array([15,30,45,60,np.inf])/30),0.]
    upper=np.r_[np.exp(-np.array([0,15,30,45,60])/30),1.]
    estimates=[rounded_bin_bounds(p,lower,upper,r) for r in [.5,1.]]
    lo,hi,config=current_bounds();i,j=CITIES.index('London'),NAMES.index('travel');mask=np.ones(lo.shape,bool);mask[i,j]=False
    assert (lo[i,j],hi[i,j])==(0.,1.)
    scenarios=[('current_city',lo.copy(),hi.copy())]
    for e in estimates:
        l,h=lo.copy(),hi.copy();l[i,j],h[i,j]=e['utility_lower'],e['utility_upper'];scenarios.append(('historic_rounding_'+str(e['rounding_points']),l,h))
    reports=[];frames=[];bounds=[];certs=[]
    for label,l,h in scenarios:
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask]);f,d=summarize(l,h,weights(config['fixed_alpha']));frames.append(f.assign(scenario=label))
        cert=certify(l,h,*config['alpha_range']);certs.extend(dict(**r,scenario=label) for r in cert)
        reports.append(dict(scenario=label,london_utility=[l[i,j],h[i,j]],london=f.iloc[i][['decision_rank','score_lower','score_upper','max_regret']].to_dict(),
            choice=[CITIES[k] for k in d['minimax_choices']],possible_champions=int(f.possible_champion.sum()),continuous_possible_champions=[c for k,c in enumerate(CITIES) if feasible_preferences(h[k],l[np.arange(len(CITIES))!=k],*config['alpha_range'])['possible']],continuous_recommendation=dict(unresolved=sum(not r['certified'] for r in cert),winners=sorted({CITIES[r['winner']] for r in cert if r['certified']}))))
        bounds.extend(dict(scenario=label,city=c,indicator=n,lower=l[k,m],upper=h[k,m]) for k,c in enumerate(CITIES) for m,n in enumerate(NAMES))
    out=ROOT/'results/task4_v106_london_historical';protect_output(out,lo,hi,config);out.mkdir(exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'utility_bounds.csv',index=False);pd.DataFrame(certs).to_csv(out/'recommendation_certificate.csv',index=False)
    result=dict(model_version=config['model_version'],main_admitted=False,actual_changed_cells=0,input_bounds_sha256=hashlib.sha256(np.stack([lo,hi]).astype('<f8').tobytes()).hexdigest(),source_summary_sha256=hashlib.sha256((source/'historical_year10_aggregates.json').read_bytes()).hexdigest(),
        fixed_alpha=config['fixed_alpha'],alpha_range=config['alpha_range'],published_percent=p,published_total=sum(p),bin_utility_lower=lower.tolist(),bin_utility_upper=upper.tolist(),estimates=estimates,scenarios=reports,
        scope='2006 London school-location Year10 respondent subgroup, not current resident age14-18 population. Rounding envelopes are conditional; no confidence interval, counts inversion, renormalization or midpoint imputation. Main model unchanged.')
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(estimates=estimates,scenarios=[{k:v for k,v in r.items() if k!='continuous_possible_champions'} for r in reports]),indent=2))

if __name__=='__main__':main()
