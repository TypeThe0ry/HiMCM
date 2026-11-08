import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from task4_registered_continuous_acquisition import run

class RegisteredAcquisitionTests(unittest.TestCase):
    def inputs(self):
        return np.zeros((25,10)),np.ones((25,10)),dict(model_version='V96',fixed_alpha=.1,alpha_range=[.05,.2])

    def test_old_output_rejected_before_search_or_write(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder);(out/'summary.json').write_text(json.dumps({'model_version':'V91'}))
            (out/'sentinel.csv').write_text('historical evidence')
            before={p.name:p.read_bytes() for p in out.iterdir()}
            with patch('task4_registered_continuous_acquisition.current_bounds',return_value=self.inputs()),patch('task4_registered_continuous_acquisition.search') as search:
                with self.assertRaisesRegex(ValueError,'different model baseline'):run(out)
                search.assert_not_called()
            self.assertEqual(before,{p.name:p.read_bytes() for p in out.iterdir()})

    def test_mislabeled_prior_rejected_without_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);prior=root/'prior';prior.mkdir();out=root/'new'
            (prior/'summary.json').write_text(json.dumps({'model_version':'V91'}))
            with patch('task4_registered_continuous_acquisition.current_bounds',return_value=self.inputs()),patch('task4_registered_continuous_acquisition.search') as search:
                with self.assertRaisesRegex(ValueError,'Prior model label'):run(out,prior,'V79')
                search.assert_not_called()
            self.assertFalse(out.exists())

if __name__=='__main__':unittest.main()
