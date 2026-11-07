"""Checks of evidence semantics and exact interval score propagation."""
import itertools
import numpy as np
from task4_v5_model import build,weights,score,NAMES,CITIES,summarize

def main():
    l0,h0,_=build(False);l,h,audit=build();w=weights()
    assert np.all(l>=l0) and np.all(h<=h0)
    assert np.allclose(l[:,7],l0[:,7]) and np.allclose(h[:,7],h0[:,7])
    assert np.count_nonzero(h[:,7]-l[:,7]<1)==3
    assert np.all(l[:,NAMES.index('public_pool_density')]==0)
    assert np.all(h[:,NAMES.index('public_pool_density')]==1)
    assert np.isclose(w.sum(),1) and np.allclose(w[[0,1,2,3,4,5,7,8]],.1125)
    for r in audit:
        if str(r.get('lower_bound_only',False)).lower()=='true':
            assert r['utility_upper']==1 and 0<r['utility_lower']<1
    # Enumerate corners for all ten utility dimensions in a real city.
    i=CITIES.index('Singapore')
    vertices=np.array([np.where(bits,h[i],l[i]) for bits in itertools.product([0,1],repeat=10)])
    s=score(vertices,w)
    assert np.isclose(s.min(),score(l,w)[i]) and np.isclose(s.max(),score(h,w)[i])
    # A withheld source expands, rather than narrows, evidence intervals.
    ls,hs,_=build(strict='no_air')
    assert np.all(ls<=l) and np.all(hs>=h)
    print('PASS: nesting, preserved teen commute, unknown pools, fixed weights, one-sided inventories, 1024 score corners, source-withholding expansion')
if __name__=='__main__': main()
