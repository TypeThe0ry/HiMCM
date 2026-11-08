"""Trace recommendation-critical SG sources and derive separate murder descriptors."""
import csv,hashlib,json
from pathlib import Path
from bs4 import BeautifulSoup
P=Path(__file__).resolve().parent

def records(name):
    d=json.loads((P/name).read_text());assert d['success']
    r=d['result'];assert len(r['records'])==r['total']
    return r['records']

def extract():
    for r in json.loads((P/'manifest.json').read_text()):
        b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    wb=json.loads((P/'wdi_homicide.json').read_text());assert wb[0]['pages']==1 and len(wb[1])==wb[0]['total']
    assert all(r['countryiso3code']=='SGP' and r['indicator']['id']=='VC.IHR.PSRC.P5' for r in wb[1])
    latest=max((r for r in wb[1] if r['value'] is not None),key=lambda r:int(r['date']))
    assert latest['date']=='2023' and latest['value']==0.0690954942050905
    assert all(next(r for r in wb[1] if r['date']==str(y))['value'] is None for y in [2024,2025])
    meta=json.loads((P/'wdi_indicator_metadata.json').read_text())[1][0]
    assert meta['id']=='VC.IHR.PSRC.P5' and 'intent to cause death or serious injury' in meta['sourceNote'] and 'UNODC' in meta['sourceOrganization']
    victims=records('victims.json');pop=records('population.json')
    def select(label,rs):
        hit=[r for r in rs if r['DataSeries']==label];assert len(hit)==1;return hit[0]
    total=select('Total Victims Of Murder',victims);male=select('Male Victims Of Murder',victims);female=select('Female Victims Of Murder',victims)
    population=select('Total Population',pop)
    for name,source in [('victims_page.html','SINGAPORE POLICE FORCE'),('population_page.html','SINGAPORE DEPARTMENT OF STATISTICS')]:
        text=BeautifulSoup((P/name).read_bytes(),'html.parser').get_text(' ',strip=True);assert source in text
    scenarios=[]
    for year in [2023,2024,2025]:
        y=str(year);n=int(total[y]);den=int(population[y]);assert n==int(male[y])+int(female[y])
        assert den==int(select('Resident Population',pop)[y])+int(select('Non-Resident Population',pop)[y])
        assert int(select('Resident Population',pop)[y])==int(select('Singapore Citizen Population',pop)[y])+int(select('Permanent Resident Population',pop)[y])
        # The under21 child rows are mutually exclusive with above21 and unknown;
        # youths7–19 is nested and MUST NOT be added a second time.
        for idx in [0,5,10]:
            assert int(victims[idx][y])==sum(int(victims[k][y]) for k in [idx+1,idx+2,idx+4])
        rate=n/den*100000
        scenarios.append(dict(year=year,murder_victims=n,total_population=den,murder_victims_per_100000=rate,conditional_risk_utility=2/(2+rate)))
    assert [r['murder_victims'] for r in scenarios]==[4,10,8]
    assert [r['total_population'] for r in scenarios]==[5917648,6036860,6111175]
    raw=(P/'../task4_v5_resources/ookla_global_index.html').read_text()
    ookla=json.JSONDecoder().raw_decode(raw.split('var results = ',1)[1])[0]
    broadband=[r for r in ookla['fixedMedian'] if r['country']['country_code']=='SG'];assert len(broadband)==1
    b=broadband[0];assert b['platform']=='Fixed' and b['month']=='2026-09' and b['download_mbps']=='476.02' and b['time_period_type']=='rolling_quarter'
    assert not any(r['city_name']=='Singapore' for r in ookla['fixedCitiesMedian'])
    mean=[r for r in ookla['fixedMean'] if r['country']['country_code']=='SG'];assert len(mean)==1 and float(mean[0]['download_mbps'])==667.71
    return dict(main_admitted=False,admitted_cells_changed=0,
        existing_homicide=dict(year=2023,rate=latest['value'],utility=2/(2+latest['value']),provider='WDI / UNODC',latest_refresh=wb[0]['lastupdated']),
        local_murder_scenarios=scenarios,
        latest_wdi_missing_years=[2024,2025],
        homicide_mapping='No verified local murder-to-ICCS intentional-homicide equivalence or inclusion mapping; separate descriptors, no main replacement or one-sided bound.',
        denominator_scope='SingStat annual total population of city-state, residents plus non-residents. Not a teenage population denominator or person-time exposure of the police victim universe.',
        broadband=dict(value=476.02,unit='Mbps',statistic='fixedMedian country download',period='2026-09',aggregate_date=b['aggregate_date'],aggregation=b['time_period_type'],geography='Singapore city-state',not_mean=667.71,utility=476.02/(100+476.02),coverage='Publisher speedtest aggregate, not household access coverage, school access or student-specific speeds.'),
        interpretation='Source/year sensitivity only. The count ratio is a recorded-murder descriptor; no causal or individual-risk interpretation. Broad age groups cannot identify exact current-high-school pupils.')

if __name__=='__main__':
    d=extract();(P/'summary.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
