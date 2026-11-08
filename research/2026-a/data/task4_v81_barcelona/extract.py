"""Verify two official municipal tabulations; do not infer a complete HS teacher pool."""
import hashlib
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

def extract():
    for record in json.loads((HERE / 'manifest.json').read_text()):
        raw = (HERE / record['file']).read_bytes()
        assert len(raw) == record['bytes']
        assert hashlib.sha256(raw).hexdigest() == record['sha256']
    reports = {}
    for year, prefix, student_file in [('2024/2025', 'teachers2024_', 'batx2024_students.csv'),
                                       ('2025/2026', 'teachers_', 'batx_students.csv')]:
        frames = []
        for suffix in ['specialty.csv', 'dedication.csv']:
            f = pd.read_csv(HERE / (prefix + suffix), sep=';', encoding='utf-8-sig')
            assert set(f.Curs) == {year}
            assert f['Personal docent'].notna().all() and (f['Personal docent'] >= 0).all()
            f = f[f['Codi municipi'] == 8019]
            assert len(f) and set(f.Municipi) == {'BARCELONA'}
            frames.append(f)
        keys = ['Codi districte', 'Naturalesa', 'Sexe']
        # Different views of the same pool; compare, never add the views together.
        a, b = [f.groupby(keys)['Personal docent'].sum().sort_index() for f in frames]
        pd.testing.assert_series_equal(a, b)
        students = pd.read_csv(HERE / student_file, sep=';', encoding='utf-8-sig')
        assert set(students.Curs) == {year}
        assert students['Alumnes matriculats'].notna().all()
        assert (students['Alumnes matriculats'] >= 0).all()
        students = students[students['Codi municipi'] == 8019]
        assert set(students.Municipi) == {'BARCELONA'}
        assert set(students.Estudis) == {'BATXILLERAT'}
        assert set(students.Nivell) == {1, 2}
        n = int(students['Alumnes matriculats'].sum())
        t = int(frames[0]['Personal docent'].sum())
        expected = {'2024/2025': (23699,11238), '2025/2026': (23149,11219)}
        assert (n,t) == expected[year]
        reports[year] = dict(
            batxillerat_students=n,
            batx_students_by_ownership={k:int(v) for k,v in students.groupby('Naturalesa')['Alumnes matriculats'].sum().items()},
            secondary_teacher_pool=t,
            teacher_pool_by_ownership={k:int(v) for k,v in frames[0].groupby('Naturalesa')['Personal docent'].sum().items()},
            teacher_pool_by_dedication={k:int(v) for k,v in frames[1].groupby('Dedicació')['Personal docent'].sum().items()},
            crossview_municipal_district_ownership_sex_match=True,
            observed_student_rows=len(students),
            observed_teacher_rows=[len(f) for f in frames])
    return dict(city='Barcelona',municipality_code='08019',geography='School municipality, not province or student residence',
                periods=reports,main_admitted=False,teacher_stage_allocation_identified=False,
                complete_upper_secondary_teacher_pool_verified=False,
                interpretation='Batxillerat student counts and broader secondary teaching pool; no whole-upper-secondary PTR or bound admitted')

if __name__ == '__main__':
    result=extract()
    (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
