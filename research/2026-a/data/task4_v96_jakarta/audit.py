"""Audit school selection, completed-questionnaire losses, and scope.

No design weights are inferred from matching school-stage proportions.
The collection-set envelope counts records, not deduplicated city pupils.
"""
import csv
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

P = Path(__file__).resolve().parent


def main():
    for name, digest in json.loads((P / 'reused_sources.json').read_text()).items():
        assert hashlib.sha256((P / name).read_bytes()).hexdigest() == digest
    prior = P.parent / 'task4_v95_jakarta'
    method = PdfReader(prior / 'thesis_chapter3.pdf')
    results = PdfReader(prior / 'thesis_chapter5.pdf')
    method38 = ' '.join(method.pages[6].extract_text().split())
    assert 'Pemilihan sekolah berdasarkan' in method38
    assert 'jumlah dan proporsi sampel' in method38
    assert 'memilih mereka secara acak' in method38
    frame36 = method.pages[4].extract_text()
    for token in ('24,429', '9,223', '11,221', '44,873'):
        assert token in frame36
    text = results.pages[2].extract_text()
    rx = re.compile(r'(?m)^\s*(?:\d+\s+)?(SMP|SMA|SMK) Negeri (\d+)\s+(.*?)\s+(\d+)\s+(\d+)\s+(\d+\.\d+)%\s*$')
    rows = []
    for stage, num, context, n, v, pct in rx.findall(text):
        rows.append(dict(stage=stage, school=f'{stage} Negeri {num}',
            collection_context=context.strip(), completed=int(n), valid=int(v),
            invalid=int(n)-int(v), published_valid_percent=pct))
    assert len(rows) == 24 and len({r['school'] for r in rows}) == 23
    assert sum(r['completed'] for r in rows) == 750
    assert sum(r['valid'] for r in rows) == 573
    assert all(0 <= r['valid'] <= r['completed'] for r in rows)
    assert all(abs(float(r['published_valid_percent'])-100*r['valid']/r['completed']) < .0051 for r in rows)
    with (P / 'collection_rows.csv').open() as f:
        saved = list(csv.DictReader(f))
    assert len(saved) == len(rows)
    for actual, expected in zip(saved, rows):
        assert actual == {k: str(v) for k, v in expected.items()}
    frames = {'SMP': (36, 24429), 'SMA': (13, 9223), 'SMK': (14, 11221)}
    stages = {}
    for stage, (schools, pupils) in frames.items():
        subset = [r for r in rows if r['stage'] == stage]
        completed = sum(r['completed'] for r in subset)
        valid = sum(r['valid'] for r in subset)
        stages[stage] = dict(quoted_2022_frame_schools=schools,
            quoted_2022_frame_pupils=pupils,
            observed_schools=len({r['school'] for r in subset}),
            collection_rows=len(subset), completed_questionnaires=completed,
            valid_questionnaires=valid, unusable_questionnaires=completed-valid,
            valid_fraction_of_completed=valid/completed)
    assert [(stages[k]['completed_questionnaires'], stages[k]['valid_questionnaires'])
            for k in ('SMP', 'SMA', 'SMK')] == [(390, 311), (124, 119), (236, 143)]
    valid = stages['SMA']['valid_questionnaires'] + stages['SMK']['valid_questionnaires']
    completed = stages['SMA']['completed_questionnaires'] + stages['SMK']['completed_questionnaires']
    missing = completed-valid
    prior_bounds = json.loads((prior / 'summary.json').read_text())['mode_stratified_school_type_bounds']
    bound = [valid*prior_bounds[0]/completed,
             (valid*prior_bounds[1]+missing)/completed]
    result = dict(main_admitted=False, quoted_frame_year=2022,
        stages=stages, total_collection_rows=24, distinct_sampled_schools=23,
        total_completed=750, total_valid=573, total_unusable=177,
        published_total_valid_percent=76.65, recomputed_total_valid_percent=100*573/750,
        upper_secondary_collection=dict(completed=completed, valid=valid, unusable=missing,
            valid_record_bounds=prior_bounds, all_collected_record_bounds=bound,
            interpretation='Conditional completed-questionnaire record-set envelope; '
            '98 unusable upper-secondary records retain [0,1] utility. '
            'Not all invited pupils, deduplicated pupils, age14-18, school-frame or city inference.'),
        selection=dict(schools='Selected to attain stage sample sizes/proportions and geographic representation',
            pupils='Method states schools chose pupils randomly; selection probabilities and frame draw details unreported',
            school_inclusion_probabilities_identified=False, design_weights_identified=False,
            invited_denominator_identified=False, unusable_record_reason_identified=False,
            person_deduplication_verified=False, resident_city_membership_identified=False),
        source_pages=dict(frame='chapter3 printed36', selection='chapter3 printed38',
            population_sample_comparison='chapter5 printed58', collections='chapter5 printed59',
            district_representation='chapter5 printed62', questionnaire='appendix printed149-152'))
    (P / 'summary.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
