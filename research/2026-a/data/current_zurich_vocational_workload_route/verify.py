#!/usr/bin/env python3
"""Verify received bodies and regenerate selected PDF text offline using Poppler."""
import hashlib, json, subprocess
from pathlib import Path
p = Path(__file__).resolve().parent
receipts = json.loads((p / 'retrieval.json').read_text())
for r in receipts:
    b = (p / r['file']).read_bytes()
    assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], r['file']
for stem in ('bbz_2023_24', 'abzh_2023_24', 'bsd_position_plan', 'abzh_facts_2025_26'):
    subprocess.run(['pdftotext', '-layout', str(p / (stem + '.pdf')), str(p / (stem + '.txt'))], check=True)
pages = (p / 'abzh_2023_24.txt').read_text().split('\f')
assert all(x in pages[35] for x in ('Lehrpersonen                  106', 'Lernende Grundbildung         2261', 'Lernende Weiterbildung         78', 'Klassen                       137'))
a = (p / 'bsd_position_plan.txt').read_text()
assert 'Verwaltungsassistent' in a and 'Rechnungssekretär' in a
print(f'{len(receipts)} response bodies match receipts; ABZH page 36 and BSDPZ position categories verified; 0 workload observations admitted.')
