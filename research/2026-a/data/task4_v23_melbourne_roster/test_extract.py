import unittest
import numpy as np
from extract_roster import weighted_bounds,jackknife_envelope,load

class RosterBoundsTests(unittest.TestCase):
    def test_missing_weighted_mass_is_retained(self):
        np.testing.assert_allclose(weighted_bounds([.2,0],[.2,1],[1,3]),[.05,.8])
        np.testing.assert_allclose(weighted_bounds([0,0],[1,1],[2,7]),[0,1])
        np.testing.assert_allclose(weighted_bounds([.2,.6],[.2,.6],[1,3]),[.5,.5])
    def test_weekday_scaling_cancels(self):
        l=[.2,0,.7];u=[.2,1,.7];w=np.array([1.,4.,2.]);rep=np.tile(w[:,None],(1,10))*np.arange(1,11)[None,:]
        a=jackknife_envelope(l,u,w,rep);b=jackknife_envelope(l,u,w*7/5,rep*7/5)
        np.testing.assert_allclose([a['lower'],a['upper']],[b['lower'],b['upper']],atol=1e-14)
        np.testing.assert_allclose(a['endpoint_standard_errors'],0,atol=1e-14)
    def test_provider_variance_factor(self):
        l=[.1,0];u=[.1,1];w=[1,1];rep=np.array([[1+i/10 for i in range(10)],[1]*10])
        r=jackknife_envelope(l,u,w,rep);estimate=weighted_bounds(l,u,w)
        manual=np.sqrt(.9*np.sum((np.array([weighted_bounds(l,u,rep[:,i]) for i in range(10)])-estimate)**2,axis=0))
        np.testing.assert_allclose(r['endpoint_standard_errors'],manual)
    def test_real_roster_preserves_missing(self):
        roster,journeys,_=load();teen=roster[roster.agegroup=='15->19']
        self.assertEqual(len(roster),322);self.assertEqual(len(teen),171)
        self.assertEqual(int(teen.has_person_weight.sum()),170)
        self.assertEqual(int(teen.has_observed_journey.sum()),107)
        self.assertEqual(int((~teen.has_observed_journey).sum()),64)
        self.assertEqual(len(journeys[journeys.persid.isin(teen.persid)]),108)
        first=journeys.sort_values('start_time').drop_duplicates('persid').set_index('persid')
        actual=roster[roster.has_observed_journey].set_index('persid')
        np.testing.assert_array_equal(actual.jteid,first.loc[actual.index,'jteid'])
        self.assertTrue(actual.transport_only.all())
        self.assertEqual(roster[roster.homelga=='Melbourne (C)'].hhid.nunique(),1)
    def test_nan_weight_is_not_silently_dropped(self):
        with self.assertRaises(ValueError):weighted_bounds([.2,0],[.2,1],[1,np.nan])

if __name__=='__main__':unittest.main()
