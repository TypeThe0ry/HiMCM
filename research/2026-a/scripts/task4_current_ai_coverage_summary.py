"""Summarize three authenticated root-log windows without private text."""
from pathlib import Path
from collections import Counter
import hashlib,json
R=Path(__file__).resolve().parents[1];O=R/'data/current_ai_continuation2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 paths=[R/'data'/n/'session_manifest.json' for n in ['task4_v178_ai_provenance','current_ai_provenance','current_ai_continuation2']]
 ms=[json.loads(p.read_text()) for p in paths];assert len({m['session_metadata']['id'] for m in ms})==1
 for a,b,p in zip(ms,ms[1:],paths):
  assert b['predecessor_source_prefix']==a['source_prefix'] and b['predecessor_manifest_sha256']==sha(p)
 windows=[];start=0;last_line=0;seen=set();models=Counter();visible=Counter();spawn=Counter()
 for index,(p,m) in enumerate(zip(paths,ms)):
  end=m['source_prefix']['bytes'];assert end>start
  counts=m.get('recorded_root_model_counts',m.get('recorded_turn_model_counts'));phases=m.get('selected_visible_counts',m.get('selected_message_counts'))
  assert sum(counts.values())==len(m['turn_contexts']) and sum(phases.values())==len(m['selected_message_inventory'])
  for inv in ['turn_contexts','selected_message_inventory','assistant_call_inventory']:
   for x in m[inv]:
    key=(inv,x['line']);assert last_line<x['line']<=m['source_prefix']['complete_lines'] and key not in seen;seen.add(key)
  models.update(counts);visible.update(phases)
  if index:spawn.update(m['requested_spawn_model_labels'])
  windows.append(dict(manifest=str(p.relative_to(R)),start_byte=start,end_byte=end,source_prefix_sha256=m['source_prefix']['sha256'],root_contexts=len(m['turn_contexts']),selected_visible_records=len(m['selected_message_inventory']),top_level_call_inputs=len(m['assistant_call_inventory'])))
  start=end;last_line=m['source_prefix']['complete_lines']
 result=dict(status='pass window-chain aggregation',windows=windows,root_contexts=sum(x['root_contexts'] for x in windows),selected_visible_records=sum(x['selected_visible_records'] for x in windows),top_level_call_inputs=sum(x['top_level_call_inputs'] for x in windows),recorded_root_model_identifiers=dict(models),selected_visible_counts=dict(visible),spawn_request_labels_in_two_continuations=dict(spawn),initial_window_spawn_labels_not_counted=True,latest_cutoff_utc=ms[-1]['delta']['last_timestamp'],source_sha256={str(p.relative_to(R)):sha(p) for p in [*paths,Path(__file__)]},complete_team_ai_history=False,submission_ready=False,scope='Counts selected record types across three nonoverlapping byte windows; no full transcript, nested execution, serving-version, child-session or complete-team claim. Earlier public selectors contain request prefixes; new selector uses fingerprints. Exact selected record exports stay private, not a content-anonymization claim.')
 (O/'coverage_summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','root_contexts','selected_visible_records','top_level_call_inputs','spawn_request_labels_in_two_continuations','latest_cutoff_utc']}))
if __name__=='__main__':main()
