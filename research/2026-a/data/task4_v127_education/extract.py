"""Verify V127 nonadmission evidence; never write model inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REGISTRY = 'research/2026-a/design/task4_user_current_model.json'
ACQUISITION_REF = 'db3d42f52c3dde79a43b99b95768d2a7c8233206'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--acquisition-ref', default=ACQUISITION_REF,
                        help='Git revision containing the registry at acquisition; must match the saved receipt')
    args = parser.parse_args()
    protected = json.loads((HERE / 'protected_sha256.json').read_text())
    live_registry = json.loads((ROOT / REGISTRY).read_text())
    live_paths = {ROOT / name for name in protected}
    live_paths.update([HERE / 'protected_sha256.json', HERE / 'audit.json'])
    snapshot_path = ROOT / 'research/2026-a/design/task4_user_v127_snapshot.json'
    if snapshot_path.exists():
        live_paths.add(snapshot_path)
        snapshot = json.loads(snapshot_path.read_text())
        live_paths.update(ROOT / 'research/2026-a' / name for name in snapshot['source_sha256'])
    before = {str(path.relative_to(ROOT)): sha(path) for path in sorted(live_paths)}
    archive = json.loads((HERE / 'archive_sha256.json').read_text())
    assert all(sha(HERE / name) == digest for name, digest in archive.items())
    sources = json.loads((HERE / 'sources.json').read_text())
    assert all(sha(HERE / row['file']) == row['sha256'] for row in sources)
    # The registry is intentionally allowed to advance after this nonadmission.
    # Authenticate its acquisition bytes from Git, never overwrite the live file.
    resolved_ref = subprocess.check_output(
        ['git', 'rev-parse', '--verify', args.acquisition_ref + '^{commit}'], cwd=ROOT
    ).decode().strip()
    acquired_registry = subprocess.check_output(
        ['git', 'show', resolved_ref + ':' + REGISTRY], cwd=ROOT
    )
    assert hashlib.sha256(acquired_registry).hexdigest() == protected[REGISTRY]
    acquisition_registry_version = json.loads(acquired_registry)['version']
    immutable = {name: digest for name, digest in protected.items() if name != REGISTRY}
    assert all(sha(ROOT / name) == digest for name, digest in immutable.items())
    metadata = json.loads((HERE / 'duo_resource_metadata_original.json').read_text())
    assert metadata['success'] is True
    description = metadata['result']['description']
    assert 'niet op vestigingsniveau verzameld' in description
    assert 'uit een of meerdere vestigingen bestaan' in description
    sample = json.loads((HERE / 'duo_amsterdam_one_record_original.json').read_text())
    assert sample['success'] is True
    rows = sample['result']['records']
    assert len(rows) == 1 and rows[0]['JAAR'] == 2006
    assert rows[0]['GEMEENTENAAM'] == 'AMSTERDAM'
    assert rows[0]['SCHOOLTYPE'] == 'havo/vwo'
    assert 'OMVANG_FORMATIE_OP' in rows[0] and 'LEERLING_LERAAR_RATIO' in rows[0]
    pages = subprocess.check_output([
        'pdftotext', '-layout', str(HERE / 'dublin_question_paper_original.pdf'), '-'
    ]).decode().split('\f')
    assert '[33194/24]' in pages[74] and '*825.' in pages[74]
    assert 'Dublin 1, Dublin 3, Dublin 7, Dublin 9 and Dublin 11' in pages[74]
    assert 'To ask the Minister' in pages[74]
    assert json.loads((HERE / 'observations.json').read_text()) == []
    attempts = json.loads((HERE / 'attempts.json').read_text())
    assert sum(row['new_entry'] for row in attempts) == 2
    assert all(not row['admitted'] for row in attempts)
    assert all(sha(ROOT / name) == digest for name, digest in before.items())
    verification = {
        'status': 'pass', 'access_date': '2026-11-09',
        'verification_purpose': 'Reproduce acquisition evidence after authorized registry advancement; original audit.json is historical and unchanged',
        'new_official_avenues_inspected': 2, 'admitted_cells': 0,
        'observations_empty': True, 'Dublin_question_is_not_answer': True,
        'DUO_institution_not_campus_definition_verified': True,
        'DUO_sample_not_used_as_city_estimate': True,
        'archived_hashes_verified': len(archive),
        'acquisition_registry': {
            'path': REGISTRY, 'git_commit': resolved_ref,
            'version': acquisition_registry_version,
            'sha256': hashlib.sha256(acquired_registry).hexdigest(),
            'matches_original_protected_receipt': True,
            'asserted_as_current_live_registry': False,
        },
        'immutable_live_hashes_verified': immutable,
        'current_live_registry': {
            'version': live_registry['version'], 'sha256': before[REGISTRY],
            'allowed_to_differ_from_acquisition': True,
            'unchanged_during_this_run': True,
        },
        'current_run_before_after_hashes_verified': before,
        'original_protected_receipt_and_audit_unchanged': True,
        'model_inputs_written': False,
    }
    (HERE / 'verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    print(json.dumps(verification, indent=2))


if __name__ == '__main__':
    main()
