"""Conservative Phoenix outcome bounds under an explicit excess-record budget.
Administrative single-school graduation guidance motivates D=0 as a scenario,
not as proof that observed school records are already deduplicated.
"""
import json,itertools
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_v7_model import baseline,apply_bounds,collect


def unique_lower(counts,duplicate_budget):
    a=np.asarray(counts)
    if a.ndim!=1 or not len(a) or not np.all(np.isfinite(a)) or np.any(a<0) or np.any(a!=np.floor(a)):
        raise ValueError('Nonnegative integer school lower counts required')
    if not np.isfinite(duplicate_budget) or duplicate_budget<0 or duplicate_budget!=int(duplicate_budget):
        raise ValueError('Nonnegative integer excess-record budget required')
    return max(int(a.max()),int(a.sum())-int(duplicate_budget))


def selfcheck():
    checks=0
    for memberships in itertools.product(range(8),repeat=4):
        counts=[sum(bool(m&(1<<j)) for m in memberships) for j in range(3)]
        union=sum(m!=0 for m in memberships);excess=sum(counts)-union
        for lower in [counts,[max(0,x-1) for x in counts]]:
            assert unique_lower(lower,excess)<=union;checks+=1
    return checks


def main():
    checks=selfcheck();p=ROOT/'data/task4_v9_phoenix'
    schools=pd.read_csv(p/'expanded_known_cohort_bounds.csv')
    state=[r for r in json.loads((p/'state_graduation_2025.json').read_text()) if r['studentGroupDescription']=='All'][0]
    gs=state['numGraduated'];fs=state['numInCohort']-gs
    counts=schools.graduates_lower.to_numpy();fmin=int((schools.cohort-schools.graduates_upper).max())
    dmax=int(counts.sum()-counts.max());qhi=gs/(gs+fmin)
    l,h,_=apply_bounds(*baseline(),collect());i=CITIES.index('Phoenix');w=np.r_[.9*weights(),.1]
    low=np.column_stack([l,np.zeros(len(l))]);high=np.column_stack([h,np.ones(len(h))])
    before,_=summarize(low,high,w)
    def state_at(d):
        gl=unique_lower(counts,d);ql=gl/(gl+fs)
        ll=low.copy();hh=high.copy();ll[i,-1]=ql;hh[i,-1]=qhi
        frame,_=summarize(ll,hh,w)
        return frame,ql
    start,_=state_at(0);end,_=state_at(dmax);transitions=[]
    # All upper endpoints stay fixed, so each rival regret is constant.
    for k,c in enumerate(CITIES):
        if k==i:continue
        target=float(start.iloc[k].max_regret)
        if float(start.iloc[i].max_regret)<=target+1e-12 and float(end.iloc[i].max_regret)>target+1e-12:
            a,b=0,dmax
            while a<b:
                mid=(a+b)//2;f,_=state_at(mid)
                if float(f.iloc[i].max_regret)>target+1e-12:b=mid
                else:a=mid+1
            transitions.append(dict(first_strictly_worse_budget=a,rival=c))
    transitions.sort(key=lambda x:x['first_strictly_worse_budget'])
    budgets=sorted(set([0,dmax]+[r['first_strictly_worse_budget'] for r in transitions]+[max(0,r['first_strictly_worse_budget']-1) for r in transitions]))
    rows=[];frames=[]
    for d in budgets:
        f,ql=state_at(d);mask=np.arange(len(CITIES))!=i
        assert np.allclose(f.loc[mask,'max_regret'],start.loc[mask,'max_regret'],rtol=0,atol=1e-12)
        f['duplicate_budget']=d;frames.append(f)
        rows.append(dict(duplicate_budget=d,unique_graduates_lower=unique_lower(counts,d),quality_lower=ql,quality_upper=qhi,phoenix_decision_rank=int(f.iloc[i].decision_rank),possible_champions=int(f.possible_champion.sum()),phoenix_score_width=float(f.iloc[i].score_upper-f.iloc[i].score_lower)))
    legacy=json.loads((ROOT/'results/task4_v9_overlap/summary.json').read_text())['scenarios'][-1]
    assert abs(rows[-1]['quality_lower']-legacy['quality_lower'])<1e-12
    assert abs(rows[-1]['quality_upper']-legacy['quality_upper'])<1e-12
    assert rows[-1]['phoenix_decision_rank']==legacy['phoenix_rank']
    out=ROOT/'results/task4_v14_duplicate_budget';out.mkdir(parents=True,exist_ok=True)
    before.to_csv(out/'unknown_quality_baseline.csv',index=False);pd.concat(frames).to_csv(out/'ranks.csv',index=False)
    result=dict(main_admitted=False,duplicate_budget_observed=False,outcome_weight=.1,graduates_lower_sum=int(counts.sum()),largest_school_lower=int(counts.max()),unrestricted_equivalent_budget=dmax,synthetic_checks=checks,transitions=transitions,scenarios=rows)
    (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
