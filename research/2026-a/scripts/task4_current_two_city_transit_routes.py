"""Verify the two bounded acquisition packets offline; no model mutation."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parents[1]
O=R/'results/current_two_city_transit_routes'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise ValueError('Preserve frozen output; use a scratch checkout for replay')
 folders=[R/'data/current_helsinki_stoparea_route',R/'data/current_dublin_stoparea_route']
 sources=[p for folder in folders for p in folder.iterdir() if p.is_file()]
 sources += [Path(__file__),R/'data/task4_v117_team_intake/city_indicators.csv',R/'design/task4_user_v204_snapshot.json',R/'design/task4_user_v203_snapshot.json']
 pinned={str(p.relative_to(R)):sha(p) for p in sources}
 # Both offline extractors must reproduce exactly the archived derived bytes.
 for folder in folders:
  subprocess.run([sys.executable,str(folder/'extract.py')],check=True,stdout=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 subprocess.run([sys.executable,str(folders[0]/'summarize.py')],check=True,stdout=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 for name,h in pinned.items():assert sha(R/name)==h,name
 receipts=0
 for folder,manifest,field in [(folders[0],'http_manifest.json','body'),(folders[1],'manifest.json','file')]:
  for r in json.loads((folder/manifest).read_text()):
   if r.get(field):
    p=folder/r[field];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes'];receipts+=1
   assert not any(k.lower() in ('set-cookie','cookie','authorization') for k in r.get('response_headers',{}))
 h=json.loads((folders[0]/'inventory_summary.json').read_text())
 assert (h['distinct_area_ids'],h['mapped_distinct_stops'],h['unknown_stop_ids'],h['unknown_area_ids'],h['stops_in_multiple_areas'])==(4715,8266,0,0,0)
 assert h['h_prefix_stop_codes']==h['h_prefix_stops_with_area']==2636
 d=json.loads((folders[1]/'extract.json').read_text())
 assert d['admitted_stop_count'] is None and not d['hierarchy_observed']
 assert set(d['download_statuses'].values())=={403}
 assert sha(R/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 # Independently check the 658 frozen scientific file bindings.
 scientific={}
 for name in ['task4_user_v203_snapshot.json','task4_user_v204_snapshot.json']:
  record=json.loads((R/'design'/name).read_text())
  for p,hsh in record['source_sha256'].items():
   assert p not in scientific or scientific[p]==hsh
   assert sha(R/p)==hsh,p
   scientific[p]=hsh
 assert len(scientific)==658,len(scientific)
 O.mkdir(parents=True)
 report=dict(status='pass offline route packets',source_sha256=pinned,
  archived_response_bodies=receipts,scientific_bindings_checked=len(scientific),
  offline_derived_files_unchanged=True,primary_admissions=0,actual_primary_width_reduction=0,
  changes_primary_model=False,changes_manuscript=False,
  scope='HSL native membership integrity is verified, not physical-stop semantics, city geography or dated service. Dublin linked feeds returned403; no populated hierarchy obtained. Direct HSL documentation requests also returned403; text-only web reading is not an archived successful source body. Numeric counts are feed diagnostics, not admitted city facilities. No server compilation claim.')
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','archived_response_bodies','scientific_bindings_checked','primary_admissions']}))
if __name__=='__main__':main()
