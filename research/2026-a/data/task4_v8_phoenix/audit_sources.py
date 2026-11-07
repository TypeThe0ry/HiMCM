"""Check preserved source bytes; do not synthesize missing observations."""
from pathlib import Path
import csv, hashlib, json
ROOT = Path(__file__).resolve().parent

def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for row in manifest:
        if 'sha256' in row:
            data = (ROOT / row['file']).read_bytes()
            assert len(data) == row['bytes']
            assert hashlib.sha256(data).hexdigest() == row['sha256']
        else:
            assert row.get('error') and not (ROOT / row['file']).exists()
    rows = list(csv.DictReader((ROOT / 'observations.csv').open()))
    assert rows == [], 'No local Phoenix student microdata were acquired in this audit.'
    gaps = list(csv.DictReader((ROOT / 'evidence_gaps.csv').open()))
    assert all(r['admissible_main'] == 'false' for r in gaps)
    print(f'PASS: {len(manifest)} download attempts; {sum("sha256" in r for r in manifest)} original archived; 0 observations; {len(gaps)} audited leads.')

if __name__ == '__main__':
    main()
