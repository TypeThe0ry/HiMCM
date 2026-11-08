"""Verify NPA originals and derive a conditional national-superset bound."""
import hashlib,json,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
for f in json.loads((P/'manifest.json').read_text()):
    b=(P/f['file']).read_bytes()
    assert len(b)==f['bytes'] and hashlib.sha256(b).hexdigest()==f['sha256']
z=zipfile.ZipFile(P/'R07_053.xlsx')
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
strings=[''.join(n.findall('.//m:t',ns)[i].text or '' for i in range(len(n.findall('.//m:t',ns)))) for n in ET.fromstring(z.read('xl/sharedStrings.xml'))]
cells={}
for c in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//m:c',ns):
    v=c.find('m:v',ns)
    if v is not None:cells[c.attrib['r']]=strings[int(v.text)] if c.attrib.get('t')=='s' else float(v.text)
assert '死者' in cells['F5'] and '刑法犯総数' in cells['A6'] and cells['F6']==631
# Rows8/9 are separate categories, row16 is a subtotal already in row15.
assert sum(cells.get('F'+str(i),0) for i in range(7,33) if i!=16)==cells['F6']
prior=ROOT/'data/task4_v46_tokyo/summary.json'
pop=json.loads(prior.read_text())['higher_education']['population']
assert pop==14254039
upper_rate=cells['F6']/pop*100000
result=dict(city='Tokyo',indicator='homicide_rate',proposed_admission=True,
 source_year=2025,population_year=2025,population=pop,population_date='2025-05-01',
 population_vintage='Original estimate retained from V46, not rebased census',
 national_recorded_criminal_death_victims=cells['F6'],national_murder_death_victims=cells['F7'],
 raw_rate_lower=0,raw_rate_upper=upper_rate,utility_before=[0,1],utility_after=[2/(2+upper_rate),1],
 rule='Geographic and offence-category superset: Tokyo recorded intentional-homicide deaths <= all Japan recorded criminal-death victims (excluding traffic negligence).',
 scope='Conditional on recorded-crime reporting universe and criminal-death coverage. Not a Tokyo observed count or point rate; not a bound on unreported deaths or resident vital mortality.',
 target_geography='Tokyo Metropolis; numerator bound is nationwide Japan',
 new_highschool_travel_observations=0,
 unchanged='Population denominator inherited exactly; cost anchor2, weights and TOPSIS formula unchanged.',
 inherited_population_summary_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
 source_cell='R07_053.xlsx sheet1 F6 (all criminal death victims), denominator inherited V46',
 limitations=['National total includes nonintentional and nonTokyo deaths, deliberately retained as broad upper bound.','No temporal correction or completeness correction inferred.','Annual2025 recordedcriminaldeaths paired with May2025 Tokyo population estimate.','Tokyo student travel remains[0,1]; selective athlete survey and daily return commute totals not admitted.'])
(P/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
