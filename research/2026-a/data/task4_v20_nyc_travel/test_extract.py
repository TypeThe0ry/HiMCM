import itertools,unittest,json
import numpy as np
import pandas as pd
from extract_commute import membership_bounds,HERE,load_people

class TravelBounds(unittest.TestCase):
    def test_membership_against_all_subsets(self):
        rng=np.random.default_rng(20261107)
        for _ in range(80):
            n=int(rng.integers(0,8));weights=rng.uniform(.1,3,3+n);lo=rng.random(3+n);hi=lo+(1-lo)*rng.random(3+n)
            frame=pd.DataFrame(dict(weight=weights,lower=lo,upper=hi));known=frame.iloc[:3];optional=frame.iloc[3:]
            got=membership_bounds(known,optional);bounds=[]
            for mask in itertools.product([0,1],repeat=n):
                w=np.r_[weights[:3],weights[3:]*mask];bounds.append([np.dot(w,lo)/w.sum(),np.dot(w,hi)/w.sum()])
            np.testing.assert_allclose(got,[min(x[0] for x in bounds),max(x[1] for x in bounds)],rtol=0,atol=1e-12)

    def test_raw_population_and_unknown_journeys(self):
        people,hh,audit=load_people();known=people[people.membership=='known'];optional=people[people.membership=='optional']
        self.assertEqual((len(known),len(optional),len(hh)),(476,127,5766))
        self.assertEqual((known.reason=='observed_direct_home_to_school').sum(),365)
        missing=known[known.reason!='observed_direct_home_to_school'];self.assertTrue((missing.lower==0).all() and (missing.upper==1).all())
        measured=known[known.reason=='observed_direct_home_to_school'];np.testing.assert_allclose(measured.lower,np.exp(-measured.duration_minutes/30));np.testing.assert_array_equal(measured.lower,measured.upper)
        summary=json.loads((HERE/'commute_summary.json').read_text());l,h=membership_bounds(known,optional)
        self.assertLessEqual(summary['sampling_envelope_lower'],l);self.assertGreaterEqual(summary['sampling_envelope_upper'],h)
        self.assertEqual(audit['invalid_short_trip_key_duplicates'],34072)

if __name__=='__main__':unittest.main()
