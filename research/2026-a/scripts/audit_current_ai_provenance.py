"""Read-only bounded AI provenance audit; never print private records.

Default: stdout only, independent of later manuscript edits. Optional
--paper-baseline REF checks a deliberately selected pre-AI manuscript snapshot.
Use --output PATH --overwrite only for an intentional report rebuild.
"""
import collections, hashlib, json, os, pathlib, re, stat, subprocess
from task4_audit_output import audit_parser,check_output,emit_report
R=pathlib.Path(__file__).resolve().parents[1]
G=R.parents[1]
M=R/'data/current_ai_provenance/session_manifest.json'
OLD=R/'data/task4_v178_ai_provenance/session_manifest.json'
H=lambda b:hashlib.sha256(b).hexdigest()
def filehash(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def fail(condition,label):
 if not condition:raise RuntimeError(label)
def main():
 ap=audit_parser(__doc__);ap.add_argument('--session',type=pathlib.Path,required=True);ap.add_argument('--private-output',type=pathlib.Path);ap.add_argument('--paper-baseline',help='Optional explicit Git revision for pre-AI body and six resource checks');args=ap.parse_args();canonical=R/'results/current_ai_review/verification.json';check_output(args,canonical,G)
 m=json.loads(M.read_text());old=json.loads(OLD.read_text());start=m['delta']['start_byte'];end=m['delta']['end_byte']
 fail(filehash(OLD)==m['predecessor_manifest_sha256'] and old['source_prefix']==m['predecessor_source_prefix'],'predecessor binding')
 fail(start==old['source_prefix']['bytes'] and end==m['source_prefix']['bytes'],'prefix bounds')
 fail(filehash(R/'scripts/task4_current_ai_provenance.py')==m['script_sha256'],'capture script hash')
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
   if pos<=start:h_old.update(raw);continue
   delta+=1;e=json.loads(raw);p=e.get('payload',{});ts=e.get('timestamp');first=first or ts;last=ts or last
   if e.get('type')=='turn_context':
    i=invt.get(lines);fail(i is not None and i['source_line_sha256']==H(raw) and i['timestamp']==ts and i['recorded_model_identifier']==p.get('model'),'context inventory');seen_t.add(lines);models[p.get('model')]+=1
   if e.get('type')!='response_item':continue
   typ=p.get('type');parts=p.get('content',[]);role=p.get('role');phase=p.get('phase')
   eligible=typ=='message' and p.get('recipient') in (None,'all') and role in ('user','assistant') and bool(parts) and all(q.get('type')==('input_text' if role=='user' else 'output_text') for q in parts)
   selected=eligible and (phase in ('commentary','final_answer') if role=='assistant' else '\n'.join(q.get('text','') for q in parts).startswith(tuple(m['request_filter_policy'])))
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
 science=json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256'];fail(len(science)==548,'science binding count')
 for path,digest in science.items():fail(filehash(R/path)==digest,'science binding mismatch')
 v=json.loads((R/'results/current_paper_review/current_verification.json').read_text());extra={}
 for key,n in [('additional_source_scope_sha256',22),('additional_figure_inputs_sha256',27),('additional_student_inputs_sha256',12)]:
  fail(len(v[key])==n,'supplemental binding count');extra.update(v[key])
 fail(len(extra)==61,'supplemental unique binding count')
 for path,digest in extra.items():fail(filehash(R/path)==digest,'supplemental binding mismatch')
 fail(m.get('record_exclusion_not_content_redaction') is True and m.get('private_arguments_unredacted') is True and m['private_content_published'] is False and m['complete_team_ai_history'] is False and m['submission_ready'] is False,'privacy and readiness flags')
 paper_baseline=None;resources=[]
 if args.paper_baseline:
  P=G.parent/'HiMCM-Overleaf';marker=b'\\section*{Report on Use of AI Tools}'
  paper_baseline=subprocess.check_output(['git','rev-parse','--verify','--end-of-options',args.paper_baseline+'^{commit}'],cwd=P,text=True).strip()
  base=subprocess.check_output(['git','show',paper_baseline+':main.tex'],cwd=P);current=(P/'main.tex').read_bytes()
  fail(base.count(marker)==1 and current.count(marker)==1 and base.split(marker)[0]==current.split(marker)[0],'pre-AI body differs from requested paper baseline')
  resources=['mcmthesis.cls','ref.bib','figures/country_contrasts.pdf','figures/identification_matrix.pdf','figures/score_intervals.pdf','figures/walktime_context.pdf']
  for path in resources:fail(subprocess.check_output(['git','show',paper_baseline+':'+path],cwd=P)==(P/path).read_bytes(),'paper resource differs from requested baseline')
 out={'supplemental_bindings_checked':len(extra),'paper_baseline_checked':paper_baseline,'pre_ai_body_matches_requested_baseline':True if paper_baseline else None,'paper_resources_checked':len(resources),'audit_script_sha256':filehash(pathlib.Path(__file__)),'capture_script_sha256':m['script_sha256'],'manifest_sha256':filehash(M),'readme_sha256':filehash(M.parent/'README.md'),'predecessor_manifest_sha256':filehash(OLD),'status':'PASS','source_prefix_sha256':h.hexdigest(),'predecessor_source_prefix_sha256':h_old.hexdigest(),'delta_lines':delta,'contexts':len(seen_t),'selected_messages':len(seen_s),'assistant_calls':len(seen_c),'private_exports_checked':bool(streams),'private_export_counts':export_counts,'core_science_bindings_checked':len(science),'scope':'Root session bounded prefix and selected source record types; requested labels do not attest serving versions. Unredacted private inputs may contain copied sensitive content; no content-redaction claim. No subagent or whole-team history claim.'}
 emit_report(out,args,canonical,G)
if __name__=='__main__':main()
