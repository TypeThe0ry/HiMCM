"""Extend the task-scoped V129 AI receipt without publishing message text.

The original V129 source prefix and export are immutable. A new receipt extends
that prefix, authenticates every selected visible message independently and
keeps the text export outside both repositories. This is still partial history.
"""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/task4_v140_ai_provenance'
OLD = ROOT / 'data/task4_v129_ai_provenance'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    parser.add_argument('--cutoff-bytes', type=int)
    args = parser.parse_args()
    os.umask(0o077)
    args.private_output.mkdir(parents=True,exist_ok=True)
    os.chmod(args.private_output,0o700)
    old = json.loads((OLD / 'session_manifest.json').read_text())
    protected = [*OLD.glob('*.json'), ROOT / 'scripts/task4_v126_ai_provenance.py',
                 ROOT / 'data/task4_v117_team_intake/city_indicators.csv',
                 ROOT / 'design/task4_user_v136_snapshot.json']
    snapshot = json.loads(protected[-1].read_text())
    protected += [ROOT / p for p in snapshot['source_sha256']]
    protected += [ROOT/'design/task4_user_current_model.json', ROOT/'design/task4_user_v137_extensions.json', ROOT/'scripts/task4_v129_ai_provenance.py']
    protected += [ROOT/p for p in json.loads((ROOT/'results/task4_v137_revision/audit.json').read_text())['result_sha256']]
    paper=ROOT.parents[2]/'HiMCM-Overleaf'
    paper_files=[paper/'main.tex',paper/'ref.bib',paper/'mcmthesis.cls',paper/'drafts/task4_v137_paper.pdf',*[paper/f'drafts/task4_v137_{k}.tex' for k in ['paper','front','core','conclusion','news','ai','references']]]
    manuscript_hashes={str(p.relative_to(paper)):sha(p.read_bytes()) for p in paper_files}
    frozen = {str(p.relative_to(ROOT)): sha(p.read_bytes()) for p in protected}
    with args.session.open('rb') as stream:
        prefix = stream.read(old['source_prefix']['bytes'])
    assert sha(prefix) == old['source_prefix']['sha256']
    assert prefix.endswith(b'\n')
    # An existing receipt replays its exact cutoff rather than silently advancing.
    manifest_path = OUT / 'session_manifest.json'
    cutoff = args.cutoff_bytes
    if cutoff is None:
        cutoff = (json.loads(manifest_path.read_text())['source_prefix']['bytes']
                  if manifest_path.exists() else args.session.stat().st_size)
    assert cutoff >= len(prefix)
    subprocess.run([sys.executable, str(ROOT / 'scripts/task4_v126_ai_provenance.py'),
                    '--session', str(args.session), '--private-output', str(args.private_output),
                    '--cutoff-bytes', str(cutoff), '--output', str(OUT)],
                   check=True, capture_output=True, text=True)
    manifest = json.loads(manifest_path.read_text())
    inventory = manifest['selected_message_inventory']
    assert inventory[:len(old['selected_message_inventory'])] == old['selected_message_inventory']
    private_file = args.private_output / 'visible_records.jsonl'
    os.chmod(args.private_output, 0o700)
    os.chmod(private_file, 0o600)
    exported = private_file.read_bytes().splitlines(keepends=True)
    assert len(exported) == len(inventory)
    index = {r['line']: (r, data) for r, data in zip(inventory, exported)}
    assert len(index) == len(inventory)
    seen, turns = [], []
    event_counts, model_counts, phases = (collections.Counter() for _ in range(3))
    source_hash = hashlib.sha256()
    source_bytes = 0
    # Independently check source identity, exact original text, role and phase.
    with args.session.open('rb') as stream:
        for line_number, raw in enumerate(stream, 1):
            if source_bytes == manifest['source_prefix']['bytes']:
                break
            assert source_bytes + len(raw) <= manifest['source_prefix']['bytes']
            assert raw.endswith(b'\n')
            source_hash.update(raw)
            source_bytes += len(raw)
            event = json.loads(raw)
            event_counts[event['type']] += 1
            p = event.get('payload', {})
            if event['type'] == 'turn_context':
                model_counts[p.get('model')] += 1
                turns.append((line_number, sha(raw), p.get('model')))
            if line_number not in index:
                continue
            receipt, encoded = index[line_number]
            record = json.loads(encoded)
            assert set(record) == {'line', 'timestamp', 'role', 'phase', 'text_parts'}
            assert event['type'] == 'response_item' and p['type'] == 'message'
            assert p.get('recipient') in [None, 'all']
            assert p['role'] in ['user', 'assistant']
            expected_type = 'input_text' if p['role'] == 'user' else 'output_text'
            assert all(part['type'] == expected_type for part in p['content'])
            if p['role'] == 'assistant':
                assert p.get('phase') in ['commentary', 'final_answer']
            assert record == dict(line=line_number, timestamp=event.get('timestamp'),
                                  role=p['role'], phase=p.get('phase'),
                                  text_parts=[part['text'] for part in p['content']])
            assert receipt['source_line_sha256'] == sha(raw)
            assert receipt['exported_record_sha256'] == sha(encoded)
            phases[f"{p['role']}:{p.get('phase')}"] += 1
            seen.append(line_number)
    assert source_bytes == manifest['source_prefix']['bytes']
    assert source_hash.hexdigest() == manifest['source_prefix']['sha256']
    assert dict(event_counts) == manifest['event_type_counts']
    assert dict(model_counts) == manifest['recorded_turn_model_counts']
    assert dict(phases) == manifest['selected_message_counts']
    assert seen == [r['line'] for r in inventory]
    assert turns == [(r['line'], r['source_line_sha256'], r['recorded_model_identifier'])
                     for r in manifest['turn_contexts']]
    assert sha(private_file.read_bytes()) == manifest['private_export']['sha256']
    assert not manifest['complete_team_ai_history']
    for rel, expected in frozen.items():
        assert sha((ROOT / rel).read_bytes()) == expected
    for name,digest in manuscript_hashes.items():assert sha((paper/name).read_bytes())==digest,name
    assert private_file.stat().st_mode & 0o777 == 0o600
    assert args.private_output.stat().st_mode & 0o777 == 0o700
    receipt = dict(status='pass', protected_manuscript_sha256=manuscript_hashes,private_directory_mode='0700',private_file_mode='0600', source_prefix=manifest['source_prefix'],
                   predecessor_prefix=old['source_prefix'],
                   selected_messages=len(inventory),
                   predecessor_selected_messages=len(old['selected_message_inventory']),
                   added_selected_messages=len(inventory)-len(old['selected_message_inventory']),
                   selected_message_counts=dict(phases), recorded_turn_model_counts=dict(model_counts),
                   cli_version=manifest['session_metadata']['cli_version'],
                   manifest_sha256=sha(manifest_path.read_bytes()),
                   extractor_sha256=sha((ROOT / 'scripts/task4_v126_ai_provenance.py').read_bytes()),
                   verifier_sha256=sha(Path(__file__).read_bytes()),
                   verified_original_prefix=True, predecessor_inventory_unchanged=True,
                   source_lines_and_export_text_exact=True, private_export_not_published=True,
                   protected_sha256=frozen, complete_team_ai_history=False,
                   limitation='One root session and selected visible messages only; tool-generated code/prose, tool outputs, attachments, subagent sessions and other team members remain outside this export.')
    target=OUT / ('recheck_verification.json' if (OUT/'verification.json').exists() else 'verification.json')
    target.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: receipt[k] for k in ['status', 'source_prefix', 'selected_messages',
          'added_selected_messages', 'selected_message_counts', 'recorded_turn_model_counts']}, indent=2))


if __name__ == '__main__':
    main()
