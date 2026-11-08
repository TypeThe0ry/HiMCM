"""Verify official DST aggregate files and derive national-superset bounds."""
from pathlib import Path
import csv
import hashlib
import io
import json

HERE = Path(__file__).resolve().parent


def extract():
    for item in json.loads((HERE/'manifest.json').read_text()):
        assert hashlib.sha256((HERE/item['file']).read_bytes()).hexdigest() == item['sha256']
    q = json.loads((HERE/'crime_query.json').read_text())
    codes = ['123073111', '123073121', '125873262', '128673131']
    assert q['table'] == 'STRAF5'
    assert {v['code']:v['values'] for v in q['variables']} == {
        'OVERTRÆD':codes, 'ALDER':['TOT'], 'KOEN':['TOT'], 'Tid':['2025']}
    meta = json.loads((HERE/'raw/crime_metadata.json').read_text())
    labels = {v['id']:v['text'] for d in meta['variables'] if d['id']=='OVERTRÆD' for v in d['values']}
    expected = {'Homicide':46, 'Child Murder':0,
        'Assault causing griveous bodily harm resulting in death':3, 'Killing by request':0}
    assert {labels[c] for c in codes} == set(expected)
    assert 'Attempted homicide' not in expected
    rows = list(csv.DictReader(io.StringIO((HERE/'raw/crime_victims.csv').read_text(encoding='utf-8-sig')), delimiter=';'))
    assert len(rows)==4
    for r in rows:
        assert r['TID']=='2025' and r['ALDER']=='Age, total' and r['KOEN']=='Total'
        assert int(r['INDHOLD'])==expected[r['OVERTRÆD']]
    count = sum(int(r['INDHOLD']) for r in rows)
    popq = json.loads((HERE/'population_query.json').read_text())
    assert {v['code']:v['values'] for v in popq['variables']} == {
        'OMRÅDE':['101'], 'KØN':['TOT'], 'ALDER':['IALT'], 'CIVILSTAND':['TOT'], 'Tid':['2025K3']}
    pop = list(csv.DictReader(io.StringIO((HERE/'raw/population.csv').read_text(encoding='utf-8-sig')),delimiter=';'))
    assert len(pop)==1 and pop[0]['OMRÅDE']=='Copenhagen' and pop[0]['TID']=='2025Q3'
    population = int(pop[0]['INDHOLD'])
    assert population==667574 and count==49
    excerpt = (HERE/'definition_provider_excerpt.txt').read_text()
    assert '237 manddrab, 238 barnedrab, 239 drab efter' in excerpt
    assert '246 kvalificeret vold med døden til følge' in excerpt
    rate_upper = count*100000/population
    observation = dict(city='Copenhagen',indicator='homicide_rate',
        utility_before=[0,1],utility_after=[2/(2+rate_upper),1],raw_count=count,
        population=population,sourceyear=2025,population_year=2025,
        population_reference_date='2025-07-01',geography='Copenhagen municipality code101; numerator upper bound is all Denmark',
        rate_lower=0,rate_upper=rate_upper,utility_anchor=2,lower_bound_only=True,
        upper_bound_only=False,raw_rate_upper_bound_only=True,
        scope='Conditional nationwide recorded-victim superset: homicide, child murder, fatal serious assault and killing by request. Not observed Copenhagen deaths, not resident vital mortality, not unreported deaths. Reporting-year 2025; not a guarantee that every incident occurred in 2025.',
        source_locator='DST STRAF5 2025 codes123073111,123073121,125873262,128673131, all ages/sexes; FOLK1A municipality101 2025K3; Justice Ministry homicide definition §§237,238,239,246.',
        source_url='https://api.statbank.dk/v1/data',
        components=expected,attempts_included=False,
        rule='Copenhagen victims within these recorded fatal-offence classes cannot exceed nationwide victims in the same reporting universe.',
        status='conditional_national_recorded_homicide_victim_superset',main_admitted=False)
    (HERE/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(observation,ensure_ascii=False,indent=2))
    return observation


if __name__=='__main__':
    extract()
