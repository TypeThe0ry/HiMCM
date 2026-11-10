"""A dated Vienna bus candidate from regular scheduled calls and native DIVA."""
import argparse,csv,datetime,json,lzma,re
from collections import defaultdict
from decimal import Decimal,ROUND_HALF_EVEN
from pathlib import Path
import numpy as np
import pandas as pd
from matplotlib.path import Path as Polygon
from task4_user_v203_revision import revised_bounds
from task4_user_city_indicators import evaluate
from task4_v5_model import NAMES,weights
R=Path(__file__).resolve().parents[1];D=R/'data/current_vienna_gtfs';B=R/'data/task4_v127_vienna_transport'
def stream(p):
    if p.exists():return p.open(encoding='utf-8-sig',newline='')
    return lzma.open(str(p)+'.xz','rt',encoding='utf-8-sig',newline='')
def rows(p,sep=','):
    with stream(p) as f:return list(csv.DictReader(f,delimiter=sep))
def xy(lon,lat):return tuple(Decimal(str(v)).quantize(Decimal('.0000001'),rounding=ROUND_HALF_EVEN) for v in [lon,lat])
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True)
    out=ap.parse_args().output_dir.resolve()
    if out.exists():raise FileExistsError('Use a new output directory')
    date='20261110';weekday=datetime.datetime.strptime(date,'%Y%m%d').strftime('%A').lower()
    calendars=rows(D/'calendar.txt');assert len({r['service_id'] for r in calendars})==len(calendars)
    active={r['service_id'] for r in calendars if r['start_date']<=date<=r['end_date'] and r[weekday]=='1'}
    exceptions=[r for r in rows(D/'calendar_dates.txt') if r['date']==date]
    assert len({r['service_id'] for r in exceptions})==len(exceptions)
    for r in exceptions:
        assert r['exception_type'] in ['1','2']
        if r['exception_type']=='1':active.add(r['service_id'])
        else:active.discard(r['service_id'])
    routes={r['route_id']:r for r in rows(D/'routes.txt')}
    agencies={r['agency_id']:r for r in rows(D/'agency.txt')};assert agencies['04']['agency_name']=='Wiener Linien GmbH & Co KG'
    trips={r['trip_id']:r for r in rows(D/'trips.txt') if r['service_id'] in active}
    stops={r['stop_id']:r for r in rows(D/'stops.txt')}
    areas=rows(B/'stop_areas.csv',';');by_name=defaultdict(list);by_point=defaultdict(list);by_diva=defaultdict(list)
    for r in areas:by_name[r['PlatformText']].append(r)
    for r in rows(B/'stop_positions.csv',';'):
        by_point[xy(r['Longitude'],r['Latitude'])].append(r);by_diva[r['DIVA']].append(r)
    feature=json.loads((B/'vienna_boundary.geojson').read_text())['features'][0]
    assert feature['geometry']['type']=='Polygon'
    rings=[Polygon(np.asarray(r,float)) for r in feature['geometry']['coordinates']]
    def inside(lon,lat):
        p=(float(lon),float(lat));return bool(rings[0].contains_point(p) and not any(r.contains_point(p) for r in rings[1:]))
    eligible={};name_area={}
    for sid,s in stops.items():
        aa=by_name[s['stop_name']]
        if len(aa)!=1:continue
        a=aa[0]
        if a['Municipality']!='Wien' or not inside(a['Longitude'],a['Latitude']) or not inside(s['stop_lon'],s['stop_lat']):continue
        name_area[sid]=a['DIVA']
        if not by_diva[a['DIVA']] or not all(inside(p['Longitude'],p['Latitude']) for p in by_diva[a['DIVA']]):continue
        pp=by_point[xy(s['stop_lon'],s['stop_lat'])]
        if not pp or {p['DIVA'] for p in pp}!={a['DIVA']} or any(p['StopText']!=s['stop_name'] for p in pp):continue
        if not all(inside(p['Longitude'],p['Latitude']) for p in pp):continue
        eligible[sid]=(a,sorted(p['StopID'] for p in pp))
    modes=defaultdict(set);witness={};counts=dict(stop_time_rows=0,active_regular_call_rows=0,qualified_A_call_rows=0)
    with stream(D/'stop_times.txt') as f:
        for r in csv.DictReader(f):
            counts['stop_time_rows']+=1;t=trips.get(r['trip_id'])
            if t is None or not (r['pickup_type'] in ['0',''] or r['drop_off_type'] in ['0','']):continue
            counts['active_regular_call_rows']+=1;route=routes[t['route_id']];sid=r['stop_id']
            if sid in name_area:modes[name_area[sid]].add(route['route_type'])
            if sid not in eligible or route['agency_id']!='04' or route['route_type']!='3' or re.fullmatch('[0-9]+A',route['route_short_name']) is None:continue
            counts['qualified_A_call_rows']+=1;a,ids=eligible[sid];diva=a['DIVA']
            if diva not in witness:
                s=stops[sid]
                witness[diva]=dict(DIVA=diva,name=a['PlatformText'],DIVA_longitude=a['Longitude'],DIVA_latitude=a['Latitude'],
                    GTFS_stop_id=sid,GTFS_longitude=s['stop_lon'],GTFS_latitude=s['stop_lat'],native_StopIDs_json=json.dumps(ids),
                    trip_id=r['trip_id'],service_id=t['service_id'],route_id=t['route_id'],route_short_name=route['route_short_name'],
                    stop_sequence=r['stop_sequence'],arrival_time=r['arrival_time'],departure_time=r['departure_time'],pickup_type=r['pickup_type'],drop_off_type=r['drop_off_type'])
    accepted=[r for k,r in sorted(witness.items()) if modes[k]=={'3'}]
    excluded=[dict(DIVA=k,name=r['name'],active_route_types_json=json.dumps(sorted(modes[k]))) for k,r in sorted(witness.items()) if modes[k]!={'3'}]
    n=len(accepted);assert n>99
    f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Vienna');j=NAMES.index('public_transport_density')
    assert f.iloc[i].population==2028399
    density=n*100000/2028399;value=density/(50+density);assert value>lo[i,j] and hi[i,j]==1
    tables=[];cases=[];bounds=[]
    for scenario in ['retained_V203','candidate_bus_subset']:
        ll=lo.copy()
        if scenario=='candidate_bus_subset':ll[i,j]=value
        mask=np.ones(lo.shape,dtype=bool);mask[i,j]=False
        assert np.array_equal(ll[mask],lo[mask])
        bounds.extend(dict(scenario=scenario,city=c,indicator=name,lower=float(ll[a,b]),upper=float(hi[a,b])) for a,c in enumerate(cities) for b,name in enumerate(NAMES))
        for ref,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
            t=evaluate(cities,ll,hi,w);tables.append(t.drop(columns=['midpoint_illustrative_score','midpoint_illustrative_rank']).assign(scenario=scenario,weight_reference=ref))
            cases.append(dict(scenario=scenario,weight_reference=ref,recommendations=t.loc[t.decision_rank.eq(1),'city'].tolist(),mean_width=float((t.score_upper-t.score_lower).mean()),possible_champions=int(t.possible_champion.sum()),necessary_champions=int(t.necessary_champion.sum())))
    out.mkdir(parents=True)
    for filename,rr in [('station_witnesses.csv',accepted),('excluded_mixed_modes.csv',excluded)]:
        with (out/filename).open('w',newline='') as f:
            fields=list(rr[0]) if rr else ['DIVA','name','active_route_types_json'];w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rr)
    pd.concat(tables,ignore_index=True).to_csv(out/'ranks.csv',index=False);pd.DataFrame(bounds).to_csv(out/'bounds.csv',index=False)
    summary=dict(status='candidate awaiting independent crosswalk and full integration review',service_day=date,timezone='Europe/Vienna',
        service_day_not_civil_day=True,active_services=len(active),active_trips=len(trips),counts=counts,coordinate_comparison_decimal_places=7,
        coordinate_comparison_is_not_accuracy_claim=True,qualified_witness_groups=len(witness),excluded_mixed_mode_groups=len(excluded),
        candidate_DIVA_groups=n,retained_metro_groups=99,counts_not_added=True,population=2028399,population_year=2025,anchor=50,candidate_utility_lower=value,
        cases=cases,primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        scope='Two dated operator sources, exact global name/rounded source-coordinate crosswalk to native DIVA, ordinary A buses with regular scheduled calls; no stop-ID prefix parsing, clustering, census, real-time-service, student-access or2025uniform-snapshot claim. Conditional score improvement is not activated primary improvement.')
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary))
if __name__=='__main__':main()
