"""Extend actual root-session evidence; keep text and tool arguments private.

Exports selected visible messages and plaintext assistant tool-call arguments.
Never exports reasoning, encrypted fields, tool results or system/developer messages.
The source scope is one explicitly identified root log, not complete team use.
"""
from pathlib import Path
from collections import Counter
from contextlib import contextmanager
import argparse
import hashlib
import json
import os
import re
import subprocess

R = Path(__file__).resolve().parents[1]
P = R.parents[2] / 'HiMCM-Overleaf'
O = R / 'data/task4_v178_ai_provenance'
OLD = R / 'data/task4_v140_ai_provenance'
THREAD = '01a1bba3-8ac1-7963-90bf-08d8c2fec116'
OLD_REQUESTS = ('请接手 ', '怎么认证overleaf', '好了 你继续', '添加一个长期longterm goal')
NEW_REQUESTS = ('确保所有提交所有东西都上传github/overleaf', '好 继续这些')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def encoded(record):
    return json.dumps(record, ensure_ascii=False, separators=(',', ':')).encode() + b'\n'


def selected_message(payload, after_old_prefix):
    if payload.get('type') != 'message':
        return False
    if payload.get('recipient') not in {None, 'all'}:
        return False
    role = payload.get('role')
    parts = payload.get('content', [])
    allowed = 'input_text' if role == 'user' else 'output_text'
    if role not in {'user', 'assistant'} or not parts or any(p.get('type') != allowed for p in parts):
        return False
    if role == 'assistant':
        return payload.get('phase') in {'commentary', 'final_answer'}
    joined = '\n'.join(p.get('text', '') for p in parts)
    return joined.startswith(OLD_REQUESTS + (NEW_REQUESTS if after_old_prefix else ()))


