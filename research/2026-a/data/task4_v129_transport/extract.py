"""Propose a Berlin inner-city metro inventory subset from original BVG HTML.

Uses embedded first-party station objects, not inferred line totals or platforms.
Only derived files in this directory are written; the model is not registered.
"""
import csv
import hashlib
import html
import json
import re
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ACCESS='2026-11-09'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    source_files=[f'berlin_u{i}.html' for i in range(1,10)]+['berlin_zone_definition.html']
    source_hashes={name:sha(HERE/name) for name in source_files}
    records={};names={};appearances=[];line_checks=[]
    for i in range(1,10):
        file=f'berlin_u{i}.html';s=(HERE/file).read_text()
        match=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',s,re.S)
        props=json.loads(match.group(1))['props']['pageProps']['pageJson']
        route=props['main']['fgiPearlString']['initialRouteData']
        assert str(route['lineType'])=='2'
        total=inside=0
        for segment_index,segment in enumerate(route['routeSegments']):
            for stop_index,stop in enumerate(segment['stops']):
                total+=1
                assert stop['zone']==segment['fareZone']
                if stop['zone']!='A':continue
                inside+=1
                slug,title=stop['slug'],stop['title']
                name=re.sub(r'^(S\+U|U) ','',title).replace('\\u200b','').replace('\u200b','')
                assert name and slug and name!=title
                assert names.setdefault(name,slug)==slug,'One name assigned multiple station identities'
                row=records.setdefault(slug,dict(name=name,raw_titles=set(),zone='A',lines=set(),positions=[]))
                assert row['name']==name,'One station slug assigned multiple normalized names'
                row['raw_titles'].add(title);row['lines'].add(f'U{i}')
                loc=dict(file=file,segment_index=segment_index,stop_index=stop_index,
                         slug=slug,title=title,zone=stop['zone'],
                         declared_subway_transfers=[x['name'] for x in stop.get('transfers',{}).get('subway',[])])
                row['positions'].append(loc);appearances.append(loc)
        line_checks.append(dict(line=f'U{i}',all_profile_stops=total,selected_zone_A_stops=inside))
    assert [r['selected_zone_A_stops'] for r in line_checks]==[13,23,16,5,13,14,22,15,10]
    assert len(appearances)==131 and len(records)==len(names)==100
    # Every cross-line occurrence must also be corroborated as an interchange
    # by the original station's subway-transfer declarations.
    for row in records.values():
        for p in row['positions']:
            own='U'+re.search(r'berlin_u(\d)',p['file']).group(1)
            assert row['lines']-{own} <= set(p['declared_subway_transfers'])
    zones=html.unescape((HERE/'berlin_zone_definition.html').read_text())
    text=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',zones))
    assert 'Berliner Innenstadt bis einschließlich S-Bahn Ring' in text
    assert 'außerhalb des S-Bahn Rings bis zur Stadtgrenze' in text
    # Only A is admitted: inside the explicitly defined Berlin inner-city ring.
    # No general assumption that every operator/tariff region equals a city.
    source=ROOT/'data/task4_v117_team_intake/city_indicators.csv'
    input_hash=sha(source)
    assert input_hash=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
    with source.open(encoding='utf-8-sig') as f:city=next(r for r in csv.DictReader(f) if r['city']=='Berlin')
    population=int(city['population']);assert population==3700577
    prior_file=ROOT/'results/task4_user_v127_revision/utility_bounds.csv'
    with prior_file.open() as f:
        prior=next(r for r in csv.DictReader(f) if r['scenario']=='after_conditional' and r['city']=='Berlin' and r['indicator']=='public_transport_density')
    assert [float(prior['lower']),float(prior['upper'])]==[0,1]
    venues=[]
    for slug,r in sorted(records.items()):
        venues.append(dict(station_slug=slug,station_name=r['name'],raw_titles=sorted(r['raw_titles']),
            station_url='https://www.bvg.de/de/verbindungen/stationsuebersicht/'+slug,
            area='BVG zoneA, explicitly Berlin inner city through S-Bahn ring',
            subway_lines=sorted(r['lines']),source_positions=r['positions']))
    (HERE/'berlin_stations.json').write_text(json.dumps(venues,ensure_ascii=False,indent=2)+'\n')
    (HERE/'berlin_line_checks.json').write_text(json.dumps(line_checks,indent=2)+'\n')
    d=len(venues)*100000/population
    observation=dict(city='Berlin',indicator='public_transport_density',raw_count=len(venues),
        population=population,population_year=2025,sourceyear=2026,access_date=ACCESS,
        population_source='Unchanged authoritative16-city attachment; not externally rechecked',
        utility_before=[0,1],utility_after=[d/(50+d),1],utility_anchor=50,
        density_per_100000_lower=d,lower_bound_only=True,
        admission_status='Candidate only; parent independent review required',
        source_locator='https://www.bvg.de/de/verbindungen/linienuebersicht',
        source_files=source_files,source_hashes=source_hashes,historical_inventory_proxy=False,
        scope='100unique official BVG station slugs with station-level zoneA classifier in current U1-U9 route-profile embedded objects, accessed2026-11-09. BVG explicitly defines A as Berlin inner city through S-Bahn ring; only that inner-city subset is selected. Cross-line slugs collapse131line occurrences to100station complexes. No B/C region, platform, exit or S-Bahn appearance added.',
        extraction='Original official HTML __NEXT_DATA__.props.pageProps.pageJson.main.fgiPearlString.initialRouteData.routeSegments[*].stops[*]: slug,title,zone,transfers. Same-name/slug bijection and all cross-line interchange declarations asserted.',
        limitations='Current published named-station inventory snapshot with unchanged2025 population; not a2025 census, complete city inventory, live operating-status audit, continuous-opening guarantee, teenage usage or accessibility measurement. Route-profile objects are not real-time disruption feeds; temporary closures/exits are not independently audited for all100. Inventory interpretation is conditional and may be withdrawn to[0,1]. Uncounted outer-city stations/modes keep upper1.')
    (HERE/'observations.json').write_text(json.dumps([observation],ensure_ascii=False,indent=2)+'\n')
    manifest=dict(access_date=ACCESS,input_sha256=input_hash,baseline='16-cityV127',
        original_source_urls={**{f'berlin_u{i}.html':f'https://www.bvg.de/de/verbindungen/linienuebersicht/u{i}' for i in range(1,10)},
            'berlin_zone_definition.html':'https://www.bvg.de/de/abos-und-tickets/tarifzonen-und-tarifbestimmungen'},
        source_hashes=source_hashes,representation='Original HTTP-response HTML bytes; native first-party embedded JSON extracted deterministically, no AI text provider',
        source_schema='pageJson.main.fgiPearlString.initialRouteData.routeSegments[*].stops[*] with official slug,title,zone and transfers.subway[*].name',
        identity_rule='Unique original station slug; normalized title is bijective with slug. Repeated profile-render blocks are not counted; only one native initialRouteData object per line.',
        geography_rule='Only station-level zoneA; publisher explicitly defines it as Berlin inner city through S-Bahn ring. No polygon overlay claimed; no inferred use of zoneB/C boundary.',
        line_checks=line_checks,appearances=131,station_complexes=100,
        original_source_status='As-accessed2026 published inventory, not an independently reconstructed2025 or real-time operation dataset',
        checks=dict(original_station_slugs=True,title_slug_bijection=True,station_level_zone_assignment=True,
            all_cross_line_transfers_corroborated=True,partial_inventory_only=True,
            original_csv_hash_unchanged=(sha(source)==input_hash)))
    (HERE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(city='Berlin',count=len(venues),density_lower=d,
        utility_after=observation['utility_after'],source_files=len(source_files)),indent=2))


if __name__=='__main__':main()
