"""Capture a bounded continuation of one actual root log; publish hashes only.

Visible selected requests/replies and plaintext top-level assistant tool inputs
stay in a separate mode-0700 directory. Source records for reasoning, tool
results, attachments, system/developer messages and injected continuations are
excluded. Selected unredacted tool-input strings may contain copied content;
this is not a content-redaction guarantee.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,os,re

R=Path(__file__).resolve().parents[1]
O=R/'data/current_ai_provenance'
OLD=R/'data/task4_v178_ai_provenance/session_manifest.json'
THREAD='01a1bba3-8ac1-7963-90bf-08d8c2fec116'
REQUESTS=('低级任务默认用luna','给这个上传到overleaf','所有的标题，summary','论文图片要按照之前的格式','标题，abstract怎么还不是你写','本地的论文要和远程保持同步')
sha=lambda b:hashlib.sha256(b).hexdigest()
def encode(x):return json.dumps(x,ensure_ascii=False,separators=(',',':')).encode()+b'\n'
def visible(p):
 if p.get('type')!='message' or p.get('recipient') not in (None,'all'):return False
 role=p.get('role');parts=p.get('content',[])
 if role not in ('user','assistant') or not parts:return False
 kind='input_text' if role=='user' else 'output_text'
 if any(x.get('type')!=kind for x in parts):return False
 if role=='assistant':return p.get('phase') in ('commentary','final_answer')
 return '\n'.join(x.get('text','') for x in parts).startswith(REQUESTS)
def call(p):
 field={'function_call':'arguments','custom_tool_call':'input'}.get(p.get('type'))
 ident=lambda x:isinstance(x,str) and re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',x) is not None
 return field if field and isinstance(p.get(field),str) and ident(p.get('name')) and (p.get('namespace') is None or ident(p['namespace'])) else None
def filehash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--session',required=True,type=Path);ap.add_argument('--private-output',required=True,type=Path);ap.add_argument('--refresh',action='store_true');a=ap.parse_args()
 old=json.loads(OLD.read_text());start=old['source_prefix']['bytes'];out=a.private_output
 assert not out.is_symlink();out=out.resolve()
 for repo in [R.parents[1],R.parents[2]/'HiMCM-Overleaf']:
  assert not out.is_relative_to(repo) and not repo.is_relative_to(out)
 names=['visible_records.jsonl','assistant_tool_arguments.jsonl']
 assert not out.exists() or (out.is_dir() and {p.name for p in out.iterdir()}<=set(names))
 prior=json.loads((O/'session_manifest.json').read_text()) if (O/'session_manifest.json').exists() else None
 if out.exists():
  for p in out.iterdir():assert prior and filehash(p)==prior['private_exports'][p.name]['sha256']
 out.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(out,0o700)
 cutoff=prior['source_prefix']['bytes'] if prior and not a.refresh else a.session.stat().st_size
 assert cutoff>=start
 streams={};temps={}
 try:
  for name in names:
   p=out/('.'+name+'.tmp');fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600);streams[name]=os.fdopen(fd,'wb');temps[name]=p
  prefix=hashlib.sha256();oldhash=hashlib.sha256();used=line=0;first=last=None;models=Counter();phases=Counter();tools=Counter();requested=Counter();contexts=[];messages=[];calls=[];metadata=None;start_line=None;old_seen=False
  with a.session.open('rb') as source:
   for raw in source:
    if used+len(raw)>cutoff or not raw.endswith(b'\n'):break
    used+=len(raw);line+=1;prefix.update(raw)
    if used<=start:oldhash.update(raw)
    if used==start:
     assert oldhash.hexdigest()==old['source_prefix']['sha256'];old_seen=True;start_line=line
    e=json.loads(raw);p=e.get('payload',{})
    if e.get('type')=='session_meta':
     assert p['id']==THREAD;metadata={k:p.get(k) for k in ['id','timestamp','originator','cli_version','model_provider','source']}
    if used<=start:continue
    ts=e.get('timestamp');first=first or ts;last=ts or last
    if e.get('type')=='turn_context':
     model=p.get('model');models[model]+=1;contexts.append(dict(line=line,timestamp=ts,recorded_model_identifier=model,source_line_sha256=sha(raw)))
    if e.get('type')!='response_item':continue
    if visible(p):
     entry=dict(line=line,timestamp=ts,role=p['role'],phase=p.get('phase'),text_parts=[x.get('text','') for x in p['content']]);b=encode(entry);streams[names[0]].write(b);phases[f"{entry['role']}:{entry['phase']}"]+=1
     messages.append(dict(line=line,timestamp=ts,role=entry['role'],phase=entry['phase'],source_line_sha256=sha(raw),exported_record_sha256=sha(b)))
    field=call(p)
    if field:
     entry=dict(line=line,timestamp=ts,call_type=p['type'],source_field=field,tool_namespace=p.get('namespace'),tool_name=p['name'],arguments=p[field]);b=encode(entry);streams[names[1]].write(b);name=(p.get('namespace')+'.' if p.get('namespace') else '')+p['name'];tools[name]+=1
     calls.append(dict(line=line,timestamp=ts,call_type=p['type'],tool_namespace=p.get('namespace'),tool_name=p['name'],source_field=field,argument_bytes=len(p[field].encode()),source_line_sha256=sha(raw),exported_record_sha256=sha(b)))
     if p['name']=='spawn_agent':
      try:q=json.loads(p[field]);m=q.get('model');requested[m if isinstance(m,str) else '(omitted/null)']+=1
      except (ValueError,AttributeError):pass
  assert metadata and old_seen and used>start and contexts
  if prior and not a.refresh:assert used==cutoff and prefix.hexdigest()==prior['source_prefix']['sha256']
  for f in streams.values():f.close()
  if prior:
   for name in names:
    with temps[name].open('rb') as f:assert sha(f.read(prior['private_exports'][name]['bytes']))==prior['private_exports'][name]['sha256'],'Prior private export not retained as prefix'
  for name in names:os.replace(temps[name],out/name)
  exports={name:dict(bytes=(out/name).stat().st_size,sha256=filehash(out/name),mode=oct((out/name).stat().st_mode&0o777),included_in_repository=False) for name in names}
  manifest=dict(version='current bounded root continuation',session_metadata=metadata,predecessor_manifest_sha256=filehash(OLD),predecessor_source_prefix=old['source_prefix'],source_prefix=dict(bytes=used,complete_lines=line,sha256=prefix.hexdigest()),delta=dict(start_byte=start,end_byte=used,complete_lines=line-start_line,first_timestamp=first,last_timestamp=last),recorded_root_model_counts=dict(models),turn_contexts=contexts,selected_visible_counts=dict(phases),top_level_call_counts=dict(tools),requested_spawn_model_labels=dict(requested),selected_message_inventory=messages,assistant_call_inventory=calls,private_exports=exports,private_directory_mode=oct(out.stat().st_mode&0o777),script_sha256=filehash(Path(__file__)),request_filter_policy=list(REQUESTS),record_exclusion_not_content_redaction=True,private_arguments_unredacted=True,private_content_published=False,complete_team_ai_history=False,submission_ready=False,excluded=['reasoning/analysis','system/developer messages','tool results','attachments','injected continuations','unselected user records','subagent sessions','other chats/team members'],scope='Bounded continuation of one root session; top-level calls only, not nested execution counts; requested agent labels are not attested serving builds; later work remains outside cutoff')
  O.mkdir(exist_ok=True);(O/'session_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({k:manifest[k] for k in ['delta','recorded_root_model_counts','selected_visible_counts','top_level_call_counts','requested_spawn_model_labels','complete_team_ai_history']},ensure_ascii=False))
 finally:
  for f in streams.values():
   if not f.closed:f.close()
  for p in temps.values():p.unlink(missing_ok=True)
if __name__=='__main__':main()
