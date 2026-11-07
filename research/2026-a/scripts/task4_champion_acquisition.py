"""Exact city-local acquisition certificates; hypothetical outcomes are NOT evidence.

For each city, hold competitors' current lower scores fixed. Enumerate subsets
of this city's uncertain cells and ask if any permissible exact measurements
could eliminate that city. Minima occur at the existing lower utility endpoints.
This is a necessary acquisition-size diagnostic, not a recommendation to set
unknown values to zero and not a guarantee that measurement eliminates anyone.
"""
import itertools
import numpy as np


def topsis_row(u,w):
    a=np.sqrt(np.dot(w,(1-u)**2));b=np.sqrt(np.dot(w,u*u))
    return 100*b/(a+b)


def certificates(lower,upper,weights,names,cities,tol=1e-10):
    lo=np.asarray(lower,float); hi=np.asarray(upper,float);w=np.asarray(weights,float)
    if lo.shape!=hi.shape or lo.ndim!=2 or lo.shape[1]!=len(w): raise ValueError('Invalid shapes')
    if not (np.all(np.isfinite(lo)) and np.all(np.isfinite(hi)) and np.all(0<=lo) and np.all(lo<=hi) and np.all(hi<=1)): raise ValueError('Invalid utility bounds')
    if not (np.all(w>0) and np.isclose(w.sum(),1)): raise ValueError('Require positive normalized weights')
    lows=np.array([topsis_row(row,w) for row in lo]);rows=[];frontiers=[]
    for i,city in enumerate(cities):
        others=np.arange(len(cities))!=i; rival=np.flatnonzero(others)[np.argmax(lows[others])]
        hurdle=lows[rival]; unknown=np.flatnonzero(hi[i]-lo[i]>tol).tolist()
        smallest=None; bundles=[]
        for count in range(len(unknown)+1):
            for subset in itertools.combinations(unknown,count):
                hypothetical=hi[i].copy(); hypothetical[list(subset)]=lo[i,list(subset)]
                best_elimination_upper=topsis_row(hypothetical,w)
                if best_elimination_upper<hurdle-tol:
                    bundles.append(subset)
                    frontiers.append(dict(city=city,indicators='|'.join(names[j] for j in subset),size=count,
                        hypothetical_min_upper=best_elimination_upper,rival_lower=hurdle,
                        interpretation='possible outcome only; not observed and not guaranteed'))
            if bundles: smallest=count;break
        rows.append(dict(city=city,rival=cities[rival],rival_lower=hurdle,current_upper=topsis_row(hi[i],w),
            minimum_city_local_exact_measurements=smallest,minimal_bundle_count=len(bundles),
            possible_with_city_local_measurements=smallest is not None,
            no_single_cell_can_eliminate=smallest is None or smallest>1))
    return rows,frontiers


def elimination_threshold(lower,upper,weights,city_index,indicator_index,tol=1e-10):
    """Largest utility x with own upper score below competitor lower score.

    Return None if even x=lower cannot eliminate. Threshold is a strict cutoff;
    A finite cutoff denotes a tie; infinity means already excluded even at upper.
    Others stay at upper, so
    only observed x below cutoff certifies elimination with remaining unknowns.
    """
    lo=np.asarray(lower);hi=np.asarray(upper);w=np.asarray(weights)
    i,j=city_index,indicator_index
    hurdle=max(topsis_row(lo[k],w) for k in range(len(lo)) if k!=i)
    row=hi[i].copy()
    def f(x):
        row[j]=x;return topsis_row(row,w)-hurdle
    if f(lo[i,j])>=-tol:return None
    if f(hi[i,j])< -tol:return float('inf')
    a,b=lo[i,j],hi[i,j]
    for _ in range(70):
        mid=(a+b)/2
        if f(mid)<0:a=mid
        else:b=mid
    return float((a+b)/2)


def selfcheck():
    # Hand-checkable two criteria: rival lower = 50; candidate upper = 100.
    # One measurement at zero leaves score 50 (a tie), so TWO are necessary.
    lo=np.array([[0.,0.],[.5,.5]]);hi=np.array([[1.,1.],[.5,.5]]);w=np.array([.5,.5])
    rows,bundles=certificates(lo,hi,w,['a','b'],['unknown','rival'])
    assert rows[0]['minimum_city_local_exact_measurements']==2
    assert rows[1]['minimum_city_local_exact_measurements'] is None
    assert elimination_threshold(lo,hi,w,0,0) is None
    # Rival at .7: a single cell can eliminate, but only below its threshold.
    lo[1]=hi[1]=.7
    t=elimination_threshold(lo,hi,w,0,0)
    assert 0<t<1
    assert topsis_row(np.array([t-1e-5,1]),w)<70
    assert topsis_row(np.array([t+1e-5,1]),w)>70
    assert np.array_equal(lo[0],[0,0]) and np.array_equal(hi[0],[1,1])
    already_lo=np.array([[.1,.1],[.8,.8]])
    already_hi=np.array([[.2,.2],[.8,.8]])
    assert np.isinf(elimination_threshold(already_lo,already_hi,w,0,0))
    # Exhaustive monotone score corners verify endpoint feasibility on random rectangles.
    rng=np.random.default_rng(601)
    for _ in range(20):
        lo=rng.uniform(0,.5,(3,3));hi=lo+rng.uniform(0,1,(3,3))*(1-lo)
        w=rng.dirichlet(np.ones(3));rows,_=certificates(lo,hi,w,list('abc'),list('xyz'))
        for i in range(3):
            hurdle=max(topsis_row(lo[k],w) for k in range(3) if k!=i)
            feasible=[]
            for n in range(4):
                for sub in itertools.combinations(range(3),n):
                    for bits in itertools.product([0,1],repeat=n):
                        row=hi[i].copy()
                        for j,b in zip(sub,bits):row[j]=hi[i,j] if b else lo[i,j]
                        if topsis_row(row,w)<hurdle-1e-10:feasible.append(n)
            assert rows[i]['minimum_city_local_exact_measurements']==(min(feasible) if feasible else None)
    print('PASS: acquisition cardinality, tied-champion exclusion, threshold sides, no mutation, 20 exhaustive randomized rectangle checks')
if __name__=='__main__':selfcheck()
