"""Extract actual Tokyo 2025 school counts with explicit headquarters scope."""
import csv
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parent


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def rows(name):
    with (P / name).open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def extract():
    for r in json.loads((P / 'manifest.json').read_text()):
        data = (P / r['file']).read_bytes()
        assert len(data) == r['bytes'] and hashlib.sha256(data).hexdigest() == r['sha256']
    school = rows('gk25qv0711.csv')
    yearly = []
    for year in (2024, 2025):
        matches = [r for r in school if r['種別'] == '総数（国・公・私立）'
                   and r['地域階層'] == '0' and r['地域'] == '総数'
                   and r['西暦（年度）'] == str(year)]
        assert len(matches) == 1
        r = matches[0]
        pupils, teachers = int(r['生徒数（人）']), int(r['教員数（本務者）（人）'])
        assert pupils == int(r['生徒数／全日制（人）']) + int(r['生徒数／定時制（人）'])
        assert pupils == int(r['生徒数／男（人）']) + int(r['生徒数／女（人）'])
        assert teachers == int(r['教員数（本務者）／男（人）']) + int(r['教員数（本務者）／女（人）'])
        yearly.append(dict(year=year, date=f'{year}-05-01', schools=int(r['学校数（校）']),
                           students=pupils, main_duty_teachers=teachers, ptr=pupils/teachers,
                           utility=15*teachers/(pupils+15*teachers)))
    assert (yearly[0]['students'], yearly[0]['main_duty_teachers']) == (302411,19325)
    universities = rows('gk25qvc0311.csv')
    matches = [r for r in universities if r['地域階層'] == '0' and r['地域'] == '総数']
    assert len(matches) == 1
    u = matches[0]
    count = int(u['学校数／計（校）'])
    ownership = {k:int(u[f'学校数／{k}（校）']) for k in ['国立','公立','私立']}
    assert count == sum(ownership.values()) == 143
    raw = (P / 'gk25qvc0311.csv').read_text(encoding='utf-8-sig')
    assert '大学本部の所在地による' in raw
    parser = Text()
    parser.feed((P / 'population_may2025.html').read_text())
    text = ' '.join(parser.parts)
    populations = re.findall(r'人口総数[\s　]*([\d,]+)人', text)
    assert populations and set(populations) == {'14,254,039'}
    population = int(populations[0].replace(',', ''))
    density = count/population*100000
    return dict(provider='Tokyo Metropolitan Government, School Basic Survey 2025',
                education_scope='Tokyo Metropolis national/public/private high schools, full-time and part-time regular courses; excludes correspondence courses and separately tabulated integrated secondary schools; main-duty teacher persons, not FTE',
                school_year_comparison=yearly,
                higher_education=dict(university_count=count, ownership=ownership,
                    count_location='University headquarters, explicitly not faculty/student location',
                    date='2025-05-01', population=population,
                    population_vintage='Original 2025-05-28 published estimate based on 2020 census; not a claim of latest rebased population',
                    university_headquarters_density_per_100k=density,
                    conditional_all_he_utility_lower=density/(1+density),
                    utility_upper=1, finite_all_he_upper_supported=False,
                    condition='Accept recognized university headquarters as qualifying institutional location. Other HE types, branches and independently qualified institutions are not claimed exhausted.',
                    not_measured='Student seats, admissions, affordability, individual campus access, complete higher-education inventory'))


if __name__ == '__main__':
    result = extract()
    (P / 'summary.json').write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(result, indent=2, ensure_ascii=False))
