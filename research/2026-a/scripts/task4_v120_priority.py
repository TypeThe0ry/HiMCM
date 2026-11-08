"""Evidence-acquisition priorities from one-cell perfect-resolution limits."""
import hashlib
import json
import numpy as np
import pandas as pd
from task4_user_v118_revision import revised_bounds, MANIFEST
from task4_user_city_indicators import SOURCE
from task4_v5_model import ROOT,NAMES,SPEC,weights,score
from task4_interval_decision import interval_decision

OUT=ROOT/'results/task4_v120_priority'

def main():
    protected={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE,MANIFEST]}
    frame,lo,hi=revised_bounds();cities=frame.city.tolist();n=len(cities)
    endpoints=[];priorities=[];thresholds=[];summaries=[]
    for ref,w in [('fixed',weights(.1)),('equal',np.ones(10)/10)]:
        L,U=score(lo,w),score(hi,w);base=interval_decision(L,U)
        assert np.all(base['possible_champion'])
        for i,j in zip(*np.where(hi>lo)):
            def evaluate(x):
                a,b=lo.copy(),hi.copy();a[i,j]=b[i,j]=x
                l,u=score(a,w),score(b,w)
                others=np.arange(n)!=i
                np.testing.assert_array_equal(l[others],L[others]);np.testing.assert_array_equal(u[others],U[others])
                d=interval_decision(l,u)
                return l,u,d
            candidates=[]
            for label,x in [('lower',lo[i,j]),('upper',hi[i,j])]:
                l,u,d=evaluate(x);remaining=[cities[k] for k in np.flatnonzero(d['possible_champion'])]
                row=dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],endpoint=label,resolved_utility=x,
                    original_lower=lo[i,j],original_upper=hi[i,j],possible_count=len(remaining),
                    excluded_count=n-len(remaining),excluded_cities=';'.join(c for c in cities if c not in remaining),
                    score_lower_before=L[i],score_upper_before=U[i],score_lower_after=l[i],score_upper_after=u[i],
                    lower_score_gain=l[i]-L[i],upper_score_reduction=U[i]-u[i],
                    strongest_lower_after=float(l.max()),minimum_other_upper=float(np.min(U[np.arange(n)!=i])),
                    minimax_choices=';'.join(cities[k] for k in d['minimax_choices']))
                endpoints.append(row);candidates.append(row)
            # With all cities initially possible, focal exclusion cannot coexist
            # with exclusion of another city: U_i(x)<max_other L<=every other U.
            # Other-city exclusions increase with x; own exclusion decreases.
            # Thus the best possible count over all resolutions is at an endpoint.
            best=min(q['possible_count'] for q in candidates)
            for x in np.linspace(lo[i,j],hi[i,j],21):
                assert int(evaluate(x)[2]['possible_champion'].sum())>=best
            low,high=candidates
            priorities.append(dict(weight_reference=ref,city=cities[i],indicator=NAMES[j],
                uncertainty='full_missing' if lo[i,j]==0 and hi[i,j]==1 else 'partial_interval',
                original_lower=lo[i,j],original_upper=hi[i,j],
                optimistic_exclusions=n-best,
                high_endpoint_exclusions=high['excluded_count'],low_endpoint_exclusions=low['excluded_count'],
                high_endpoint_strongest_lower=high['strongest_lower_after'],
                high_endpoint_city_lower=high['score_lower_after'],
                low_endpoint_city_upper=low['score_upper_after'],
                baseline_city_upper=U[i],upper_score_reduction=low['upper_score_reduction'],
                lower_score_gain=high['lower_score_gain']))
            if low['excluded_count']:
                target=float(np.max(L[np.arange(n)!=i]))
                left,right=float(lo[i,j]),float(hi[i,j])
                for _ in range(50):
                    mid=(left+right)/2
                    if evaluate(mid)[1][i]<target:left=mid
                    else:right=mid
                x=(left+right)/2
                record=dict(weight_reference=ref,source_city=cities[i],indicator=NAMES[j],excluded_city=cities[i],
                    utility_threshold=x,strict_requirement='observed upper utility must fall below threshold; equality retains possible tie',
                    source_upper_at_threshold=float(evaluate(x)[1][i]),strongest_other_lower=target)
                if NAMES[j]!='travel':
                    anchor=SPEC[j][2];benefit=SPEC[j][1]
                    record['raw_density_or_ptr_threshold']=anchor*x/(1-x) if benefit else anchor*(1-x)/x
                    record['raw_requirement']='below threshold' if benefit else 'above threshold'
                else:
                    record['mean_interpretation']='A mean alone provides no such upper utility bound; a suitable travel distribution or certified duration bounds are required.'
                thresholds.append(record)
            # Other-city exclusion requires only an improved lower bound, not
            # exact cell identification; these thresholds support data triage.
            for k in range(n):
                if k==i or high['score_lower_after']<=U[k]+1e-12:continue
                left,right=float(lo[i,j]),float(hi[i,j])
                for _ in range(50):
                    mid=(left+right)/2
                    if evaluate(mid)[0][i]>U[k]:right=mid
                    else:left=mid
                x=(left+right)/2
                record=dict(weight_reference=ref,source_city=cities[i],indicator=NAMES[j],excluded_city=cities[k],
                    utility_threshold=x,strict_requirement='observed lower utility must exceed threshold; equality retains possible tie',
                    source_lower_at_threshold=float(evaluate(x)[0][i]),excluded_city_upper=U[k])
                if NAMES[j]=='travel':
                    record['sufficient_mean_minutes_below']=-30*np.log(x)
                    record['mean_interpretation']='Sufficient via Jensen only if new mean belongs to the required student travel population; not an exact utility inversion.'
                thresholds.append(record)
        summaries.append(dict(weight_reference=ref,baseline_possible_count=n,
            baseline_minimax_choices=[cities[k] for k in base['minimax_choices']],
            best_single_cell_possible_count=min(r['possible_count'] for r in endpoints if r['weight_reference']==ref)))
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(endpoints).to_csv(OUT/'endpoint_limits.csv',index=False)
    pr=pd.DataFrame(priorities).sort_values(['weight_reference','optimistic_exclusions','high_endpoint_strongest_lower','baseline_city_upper'],ascending=[True,False,False,False])
    pr.to_csv(OUT/'priority.csv',index=False)
    pd.DataFrame(thresholds).to_csv(OUT/'exclusion_thresholds.csv',index=False)
    summary=dict(base='V118 user16',purpose='Optimistic acquisition limits, not newly observed evidence or probabilities',
        uncertain_cells=int(np.sum(hi>lo)),weight_references=summaries,
        single_cell_endpoint_sufficiency='All 16 currently possible. A focal city cannot be excluded while its lower endpoint excludes any other initially possible city; other-city exclusions are monotone in resolved utility. Minimum remaining count therefore occurs at an endpoint.',
        threshold_interpretation='Closed interval ties remain possible. Strictly exceeding stated lower-utility thresholds is necessary for these particular exclusions.',
        input_sha256={str(p.relative_to(ROOT)):h for p,h in protected.items()})
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    for p,h in protected.items():assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    print(json.dumps(summary,indent=2));print(pd.DataFrame(thresholds).to_string(index=False))

if __name__=='__main__':main()
