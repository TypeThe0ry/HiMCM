"""Paired age-scope correction of the existing OD2023 high-school observations."""
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import xml.etree.ElementTree as ET
import zipfile
import numpy as np
from dbfread import DBF

P = Path(__file__).resolve().parent
OLD = P.parent / 'task4_v10_saopaulo'
spec = importlib.util.spec_from_file_location('legacy_saopaulo', OLD / 'extract_commute.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)


def layout_rows():
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(OLD / 'Layout_BD_OD2023_190225.xlsx') as z:
        strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si', ns)]
        rows = []
        for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:row', ns):
            values = []
            for c in r.findall('m:c', ns):
                v = c.find('m:v', ns)
                text = v.text if v is not None else ''
                values.append(strings[int(text)] if c.get('t') == 's' else text)
            rows.append(values)
    age = next(r for r in rows if 'IDADE' in r)
    current = next(i for i, r in enumerate(rows) if 'ESTUDA' in r)
    assert age[2] == 'Idade (em anos)'
    assert 'Estuda Atualmente?' in rows[current]
    assert '4 - 2º Grau/Médio' in rows[current + 3]
    return dict(age_row=age, current_study_rows=rows[current:current+6])


def main():
    for r in json.loads((P / 'manifest.json').read_text()):
        b = (P / r['file']).read_bytes()
        assert len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256']
    layout = layout_rows()
    raw = gzip.decompress((OLD / 'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    source = json.loads((OLD / 'microdata_manifest.json').read_text())
    assert len(raw) == source['files'][0]['bytes']
    assert hashlib.sha256(raw).hexdigest() == source['files'][0]['sha256']
    municipality = list(DBF(str(OLD / 'Municipios_2023.dbf'), encoding='latin1'))
    assert any(r['NumeroMuni'] == 36 and str(r['CD_IBGE']) == '3550308' for r in municipality)
    households = {}
    people = defaultdict(list)
    total = 0
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / 'source.dbf'
        f.write_bytes(raw)
        for r in DBF(str(f), encoding='latin1'):
            total += 1
            hid, metadata = r['ID_DOM'], (r['ZONA'], r['MUNI_DOM'])
            if hid in households:
                assert households[hid]['metadata'] == metadata
            else:
                households[hid] = dict(metadata=metadata, sums=np.zeros(6))
            if r['ESTUDA'] == 4:
                people[r['ID_PESS']].append(r)
    audit = []
    for pid, rows in people.items():
        for key in ['ID_DOM', 'MUNI_DOM', 'ESTUDA', 'FE_PESS', 'DATA', 'IDADE']:
            assert len({r[key] for r in rows}) == 1, (pid, key)
        assert sum(r['F_PESS'] == 1 for r in rows) == 1
        r = rows[0]
        age, w = r['IDADE'], r['FE_PESS']
        # Unknown age cannot silently become a definite excluded member.
        assert age is not None and math.isfinite(age) and 0 <= age <= 120 and age == int(age), (pid, age)
        assert w is not None and math.isfinite(w) and w > 0
        eligible = 14 <= age <= 18
        lower, upper, status = legacy.person_bound(rows)
        contribution = w * np.array([lower, upper, 1])
        households[r['ID_DOM']]['sums'][:3] += contribution
        if eligible:
            households[r['ID_DOM']]['sums'][3:] += contribution
        if r['MUNI_DOM'] == 36:
            audit.append(dict(person_id=pid, household_id=r['ID_DOM'], age=int(age),
                age14_18=eligible, current_study=4, person_weight=w,
                utility_lower=lower, utility_upper=upper, status=status))
    groups = defaultdict(list)
    for record in households.values():
        zone, muni = record['metadata']
        if muni == 36:
            groups[zone].append(record['sums'])
    # Identical household draws, including households without eligible students,
    # are used for old and new cohorts. This isolates membership changes.
    rng = np.random.default_rng(20261107)
    totals = np.zeros((2000, 6))
    for zone in sorted(groups):
        array = np.asarray(groups[zone], float)
        n = len(array)
        multiplicities = rng.multinomial(n, np.full(n, 1/n), size=2000)
        totals += multiplicities @ array
    point = np.sum([a for g in groups.values() for a in g], axis=0)
    results = {}
    for name, offset in [('all_age', 0), ('age14_18', 3)]:
        assert np.all(totals[:, offset+2] > 0)
        endpoints = totals[:, offset:offset+2] / totals[:, offset+2, None]
        identified = point[offset:offset+2] / point[offset+2]
        assert np.all(endpoints[:, 0] <= endpoints[:, 1] + 1e-12)
        subset = audit if offset == 0 else [r for r in audit if r['age14_18']]
        results[name] = dict(students=len(subset),
            households_with_students=len({r['household_id'] for r in subset}),
            weighted_students=float(point[offset+2]),
            ages={str(k): v for k, v in sorted(Counter(r['age'] for r in subset).items())},
            status_counts=dict(Counter(r['status'] for r in subset)),
            utility_lower=float(identified[0]), utility_upper=float(identified[1]),
            sampling_lower=float(min(identified[0], np.quantile(endpoints[:, 0], .025))),
            sampling_upper=float(max(identified[1], np.quantile(endpoints[:, 1], .975))))
    old_point = json.loads((OLD / 'commute_summary.json').read_text())['scopes']['municipality_sao_paulo']
    old_sampling = json.loads((OLD / 'sampling_sensitivity.json').read_text())['scopes']['municipality_sao_paulo']
    assert results['all_age']['students'] == old_point['students'] == 1778
    for k in ['utility_lower', 'utility_upper']:
        np.testing.assert_allclose(results['all_age'][k], old_point[k], rtol=0, atol=1e-12)
    np.testing.assert_allclose([results['all_age']['sampling_lower'], results['all_age']['sampling_upper']],
                              [old_sampling['utility_lower'], old_sampling['utility_upper']], rtol=0, atol=1e-12)
    assert sum(map(len, groups.values())) == old_sampling['households'] == 21917
    with (P / 'municipal_students_audit.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, list(audit[0]))
        writer.writeheader()
        writer.writerows(audit)
    result = dict(source='Existing OD2023 public research mirror, unchanged raw bytes',
        official_byte_identity_verified=False, main_admitted=False, raw_rows=total,
        current_school_condition='ESTUDA=4; actual current upper-secondary enrolment',
        target_age_condition='IDADE in integer years 14 through 18 inclusive',
        geography='Municipality 36, IBGE 3550308, Sao Paulo residence; not metro-wide',
        unknown_age_students=0, unknown_weight_students=0,
        first_journey_method='Unchanged legacy person_bound: first study-purpose journey, confirmed home origin, valid clocks/duration and weekday; unresolved remains [0,1]',
        bootstrap=dict(method='Exploratory zone-stratified household bootstrap with fixed final person weights',
            seed=20261107, replicates=2000, paired_draws=True, design_valid_confidence_interval=False,
            all_households_including_zero_eligible=sum(map(len, groups.values())), zones=len(groups)),
        layout_verification=layout, scopes=results)
    (P / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
