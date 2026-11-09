"""Independent geometry/record audit and read-only candidate effect preview."""
from pathlib import Path
import gzip,hashlib,json,sys
import numpy as np
from matplotlib.path import Path as PolygonPath
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from task4_user_v130_revision import revised_bounds
from task4_v5_model import NAMES
from task4_user_city_indicators import evaluate

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 extract=read(HERE/'extraction.json');original=Path(extract['external_original']['path']);body=gzip.decompress((HERE/'tube_stops_original.json.gz').read_bytes());assert hashlib.sha256(body).hexdigest()==extract['external_original']['sha256']
 assert sha(HERE/'tube_stops_original.json.gz')==extract['lossless_original_archive']['sha256']
 if original.exists():assert original.read_bytes()==body
 assert all(sha(HERE/p)==h for p,h in extract['source_hashes'].items())
 raw=json.loads(body);stations={x['id']:x for x in raw['stopPoints'] if x['stopType']=='NaptanMetroStation'};assert len(stations)==272
 entities=read(HERE/'station_entities.json');assert len(entities)==59
 source_ids=[sid for e in entities for sid in e['station_ids']];assert len(source_ids)==len(set(source_ids))==60
 assert not {'940GZZLUMMT','940GZZLUERB'} & set(source_ids)
 polygon=read(HERE/'london_region_bfc_original.geojson')['features'][0]
 assert polygon['properties']['RGN25CD']=='E12000007';polygons=polygon['geometry']['coordinates']
 assert polygon['geometry']['type']=='MultiPolygon'
 for entity in entities:
  assert len(set((stations[x].get('hubNaptanCode') or x) for x in entity['station_ids']))==1
  for sid,index,point in zip(entity['station_ids'],entity['source_indices'],entity['points']):
   stop=stations[sid];assert raw['stopPoints'][index]==stop
   assert any(p['key']=='Zone' and p['value']=='1' for p in stop['additionalProperties'])
   assert stop['modes']==['tube'] or 'tube' in stop['modes']
   assert point==[stop['lon'],stop['lat']] and stop['lines']
   assert any(PolygonPath(np.asarray(poly[0])).contains_point(point) and not any(PolygonPath(np.asarray(hole)).contains_point(point) for hole in poly[1:]) for poly in polygons)
 snapshot=read(ROOT/'design/task4_user_v130_snapshot.json');protected=dict(snapshot['source_sha256'])
 protected['design/task4_user_current_model.json']=sha(ROOT/'design/task4_user_current_model.json')
 for v in ['128','131']:protected.update(read(ROOT/f'results/task4_v{v}_revision/audit.json')['result_sha256'])
 assert all(sha(ROOT/p)==h for p,h in protected.items())
 frame,lo,hi=revised_bounds();i=frame.city.tolist().index('London');j=NAMES.index('public_transport_density')
 assert [lo[i,j],hi[i,j]]==[0,1] and frame.iloc[i].population==9122909
 obs=read(HERE/'observations.json')[0];u=59/(9122909/2000+59);np.testing.assert_allclose(obs['utility_after'],[u,1],atol=1e-15,rtol=0)
 after=lo.copy();after[i,j]=u;keep=np.ones(lo.shape,bool);keep[i,j]=False;np.testing.assert_array_equal(after[keep],lo[keep])
 def score(a,w):
  d=np.linalg.norm(a*np.sqrt(w),axis=1);g=np.linalg.norm((1-a)*np.sqrt(w),axis=1);return 100*d/(d+g)
 previews=[]
 for ref,w in [('fixed',np.array([.1125]*6+[.05,.1125,.1125,.05])),('equal',np.ones(10)/10)]:
  a,b,c=score(lo,w),score(after,w),score(hi,w)
  regret=np.array([max(0,max(np.delete(c,k))-b[k]) for k in range(16)])
  produced=evaluate(frame.city.tolist(),after,hi,w)
  np.testing.assert_allclose(produced.score_lower,b,atol=1e-12,rtol=0);np.testing.assert_allclose(produced.max_regret,regret,atol=1e-12,rtol=0)
  previews.append(dict(weight_reference=ref,London_score_lower_before=float(a[i]),London_score_lower_candidate=float(b[i]),mean_width_before=float(np.mean(c-a)),mean_width_candidate=float(np.mean(c-b)),relative_width_reduction_percent=float(100*np.mean(b-a)/np.mean(c-a)),conservative_choice=frame.iloc[int(np.argmin(regret))].city,possible_champions=int(produced.possible_champion.sum()),necessary_champions=int(produced.necessary_champion.sum()),London_decision_rank=int(produced.iloc[i].decision_rank),interpretation='Candidate assumption only,not admitted primary evidence'))
 assert all(sha(ROOT/p)==h for p,h in protected.items())
 report=dict(status='pass',audit_scope='Conditional native operator station/hub inventory qualified; controlled primary admission and complete analysis/paper migration pending',candidate_entities=59,source_station_ids=60,independent_polygon_checks=60,primary_admissions=0,
  inventory_not_live_service=True,raw_original_outside_Git=True,raw_original_sha256=hashlib.sha256(body).hexdigest(),lossless_original_archive_in_Git=True,source_hashes=extract['source_hashes'],protected_scientific_files=len(protected),previews=previews,
  candidate_files_sha256={p.name:sha(p) for p in [HERE/'extract.py',HERE/'observations.json',HERE/'station_entities.json',HERE/'extraction.json']},own_script_sha256=sha(Path(__file__)))
 (HERE/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='pass',candidate_entities=59,previews=previews),indent=2))
if __name__=='__main__':main()
