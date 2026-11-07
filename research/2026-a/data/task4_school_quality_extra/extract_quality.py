"""Offline, dependency-free extraction of archived primary-source XLSX cells."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as E
import json
import csv

ROOT = Path(__file__).resolve().parent
NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def read_sheet(filename, number=1):
    with ZipFile(ROOT / filename) as z:
        strings = [''.join(t.itertext()) for t in E.fromstring(
            z.read('xl/sharedStrings.xml')).findall('m:si', NS)]
        rows = []
        for row in E.fromstring(z.read(f'xl/worksheets/sheet{number}.xml')).findall('.//m:row', NS):
            values = {}
            for c in row:
                v = c.find('m:v', NS)
                value = '' if v is None else v.text
                values[c.attrib['r']] = strings[int(value)] if c.get('t') == 's' else value
            rows.append(values)
    return rows


if __name__ == '__main__':
    rows = read_sheet('ontario_board2026.xlsx')
    assert rows[0]['O1'] == 'Four Year Graduation Rate 2020-2021 Grade\xa09 Cohort'
    result = []
    for r in rows[1:]:
        rownum = next(iter(r))[1:]
        name = r.get('B' + rownum)
        if name not in ['Toronto DSB', 'Toronto CDSB']:
            continue
        result.append(dict(city='Toronto', school_system=name, entry_cohort='2020-2021',
                           outcome_school_year='2023-2024', four_year_completion=float(r['O'+rownum]),
                           five_year_completion_other_cohort=float(r['Q'+rownum]),
                           cell='O'+rownum, source_file='ontario_board2026.xlsx',
                           coverage='English-language publicly funded board; not all city schools'))
    assert len(result) == 2
    (ROOT / 'toronto_extracted.json').write_text(json.dumps(result, indent=2)+'\n')
    with (ROOT / 'toronto_extracted.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=result[0].keys());writer.writeheader();writer.writerows(result)
    print(json.dumps(result, indent=2))
