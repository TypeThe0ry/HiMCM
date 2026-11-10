"""Shared opt-in report delivery for read-only scientific audits."""
import argparse,json,os,tempfile
from pathlib import Path

def audit_parser(description):
 parser=argparse.ArgumentParser(description=description)
 parser.add_argument('--output',type=Path,help='Explicit JSON report destination; default is stdout only')
 parser.add_argument('--overwrite',action='store_true',help='Allow replacing the explicitly selected report')
 return parser

def check_output(args,canonical,repo_root):
 if args.output is None:
  if args.overwrite:raise ValueError('--overwrite requires --output')
  return None
 path=Path(args.output).expanduser()
 if path.is_symlink():raise ValueError('Report destination cannot be a symbolic link')
 if path.suffix.lower()!='.json':raise ValueError('Report destination must be JSON')
 path=path.resolve();canonical=Path(canonical).resolve();repo_root=Path(repo_root).resolve()
 if path.is_relative_to(repo_root.parent/'HiMCM-Overleaf'):
  raise ValueError('Research audit reports cannot be written into the manuscript checkout')
 if path.is_relative_to(repo_root) and path!=canonical:
  raise ValueError('Inside the research repository, only this audit canonical report is allowed')
 if path.exists() and (not path.is_file() or not args.overwrite):
  raise ValueError('Existing report requires explicit --overwrite')
 return path

def emit_report(report,args,canonical,repo_root):
 path=check_output(args,canonical,repo_root)
 rendered=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
 if path is not None:
  path.parent.mkdir(parents=True,exist_ok=True)
  temporary=None
  try:
   with tempfile.NamedTemporaryFile('w',encoding='utf-8',dir=path.parent,prefix='.'+path.name+'.',delete=False) as out:
    temporary=Path(out.name);out.write(rendered)
   # Recheck after computation; do not overwrite a newly appeared report by default.
   check_output(args,canonical,repo_root)
   if args.overwrite:os.replace(temporary,path)
   else:
    os.link(temporary,path);temporary.unlink()
   temporary=None
  finally:
   if temporary is not None:temporary.unlink(missing_ok=True)
 print(rendered,end='')
