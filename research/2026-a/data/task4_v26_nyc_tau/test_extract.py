import json
import unittest
import numpy as np
import pandas as pd
from extract_tau import HERE,V21,rescale

class DiaryScaleTests(unittest.TestCase):
    def test_missing_and_membership_preserved(self):
        raw=pd.read_csv(V21/'student_journey_audit.csv')
        keep=[x for x in raw.columns if x not in ['lower','upper']]
        for tau in [15,20,30,45,60]:
            actual=rescale(raw,tau)
            pd.testing.assert_frame_equal(raw[keep],actual[keep])
            missing=raw.duration_minutes.isna()
            np.testing.assert_array_equal(actual.loc[missing,['lower','upper']],raw.loc[missing,['lower','upper']])
            self.assertEqual(int((~missing).sum()),410)
        baseline=rescale(raw,30)
        np.testing.assert_allclose(baseline[['lower','upper']],raw[['lower','upper']],rtol=0,atol=1e-14)
    def test_time_scale_and_invalid(self):
        row=pd.DataFrame(dict(duration_minutes=[30.,np.nan],lower=[np.exp(-1),0],upper=[np.exp(-1),1]))
        self.assertAlmostEqual(rescale(row,15).lower.iloc[0],np.exp(-2))
        self.assertAlmostEqual(rescale(row,60).upper.iloc[0],np.exp(-.5))
        for tau in [0,-1,float('inf'),float('nan')]:
            with self.assertRaises(ValueError):rescale(row,tau)
    def test_saved_baseline_and_monotonicity(self):
        result=json.loads((HERE/'summary.json').read_text())
        old=json.loads((V21/'summary.json').read_text())['scopes']
        self.assertEqual(len(result['scenarios']),10)
        self.assertEqual(result['households_resampled'],5766)
        self.assertEqual(result['missing_journeys'],193)
        for scope,n,o in [('all_age',476,127),('under19',460,33)]:
            rows=[r for r in result['scenarios'] if r['age_scope']==scope]
            for r in rows:
                self.assertEqual((r['known_students'],r['optional_students']),(n,o))
                self.assertLessEqual(r['sampling_lower'],r['utility_lower'])
                self.assertGreaterEqual(r['sampling_upper'],r['utility_upper'])
            for key in ['utility_lower','utility_upper','sampling_lower','sampling_upper']:
                self.assertTrue(np.all(np.diff([r[key] for r in rows])>=-1e-12))
                old_key=key.replace('utility','membership')
                self.assertAlmostEqual(next(r for r in rows if r['tau_minutes']==30)[key],old[scope][old_key],places=12)

if __name__=='__main__':unittest.main()
