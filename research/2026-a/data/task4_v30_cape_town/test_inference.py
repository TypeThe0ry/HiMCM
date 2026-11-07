import unittest
import numpy as np
import pandas as pd
from inference import endpoint_envelope


class InferenceTests(unittest.TestCase):
    def setUp(self):
        self.frame=pd.DataFrame({'stratum':[1,1,2,2],'psu':[11,12,21,22],'person_wgt':[1.,1.,1.,1.]})
        self.domain=np.array([True,False,True,False])
        self.u=np.array([0.,np.nan,1.,np.nan])

    def test_zero_domain_psus_enter_variance(self):
        result=endpoint_envelope(self.frame,self.domain,self.u,self.u)
        np.testing.assert_allclose(result['point_bounds'],[.5,.5])
        np.testing.assert_allclose(result['endpoint_standard_errors'],[np.sqrt(.125)]*2)
        self.assertEqual(result['psus_all_relevant_strata'],4)
        self.assertEqual(result['degrees_of_freedom'],2)

    def test_weight_scale_invariance(self):
        a=endpoint_envelope(self.frame,self.domain,self.u,self.u)
        frame=self.frame.copy();frame.person_wgt*=97
        b=endpoint_envelope(frame,self.domain,self.u,self.u)
        np.testing.assert_allclose(a['joint_95_percent_approximate_envelope'],b['joint_95_percent_approximate_envelope'])
        np.testing.assert_allclose(a['endpoint_standard_errors'],b['endpoint_standard_errors'])

    def test_singleton_not_silently_accepted(self):
        with self.assertRaisesRegex(ValueError,'Singleton'):
            endpoint_envelope(self.frame.iloc[[0,2]],np.ones(2,dtype=bool),[0,1],[0,1])

    def test_invalid_bounds_and_weights_rejected(self):
        with self.assertRaises(ValueError):endpoint_envelope(self.frame,self.domain,self.u,[1,0,.9,0])
        frame=self.frame.copy();frame.loc[0,'person_wgt']=0
        with self.assertRaises(ValueError):endpoint_envelope(frame,self.domain,self.u,self.u)

if __name__=='__main__':unittest.main()
