"""Verify the V129 research/support delivery against the unchanged V127/V128."""
import hashlib
import json
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parents[2]
OVERLEAF = ROOT.parents[1].with_name('HiMCM-Overleaf')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


def main():
    primary = read(ROOT / 'design/task4_user_v127_snapshot.json')
    assert all(sha(ROOT / p) == h for p, h in primary['source_sha256'].items())
    extension = read(ROOT / 'results/task4_v128_revision/audit.json')
    assert extension['status'] == 'pass'
    assert all(sha(ROOT / p) == h for p, h in extension['result_sha256'].items())
    priority = read(ROOT / 'results/task4_v129_priority/audit.json')
    priority_input = read(ROOT / 'results/task4_v129_priority/summary.json')
    assert priority['status'] == 'pass' and priority['candidate_primary_admissions'] == 0
    assert all(sha(ROOT / p) == h for p, h in priority_input['source_sha256'].items())
    assert sha(ROOT / 'design/task4_user_current_model.json') == priority['live_registry_sha256_before']
    source = read(ROOT / 'data/task4_v129_transport/manifest.json')
    assert source['appearances'] == 131 and source['station_complexes'] == 100
    assert all(sha(ROOT / 'data/task4_v129_transport' / p) == h for p, h in source['source_hashes'].items())
    review = read(ROOT / 'results/task4_v129_candidate_review/audit.json')
    assert review['status'] == 'pass' and review['primary_admissions'] == 0
    assert all(sha(ROOT / 'data/task4_v129_transport' / p) == h for p, h in review['candidate_files_sha256'].items())
    education = read(ROOT / 'data/task4_v129_education/verification.json')
    assert education['status'] == 'pass' and education['admitted_cells'] == 0
    assert read(ROOT / 'data/task4_v129_education/observations.json') == []
    ai_dir = ROOT / 'data/task4_v129_ai_provenance'
    ai = read(ai_dir / 'verification.json')
    current = read(ai_dir / 'session_manifest.json')
    old = read(ROOT / 'data/task4_v126_ai_provenance/session_manifest.json')
    assert ai['status'] == 'pass' and sha(ai_dir / 'session_manifest.json') == ai['manifest_sha256']
    assert current['selected_message_inventory'][:52] == old['selected_message_inventory']
    assert len(current['selected_message_inventory']) == 66 and not current['complete_team_ai_history']
    private = Path('/data/scratch/himcm_v129_ai_provenance/visible_records.jsonl')
    assert sha(private) == current['private_export']['sha256']
    assert stat.S_IMODE(private.stat().st_mode) == 0o600
    assert stat.S_IMODE(private.parent.stat().st_mode) == 0o700
    support = OVERLEAF / 'drafts/task4_v129_support'
    delivery = read(support / 'manifest.json')
    assert delivery['status'] == 'pass' and delivery['primary_admissions'] == 0
    assert all(sha(OVERLEAF / p) == h for p, h in delivery['protected_manuscript_sha256'].items())
    assert sha(OVERLEAF / 'drafts/task4_v129_support_README.md') == delivery['support_note_sha256']
    for name, row in delivery['copied_sources'].items():
        assert sha(ROOT / row['research_path']) == row['sha256'] == sha(support / name)
    assert sha(OVERLEAF / 'drafts/task4_v128_paper.pdf') == '20b75e41063e9597a47e43226bd2a95e2a4796aba1db9a46295701111e866081'
    receipt = dict(status='pass', scientific_primary='V127', complete_review='V128',
        actual_primary_admissions=0, primary_shape='112 point /31 partial /17 fully missing',
        primary_snapshot_files_verified=len(primary['source_sha256']),
        V128_result_files_verified=len(extension['result_sha256']),
        priority_protected_files_verified=priority['protected_file_count'],
        priority_independent_evaluations=priority['independent_evaluations'],
        joint_mixed_coordinate_probes=sum(r['mixed_coordinate_probes'] for r in priority['joint_mixed_coordinate_checks']),
        berlin_candidate_station_ids=100, berlin_line_appearances=131,
        education_routes=2, education_admissions=0, ai_selected_messages=66,
        old_AI_inventory_preserved=True, private_export_outside_both_repositories=True,
        manuscript_protected_files_verified=len(delivery['protected_manuscript_sha256']),
        selected_support_copies_verified=len(delivery['copied_sources']),
        V128_PDF_unchanged=True, new_PDF_authored_or_visual_review_claimed=False,
        own_script_sha256=sha(Path(__file__)),
        limitation='Source-qualified Berlin candidate and conditional previews are not activated primary results. Full-team AI history, actual control number and authorized manuscript integration remain incomplete.')
    (Path(__file__).parent / 'verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
