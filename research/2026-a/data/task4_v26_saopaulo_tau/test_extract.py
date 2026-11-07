import unittest
import json
import numpy as np
from extract import bounds_for_person,paired_resample,TAUS,HERE,SOURCE
from sampling_sensitivity import resample

class DirectScaleTests(unittest.TestCase):
    def test_known_duration_and_missing(self):
        row=dict(MOTIVO_D=4,N_VIAG=1,MOTIVO_O=8,H_SAIDA=7,MIN_SAIDA=0,H_CHEG=7,MIN_CHEG=30,DURACAO=30,DIA_SEM=2)
        values,status,duration=bounds_for_person([row])
        self.assertEqual(duration,30);self.assertEqual(status,'observed_direct_journey')
        np.testing.assert_allclose(values,np.repeat(np.exp(-30/np.array(TAUS)),2))
        for change in [dict(DURACAO=None),dict(MOTIVO_O=3),dict(MOTIVO_D=1)]:
            values,status,duration=bounds_for_person([dict(row,**change)])
            np.testing.assert_array_equal(values,np.tile([0,1],5));self.assertIsNone(duration)
    def test_same_household_draws_as_original(self):
        x=np.repeat(np.exp(-20/np.array(TAUS)),2)
        y=np.repeat(np.exp(-45/np.array(TAUS)),2)
        groups={1:[np.r_[x,1.],np.zeros(11)],2:[np.r_[2*y,2.]]}
        result=paired_resample(groups,draws=100)
        original={z:[r[[4,5,10]] for r in rows] for z,rows in groups.items()}
        np.testing.assert_allclose(result[:,4:6],resample(original,draws=100),atol=1e-14,rtol=0)
    def test_archived_baseline_and_population(self):
        result=json.loads((HERE/'summary.json').read_text());old=json.loads((SOURCE/'sampling_sensitivity.json').read_text())['scopes']['municipality_sao_paulo']
        r=next(r for r in result['scenarios'] if r['tau_minutes']==30)
        np.testing.assert_allclose([r['utility_lower'],r['utility_upper'],r['sampling_lower'],r['sampling_upper']],
            [old['point_lower'],old['point_upper'],old['utility_lower'],old['utility_upper']],atol=1e-12,rtol=0)
        self.assertEqual(result['households'],21917);self.assertEqual(result['households_with_hs'],1648)
        self.assertEqual(result['students'],1778);self.assertEqual(result['status_counts']['observed_direct_journey'],1546)

if __name__=='__main__':unittest.main()
