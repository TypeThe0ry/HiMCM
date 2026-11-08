"""Freeze reviewed V121 candidate observations and local evidence hashes."""
from pathlib import Path
import hashlib
import json

from task4_user_city_indicators import SOURCE
from task4_v5_model import ROOT


def main():
    directories = ['task4_v121_education', 'task4_v121_transport', 'task4_v121_pools']
    expected = {
        ('Stockholm', 'upper_secondary_ptr'), ('Stockholm', 'public_transport_density'),
        ('Stockholm', 'public_pool_density'), ('Paris', 'public_transport_density'),
        ('Dublin', 'public_transport_density')}
    observations, sources = [], []
    for directory in directories:
        path = ROOT / 'data' / directory
        for candidate in json.loads((path / 'observations.json').read_text()):
            row = dict(candidate)
            row.pop('candidate_only', None)
            row['admissible'] = 'conditional_school_resource_fte' if row.get('kind') == 'ratio_interval' else 'conditional_inventory_lower_bound'
            row['candidate_file'] = str((path / 'observations.json').relative_to(ROOT))
            observations.append(row)
        # Preserve original and derived evidence, extraction and provenance.
        # README copy changes do not change scientific inputs.
        sources.extend(p for p in path.iterdir() if p.is_file() and p.suffix != '.md')
    assert {(r['city'], r['indicator']) for r in observations} == expected
    assert len(observations) == len(expected)
    sources.extend(ROOT / p for p in [
        'design/task4_user_v118_admissions.json', 'design/task4_user_v120_admissions.json',
        'scripts/task4_user_v120_revision.py', 'scripts/task4_user_v118_revision.py',
        'scripts/task4_user_city_indicators.py', 'scripts/task4_v5_model.py',
        'scripts/task4_interval_decision.py', 'scripts/task4_ahp_mc_baseline.py',
        'scripts/task4_user_v121_revision.py', 'scripts/task4_v121_admissions.py'])
    manifest = dict(
        version='V121', baseline='V120 user16', access_date='2026-11-08',
        input_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        source_policy='Submitted measurements and all V120 nonmissing bounds retained exactly; '
                      'only five V120 fully missing cells supplemented. No new weight, anchor, '
                      'travel imputation or finite inventory upper bound.',
        scope='Mixed-vintage school-resource and facility inventories, not identified '
              'ages14-18 resident outcomes or a common-year city census. Paris inventory '
              'uses RATP2021/Apur2022; Dublin uses existing stock in the2023 plan issued2024.',
        observations=observations,
        source_hashes={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in sorted(set(sources))})
    assert manifest['input_sha256'] == '430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    out = ROOT / 'design/task4_user_v121_admissions.json'
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(observations)} reviewed cells; {len(sources)} evidence/code hashes; {out}')


if __name__ == '__main__':
    main()
