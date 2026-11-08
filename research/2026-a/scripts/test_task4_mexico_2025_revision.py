import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from task4_mexico_2025_revision import source_2025,mexico_2025_bounds
from task4_copenhagen_institution_revision import copenhagen_bounds
from task4_v5_model import CITIES,NAMES

class MexicoRevisionTests(unittest.TestCase):
    def test_public_reproduction_never_reads_local_person_file(self):
        original=Path.read_bytes
        def guarded(path):
            if 'local_only' in path.parts:raise AssertionError('Published model must not require personal raw records')
            return original(path)
        with patch.object(Path,'read_bytes',guarded):
            r=source_2025()
        self.assertLessEqual(r['boundary3_optional'][0],r['legacy_progression'][0])
        self.assertGreaterEqual(r['boundary3_optional'][1],r['legacy_progression'][1])

    def test_single_cell_update_and_exact_withdrawal(self):
        baseline=copenhagen_bounds();current=mexico_2025_bounds();withdrawn=mexico_2025_bounds(True)
        expected=np.zeros_like(baseline[0],bool);expected[CITIES.index('Mexico City'),NAMES.index('travel')]=True
        np.testing.assert_array_equal((baseline[0]!=current[0])|(baseline[1]!=current[1]),expected)
        for a,b in zip(baseline,withdrawn):np.testing.assert_array_equal(a,b)

if __name__=='__main__':unittest.main()
