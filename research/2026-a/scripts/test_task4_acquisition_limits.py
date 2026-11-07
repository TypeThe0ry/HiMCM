"""Universal-revelation certificates and nondefault preference settings."""
import unittest
import json
import tempfile
from pathlib import Path
from itertools import product
import numpy as np
from task4_acquisition_limits import certificate,checks
from task4_v5_model import score,weights

class AcquisitionTests(unittest.TestCase):
    def test_refuses_other_analysis_before_writes(self):
        from task4_registered_acquisition_limits import protect_analysis
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);p=out/'summary.json';p.write_text(json.dumps({'analysis_kind':'stress'}))
            before=p.read_bytes()
            with self.assertRaisesRegex(ValueError,'different analysis kind'):
                protect_analysis(out,None,None,{})
            self.assertEqual(p.read_bytes(),before)
            self.assertEqual(list(out.iterdir()),[p])

    def test_existing_quantifier_cases(self):
        checks()

    def test_configurable_preferences_against_exhaustion(self):
        rng=np.random.default_rng(7301)
        for alpha in (.06,.13,.19):
            lo=rng.uniform(.15,.4,(3,10));hi=lo+rng.uniform(.1,.5,(3,10))
            mask=np.zeros_like(lo,bool);mask[0,4]=mask[1,7]=mask[2,6]=True
            cert=certificate(lo,hi,mask,alpha,(alpha,alpha))
            every=np.ones(3,bool)
            for bits in product((0,1),repeat=3):
                l,h=lo.copy(),hi.copy()
                for (i,j),bit in zip(zip(*np.where(mask)),bits):l[i,j]=h[i,j]=hi[i,j] if bit else lo[i,j]
                a,b=score(l,weights(alpha)),score(h,weights(alpha))
                every &= np.array([b[i]>=np.delete(a,i).max()-1e-10 for i in range(3)])
            self.assertEqual(every.tolist(),[r['fixed_unavoidable'] for r in cert])
            self.assertEqual(every.tolist(),[r['continuous_unavoidable'] for r in cert])

    def test_preference_range_is_used(self):
        # Opposed main/auxiliary attributes yield different winners at endpoints.
        lo=np.array([[.6]*10,[.5]*10]);lo[0,[6,9]]=0
        low=certificate(lo,lo,np.zeros_like(lo,bool),.05,(.05,.05))
        high=certificate(lo,lo,np.zeros_like(lo,bool),.4,(.4,.4))
        self.assertNotEqual([r['fixed_unavoidable'] for r in low],[r['fixed_unavoidable'] for r in high])
        for r in (low,high):
            self.assertEqual([x['fixed_unavoidable'] for x in r],[x['continuous_unavoidable'] for x in r])
        with self.assertRaises(ValueError):certificate(lo,lo,np.zeros_like(lo,bool),.4,(.05,.2))

if __name__=='__main__':unittest.main()
