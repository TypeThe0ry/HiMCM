"""Verify saved official sources and derive a partial HE density lower bound."""
from pathlib import Path
import csv
import hashlib
import io
import json
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent

def extract():
    for item in json.loads((ROOT / 'manifest.json').read_text()):
        assert hashlib.sha256((ROOT / item['file']).read_bytes()).hexdigest() == item['sha256'], item['file']
    def text(name):
        p = ROOT / 'raw' / name
        if p.suffix == '.pdf':
            return ' '.join(' '.join(page.extract_text().split()) for page in PdfReader(p).pages)
        return BeautifulSoup(p.read_bytes(), 'html.parser').get_text(' ', strip=True)
    names = ['Københavns Universitet', 'IT-Universitetet i København', 'Københavns Professionshøjskole', 'Erhvervsakademi København']
    recognized = text('supervisor.html')
    assert all(n in recognized for n in names)
    assert 'hjemsted og værneting i København' in text('ku_statute.html')
    assert 'Nørregade 10' in text('ku_contact.html')
    assert 'Rued Langgaards Vej 7' in text('itu_contact.html')
    assert 'DK-2300 Copenhagen S' in text('itu_contact.html')
    assert 'KOMMUNE NR. 101' in text('itu_energy.pdf')
    assert 'Rued Langgaards Vej 7, 2300 København S' in text('itu_energy.pdf')
    for name in ['kp_statute.pdf', 'ek_statute.pdf']:
        assert 'hjemsted i Københavns Kommune' in text(name)
    assert '1. juli 2025' in text('ek_statute.pdf')
    assert 'opløst den 30. juni 2025' in text('ek_statute.pdf')
    meta = json.loads((ROOT/'raw/population_metadata.json').read_text())
    assert 'first day of the quarter' in meta['text']
    query = json.loads((ROOT/'population_query.json').read_text())
    expected = {'OMRÅDE': ['101'], 'KØN': ['TOT'], 'ALDER': ['IALT'], 'CIVILSTAND': ['TOT'], 'Tid': ['2026K3']}
    assert {v['code']:v['values'] for v in query['variables']} == expected
    rows = list(csv.DictReader(io.StringIO((ROOT/'raw/population.csv').read_text(encoding='utf-8-sig')), delimiter=';'))
    assert len(rows)==1 and rows[0]['OMRÅDE']=='Copenhagen' and rows[0]['TID']=='2026Q3'
    population=int(rows[0]['INDHOLD'])
    count=len(names)
    density=count*100000/population
    return {'city':'Copenhagen','criterion':'research_he_density','status':'conditional_partial_lower_bound',
            'verified_count':count,'institutions':names,'population':population,
            'population_reference_date':'2026-07-01','population_period':'2026Q3',
            'population_geography':'Copenhagen municipality, Denmark, code101',
            'institution_evidence_snapshot_date':'2026-11-08','institution_reference_year':2026,
            'density_lower_per_100000':density,'utility_lower':density/(1+density),'utility_upper':1.0,
            'finite_count_upper':None,'complete_city_inventory':False,
            'count_definition':'Distinct government-recognized HE institutions with central institutional address or legal seat in Copenhagen municipality; campuses and predecessor institutions deduplicated.',
            'time_alignment':'Same calendar year; institution snapshot November and population July1, not exact same day.',
            'itu_geography_basis':'Official central contact and rector address Rued Langgaards Vej7,2300 Copenhagen S; officially hosted energy certificate identifies same address with KOMMUNE NR.101.',
            'merger_rule':'EK counted once; KEA and Cphbusiness dissolved June30,2025; successor formed July1,2025.'}

if __name__=='__main__':
    print(json.dumps(extract(),ensure_ascii=False,indent=2))
