import itertools,unittest
import numpy as np
from task4_survivor_set_search import endpoint_completion,evaluate,search
from task4_v5_model import score,weights

class SurvivorSetTests(unittest.TestCase):
    def test_shared_completion_changes_only_selected_cells(self):
        lo=np.full((3,10),.2);hi=np.full((3,10),.8);mask=np.zeros_like(lo,bool);mask[:,7]=True
        l,h=endpoint_completion(lo,hi,mask,(1,))
        np.testing.assert_array_equal(l[~mask],lo[~mask]);np.testing.assert_array_equal(h[~mask],hi[~mask])
        np.testing.assert_array_equal(l[:,7],[.2,.8,.2]);np.testing.assert_array_equal(h[:,7],l[:,7])

    def test_boundary_tie_is_not_excluded_or_false_minimum(self):
        lo=hi=np.full((3,10),.5);mask=np.ones_like(lo,bool)
        self.assertEqual(evaluate(lo,hi,mask,(0,))['status'],'unresolved_boundary')
        r=search(lo,hi,mask,(),3)
        self.assertFalse(r['minimum_proved']);self.assertIsNone(r['certified_minimum'])
        self.assertEqual(r['attained_upper_bound'],3)

    def test_fully_measured_strict_witness_attains_one(self):
        lo=np.full((3,10),.1);hi=np.full((3,10),.9);mask=np.ones_like(lo,bool)
        r=search(lo,hi,mask,(),3)
        self.assertEqual(r['certified_minimum'],1);self.assertEqual(len(r['successful_sets']),3)

    def test_endpoint_reduction_against_shared_interior_completions(self):
        rng=np.random.default_rng(103)
        lo=rng.uniform(.1,.4,(3,10));hi=lo+rng.uniform(.1,.3,(3,10));mask=np.zeros_like(lo,bool);mask[:,7]=True
        for keep in [(0,),(1,),(2,),(0,1),(0,2),(1,2)]:
            outside=[i for i in range(3) if i not in keep];endlo,endhi=endpoint_completion(lo,hi,mask,keep)
            for fractions in itertools.product((0,.5,1),repeat=3):
                l,h=lo.copy(),hi.copy();l[:,7]=h[:,7]=lo[:,7]+np.array(fractions)*(hi[:,7]-lo[:,7])
                for a in [.05,.1,.2]:
                    if np.all(score(h,weights(a))[outside]<max(score(l,weights(a))[list(keep)])):
                        self.assertTrue(np.all(score(endhi,weights(a))[outside]<max(score(endlo,weights(a))[list(keep)])))

    def test_invalid_empty_or_duplicate_survivors_rejected(self):
        lo=np.zeros((2,10));hi=np.ones_like(lo);mask=np.ones_like(lo,bool)
        for k in [(),(0,0),(-1,),(2,)]:
            with self.assertRaises(ValueError):endpoint_completion(lo,hi,mask,k)

if __name__=='__main__':unittest.main()
