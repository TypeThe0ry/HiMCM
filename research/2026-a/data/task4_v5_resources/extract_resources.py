"""Offline extraction: correctly typed Ookla medians and verified HE lower bound."""
from pathlib import Path
from zipfile import ZipFile
import json,hashlib,unicodedata
import pandas as pd
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
COUNTRY={'Canada':'CA','United States':'US','Mexico':'MX','Colombia':'CO','Brazil':'BR','Chile':'CL','Denmark':'DK','United Kingdom':'GB','Spain':'ES','Poland':'PL','Greece':'GR','Kenya':'KE','Nigeria':'NG','South Africa':'ZA','United Arab Emirates':'AE','Turkey':'TR','India':'IN','Bangladesh':'BD','Japan':'JP','China':'CN','Singapore':'SG','Indonesia':'ID','Australia':'AU'}
def norm(x):return unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().casefold()
def main():
 for r in json.loads((P/'manifest.json').read_text()):
  if r.get('file') and r.get('sha256'):assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
 raw=(P/'ookla_global_index.html').read_text()
 d=json.JSONDecoder().raw_decode(raw.split('var results = ',1)[1])[0]
 cities=pd.read_csv(ROOT/'data/city_candidates_team_25.csv')
 out=[];audit=[]
 for c in cities.itertuples():
  hits=[r for r in d['fixedCitiesMedian'] if norm(r['city_name'])==norm(c.city) and r['country']['country_code']==COUNTRY[c.country]]
  scope='Ookla city aggregation; user-initiated fixed tests; not household census'
  if c.city=='Singapore':
   assert len(hits)==0
   hits=[r for r in d['fixedMedian'] if r['country']['country_code']=='SG']
   scope='Singapore city-state country median; geographic equivalence explicit; not mean or city-table entry'
  if not hits:
   audit.append(dict(city=c.city,reason='No exact city/country entry; no regional substitute'))
   continue
  assert len(hits)==1
  r=hits[0];assert r['month']=='2026-09' and r['global_index_date']=='2026-09-01'
  assert r.get('service',r.get('platform'))=='Fixed'
  out.append(dict(city=c.city,indicator='fixed_broadband_mbps',value=float(r['download_mbps']),year=2026,
                  unit='Mbps',source_url='https://www.speedtest.net/global-index',scope=scope,status='observed',
                  lower_bound_only=False,period='2026-09',source_aggregation='rolling_quarter from 2026-07-01'))
 pd.DataFrame(audit).to_csv(P/'broadband_missing_audit.csv',index=False)
 with ZipFile(P/'ror_2026_10_06.zip') as z:
  records=json.loads(z.read(next(n for n in z.namelist() if n.endswith('.json'))))
 assert hashlib.md5((P/'ror_2026_10_06.zip').read_bytes()).hexdigest()=='e16a5ceb8ff06f1a274dbd9288fe0159'
 eligible=[r for r in records if r['status']=='active' and 'education' in r['types']]
 sg=[r for r in eligible if any(l['geonames_details']['country_code']=='SG' for l in r['locations'])]
 assert len(sg)==120
 display=lambda r:next(n['value'] for n in r['names'] if 'ror_display' in n['types'])
 pd.DataFrame([dict(ror_id=r['id'],name=display(r),types=';'.join(r['types']),
    geonames_ids=';'.join(str(l['geonames_id']) for l in r['locations']),
    location_names=';'.join(l['geonames_details']['name'] for l in r['locations'])) for r in sg]).to_csv(P/'sg_ror_education_diagnostic.csv',index=False)
 # Government directory establishes six universities. Registry education tags alone
 # also match high schools and academies and are NOT an HE eligibility criterion.
 names=['National University of Singapore','Nanyang Technological University','Singapore Management University',
        'Singapore University of Technology and Design','Singapore Institute of Technology','Singapore University of Social Sciences']
 source=BeautifulSoup((P/'sg_autonomous_universities.html').read_text(),'html.parser').get_text(' ',strip=True).casefold()
 inventory=[]
 for name in names:
  assert name.casefold() in source
  hit=[r for r in sg if any(norm(n['value'])==norm(name) for n in r['names'])]
  assert len(hit)==1,(name,len(hit))
  r=hit[0];inventory.append(dict(name=name,ror_id=r['id'],status=r['status'],
    geographic_rule='All locations inside Singapore country/city-state, including Jurong West',
    type_verification='Singapore Government Directory autonomous university'))
 assert len(set(r['ror_id'] for r in inventory))==6
 pd.DataFrame(inventory).to_csv(P/'sg_verified_university_inventory.csv',index=False)
 population_row=json.loads((P/'sg_population_verified_web_extract.json').read_text())
 assert population_row['year']==2026 and population_row['unit']=='thousands'
 population=population_row['value']*1000
 out.append(dict(city='Singapore',indicator='research_he_density',value=len(inventory)/population*1e5,year=2026,
    unit='verified universities per 100000 total population; LOWER BOUND',
    source_url='https://www.sgdi.gov.sg/other-organisations/autonomous-universities',
    scope='6 verified autonomous universities; incomplete HE inventory; Singapore whole city-state population6208500',
    status='verified_inventory_lower_bound',lower_bound_only=True,period='2026-10 snapshot / June2026 population',
    source_aggregation='ROR v2.14 matched to government university directory; no finite total-HE upper bound'))
 pd.DataFrame(out).to_csv(P/'observations.csv',index=False)
 print(pd.DataFrame(out)[['city','indicator','value','lower_bound_only']].to_string(index=False))
if __name__=='__main__':main()
