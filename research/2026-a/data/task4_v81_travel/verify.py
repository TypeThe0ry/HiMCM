"""Verify the newly acquired 2025 originals and the year-specific field distinction."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
for item in json.loads((HERE / 'manifest.json').read_text())['files']:
    raw = (HERE / item['file']).read_bytes()
    assert len(raw) == item['bytes']
    assert hashlib.sha256(raw).hexdigest() == item['sha256']

def text(path, page=None):
    command = ['pdftotext', '-layout']
    if page is not None:
        command += ['-f', str(page), '-l', str(page)]
    return subprocess.check_output(command + [str(path), '-'], text=True)

question = text(HERE / 'questionnaire2025.pdf', 10)
assert all(s in question for s in ['B1.', 'B2.', 'B3.', 'Transport públic'])
assert question.index('B1.') < question.index('B2.') < question.index('B3.')
assert 'minut' not in question[question.index('B1.'):question.index('B2.')].lower()
new = text(HERE / 'manual2025.pdf')
old = text(HERE.parent / 'task4_v44_barcelona/manual2021.pdf')
fields = ['peuanar_m', 'bicianar_m', 'tpanar_m', 'cotxeanar_m',
          'motoanar_m', 'patinet_anar_m', 'altanar_m']
for field in fields:
    assert field in old and field not in new, field
assert 'Mitjà de transport per anar al centre escolar' in new
print('Official 2025 hashes and identified questionnaire/field contrast passed; no travel observations admitted.')
