"""Integration check for read-only current audits.

Requires --session and optionally --private-output for the AI audit. Reports to
stdout by default; use --output PATH (and --overwrite if needed) to save JSON.
"""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from task4_current_research_bindings import verify_current_research

R=Path(__file__).resolve().parents[1]; G=R.parents[1]; P=G.parent/'HiMCM-Overleaf'; S=R/'scripts'
CANONICAL=R/'results/current_audit_workflow/verification.json'
parser=audit_parser(__doc__)
parser.add_argument('--session',type=Path,required=True)
parser.add_argument('--private-output',type=Path)
args=parser.parse_args();check_output(args,CANONICAL,G)

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def git(repo,*cmd):return subprocess.check_output(['git',*cmd],cwd=repo)
def state(repo):return (git(repo,'rev-parse','HEAD'),git(repo,'status','--porcelain=v1','-z','--untracked-files=all'))
def require(ok,label):
 if not ok:raise RuntimeError(label)

v=json.loads((R/'results/current_paper_review/current_verification.json').read_text())
keys=['additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256','additional_point_error_inputs_sha256']
bindings={}
for k in keys:bindings.update(v[k])
require(len(bindings) in (76,77),'unexpected supplemental binding count')
files={R/p for p in bindings}
files.update(R/p for p in v.get('withdrawal_source_sha256',{}))
files.update(R/p for p in v.get('edition_source_sha256',{}))
files.update(R/p for p in json.loads((R/'design/task4_user_v203_snapshot.json').read_text())['source_sha256'])
for name in ['current_ai_review','current_point_error','current_joint_collection','current_zurich_source_review','current_paper_review']:
 files.add(R/'results'/name/'verification.json')
files.add(R/'results/current_joint_collection/optimal_three_cell_sets.csv')
files.update([R/'results/current_paper_review/current_verification.json',R/'results/current_edition_paper_review/review.json',G/'paper/current/main.pdf'])
files.add(R/'results/current_remote_definition_review/review.json')
for p in v['current_files_sha256']:
 files.add(P/p);files.add(G/'paper/current'/p)
require(len(v['current_files_sha256'])==7,'paper dependency count')
research_integrity,research_protected=verify_current_research(R)
files.update(Path(n) for n in research_protected)
before={p:digest(p) for p in files}; states={p:state(p) for p in (G,P)}
python=str(G/'.venv-v120/bin/python'); env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['UV_CACHE_DIR']='/data/scratch/uv-cache'
ai=[python,str(S/'audit_current_ai_provenance.py'),'--session',str(args.session.resolve())]
if args.private_output:ai+=['--private-output',str(args.private_output.resolve())]
commands={
 'ai':ai,
 'point':[python,str(S/'audit_current_point_error.py')],
 'withdrawal':[python,str(S/'audit_current_point_withdrawal.py')],
 'joint':[python,str(S/'audit_current_joint_collection.py')],
 'zurich':['uv','run','--no-project','--with','openpyxl==3.1.5','python',str(S/'audit_current_zurich_source2026.py')],
 'paper':[python,str(S/'audit_current_paper.py')],
 'research_bindings':[python,str(S/'audit_current_research_bindings.py')],
}
checks={}
with tempfile.TemporaryDirectory(prefix='himcm-audit-test-',dir='/data/scratch') as temp:
 scratch=Path(temp)
 def run(label,cmd,success=True):
  result=subprocess.run(cmd,cwd=scratch,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  require((result.returncode==0)==success,label+' unexpected exit')
  if success:
   try:out=json.loads(result.stdout)
   except (ValueError,UnicodeDecodeError):raise RuntimeError(label+' invalid JSON') from None
   require(str(out.get('status','')).lower().startswith('pass'),label+' status')
  checks[label]='pass' if success else 'expected rejection'
  return result
 for name,cmd in commands.items():run('default_'+name,cmd)
 run('ai_head_baseline',ai+['--paper-baseline','HEAD'])
 marker=b'\\section*{Report on Use of AI Tools}'
 legacy=git(P,'show','d1a3996:main.tex');current=(P/'main.tex').read_bytes()
 require(legacy.count(marker)==1 and current.count(marker)==1,'baseline marker')
 if legacy.split(marker)[0]!=current.split(marker)[0]:run('ai_legacy_baseline',ai+['--paper-baseline','d1a3996'],False)
 output=scratch/'report.json'
 run('explicit_create',ai+['--output',str(output)])
 require(output.is_file(),'explicit report absent')
 written=digest(output)
 run('existing_without_overwrite',ai+['--output',str(output)],False)
 require(digest(output)==written,'existing report changed')
 invalid=G/'audit-test-invalid.json';overleaf=P/'audit-test-invalid.json';link=scratch/'link.json';link.symlink_to(output)
 for label,path in [('repository',invalid),('overleaf',overleaf),('symlink',link)]:
  require(path==link or not path.exists(),label+' destination already exists')
  run('reject_'+label,ai+['--output',str(path),'--overwrite'],False)
  require(path==link or not path.exists(),label+' destination created')
 require(digest(output)==written,'symlink target changed')
require({p:digest(p) for p in files}==before,'protected files changed')
require({p:state(p) for p in (G,P)}==states,'repository head or status changed')
sources=[Path(__file__),S/'task4_audit_output.py',S/'task4_current_research_bindings.py',R/'design/task4_current_research_integrity.json']+[Path(c[-1]) for k,c in commands.items() if k in ('point','withdrawal','joint','zurich','paper','research_bindings')]+[S/'audit_current_ai_provenance.py']
report={'status':'pass','checks':checks,'protected_files_checked':len(files),'supplemental_bindings_checked':len(bindings),'manuscript_withdrawal_binding_entries':len(v.get('withdrawal_source_sha256',{})),'paper_dependencies_per_checkout':7,'repositories_checked':2,'source_sha256':{str(p.relative_to(R)):digest(p) for p in sources}}
report['manuscript_edition_binding_entries']=len(v.get('edition_source_sha256',{}))
report['registered_research_integrity']=research_integrity
emit_report(report,args,CANONICAL,G)
