"""Reproduce baseline costs and audited Singapore core observations offline."""
from pathlib import Path
import hashlib,json
import pandas as pd
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent
SOURCE='https://www.numbeo.com/quality-of-life/rankings.jsp?title=2025'

def main():
 for r in json.loads((P/'manifest.json').read_text()):
  if r.get('sha256'):
   assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256'],r['file']
 raw=(P.parent/'task4_real/numbeo_quality_of_life_2025.html').read_bytes()
 assert hashlib.sha256(raw).hexdigest()=='b5b9bc3bae7488bfe05be50420df86e74ccaf29be22447f273c1ae4d685280bf'
 table=BeautifulSoup(raw,'html.parser').find('table',id='t2')
 cols=[x.get_text(' ',strip=True) for x in table.select('thead th')]
 data=pd.DataFrame([[x.get_text(' ',strip=True) for x in tr.find_all('td')] for tr in table.select('tbody tr')],columns=cols)
 prior=pd.read_csv(P.parent/'task4_real/city_indicators_2025.csv')
 assert len(prior)==25 and prior.city.is_unique
 records=[]
 for r in prior.itertuples():
  hits=data[data.City==r.source_city]
  assert len(hits)==1
  h=hits.iloc[0]
  for field,indicator,unit in [('Cost of Living Index','cost_living_index','New York=100; excludes rent'),('Property Price to Income Ratio','price_income_ratio','dimensionless Numbeo model ratio')]:
   value=float(h[field]);assert value>0
   if indicator=='price_income_ratio':assert abs(value-float(prior.loc[prior.city==r.city,field].iloc[0]))<1e-12
   records.append(dict(city=r.city,indicator=indicator,value=value,year=2025,unit=unit,source_url=SOURCE,
      scope='Numbeo named-city crowdsource aggregation; administrative boundaries not independently harmonized',
      status='observed',lower_bound_only=False))
 wb=json.loads((P/'sg_homicide_wb.json').read_text())
 eligible=[x for x in wb[1] if x['value'] is not None]
 x=max(eligible,key=lambda x:int(x['date']))
 assert x['countryiso3code']=='SGP' and x['indicator']['id']=='VC.IHR.PSRC.P5'
 assert x['date']=='2023'
 records.append(dict(city='Singapore',indicator='homicide_rate',value=x['value'],year=int(x['date']),
   unit='intentional homicides per 100000 population',
   source_url='https://api.worldbank.org/v2/country/SGP/indicator/VC.IHR.PSRC.P5?format=json',
   scope='Singapore city-state national boundary equivalent; WDI compilation; not homicide attempts or perceived safety',
   status='observed',lower_bound_only=False))
 g=json.loads((P/'sg_bus_stops.geojson').read_text());assert g['type']=='FeatureCollection'
 ids=[f['properties']['BUS_STOP_NUM'] for f in g['features']]
 assert all(ids) and len(set(ids))==len(ids)==5205
 assert all(f['geometry']['type']=='Point' for f in g['features'])
 assert all(f['properties']['FMEL_UPD_D'].startswith('2026') for f in g['features'])
 # Boarding/stop codes, NOT an unreported50-m clustering of physical interchange sites.
 population=6208500 # SingStat total2026 population; audited resources directory extract.
 records.append(dict(city='Singapore',indicator='public_transport_density',value=len(set(ids))/population*1e5,year=2026,
   unit='unique listed bus-stop codes per 100000 total population; lower bound',
   source_url='https://data.gov.sg/datasets/d_3f172c6feb3f4f92a2f47d93eed2908a/view',
   scope='LTA bus-stop catalogue codes; no 50m clustering; buses only; operation not independently verified; rail excluded',
   status='conditional_catalogue_lower_bound',lower_bound_only=True))
 out=pd.DataFrame(records);assert len(out)==52 and not out.duplicated(['city','indicator']).any()
 out.to_csv(P/'observations.csv',index=False)
 print(out.groupby('indicator').size().to_string())
 print(out[out.city=='Singapore'].to_string(index=False))
if __name__=='__main__':main()
