"""Guard against wrong-scenario selection and silent changes in current scores."""
import unittest
import numpy as np
import pandas as pd
from task4_current_model import current_bounds,verify_baseline,verify_bounds
from task4_v5_model import weights,summarize,CITIES,NAMES


class CurrentModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lo,hi,config=current_bounds();cls.frame,_=summarize(lo,hi,weights(config['fixed_alpha']))

    def test_wrong_scenario_or_city_order_rejected(self):
        with self.assertRaises(ValueError):verify_baseline(self.frame,self.frame.iloc[:0])
        with self.assertRaises(ValueError):verify_baseline(self.frame,self.frame.iloc[::-1])

    def test_score_or_champion_change_rejected(self):
        for col in ['score_lower','max_regret','possible_champion']:
            changed=self.frame.copy()
            if col=='possible_champion':changed.loc[0,col]=not changed.loc[0,col]
            else:changed.loc[0,col]+=0.01
            with self.assertRaises(AssertionError):verify_baseline(self.frame,changed)

    def test_indicator_swap_detected_even_when_scores_match(self):
        lo=np.zeros((len(CITIES),len(NAMES)));hi=np.ones_like(lo)
        lo[0,0]=.2;lo[0,1]=.7
        baseline=pd.DataFrame([dict(city=c,indicator=n,lower=lo[i,j],upper=hi[i,j]) for i,c in enumerate(CITIES) for j,n in enumerate(NAMES)])
        swapped=lo.copy();swapped[0,[0,1]]=lo[0,[1,0]]
        before,_=summarize(lo,hi,weights());after,_=summarize(swapped,hi,weights())
        np.testing.assert_allclose(before.score_lower,after.score_lower)
        with self.assertRaises(AssertionError):verify_bounds(swapped,hi,baseline)

    def test_valid_snapshot_accepted(self):
        verify_baseline(self.frame,self.frame.copy())

if __name__=='__main__':unittest.main()
