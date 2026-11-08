"""Extract a conservative city-boundary metro subset from the CRTM archive."""
from pathlib import Path
from collections import defaultdict
import csv, hashlib, html, json, re
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'data/task4_v117_team_intake/city_indicators.csv'
EXPECTED='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    retrievals=json.loads((HERE/'retrievals.json').read_text())
    for row in retrievals:
        if 'sha256' in row:assert hashlib.sha256((HERE/row['file']).read_bytes()).hexdigest()==row['sha256']
    item=json.loads((HERE/'metro_item.json').read_text())
    assert item['owner']=='ConsorcioRegional' and item['orgId']=='UxADft6QPcvFyDU1'
    assert 'CRTM' in item['accessInformation'] and item['access']=='public'
    metadata=json.loads((HERE/'metro_metadata.json').read_text())
    assert metadata['name']=='M4_Estaciones' and metadata['id']==0
    codes=html.unescape(re.sub('<[^>]+>',' ',(HERE/'ine_municipality_codes.html').read_text()))
    assert re.search(r'28079\s+Madrid',codes)
    data=json.loads((HERE/'metro_stations_all.json').read_text())
    assert not data.get('exceededTransferLimit',False)
    features=data['features'];assert len(features)==293 and len(features)<metadata['maxRecordCount']
    attrs=[r['attributes'] for r in features]
    city=[r for r in attrs if r['CODIGOPROVINCIA']=='28' and r['CODIGOMUNICIPIO']=='079']
    valid=[r for r in city if r['DENOMINACION'] and r['LINEAS'] and r['CODIGOCTMESTACIONREDMETRO'] and r['FECHAFIN'] is None]
    omitted=[r for r in city if r not in valid]
    assert len(city)==242 and len(valid)==240 and len(omitted)==2
    assert all(not r['DENOMINACION'] and not r['LINEAS'] for r in omitted)
    assert {r['FECHAACTUAL'] for r in attrs}=={'20260529'}
    groups=defaultdict(list)
    for r in valid:
        assert r['MODO']==4
        groups[r['CODIGOCTMESTACIONREDMETRO']].append(r)
    assert len(groups)==191
    records=[]
    for key,rows in sorted(groups.items()):
        records.append(dict(network_station_code=key,names=';'.join(sorted({r['DENOMINACION'] for r in rows})),
            source_records=len(rows),source_object_ids=';'.join(str(r['OBJECTID']) for r in rows),
            city_code='28079',lines=';'.join(sorted({r['LINEAS'] for r in rows}))))
    with (HERE/'madrid_metro_complexes.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    frame=pd.read_csv(SOURCE); row=frame.loc[frame.city.eq('Madrid')].iloc[0]
    population=int(row.population);assert population==3527924
    density=100000*len(groups)/population;utility=density/(50+density)
    observation=dict(city='Madrid',indicator='public_transport_density',raw_count=len(groups),population=population,
        population_year=int(row.population_year),population_source='Unchanged authoritative team CSV; not externally rechecked',
        sourceyear=2026,record_date='2026-05-29',access_date='2026-11-09',
        lower_bound_only=True,density_per_100000_lower=density,utility_after=[utility,1],
        utility_before=[0,1],utility_anchor=50,source_url=item['url']+'/0',
        source_files=['metro_stations_all.json','metro_metadata.json','metro_item.json','crtm_service.json','ine_municipality_codes.html'],
        candidate_only=True,admissible='conditional_inventory_lower_bound',historical_inventory_proxy=False,
        scope='CRTM metro station records tagged province28/municipality079 (Madrid city); group 240 named route-bearing records by 191 nonnull provider network-station codes. Noviciado/Plaza de España and Embajadores/Acacias are each conservatively consolidated as one linked complex. Two unnamed/no-line records and 51 outside-city records omitted. No bus, commuter rail or light-rail count is added.',
        limitations='2026 registry inventory at source record date, with unchanged2025 team population; not a2025 same-year census, real-time service availability, all-provider stop inventory or teenage access measure. Temporary closures cannot be reconstructed from the registry. Unknown uncounted modes retain upper utility1. SITUACION codes are not interpreted as operating status.',
        extraction='Offline extract.py with all293 source records archived; city-code mapping independently documented by INE.')
    (HERE/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
    audit=dict(status='pass',original_csv_sha256=EXPECTED,all_source_hashes_verified=True,provider_records=293,city_records=242,
        outside_city_records=51,unnamed_no_line_city_records_omitted=2,named_city_records=240,consolidated_complexes=191,
        duplicate_line_records_consolidated=49,nonpoint_population_preserved=True,
        multi_name_complexes={k:sorted({r['DENOMINACION'] for r in rows}) for k,rows in groups.items() if len({r['DENOMINACION'] for r in rows})>1},
        transfer_limit_exceeded=False,observed_utility_lower=utility,upper_remains_one=True)
    (HERE/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(audit,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
