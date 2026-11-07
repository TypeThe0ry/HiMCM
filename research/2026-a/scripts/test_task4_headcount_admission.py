"""Regression checks for diagnostic/FTE rows entering headcount-only targets."""
import unittest
import numpy as np
import pandas as pd
from task4_v5_model import admitted_v5, ROOT, CITIES, NAMES
from task4_v6_model import admit_observations
from task4_v7_model import baseline, apply_bounds, collect

class AdmissionTests(unittest.TestCase):
    def test_legacy_diagnostic_rejected(self):
        row=dict(indicator='upper_secondary_ptr',value=20.4,unit='students_per_teacher_FTE',status='diagnostic_complete_record_subset_not_admitted_citywide')
        self.assertFalse(admitted_v5('education',row))
    def test_known_status_cannot_override_fte_unit(self):
        row=dict(indicator='upper_secondary_ptr',unit='students_per_teacher_FTE',status='observed_upper_secondary_scope_conditional')
        self.assertFalse(admitted_v5('education',row))
    def test_unreviewed_observed_status_rejected(self):
        self.check_v6_rejected('observed_mixed_grade_subset','students_per_teacher_headcount')
    def test_headcount_substring_not_sufficient(self):
        self.check_v6_rejected('observed_general_upper_secondary_scope_conditional','students_per_teacher_not_headcount')
    def test_approved_unit_must_match_reviewed_status(self):
        self.check_v6_rejected('observed_general_upper_secondary_scope_conditional','students_per_teacher_including_headmaster_headcount')
    def check_v6_rejected(self,status,unit):
        lo=np.zeros((len(CITIES),len(NAMES)));hi=np.ones_like(lo)
        row=dict(city='Phoenix',indicator='upper_secondary_ptr',value=20,status=status,unit=unit)
        l,h,audit=admit_observations(lo,hi,pd.DataFrame([row]))
        np.testing.assert_array_equal(l,lo);np.testing.assert_array_equal(h,hi)
        self.assertFalse(audit[0]['admitted'])
    def test_existing_admitted_endpoints_unchanged(self):
        l,h,_=apply_bounds(*baseline(),collect())
        old=pd.read_csv(ROOT/'results/task4_v7/utility_bounds.csv')
        for r in old.to_dict('records'):
            i=CITIES.index(r['city']);j=NAMES.index(r['indicator'])
            self.assertAlmostEqual(l[i,j],r['after_lower'],places=12)
            self.assertAlmostEqual(h[i,j],r['after_upper'],places=12)

if __name__=='__main__':unittest.main()
