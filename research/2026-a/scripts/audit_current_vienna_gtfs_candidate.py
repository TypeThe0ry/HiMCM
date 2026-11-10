"""Verify candidate structure and arithmetic, leaving service eligibility pending."""
import csv,hashlib,json,lzma,math,re
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
from task4_audit_output import audit_parser,check_output,emit_report
from audit_current_oslo_cost_ptr_sources import protected_inputs
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];G=R.parents[1];D=R/'data/current_vienna_gtfs';O=R/'results/current_vienna_gtfs_candidate';B=R/'data/task4_v127_vienna_transport'
def read(p):return json.loads(p.read_text())
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def stream(p):return p.open(encoding='utf-8-sig',newline='') if p.exists() else lzma.open(str(p)+'.xz','rt',encoding='utf-8-sig',newline='')
def rows(p,sep=','):
    with stream(p) as f:return list(csv.DictReader(f,delimiter=sep))
def xy(lon,lat):return tuple(Decimal(str(v)).quantize(Decimal('.0000001')) for v in [lon,lat])
def close(a,b):assert math.isclose(float(a),float(b),abs_tol=2e-11,rel_tol=0),(a,b)
def score(u,w):
    a=math.sqrt(math.fsum(v*x*x for v,x in zip(w,u)));b=math.sqrt(math.fsum(v*(1-x)**2 for v,x in zip(w,u)));return 100*a/(a+b)
