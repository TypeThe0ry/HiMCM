"""Offline reproduction of archived PID inventory and new source packets."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parents[1];O=R/'results/current_prague_source_review/verification.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise ValueError('Preserve frozen proof; replay in scratch checkout')
 import bs4
 assert bs4.__version__=='4.14.3'
 dirs=[R/'data/current_prague_node_semantics',R/'data/current_prague_bus_node_candidate',R/'results/current_prague_bus_node_candidate',R/'results/current_prague_bus_crosswalk',R/'results/current_prague_bus_candidate_preview']
 paths=[p for folder in dirs for p in folder.iterdir() if p.is_file()]
 old=R/'data/task4_v127_prague';req=json.loads((old/'retrieval_requests.json').read_text())
 paths += [old/r['file'] for r in req]+[old/'retrieval_requests.json',old/'manifest.json',old/'station_complexes.csv',Path(__file__),R/'data/task4_v117_team_intake/city_indicators.csv',R/'design/task4_user_v203_snapshot.json',R/'design/task4_user_v204_snapshot.json']
 pinned={str(p.relative_to(R)):sha(p) for p in paths}
 for script in [R/'data/current_prague_bus_node_candidate/inventory.py',R/'results/current_prague_bus_crosswalk/extract.py']:
  subprocess.run([sys.executable,str(script)],check=True,stdout=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 for p,h in pinned.items():assert sha(R/p)==h,p
 new=json.loads((dirs[0]/'manifest.json').read_text())['requests']
 for item in new:
  p=dirs[0]/item['file'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
 assert len(new)==9
 # Verify both upstream scientific manifests in addition to the source packets.
 science={}
 for name in ['task4_user_v203_snapshot.json','task4_user_v204_snapshot.json']:
  for p,h in json.loads((R/'design'/name).read_text())['source_sha256'].items():
   assert p not in science or science[p]==h
   assert sha(R/p)==h,p
   science[p]=h
 assert len(science)==658
 assert sha(R/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 peer=R/'results/current_prague_source_review/peer_review.json';p=json.loads(peer.read_text())
 maps=[v for k,v in p.items() if isinstance(v,dict) and k.endswith('sha256')]
 assert maps
 for mapping in maps:
  for name,h in mapping.items():assert sha(R/name)==h,name
 pinned[str(peer.relative_to(R))]=sha(peer)
 report=dict(status='pass offline Prague packet reproduction',source_sha256=pinned,new_original_HTTP_bodies=9,reused_archived_response_bodies=21,scientific_bindings_checked=658,derived_outputs_byte_identical=True,parser_dependency='beautifulsoup4==4.14.3; Python html.parser; isolated uv environment',primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,scope='File identity and reproducibility plus separately recorded independent parser/scalar review. Source-defined cross-snapshot associations do not certify distinct physical facilities, day service, current-year census or primary admission; completeGTFSnotobtained. No MC replay or server build verification.')
 O.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','new_original_HTTP_bodies','reused_archived_response_bodies','scientific_bindings_checked']}))
if __name__=='__main__':main()
