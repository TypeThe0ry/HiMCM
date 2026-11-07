import itertools
import json
import unittest
import numpy as np
from task4_direct_travel_scale import bins_at_scale,local_recomputation,module
from task4_v5_model import ROOT,CITIES,NAMES
from task4_roster_coverage_comparison import current_bounds

class DirectScaleTests(unittest.TestCase):
    def test_unknown_time_retained(self):
        for tau in [15,20,30,45,60]:
            f=bins_at_scale({'':1,'6':2,'9':3},tau)
            np.testing.assert_array_equal(f.lower,[0,0,0]);np.testing.assert_array_equal(f.upper,[1,1,1])
    def test_real_optional_membership_exhaustive(self):
        m=json.loads((ROOT/'data/task4_v23_mexico_membership/summary.json').read_text())['scopes']['age3_17']
        fn=module('membership_test_v26','data/task4_v20_nyc_travel/extract_commute.py').membership_bounds
        for tau in [15,20,30,45,60]:
            known=bins_at_scale(m['known_time_bins'],tau);optional=bins_at_scale(m['corrected_optional_time_bins'],tau)
            n=known.weight.sum();a=known.weight@known.lower;b=known.weight@known.upper
            bounds=[]
            for bits in itertools.product([0,1],repeat=len(optional)):
                ww=optional.weight.to_numpy()*bits;den=n+ww.sum()
                bounds.append([(a+ww@optional.lower)/den,(b+ww@optional.upper)/den])
            np.testing.assert_allclose(fn(known,optional),[min(v[0] for v in bounds),max(v[1] for v in bounds)],rtol=0,atol=1e-14)
    def test_real_baseline_and_missing_mass(self):
        records=local_recomputation();lo,hi=current_bounds();j=NAMES.index('travel')
        for r in records:
            if r['tau_minutes']==30:
                i=CITIES.index(r['city']);np.testing.assert_allclose([r['utility_lower'],r['utility_upper']],[lo[i,j],hi[i,j]],rtol=0,atol=1e-12)
        melb=[r for r in records if r['city']=='Melbourne']
        widths=[r['point_upper']-r['point_lower'] for r in melb]
        np.testing.assert_allclose(widths,np.repeat(widths[0],5),rtol=0,atol=1e-14)
        self.assertTrue(all(a['point_lower']<b['point_lower'] for a,b in zip(melb,melb[1:])))

if __name__=='__main__':unittest.main()
