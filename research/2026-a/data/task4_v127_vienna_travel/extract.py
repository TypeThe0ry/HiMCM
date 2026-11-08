"""Offline historical review of a locally held, non-redistributable source PDF.

Only derived aggregate counts, metadata and audits are written. No primary-model
observation is produced. Supply the original privately with --source-pdf.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPECTED = 'ac650df634fea8e0f5b4bfceae84065f61f9ec69d9af2e2e33fd7d6d2760a814'
URL = 'https://www.statistik.at/fileadmin/publications/Volkszaehlung_2001__Schueler_und_Studenten.pdf'
STAGES = ['Berufsbildende mittlere Schule', 'AHS-Oberstufe', 'Berufsbildende höhere Schule']
LABELS = ['1-5', '6-10', '11-15', '16-30', '31-45', '46-60', '61+']
MANUAL = [
    [6680, 6479, 83, 252, 467, 2416, 1797, 1003, 461],
    [18930, 18604, 1056, 2287, 2908, 8009, 2900, 1005, 439],
    [15865, 15521, 179, 546, 1091, 6016, 4484, 2254, 951]]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integers(text):
    return [0 if x == '-' else int(x) for x in re.findall(r'\d+|-', text)]


def time_row(block, stage):
    match = re.search(r'^\s*'+re.escape(stage)+r'\s+(.*?)\s*$', block, re.M)
    assert match, stage
    values = integers(match.group(1))
    assert len(values) == 9 and sum(values[2:]) == values[1]
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-pdf', type=Path, required=True)
    args = parser.parse_args()
    assert sha(args.source_pdf) == EXPECTED
    protected = [ROOT/'data/task4_v117_team_intake/city_indicators.csv',
                 ROOT/'design/task4_user_current_model.json']
    before = {str(p.relative_to(ROOT)): sha(p) for p in protected}
    full_text = subprocess.check_output(['pdftotext', '-layout', '-enc', 'UTF-8',
                                         str(args.source_pdf), '-'], text=True)
    pages = full_text.split('\f')
    assert len(pages) >= 201
    # Definitions: reference date, resident students, school-type split, employed
    # students answering work travel, and official reconstruction/imputation.
    assert '15. Mai 2001' in pages[27]
    assert 'Berufspendler und nicht als Schülerpendler' in pages[27]
    assert 'Unter- und Ober-' in pages[27]
    assert 'durchschnittliche Dauer des täglichen Hinwegs' in pages[29]
    assert 'rekonstru-' in pages[29] and 'aufgeschätzt' in pages[29]
    assert 'Wiener Gemeindebezirke wie Gemeinden' in pages[29]
    city_time = re.split(r'^\s*9 Wien\s*$', pages[182], flags=re.M)[1].split('901 Wien')[0]
    city_mode = re.split(r'^\s*9 Wien\s*$', pages[183], flags=re.M)[1].split('901 Wien')[0]
    stage_values = np.array([time_row(city_time, stage) for stage in STAGES])
    np.testing.assert_array_equal(stage_values, MANUAL)
    full_student_block = re.split(r'^\s*Wien\s*$', pages[46], flags=re.M)[1]
    total_line = re.search(r'^\s*Insgesamt\s+(.*?)\s*$', full_student_block, re.M).group(1)
    totals = integers(total_line)
    assert len(totals) == 12 and totals[0] == 222968 and sum(totals[1:]) == totals[0]
    denominators = np.array(totals[6:9])
    np.testing.assert_array_equal(denominators, [6929, 19373, 16472])

    # Independent geography/arithmetic check across all23 resident districts.
    district_sum = np.zeros((3, 9), dtype=int)
    districts = []
    for page in [183, 185, 187, 189, 191]:
        parts = re.split(r'^\s*(9\d{2})\s+Wien[^\n]*\n', pages[page-1], flags=re.M)
        for k in range(1, len(parts), 2):
            code, block = parts[k:k+2]
            districts.append(code)
            for s, stage in enumerate(STAGES):
                district_sum[s] += time_row(block, stage)
    assert districts == [str(x) for x in range(901, 924)]
    np.testing.assert_array_equal(district_sum, stage_values)

    counts = stage_values[:, 2:]
    unknown = denominators-counts.sum(1)
    rows = []
    for k, stage in enumerate(STAGES):
        mode_line = re.search(r'^\s*(.*?)\s+'+re.escape(stage)+r'\s*$', city_mode, re.M).group(1)
        modes = integers(mode_line)
        assert len(modes) == 11 and sum(modes[:9]) == stage_values[k, 1]
        changing, nondaily = modes[9:]
        assert stage_values[k, 0] == stage_values[k, 1]+changing+nondaily
        unrepresented = int(denominators[k]-stage_values[k, 0])
        assert unknown[k] == changing+nondaily+unrepresented
        row = dict(school_type=stage, full_resident_students=int(denominators[k]),
            table10_students=int(stage_values[k, 0]), daily_duration_students=int(stage_values[k, 1]),
            changing_destination_students=changing, non_daily_students=nondaily,
            not_represented_in_table10=unrepresented, total_unidentified_duration_students=int(unknown[k]),
            table1_pdf_page=47, table1_printed_page=48,
            time_pdf_page=183, time_printed_page=184, mode_pdf_page=184, mode_printed_page=185)
        row.update({'count_'+label.replace('+', 'plus'): int(counts[k, j]) for j, label in enumerate(LABELS)})
        rows.append(row)
    assert int(denominators.sum()) == 42774 and int(counts.sum()) == 40604 and int(unknown.sum()) == 2170
    with (HERE/'stage_counts.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

    results = {}
    high_minutes = np.array([5, 10, 15, 30, 45, 60, np.inf])
    for rule, low_minutes in [
        ('conservative_continuous_closure', np.array([0, 5, 10, 15, 30, 45, 60])),
        ('literal_published_integer_classes', np.array([1, 6, 11, 16, 31, 46, 61]))]:
        lower = counts @ np.exp(-high_minutes/30)/denominators
        upper = (counts @ np.exp(-low_minutes/30)+unknown)/denominators
        stage_results = [dict(school_type=stage, lower=float(lower[k]), upper=float(upper[k]),
                              denominator=int(denominators[k]), unknown_duration_mass=int(unknown[k]))
                         for k, stage in enumerate(STAGES)]
        pooled = [float(np.dot(lower, denominators)/denominators.sum()),
                  float(np.dot(upper, denominators)/denominators.sum())]
        results[rule] = dict(lower_minutes=low_minutes.tolist(),
            upper_minutes=[5, 10, 15, 30, 45, 60, None], tail_upper='infinite; utility lower0',
            stages=stage_results, pooled_full_schooltype_enrolment_bounds=pooled,
            unknown_stage_mixture_hull=[float(lower.min()), float(upper.max())])
    bounds = dict(city='Vienna', census_date='2001-05-15', publication_year=2005,
        admission_status='historical_case_only_not_current16', primary_admissions=0,
        default_historical_rule='conservative_continuous_closure', utility='exp(-reported_outward_minutes/30)',
        full_selected_schooltype_denominator=42774, daily_binned_mass=40604, unidentified_duration_mass=2170,
        rules=results, strict_current_or_unmodelled_source_editing_error_bounds=[0, 1],
        interpretation='Bounds condition on the published2001 edited census cells and selected schooltypes, not raw unedited journeys or2025/26 residents; no sampling confidence or error calibration is claimed.',
        imputation='Official definitions reconstruct/impute missing times; the number and quality of such edits are not identified by these aggregates. They are not an independently quantifiable unknown-mass count.',
        schooltype_scope='BMS, AHS upper stage and BHS only; includes their full-age resident enrolments, not exact14-18 and not every secondary school setting.',
        mixing='Pooled arm uses known all-age selected-schooltype proportions. Hull leaves the three-schooltype mixture unspecified; neither identifies an exact-age cohort.')
    (HERE/'historical_bounds.json').write_text(json.dumps(bounds, ensure_ascii=False, indent=2)+'\n')
    (HERE/'observations.json').write_text('[]\n')
    manifest = dict(provider='Statistics Austria', publication='Volkszählung2001: Schüler und Studenten',
        source_url=URL, source_sha256=EXPECTED, census_date='2001-05-15', publication_year=2005,
        source_pdf_not_redistributed=True, source_pages_or_images_not_committed=True,
        locators=dict(table1='PDF47/printed48, Vienna total row', table10_time='PDF183/printed184,9Wien',
                      table10_modes='PDF184/printed185,9Wien',
                      definitions='PDF28/printed29 andPDF30/printed31',
                      district_crosscheck='PDF183,185,187,189,191;Vienna districts901-923'),
        visual_review_pdf_pages=[47, 183, 184, 30],
        representation='Only selected factual derived counts, mathematical bounds and paraphrased scope checks saved; full source remains a private local review copy.',
        admission_status='historical_case_only_not_current16', primary_admissions=0)
    (HERE/'source_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    for path, expected in before.items():
        assert sha(ROOT/path) == expected
    audit = dict(status='pass', original_source_sha256=EXPECTED,
        selected_stage_city_rows_visually_checked=True, district_count=23,
        all23_district_stage_vectors_equal_city_aggregate=True,
        table1_full_denominator_42774=True, known_bins_plus_unknown_equal_full_denominator=True,
        daily_bin_totals_40604=True, unknown_mass_2170=True,
        employed_or_other_unrepresented_students_not_silently_dropped=True,
        changing_destination_and_non_daily_not_assigned_zero_duration=True,
        open_tail_not_finitely_capped=True, no_midpoint_or_random_imputation=True,
        official_source_imputation_not_mislabelled_raw_observation=True,
        admission_status='historical_case_only_not_current16', primary_admissions=0,
        original_CSV_registry_unchanged=True,
        derived_sha256={name: sha(HERE/name) for name in ['stage_counts.csv', 'historical_bounds.json', 'observations.json', 'source_manifest.json']})
    (HERE/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps(dict(admission_status=audit['admission_status'], primary_admissions=0,
                         historical_default=results['conservative_continuous_closure']), indent=2))


if __name__ == '__main__':
    main()
