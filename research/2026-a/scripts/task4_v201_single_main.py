"""Prepare one self-contained main.tex and three current figures without pruning sources.

Recreates the one-time migration from the exact GitHub pre-cleanup archive;
future paper edits update the same current main instead of rerunning this migration.
"""
from pathlib import Path
import hashlib,json,re,shutil,argparse
R=Path(__file__).resolve().parents[1];P=R.parents[1]/'paper/history/overleaf_before_single_main_20261110';D=P/'drafts'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(out):
 assert not out.exists() or not any(out.iterdir()),'Use a new/empty output directory'
 out.mkdir(parents=True,exist_ok=True);bound={}
 def inline(path,stack=()):
  path=path.resolve();assert path not in stack,'Cyclic input';assert path.is_relative_to(P)
  bound[str(path.relative_to(P))]=sha(path);text=path.read_text()
  def replace(match):
   name=match[1];target=path.parent/name
   if not target.exists():target=D/name
   assert target.is_file(),name
   return inline(target,(*stack,path))
  return re.sub(r'\\input\{([^}]+)\}',replace,text)
 text=inline(D/'task4_v201_paper.tex')
 text=text.replace('% V201 owned review; provisional template number, registration unverified; user-supplied mcmthesis format, shared class unchanged.','% Current owned HiMCM manuscript. History and verification are maintained in GitHub.\n% Provisional template control number; actual registration unverified. Shared class unchanged.')
 text=text.replace(r'\graphicspath{{./}{drafts/}}',r'\graphicspath{{./}{figures/}}')
 figures={}
 for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',text):
  source=D/name;assert source.is_file(),source
  target='figures/'+Path(name).name;assert target not in figures or figures[target]==sha(source)
  (out/'figures').mkdir(exist_ok=True);shutil.copy2(source,out/target);figures[target]=sha(source);text=text.replace('{'+name+'}','{'+target+'}')
 assert len(figures)==3 and not re.search(r'\\input\{',text)
 (out/'main.tex').write_text(text)
 for name in ['mcmthesis.cls','ref.bib']:shutil.copy2(P/name,out/name)
 manifest=dict(scope='Single current self-contained main and required figures; source history remains in GitHub',source_sha256=bound,current_files_sha256={str(f.relative_to(out)):sha(f) for f in sorted(out.rglob('*')) if f.is_file()},reference_pdf_sha256=sha(D/'task4_v201_paper.pdf'),primary_model='V200',owned_review='V201',teammate_class_bibliography_unchanged=True)
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);a=p.parse_args();m=prepare(a.output_dir);a.manifest.parent.mkdir(exist_ok=True,parents=True);a.manifest.write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(dict(files=len(m['current_files_sha256']),inputs=len(m['source_sha256']))))
