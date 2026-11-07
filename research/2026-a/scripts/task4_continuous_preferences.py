"""Certify TOPSIS comparisons over a continuous main/auxiliary weight range.

Within each group weights are equal; alpha is total auxiliary mass. Comparing
scores reduces to a quadratic in alpha. Partition at ALL real comparison roots,
so the search is not a sampled sensitivity grid. Numerical tolerance is explicit.
"""
import numpy as np
MAIN=np.array([0,1,2,3,4,5,7,8]);AUX=np.array([6,9])


def terms(u):
    u=np.asarray(u,float)
    if u.shape!=(10,) or not np.isfinite(u).all() or np.any((u<0)|(u>1)):raise ValueError('Ten finite utilities in [0,1] required')
    b0=np.mean(u[MAIN]**2);b1=np.mean(u[AUX]**2)
    a0=np.mean((1-u[MAIN])**2);a1=np.mean((1-u[AUX])**2)
    return np.array([a0,a1-a0]),np.array([b0,b1-b0])


def comparison(u,v):
    """Coefficient vector G(alpha): score(u)>=score(v) iff G>=0."""
    a,b=terms(u);c,d=terms(v)
    return np.polynomial.polynomial.polysub(np.polynomial.polynomial.polymul(b,c),np.polynomial.polynomial.polymul(d,a))


def feasible_preferences(candidate,challengers,alpha_min=.05,alpha_max=.2,tol=1e-12):
    return feasible_polynomials([comparison(candidate,r) for r in challengers],alpha_min,alpha_max,tol)


def feasible_polynomials(polys,alpha_min=.05,alpha_max=.2,tol=1e-12):
    """Common nonnegative region of comparison polynomials on an interval."""
    if not 0<alpha_min<=alpha_max<1:raise ValueError('Interior alpha interval required')
    cuts=[float(alpha_min),float(alpha_max)]
    for p in polys:
        q=np.trim_zeros(p,'b')
        if len(q)>1:
            for root in np.polynomial.polynomial.polyroots(q):
                if abs(root.imag)<1e-10 and alpha_min<root.real<alpha_max:cuts.append(float(root.real))
    cuts=sorted(set(cuts))
    def valid(x):return all(np.polynomial.polynomial.polyval(x,p)>=-tol for p in polys)
    # All signs are constant on every open segment between consecutive roots.
    intervals=[(a,b) for a,b in zip(cuts[:-1],cuts[1:]) if valid((a+b)/2)]
    points=[x for x in cuts if valid(x)]
    witness=(sum(intervals[0])/2 if intervals else points[0] if points else None)
    return dict(possible=witness is not None,witness_alpha=witness,feasible_interval_closures=intervals,feasible_boundary_points=points,
                partition_count=len(cuts),tolerance=tol)


def robust_exclusion_cutoff(lower,upper,i,j,alpha_min=.05,alpha_max=.2,tol=1e-12):
    """Strict utility cutoff excluding i at EVERY allowed alpha.

    None: lower endpoint cannot certify exclusion. Infinity: already excluded.
    Finite cutoff is conservative for floating tolerance; tie remains possible.
    """
    lo=np.asarray(lower,float);hi=np.asarray(upper,float);others=np.arange(len(lo))!=i
    row=hi[i].copy()
    def possible(x):
        row[j]=x
        return feasible_preferences(row,lo[others],alpha_min,alpha_max,tol)['possible']
    if possible(lo[i,j]):return None
    if not possible(hi[i,j]):return float('inf')
    a,b=float(lo[i,j]),float(hi[i,j])
    for _ in range(65):
        m=(a+b)/2
        if possible(m):b=m
        else:a=m
    return a


def selfcheck():
    from task4_v5_model import score,weights
    rng=np.random.default_rng(802)
    for _ in range(100):
        x,y=rng.uniform(0,1,(2,10));p=comparison(x,y)
        for alpha in rng.uniform(.05,.2,5):
            a=score(np.array([x,y]),weights(alpha))
            assert np.sign(a[0]-a[1])==np.sign(np.polynomial.polynomial.polyval(alpha,p))
    # All exact ties are feasible; componentwise dominated vectors never are.
    assert feasible_preferences(np.full(10,.5),[np.full(10,.5)])['possible']
    assert not feasible_preferences(np.full(10,.4),[np.full(10,.5)])['possible']
    for _ in range(40):
        x=rng.uniform(0,1,10);ys=rng.uniform(0,1,(4,10))
        r=feasible_preferences(x,ys)
        grid=np.linspace(.05,.2,1001)
        brute=any(np.all(score(np.vstack([x,ys]),weights(a))[0]>=score(ys,weights(a))-1e-10) for a in grid)
        if brute:assert r['possible']
        if r['possible']:
            a=r['witness_alpha'];s=score(np.vstack([x,ys]),weights(a))
            assert s[0]>=max(s[1:])-1e-8
    print('PASS: 500 score-polynomial signs, exact ties, dominance, 40 dense-grid cross-checks and feasible witnesses')
if __name__=='__main__':selfcheck()
