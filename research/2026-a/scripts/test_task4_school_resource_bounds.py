import unittest
import numpy as np
from task4_school_resource_bounds import resource_bounds
class BoundsTests(unittest.TestCase):
    def test_missing_retained(self):
        l,h,m,c=resource_bounds([100,100],[10,np.nan]);self.assertEqual(l,0);self.assertAlmostEqual(h,.8);self.assertEqual(m,.5)
    def test_all_missing(self):
        self.assertEqual(resource_bounds([1,9],[np.nan,np.nan])[:3],(0.,1.,1.))
    def test_weighted_not_school_average(self):
        self.assertAlmostEqual(resource_bounds([100,300],[10,np.nan])[1],.9)
    def test_resolution_monotonicity(self):
        self.assertLess(resource_bounds([100,100],[10,20])[1],resource_bounds([100,100],[10,np.nan])[1])
    def test_split_invariance(self):
        np.testing.assert_allclose(resource_bounds([100,100],[10,np.nan])[:3],resource_bounds([50,50,100],[5,5,np.nan])[:3])
    def test_small_endpoint_enumeration(self):
        import itertools
        s=np.array([10.,20.,30.]);t=np.array([1.,4.,np.nan]);values=[]
        for choices in itertools.product([0.,1.],repeat=3):
            u=np.array([15*t[k]*choices[k]/(s[k]+15*t[k]*choices[k]) for k in range(2)]+[choices[2]])
            values.append((s@u)/s.sum())
        l,h,_,_=resource_bounds(s,t)
        self.assertAlmostEqual(l,min(values));self.assertAlmostEqual(h,max(values))
    def test_complete_jensen(self):
        s=np.array([100.,200.]);t=np.array([5.,40.]);pool=15*t.sum()/(s.sum()+15*t.sum())
        self.assertLessEqual(resource_bounds(s,t)[1],pool)
    def test_invalid(self):
        for s,t in [([0],[1]),([1],[-1]),([1],[np.inf]),([np.nan],[1])]:
            with self.assertRaises(ValueError):resource_bounds(s,t)
if __name__=='__main__':unittest.main()