def selected_call(payload):
    field = {'function_call': 'arguments', 'custom_tool_call': 'input'}.get(payload.get('type'))
    namespace = payload.get('namespace')
    return (field is not None
            and isinstance(payload.get(field), str)
            and isinstance(payload.get('name'), str)
            and re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}', payload['name']) is not None
            and (namespace is None or (isinstance(namespace, str) and re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}', namespace) is not None)))


@contextmanager
def private_file(path):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW, 0o600)
    os.chmod(path, 0o600)
    stream = os.fdopen(descriptor, 'wb')
    try:
        yield stream
    except BaseException:
        stream.close()
        path.unlink(missing_ok=True)
        raise
    finally:
        stream.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    args = parser.parse_args()
    raw_private = args.private_output.expanduser()
    assert not raw_private.is_symlink(), 'Private output itself cannot be a symlink'
    private = raw_private.resolve()
    for repo in [R.parents[1], P]:
        assert not private.is_relative_to(repo) and not repo.is_relative_to(private), 'Choose private output outside both repositories and not their ancestor'
    if private.exists():
        assert private.is_dir() and set(x.name for x in private.iterdir()) <= {'visible_records.jsonl', 'assistant_tool_arguments.jsonl', '.visible_records.jsonl.tmp', '.assistant_tool_arguments.jsonl.tmp'}, 'Private output must be new or contain only this capture files'
    private.mkdir(parents=True, mode=0o700, exist_ok=True)
    os.chmod(private, 0o700)
    old = read(OLD / 'session_manifest.json')
    manifest_path = O / 'session_manifest.json'
    previous = read(manifest_path) if manifest_path.exists() else None
    for name in ['visible_records.jsonl', 'assistant_tool_arguments.jsonl']:
        if (private/name).exists():
            assert previous is not None and sha((private/name).read_bytes()) == previous['private_exports'][name]['sha256'], 'Do not overwrite a different private capture'
    cutoff = previous['source_prefix']['bytes'] if previous else args.session.stat().st_size
    assert cutoff >= old['source_prefix']['bytes']
    O.mkdir(exist_ok=True)
    protection_path = O / 'protected_files.json'
    if protection_path.exists():
        protected = read(protection_path)
    else:
        names = subprocess.check_output(['git', '-C', str(P), 'ls-files', '-z']).decode().split('\0')[:-1]
        protected = dict(science=read(R / 'design/task4_user_v154_snapshot.json')['source_sha256'],
                         paper={n: sha((P/n).read_bytes()) for n in names},
                         old_provenance={str(p.relative_to(R)): sha(p.read_bytes()) for p in OLD.glob('*.json')})
    for root, mapping in [(R, protected['science']), (P, protected['paper']), (R, protected['old_provenance'])]:
        for name, expected in mapping.items():
            assert sha((root/name).read_bytes()) == expected, name
    total_hash, old_hash = hashlib.sha256(), hashlib.sha256()
    used, line_number, first, last, metadata = 0, 0, None, None, None
    events, models, phases, tools = (Counter() for _ in range(4))
    messages, calls, contexts = [], [], []
    message_temp, argument_temp = private/'.visible_records.jsonl.tmp', private/'.assistant_tool_arguments.jsonl.tmp'
    with args.session.open('rb') as source, private_file(message_temp) as visible, private_file(argument_temp) as arguments:
        for raw in source:
            if used + len(raw) > cutoff or not raw.endswith(b'\n'):
                break
            used += len(raw)
            line_number += 1
            total_hash.update(raw)
            if used <= old['source_prefix']['bytes']:
                old_hash.update(raw)
            if used == old['source_prefix']['bytes']:
                assert old_hash.hexdigest() == old['source_prefix']['sha256']
            event = json.loads(raw)
            events[event['type']] += 1
            timestamp = event.get('timestamp')
            if timestamp:
                first, last = first or timestamp, timestamp
            payload = event.get('payload', {})
            if event['type'] == 'session_meta':
                assert payload['id'] == THREAD
                metadata = {k: payload.get(k) for k in ['id', 'timestamp', 'originator', 'cli_version', 'model_provider', 'source']}
            if event['type'] == 'turn_context':
                model = payload.get('model')
                models[model] += 1
                contexts.append(dict(line=line_number, timestamp=timestamp, turn_id=payload.get('turn_id'), recorded_model_identifier=model, source_line_sha256=sha(raw)))
            if event['type'] != 'response_item':
                continue
            if selected_message(payload, used > old['source_prefix']['bytes']):
                parts = [p.get('text', '') for p in payload['content']]
                entry = dict(line=line_number, timestamp=timestamp, role=payload['role'], phase=payload.get('phase'), text_parts=parts)
                data = encoded(entry)
                visible.write(data)
                messages.append(dict(line=line_number, timestamp=timestamp, role=entry['role'], phase=entry['phase'], text_parts_count=len(parts), text_characters=sum(map(len, parts)), source_line_sha256=sha(raw), exported_record_sha256=sha(data)))
                phases[f"{entry['role']}:{entry['phase']}"] += 1
            if selected_call(payload):
                field = 'arguments' if payload['type'] == 'function_call' else 'input'
                entry = dict(line=line_number, timestamp=timestamp, call_type=payload['type'], source_field=field, tool_namespace=payload.get('namespace'), tool_name=payload['name'], arguments=payload[field])
                data = encoded(entry)
                arguments.write(data)
                calls.append(dict(line=line_number, timestamp=timestamp, call_type=entry['call_type'], source_field=field, tool_namespace=entry['tool_namespace'], tool_name=entry['tool_name'], argument_bytes=len(entry['arguments'].encode()), source_line_sha256=sha(raw), exported_record_sha256=sha(data)))
                tools[(entry['tool_namespace']+'.' if entry['tool_namespace'] else '')+entry['tool_name']] += 1
        assert metadata and metadata['id'] == THREAD and contexts and calls
        assert old_hash.hexdigest() == old['source_prefix']['sha256']
        if previous:
            assert used == cutoff and total_hash.hexdigest() == previous['source_prefix']['sha256'], 'Frozen source prefix changed'
        assert messages[:len(old['selected_message_inventory'])] == old['selected_message_inventory']
        visible.flush()
        arguments.flush()
        with message_temp.open('rb') as stream:
            assert sha(stream.read(old['private_export']['bytes'])) == old['private_export']['sha256']
    os.replace(message_temp, private/'visible_records.jsonl')
    os.replace(argument_temp, private/'assistant_tool_arguments.jsonl')
    exports = {p.name: dict(bytes=p.stat().st_size, sha256=sha(p.read_bytes()), mode=oct(p.stat().st_mode & 0o777), included_in_repository=False) for p in [private/'visible_records.jsonl', private/'assistant_tool_arguments.jsonl']}
    manifest = dict(version='V178', scope='One explicitly identified root session;selected visible messages and plaintext assistant function/custom-tool call arguments only', session_metadata=metadata,
                    source_prefix=dict(bytes=used, complete_lines=line_number, sha256=total_hash.hexdigest(), first_timestamp=first, last_timestamp=last),
                    predecessor_source_prefix=old['source_prefix'], predecessor_125_visible_records_preserved=True,
                    event_type_counts=dict(events), recorded_turn_model_counts=dict(models), turn_contexts=contexts,
                    selected_message_counts=dict(phases), recorded_call_namespaces_and_names=dict(tools),
                    selected_message_inventory=messages, assistant_call_inventory=calls, private_exports=exports,
                    private_directory_mode=oct(private.stat().st_mode & 0o777),
                    request_filter_policy='Four frozen V140 prefixes;two explicitly selected later requests;reply and attachment envelopes excluded',
                    excluded=['reasoning/analysis','system/developer messages','encrypted_content and internal metadata','tool results','injected goal/environment/AGENTS messages','attachment contents','unselected user reply envelopes','subagent response sessions','other team members and earlier chats'],
                    function_call_interpretation='Exact recorded assistant plaintext arguments for function_call and input for custom_tool_call;not proof that each invocation succeeded or that every nested tool ran. Includes tool-contained drafts/code where present.',
                    model_identifier_interpretation='Recorded root turn-context labels;not immutable serving builds or all concurrent assistants',
                    private_content_published=False, complete_team_ai_history=False, submission_ready=False,
                    source_continues_after_frozen_cutoff=True, script_sha256=sha(Path(__file__).read_bytes()))
    (O/'session_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    protection_path.write_text(json.dumps(protected, indent=2)+'\n')
    for root, mapping in [(R, protected['science']), (P, protected['paper']), (R, protected['old_provenance'])]:
        for name, expected in mapping.items():
            assert sha((root/name).read_bytes()) == expected, name
    print(json.dumps(dict(source_prefix=manifest['source_prefix'], models=dict(models), messages=dict(phases), assistant_argument_records=len(calls), private_export_bytes={k:v['bytes'] for k,v in exports.items()}, complete_team_ai_history=False), indent=2))


if __name__ == '__main__':
    main()
