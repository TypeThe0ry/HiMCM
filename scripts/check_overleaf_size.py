"""Check staged Git blobs against Overleaf limits and sync size guidance."""
from pathlib import Path
import argparse
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1].parent / 'HiMCM-Overleaf'
GIT = ['arch', '-arm64', '/usr/bin/git'] if sys.platform == 'darwin' and platform.machine() == 'x86_64' else ['git']

def git(*args, data=None):
    return subprocess.check_output(GIT + list(args), cwd=ROOT, input=data)

def main():
    global ROOT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manuscript_root', nargs='?', type=Path, default=ROOT)
    ROOT = parser.parse_args().manuscript_root.expanduser().resolve()
    entries = git('ls-files', '--stage', '-z').split(b'\0')
    objects = []
    for entry in filter(None, entries):
        meta, path = entry.split(b'\t', 1)
        mode, oid, stage = meta.split()
        if stage != b'0':
            raise SystemExit('Resolve staged merge conflicts before checking limits')
        objects.append((oid, path.decode()))
    sizes = git('cat-file', '--batch-check=%(objectsize)', data=b'\n'.join(o for o, _ in objects)+b'\n').splitlines()
    files = [(p, int(n)) for (_, p), n in zip(objects, sizes)]
    editable = [(p,n) for p,n in files if Path(p).suffix.lower() in {'.tex','.bib','.cls','.sty','.md','.txt','.csv','.json','.py','.yaml','.yml','.html','.css','.js'}]
    checks = {
        'file_count_at_most_2000': len(files) <= 2000,
        'recommended_sync_under_100_MB': sum(n for _,n in files) < 100_000_000,
        'each_file_at_most_50_MB': all(n <= 50_000_000 for _,n in files),
        'editable_total_at_most_7_MB': sum(n for _,n in editable) <= 7_000_000,
        'editable_file_at_most_2_MB': all(n <= 2_000_000 for _,n in editable),
    }
    print(json.dumps({'scope':'Git index blobs, excluding Git history', 'manuscript_root':str(ROOT), 'files':len(files), 'bytes':sum(n for _,n in files), 'checks':checks}, indent=2))
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    sys.exit(main())
