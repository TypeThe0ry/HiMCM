"""2030 conditional stress scenarios, not forecasts or a historical panel."""
import hashlib
import json
import numpy as np
import pandas as pd
from scipy.stats import kendalltau
from task4_user_v118_revision import revised_bounds, MANIFEST
from task4_user_city_indicators import SOURCE, evaluate
from task4_v5_model import ROOT, NAMES, SPEC, weights

OUT=ROOT/'results/task4_v119_future'
SCENARIOS={
 'baseline':{},
 'resource_expansion':dict(research_he_density=1.1,public_transport_density=1.1,public_pool_density=1.1),
 'living_pressure':dict(cost_living_index=1.1,price_income_ratio=1.1,travel=1.1),
 'balanced_improvement':dict(upper_secondary_ptr=.9,pm25=.9,travel=.9)}
IMPROVE=['upper_secondary_ptr','pm25','travel']
TOL=1e-10

def transform(lo,hi,factors,rows=None):
    a,b=lo.copy(),hi.copy()
    rows=np.arange(len(a)) if rows is None else np.asarray(rows)
    for name,r in factors.items():
        assert r>0
        j=NAMES.index(name)
        if name=='travel':
            # Requires submitted mean-only Jensen bounds or complete missingness.
            assert np.all(hi[:,j]==1)
            a[rows,j]=lo[rows,j]**r
            b[rows,j]=1
        else:
            benefit=SPEC[j][1]
            def f(u):return r*u/(1-u+r*u) if benefit else u/(u+r*(1-u))
            a[rows,j]=f(lo[rows,j]);b[rows,j]=f(hi[rows,j])
    assert np.all((0<=a)&(a<=b)&(b<=1))
    changed_cols=[NAMES.index(n) for n in factors]
    unchanged=np.ones(a.shape,dtype=bool)
    unchanged[np.ix_(rows,changed_cols)]=False
    np.testing.assert_array_equal(a[unchanged],lo[unchanged])
    np.testing.assert_array_equal(b[unchanged],hi[unchanged])
    return a,b

def threshold(cities,lo,hi,w,city):
    k=cities.index(city);oslo=cities.index('Oslo');other=np.arange(len(cities))!=k
    def calc(r):
        a,b=transform(lo,hi,dict.fromkeys(IMPROVE,r),[k])
        f=evaluate(cities,a,b,w);rr=f.max_regret.to_numpy()
        return rr[k]-rr[other].min(),rr[k]-rr[oslo],f
    grid=np.linspace(1,.5,501)
    values=[calc(float(r))[0] for r in grid]
    # As raw costs fall, the candidate's regret cannot rise; others cannot fall.
    assert np.all(np.diff(values)<=1e-9)
    result=dict(city=city,raw_multiplier_range=[.5,1],baseline_gap_to_best_other=values[0],
        gap_at_50pct_cost_reduction=values[-1],status='not_reached',
        threshold_raw_multiplier=None,required_cost_reduction_fraction=None)
    hits=np.flatnonzero(np.asarray(values)<-TOL)
    if len(hits):
        h=int(hits[0])
        if h==0:
            result.update(status='already_strict_minimax',threshold_raw_multiplier=1.,required_cost_reduction_fraction=0.)
        else:
            left,right=float(grid[h]),float(grid[h-1])
            for _ in range(45):
                mid=(left+right)/2
                if calc(mid)[0]<0:left=mid
                else:right=mid
            r=(left+right)/2;gap,oslogap,f=calc(r)
            result.update(status='crossing_found',threshold_raw_multiplier=r,
                required_cost_reduction_fraction=1-r,threshold_bracket=[left,right],
                regret_gap_at_threshold=gap,gap_to_Oslo_at_threshold=oslogap,
                tied_minimax_choices=f.loc[f.max_regret<=f.max_regret.min()+TOL,'city'].tolist(),
                strict_rule='candidate regret < every other city regret - 1e-10; equality is a tied recommendation')
            assert abs(gap)<1e-8
            assert calc(r-1e-6)[0] < -TOL and calc(r+1e-6)[0] > TOL
            result['local_crossing_verified_at_multiplier_offset']=1e-6
    elif abs(values[-1])<=TOL:
        result['status']='tie_only_at_endpoint'
    return result,[dict(city=city,raw_multiplier=float(r),regret_gap_to_best_other=g) for r,g in zip(grid,values)]

