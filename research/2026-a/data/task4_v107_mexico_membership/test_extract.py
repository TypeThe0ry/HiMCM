import unittest
from extract import classify

class MembershipTests(unittest.TestCase):
    def row(self,**kw):
        r=dict(EDAD='14',ASISTEN='1',NIVACAD='03',ESCOLARI='03');r.update(kw);return r
    def test_zero_padded_transition_becomes_optional(self):
        self.assertEqual(classify(self.row()),'transition_optional')
        self.assertEqual(classify(self.row(NIVACAD='3',ESCOLARI='3')),'transition_optional')
    def test_started_high_school_retains_conditional_status(self):
        self.assertEqual(classify(self.row(NIVACAD='04',ESCOLARI='01')),'conditional_classified')
    def test_unknown_age_or_attendance_stays_optional(self):
        self.assertEqual(classify(self.row(EDAD='999')),'optional');self.assertEqual(classify(self.row(ASISTEN='9')),'optional')
    def test_known_outside_age_or_nonattendance_excluded(self):
        self.assertIsNone(classify(self.row(EDAD='19')));self.assertIsNone(classify(self.row(ASISTEN='3')))

if __name__=='__main__':unittest.main()