def main():
    a=audit_parser(__doc__).parse_args();canonical=O/'verification.json';check_output(a,canonical,G);before=protected_inputs()
    storage=read(D/'storage.json');assert len(storage)==11
    for item in storage:
        p=D/item['stored_file'];assert p.stat().st_size==item['stored_bytes'] and sha(p)==item['stored_sha256']
        receipt=read(D/(item['original_file']+'.receipt.json'));assert receipt['status']==200 and receipt['sha256']==item['original_sha256'] and receipt['bytes']==item['original_bytes']
        if item['codec']=='xz':
            with lzma.open(p,'rb') as f:
                h=hashlib.sha256();n=0
                for chunk in iter(lambda:f.read(8*1024*1024),b''):h.update(chunk);n+=len(chunk)
            assert n==receipt['bytes'] and h.hexdigest()==receipt['sha256']
        else:assert sha(p)==receipt['sha256'] and p.stat().st_size==receipt['bytes']
    spec=(D/'gtfs_reference.md').read_text();assert 'Regularly scheduled pickup' in spec and 'Regularly scheduled drop off' in spec
    wfs=read(D/'HALTESTELLEWLOGD.geojson')['features'];public=read(D/'OEFFHALTESTOGD.geojson')['features']
    assert len(wfs)==1807 and len(public)==10471 and all(x['properties']['DIVA_ID'] is None for x in public)
    assert any('Betriebshof' in x['properties']['BEZEICHNUNG'] for x in wfs)
    cal=rows(D/'calendar.txt');active={x['service_id'] for x in cal if x['start_date']<='20261110'<=x['end_date'] and x['tuesday']=='1'}
    for x in rows(D/'calendar_dates.txt'):
        if x['date']=='20261110':
            if x['exception_type']=='1':active.add(x['service_id'])
            else:assert x['exception_type']=='2';active.discard(x['service_id'])
    assert len(active)==94
    trips={x['trip_id']:x for x in rows(D/'trips.txt')};routes={x['route_id']:x for x in rows(D/'routes.txt')};stops={x['stop_id']:x for x in rows(D/'stops.txt')}
    assert len([t for t in trips.values() if t['service_id'] in active])==35541
    areas={x['DIVA']:x for x in rows(B/'stop_areas.csv',';')};names=defaultdict(set);positions=defaultdict(list);points=defaultdict(list)
    for k,x in areas.items():names[x['PlatformText']].add(k)
    for x in rows(B/'stop_positions.csv',';'):positions[x['DIVA']].append(x);points[xy(x['Longitude'],x['Latitude'])].append(x)
    rings=read(B/'vienna_boundary.geojson')['features'][0]['geometry']['coordinates']
    def in_ring(lon,lat,ring):
        x,y=float(lon),float(lat);inside=False
        for (x1,y1),(x2,y2) in zip(ring,ring[1:]):
            if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:inside=not inside
        return inside
    def inside(lon,lat):return in_ring(lon,lat,rings[0]) and not any(in_ring(lon,lat,r) for r in rings[1:])
    witnesses=rows(O/'station_witnesses.csv');assert len(witnesses)==len({x['DIVA'] for x in witnesses})==378
    expected={}
    for w in witnesses:
        k=w['DIVA'];p=areas[k];s=stops[w['GTFS_stop_id']];t=trips[w['trip_id']];route=routes[t['route_id']]
        assert names[w['name']]=={k} and p['PlatformText']==s['stop_name']==w['name'] and p['Municipality']=='Wien'
        assert t['service_id']==w['service_id'] and w['service_id'] in active and route['agency_id']=='04' and route['route_type']=='3' and re.fullmatch('[0-9]+A',route['route_short_name'])
        assert route['route_short_name']==w['route_short_name'] and t['route_id']==w['route_id']
        assert w['DIVA_longitude']==p['Longitude'] and w['DIVA_latitude']==p['Latitude']
        assert w['GTFS_longitude']==s['stop_lon'] and w['GTFS_latitude']==s['stop_lat']
        pp=points[xy(s['stop_lon'],s['stop_lat'])];assert {x['DIVA'] for x in pp}=={k} and {x['StopText'] for x in pp}=={w['name']}
        assert sorted(x['StopID'] for x in pp)==json.loads(w['native_StopIDs_json'])
        assert inside(p['Longitude'],p['Latitude']) and inside(s['stop_lon'],s['stop_lat'])
        assert all(inside(x['Longitude'],x['Latitude']) for x in positions[k])
        expected[w['trip_id'],w['stop_sequence'],w['GTFS_stop_id']]=w
    assert '60200810' not in {w['DIVA'] for w in witnesses}
    assert any(not inside(x['Longitude'],x['Latitude']) for x in positions['60200810'])
    found=set();total=0
    with stream(D/'stop_times.txt') as f:
        for x in csv.DictReader(f):
            total+=1;key=(x['trip_id'],x['stop_sequence'],x['stop_id'])
            if key not in expected:continue
            w=expected[key]
            for n in ['arrival_time','departure_time','pickup_type','drop_off_type']:assert w[n]==x[n]
            assert x['pickup_type'] in ['0',''] or x['drop_off_type'] in ['0',''];found.add(key)
    assert len(found)==378 and total==8853107
    f,lo,hi=revised_bounds();cities=f.city.tolist();i=cities.index('Vienna');j=NAMES.index('public_transport_density');value=378*100000/(50*2028399+378*100000)
    s=read(O/'summary.json');assert s['candidate_DIVA_groups']==378 and s['counts_not_added'] and s['primary_admissions']==s['actual_primary_width_reduction']==0
    bounds=rows(O/'bounds.csv');ranking=rows(O/'ranks.csv');assert len(bounds)==320 and len(ranking)==64
    for scenario in ['retained_V203','candidate_bus_subset']:
        ll=lo.tolist();hh=hi.tolist()
        if scenario=='candidate_bus_subset':ll[i][j]=value
        saved={(x['city'],x['indicator']):x for x in bounds if x['scenario']==scenario};assert len(saved)==160
        for c,city in enumerate(cities):
            for d,n in enumerate(NAMES):close(saved[city,n]['lower'],ll[c][d]);close(saved[city,n]['upper'],hh[c][d])
        for ref in ['fixed','equal']:
            w=[.1]*10 if ref=='equal' else [.05 if d in [6,9] else .1125 for d in range(10)]
            lower=[score(u,w) for u in ll];upper=[score(u,w) for u in hh];regret=[max(0,max(upper[k] for k in range(16) if k!=c)-lower[c]) for c in range(16)]
            rr={x['city']:x for x in ranking if (x['scenario'],x['weight_reference'])==(scenario,ref)};assert len(rr)==16
            for c,city in enumerate(cities):
                for n,v in [('score_lower',lower[c]),('score_upper',upper[c]),('max_regret',regret[c])]:close(rr[city][n],v)
                assert int(rr[city]['decision_rank'])==1+sum(v<regret[c]-1e-10 for v in regret)
                assert rr[city]['possible_champion']=='True' and upper[c]>=max(lower[k] for k in range(16) if k!=c)-1e-12
                assert rr[city]['necessary_champion']=='False' and lower[c]<max(upper[k] for k in range(16) if k!=c)-1e-12
                assert int(rr[city]['best_rank'])==1+sum(lower[k]>upper[c]+1e-12 for k in range(16) if k!=c)
                assert int(rr[city]['worst_rank'])==1+sum(upper[k]>lower[c]+1e-12 for k in range(16) if k!=c)
            case=next(x for x in s['cases'] if (x['scenario'],x['weight_reference'])==(scenario,ref))
            close(case['mean_width'],math.fsum(b-a for a,b in zip(lower,upper))/16)
            assert case['recommendations']==[cities[c] for c,r in enumerate(regret) if r<=min(regret)+1e-12]==(['Oslo'] if ref=='fixed' else ['Zurich'])
            assert case['possible_champions']==16 and case['necessary_champions']==0
    assert protected_inputs()==before
    for n,h in read(R/'results/current_paper_review/current_verification.json')['edition_source_sha256'].items():assert sha(R/n)==h,n
    files=[*sorted(D.iterdir()),*[O/n for n in ['README.md','summary.json','station_witnesses.csv','excluded_mixed_modes.csv','bounds.csv','ranks.csv','peer_review.json']],
        *[B/n for n in ['stop_areas.csv','stop_positions.csv','vienna_boundary.geojson','operator_ogd_index.html','ogd_schema.pdf']],R/'scripts/task4_current_vienna_gtfs_candidate.py',Path(__file__)]
    report=dict(status='pass structural candidate checks; public-service eligibility and full integration pending',**before,edition_entries_checked=24,
        HTTP200_originals_recovered=11,lossless_originals_recovered=2,service_day='20261110',witnesses_checked=378,all_known_native_positions_inside=True,
        cross_boundary_DIVA_excluded='60200810',GTFS_stop_time_rows_scanned=total,utility_bound_rows=320,scalar_city_cases=64,
        other159_lower_and_all160_upper_preserved=True,public_service_eligibility_certified=False,nonbus_alias_screen_exhaustive=False,
        primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
        source_sha256={str(p.relative_to(R)):sha(p) for p in files if p.is_file()},
        scope='Exact source-position corroboration and scheduled service-day witnesses, not real-time operation or uniform2025/student-access evidence. Candidate scores do not activate a primary model revision.')
    emit_report(report,a,canonical,G)
if __name__=='__main__':main()
