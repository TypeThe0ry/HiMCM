"""Verify official originals and extract the Shanghai programme/school-scope audit."""
import hashlib
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
records = json.loads((ROOT / 'retrieval.json').read_text())
texts = {}
for record in records:
    if record['status'] != 200:
        continue
    raw = (ROOT / record['file']).read_bytes()
    assert len(raw) == record['bytes']
    assert hashlib.sha256(raw).hexdigest() == record['sha256']
    texts[record['file']] = re.sub(r'\s+', '', BeautifulSoup(raw, 'html.parser').get_text())

local = texts['changning2025_bulletin.html']
assert '职校117164.1' in local, 'Expected table: 1 school, 1716 students, growth 4.1%'
assert '职校在校学生数包括职校生和成人中专学生数' in local
admission = texts['adult_admission2025.html']
start = admission.index('本市各全日制普通中等职业学校')
end = admission.index('二、招生对象', start)
assert '包括中等专业学校、职业学校、技工学校' in admission[start:end]
assert '方可开展成人中等职业教育' in admission[start:end]
audit = {
    'year': 2025,
    'status': 'programme_scope_unresolved_no_model_update',
    'new_admitted_city_counts': 0,
    'model_cells_changed': 0,
    'changning_district_only': {
        'vocational_schools': 1,
        'vocational_students_including_adult_programmes': 1716,
        'adult_students_separately': None,
        'note': '职校在校学生数包括职校生和成人中专学生数',
        'not_a_city_total': True,
    },
    'ordinary_vocational_schools_can_offer_adult_programmes': True,
    'admissions_rule_excerpt': admission[start:end],
    'shanghai_2025_adult_secondary_student_stock': None,
    'deducting_standalone_adult_school_teachers_sufficient': False,
    'does_not_establish_city_bulletin_includes_adult_students': True,
    'prior_v54_numbers_not_reestimated': {
        'ordinary_high_students': 235542,
        'ordinary_high_fulltime_teachers_headcount': 23999,
        'vocational_total_teachers': 7273,
        'adult_school_teachers': 59,
        'conditional_nonadult_institution_teachers': 7214,
        'rounded_vocational_students': 109000,
    },
    'required_next_evidence': [
        '2025 city vocational pupil stock split by regular/adult programme with coverage definitions',
        '2025 teacher allocation to the same regular upper-secondary programme population',
    ],
    'verified_originals': [r for r in records if r['status'] == 200],
}
(ROOT / 'audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
print('PASS: two official original hashes, district table, adult-programme note, admissions scope; no model update')
