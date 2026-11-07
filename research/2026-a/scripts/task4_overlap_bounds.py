"""Graduation bounds allowing cross-school overlap; assumptions remain explicit."""
import math,json,itertools
import numpy as np
import pandas as pd
from task4_v5_model import ROOT,CITIES,weights,summarize
from task4_v7_model import baseline,apply_bounds,collect


def lower_union(counts,max_multiplicity=None):
    counts=np.asarray(counts,int)
    if len(counts)==0 or np.any(counts<0):raise ValueError('Nonnegative nonempty counts required')
    if max_multiplicity is None:return int(counts.max())
    if max_multiplicity<1 or int(max_multiplicity)!=max_multiplicity:raise ValueError('Positive integer multiplicity required')
    return max(int(counts.max()),math.ceil(int(counts.sum())/max_multiplicity))


def selfcheck():
    # Exhaust all three-school memberships of four synthetic people, allowing overlap.
    for memberships in itertools.product(range(8),repeat=4):
        counts=[sum(bool(m&(1<<j)) for m in memberships) for j in range(3)]
        union=sum(m!=0 for m in memberships)
        mult=max([bin(m).count('1') for m in memberships]+[1])
        assert lower_union(counts)<=union
        assert lower_union(counts,mult)<=union
    assert lower_union([10,10])==10 and lower_union([10,10],1)==20


def main():
    selfcheck();p=ROOT/'data/task4_v9_phoenix'
    schools=pd.read_csv(p/'expanded_known_cohort_bounds.csv')
    state=[r for r in json.loads((p/'state_graduation_2025.json').read_text()) if r['studentGroupDescription']=='All'][0]
    gs=state['numGraduated'];fs=state['numInCohort']-gs
    l,h,_=apply_bounds(*baseline(),collect());i=CITIES.index('Phoenix');beta=.1;w=np.r_[.9*weights(),beta]
    lo=np.column_stack([l,np.zeros(len(l))]);hi=np.column_stack([h,np.ones(len(l))]);before,_=summarize(lo,hi,w)
    rows=[];frames=[]
    for m in [1,2,3,None]:
        gl=lower_union(schools.graduates_lower,m);fl=lower_union(schools.cohort-schools.graduates_upper,m)
        ql=gl/(gl+fs);qh=gs/(gs+fl)
        assert gl<=gs and fl<=fs
        ll=lo.copy();hh=hi.copy();ll[i,-1]=ql;hh[i,-1]=qh
        f,_=summarize(ll,hh,w);f['multiplicity']='unrestricted' if m is None else str(m);frames.append(f)
        rows.append(dict(max_multiplicity=m,unique_graduates_lower=gl,unique_nongraduates_lower=fl,quality_lower=ql,quality_upper=qh,
                         phoenix_rank=int(f.iloc[i].decision_rank),possible_champions=int(f.possible_champion.sum()),phoenix_width=float(f.iloc[i].score_upper-f.iloc[i].score_lower)))
    assert all(rows[j]['quality_lower']>=rows[j+1]['quality_lower'] and rows[j]['quality_upper']<=rows[j+1]['quality_upper'] for j in range(3))
    out=ROOT/'results/task4_v9_overlap';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames).to_csv(out/'ranks.csv',index=False);before.to_csv(out/'unknown_outcome_baseline.csv',index=False)
    result=dict(main_admission=False,outcome_weight=beta,assumptions=['Within-school counts are unique and graduate/non-graduate status agrees with the same statewide cohort','School membership and target geography are compatible; unresolved current-vs-historical locations'],validation='4096 synthetic overlapping membership assignments; nested bounds as multiplicity increases',scenarios=rows)
    (out/'summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
