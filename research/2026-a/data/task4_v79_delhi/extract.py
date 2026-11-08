"""Verify Delhi school exports against age tables and official UDISE totals."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import pandas as pd

HERE = Path(__file__).resolve().parent
GRADES = ['c11_b', 'c11_g', 'c12_b', 'c12_g']


def extract():
    for entry in json.loads((HERE / 'manifest.json').read_text())['files']:
        raw = (HERE / entry['file']).read_bytes()
        assert len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256']
    e = pd.read_csv(HERE / '07_enr1.csv')
    a = pd.read_csv(HERE / '07_enr2.csv')
    t = pd.read_csv(HERE / '07_tch.csv').set_index('pseudocode')
    profile = pd.read_csv(HERE / '07_prof1.csv').set_index('pseudocode')
    assert t.index.is_unique and profile.index.is_unique
    for frame in (e, a, t):
        assert not frame.isna().any().any()
        assert (frame.select_dtypes('number') >= 0).all().all()
    for frame in (e, a):
        assert not frame.duplicated(['pseudocode', 'item_group', 'item_id']).any()
    assert set(a.item_group) == {8}
    social = e[e.item_group == 1]
    assert set(social.item_id) == {1, 2, 3, 4}
    cols = [c for c in social if c.startswith('c')]
    pupils = social.groupby('pseudocode')[cols].sum().sort_index()
    pd.testing.assert_frame_equal(pupils, a.groupby('pseudocode')[cols].sum().sort_index())
    assert set(pupils.index) == set(t.index) == set(profile.index)
    assert set(profile.state) == {'DELHI'}
    classes = [c for c in t if c.startswith(('class_taught_', 'class_taugt_'))]
    assert len(classes) == 9 and (t[classes].sum(axis=1) == t.total_tch).all()
    assert (t[['regular', 'contract', 'part_time']].sum(axis=1) == t.total_tch).all()
    hs = pupils[GRADES].sum(axis=1)
    assert (profile.loc[hs[hs > 0].index, 'highclass'] >= 12).all()
    zero = hs == 0
    dedicated = int(t.class_taught_hsec_only.sum())
    shared = int(t.class_taught_sec_hsec.sum())
    zero_dedicated = int(t.loc[zero, 'class_taught_hsec_only'].sum())
    zero_shared = int(t.loc[zero, 'class_taught_sec_hsec'].sum())
    n = int(hs.sum())
    # Independent original publication corroborates export aggregate counts.
    official = HERE.parent / 'task4_v34_education'
    entry = next(x for x in json.loads((official / 'manifest.json').read_text()) if x['file'] == 'udise_2024_25.pdf')
    raw = (official / entry['file']).read_bytes()
    assert len(raw) == entry['bytes'] and hashlib.sha256(raw).hexdigest() == entry['sha256']
    pdf = subprocess.check_output(['pdftotext', '-layout', str(official / entry['file']), '-'], text=True).split('\f')
    def row(page, heading):
        assert heading in pdf[page-1]
        line = next(x for x in pdf[page-1].splitlines() if re.match(r'^\s*Delhi\s', x))
        return [int(x) for x in re.findall(r'\b\d+\b', line)]
    teacher_row = row(58, 'Table 4.7:')
    pupil_row = row(85, 'Table 5.1:')
    assert (dedicated, shared, n) == (teacher_row[-1], teacher_row[-2], pupil_row[-1])
    assert int(t.total_tch.sum()) == teacher_row[0]
    assert int(pupils.sum().sum()) == pupil_row[0]
    assert re.search(r'Delhi\s+5556\s+4491032\s+161958', pdf[30])
    assert (len(t), int(pupils.sum().sum()), int(t.total_tch.sum())) == (5556,4491032,161958)
    lower, upper = dedicated-zero_dedicated, dedicated+shared
    assert (n, dedicated, shared, zero_dedicated, zero_shared) == (603437,26766,3420,105,14)
    return dict(reference_year='2024-25', geography='Delhi NCT; all DELHI state school profiles',
        population='All ages enrolled in XI-XII; school location, not residence',
        schools=len(t), schools_with_hs_pupils=int((hs>0).sum()),
        zero_hs_schools_with_hs_teachers=int((zero & ((t.class_taught_hsec_only+t.class_taught_sec_hsec)>0)).sum()),
        students_upper_secondary=n, students_age14_18=int(a[a.item_id.between(14,18)][GRADES].sum().sum()),
        reported_dedicated_teachers=dedicated, shared_teachers=shared,
        zero_hs_dedicated_teachers=zero_dedicated, zero_hs_shared_teachers=zero_shared,
        teacher_lower=lower, teacher_upper=upper,
        utility_lower=15*lower/(n+15*lower), utility_upper=15*upper/(n+15*upper),
        dedicated_allocation_utility_lower=15*dedicated/(n+15*dedicated),
        official_aggregate_counts_match=True, official_pdf_sha256=entry['sha256'],
        all_grade_age_social_cells_match=True, teacher_class_partition_verified=True,
        mirror_official_byte_identity_verified=False,
        interpretation='Conditional nominal teaching-resource allocation; not FTE, instructional hours or empirical confidence interval')


if __name__ == '__main__':
    result = extract()
    (HERE / 'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
