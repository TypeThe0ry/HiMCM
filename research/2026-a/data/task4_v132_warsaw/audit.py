"""Verify the V132 nonadmission archive and protect current science."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 files=read(HERE/'archive_sha256.json')
 assert all(sha(HERE/n)==h for n,h in files.items())
 observations=read(HERE/'observations.json');assert observations==[]
 scope=read(HERE/'scope_audit.json');assert scope['admissions']==0
 requests=read(HERE/'retrievals.json')
 assert requests[0]['status']==202 and requests[0]['bytes']==0
 assert sha(HERE/requests[0]['file'])==requests[0]['sha256']
 assert 'error' in requests[1]
 text=read(HERE/'followup_web_representation.json')
 assert isinstance(text,str) and 'powyżej 6' in text and scope['official_summary_url'] in text
 registry=ROOT/'design/task4_user_current_model.json'
 protected={str(registry.relative_to(ROOT)):sha(registry)}
 snapshot=read(ROOT/'design/task4_user_v130_snapshot.json')
 protected.update(snapshot['source_sha256'])
 for version in ['128','131']:
  protected.update(read(ROOT/f'results/task4_v{version}_revision/audit.json')['result_sha256'])
 assert all(sha(ROOT/p)==h for p,h in protected.items())
 report=dict(status='pass',source_archive_files=len(files),original_HTTP202_empty_verified=True,
    original_timeout_verified=True,official_summary_representation_not_original=True,
    human_scope_audit_not_full_report_review=True,admissions=0,main_registry_version=read(registry)['version'],
    protected_scientific_files=len(protected),protected_sha256=protected,own_script_sha256=sha(Path(__file__)))
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: archive, zero admission, current registry/primary and old/new extensions protected')
if __name__=='__main__':main()
