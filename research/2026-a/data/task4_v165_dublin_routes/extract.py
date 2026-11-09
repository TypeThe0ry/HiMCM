"""Offline scope audit of two official Dublin teacher-data discovery routes."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name):
    return json.loads((HERE / name).read_text())


def dimensions(data):
    return {name: dict(label=data['dimension'][name]['label'],
                      category_labels=data['dimension'][name]['category']['label'])
            for name in data['id']}


def main():
    receipt = load('retrieval.json')
    assert len(receipt) == 2
    for row in receipt:
        assert row['status'] == 200
        assert len((HERE / row['file']).read_bytes()) == row['bytes']
        assert sha(HERE / row['file']) == row['sha256']
        assert row['retrieval_started_utc'] <= row['retrieval_finished_utc']
    euro = load('eurostat_dublin_education_original.json')
    assert euro['id'] == ['freq', 'indic_ur', 'cities', 'time']
    assert euro['size'] == [1, 14, 1, 36]
    edims = dimensions(euro)
    labels = edims['indic_ur']['category_labels']
    assert len(labels) == 14
    assert edims['cities']['category_labels'] == {'IE001C': 'Dublin (greater city)'}
    assert not any(re.search(r'teacher|teaching|full.time.equivalent|\bFTE\b', s, re.I)
                   for s in labels.values())
    cso = load('cso_wmi07_teachers_original.json')
    assert cso['id'] == ['STATISTIC', 'TLIST(A1)', 'C02199V02655', 'C04026V04786']
    assert cso['size'] == [2, 8, 3, 41]
    cdims = dimensions(cso)
    assert cdims['STATISTIC']['category_labels'] == {
        'WMI07C01': 'Primary Education Teachers',
        'WMI07C02': 'Secondary Education Teachers'}
    assert cdims['C04026V04786']['label'] == 'Country'
    assert cdims['C04026V04786']['category_labels']['IE'] == 'Ireland'
    assert not any('Dublin' in s for s in cdims['C04026V04786']['category_labels'].values())
    report = dict(
        status='pass_nonadmission_scope_audit', admitted_cells=0,
        scope='Two new official API routes only; not an exhaustive claim about all possible Dublin sources',
        raw_responses_sha256={r['file']: r['sha256'] for r in receipt},
        retrieval_receipt_sha256=sha(HERE / 'retrieval.json'),
        extractor_sha256=sha(Path(__file__)),
        eurostat=dict(dataset='urb_ceduc', dimension_ids=euro['id'], sizes=euro['size'],
            dimensions=edims,
            teacher_or_FTE_indicator_in_returned_14=False,
            upper_secondary_student_teacher_pair_present=False,
            geographic_label='Dublin (greater city)',
            municipal_boundary_match_established=False,
            decision='No teacher denominator in this dataset. Greater-city label is not assumed to match Dublin City municipal scope; no boundary equivalence was recovered.'),
        cso=dict(dataset='WMI07', dimension_ids=cso['id'], sizes=cso['size'],
            dimensions=cdims,
            statistic_units=cso['dimension']['STATISTIC']['category'].get('unit'),
            geography_dimension='Country', city_or_school_dimension_present=False,
            provider_or_upper_secondary_only_breakdown_present=False,
            decision='National primary/secondary teacher series has no Dublin city denominator or matched upper-secondary/provider breakdown. No inference about FTE units is needed for this geographic rejection.'),
        interpretation='Missing geography/stage/provider variables are not zero-valued teachers. No ratio, utility, city extrapolation or allocation-to-actual conversion is computed.',
        excluded_prior_routes='No reused ETB376.1 allocation upper bound,411.8/3862 mismatched-year ratio, or private-provider exclusion substitution.',
        scope_inputs_written=False, model_or_manuscript_written=False,
        network_required_for_reproduction=False)
    (HERE / 'scope_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], admitted_cells=0,
        eurostat_dimensions=euro['size'], cso_dimensions=cso['size'],
        scope_audit_sha256=sha(HERE / 'scope_audit.json')), indent=2))


if __name__ == '__main__':
    main()
