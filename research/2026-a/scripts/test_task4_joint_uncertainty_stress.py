import unittest
import numpy as np
from task4_joint_uncertainty_stress import expand,rectangle_enclosure,certify_prefix
from task4_v5_model import score,weights

class JointStressTests(unittest.TestCase):
    def test_enclosure_contains_interior_regrets_with_clipping(self):
        rng=np.random.default_rng(6701)
        for _ in range(15):
            lo=rng.uniform(0,.7,(4,10));hi=lo+rng.uniform(0,1,(4,10))*(1-lo)
            for target in [None,0]:
                lower,upper=rectangle_enclosure(lo,hi,.03,.45,.05,.2,target)
                for _ in range(20):
                    l,h=expand(lo,hi,rng.uniform(.03,.45),target)
                    a=rng.uniform(.05,.2);ls,us=score(l,weights(a)),score(h,weights(a))
                    r=np.array([max(0,np.delete(us,i).max()-ls[i]) for i in range(4)])
                    self.assertTrue(np.all(lower<=r) and np.all(r<=upper))

    def test_ties_unresolved_and_dominance_certified(self):
        tied=np.full((2,10),.5)
        self.assertFalse(any(x['certified'] for x in certify_prefix(tied,tied,0,max_depth=2)))
        x=np.array([[.9]*10,[.1]*10])
        self.assertTrue(all(r['certified'] for r in certify_prefix(x,x,0)))

    def test_targeted_expansion_preserves_other_rows(self):
        x=np.array([[.2]*10,[.6]*10]);l,h=expand(x,x,.3,0)
        np.testing.assert_array_equal(l[1],x[1]);np.testing.assert_array_equal(h[1],x[1])
        np.testing.assert_array_equal(l[0],np.zeros(10))
        with self.assertRaises(ValueError):expand(x,x,-.1)
        with self.assertRaises(ValueError):expand(x,x-.1,.1)
        z=np.array([[0]*10,[1]*10]);l,h=expand(z,z,.2)
        np.testing.assert_allclose(h[0],.2);np.testing.assert_allclose(l[1],.8)

if __name__=='__main__':unittest.main()
