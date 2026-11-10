"""Reconcile published Zurich point records and municipal geometry; no count admission."""
from pathlib import Path
from html.parser import HTMLParser
import collections,csv,hashlib,json,math,sys
import shapely
from shapely.geometry import Point,shape
D=Path(__file__).resolve().parent;R=D.parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';O=R/'results/current_zurich_transit_boundary_followup'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,value):p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
class Text(HTMLParser):
 def __init__(self):super().__init__();self.parts=[]
 def handle_data(self,s):self.parts.append(s)
def text(p):
 a=Text();a.feed(p.read_text());return ' '.join(' '.join(a.parts).split())
def csvout(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 snapshot=read(R/'design/task4_user_v204_snapshot.json');science={**snapshot['upstream_source_sha256'],**snapshot['source_sha256']};assert len(science)==658
 protected={R/n:h for n,h in science.items()};proof=read(R/'results/current_paper_review/current_verification.json')
 for n,h in proof['current_files_sha256'].items():protected[P/n]=h;protected[G/'paper/current'/n]=h
 protected[G/'paper/current/main.pdf']=proof['pdf_sha256'];assert all(sha(p)==h for p,h in protected.items())
 receipts=read(D/'retrievals.json');assert len(receipts)==13
 for r in receipts:assert r['status']==200 and sha(D/r['file'])==r['sha256'] and (D/r['file']).stat().st_size==r['bytes']
 metadata=text(D/'stops_metadata.html');assert 'Die Haltestellen können redundant in diesen drei Kategorien vorkommen.' in metadata
 assert 'Bahnstationen und dazugehörige Bushaltestellen wurden immer getrennt erfasst' in metadata
 assert '14.12.2025' in metadata and '30.01.2026' in text(D/'boundary_metadata.html')
 bd=read(D/'zurich_municipal_boundary.geojson');assert bd['numberMatched']==len(bd['features'])==1
 feature=bd['features'][0];assert feature['properties']['bfs']==261 and feature['properties']['gemeindename']=='Zürich'
 polygon=shape(feature['geometry']);assert polygon.is_valid and polygon.geom_type=='Polygon'
 oldpath=R/'data/current_zurich_transport/kanton_zh_wfs.geojson';old=read(oldpath);assert sha(oldpath)==read(oldpath.parent/'provenance.json')['sha256'];assert old['numberMatched']==len(old['features'])==3004
 assert bd['crs']==old['crs']=={'type':'name','properties':{'name':'urn:ogc:def:crs:EPSG::2056'}}
 spatial=[];mismatch=[];inside=[]
 for f in old['features']:
  a=f['properties'];q=shape(f['geometry']);assert q.geom_type=='Point';assert q.x==a['x_koord'] and q.y==a['y_koord']
  yes=polygon.covers(q);row=dict(nhstid=a['nhstid'],name=a['chstname'],cname=a['cname'],x=q.x,y=q.y,inside_bfs261_polygon=yes,has_listed_lines=bool(a['linien']),boundary_distance_m=q.distance(polygon.boundary))
  spatial.append(row)
  if yes:inside.append(f)
  if yes!=(a['cname']=='Zürich'):mismatch.append(row)
 assert len(inside)==478 and len(mismatch)==3 and sum(x['properties']['linien']!='' for x in inside)==460
 assert {r['nhstid'] for r in mismatch}=={'8511418','8591128','8591297'}
 national=[]
 for offset in range(0,579,100):
  p=D/f'national_ordered_{offset}.json';r=read(p);assert r['total_count']==579 and len(r['results'])==min(100,579-offset)
  national+=r['results']
 assert len(national)==len({r['number'] for r in national})==579
 assert [r['number'] for r in national]==sorted(r['number'] for r in national)
 assert all(r['fsonumber']=='261' and r['municipalityname']=='Zürich' for r in national)
 assert all(polygon.covers(Point(r['lv95east'],r['lv95north'])) for r in national)
 types=collections.Counter(r['stop_type'] or 'null' for r in national);assert types=={'ORDERLY':473,'ON_REQUEST':5,'null':101}
 keyed={r['number']:r for r in national};cross=[]
 for f in inside:
  a=f['properties'];b=keyed.get(a['nhstid']);x,y=f['geometry']['coordinates']
  cross.append(dict(nhstid=a['nhstid'],wfs_name=a['chstname'],wfs_has_listed_lines=bool(a['linien']),exact_number_match=b is not None,national_name=b['designationofficial'] if b else '',national_sloid=b['sloid'] if b else '',national_stop_type=b['stop_type'] if b else '',national_status=b['status'] if b else '',coordinate_difference_m=math.hypot(x-b['lv95east'],y-b['lv95north']) if b else ''))
 assert sum(r['exact_number_match'] for r in cross)==474
 assert {r['nhstid'] for r in cross if not r['exact_number_match']}=={'8503044','8503449','8516661','8585407'}
 O.mkdir(exist_ok=True);csvout('wfs_geometry.csv',spatial);csvout('mismatches.csv',mismatch);csvout('national_crosswalk.csv',cross)
 csvout('national_inventory.csv',[dict(number=a['number'],sloid=a['sloid'],name=a['designationofficial'],stop_type=a['stop_type'] or '',status=a['status'],fsonumber=a['fsonumber'],means_of_transport=a['means_of_transport'] or '',x=a['lv95east'],y=a['lv95north'],inside_bfs261_polygon=True) for a in national])
 summary=dict(primary_model='V204 unchanged',wfs_total=3004,exact_name_records=479,geometry_inside_records=478,geometry_inside_with_listed_lines=460,name_geometry_mismatches=mismatch,national_municipal_query_records=579,national_type_counts=dict(types),national_all_inside_polygon=True,exact_DiDok_matches_among_478=474,unmatched_in_municipal_query=[r['nhstid'] for r in cross if not r['exact_number_match']],boundary_data_label='30.01.2026',stop_data_label='14.12.2025',national_scope='Six ordered pages of municipal query, archived within two seconds; daily current publication, not an immutable national version or historical 2025 census.',geometry_scope='Published representative points against published municipal polygon; no conversion of nominal accuracy into a hard error envelope.',identifier_scope='Exact nhstid/number string equality for same documented DiDok namespace; no diva_nr, prefix, parent, name or proximity inference. This does not merge operational points into commercial or physical stops.',primary_admissions=0,actual_primary_width_reduction=0,baseline_446_unchanged=True,remaining_gate='Comparable unique commercial/physical stop grouping and qualifying service; record identifiers, ORDERLY type and listed lines do not by themselves prove this.')
 write(O/'summary.json',summary)
 files=[p for p in D.iterdir() if p.is_file()]+[oldpath,oldpath.parent/'provenance.json',R/'design/task4_user_v204_snapshot.json',R/'data/task4_v117_team_intake/city_indicators.csv',R/'results/current_swiss_servicepoint_followup/verification.json',R/'results/current_zurich_wfs_inventory/verification.json']
 changed=[str(p) for p,h in protected.items() if sha(p)!=h];assert not changed
 report=dict(status='pass spatial and exact-identifier reconciliation',source_sha256={str(p.relative_to(R)):sha(p) for p in files},output_sha256={n:sha(O/n) for n in ['wfs_geometry.csv','mismatches.csv','national_crosswalk.csv','national_inventory.csv','summary.json']},input_protection=dict(scientific_files=658,paper_dependencies_each_copy=7,canonical_PDF=1,changed=changed),environment=dict(python=sys.version.split()[0],shapely=shapely.__version__),primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,scope='Archived municipal query and coordinate/identifier checks; not unique commercial-stop counting, observed-service verification, original446 lineage or all-national roster validation.')
 write(O/'verification.json',report);print(json.dumps({k:summary[k] for k in ['geometry_inside_records','geometry_inside_with_listed_lines','national_municipal_query_records','exact_DiDok_matches_among_478','primary_admissions']}))
if __name__=='__main__':main()
