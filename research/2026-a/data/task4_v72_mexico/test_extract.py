"""Age boundary cases and independent linear-fractional endpoint verification."""
import unittest
from math import exp
import numpy as np
from scipy.optimize import linprog
from extract import classify, derive

def lp_bound(known, optional, upper):
    ends={str(i+1):((exp(-b/30) if b is not None else 0),exp(-a/30))
          for i,(a,b) in enumerate(zip([0,15,30,60,120],[15,30,60,120,None]))}
    ends.update({'6':(0,1),'9':(0,1),'':(0,1)})
    keys=list(optional); col=int(upper)
    c=np.array([sum(w*ends[k][col] for k,w in known.items())]+[ends[k][col] for k in keys])
    a=np.zeros((len(keys),len(keys)+1))
    for i,k in enumerate(keys):a[i,0]=-optional[k];a[i,i+1]=1
    r=linprog(-c if upper else c,A_ub=a,b_ub=np.zeros(len(keys)),
              A_eq=[[sum(known.values())]+[1]*len(keys)],b_eq=[1],bounds=(0,None),method='highs')
    assert r.success,r.message
    return -r.fun if upper else r.fun

class AgeTests(unittest.TestCase):
    def test_boundary_and_unknowns(self):
        row=dict(EDAD='14',ASISTEN='1',NIVACAD='03',ESCOLARI='03')
        for age in ['14','18']:self.assertEqual(classify(dict(row,EDAD=age)),'conditional_classified')
        for age in ['13','19','3']:self.assertIsNone(classify(dict(row,EDAD=age)))
        self.assertEqual(classify(dict(row,EDAD='999')),'optional')
        self.assertEqual(classify(dict(row,ASISTEN='9')),'optional')
        self.assertEqual(classify(dict(row,ESCOLARI='99')),'optional')
        self.assertIsNone(classify(dict(row,ASISTEN='3')))
        self.assertIsNone(classify(dict(row,NIVACAD='02',ESCOLARI='06')))
    def test_raw_population_and_endpoints(self):
        result=derive(); old=result['scopes']['age3_17'];new=result['scopes']['age14_18']
        self.assertEqual(new['n_known'],9217);self.assertEqual(new['n_optional'],86)
        self.assertEqual(new['known_weight']-old['known_weight'],51677)
        self.assertEqual(new['ages_known']['18'],51677)
        self.assertEqual(new['ages_optional']['999'],old['ages_optional']['999'])
        self.assertEqual(set(new['ages_known']),{'14','15','16','17','18'})
        self.assertEqual(set(new['ages_optional']),{'14','15','16','17','18','999'})
        for g in (old,new):
            for upper in (False,True):
                self.assertAlmostEqual(lp_bound(g['known'],g['optional'],upper),g['utility_upper' if upper else 'utility_lower'],places=10)
        # A changed target age population need not give a nested interval.
        self.assertLess(new['utility_lower'],old['utility_lower'])
        self.assertLess(new['utility_upper'],old['utility_upper'])
if __name__=='__main__':unittest.main()
