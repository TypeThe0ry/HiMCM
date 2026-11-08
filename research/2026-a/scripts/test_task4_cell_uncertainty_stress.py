import unittest
import numpy as np
from task4_cell_uncertainty_stress import cell_bounds, regrets
from task4_joint_uncertainty_stress import rectangle_enclosure, certify_prefix


class CellStressTests(unittest.TestCase):
    def test_only_selected_cell_changes_and_inputs_stay_identical(self):
        lo=np.full((3,10),.1);hi=np.full((3,10),.8)
        l,h=cell_bounds(lo,hi,.3,(1,7))
        mask=np.ones(lo.shape,dtype=bool);mask[1,7]=False
        np.testing.assert_array_equal(l[mask],lo[mask]);np.testing.assert_array_equal(h[mask],hi[mask])
        self.assertEqual((l[1,7],h[1,7]),(0.,1.))
        np.testing.assert_array_equal(lo,np.full((3,10),.1))
        np.testing.assert_array_equal(hi,np.full((3,10),.8))

    def test_unknown_cell_is_invariant_under_withdrawal(self):
        lo=np.full((2,10),.3);hi=np.full((2,10),.7)
        lo[0,4]=0;hi[0,4]=1
        l,h=cell_bounds(lo,hi,1.,(0,4))
        np.testing.assert_array_equal(l,lo);np.testing.assert_array_equal(h,hi)

    def test_bad_cell_cannot_silently_select_whole_row(self):
        lo=np.zeros((3,10));hi=np.ones((3,10))
        for cell in [1,(1,),(-1,0),(3,0),(1,10),(1,1.5)]:
            with self.assertRaises(ValueError):cell_bounds(lo,hi,.2,cell)

    def test_cell_enclosure_contains_interior_with_clipping(self):
        rng=np.random.default_rng(991)
        for _ in range(10):
            lo=rng.uniform(0,.7,(4,10));hi=lo+rng.uniform(0,1,(4,10))*(1-lo)
            cell=(int(rng.integers(4)),int(rng.integers(10)))
            lower,upper=rectangle_enclosure(lo,hi,.03,.4,.05,.2,cell)
            for _ in range(20):
                l,h=cell_bounds(lo,hi,rng.uniform(.03,.4),cell)
                rr=regrets(l,h,rng.uniform(.05,.2))
                self.assertTrue(np.all(lower<=rr) and np.all(rr<=upper))

    def test_nonfirst_choice_and_ties_remain_distinct(self):
        x=np.array([[.1]*10,[.9]*10])
        self.assertTrue(all(r['certified'] for r in certify_prefix(x,x,1,target=(1,4),max_depth=3)))
        tied=np.full((2,10),.5)
        self.assertFalse(any(r['certified'] for r in certify_prefix(tied,tied,1,target=(1,4),max_depth=3)))


if __name__=='__main__':unittest.main()
