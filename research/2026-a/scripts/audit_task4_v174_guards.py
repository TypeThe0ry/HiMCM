"""Exercise only malformed-input/directory/archive boundaries in temporary fixtures."""
from pathlib import Path
import argparse,json,subprocess,tempfile
from task4_v174_reproduce import archive_snapshot,check_pdf_identity,sha,safe_output

def main():
 p=argparse.ArgumentParser();p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
 research=Path(__file__).resolve().parents[3];paper=research.parent/'HiMCM-Overleaf'
 out=safe_output(a.output_dir,research,paper);passed=[]
 def rejects(name,fn,contains):
  try:fn()
  except ValueError as error:
   assert contains in str(error),(name,error);passed.append(dict(case=name,rejected=True,reason=str(error)))
  else:raise AssertionError(name+' was accepted')
 with tempfile.TemporaryDirectory(prefix='fixtures-',dir=out) as t:
  registry=json.loads((research/'research/2026-a/design/task4_user_current_review.json').read_text())
  temp=Path(t);canonical=paper/registry['pdf'];expected=registry['pdf_sha256']
  check_pdf_identity(canonical,expected)
  corrupt=temp/'corrupt.pdf';corrupt.write_bytes(canonical.read_bytes()+b'changed-fixture')
  rejects('canonical_pdf_identity',lambda:check_pdf_identity(corrupt,expected),'SHA256 mismatch')
  inside=research/'v174-must-not-be-created'
  rejects('output_inside_repository',lambda:safe_output(inside,research,paper),'outside both repositories')
  assert not inside.exists()
  rejects('output_repository_ancestor',lambda:safe_output(research.parent,research,paper),'outside both repositories')
  nonempty=temp/'nonempty';nonempty.mkdir();sentinel=nonempty/'sentinel';sentinel.write_text('preserve me')
  rejects('output_nonempty',lambda:safe_output(nonempty,research,paper),'new or empty');assert sentinel.read_text()=='preserve me'
  link=temp/'output-link';link.symlink_to(research,target_is_directory=True)
  rejects('output_symlink',lambda:safe_output(link,research,paper),'cannot be a symlink')
  for kind in ['export-ignore','export-subst','symlink']:
   repo=temp/kind;repo.mkdir();subprocess.run(['git','init','-q',str(repo)],check=True)
   (repo/'ordinary.txt').write_text('synthetic guard fixture\n')
   if kind=='export-ignore':
    (repo/'.gitattributes').write_text('ordinary.txt export-ignore\n')
   elif kind=='export-subst':
    (repo/'.gitattributes').write_text('ordinary.txt export-subst\n');(repo/'ordinary.txt').write_text('$Format:%H$\n')
   else:(repo/'external-link').symlink_to(sentinel)
   subprocess.run(['git','-C',str(repo),'add','.'],check=True)
   subprocess.run(['git','-C',str(repo),'-c','user.name=Reproduction Guard Fixture','-c','user.email=guard@example.invalid','-c','commit.gpgsign=false','-c','core.hooksPath=/dev/null','commit','-qm','Synthetic local guard fixture'],check=True)
   work=temp/(kind+'-work');work.mkdir()
   expected_reason={'export-ignore':'omits tracked files','export-subst':'differs from tracked blob','symlink':'Unsupported Git tree mode'}[kind]
   rejects('archive_'+kind,lambda repo=repo,work=work:archive_snapshot(repo,work/'source',work),expected_reason)
 report=dict(status='pass',guard_script_sha256=sha(Path(__file__)),runner_sha256=sha(Path(__file__).with_name('task4_v174_reproduce.py')),negative_guard_cases=len(passed),canonical_identity_positive_case=True,cases=passed,
  scope='Temporary synthetic fixtures only;no paper/model input edits or TeX builds in this guard test')
 (out/'guards.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='pass',negative_guard_cases=len(passed),report=str(out/'guards.json'))))
if __name__=='__main__':main()
