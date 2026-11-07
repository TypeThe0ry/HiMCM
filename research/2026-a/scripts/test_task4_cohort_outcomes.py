import unittest
import numpy as np
from task4_cohort_outcomes import outcome_terms,outcome_feasible,scenario_bounds
from task4_combined_evidence import combined_bounds
from task4_continuous_preferences import feasible_preferences
from task4_v5_model import score,weights,summarize

class CohortModel(unittest.TestCase):
    def test_zero_weight_reproduces_all_baseline_cities(self):
        l,h=combined_bounds();expected,_=summarize(l,h,weights())
        for lo,hi in scenario_bounds().values():
            actual,_=summarize(lo,hi,np.r_[weights(),0])
            np.testing.assert_allclose(actual.select_dtypes('number'),expected.select_dtypes('number'),rtol=0,atol=1e-12)
            for i in range(len(lo)):
                mask=np.arange(len(lo))!=i
                self.assertEqual(outcome_feasible(hi[i],lo[mask],0)['possible'],feasible_preferences(h[i],l[mask])['possible'])

    def test_affine_terms_and_collapsed_range(self):
        rng=np.random.default_rng(20261107)
        for _ in range(80):
            rows=rng.random((5,11));beta=rng.uniform(.01,.4);alpha=rng.uniform(.05,.2)
            scores=score(rows,np.r_[(1-beta)*weights(alpha),beta])
            for row,expected in zip(rows,scores):
                a,b=outcome_terms(row,beta);aa=a[0]+alpha*a[1];bb=b[0]+alpha*b[1]
                self.assertAlmostEqual(100*np.sqrt(bb)/(np.sqrt(aa)+np.sqrt(bb)),expected,places=12)
            result=outcome_feasible(rows[0],rows[1:],beta,alpha,alpha)
            self.assertEqual(result['possible'],scores[0]>=max(scores[1:]))
        self.assertTrue(outcome_feasible(np.full(11,.5),[np.full(11,.5)],.1)['possible'])

    def test_evidence_reduces_only_admitted_city_intervals(self):
        cases=scenario_bounds();lo,hi=cases['phoenix_unrestricted'];ll,hh=cases['phoenix_nyc2024']
        from task4_v5_model import CITIES
        i=CITIES.index('New York');mask=np.arange(len(lo))!=i
        np.testing.assert_array_equal(lo[mask],ll[mask]);np.testing.assert_array_equal(hi[mask],hh[mask])
        self.assertTrue(np.all(ll>=lo));self.assertTrue(np.all(hh<=hi))
        self.assertGreater(hh[i,-1],ll[i,-1])

if __name__=='__main__':unittest.main()
