"""Verify and extract the official published combined Mumbai grade XI-XII PTR."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent

def extract():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for item in manifest:
        raw = (HERE / item['file']).read_bytes()
        assert len(raw) == item['bytes']
        assert hashlib.sha256(raw).hexdigest() == item['sha256']
    text = subprocess.check_output([
        'pdftotext', '-f', '346', '-l', '346', '-layout',
        str(HERE / 'economic_survey2025_26.pdf'), '-'], text=True)
    assert 'SELECTED SOCIO-ECONOMIC INDICATORS OF DISTRICTS' in text
    assert 'Pupil Teachers Ratio' in text and '2024-25' in text
    assert 'Std XI-' in text and 'XII)' in text
    row = next(line for line in text.splitlines() if line.strip().startswith('Mumbai City'))
    match = re.search(r'38\^\s+16\^\s+(\d+)\^\s*$', row)
    assert match and int(match.group(1)) == 41
    assert '^ Including Mumbai Suburban' in text
    sub = next(line for line in text.splitlines() if line.strip().startswith('Mumbai Suburban'))
    assert re.search(r'-\s+-\s+-\s*$', sub)
    result = {
        'city': 'Mumbai', 'geography': 'Mumbai City and Mumbai Suburban combined',
        'reference_year': '2024-25', 'stage': 'Higher Secondary, standards XI-XII',
        'pdf_page_1based': 346, 'printed_page': 316, 'column': 24,
        'reported_ptr': 41, 'reported_utility': 15 / (15 + 41),
        'unit': 'Published pupils per teacher at the indicated education level',
        'rounding_rule_verified': False, 'fte_verified': False,
        'sampling_confidence_interval_available': False,
        'unrounded_counts_available': False,
        'scope': 'Official published stage-specific resource statistic; not a verified exact unrounded or FTE ratio.',
        'source_pdf_sha256': manifest[0]['sha256'],
    }
    return result

if __name__ == '__main__':
    result = extract()
    (HERE / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
