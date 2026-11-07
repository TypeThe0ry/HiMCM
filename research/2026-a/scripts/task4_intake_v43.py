"""Audit suppressed LEA counts and recheck the canonical city ranking."""
import csv
import json
from task4_intake_v40 import run
from task4_v5_model import ROOT


def main():
    path = ROOT / 'data/task4_v43_phoenix_lea'
    with (path / 'maricopa_lea_membership_rows.csv').open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 227
    assert all(r['LEAID'] == '0403860' and r['SCHOOL_YEAR'] == '2024-2025'
               and r['ST_LEAID'] == 'AZ-4234' for r in rows)
    assert all(r['DMS_FLAG'] == 'Suppressed' and r['STUDENT_COUNT'] == ''
               for r in rows)
    audit = json.loads((path / 'summary.json').read_text())
    assert audit['matched_rows'] == len(rows)
    assert not audit['has_finite_school_upper_bound']
    run(folders=('task4_v43_phoenix_lea',),
        output='results/task4_v43_lea_audit',
        distinction='All 227 same-year LEA membership records are suppressed. '
        'No numerical district upper bound is identified. Phoenix education '
        'intervals and all canonical city inputs remain unchanged; the V42 '
        '1178-pupil snapshot scenario remains conditional.')


if __name__ == '__main__':
    main()
