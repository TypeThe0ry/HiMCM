"""Independent scalar recomputation of the isolated V202 transport preview."""
import csv,hashlib,json,math,pathlib,zipfile,xml.etree.ElementTree as ET
from collections import Counter
from task4_user_v202_revision import revised_bounds
from task4_v5_model import NAMES
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'results/current_transport_candidate'; D=R/'data/current_oslo_transport'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
science=read(R/'design/task4_user_v202_snapshot.json')['source_sha256'];assert len(science)==476
for p,h in science.items(): assert sha(R/p)==h,p
preview=read(O/'preview.json'); assert preview['science_bindings_verified']==476 and preview['primary_admissions']==0
assert preview['active_science']=='V202 unchanged'
for p,h in preview['source_sha256'].items():
 if not p.startswith('design/task4_user_current_'): assert sha(R/p)==h,p
with zipfile.ZipFile(D/'03_Oslo_latest.zip') as z:
 assert len(z.namelist())==1
 x=ET.fromstring(z.read(z.namelist()[0]))
ns={'n':'http://www.netex.org.uk/netex'}; raw=x.findall('.//n:StopPlace',ns)
with (D/'native_stopplaces.csv').open(newline='') as f: saved=list(csv.DictReader(f))
assert len(raw)==len(saved)==1257
fields={'name':'Name','longitude':'Centroid/Location/Longitude','latitude':'Centroid/Location/Latitude','mode':'TransportMode','stop_place_type':'StopPlaceType'}
def val(s,path):return s.findtext('/'.join('n:'+p for p in path.split('/')),default='',namespaces=ns)
def cv(s):
 d={'id':s.get('id'),'municipality_ref':'','parent_ref':''}
 for col,path in fields.items():d[col]=val(s,path)
 for col,path in [('municipality_ref','TopographicPlaceRef'),('parent_ref','ParentSiteRef')]:
  el=s.find('n:'+path,ns); d[col]=el.get('ref','') if el is not None else ''
 return d
raws=[cv(s) for s in raw]; assert len({r['id'] for r in raws})==1257
assert {r['id']:r for r in raws}=={r['id']:r for r in saved}
assert sum(r['municipality_ref']=='KVE:TopographicPlace:0301' for r in raws)==1256
f,lo,hi=revised_bounds();cities=f.city.tolist();oi=cities.index('Oslo');j=NAMES.index('public_transport_density');assert int(f.iloc[oi].population)==727797
refs={'fixed':[.1125]*6+[.05,.1125,.1125,.05],'equal':[.1]*10}
def score(row,w):
 good=math.sqrt(math.fsum(wi*float(v)**2 for wi,v in zip(w,row)));bad=math.sqrt(math.fsum(wi*(1-float(v))**2 for wi,v in zip(w,row)));return 100*good/(good+bad)
def compute(count,w):
 low=[list(map(float,row)) for row in lo]; upper=[list(map(float,row)) for row in hi];density=count*100000/727797;low[oi][j]=density/(50+density)
 L=[score(row,w) for row in low];U=[score(row,w) for row in upper]
 regret=[max(0,max(U[k] for k in range(16) if k!=i)-L[i]) for i in range(16)]
 possible=[U[i]>=max(L[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 necessary=[L[i]>=max(U[k] for k in range(16) if k!=i)-1e-12 for i in range(16)]
 return L,U,regret,possible,necessary
with (O/'scores.csv').open(newline='') as f: table=list(csv.DictReader(f))
assert len(table)==256
cases=0;gaps={}
for item in preview['comparisons']:
 ref=item['weight_reference'];n=item['count'];scenario=item['scenario'];L,U,G,P,N=compute(n,refs[ref]); subset=[r for r in table if r['weight_reference']==ref and r['scenario']==scenario];assert len(subset)==16
 assert item['possible_champions']==sum(P)==16 and item['necessary_champions']==sum(N)==0
 assert item['recommendation']==[cities[i] for i in range(16) if G[i]<=min(G)+1e-12]
 assert abs(item['Oslo_regret_gap_to_best_other']-(G[oi]-min(G[k] for k in range(16) if k!=oi)))<1e-10
 assert abs(item['mean_score_width']-math.fsum(u-l for l,u in zip(L,U))/16)<1e-10
 for i,city in enumerate(cities):
  r=next(r for r in subset if r['city']==city)
  for col,v in [('score_lower',L[i]),('score_upper',U[i]),('max_regret',G[i])]:assert abs(float(r[col])-v)<1e-10,(ref,scenario,city,col)
  assert (r['possible_champion']=='True')==P[i] and (r['necessary_champion']=='True')==N[i]
  cases+=1
 if n in (226,227,639,640):gaps[ref,n]=G[oi]-min(G[k] for k in range(16) if k!=oi)
assert cases==256
assert gaps['fixed',226]>0>gaps['fixed',227] and gaps['equal',639]>0>gaps['equal',640]
assert {r['weight_reference']:r['first_strict_integer_count'] for r in preview['thresholds']}=={'fixed':227,'equal':640}
for p,h in science.items():assert sha(R/p)==h,p
out={'status':'PASS','scope':'Independent scalar recomputation against revised V202 bounds and frozen preview; no new source admission.','city_weight_scenario_cases':cases,'source_bindings_verified':len(science),'xml_csv_all_fields_rows':len(saved),'oslo_0301_references':1256,'scenario_counts':[89,517,829,226,227,639,640],'first_strict_integer_counts':{'fixed':227,'equal':640},'threshold_neighbor_gaps':{f'{k[0]}_{k[1]}':v for k,v in gaps.items()},'all_scenarios_possible_champions':16,'all_scenarios_necessary_champions':0,'interpretation':'829 is a conditional NSR administrative inventory, not a proven physical-facility lower bound. 517 is an unvalidated clustering heuristic and is not admitted. Neither is added to 89. V202 remains active.','scope_limitation':'No claim that paper or navigation files stayed unchanged during audit; preview binds their historical hashes. HTTP capture metadata is not independent evidence of live status.','sha256':{str(p.relative_to(R)):sha(p) for p in [pathlib.Path(__file__),O/'preview.json',O/'scores.csv',D/'03_Oslo_latest.zip',D/'native_stopplaces.csv',D/'semantics_nsr.html',D/'semantics_nsr_metadata.json',D/'semantics_n801_metadata.json']}}
(O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
