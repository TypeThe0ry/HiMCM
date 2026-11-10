"""Check the archived TBZ route offline; never infer FTE from headcounts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/current_zurich_tbz_workload_route'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    pdf = DATA / 'report2024.pdf'
    assert sha(pdf) == '12b89332a94bfdc43ac64eb43ae838ff68c25aeb1ec7a7720661f9ef8183aca6'
    extracted = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'])
    assert extracted == (DATA / 'report2024.txt').read_bytes(), 'Archived extraction differs'
    pages = extracted.decode().split('\f')
    assert '3‘559' in pages[32] and '3‘132' in pages[32] and '427' in pages[32]
    assert 'Grundbildung' in pages[32]
    assert '240' in pages[33] and '173' in pages[33]
    assert 'Lehrpersonen, inkl.' in pages[33] and 'Abteilungsleitung' in pages[33]
    terms = re.findall(r'vollzeit\w*|pensen\w*|stellenprozent\w*|vollzeiteinheit\w*|\bFTE\b',
                       extracted.decode(), re.IGNORECASE)
    files = sorted(p for p in DATA.iterdir() if p.is_file()) + [Path(__file__).resolve()]
    return {
        'status': 'pass bounded offline source check',
        'source_sha256': {str(p.relative_to(ROOT)): sha(p) for p in files},
        'report_year': 2024, 'pdf_pages_checked': [33, 34],
        'basic_vocational_learners': 3559, 'continuing_education_students': 240,
        'teacher_headcount_including_department_leadership': 173,
        'text_workload_keyword_matches': terms,
        'actual_upper_secondary_teaching_FTE_verified': False,
        'reference_date_and_2024_25_alignment_verified': False,
        'primary_admissions': 0, 'actual_primary_width_reduction': 0,
        'changes_primary_model': False, 'changes_manuscript': False,
        'scope': 'Byte integrity and full PDF text replay plus selected figure/scope checks. '
                 'Keyword absence covers extractable report text, not all school sources. '
                 'Headcount and continuing-education scope cannot supply matched teaching FTE. '
                 'Source semantics also require the recorded independent review.'
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New report path; refuses overwrite')
    args = parser.parse_args()
    result = audit()
    raw = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as handle:
            handle.write(raw)
    else:
        print(raw, end='')
