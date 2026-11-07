"""Retain unspecified attendance and age as optional EMS membership.

This preserves V15's conditional completed-grade progression rule and broad
stage-99 treatment. It does not identify current grade directly.
"""
from collections import Counter
from pathlib import Path
from zipfile import ZipFile
import csv
import hashlib
import importlib.util
import io
import json

P = Path(__file__).resolve().parent
OLD = P.parent / 'task4_v15_mexico2020'
_spec = importlib.util.spec_from_file_location('v15_mexico_extract', OLD/'extract_commute.py')
v15 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v15)
SCOPES = ('age3_17', 'all_age3plus')


def stage_possible(row):
    """Original progression rule, without assuming attendance is known."""
    level, grade = row['NIVACAD'], row['ESCOLARI']
    if not level.isdigit() or not grade.isdigit():
        return False
    level, grade = int(level), int(grade)
    return (level == 99 or grade == 99 or (level == 3 and grade == 3)
            or (level in (4, 5, 7) and 0 <= grade < 3))


def additional_scope(row, scope):
    """Extra optional memberships omitted by V15; known nonattenders excluded."""
    age = int(row['EDAD'])
    if row['ASISTEN'] not in ('1', '9') or not stage_possible(row):
        return None
    if not (age == 999 or (3 <= age <= (17 if scope == 'age3_17' else 130))):
        return None
    if row['ASISTEN'] == '9':
        return 'unknown_attendance_unknown_age' if age == 999 else 'unknown_attendance_known_age'
    if age == 999 and scope == 'age3_17':
        return 'current_attender_unknown_age'
    # All-age V15 already includes classifiable or stage-99 current attenders.
    return None


def derive():
    for entry in json.loads((OLD/'manifest.json').read_text()):
        assert hashlib.sha256((OLD/entry['file']).read_bytes()).hexdigest() == entry['sha256']
    archived = json.loads((OLD/'commute_summary.json').read_text())
    groups = {s: {'known': Counter(), 'old_optional': Counter(), 'added_optional': Counter(),
                  'known_rows': 0, 'old_optional_rows': 0, 'added_optional_rows': 0,
                  'added_reasons_rows': Counter(), 'added_reasons_weight': Counter()}
              for s in SCOPES}
    attendance_rows, attendance_weight = Counter(), Counter()
    blank_ages, unknown_age_attenders = Counter(), Counter()
    additional_records = []
    ids = set()
    with ZipFile(OLD/'Censo2020_CA_cdmx_csv.zip') as z:
        for row in csv.DictReader(io.TextIOWrapper(z.open('Personas09.CSV'), encoding='utf-8-sig')):
            assert row['ENT'] == '09' and row['ID_PERSONA'] not in ids
            ids.add(row['ID_PERSONA'])
            weight, age = int(row['FACTOR']), int(row['EDAD'])
            assert weight > 0 and row['ASISTEN'] in ('', '1', '3', '9')
            attendance_rows[row['ASISTEN']] += 1
            attendance_weight[row['ASISTEN']] += weight
            if row['ASISTEN'] == '':
                blank_ages[str(age)] += 1
            if age == 999 and row['ASISTEN'] == '1':
                unknown_age_attenders[f"{row['NIVACAD']}:{row['ESCOLARI']}"] += weight
            added = []
            for scope in SCOPES:
                g = groups[scope]
                old_age_ok = scope == 'all_age3plus' or 3 <= age <= 17
                if old_age_ok and v15.reconstructed_ems(row):
                    g['known'][row['TIE_TRASLADO_ESCU']] += weight
                    g['known_rows'] += 1
                if old_age_ok and row['ASISTEN'] == '1' and (row['NIVACAD'] == '99' or row['ESCOLARI'] == '99'):
                    g['old_optional'][row['TIE_TRASLADO_ESCU']] += weight
                    g['old_optional_rows'] += 1
                reason = additional_scope(row, scope)
                if reason:
                    g['added_optional'][row['TIE_TRASLADO_ESCU']] += weight
                    g['added_optional_rows'] += 1
                    g['added_reasons_rows'][reason] += 1
                    g['added_reasons_weight'][reason] += weight
                    added.append(scope)
            if added:
                additional_records.append({k: row[k] for k in
                    ['ID_PERSONA', 'EDAD', 'ASISTEN', 'NIVACAD', 'ESCOLARI', 'TIE_TRASLADO_ESCU', 'FACTOR']} |
                    {'optional_scopes': '|'.join(added)})
    assert len(ids) == archived['person_rows']
    assert sum(attendance_weight.values()) == archived['weighted_private_household_population']
    assert set(blank_ages) <= {'0', '1', '2'}
    result = dict(year=2020, main_admitted=False, current_stage_directly_observed=False,
                  stage_assumption=archived['stage_definition'],
                  optional_stage_rule='Original broad NIVACAD99 or ESCOLARI99 retained; can include known incompatible levels with unspecified grade. Conservative optional set, not established EMS attendance.',
                  age_rule='Age 999 is optional for both age scopes; age 0-2 excluded. Known ages retained as recorded.',
                  new_downloads=0, person_rows=len(ids),
                  attendance_rows=dict(attendance_rows), attendance_weight=dict(attendance_weight),
                  blank_attendance_age_counts=dict(blank_ages),
                  current_attender_unknown_age_stage_weights=dict(unknown_age_attenders), scopes={})
    for scope, g in groups.items():
        old = archived['scopes'][scope]
        assert dict(g['known']) == old['weighted_time_bins']
        assert dict(g['old_optional']) == old['optional_stage_time_bins']
        assert g['known_rows'] == old['sample_rows']
        old_lo, old_hi = v15.optional_membership(g['known'], g['old_optional'])
        assert abs(old_lo-old['membership_utility_lower']) < 1e-14
        assert abs(old_hi-old['membership_utility_upper']) < 1e-14
        optional = g['old_optional'] + g['added_optional']
        lo, hi = v15.optional_membership(g['known'], optional)
        assert lo <= old_lo+1e-14 and hi >= old_hi-1e-14
        result['scopes'][scope] = dict(
            known_sample_rows=g['known_rows'], known_weight=sum(g['known'].values()),
            known_time_bins=dict(g['known']), old_optional_sample_rows=g['old_optional_rows'],
            old_optional_weight=sum(g['old_optional'].values()), old_optional_time_bins=dict(g['old_optional']),
            added_optional_sample_rows=g['added_optional_rows'], added_optional_weight=sum(g['added_optional'].values()),
            added_optional_time_bins=dict(g['added_optional']), added_reasons_rows=dict(g['added_reasons_rows']),
            added_reasons_weight=dict(g['added_reasons_weight']), corrected_optional_time_bins=dict(optional),
            before_lower=old_lo, before_upper=old_hi, utility_lower=lo, utility_upper=hi,
            utility_width_increase=(hi-lo)-(old_hi-old_lo))
    sources = ['Censo2020_CA_cdmx_csv.zip', 'extract_commute.py', 'commute_summary.json', 'school_attendance_metadata.html']
    result['sources'] = [dict(path='../task4_v15_mexico2020/'+name,
                              sha256=hashlib.sha256((OLD/name).read_bytes()).hexdigest()) for name in sources]
    return result, additional_records


def main():
    result, records = derive()
    (P/'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    with (P/'added_optional_records.csv').open('w', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    print(json.dumps(result['scopes'], indent=2))

if __name__ == '__main__':
    main()
