"""Preserve actual Ontario board graduation rates without inventing cohort counts."""
import csv
import hashlib
import json
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile

P = Path(__file__).resolve().parent
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
BOARDS = {'B66052': 'Toronto DSB', 'B67059': 'Toronto CDSB',
          'B66303': 'CS Viamonde', 'B67318': 'CS catholique MonAvenir'}


def main():
    for item in json.loads((P / 'manifest.json').read_text()):
        b = (P / item['file']).read_bytes()
        assert len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256']
    with ZipFile(P / 'board_progress2026.xlsx') as z:
        strings = [''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        rows = []
        for r in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:row', NS):
            d = {}
            for c in r.findall('m:c', NS):
                v = c.find('m:v', NS)
                if v is None:
                    continue
                value = strings[int(v.text)] if c.get('t') == 's' else v.text
                column = ''.join(x for x in c.get('r') if x.isalpha())
                d[column] = value
            if d:
                rows.append(d)
    headers = rows[0]
    assert len(headers) == 18
    assert '2020-2021' in headers['O'] and 'Four Year' in headers['O']
    assert '2019-2020' in headers['Q'] and 'Five Year' in headers['Q']
    selected = []
    for row in rows[1:]:
        if row.get('A') not in BOARDS:
            continue
        assert row['B'] == BOARDS[row['A']]
        four, five = float(row['O']), float(row['Q'])
        assert 0 <= four <= 1 and 0 <= five <= 1
        selected.append(dict(board_id=row['A'], board=row['B'],
            four_year_grade9_cohort='2020-2021', four_year_rate=four,
            five_year_grade9_cohort='2019-2020', five_year_rate=five,
            graduation_reference_year='2023-2024',
            cohort_denominator=None, graduates=None,
            geographic_scope='Full school board, not Toronto resident or municipal-school subset'))
    assert len(selected) == 4 and {r['board_id'] for r in selected} == set(BOARDS)
    with (P / 'board_graduation_rates.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, list(selected[0]))
        writer.writeheader()
        writer.writerows(selected)
    summary = dict(main_admitted=False, original_columns=headers, board_records=selected,
        graduation_count_fields_available=False,
        four_and_five_year_rates_share_cohort=False,
        city_rate_identified=False,
        reason='Only rounded board rates are published; no graduates or cohort counts. '
               'French board geography extends beyond Toronto. Four- and five-year '
               'columns follow different Grade 9 entry cohorts, so their difference '
               'does not measure fifth-year completion for the same students.')
    (P / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(selected, indent=2))


if __name__ == '__main__':
    main()
