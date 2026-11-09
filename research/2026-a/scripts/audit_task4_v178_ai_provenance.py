"""Audit fixed-prefix AI provenance without displaying or publishing private text."""
from pathlib import Path
from collections import Counter
import argparse
from contextlib import redirect_stderr, redirect_stdout
import copy
import hashlib
import importlib.util
import io
import json
import re
import stat
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
O = R / 'data/task4_v178_ai_provenance'
OLD = R / 'data/task4_v140_ai_provenance'
THREAD = '01a1bba3-8ac1-7963-90bf-08d8c2fec116'
OLD_STARTS = ('请接手 ', '怎么认证overleaf', '好了 你继续', '添加一个长期longterm goal')
NEW_STARTS = ('确保所有提交所有东西都上传github/overleaf', '好 继续这些')


def read(path):
    return json.loads(path.read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def encode(record):
    return json.dumps(record, ensure_ascii=False, separators=(',', ':')).encode() + b'\n'


def independent_message(payload, after_old):
    if payload.get('type') != 'message' or payload.get('recipient') not in [None, 'all']:
        return False
    role, parts = payload.get('role'), payload.get('content', [])
    if role not in ['user', 'assistant'] or not parts:
        return False
    expected = 'input_text' if role == 'user' else 'output_text'
    if any(p.get('type') != expected for p in parts):
        return False
    if role == 'assistant':
        return payload.get('phase') in ['commentary', 'final_answer']
    return '\n'.join(p.get('text', '') for p in parts).startswith(
        OLD_STARTS + (NEW_STARTS if after_old else ()))


def independent_call(payload):
    kind = payload.get('type')
    if kind not in ['function_call', 'custom_tool_call']:
        return False
    field = 'arguments' if kind == 'function_call' else 'input'
    name, namespace = payload.get('name'), payload.get('namespace')
    valid_identifier = lambda value: isinstance(value, str) and re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}', value) is not None
    return (isinstance(payload.get(field), str) and valid_identifier(name)
            and (namespace is None or valid_identifier(namespace)))


def synthetic_filters():
    spec = importlib.util.spec_from_file_location('v178_extractor_filter_audit', R / 'scripts/task4_v178_ai_provenance.py')
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    assert extractor.OLD_REQUESTS == OLD_STARTS and extractor.NEW_REQUESTS == NEW_STARTS
    def message(role='assistant', phase='final_answer', text='SYNTHETIC_VISIBLE', **extra):
        return dict(type='message', role=role, phase=phase,
                    content=[dict(type='input_text' if role == 'user' else 'output_text', text=text)], **extra)
    message_cases = [
        (message(), False, True),
        (message(phase='commentary', recipient='all'), False, True),
        (message(role='user', text=OLD_STARTS[0] + 'SYNTHETIC'), False, True),
        (message(role='user', text=NEW_STARTS[0]), False, False),
        (message(role='user', text=NEW_STARTS[0]), True, True),
        (message(role='system'), True, False),
        (message(role='developer'), True, False),
        (message(role='tool'), True, False),
        (message(phase='analysis'), True, False),
        (message(recipient='functions.exec'), True, False),
        (message(role='user', text='<codex_internal_context source="goal">SYNTHETIC</codex_internal_context>'), True, False),
        (message(role='user', text='<environment_context>SYNTHETIC</environment_context>'), True, False),
        (message(role='user', text='# AGENTS.md instructions SYNTHETIC'), True, False),
        (message(role='user', text='# Files pasted by the user: SYNTHETIC'), True, False),
        (dict(type='message', role='assistant', phase='final_answer', content=[dict(type='image', image='SYNTHETIC')]), True, False),
        (dict(type='message', role='assistant', phase='final_answer', content=[]), True, False),
    ]
    for payload, after_old, wanted in message_cases:
        assert extractor.selected_message(payload, after_old) == independent_message(payload, after_old) == wanted
    base = dict(type='function_call', name='functions.exec', arguments='SYNTHETIC_ARGUMENTS')
    custom = dict(type='custom_tool_call', name='functions.exec', input='SYNTHETIC_INPUT')
    call_cases = [
        (base, True), (custom, True),
        ({**base, 'namespace': 'functions'}, True),
        ({**base, 'namespace': 'SYNTHETIC\nNOT_IDENTIFIER'}, False),
        ({**base, 'name': 'SYNTHETIC NOT IDENTIFIER'}, False),
        ({**base, 'arguments': {'SYNTHETIC': True}}, False),
        ({**custom, 'input': None}, False),
        (dict(type='function_call', name='functions.exec', encrypted_content='SYNTHETIC_ENCRYPTED_ONLY'), False),
        (dict(type='custom_tool_call', name='functions.exec', encrypted_content='SYNTHETIC_ENCRYPTED_ONLY'), False),
        ({**base, 'type': 'function_call_output'}, False),
        ({**custom, 'type': 'custom_tool_call_output'}, False),
        (dict(type='reasoning', encrypted_content='SYNTHETIC_ENCRYPTED_ONLY'), False),
        ({**custom, 'encrypted_content': 'SYNTHETIC_ENCRYPTED_EXTRA', 'internal_metadata': {'SYNTHETIC': True}}, True),
    ]
    for payload, wanted in call_cases:
        assert extractor.selected_call(payload) == independent_call(payload) == wanted
    return len(message_cases) + len(call_cases)


