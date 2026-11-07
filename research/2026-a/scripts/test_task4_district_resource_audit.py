import unittest
import numpy as np
from task4_district_resource_audit import resource_gap
class ResourceGapTests(unittest.TestCase):
    def test_homogeneous_is_exact(self):
        pool,local,gap,_=resource_gap([100,200],[10,20]);self.assertAlmostEqual(pool,local);self.assertAlmostEqual(gap,0)
    def test_known_heterogeneity(self):
        pool,local,gap,_=resource_gap([100,100],[0,20]);self.assertAlmostEqual(pool,.6);self.assertAlmostEqual(local,.375);self.assertAlmostEqual(gap,.225)
    def test_split_invariance(self):
        a=resource_gap([100,200],[5,40]);b=resource_gap([50,50,200],[2.5,2.5,40]);np.testing.assert_allclose(a[:3],b[:3],atol=1e-14,rtol=0)
    def test_invalid_counts(self):
        for s,t in [([0,1],[1,1]),([1],[float('nan')]),([1,2],[1]),([1],[-1])]:
            with self.assertRaises(ValueError):resource_gap(s,t)
if __name__=='__main__':unittest.main()
