"""Focused inference and application regressions for V108."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import task4_mexico_sampling_revision as model

class SamplingEnvelopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=model.inference()

    def test_complete_fixed_prefix_family_including_unobserved_codes(self):
        for scenario in self.result['scenarios'].values():
            for side in ('lower','upper'):
                candidates=scenario['candidates'][side]['candidates']
                self.assertEqual([r['prefix'] for r in candidates],list(range(9)))
                self.assertEqual(candidates[0]['optional_time_codes'],[])
                self.assertEqual(set(candidates[-1]['optional_time_codes']),{'1','2','3','4','5','6','9','blank'})
                for k,r in enumerate(candidates):
                    self.assertEqual(len(r['optional_time_codes']),k)
                    self.assertGreater(r['B'],0)

    def test_point_outer_familywise_nesting_and_actual_extremizers(self):
        for scenario in self.result['scenarios'].values():
            p,o,f=[scenario[k] for k in ('point','outer','familywise')]
            self.assertTrue(0<=f[0]<=o[0]<=p[0]<=p[1]<=o[1]<=f[1]<=1)
            for label in ('outer','familywise'):
                for ix,(side,sign) in enumerate((('lower',-1),('upper',1))):
                    cs=scenario['candidates'][side]['candidates']
                    values=[r['ratio']+sign*scenario[label+'_critical']*r['taylor_se'] for r in cs]
                    optimum=(min if ix==0 else max)(values)
                    self.assertAlmostEqual(scenario[label][ix],max(0,min(1,optimum)),14)

    def test_design_df_and_zero_target_psus_preserved_in_source(self):
        p=model.ROOT/'data/task4_v108_mexico_design'
        m=json.loads((p/'manifest.json').read_text())
        d=json.loads((p/m['file']).read_text())['diagnostics']
        self.assertEqual(self.result['df'],d['psu_n']-d['strata_n'])
        self.assertEqual(d['singleton_strata_n'],0)
        self.assertEqual(d['psus_zero_target_vector'],586)
        self.assertGreater(d['psu_n'],d['psus_zero_target_vector'])

    def test_application_changes_only_mexico_travel_and_rollback(self):
        shape=(len(model.CITIES),len(model.NAMES))
        lo=np.full(shape,.1);hi=np.full(shape,.9)
        i,j=model.CITIES.index('Mexico City'),model.NAMES.index('travel')
        mask=np.ones(shape,bool);mask[i,j]=False
        with patch.object(model,'mexico_2025_bounds',side_effect=lambda:(lo.copy(),hi.copy())):
            for family in (False,True):
                revised=model.mexico_sampling_bounds(familywise=family)
                label='familywise' if family else 'outer'
                for side,array in enumerate(revised):
                    np.testing.assert_array_equal(array[mask],(lo,hi)[side][mask])
                    self.assertEqual(array[i,j],self.result['scenarios']['boundary3_optional'][label][side])
            restored=model.mexico_sampling_bounds(withdraw=True)
            for original,back in zip((lo,hi),restored):np.testing.assert_array_equal(original,back)
        self.assertEqual(mask.sum(),249)
        np.testing.assert_array_equal(lo,np.full(shape,.1))
        np.testing.assert_array_equal(hi,np.full(shape,.9))

if __name__=='__main__':unittest.main()
