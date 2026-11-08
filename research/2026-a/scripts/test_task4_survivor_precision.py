import itertools,unittest
import numpy as np
from task4_survivor_precision import finite_completion,evaluate,frontier
from task4_survivor_set_search import endpoint_completion
from task4_v5_model import score,weights

class PrecisionTests(unittest.TestCase):
    def setUp(self):
        rng=np.random.default_rng(104);self.lo=rng.uniform(.1,.3,(3,10));self.hi=self.lo+rng.uniform(.1,.5,(3,10));self.mask=np.zeros_like(self.lo,bool);self.mask[:,[0,4,7]]=True

    def test_zero_matches_exact_and_one_restores_original(self):
        for actual,want in zip(finite_completion(self.lo,self.hi,self.mask,(0,),0),endpoint_completion(self.lo,self.hi,self.mask,(0,))):np.testing.assert_array_equal(actual,want)
        for actual,want in zip(finite_completion(self.lo,self.hi,self.mask,(0,),1),(self.lo,self.hi)):np.testing.assert_allclose(actual,want,atol=1e-15)

    def test_width_clipping_nested_intervals_and_no_unselected_change(self):
        self.hi[0,0]=self.lo[0,0];previous=None
        for d in [0,.01,.1,.5,1]:
            l,h=finite_completion(self.lo,self.hi,self.mask,(0,1),d)
            np.testing.assert_array_equal(l[~self.mask],self.lo[~self.mask]);np.testing.assert_array_equal(h[~self.mask],self.hi[~self.mask])
            np.testing.assert_allclose((h-l)[self.mask],np.minimum(d,self.hi-self.lo)[self.mask],atol=1e-15)
            if previous is not None:self.assertTrue(np.all(l<=previous[0]+1e-15));self.assertTrue(np.all(h>=previous[1]-1e-15))
            previous=(l,h)

    def test_invalid_width_rejected(self):
        for d in [-.1,1.1,np.nan,np.inf,[.1]]:
            with self.assertRaises(ValueError):finite_completion(self.lo,self.hi,self.mask,(0,),d)

    def test_shared_interior_intervals_obey_extremal_reduction(self):
        d=np.minimum(.1,self.hi-self.lo)
        for keep in [(0,),(1,),(0,1)]:
            outside=[i for i in range(3) if i not in keep];el,eh=finite_completion(self.lo,self.hi,self.mask,keep,.1)
            for frac in itertools.product([0,.5,1],repeat=3):
                l=np.where(self.mask,self.lo+np.array(frac)[:,None]*(self.hi-self.lo-d),self.lo);h=np.where(self.mask,l+d,self.hi)
                for a in [.05,.1,.2]:
                    if np.all(score(h,weights(a))[outside]<max(score(l,weights(a))[list(keep)])):
                        self.assertTrue(np.all(score(eh,weights(a))[outside]<max(score(el,weights(a))[list(keep)])))

    def test_exact_tie_stays_unresolved(self):
        lo=np.zeros((2,10));hi=np.ones_like(lo);mask=np.ones_like(lo,bool)
        r=evaluate(lo,hi,mask,(0,),.5)
        self.assertEqual(r['status'],'unresolved_boundary')
        b=frontier(lo,hi,mask,(0,),precision=1e-4)
        self.assertEqual(b['status'],'bracketed_with_unresolved_boundary')
        self.assertLess(b['feasible']['delta'],.5);self.assertGreater(b['infeasible']['delta'],.5)

if __name__=='__main__':unittest.main()
