"""Verify new MOE sources; do not transplant their counts into Census travel bins."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for item in json.loads((ROOT / 'manifest.json').read_text()):
    raw = (ROOT / item['file']).read_bytes()
    assert len(raw) == item['bytes'], item['file']
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['file']
result = json.loads((ROOT / 'moe_level_age_api.json').read_text())['result']
records = result['records']
assert len(records) == result['total'] == 541
assert len({r['_id'] for r in records}) == len(records)
rows = [r for r in records if r['YEAR'] == '2020' and r['SEX'] == 'MF']
assert len(rows) == 30
assert len({(r['LEVEL'], r['AGE']) for r in rows}) == len(rows)
by_grade = {level: sum(int(r['ENROLMENT']) for r in rows if r['LEVEL'] == level)
            for level in sorted({r['LEVEL'] for r in rows})}
assert list(by_grade.values()) == [40154, 39719, 39909, 38809, 3480]
upper = [r for r in rows if r['LEVEL'] in ['Secondary 3', 'Secondary 4', 'Secondary 5']]
jan_14_17 = sum(int(r['ENROLMENT']) for r in upper if r['AGE'] in ['14 YRS','15 YRS','16 YRS','17 YRS'])
jan_14_18 = sum(int(r['ENROLMENT']) for r in upper if r['AGE'] in ['14 YRS','15 YRS','16 YRS','17 YRS','18 YRS'])
assert jan_14_17 == 82000 and jan_14_18 == 82165
metadata = (ROOT / 'moe_level_age.html').read_text()
assert 'Age is as at the start of the year.' in metadata
assert '2-year work-study programme after completing ISC' in metadata
reply = (ROOT / 'moe_international_reply.html').read_text()
assert 'less than 5%' in reply and 'in 2019 and 2020' in reply
summary = {
    'year': 2020,
    'observed_population': 'MOE secondary school enrolment, both sexes; citizenship not tabulated',
    'age_reference': 'start of year; enrolment reference date not established',
    'by_grade': by_grade,
    'secondary_total': sum(by_grade.values()),
    'secondary_3_to_5_total': sum(int(r['ENROLMENT']) for r in upper),
    'secondary_3_to_5_age_14_to_17_at_start_of_year': jan_14_17,
    'secondary_3_to_5_age_14_to_18_at_start_of_year': jan_14_18,
    'upper_grade_age_rows': upper,
    'international_student_evidence': 'MOE 11 May 2021 reply: less than 5% in primary schools, secondary schools and Junior Colleges in 2019 and 2020; no grade-age cross-tab or Census-date reconciliation',
    'admitted_to_model': False,
    'target_mass_lower_bound_identified': False,
    'revised_travel_interval': [0, 1],
    'blockers': [
        'Start-of-year ages and unspecified enrolment date do not establish membership on the Census reference date.',
        'No age-grade-citizenship joint tabulation; reply does not establish a common resident population with Census.',
        'MOE coverage includes ISC/work-study; ordinary ISCED-3 course membership cannot be separated in this table.',
        'Census travel excludes home learners and people overseas at least six months; these exclusions are not bounded for MOE subgroup.',
    ],
}
(ROOT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in summary.items() if k != 'upper_grade_age_rows'}, ensure_ascii=False, indent=2))
