"""Extract a conservative Zone1 London Tube inventory candidate; no activation."""
import argparse,csv,gzip,hashlib,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
DEFAULT=Path('/data/datasets/HiMCM/source_archives/task4_v135_london/tube_stops_response_original.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inside(point,ring):
 x,y=point;result=False
 for a,b in zip(ring,ring[1:]+ring[:1]):
  if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:result=not result
 return result
def boundary_distance(point,ring):
 scale=111195.;cx=math.cos(math.radians(point[1]));q=(point[0]*scale*cx,point[1]*scale);minimum=math.inf
 for a,b in zip(ring,ring[1:]+ring[:1]):
  a=(a[0]*scale*cx,a[1]*scale);b=(b[0]*scale*cx,b[1]*scale);d=(b[0]-a[0],b[1]-a[1]);den=d[0]**2+d[1]**2
  t=max(0,min(1,((q[0]-a[0])*d[0]+(q[1]-a[1])*d[1])/den)) if den else 0
  minimum=min(minimum,math.hypot(q[0]-a[0]-t*d[0],q[1]-a[1]-t*d[1]))
 return minimum
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source-json',type=Path,default=DEFAULT);args=ap.parse_args()
 receipts=json.loads((HERE/'retrievals.json').read_text());receipt=receipts[0]
 body=args.source_json.read_bytes() if args.source_json.exists() else gzip.decompress((HERE/'tube_stops_original.json.gz').read_bytes())
 assert hashlib.sha256(body).hexdigest()==receipt['sha256'] and receipt['status']==200
 raw=json.loads(body);assert len(raw['stopPoints'])==raw['total']==raw['pageSize']==1751
 types=json.loads((HERE/'stop_types_response_original.json').read_text());assert 'NaptanMetroStation' in types
 stations=[(i,x) for i,x in enumerate(raw['stopPoints']) if x['stopType']=='NaptanMetroStation'];assert len(stations)==272
 chosen=[(i,x) for i,x in stations if any(a['key']=='Zone' and a['value']=='1' for a in x['additionalProperties'])];assert len(chosen)==62
 feature=json.loads((HERE/'london_region_bfc_original.geojson').read_text())['features'];assert len(feature)==1
 assert feature[0]['properties']['RGN25CD']=='E12000007' and feature[0]['properties']['RGN25NM']=='London'
 geom=feature[0]['geometry'];assert geom['type']=='MultiPolygon';polygons=geom['coordinates'];rings=[ring for polygon in polygons for ring in polygon]
 # Omit ambiguous nearby/connected named entities, rather than infer extra facilities.
 omit={'940GZZLUMMT':'Monument omitted as a precaution about the Bank/Monument connected complex',
       '940GZZLUERB':'Edgware Road Bakerloo omitted as a same-name precaution; no claim that the two stations share a paid complex'}
 groups={};omitted=[]
 for index,stop in chosen:
  assert stop['id']==stop['naptanId']==stop['stationNaptan'] and 'tube' in stop['modes'] and stop['lines']
  if stop['id'] in omit:omitted.append(dict(id=stop['id'],name=stop['commonName'],reason=omit[stop['id']]));continue
  assert any(inside((stop['lon'],stop['lat']),polygon[0]) and not any(inside((stop['lon'],stop['lat']),hole) for hole in polygon[1:]) for polygon in polygons)
  key=stop.get('hubNaptanCode') or stop['stationNaptan']
  row=groups.setdefault(key,dict(entity_key=key,station_ids=[],names=[],source_indices=[],points=[],lines=set()))
  row['station_ids'].append(stop['id']);row['names'].append(stop['commonName']);row['source_indices'].append(index)
  row['points'].append([stop['lon'],stop['lat']]);row['lines'].update(x['id'] for x in stop['lines'])
 assert len(groups)==59 and sum(len(x['station_ids']) for x in groups.values())==60
 assert sorted(groups['HUBPAD']['station_ids'])==['940GZZLUPAC','940GZZLUPAH']
 distances=[min(boundary_distance(point,ring) for ring in rings) for g in groups.values() for point in g['points']];assert min(distances)>0
 rows=[]
 for key,g in sorted(groups.items()):g['lines']=sorted(g['lines']);rows.append(g)
 (HERE/'station_entities.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
 with (ROOT/'data/task4_v117_team_intake/city_indicators.csv').open(encoding='utf-8-sig') as f:city=next(x for x in csv.DictReader(f) if x['city']=='London')
 assert city['population']=='9122909' and city['population_year']=='2025'
 density=59*100000/9122909;utility=density/(50+density)
 observations=[dict(city='London',indicator='public_transport_density',raw_count=59,population=9122909,population_year=2025,
  sourceyear=2026,access_date='2026-11-09',utility_before=[0,1],utility_after=[utility,1],utility_anchor=50,lower_bound_only=True,
  admission_status='candidate_only_independent_review_and_controlled_admission_pending',
  scope='Exact Zone1 NaptanMetroStation objects only, point-in-ONS London region E12000007; hub dedup plus two conservative omissions. Other modes/zones remain uncounted.',
  limitations='Static as-accessed inventory, not real-time opening, service frequency, student eligibility or individual accessibility. ONS2025 full-resolution coastline-clipped boundary used at representative station coordinates; boundary distances are diagnostic, not accuracy guarantees. Supplied2025 population unchanged/not externally rechecked. No complete city transport census.')]
 (HERE/'observations.json').write_text(json.dumps(observations,indent=2)+'\n')
 report=dict(status='candidate_extracted_not_admitted',raw_objects=1751,metro_station_objects=272,exact_zone1_station_ids=62,
  omitted=omitted,shared_hub_collapsed=['940GZZLUPAC','940GZZLUPAH'],candidate_entities=59,
  approximate_min_boundary_margin_metres=min(distances),density_lower=density,utility_candidate=[utility,1],
  extraction_source='uncompressed supplied file' if args.source_json.exists() else 'lossless gzip fallback',
  external_original=dict(path=receipt['local_original'],bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),url=receipt['url'],included_in_Git=False),
  lossless_original_archive=dict(file='tube_stops_original.json.gz',bytes=(HERE/'tube_stops_original.json.gz').stat().st_size,sha256=sha(HERE/'tube_stops_original.json.gz'),decompressed_sha256=hashlib.sha256(body).hexdigest()),
  source_hashes={p.name:sha(p) for p in [HERE/'london_region_bfc_original.geojson',HERE/'ons_bfc_layer_original.json',HERE/'stop_types_response_original.json']},
  population_original_unchanged=True,primary_admissions=0)
 (HERE/'extraction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['candidate_entities','approximate_min_boundary_margin_metres','density_lower','utility_candidate','primary_admissions']}))
if __name__=='__main__':main()
