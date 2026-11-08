"""Reconcile mirrored UDISE school/grade counts and retain teacher allocation unknowns."""
import hashlib
import json
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
GRADES = ['c11_b', 'c11_g', 'c12_b', 'c12_g']

def extract():
    manifest = json.loads((HERE / 'manifest.json').read_text())
    for entry in manifest['files']:
        raw = (HERE / entry['file']).read_bytes()
        assert len(raw) == entry['bytes']
        assert hashlib.sha256(raw).hexdigest() == entry['sha256']
    reports, ids = {}, []
    for district in ['2723', '2722']:
        e = pd.read_csv(HERE / f'{district}_enr1.csv')
        a = pd.read_csv(HERE / f'{district}_enr2.csv')
        t = pd.read_csv(HERE / f'{district}_tch.csv').set_index('pseudocode')
        assert t.index.is_unique
        assert not e.duplicated(['pseudocode', 'item_group', 'item_id']).any()
        assert not a.duplicated(['pseudocode', 'item_group', 'item_id']).any()
        for frame in [e, a, t]:
            assert not frame.isna().any().any()
            assert (frame.select_dtypes('number') >= 0).all().all()
        assert set(a.item_group) == {8}
        social = e[e.item_group == 1]
        assert set(social.item_id) == {1, 2, 3, 4}
        n = social.groupby('pseudocode')[GRADES].sum().sort_index()
        ages = a.groupby('pseudocode')[GRADES].sum().sort_index()
        pd.testing.assert_frame_equal(n, ages)
        assert set(n.index) == set(t.index)
        taught = [c for c in t if c.startswith(('class_taught_', 'class_taugt_'))]
        assert len(taught) == 9
        assert (t[taught].sum(axis=1) == t.total_tch).all()
        zero = n.sum(axis=1) == 0
        reports[district] = dict(
            schools=len(t), pupils=int(n.sum().sum()),
            pupils_14_18=int(a[a.item_id.between(14, 18)][GRADES].sum().sum()),
            pupils_by_grade_sex={k:int(v) for k,v in n.sum().items()},
            schools_with_hs_pupils=int((~zero).sum()),
            zero_hs_schools_with_hs_teachers=int((zero & ((t.class_taught_hsec_only+t.class_taught_sec_hsec)>0)).sum()),
            teachers_hs_only=int(t.class_taught_hsec_only.sum()),
            teachers_secondary_and_hs=int(t.class_taught_sec_hsec.sum()),
            hs_only_teachers_at_zero_hs_enrolment=int(t.loc[zero,'class_taught_hsec_only'].sum()),
            shared_teachers_at_zero_hs_enrolment=int(t.loc[zero,'class_taught_sec_hsec'].sum()),
            teacher_class_partition_verified=True, age_social_crosscheck_each_cell=True)
        ids.append(set(t.index))
    assert not ids[0] & ids[1]
    profile = pd.read_csv(HERE / '2723_prof1.csv')
    assert profile.pseudocode.is_unique and set(profile.pseudocode) == ids[0]
    assert set(profile.district) == {'MUMBAI II'}
    assert set(profile.lgd_urban_local_body_name) == {'Greater Mumbai_Municipal Corporations'}
    assert (profile.highclass <= 12).all()
    def total(k): return sum(r[k] for r in reports.values())
    n = total('pupils'); dedicated = total('teachers_hs_only')
    shared = total('teachers_secondary_and_hs')
    lower = dedicated - total('hs_only_teachers_at_zero_hs_enrolment')
    upper = dedicated + shared
    assert (n, dedicated, shared, lower, upper) == (280140,5887,967,5848,6854)
    out = dict(reference_year='2024-25', district_exports=reports,
        reported_geography='MUMBAI II export: all 1750 profiles in Greater Mumbai Municipal Corporations',
        mirror_official_byte_identity_verified=False,
        population='All ages enrolled in grades XI-XII; school location, not residence',
        pupils=n, students_upper_secondary=n, teacher_lower=lower, teacher_upper=upper,
        reported_dedicated_teachers=dedicated,
        utility_lower=15*lower/(n+15*lower), utility_upper=15*upper/(n+15*upper),
        reported_resource_utility_lower=15*dedicated/(n+15*dedicated),
        official_ratio_crosscheck=n/upper,
        interpretation='Conditional reported-school teaching-resource allocation; not FTE, staffing quality, sampling CI, or proof of complete independent-school coverage')
    return out

if __name__ == '__main__':
    result = extract()
    (HERE / 'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result,indent=2))
