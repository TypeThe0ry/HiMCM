"""Prevent historical or new unregistered sources silently becoming current evidence."""
import json
from pathlib import Path
import tempfile
import unittest
from task4_travel_evidence_index import build_index


class TravelEvidenceIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'source.json').write_text(json.dumps({'bounds': [.2, .6]}))
        self.source = dict(path='source.json', keys=[], endpoints='bounds', year='2020',
            age_stage='fixture', geography='fixture', observation='fixture',
            conditions='fixture', original_source='source.json')
        self.options = dict(cities=['Known', 'Unknown'], sources={'Known': self.source},
                            withdrawn={}, root=self.root)

    def test_new_informative_city_requires_registration(self):
        with self.assertRaisesRegex(ValueError, 'evidence registration'):
            build_index([.2, .1], [.6, 1], **self.options)

    def test_source_bound_mismatch_rejected(self):
        (self.root / 'source.json').write_text(json.dumps({'bounds': [.3, .6]}))
        with self.assertRaisesRegex(ValueError, 'bound mismatch'):
            build_index([.2, 0], [.6, 1], **self.options)

    def test_valid_source_and_unknown_retained(self):
        result = build_index([.2, 0], [.6, 1], **self.options)
        self.assertEqual(result.status.tolist(), ['informative_conditional', 'unknown'])
        self.assertEqual(result.bound_verified.tolist(), [True, False])
        self.assertFalse(result.main_admitted.any())

    def test_stale_informative_registration_rejected(self):
        with self.assertRaisesRegex(ValueError, 'evidence registration'):
            build_index([0, 0], [1, 1], **self.options)


if __name__ == '__main__':
    unittest.main()
