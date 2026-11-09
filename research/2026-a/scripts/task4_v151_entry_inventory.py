"""Read-only literal dependency and available-history audit of shared entry."""
from pathlib import Path
from collections import defaultdict
import csv,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v151_shared_entry'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(root,*a):return subprocess.check_output(['git',*a],cwd=root,text=True)
def clean_tex(s):
 # Keep newline counts so inventory lines remain original-source line numbers.
 lines=[]
 for line in s.splitlines():
  cut=len(line)
  for i,ch in enumerate(line):
   if ch!='%':continue
   k=i-1
   while k>=0 and line[k]=='\\':k-=1
   if (i-k-1)%2==0:cut=i;break
  lines.append(line[:cut])
 s='\n'.join(lines)
 return re.sub(r'\\begin\{comment\}.*?\\end\{comment\}',lambda m:'\n'*m.group().count('\n'),s,flags=re.S)
def main():
 O.mkdir(exist_ok=True);queue=['main.tex'];seen=set();rows=[]
 while queue:
  rel=queue.pop(0)
  if rel in seen:continue
  seen.add(rel);raw=(P/rel).read_text();text=clean_tex(raw)
  for m in re.finditer(r'\\(includegraphics|input|include|addbibresource)\s*(?:\[[^\]]*\]\s*)?\{([^{}]+)\}',text):
   cmd,name=m.groups();name=name.strip();kind='graphics' if cmd=='includegraphics' else 'bibliography' if cmd=='addbibresource' else 'tex_input';target=name
   if kind=='tex_input' and not Path(target).suffix:target+='.tex'
   exists=(P/target).is_file();row=dict(source=rel,line=text[:m.start()].count('\n')+1,command=cmd,kind=kind,literal_target=name,resolved_project_path=target,exists=exists,sha256=sha(P/target) if exists else '')
   rows.append(row)
   if kind=='tex_input' and exists:queue.append(target)
 missing=[r for r in rows if not r['exists']];names={Path(x['literal_target']).name.lower() for x in missing};hits=[];history_info={}
 for label,root in [('overleaf',P),('research',R.parents[1])]:
  current=subprocess.check_output(['rg','--files','--hidden','--no-ignore','-g','!**/.git/**','-g','!**/.venv*/**','-g','!**/__pycache__/**','-g','!**/node_modules/**'],cwd=root,text=True).splitlines()
  past=set(git(root,'log','--all','--format=','--name-only','--no-renames','--','*.png','*.jpg','*.jpeg','*.pdf','*.eps','*.svg').splitlines())
  for origin,paths in [('working_files',current),('available_git_path_history',past)]:
   for path in paths:
    if Path(path).name.lower() in names:hits.append(dict(repository=label,scope=origin,path=path))
  history_info[label]=dict(head=git(root,'rev-parse','HEAD').strip(),shallow=git(root,'rev-parse','--is-shallow-repository').strip()=='true',image_path_history_entries=len(past),scope='Available local refs/history; not a claim about outside archives, other machines or remote server history not fetched.')
 with (O/'shared_dependencies.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 shared=(P/'main.tex').read_text();stage=(P/'sections/task4_stage_progress.tex').read_text();assert '2029 Super Bowl' in shared and '25 cities' in stage and 'Singapore is the conservative recommendation' in stage
 own=(P/'drafts/task4_v137_core.tex').read_text();assert 'M=16' in own
 report=dict(iteration='V151',scope='Literal project dependencies after stripping TeX line comments and comment environments; not a full TeX interpreter or Overleaf UI inspection.',shared_root='main.tex',scanned_tex_sources=sorted(seen),dependency_references=len(rows),graphics_references=sum(r['kind']=='graphics' for r in rows),missing_graphics=sum(r['kind']=='graphics' for r in missing),missing_dependencies=missing,available_name_matches=hits,history_search=history_info,shared_body_scope='Retained sports-event location template; also includes a frozen 25-city interim section.',shared_control_labels_unverified=dict(mcmsetup_tcn=re.search(r'tcn\s*=\s*(\d+)',shared).group(1),author_label=re.search(r'Team\s*\\#(\d+)',shared).group(1)),current_owned_review=dict(source='drafts/task4_v137_paper.tex',documentation_revision='V148',primary_cities=16,control='PENDING'),proposed_root_review_entry='task4_review_entry.tex',project_main_setting_inspected=False,project_main_setting_changed=False,team_files_modified=False,asset_replacements=0,original_asset_authenticity='No replacement is inferred from a similar filename or a newer workflow figure.',source_sha256={n:sha(P/n) for n in sorted(set(seen)|{'ref.bib','mcmthesis.cls'})},inventory_sha256=sha(O/'shared_dependencies.csv'),generator_sha256=sha(Path(__file__)))
 (O/'inventory.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['dependency_references','graphics_references','missing_graphics','available_name_matches','scanned_tex_sources']},indent=2))
if __name__=='__main__':main()
