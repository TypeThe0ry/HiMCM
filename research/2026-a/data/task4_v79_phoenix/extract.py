"""Verify PXU's published operating ratio and its explicit vacancy definition."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent

def extract():
    for r in json.loads((HERE / 'manifest.json').read_text()):
        raw = (HERE / r['file']).read_bytes()
        assert len(raw) == r['bytes']
        assert hashlib.sha256(raw).hexdigest() == r['sha256']
    text = subprocess.check_output(['pdftotext', '-f', '140', '-l', '140', '-layout',
        str(HERE / 'acfr2025.pdf'), '-'], text=True)
    assert 'Operating Statistics' in text
    assert 'Teaching Staff (FTE) includes all teaching positions filled and vacant.' in text
    row = next(r for r in text.splitlines() if re.match(r'\s*2025\s', r))
    assert re.search(r'2025\s+25,502\s', row)
    assert re.search(r'1,635\s+15\.6\s+77\.0', row)
    result = dict(reference_year='Fiscal year ended June 30, 2025',
        population='Phoenix Union High School District, not Phoenix municipal school universe',
        pdf_page_1based=140, printed_page=133,
        average_daily_membership=25502, teaching_positions_fte_filled_and_vacant=1635,
        reported_pupil_teacher_ratio=15.6, reconstructed_ratio=25502/1635,
        actual_filled_teacher_count_identified=False,
        grade9_12_specific_staff_assignment_verified=False,
        main_model_admitted=False,
        interpretation='Operating ratio uses ADM and FTE positions including vacancies; not a city actual-teacher headcount ratio')
    assert round(result['reconstructed_ratio'],1) == result['reported_pupil_teacher_ratio']
    return result

if __name__ == '__main__':
    result = extract()
    (HERE / 'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