def main():
    protected={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE,MANIFEST]}
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();assert len(cities)==16
    # Establish the special travel scope before applying exponent transformation.
    j=NAMES.index('travel')
    expected=np.where(frame.commute_min.notna(),np.exp(-frame.commute_min.fillna(0).to_numpy()/30),0.)
    np.testing.assert_allclose(lo[:,j],expected,atol=1e-14,rtol=0)
    np.testing.assert_array_equal(hi[:,j],np.ones(16))
    # Identity, reversible scaling and endpoint tests cover all transform families.
    one=dict.fromkeys(NAMES,1.)
    a,b=transform(lo,hi,one);np.testing.assert_allclose(a,lo);np.testing.assert_allclose(b,hi)
    for label,factors in SCENARIOS.items():
        a,b=transform(lo,hi,factors)
        c,d=transform(a,b,{n:1/r for n,r in factors.items()})
        np.testing.assert_allclose(c,lo,atol=1e-14);np.testing.assert_allclose(d,hi,atol=1e-14)
    reports=[];tables=[];bounds=[];thresholds=[];scans=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        baseline=evaluate(cities,lo,hi,w)
        for label,factors in SCENARIOS.items():
            a,b=transform(lo,hi,factors);f=evaluate(cities,a,b,w)
            f['baseline_decision_rank']=baseline.decision_rank
            f['rank_change_positive_improves']=baseline.decision_rank-f.decision_rank
            f['score_lower_change']=f.score_lower-baseline.score_lower
            f['score_upper_change']=f.score_upper-baseline.score_upper
            tables.append(f.assign(scenario=label,weight_reference=ref))
            reports.append(dict(scenario=label,weight_reference=ref,
                minimax_choices=f.loc[f.max_regret<=f.max_regret.min()+TOL,'city'].tolist(),
                possible_champions=f.loc[f.possible_champion,'city'].tolist(),
                necessary_champions=f.loc[f.necessary_champion,'city'].tolist(),
                kendall_decision_tau_b=float(kendalltau(baseline.decision_rank,f.decision_rank).statistic),
                mean_score_interval_width=float((f.score_upper-f.score_lower).mean())))
            if ref=='fixed':
                bounds.extend(dict(scenario=label,city=c,indicator=n,lower=a[i,j],upper=b[i,j])
                              for i,c in enumerate(cities) for j,n in enumerate(NAMES))
        for city in ['Singapore','Zurich','Dublin']:
            result,scan=threshold(cities,lo,hi,w,city)
            thresholds.append(dict(weight_reference=ref,**result))
            scans.extend(dict(weight_reference=ref,**row) for row in scan)
    OUT.mkdir(exist_ok=True)
    pd.concat(tables,ignore_index=True).to_csv(OUT/'ranks.csv',index=False)
    pd.DataFrame(bounds).to_csv(OUT/'utility_bounds.csv',index=False)
    pd.DataFrame(scans).to_csv(OUT/'threshold_scan.csv',index=False)
    pd.DataFrame(thresholds).to_csv(OUT/'thresholds.csv',index=False)
    result=dict(version='V119',interpretation='2030 conditional stress scenarios, not forecasts',
        base='16-city V118',stress_parameter=.1,scenario_raw_multipliers=SCENARIOS,
        travel_scope='All 16 cells verified as submitted mean Jensen [exp(-mean/30),1] or complete missing [0,1]',
        interval_interpretation='Partial identification under conditional inputs; not confidence intervals',
        weights={ref:w.tolist() for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]},
        source_sha256={str(p.relative_to(ROOT)):h for p,h in protected.items()},
        scenarios=reports,thresholds=thresholds)
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    for p,h in protected.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    print(json.dumps(dict(scenarios=reports,thresholds=thresholds),indent=2))

if __name__=='__main__':main()
