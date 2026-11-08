"""Inventory this task's recorded AI metadata; keep visible-message exports private.

Reads an explicit local session only. Never exports reasoning, tool payloads,
system/developer instructions, injected goal continuations or environment text.
The public-safe manifest authenticates a complete-line prefix of the live log.
It is evidence of recorded labels and selected messages, not full-team coverage.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THREAD = '01a1bba3-8ac1-7963-90bf-08d8c2fec116'
REQUEST_STARTS = ('请接手 ', '怎么认证overleaf', '好了 你继续', '添加一个长期longterm goal')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--session', type=Path, required=True)
    parser.add_argument('--private-output', type=Path, required=True)
    parser.add_argument('--cutoff-bytes', type=int)
    parser.add_argument('--output', type=Path, default=ROOT/'data/task4_v126_ai_provenance')
    args = parser.parse_args()
    # The transcript stays outside either versioned repository.
    private = args.private_output.resolve()
    for repo in [ROOT.parents[1], ROOT.parents[1].with_name('HiMCM-Overleaf')]:
        assert not private.is_relative_to(repo.resolve()), 'Private export must be outside Git repositories'
    size = args.cutoff_bytes if args.cutoff_bytes is not None else args.session.stat().st_size
    assert size > 0
    prefix_hash = hashlib.sha256()
    used = 0
    meta = None
    kinds, models, phases, excluded = (collections.Counter() for _ in range(4))
    turns, records = [], []
    for_export = []
    timestamps = []
    with args.session.open('rb') as stream:
        for line_number, raw in enumerate(stream, 1):
            if used + len(raw) > size or not raw.endswith(b'\n'):
                break
            prefix_hash.update(raw)
            used += len(raw)
            event = json.loads(raw)
            kinds[event['type']] += 1
            timestamp = event.get('timestamp')
            if timestamp:
                timestamps.append(timestamp)
            payload = event.get('payload', {})
            if event['type'] == 'session_meta':
                assert payload['id'] == THREAD, 'Not the explicitly scoped current task'
                meta = {key: payload.get(key) for key in ['id', 'timestamp', 'originator', 'cli_version', 'model_provider', 'source']}
            elif event['type'] == 'turn_context':
                model = payload.get('model')
                models[model] += 1
                turns.append(dict(line=line_number, timestamp=timestamp,
                                  turn_id=payload.get('turn_id'), recorded_model_identifier=model,
                                  source_line_sha256=digest(raw)))
            if event['type'] != 'response_item' or payload.get('type') != 'message':
                continue
            role = payload.get('role')
            parts = payload.get('content', [])
            allowed = 'input_text' if role == 'user' else 'output_text'
            if role not in ['user', 'assistant'] or any(p.get('type') != allowed for p in parts):
                excluded['non_visible_or_non_text_message'] += 1
                continue
            texts = [p.get('text', '') for p in parts]
            joined = '\n'.join(texts)
            phase = payload.get('phase')
            if role == 'user' and not joined.startswith(REQUEST_STARTS):
                excluded['injected_context_or_attachment_wrapper'] += 1
                continue
            if role == 'assistant' and phase not in ['commentary', 'final_answer']:
                excluded['assistant_phase_not_visible'] += 1
                continue
            # Preserve the original text parts verbatim; metadata never contains their text.
            entry = dict(line=line_number, timestamp=timestamp, role=role, phase=phase,
                         text_parts=texts)
            encoded = json.dumps(entry, ensure_ascii=False, separators=(',', ':')).encode()+b'\n'
            record = dict(line=line_number, timestamp=timestamp, role=role, phase=phase,
                          text_parts_count=len(texts), text_characters=sum(map(len, texts)),
                          source_line_sha256=digest(raw), exported_record_sha256=digest(encoded))
            records.append(record)
            for_export.append(encoded)
            phases[f'{role}:{phase}'] += 1
    assert meta and turns and for_export
    private.mkdir(parents=True, exist_ok=True)
    private_file = private/'visible_records.jsonl'
    private_file.write_bytes(b''.join(for_export))
    manifest = dict(
        scope='Explicit current task only; selected genuine requests and complete visible assistant message text parts',
        session_metadata=meta,
        source_prefix=dict(bytes=used, complete_lines=sum(kinds.values()), sha256=prefix_hash.hexdigest(),
                           first_timestamp=timestamps[0], last_timestamp=timestamps[-1]),
        event_type_counts=dict(kinds), recorded_turn_model_counts=dict(models), turn_contexts=turns,
        selected_message_counts=dict(phases), excluded_message_counts=dict(excluded),
        private_export=dict(basename=private_file.name, bytes=private_file.stat().st_size,
                            sha256=digest(private_file.read_bytes()), included_in_repository=False),
        selected_message_inventory=records,
        serving_build_identified=False, complete_team_ai_history=False,
        model_identifier_interpretation='Actual turn_context label, not proof of an immutable serving build or every subagent model',
        transcript_interpretation='Private selected visible-message export, not complete AI interaction history: tool-generated code/prose, tool results, attachments, earlier tasks and other team members are not covered',
        excluded_content='No reasoning, system/developer instructions, tool payloads, injected goal/environment/AGENTS context or attachment contents',
        publication_status='Metadata inventory only; private export requires team review before any publication or submission',
    )
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'session_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: manifest[k] for k in ['source_prefix', 'recorded_turn_model_counts', 'selected_message_counts', 'private_export', 'complete_team_ai_history']}, indent=2))


if __name__ == '__main__':
    main()
