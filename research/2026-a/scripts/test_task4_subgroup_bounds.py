"""Independent subset enumeration and LP checks for latent-group identification."""
import itertools
import unittest
import numpy as np
from scipy.optimize import linprog
from task4_subgroup_bounds import subgroup_bounds


class SubgroupBoundsTests(unittest.TestCase):
    def test_enumerate_all_integer_subgroups(self):
        capacities = [2, 1, 2]
        low = np.array([.05, .4, .8]); high = np.array([.2, .6, 1.])
        for m0 in range(1, 6):
            for m1 in range(m0, 6):
                feasible = [np.array(a) for a in itertools.product(range(3), range(2), range(3)) if m0 <= sum(a) <= m1]
                expected = min(a@low/a.sum() for a in feasible), max(a@high/a.sum() for a in feasible)
                np.testing.assert_allclose(subgroup_bounds(capacities, low, high, [m0,m1]), expected)

    def test_fractional_capacities_against_lp(self):
        rng = np.random.default_rng(70)
        for _ in range(50):
            n = rng.uniform(.1, 10, 5); low = rng.uniform(0,.7,5); high = low+rng.uniform(0,1,5)*(1-low)
            m = rng.uniform(.01,n.sum())
            args = dict(A_eq=np.ones((1,5)), b_eq=[m], bounds=list(zip(np.zeros(5),n)), method='highs')
            a,b = linprog(low,**args),linprog(-high,**args)
            self.assertTrue(a.success and b.success)
            np.testing.assert_allclose(subgroup_bounds(n,low,high,[m,n.sum()]),[a.fun/m,-b.fun/m],atol=1e-10)

    def test_parent_mean_does_not_bound_subgroup(self):
        # Parent mean is exactly 0.5; a one-person subgroup can have either endpoint.
        self.assertEqual(subgroup_bounds([1,1],[0,1],[0,1],[1,1]),(0.,1.))
        self.assertEqual(subgroup_bounds([0,2,3],[0,.2,.6],[1,.4,.8],[0,5]),(.2,.8))
        np.testing.assert_allclose(subgroup_bounds([2,3],[.2,.6],[.4,.8],[5,5]),[.44,.64])

    def test_invalid_inputs(self):
        for counts,low,high,mass in [([1],[.5],[.4],[1,1]),([0],[0],[1],[0,0]),([1],[0],[1],[0,2]),([-1],[0],[1],[0,1]),([1],[0],[1],[float('nan'),1])]:
            with self.assertRaises(ValueError): subgroup_bounds(counts,low,high,mass)


if __name__ == '__main__': unittest.main()
