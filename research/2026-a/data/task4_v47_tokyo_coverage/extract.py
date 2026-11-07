"""Tokyo integrated secondary upper-course coverage and unknown teacher allocation."""
import csv
import hashlib
import json
from pathlib import Path

P = Path(__file__).resolve().parent


def rows(name):
    with (P / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def unique_total(data, year, kind):
    selected = [r for r in data if r['種別'] == kind and r['地域階層'] == '0'
                and r['地域'] == '総数' and r['西暦（年度）'] == str(year)]
    assert len(selected) == 1
    return selected[0]


def extract():
    for r in json.loads((P / 'manifest.json').read_text()):
        b = (P / r['file']).read_bytes()
        assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256']
    baseline = unique_total(rows('../task4_v46_tokyo/gk25qv0711.csv'), 2025, '総数（国・公・私立）')
    records = rows('gk25qv0911.csv')
    total = unique_total(records, 2025, '総数（国・公立）')
    ownership = [unique_total(records, 2025, k) for k in ['国立', '公立']]
    for name in ['学校数（校）', '前期課程／生徒数（人）', '後期課程／生徒数（人）', '教員数（本務者）（人）']:
        assert int(total[name]) == sum(int(r[name]) for r in ownership)
    for r in [total] + ownership:
        for stage in ['前期課程', '後期課程']:
            n = int(r[stage + '／生徒数（人）'])
            assert n == int(r[stage + '／生徒数／男（人）']) + int(r[stage + '／生徒数／女（人）'])
        assert int(r['後期課程／生徒数（人）']) == int(r['後期課程／生徒数／全日制（人）'])
        assert int(r['後期課程／生徒数（人）']) == sum(int(r[f'後期課程／生徒数／全日制／{g}学年（人）']) for g in (1, 2, 3))
        assert r['後期課程／生徒数／定時制（人）'] == '-'
        assert int(r['教員数（本務者）（人）']) == int(r['教員数（本務者）／男（人）']) + int(r['教員数（本務者）／女（人）'])
    raw = (P / 'gk25qv0911.csv').read_text(encoding='utf-8-sig')
    assert '私立に中等教育学校はない' in raw
    students, teachers = int(baseline['生徒数（人）']), int(baseline['教員数（本務者）（人）'])
    extra_students = int(total['後期課程／生徒数（人）'])
    pool = int(total['教員数（本務者）（人）'])
    expanded = students + extra_students
    utility = lambda teacher_count: 15 * teacher_count / (expanded + 15 * teacher_count)
    correspondence = unique_total(rows('gk25qv0811.csv'), 2025, '総数（公・私立）')
    return dict(provider='Tokyo Metropolitan Government School Basic Survey 2025',
        date='2025-05-01', geography='Tokyo Metropolis',
        baseline_students=students, baseline_main_duty_teachers=teachers,
        integrated_schools=int(total['学校数（校）']),
        integrated_lower_course_students=int(total['前期課程／生徒数（人）']),
        added_upper_course_students=extra_students,
        integrated_all_course_main_duty_teachers=pool,
        ownership=[dict(category=r['種別'], schools=int(r['学校数（校）']),
                        upper_course_students=int(r['後期課程／生徒数（人）']),
                        all_course_main_duty_teachers=int(r['教員数（本務者）（人）'])) for r in ownership],
        expanded_students=expanded,
        added_upper_course_teacher_interval=[0, pool],
        expanded_teacher_interval=[teachers, teachers + pool],
        expanded_utility_interval=[utility(teachers), utility(teachers + pool)],
        baseline_utility=15 * teachers / (students + 15 * teachers),
        teacher_definition='Main-duty school-assigned persons, not FTE; upper-course participation of the integrated-school pool is unreported.',
        coverage='Full/part-time high-school courses plus integrated secondary upper courses; does not claim all upper-secondary programmes.',
        exclusions=['correspondence high-school courses', 'special-needs upper-secondary departments', 'specialized-training high-school courses'],
        correspondence_audit=dict(students=int(correspondence['生徒数（人）']),
            main_duty_teachers=int(correspondence['教員数（本務者）（人）']),
            independent_schools=int(correspondence['学校数／独立校（校）']),
            colocated_schools=int(correspondence['学校数／併置校（校）']),
            admitted=False, reason='Different course and distance-learning population; co-location and teacher attribution require separate review.'))


if __name__ == '__main__':
    result = extract()
    (P / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
