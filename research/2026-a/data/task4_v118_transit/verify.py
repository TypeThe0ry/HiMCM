"""Offline Oslo metro-only lower-bound extraction; no network required."""
import csv
import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def in_ring(x, y, vertices):
    inside = False
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        if (a[1] > y) != (b[1] > y):
            if x < (b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
                inside = not inside
    return inside

def main():
    stops = json.loads((ROOT/'oslo_stops_raw.json').read_text())
    boundary = json.loads((ROOT/'oslo_boundary_raw.json').read_text())
    assert boundary['kommunenummer'] == '0301'
    assert not stops.get('exceededTransferLimit', False)
    assert stops['spatialReference']['wkid'] == 4326
    features = stops['features']
    assert len(features) == len({f['attributes']['objectid'] for f in features}) == 2109
    polygons = boundary['omrade']['coordinates']
    def within(f):
        x,y=f['geometry']['x'],f['geometry']['y']
        return any(in_ring(x,y,p[0]) and not any(in_ring(x,y,h) for h in p[1:]) for p in polygons)
    groups = defaultdict(list)
    for f in features:
        a=f['attributes']
        if within(f) and a['transporttype']=='Tbane' and a['holdeplasstype']=='Tbanestasjon':
            assert a['navn'] and a['navn'].strip()==a['navn']
            groups[a['navn']].append(f)
    # Same name across platforms/lines counted once. This is a metro-only subset.
    assert len(groups)==89 and sum(map(len,groups.values()))==186
    distances=[]
    for a in groups:
        for b in groups:
            if a<b:
                distances.append(min(math.hypot((f['geometry']['x']-g['geometry']['x'])*55600,
                                               (f['geometry']['y']-g['geometry']['y'])*111200)
                                     for f in groups[a] for g in groups[b]))
    assert min(distances)>200
    population=727797
    n=len(groups)
    density=n*100000/population
    utility=density/(50+density)
    dates=sorted({datetime.fromtimestamp(f['attributes']['kopidato']/1000,timezone.utc).isoformat() for f in features})
    observation={
        'city':'Oslo','indicator':'public_transport_density',
        'utility_before':[0,1],'utility_after':[utility,1],
        'raw_count':n,'population':population,'density_per_100000_lower':density,
        'sourceyear':2026,'scope':'Oslo municipality 0301; named metro stations only, platforms deduplicated by exact station name',
        'source_locator':json.loads((ROOT/'request_urls.json').read_text())['stops'],
        'lower_bound_only':True,'upper_bound_only':False,
        'admission_condition':'2026 observed infrastructure subset; not asserted as a 2025 count. Population remains user attachment 727797.',
        'limitations':'Current municipal map omits stable Entur StopPlace identifiers. Restriction to metro station names avoids bus and cross-mode alias ambiguity. Count is not a full all-mode inventory.'
    }
    (ROOT/'observations.json').write_text(json.dumps([observation],indent=2)+'\n')
    with (ROOT/'oslo_metro_station_subset.csv').open('w') as stream:
        writer=csv.writer(stream);writer.writerow(['station_name','platform_records','objectids'])
        for name,fs in sorted(groups.items()):
            writer.writerow([name,len(fs),';'.join(str(f['attributes']['objectid']) for f in fs)])
    summary={'all_source_records':len(features),'all_in_boundary_records':sum(map(within,features)),
             'metro_platform_records':186,'metro_distinct_names':n,'minimum_different_station_platform_separation_approx_m':min(distances),
             'source_copy_timestamps_utc':dates,'utility_lower':utility,
             'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                             for name in ['oslo_stops_raw.json','oslo_boundary_raw.json','map_metadata_raw.json']}}
    (ROOT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
