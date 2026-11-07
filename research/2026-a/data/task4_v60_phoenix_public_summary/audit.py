from pathlib import Path
import hashlib, json, subprocess
p = Path(__file__).resolve().parent
rows = json.loads((p / 'manifest.json').read_text())
assert len(rows) == 2
for r in rows:
    raw = (p / r['file']).read_bytes()
    assert raw.startswith(b'%PDF-')
    assert len(raw) == r['bytes']
    assert hashlib.sha256(raw).hexdigest() == r['sha256']
    text = subprocess.check_output(['pdftotext', str(p / r['file']), '-']).decode()
    assert 'To: Phoenix Union Employees' in text
    assert 'work' in text
    assert r['admissible_student_commute'] is False
assert json.loads((p / 'search_audit.json').read_text())['new_admissible_student_duration_observations'] == 0
print('PASS: 2 original employee-program PDFs; 0 admissible student-duration observations.')