def failed_replay_preserves_exports():
    """Exercise the actual entry point with synthetic external fixtures only."""
    spec = importlib.util.spec_from_file_location('v178_failed_replay_audit', R / 'scripts/task4_v178_ai_provenance.py')
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    original_argv = sys.argv[:]
    cases = 0
    with tempfile.TemporaryDirectory(prefix='himcm-v178-replay-audit-', dir='/data/scratch') as directory:
        fixture_root = Path(directory)
        for wrong_thread in [False, True]:
            fixture = fixture_root / ('wrong_thread' if wrong_thread else 'late_bad_prefix')
            public, old, private = (fixture / name for name in ['public', 'old', 'private'])
            for path in [public, old, private]:
                path.mkdir(parents=True, mode=0o700)
            sentinels = {'visible_records.jsonl': b'SYNTHETIC_OLD_VISIBLE\n',
                         'assistant_tool_arguments.jsonl': b'SYNTHETIC_OLD_ARGUMENTS\n'}
            previous = copy.deepcopy(read(O / 'session_manifest.json'))
            for name, content in sentinels.items():
                (private / name).write_bytes(content)
                (private / name).chmod(0o600)
                previous['private_exports'][name].update(bytes=len(content), sha256=digest(content))
            events = [
                dict(type='session_meta', payload=dict(id='SYNTHETIC_WRONG_THREAD' if wrong_thread else THREAD)),
                dict(type='turn_context', payload=dict(model='synthetic-fixture-model')),
                dict(type='response_item', payload=dict(type='message', role='assistant', phase='final_answer',
                                                       content=[dict(type='output_text', text='SYNTHETIC_NEW_VISIBLE')])),
                dict(type='response_item', payload=dict(type='custom_tool_call', name='synthetic.tool', input='SYNTHETIC_NEW_ARGUMENTS')),
                dict(type='event_msg', payload=dict(type='SYNTHETIC_FILLER')),
            ]
            source_bytes = b''.join(encode(event) for event in events)
            source = fixture / 'synthetic_source.jsonl'
            source.write_bytes(source_bytes)
            previous['source_prefix'].update(bytes=len(source_bytes), complete_lines=len(events), sha256=digest(source_bytes))
            (public / 'session_manifest.json').write_text(json.dumps(previous))
            (public / 'protected_files.json').write_bytes((O / 'protected_files.json').read_bytes())
            (old / 'session_manifest.json').write_text(json.dumps(dict(
                source_prefix=dict(bytes=len(source_bytes), complete_lines=len(events), sha256='0' * 64),
                selected_message_inventory=[], private_export=dict(bytes=0, sha256=digest(b'')))))
            public_before = {p.name: p.read_bytes() for p in public.iterdir()}
            extractor.O, extractor.OLD = public, old
            sys.argv = ['synthetic-replay-audit', '--session', str(source), '--private-output', str(private)]
            rejected, stdout, stderr = False, io.StringIO(), io.StringIO()
            try:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    extractor.main()
            except AssertionError:
                rejected = True
            finally:
                sys.argv = original_argv
            assert rejected and not stdout.getvalue() and not stderr.getvalue()
            assert {p.name: p.read_bytes() for p in public.iterdir()} == public_before
            assert {p.name: p.read_bytes() for p in private.iterdir()} == sentinels
            assert stat.S_IMODE(private.stat().st_mode) == 0o700
            assert all(stat.S_IMODE(p.stat().st_mode) == 0o600 for p in private.iterdir())
            cases += 1
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    args = parser.parse_args()
    manifest = read(O / 'session_manifest.json')
    predecessor = read(OLD / 'session_manifest.json')
    protected = read(O / 'protected_files.json')
    assert set(manifest) == {
        'version', 'scope', 'session_metadata', 'source_prefix', 'predecessor_source_prefix',
        'predecessor_125_visible_records_preserved', 'event_type_counts', 'recorded_turn_model_counts',
        'turn_contexts', 'selected_message_counts', 'recorded_call_namespaces_and_names',
        'selected_message_inventory', 'assistant_call_inventory', 'private_exports',
        'private_directory_mode', 'request_filter_policy', 'excluded', 'function_call_interpretation',
        'model_identifier_interpretation', 'private_content_published', 'complete_team_ai_history',
        'submission_ready', 'source_continues_after_frozen_cutoff', 'script_sha256',
    }
    assert manifest['version'] == 'V178'
    assert manifest['script_sha256'] == file_digest(R / 'scripts/task4_v178_ai_provenance.py')
    assert manifest['session_metadata']['id'] == THREAD
    assert manifest['predecessor_source_prefix'] == predecessor['source_prefix']
    assert len(predecessor['selected_message_inventory']) == 125
    assert manifest['selected_message_inventory'][:125] == predecessor['selected_message_inventory']
    for key in ['private_content_published', 'complete_team_ai_history', 'submission_ready']:
        assert manifest[key] is False
    assert manifest['predecessor_125_visible_records_preserved'] is True

    private = args.private_output.resolve()
    assert not args.private_output.is_symlink() and stat.S_IMODE(private.stat().st_mode) == 0o700
    for repo in [R.parents[1], P]:
        assert not private.is_relative_to(repo.resolve()) and not repo.resolve().is_relative_to(private)
    assert set(manifest['private_exports']) == {'visible_records.jsonl', 'assistant_tool_arguments.jsonl'}
    for name, metadata in manifest['private_exports'].items():
        path = private / name
        assert set(metadata) == {'bytes', 'sha256', 'mode', 'included_in_repository'}
        assert not path.is_symlink() and stat.S_ISREG(path.stat().st_mode)
        assert stat.S_IMODE(path.stat().st_mode) == 0o600 and metadata['mode'] == '0o600'
        assert path.stat().st_size == metadata['bytes'] and file_digest(path) == metadata['sha256']
        assert metadata['included_in_repository'] is False
    assert manifest['private_directory_mode'] == '0o700'
    with (private / 'visible_records.jsonl').open('rb') as stream:
        assert digest(stream.read(predecessor['private_export']['bytes'])) == predecessor['private_export']['sha256']

    inventory, calls, contexts = [], [], []
    counts, models, phases, tools, call_types = (Counter() for _ in range(5))
    prefix_hash, predecessor_hash = hashlib.sha256(), hashlib.sha256()
    used = lines = 0
    reached_old = False
    first = last = metadata = None
    cutoff = manifest['source_prefix']['bytes']
    with args.session.open('rb') as source, (private / 'visible_records.jsonl').open('rb') as messages, (private / 'assistant_tool_arguments.jsonl').open('rb') as arguments:
        while used < cutoff:
            raw = source.readline()
            assert raw.endswith(b'\n') and used + len(raw) <= cutoff
            used += len(raw)
            lines += 1
            prefix_hash.update(raw)
            if used <= predecessor['source_prefix']['bytes']:
                predecessor_hash.update(raw)
            if used == predecessor['source_prefix']['bytes']:
                assert predecessor_hash.hexdigest() == predecessor['source_prefix']['sha256']
                reached_old = True
            event = json.loads(raw)
            counts[event['type']] += 1
            timestamp = event.get('timestamp')
            if timestamp:
                first, last = first or timestamp, timestamp
            payload = event.get('payload', {})
            if event['type'] == 'session_meta':
                metadata = {k: payload.get(k) for k in ['id', 'timestamp', 'originator', 'cli_version', 'model_provider', 'source']}
                assert metadata['id'] == THREAD
            if event['type'] == 'turn_context':
                models[payload.get('model')] += 1
                contexts.append(dict(line=lines, timestamp=timestamp, turn_id=payload.get('turn_id'),
                                     recorded_model_identifier=payload.get('model'), source_line_sha256=digest(raw)))
            if event['type'] != 'response_item':
                continue
            if independent_message(payload, used > predecessor['source_prefix']['bytes']):
                parts = [p.get('text', '') for p in payload['content']]
                expected = dict(line=lines, timestamp=timestamp, role=payload['role'], phase=payload.get('phase'), text_parts=parts)
                encoded = messages.readline()
                assert encoded == encode(expected)
                inventory.append(dict(line=lines, timestamp=timestamp, role=expected['role'], phase=expected['phase'],
                                      text_parts_count=len(parts), text_characters=sum(map(len, parts)),
                                      source_line_sha256=digest(raw), exported_record_sha256=digest(encoded)))
                phases[f"{expected['role']}:{expected['phase']}"] += 1
            if independent_call(payload):
                source_field = 'arguments' if payload['type'] == 'function_call' else 'input'
                expected = dict(line=lines, timestamp=timestamp, call_type=payload['type'], source_field=source_field,
                                tool_namespace=payload.get('namespace'), tool_name=payload['name'], arguments=payload[source_field])
                encoded = arguments.readline()
                assert encoded == encode(expected)
                calls.append(dict(line=lines, timestamp=timestamp, call_type=payload['type'], source_field=source_field,
                                  tool_namespace=expected['tool_namespace'], tool_name=expected['tool_name'],
                                  argument_bytes=len(expected['arguments'].encode()), source_line_sha256=digest(raw),
                                  exported_record_sha256=digest(encoded)))
                tool_label = f"{expected['tool_namespace']}.{expected['tool_name']}" if expected['tool_namespace'] else expected['tool_name']
                tools[tool_label] += 1
                call_types[payload['type']] += 1
        assert not messages.read(1) and not arguments.read(1)
    assert reached_old
    assert dict(bytes=used, complete_lines=lines, sha256=prefix_hash.hexdigest(),
                first_timestamp=first, last_timestamp=last) == manifest['source_prefix']
    assert metadata == manifest['session_metadata']
    assert dict(counts) == manifest['event_type_counts']
    assert dict(models) == manifest['recorded_turn_model_counts']
    assert dict(phases) == manifest['selected_message_counts']
    assert dict(tools) == manifest['recorded_call_namespaces_and_names']
    assert inventory == manifest['selected_message_inventory']
    assert calls == manifest['assistant_call_inventory'] and contexts == manifest['turn_contexts']

    snapshot = read(R / 'design/task4_user_v154_snapshot.json')['source_sha256']
    assert protected['science'] == snapshot and len(snapshot) == 187
    assert len(protected['paper']) == 621 and len(protected['old_provenance']) == 3
    for root, mapping in [(R, snapshot), (P, protected['paper']), (R, protected['old_provenance'])]:
        for name, expected in mapping.items():
            assert file_digest(root / name) == expected, name
    registries = {}
    for name, field, version in [('task4_user_current_model.json', 'version', 'V154'),
                                  ('task4_user_current_extensions.json', 'extension_version', 'V154'),
                                  ('task4_user_current_review.json', 'version', 'V176')]:
        path = R / 'design' / name
        relative = 'research/2026-a/design/' + name
        assert read(path)[field] == version
        assert path.read_bytes() == subprocess.check_output(['git', '-C', str(R.parents[1]), 'show', 'HEAD:' + relative])
        registries[relative] = file_digest(path)
    review = read(R / 'design/task4_user_current_review.json')
    assert review == read(P / 'drafts/task4_current_review.json')
    assert file_digest(P / review['pdf']) == review['pdf_sha256']
    tested = synthetic_filters()
    replay_tests = failed_replay_preserves_exports()
    report = dict(version='V178', status='pass', source_prefix=manifest['source_prefix'],
                  predecessor_visible_messages_preserved=125, predecessor_private_visible_prefix_preserved=True,
                  selected_visible_messages=len(inventory), selected_visible_counts=dict(phases),
                  assistant_argument_records=len(calls), assistant_call_type_counts=dict(call_types),
                  turn_contexts_checked=len(contexts), recorded_root_model_counts=dict(models),
                  every_selected_record_and_public_inventory_checked=True, source_selection_independent=True,
                  strict_private_projection='Visible text parts or plaintext function/custom-call arguments; no other source fields',
                  strict_public_projection='Metadata inventories only; no exported message or tool-argument text',
                  synthetic_filter_cases=tested, synthetic_fixtures_not_research_data=True,
                  failed_replay_preservation_cases=replay_tests,
                  failed_replay_preserves_canonical_private_and_public_files=True,
                  failed_replay_temporary_files_cleaned=True,
                  private_directory_mode='0700', private_file_modes='0600',
                  private_exports_outside_both_repositories=True, private_content_printed=False,
                  private_content_published=False, complete_team_ai_history=False,
                  invocation_success_or_nested_tool_execution_certified=False,
                  excluded_scope='Reasoning, internal instructions and encrypted fields; tool outputs, attachments, unselected envelopes, other sessions and teammates',
                  scientific_files_unchanged=187, existing_paper_files_unchanged=621,
                  old_provenance_files_unchanged=3, current_paper='V176 unchanged', primary_science='V154 unchanged',
                  unchanged_registry_sha256=registries, canonical_pdf_sha256=review['pdf_sha256'],
                  manifest_sha256=file_digest(O / 'session_manifest.json'),
                  protected_files_sha256=file_digest(O / 'protected_files.json'),
                  extractor_sha256=manifest['script_sha256'], auditor_sha256=file_digest(Path(__file__)),
                  submission_ready=False)
    (O / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
