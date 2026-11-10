"""Offline integrity/scope checks for bounded V195 sources; no model admission."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from task4_v5_model import ROOT

OUT=ROOT/'results/task4_v195_sources'
P=ROOT.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args):return subprocess.check_output(args,text=True).strip()
def main():
    snapshot=json.loads((ROOT/'design/task4_user_v192_snapshot.json').read_text())['source_sha256']
    assert len(snapshot)==327
    for n,h in snapshot.items():assert sha(ROOT/n)==h,n
    previous=json.loads((ROOT/'results/task4_v194_priority/summary.json').read_text())['source_sha256']
    nav={n:h for n,h in previous.items() if n.startswith('design/task4_user_current_')}
    assert len(nav)==4
    for n,h in nav.items():assert sha(ROOT/n)==h,n
    checks={}
    for city in ['vienna','warsaw','helsinki']:
        script=ROOT/f'data/task4_v195_{city}'/('extract.py' if city=='helsinki' else 'verify.py')
        checks[city]=run([sys.executable,str(script)])
    tokyo=json.loads((ROOT/'data/task4_v195_tokyo/routes.json').read_text())
    assert len(tokyo['routes'])==2 and tokyo['primary_admissions']==0
    assert all(not r['source_table_admitted'] for r in tokyo['routes'])
    collector=ROOT/'data/task4_v194_dublin/collect.py'
    # Simulate the precise interruption: original exists but no receipt exists.
    with tempfile.TemporaryDirectory(prefix='himcm-v195-guard-') as tmp:
        q=Path(tmp);(q/'collect.py').write_bytes(collector.read_bytes())
        raw=q/'ncse_postprimary_allocations_original.csv';raw.write_bytes(b'preserve-interrupted-capture')
        result=subprocess.run([sys.executable,str(q/'collect.py')],capture_output=True,text=True)
        assert result.returncode!=0 and 'FileExistsError: Existing raw capture' in result.stderr
        assert raw.read_bytes()==b'preserve-interrupted-capture' and not (q/'retrievals.json').exists()
    assert run(['git','-C',str(P),'status','--porcelain'])==''
    assert run(['git','-C',str(P),'rev-parse','HEAD'])=='ea3ea5c7b5c7d1f1ece1cd07d708df97bc3e4c0d'
    paths=[Path(__file__),collector,*[p for city in ['vienna','warsaw','helsinki','tokyo'] for p in (ROOT/f'data/task4_v195_{city}').iterdir() if p.is_file()]]
    report=dict(status='pass',science='V192 unchanged',paper='V193 unchanged',primary_admissions=0,actual_score_width_reduction=0,immutable_science_bindings=327,current_navigation_bindings=nav,source_checks=checks,Tokyo_failed_browser_routes=2,interrupted_raw_capture_guard='pass; rejects before fetching and preserves bytes without receipt',overleaf_worktree_clean=True,overleaf_head='ea3ea5c7b5c7d1f1ece1cd07d708df97bc3e4c0d',scope='Source integrity and recorded measurement definitions; no server compile or new numerical source admission claimed.',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in paths})
    OUT.mkdir(exist_ok=True)
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='source_sha256'},indent=2))
if __name__=='__main__':main()
