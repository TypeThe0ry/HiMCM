import unittest
from task4_phoenix_public_year_control import public_utility

class PublicCoverageTests(unittest.TestCase):
    def row(self):return dict(grade9_12_lower=72562,including_possible_ungraded_upper=72668,known_strict_teacher_fte_lower=2185,teacher_fte_upper=None)

    def test_unknown_enrollment_upper_erases_positive_lower(self):
        r=self.row();r['including_possible_ungraded_upper']=None
        self.assertEqual(public_utility(r),[0,1])

    def test_observed_counts_provide_only_lower_when_staff_missing(self):
        lower,upper=public_utility(self.row());self.assertAlmostEqual(lower,32775/(72668+32775));self.assertEqual(upper,1)

    def test_joint_extrema_use_opposite_denominators(self):
        r=self.row();r['teacher_fte_upper']=3000
        self.assertEqual(public_utility(r),[32775/(72668+32775),45000/(72562+45000)])

    def test_invalid_bounds_are_rejected(self):
        for key,value in [('including_possible_ungraded_upper',100),('teacher_fte_upper',1),('grade9_12_lower',0),('known_strict_teacher_fte_lower',float('nan'))]:
            r=self.row();r[key]=value
            with self.assertRaises(ValueError):public_utility(r)

if __name__=='__main__':unittest.main()
