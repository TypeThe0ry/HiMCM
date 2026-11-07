"""Offline extraction; run python3 extract_education.py. Requires beautifulsoup4."""
import csv
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'manifest.json').read_text())
for entry in manifest:
    if 'sha256' in entry:
        assert hashlib.sha256((ROOT / entry['file']).read_bytes()).hexdigest() == entry['sha256'], entry['file']

def url(name):
    return next(r['url'] for r in manifest if r.get('file') == name and 'sha256' in r)

rows = []
def observation(city, students, teachers, sources, scope, status):
    rows.append(dict(city=city, indicator='upper_secondary_ptr', value=students / teachers,
                     year=2024, unit='students_per_teacher_headcount', source_url=' | '.join(sources),
                     scope=scope, status=status, students=students, teachers=teachers))

with (ROOT / 'tokyo_highschool_totals2024.csv').open(encoding='utf-8-sig') as f:
    matches = [r for r in csv.DictReader(f) if r['種別'] == '総数（国・公・私立）' and r['地域'] == '総数' and r['西暦（年度）'] == '2024']
assert len(matches) == 1
r = matches[0]
observation('Tokyo', int(r['生徒数（人）']), int(r['教員数（本務者）（人）']),
            [url('tokyo_highschool_totals2024.csv')],
            'Tokyo prefecture; national/public/private high schools full-time and part-time courses; main-duty teacher headcount; excludes correspondence and separately tabulated integrated secondary schools; not FTE',
            'observed_upper_secondary_scope_conditional')

school_types = {'Government', 'Government-Aided', 'Independent'}
def sg_total(filename, field):
    data = json.loads((ROOT / filename).read_text())['result']
    assert len(data['records']) == data['total'], 'Pagination incomplete'
    matches = [r for r in data['records'] if r['year'] == '2024' and r['sex'] == 'MF' and r['school_type'] in school_types]
    assert len(matches) == 3 and {r['school_type'] for r in matches} == school_types
    return sum(int(r[field]) for r in matches)
observation('Singapore', sg_total('sg_preu_students.json', 'students_preu'), sg_total('sg_preu_teachers.json', 'teachers_preu'),
            [url('sg_preu_students.json'), url('sg_preu_teachers.json')],
            'Pre-university; Government/Government-Aided/Independent matched school strata; excludes Specialised Independent because teacher count unavailable; JC/CI/Pre-U centres; student and teacher reference dates differ within year; headcount not FTE; not all ages or all upper-secondary programmes',
            'observed_preuniversity_subset_scope_conditional')

soup = BeautifulSoup((ROOT / 'shanghai_students2024.html').read_bytes(), 'html.parser')
sh = [[c.get_text(' ', strip=True) for c in tr.find_all(['td','th'], recursive=False)] for tr in soup.find_all('tr')]
sh = [r for r in sh if any(c == '上 海 Shanghai' for c in r)]
assert len(sh) == 1, sh
# English and Chinese region labels occupy separate cells; enrolment is third numeric count.
numbers = [int(c.replace(',', '')) for c in sh[0] if c.replace(',', '').isdigit()]
assert numbers[:3] == [59179, 77188, 224186], numbers
teachers = json.loads((ROOT / 'shanghai_teachers2024_extracted.json').read_text())
assert teachers['year'] == 2024 and teachers['region'] == 'Shanghai'
observation('Shanghai', numbers[2], teachers['teachers'],
            [url('shanghai_students2024.html'), teachers['source_url']],
            'Shanghai municipality; regular senior-secondary schools only (excludes vocational); full-time teacher headcount not international FTE; teacher count manually transcribed from official indexed table; full teacher HTML unavailable',
            'observed_upper_secondary_manual_source_scope_conditional')
with (ROOT / 'observations.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
for row in rows:
    print(row['city'], row['students'], row['teachers'], round(row['value'], 8))
