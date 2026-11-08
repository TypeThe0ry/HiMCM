"""Focused checks for conditional integer count bounds."""
import unittest
from reconstruct import integer_ranges


class CountBoundsTest(unittest.TestCase):
    def test_small_integer_populations(self):
        for n in range(1, 21):
            for a in range(n+1):
                for b in range(n-a+1):
                    actual = (a, b, n-a-b)
                    tenths = [(2000*k+n)//(2*n) for k in actual]
                    lower, upper = integer_ranges(n, [q/10 for q in tenths])
                    self.assertEqual(lower, list(actual))
                    self.assertEqual(upper, list(actual))

    def test_uninterpretable_and_incompatible(self):
        self.assertIsNone(integer_ranges(9, [0, 0, 0]))
        self.assertIsNone(integer_ranges(3, [33.3, 33.3, 33.4]))
        with self.assertRaises(ValueError):
            integer_ranges(10, [float('nan'), 0, 100])

    def test_rounding_ties_and_total_constraint(self):
        self.assertEqual(integer_ranges(2000, [50, 25, 25]),
                         ([999, 499, 499], [1001, 501, 501]))
        self.assertEqual(integer_ranges(2000, [33.3, 33.3, 33.3]),
                         ([666, 666, 666], [667, 667, 667]))


if __name__ == '__main__':
    unittest.main()
