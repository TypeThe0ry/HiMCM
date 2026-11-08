"""Analytic threshold, degenerate cases and continuous-preference monotonicity."""
import unittest
import json,tempfile
from pathlib import Path
from unittest.mock import patch
import numpy as np
from task4_precision_frontier import threshold
from task4_continuous_preferences import feasible_preferences

class PrecisionTests(unittest.TestCase):
    def test_foreign_output_is_preserved(self):
        from task4_precision_frontier import run,KIND
        x=np.full((25,10),.5)
        for previous in ({'analysis_kind':'stress','city':'Phoenix'},{'analysis_kind':KIND,'city':'Tokyo'}):
            with tempfile.TemporaryDirectory() as tmp:
                out=Path(tmp);p=out/'summary.json';p.write_text(json.dumps(previous));before=p.read_bytes()
                with patch('task4_precision_frontier.current_bounds',return_value=(x,x,{})):
                    with self.assertRaisesRegex(ValueError,'different analysis or city'):run(out)
                self.assertEqual(p.read_bytes(),before)
                self.assertEqual(list(out.iterdir()),[p])

    def test_analytic_equal_coordinate_threshold(self):
        lo=np.array([[0.]*10,[.5]*10]);hi=np.array([[1.]*10,[.5]*10])
        result=threshold(lo,hi,0,range(10),(.3,.4))
        self.assertEqual(result['status'],'bracketed')
        self.assertLessEqual(result['possible_rho']-result['excluded_rho'],2**-40)
        self.assertAlmostEqual(result['excluded_rho'],.5,places=9)
        self.assertAlmostEqual(result['possible_rho'],.5,places=9)
        self.assertFalse(feasible_preferences(np.full(10,result['excluded_rho']),lo[1:],.3,.4)['possible'])
        self.assertTrue(feasible_preferences(np.full(10,result['possible_rho']),lo[1:],.3,.4)['possible'])
        # Same residual width anchored at the upper end keeps upper=1: no exclusion.
        self.assertTrue(feasible_preferences(hi[0],lo[1:],.3,.4)['possible'])

    def test_ties_already_excluded_and_invalid_inputs(self):
        tied=np.full((2,10),.5)
        self.assertEqual(threshold(tied,tied,0,[])['status'],'cannot_exclude_even_exact')
        worse=tied.copy();worse[0]=.4
        self.assertEqual(threshold(worse,worse,0,[])['status'],'already_excluded')
        for subset in ([0,0],[10],[.5]):
            with self.assertRaises(ValueError):threshold(tied,tied,0,subset)
        with self.assertRaises(ValueError):threshold(tied,tied,.5,[])
        with self.assertRaises(ValueError):threshold(tied,tied,0,[],(.4,.3))

    def test_continuous_feasibility_monotone_in_residual(self):
        rng=np.random.default_rng(7601)
        for _ in range(15):
            lo=rng.uniform(.1,.5,(4,10));hi=lo+rng.uniform(.1,.4,(4,10));js=[1,4,6,7]
            states=[]
            for rho in np.linspace(0,1,13):
                row=hi[0].copy();row[js]=lo[0,js]+rho*(hi[0,js]-lo[0,js])
                states.append(feasible_preferences(row,lo[1:])['possible'])
            self.assertEqual(states,sorted(states))

if __name__=='__main__':unittest.main()
