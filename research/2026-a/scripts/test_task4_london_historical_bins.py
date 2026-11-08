import unittest
from task4_london_historical_bins import rounded_bin_bounds

class RoundedBinTests(unittest.TestCase):
    def test_exact_percentages(self):
        r=rounded_bin_bounds([50,50],[0,.5],[.25,1],0)
        self.assertEqual(r['utility_lower'],.25);self.assertEqual(r['utility_upper'],.625)

    def test_all_missing_remains_fully_unknown(self):
        r=rounded_bin_bounds([100],[0],[1],.5)
        self.assertEqual([r['utility_lower'],r['utility_upper']],[0,1])

    def test_infeasible_published_total_is_not_renormalized(self):
        with self.assertRaises(ValueError):rounded_bin_bounds([30,69],[0,0],[1,1],0)

    def test_rounding_relaxation_only_expands_envelope(self):
        a=rounded_bin_bounds([30,69],[.2,.4],[.6,1],.5)
        b=rounded_bin_bounds([30,69],[.2,.4],[.6,1],1)
        self.assertLessEqual(b['utility_lower'],a['utility_lower']);self.assertGreaterEqual(b['utility_upper'],a['utility_upper'])
        for r in [a,b]:
            self.assertAlmostEqual(sum(r['lower_probability_witness']),1);self.assertAlmostEqual(sum(r['upper_probability_witness']),1)

    def test_invalid_utility_interval_rejected(self):
        with self.assertRaises(ValueError):rounded_bin_bounds([100],[.8],[.2])

if __name__=='__main__':unittest.main()
