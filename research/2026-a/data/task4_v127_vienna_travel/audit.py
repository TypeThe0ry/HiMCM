"""Independent manual-row and scalar endpoint check of the historical extract."""
import csv
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUAL = {
    'Berufsbildende mittlere Schule': (6929, 6680, 6479, 7, 194, [83,252,467,2416,1797,1003,461]),
    'AHS-Oberstufe': (19373,18930,18604,0,326,[1056,2287,2908,8009,2900,1005,439]),
    'Berufsbildende höhere Schule': (16472,15865,15521,1,343,[179,546,1091,6016,4484,2254,951])}


def main():
    rows = list(csv.DictReader((HERE/'stage_counts.csv').open()))
    source = json.loads((HERE/'historical_bounds.json').read_text())
    assert source['admission_status'] == 'historical_case_only_not_current16' and source['primary_admissions'] == 0
    assert json.loads((HERE/'observations.json').read_text()) == []
    labels = ['1-5','6-10','11-15','16-30','31-45','46-60','61plus']
    total, known, unknown = 0, 0, 0
    for row in rows:
        den, table10, daily, changing, nondaily, bins = MANUAL[row['school_type']]
        assert [int(row['count_'+label]) for label in labels] == bins
        assert int(row['full_resident_students']) == den
        assert int(row['table10_students']) == table10 and int(row['daily_duration_students']) == daily
        assert sum(bins) == daily and changing+nondaily+daily == table10
        missing = den-daily
        assert missing == int(row['total_unidentified_duration_students'])
        assert den-table10 == int(row['not_represented_in_table10'])
        for rule, low in [('conservative_continuous_closure',[0,5,10,15,30,45,60]),
                          ('literal_published_integer_classes',[1,6,11,16,31,46,61])]:
            hi = [5,10,15,30,45,60,math.inf]
            a = math.fsum(n*math.exp(-t/30) for n,t in zip(bins,hi))/den
            b = (math.fsum(n*math.exp(-t/30) for n,t in zip(bins,low))+missing)/den
            saved = next(x for x in source['rules'][rule]['stages'] if x['school_type'] == row['school_type'])
            assert abs(a-saved['lower']) < 1e-14 and abs(b-saved['upper']) < 1e-14
        total += den; known += daily; unknown += missing
    assert (total, known, unknown) == (42774,40604,2170)
    for rule in source['rules'].values():
        assert abs(sum(x['denominator']*x['lower'] for x in rule['stages'])/total-rule['pooled_full_schooltype_enrolment_bounds'][0]) < 1e-14
        assert abs(sum(x['denominator']*x['upper'] for x in rule['stages'])/total-rule['pooled_full_schooltype_enrolment_bounds'][1]) < 1e-14
        assert rule['unknown_stage_mixture_hull'] == [min(x['lower'] for x in rule['stages']), max(x['upper'] for x in rule['stages'])]
    audit = json.loads((HERE/'audit.json').read_text())
    for name, expected in audit['derived_sha256'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == expected
    audit.update(independent_manual_counts_and_scalar_bounds=True, independent_stage_and_pooled_hull_checks=True)
    (HERE/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print('PASS: three manual stage vectors, full denominators, both endpoint conventions, pooled/hull bounds and zero primary admissions')


if __name__ == '__main__':
    main()
