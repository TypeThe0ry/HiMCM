"""Classification edge cases and independent fractional-program bound checks."""
import unittest
import numpy as np
from math import exp
from scipy.optimize import linprog
from extract import additional_scope, derive


def ratio_lp(known, optional, upper=False):
    endpoints = {str(i+1): ((exp(-b/30) if b is not None else 0), exp(-a/30))
                 for i,(a,b) in enumerate(zip([0,15,30,60,120],[15,30,60,120,None]))}
    endpoints.update({'6':(0,1),'9':(0,1),'':(0,1)})
    col=int(upper); n=sum(known.values())
    # Charnes-Cooper: z=1/(N+sum x), y=x*z, 0<=y<=w*z.
    codes=list(optional)
    objective=np.array([sum(w*endpoints[k][col] for k,w in known.items())]+
                       [endpoints[k][col] for k in codes],float)
    constraints=np.zeros((len(codes),len(codes)+1))
    for i,k in enumerate(codes):constraints[i,0]=-optional[k];constraints[i,i+1]=1
    r=linprog(-objective if upper else objective, A_ub=constraints,
              b_ub=np.zeros(len(codes)), A_eq=[[n]+[1]*len(codes)], b_eq=[1],
              bounds=[(0,None)]*(len(codes)+1), method='highs')
    assert r.success,r.message
    return (-r.fun if upper else r.fun)


class MembershipTests(unittest.TestCase):
    def test_classification(self):
        base=dict(ASISTEN='9',NIVACAD='03',ESCOLARI='03',EDAD='15')
        self.assertEqual(additional_scope(base,'age3_17'),'unknown_attendance_known_age')
        self.assertIsNone(additional_scope(dict(base,ASISTEN='3'),'age3_17'))
        self.assertEqual(additional_scope(dict(base,ASISTEN='1',EDAD='999'),'age3_17'),'current_attender_unknown_age')
        self.assertIsNone(additional_scope(dict(base,ASISTEN='1',EDAD='999'),'all_age3plus'))
        self.assertIsNone(additional_scope(dict(base,EDAD='2'),'age3_17'))
        self.assertIsNone(additional_scope(dict(base,NIVACAD='02',ESCOLARI='06'),'age3_17'))

    def test_raw_counts_and_independent_extrema(self):
        summary, records=derive()
        self.assertEqual(len(records),252)
        self.assertEqual(len({r['ID_PERSONA'] for r in records}),252)
        self.assertEqual(summary['attendance_rows']['9'],304)
        self.assertEqual(sum(summary['current_attender_unknown_age_stage_weights'].values()),63)
        for scope,count,weight in [('age3_17',60,1631),('all_age3plus',252,8155)]:
            s=summary['scopes'][scope]
            self.assertEqual(s['added_optional_sample_rows'],count)
            self.assertEqual(s['added_optional_weight'],weight)
            self.assertEqual(s['added_optional_time_bins'],{'':weight})
            self.assertLess(s['utility_lower'],s['before_lower'])
            self.assertGreater(s['utility_upper'],s['before_upper'])
            for upper in (False,True):
                lp=ratio_lp(s['known_time_bins'],s['corrected_optional_time_bins'],upper)
                self.assertAlmostEqual(lp,s['utility_upper' if upper else 'utility_lower'],places=10)

if __name__=='__main__':unittest.main()
