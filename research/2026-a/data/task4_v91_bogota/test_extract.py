"""Regression checks for the observed thousands-separator parsing defect."""
import unittest
import pandas as pd
from extract import numeric

class NumericParsingTest(unittest.TestCase):
    def test_european_grouping_and_decimal(self):
        actual = numeric(pd.Series(['1.554,6','12.345.678,90',' 683,2 ','274,9','1554.6','0','-1.554,6']))
        self.assertEqual(actual.tolist(), [1554.6,12345678.9,683.2,274.9,1554.6,0,-1554.6])

    def test_missing_and_malformed_are_not_filled(self):
        self.assertTrue(numeric(pd.Series(['-',None,'','1.23,4','12.34.567,8'])).isna().all())

    def test_period_not_blindly_stripped(self):
        self.assertEqual(numeric(pd.Series(['15.5','1234.567','1.234,5'])).tolist(), [15.5,1234.567,1234.5])

if __name__ == '__main__':
    unittest.main()
