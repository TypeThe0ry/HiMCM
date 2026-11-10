"""Recheck new workload/travel packets offline and preserve frozen science."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
R=Path(__file__).resolve().parents[1];O=R/'results/current_zurich_target_routes'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 if O.exists():raise ValueError('Frozen output exists; replay in scratch checkout')
 folders=[R/'data/current_zurich_vocational_workload_route',R/'data/current_zurich_schooltrip_route']
 sources=[p for folder in folders for p in folder.iterdir() if p.is_file()]
 sources += [Path(__file__),R/'data/task4_v117_team_intake/city_indicators.csv',R/'design/task4_user_v204_snapshot.json',R/'design/task4_user_v203_snapshot.json']
 pinned={str(p.relative_to(R)):sha(p) for p in sources}
 for folder,script in zip(folders,['verify.py','extract.py']):
  subprocess.run([sys.executable,str(folder/script)],check=True,stdout=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 for name,h in pinned.items():assert sha(R/name)==h,name
 receipts=[]
 for folder,manifest in zip(folders,['retrieval.json','retrievals.json']):
  for r in json.loads((folder/manifest).read_text()):
   p=folder/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
   receipts.append(r)
 assert len(receipts)==11
 scientific={}
 for name in ['task4_user_v203_snapshot.json','task4_user_v204_snapshot.json']:
  record=json.loads((R/'design'/name).read_text())
  for p,hsh in record['source_sha256'].items():
   assert p not in scientific or scientific[p]==hsh
   assert sha(R/p)==hsh,p
   scientific[p]=hsh
 assert len(scientific)==658
 assert sha(R/'data/task4_v117_team_intake/city_indicators.csv')=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 O.mkdir(parents=True)
 report=dict(status='pass offline Zurich source packets',source_sha256=pinned,
  archived_response_bodies=len(receipts),successful_response_bodies=sum(r['status']==200 for r in receipts),scientific_bindings_checked=len(scientific),
  offline_derived_files_unchanged=True,visual_source_review={'ABZH_2023_24_PDF_page36':'106 teacher persons;2261initial/78continuing learners;137classes','ABZH_2025_26_PDF_page1':'101 teacher persons;2452learners;age15-53;traininglist footnote excludescontinuing'},
  primary_admissions=0,actual_primary_width_reduction=0,changes_primary_model=False,changes_manuscript=False,
  scope='Measured city upper-stage teachingFTE and matching one-way travel distribution not established by these bounded routes. Headcounts/positionplans not actualFTE. Education-purpose microcensus paths may include returns,universities,courses; not directschooltrip bins. Planned2027 release is publisher plan,not verified future availability. Receipt/extract/visual checks do not prove source exhaustiveness, target coverage or census validity.')
 (O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','archived_response_bodies','successful_response_bodies','scientific_bindings_checked','primary_admissions']}))
if __name__=='__main__':main()
