"""Analytic identification cases, including outcomes and impossible champions."""
import unittest
import numpy as np
from task4_optimism_threshold import threshold

class ThresholdTests(unittest.TestCase):
    def test_uniform_analytic(self):
        for n,beta in [(10,0),(11,.1)]:
            for rival in [.1,.3,.5,.8,1.]:
                r=threshold(np.zeros(n),np.ones(n),np.full((2,n),rival),beta)
                self.assertTrue(r['possible'])
                self.assertAlmostEqual(r['threshold_upper'],rival,places=8)
                self.assertLessEqual(r['threshold_upper']-r['threshold_lower'],2**-45)
    def test_already_possible_and_impossible(self):
        self.assertEqual(threshold(np.ones(10)*.7,np.ones(10),np.ones((2,10))*.6)['threshold_upper'],0)
        self.assertFalse(threshold(np.zeros(10),np.ones(10)*.5,np.ones((2,10))*.6)['possible'])
    def test_interval_not_zero_origin(self):
        r=threshold(np.ones(10)*.2,np.ones(10)*.8,np.ones((2,10))*.5)
        self.assertAlmostEqual(r['threshold_upper'],.5,places=8)

if __name__=='__main__':unittest.main()
