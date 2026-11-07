import unittest
import numpy as np
from task4_travel_scale_sensitivity import mean_utility_bounds

class ScaleBoundsTests(unittest.TestCase):
    def test_observed_distributions_are_enclosed(self):
        rng=np.random.default_rng(20261107)
        for _ in range(200):
            x=rng.uniform(0,1,25);w=rng.uniform(.1,5,25);m=np.average(x,weights=w)
            for tau in [15,20,30,45,60]:
                l,h=mean_utility_bounds(m,m,tau)
                value=np.average(x**(30/tau),weights=w)
                self.assertLessEqual(float(l),value+1e-14)
                self.assertGreaterEqual(float(h),value-1e-14)
    def test_sharp_constant_and_endpoint_mixtures(self):
        for m in [.0,.1,.5,.9,1.]:
            for tau in [15,60]:
                l,h=mean_utility_bounds(m,m,tau)
                values=[m**(30/tau),np.average(np.array([0.,1.])**(30/tau),weights=[1-m,m])]
                self.assertAlmostEqual(float(l),min(values))
                self.assertAlmostEqual(float(h),max(values))
    def test_missing_and_identity(self):
        for tau in [15,30,60]:
            np.testing.assert_array_equal(mean_utility_bounds([0],[1],tau),[[0],[1]])
        np.testing.assert_array_equal(mean_utility_bounds([.2,.4],[.6,.8],30),[[.2,.4],[.6,.8]])
    def test_invalid(self):
        for l,h,tau in [(.8,.2,30),(-.1,.5,30),(.2,1.1,30),(.2,.5,0),(.2,.5,float('nan'))]:
            with self.assertRaises(ValueError):mean_utility_bounds(l,h,tau)

if __name__=='__main__':unittest.main()
