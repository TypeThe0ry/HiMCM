"""Read-only bounded AI provenance audit; never print private records.

Default: stdout only, independent of later manuscript edits. Optional
--paper-baseline REF checks a deliberately selected pre-AI manuscript snapshot.
Use --output PATH --overwrite only for an intentional report rebuild.
"""
import collections, hashlib, json, os, pathlib, re, stat, subprocess
from task4_audit_output import audit_parser,check_output,emit_report
from task4_current_ai_continuation2 import REQUEST_FINGERPRINTS
R=pathlib.Path(__file__).resolve().parents[1]
G=R.parents[1]
M=R/'data/current_ai_continuation2/session_manifest.json'
OLD=R/'data/current_ai_provenance/session_manifest.json'
H=lambda b:hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def fail(condition,label):
 if not condition:raise RuntimeError(label)
def main():
 ap=audit_parser(__doc__);ap.add_argument('--session',type=pathlib.Path,required=True);ap.add_argument('--private-output',type=pathlib.Path);ap.add_argument('--paper-baseline',help='Optional explicit Git revision for pre-AI body and six resource checks');args=ap.parse_args();canonical=R/'results/current_ai_continuation2/verification.json';check_output(args,canonical,G)
 m=json.loads(M.read_text());old=json.loads(OLD.read_text());start=m['delta']['start_byte'];end=m['delta']['end_byte']
 allowed={'version','session_metadata','predecessor_manifest_sha256','predecessor_source_prefix','source_prefix','delta','recorded_root_model_counts','turn_contexts','selected_visible_counts','top_level_call_counts','requested_spawn_model_labels','selected_message_inventory','assistant_call_inventory','private_exports','private_directory_mode','script_sha256','request_filter_fingerprints','record_exclusion_not_content_redaction','private_arguments_unredacted','private_content_published','complete_team_ai_history','submission_ready','excluded','scope'}
 fail(set(m)==allowed,'manifest schema')
 fail(m['version']=='third bounded root window' and m['excluded']==['reasoning/analysis','system/developer messages','tool results','attachments','injected continuations','unselected user records','subagent sessions','other chats/team members'] and m['scope']=='Bounded continuation of one root session; top-level calls only, not nested execution counts; requested agent labels are not attested serving builds; later work remains outside cutoff','manifest prose schema')
 fail(m['request_filter_fingerprints']==REQUEST_FINGERPRINTS,'request filter fingerprints')
 for key,fields in [('turn_contexts',{'line','timestamp','recorded_model_identifier','source_line_sha256'}),('selected_message_inventory',{'line','timestamp','role','phase','source_line_sha256','exported_record_sha256'}),('assistant_call_inventory',{'line','timestamp','call_type','tool_namespace','tool_name','source_field','argument_bytes','source_line_sha256','exported_record_sha256'})]:
  fail(all(set(row)==fields for row in m[key]),'inventory schema')
 fail(m['private_directory_mode']=='0o700' and all(set(v)=={'bytes','sha256','mode','included_in_repository'} and v['mode']=='0o600' for v in m['private_exports'].values()),'export metadata schema')

 fail(filehash(OLD)==m['predecessor_manifest_sha256'] and old['source_prefix']==m['predecessor_source_prefix'],'predecessor binding')
 fail(start==old['source_prefix']['bytes'] and end==m['source_prefix']['bytes'],'prefix bounds')
 fail(filehash(R/'scripts/task4_current_ai_continuation2.py')==m['script_sha256'],'capture script hash')
 invs={i['line']:i for i in m['selected_message_inventory']}; invc={i['line']:i for i in m['assistant_call_inventory']}; invt={i['line']:i for i in m['turn_contexts']}
 fail(len(invs)==len(m['selected_message_inventory']) and len(invc)==len(m['assistant_call_inventory']) and len(invt)==len(m['turn_contexts']),'duplicate inventory line')
 streams={};export_counts={}
 if args.private_output:
  d=args.private_output
  fail(not d.is_symlink() and d.is_dir() and stat.S_IMODE(d.stat().st_mode)==0o700,'private directory')
  d=d.resolve();fail(not d.is_relative_to(G) and not d.is_relative_to(G.parent/'HiMCM-Overleaf'),'private location')
  fail(set(p.name for p in d.iterdir())==set(m['private_exports']),'private file set')
  for name,info in m['private_exports'].items():
   p=d/name;fail(not p.is_symlink() and p.is_file() and stat.S_IMODE(p.stat().st_mode)==0o600,'private file permissions')
   fail(p.stat().st_size==info['bytes'] and filehash(p)==info['sha256'] and not info['included_in_repository'],'private file hash')
   streams[name]=p.open('rb');export_counts[name]=0
 h=hashlib.sha256();h_old=hashlib.sha256();pos=lines=delta=0;first=last=None;models=collections.Counter();phases=collections.Counter();tools=collections.Counter();spawn=collections.Counter();seen_s=set();seen_c=set();seen_t=set()
 with args.session.open('rb') as f:
  while pos<end:
   raw=f.readline(end-pos);fail(raw.endswith(b'\n'),'line boundary');pos+=len(raw);lines+=1;h.update(raw)
   if pos<=start:
    h_old.update(raw)
    if lines==1:
     meta=json.loads(raw);payload=meta.get('payload',{});fail(meta.get('type')=='session_meta' and {k:payload.get(k) for k in ['id','timestamp','originator','cli_version','model_provider','source']}==m['session_metadata'],'session metadata')
    continue
   delta+=1;e=json.loads(raw);p=e.get('payload',{});ts=e.get('timestamp');first=first or ts;last=ts or last
   if e.get('type')=='turn_context':
    i=invt.get(lines);fail(i is not None and i['source_line_sha256']==H(raw) and i['timestamp']==ts and i['recorded_model_identifier']==p.get('model'),'context inventory');seen_t.add(lines);models[p.get('model')]+=1
   if e.get('type')!='response_item':continue
   typ=p.get('type');parts=p.get('content',[]);role=p.get('role');phase=p.get('phase')
   eligible=typ=='message' and p.get('recipient') in (None,'all') and role in ('user','assistant') and bool(parts) and all(q.get('type')==('input_text' if role=='user' else 'output_text') for q in parts)
   selected=eligible and (phase in ('commentary','final_answer') if role=='assistant' else any(H(('\n'.join(q.get('text','') for q in parts)).encode()[:x['utf8_bytes']])==x['sha256'] for x in REQUEST_FINGERPRINTS))
   if selected:
    i=invs.get(lines);fail(i is not None and (i['timestamp'],i['role'],i['phase'],i['source_line_sha256'])==(ts,role,phase,H(raw)),'message inventory');seen_s.add(lines);phases[f'{role}:{phase}']+=1
    if streams:
     b=streams['visible_records.jsonl'].readline();z=json.loads(b);fail(H(b)==i['exported_record_sha256'] and z==dict(line=lines,timestamp=ts,role=role,phase=phase,text_parts=[q.get('text','') for q in parts]),'message export');export_counts['visible_records.jsonl']+=1
   field={'function_call':'arguments','custom_tool_call':'input'}.get(typ);name=p.get('name');ns=p.get('namespace');ident=lambda v:isinstance(v,str) and re.fullmatch(r'[A-Za-z0-9_.:-]{1,160}',v) is not None
   if field and isinstance(p.get(field),str) and ident(name) and (ns is None or ident(ns)):
    i=invc.get(lines);fail(i is not None and (i['timestamp'],i['call_type'],i['tool_namespace'],i['tool_name'],i['source_field'],i['argument_bytes'],i['source_line_sha256'])==(ts,typ,ns,name,field,len(p[field].encode()),H(raw)),'call inventory');seen_c.add(lines);tools[(ns+'.' if ns else '')+name]+=1
    if name=='spawn_agent':
     try:
      q=json.loads(p[field]);model=q.get('model');spawn[model if isinstance(model,str) else '(omitted/null)']+=1
     except (ValueError,AttributeError):pass
    if streams:
     b=streams['assistant_tool_arguments.jsonl'].readline();z=json.loads(b);fail(H(b)==i['exported_record_sha256'] and z==dict(line=lines,timestamp=ts,call_type=typ,source_field=field,tool_namespace=ns,tool_name=name,arguments=p[field]),'call export');export_counts['assistant_tool_arguments.jsonl']+=1
 for f in streams.values():fail(f.read(1)==b'','extra private records');f.close()
 fail(pos==end and h.hexdigest()==m['source_prefix']['sha256'] and h_old.hexdigest()==old['source_prefix']['sha256'],'source prefix hash')
 fail(lines==m['source_prefix']['complete_lines'] and delta==m['delta']['complete_lines'] and first==m['delta']['first_timestamp'] and last==m['delta']['last_timestamp'],'source metadata')
 fail(seen_s==set(invs) and seen_c==set(invc) and seen_t==set(invt),'inventory completeness')
 fail(dict(models)==m['recorded_root_model_counts'] and dict(phases)==m['selected_visible_counts'] and dict(tools)==m['top_level_call_counts'] and dict(spawn)==m['requested_spawn_model_labels'],'aggregate counts')
 v=json.loads((R/'results/current_paper_review/current_verification.json').read_text());science=json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256']
 current=json.loads((R/'design/task4_user_v204_snapshot.json').read_text())['source_sha256']
 fail(len(science)==548 and len(current)==110,'science binding count')
 for group in (science,current,v['v204_science_sha256']):
  for path,digest in group.items():fail(filehash(R/path)==digest,'science binding mismatch')
 P=G.parent/'HiMCM-Overleaf'
 fail(len(v['current_files_sha256'])==7,'paper dependency count')
 for path,digest in v['current_files_sha256'].items():fail(filehash(P/path)==filehash(G/'paper/current'/path)==digest,'paper dependency mismatch')
 fail(filehash(G/'paper/current/main.pdf')==v['pdf_sha256'],'paper PDF mismatch')
 paper_baseline=None;resources=[]
 if args.paper_baseline:
  marker=b'\\section*{Report on Use of AI Tools}'
  paper_baseline=subprocess.check_output(['git','rev-parse','--verify','--end-of-options',args.paper_baseline+'^{commit}'],cwd=P,text=True).strip()
  base=subprocess.check_output(['git','show',paper_baseline+':main.tex'],cwd=P);body=(P/'main.tex').read_bytes()
  fail(base.count(marker)==1 and body.count(marker)==1 and base.split(marker)[0]==body.split(marker)[0],'pre-AI body differs from requested baseline')
  resources=['mcmthesis.cls','ref.bib','figures/country_contrasts.pdf','figures/identification_matrix.pdf','figures/score_intervals.pdf','figures/walktime_context.pdf']
  for path in resources:fail(subprocess.check_output(['git','show',paper_baseline+':'+path],cwd=P)==(P/path).read_bytes(),'paper resource differs from requested baseline')
 fail(m.get('record_exclusion_not_content_redaction') is True and m.get('private_arguments_unredacted') is True and m['private_content_published'] is False and m['complete_team_ai_history'] is False and m['submission_ready'] is False,'privacy and readiness flags')
 sources=[M,OLD,R/'scripts/task4_current_ai_continuation2.py',pathlib.Path(__file__),R/'scripts/task4_audit_output.py']
 out={'status':'PASS','source_sha256':{str(p.relative_to(R)):filehash(p) for p in sources},'source_prefix_sha256':h.hexdigest(),'predecessor_source_prefix_sha256':h_old.hexdigest(),'delta_lines':delta,'contexts':len(seen_t),'selected_messages':len(seen_s),'assistant_calls':len(seen_c),'recorded_root_model_counts':dict(models),'selected_visible_counts':dict(phases),'requested_spawn_model_labels':dict(spawn),'private_exports_checked':bool(streams),'private_export_counts':export_counts,'science_bindings_checked':len(science)+len(current),'paper_dependencies_each_copy':7,'scope':'Fixed third window of one root session. Recorded model identifiers and requested agent labels do not attest serving builds. Requests do not prove successful execution; nested calls are not counted. No subagent sessions or complete team history. Selected private inputs are unredacted; record-type exclusion does not guarantee content redaction.'}
 out.update(paper_baseline_checked=paper_baseline,pre_ai_body_matches_requested_baseline=True if paper_baseline else None,paper_resources_checked=len(resources))
 emit_report(out,args,canonical,G)
if __name__=='__main__':main()
