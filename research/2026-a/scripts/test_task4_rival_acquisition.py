"""Cross-check rival certificates against the independent root-partition solver."""
import unittest
import numpy as np
from task4_rival_acquisition import polynomial_minimum,strict_certificates,analyze
from task4_combined_evidence import combined_bounds
from task4_continuous_preferences import feasible_preferences
from task4_v5_model import CITIES,NAMES,score,weights

class RivalCertificates(unittest.TestCase):
    def test_quadratic_cases(self):
        # Minimum at interior vertex, linear endpoint, concave endpoint, and tie.
        p=np.array([[.01,-.2,1],[0,1,0],[0,0,-1],[0,0,0]])
        np.testing.assert_allclose(polynomial_minimum(p),[0,.05,-.04,0],atol=1e-15)
        self.assertFalse(strict_certificates(np.full((1,10),.5),np.full((1,10),.5))[0][0,0])

    def test_random_independent_solver(self):
        rng=np.random.default_rng(20261108)
        for _ in range(120):
            x,y=rng.random((2,10))
            yes,_=strict_certificates(x[None,:],y[None,:])
            self.assertEqual(bool(yes[0,0]),not feasible_preferences(y,[x])['possible'])
            if yes[0,0]:
                for alpha in [.05,.1,.2]:self.assertGreater(score(x[None,:],weights(alpha))[0],score(y[None,:],weights(alpha))[0])

    def test_real_witnesses_and_budget_monotonicity(self):
        lo,hi=combined_bounds();saved=(lo.copy(),hi.copy());profiles,targets=analyze(lo,hi)
        checked=0
        for row in profiles:
            k=CITIES.index(row['source_city']);v=lo[k].copy()
            for name in filter(None,row['example_indicators'].split('|')):j=NAMES.index(name);v[j]=hi[k,j]
            excluded=list(filter(None,row['excluded_candidates'].split('|')))
            self.assertEqual(len(excluded),row['max_excluded']);self.assertNotIn(CITIES[k],excluded)
            for city in excluded:
                self.assertFalse(feasible_preferences(hi[CITIES.index(city)],[v])['possible']);checked+=1
        for city in CITIES:
            counts=[r['max_excluded'] for r in profiles if r['source_city']==city]
            self.assertEqual(counts,sorted(counts))
        for row in targets:
            n=row['minimum_single_rival_certificate_measurements']
            if n is not None:
                # Every profile below n has maximum 0 for this target, independently
                # enumerate all smaller subsets of every source city.
                import itertools
                i=CITIES.index(row['candidate'])
                for k in range(len(CITIES)):
                    if k==i:continue
                    uncertain=np.flatnonzero(hi[k]-lo[k]>1e-12)
                    for size in range(n):
                        for subset in itertools.combinations(uncertain,size):
                            v=lo[k].copy();v[list(subset)]=hi[k,list(subset)]
                            self.assertFalse(strict_certificates(v[None,:],hi[i:i+1])[0][0,0])
        np.testing.assert_array_equal(lo,saved[0]);np.testing.assert_array_equal(hi,saved[1])
        print('Independent root-partition checks for',checked,'reported real-data exclusion witnesses')

if __name__=='__main__':unittest.main()
