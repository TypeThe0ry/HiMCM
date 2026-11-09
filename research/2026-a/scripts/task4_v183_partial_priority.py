"""Screen remaining partial intervals alongside all completely missing cells.

Conditional exact-utility information limits; not source availability or forecasts.
"""
import hashlib,json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from task4_interval_decision import interval_decision,voi_1d
from task4_user_v181_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v124_priority import independent_scores
from task4_v5_model import ROOT,NAMES,weights,score
O=ROOT/'results/task4_v183_priority'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def regret(l,u):return np.array([max(0.,max(np.delete(u,i))-l[i]) for i in range(len(l))])
def main():
    f,lo,hi=revised_bounds();initial=np.stack([lo,hi]).copy();cities=f.city.tolist()
    partial=(lo<hi)&~((lo==0)&(hi==1));assert partial.sum()==35
    rows=[];endpoints=[];checks=0
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        L,U=score(lo,w),score(hi,w);risk=float(regret(L,U).min())
        for i,j in zip(*np.where(partial)):
            lower,upper=float(lo[i,j]),float(hi[i,j])
            def callback(x):
                a,b=lo.copy(),hi.copy();a[i,j]=b[i,j]=x
                mask=np.ones((16,10),bool);mask[i,j]=False
                np.testing.assert_array_equal(np.stack([a,b])[:,mask],initial[:,mask])
                l,u=score(a,w),score(b,w)
                np.testing.assert_allclose(l,independent_scores(a,w),atol=1e-12,rtol=0)
                np.testing.assert_allclose(u,independent_scores(b,w),atol=1e-12,rtol=0)
                return l,u
            information=voi_1d(callback,i,lower,upper,baseline=(L,U))
            def branch(x):
                l,u=callback(x);r=regret(l,u);return float(r[i]),float(np.delete(r,i).min())
            def gap(x):a,b=branch(x);return a-b
            candidates=[lower,upper]
            if gap(lower)>=0>=gap(upper):candidates.append(brentq(gap,lower,upper,xtol=1e-14))
            worst=max(min(branch(x)) for x in candidates);best=min(min(branch(lower)),min(branch(upper)))
            np.testing.assert_allclose([information['guaranteed_gain'],information['best_possible_gain']],[risk-worst,risk-best],atol=1e-10,rtol=0)
            possibilities=[]
            for label,x in [('lower',lower),('upper',upper)]:
                l,u=callback(x);d=interval_decision(l,u);possibilities.append(int(d['possible_champion'].sum()))
                endpoints.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],endpoint=label,resolved_utility=x,possible_count=int(d['possible_champion'].sum()),minimax_regret=float(d['minimax_regret']),conservative_recommendation=';'.join(cities[k] for k in d['minimax_choices']),excluded_cities=';'.join(cities[k] for k in range(16) if not d['possible_champion'][k])))
            ceiling=16-min(possibilities)
            for x in np.linspace(lower,upper,21):
                l,u=callback(float(x));d=interval_decision(l,u)
                assert best-1e-10<=d['minimax_regret']<=worst+1e-10
                assert 16-int(d['possible_champion'].sum())<=ceiling
                checks+=1
            rows.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],current_lower=lower,current_upper=upper,current_information='partial_interval',guaranteed_exact_resolution_regret_reduction=information['guaranteed_gain'],best_possible_exact_resolution_regret_reduction=information['best_possible_gain'],optimistic_champion_exclusions=ceiling,worst_post_regret=worst,best_post_regret=best))
    partial_table=pd.DataFrame(rows);partial_table.to_csv(O/'partial_priority.csv',index=False)
    pd.DataFrame(endpoints).to_csv(O/'partial_endpoints.csv',index=False)
    unknown=pd.read_csv(O/'priority.csv',float_precision='round_trip').assign(current_lower=0.,current_upper=1.,current_information='fully_missing')
    columns=list(partial_table.columns);combined=pd.concat([unknown[columns],partial_table],ignore_index=True).sort_values(['weight_reference','guaranteed_exact_resolution_regret_reduction','best_possible_exact_resolution_regret_reduction','city','indicator'],ascending=[True,False,False,True,True])
    assert len(combined)==96 and combined[['weight_reference','city','indicator']].duplicated().sum()==0
    combined.to_csv(O/'all_uncertain_priority.csv',index=False)
    _,a,b=revised_bounds();np.testing.assert_array_equal(initial,np.stack([a,b]))
    report=dict(version='V183 partial-interval information limits',primary='V181 unchanged',paper='V182 unchanged',partial_cells=35,fully_missing_cells=13,uncertain_cells=48,combined_city_indicator_weight_rows=96,partial_exact_resolution_cases=70,independent_two_branch_optimizations=70,interior_probes=checks,all160_bounds_unchanged=True,primary_admissions=0,scope='Exact utility identification inside each retained interval, conditional on the model rectangle; not a source availability probability, attainable raw observation or guarantee for a partial count/mean.', acquisition_alignment='Partial-source refinement must match the retained measurement, population and vintage; an unrelated school-trip distribution cannot simply narrow an existing general-commute mean proxy or replace a supplied value.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'scripts/task4_v183_priority.py',ROOT/'design/task4_user_v181_snapshot.json',O/'priority.csv']})
    (O/'partial_summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'},indent=2))
if __name__=='__main__':main()
