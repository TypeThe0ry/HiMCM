"""Shared revelation, nonattainment and tie cases with analytic solutions."""
import unittest
import numpy as np
from task4_joint_acquisition_minima import analyse


class JointMinimaTests(unittest.TestCase):
    def test_shared_completion_is_one_matrix_and_preserves_inputs(self):
        lo = np.full((3, 10), .2); hi = np.full((3, 10), .8)
        mask = np.ones_like(lo, bool); mask[:, 0] = False
        saved = (lo.copy(), hi.copy())
        cert, answers = analyse(lo, hi, mask, preferred_anchor=0)
        for l, h, rows, result in answers:
            self.assertEqual(result['certified_minimum'], 1)
            self.assertEqual(result['surviving_indices'], [0])
            np.testing.assert_array_equal(l[mask], h[mask])
            np.testing.assert_array_equal(l[:, 0], lo[:, 0])
            np.testing.assert_array_equal(h[:, 0], hi[:, 0])
            np.testing.assert_array_equal(l[0, 1:], hi[0, 1:])
            np.testing.assert_array_equal(h[1:, 1:], lo[1:, 1:])
        np.testing.assert_array_equal(lo, saved[0]); np.testing.assert_array_equal(hi, saved[1])

    def test_a_failed_anchor_is_not_called_the_global_minimum(self):
        lo = np.array([[.1]*10, [.5]*10, [.5]*10])
        hi = np.array([[.4]*10, [.9]*10, [.9]*10])
        mask = np.ones_like(lo, bool)
        cert, failed = analyse(lo, hi, mask, preferred_anchor=0)
        for l, h, rows, result in failed:
            self.assertEqual(result['universal_count_lower_bound'], 1)
            self.assertEqual(result['attained_count_upper_bound'], 2)
            self.assertFalse(result['joint_minimum_certified'])
            self.assertIsNone(result['certified_minimum'])
            self.assertEqual(result['status'], 'unresolved_gap')
        # A different legal completion proves the failure was of this witness,
        # not evidence that the true minimum is two.
        _, succeeded = analyse(lo, hi, mask, preferred_anchor=1)
        self.assertTrue(all(r[3]['certified_minimum'] == 1 for r in succeeded))

    def test_exact_ties_and_empty_measurement_cannot_invent_exclusion(self):
        tied = np.full((3, 10), .5)
        for mask in (np.ones_like(tied, bool), np.zeros_like(tied, bool)):
            _, answers = analyse(tied, tied, mask)
            self.assertTrue(all(r[3]['certified_minimum'] == 3 for r in answers))

    def test_unavoidable_city_does_not_make_its_count_attainable(self):
        lo = np.array([[0.]*10, [.2]*10, [.3]*10])
        hi = np.array([[1.]*10, [.9]*10, [.8]*10])
        mask = np.ones_like(lo, bool); mask[0] = False
        _, answers = analyse(lo, hi, mask)
        for l, h, rows, result in answers:
            self.assertEqual(result['unavoidable_indices'], [0])
            self.assertEqual(result['universal_count_lower_bound'], 1)
            self.assertEqual(result['attained_count_upper_bound'], 2)
            self.assertIsNone(result['certified_minimum'])
            self.assertEqual(result['status'], 'unresolved_gap')

    def test_invalid_inputs_do_not_generate_a_witness(self):
        lo = np.full((3, 10), .2); hi = np.full((3, 10), .8)
        with self.assertRaises(ValueError): analyse(hi, lo, np.ones_like(lo, bool))
        with self.assertRaises(ValueError): analyse(lo, hi, np.ones_like(lo, float))
        with self.assertRaises(ValueError): analyse(lo, hi, np.ones_like(lo, bool), preferred_anchor=3)


if __name__ == '__main__':
    unittest.main()
