"""Independent source/context audit; does not invoke the source extractor."""
import csv
import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'task4_v102_copenhagen'
manifest = json.loads((SOURCE/'manifest.json').read_text())
for row in manifest:
    content = (SOURCE/row['file']).read_bytes()
    assert len(content) == row['bytes']
    assert hashlib.sha256(content).hexdigest() == row['sha256']

def html(name):
    return BeautifulSoup((SOURCE/'raw'/name).read_bytes(), 'html.parser').get_text(' ', strip=True)

def page(name, index):
    return ' '.join(PdfReader(SOURCE/'raw'/name).pages[index].extract_text().split())

supervisor = html('supervisor.html')
current_he = supervisor.split('Selvejende videregående uddannelsesinstitutioner',1)[1].split('Maritime uddannelsesinstitutioner',1)[0]
for label in ['Københavns Universitet', 'IT-Universitetet i København', 'Københavns Professionshøjskole', 'Erhvervsakademi København']:
    assert label in current_he
assert 'Styrelsen har hovedansvar' in supervisor
assert 'hjemsted og værneting i København' in html('ku_statute.html')
assert 'Nørregade 10' in html('ku_contact.html')
itu = html('itu_contact.html')
assert 'Address IT University of Copenhagen Rued Langgaards Vej 7 DK-2300 Copenhagen S' in itu
assert 'Rector Per Bruun Brockhoff' in itu
energy = page('itu_energy.pdf',4)
assert 'KOMMUNE NR. 101' in energy and 'Rued Langgaards Vej 7' in energy
assert '27. juni 2025 - 27. juni 2035' in energy
kp, ek = page('kp_statute.pdf',0), page('ek_statute.pdf',0)
assert 'hjemsted i Københavns Kommune' in kp and 'hjemsted i Københavns Kommune' in ek
assert 'sammenlagt den 1. marts 2018' in kp
assert 'oprettet den 1. juli 2025' in ek and 'opløst den 30. juni 2025' in ek
assert '30 89 17 32' in kp and '45360644' in ek
about = html('about.html')
assert 'existing and former' in about and 'defence, police and other authorities' in about
query = json.loads((SOURCE/'population_query.json').read_text())
assert query['table'] == 'FOLK1A'
assert {x['code']: x['values'] for x in query['variables']} == {'OMRÅDE':['101'],'KØN':['TOT'],'ALDER':['IALT'],'CIVILSTAND':['TOT'],'Tid':['2026K3']}
meta = json.loads((SOURCE/'raw/population_metadata.json').read_text())
assert 'first day of the quarter' in meta['text']
with (SOURCE/'raw/population.csv').open(encoding='utf-8-sig') as f:
    rows=list(csv.DictReader(f,delimiter=';'))
assert len(rows)==1 and rows[0] == {'OMRÅDE':'Copenhagen','KØN':'Total','ALDER':'Age, total','CIVILSTAND':'Total','TID':'2026Q3','INDHOLD':'670389'}
density=400000/670389
utility=400000/(670389+400000)
summary=json.loads((SOURCE/'summary.json').read_text())
assert abs(summary['utility_lower']-utility)<1e-14
assert abs(summary['density_lower_per_100000']-density)<1e-14
assert summary['finite_count_upper'] is None and summary['utility_upper']==1
assert summary['complete_city_inventory'] is False
result={
 'decision':'accept_conditional_partial_lower_bound',
 'source_manifest_sha256':hashlib.sha256((SOURCE/'manifest.json').read_bytes()).hexdigest(),
 'source_summary_sha256':hashlib.sha256((SOURCE/'summary.json').read_bytes()).hexdigest(),
 'independently_checked_sources':len(manifest),
 'institution_count_lower':4,'population':670389,
 'density_lower_per_100000':density,'utility_lower':utility,'utility_upper':1,
 'finite_count_upper':None,
 'recognition':'Four names appear in the current government supervisor list under HE institution types, not merely in the historical recognition database.',
 'geography':'KU legal seat and main address; KP/EK explicit municipal legal seats; ITU central contact address matched to energy-certificate municipality101, page5.',
 'deduplication':'Four distinct institutional entities; no faculties, campuses, KP2018 predecessors or EK2025 predecessors counted separately.',
 'time_condition':'2026 institution snapshot and July1 population; same calendar year, not synchronized census date. Statutes/certificate are older continuing evidence.',
 'scope_condition':'Existing V46 headquarters-location policy, broad recognized HE institution supply. Not high-school access, admission, quality or commute.',
 'upper_bound_condition':'Unverified remainder remains unknown; current subset and historical/exclusion-bearing HE database do not establish exhaustive universe.',
 'numeric_model_audit':'Not performed here; this is source admission review only.'}
print(json.dumps(result,ensure_ascii=False,indent=2))
