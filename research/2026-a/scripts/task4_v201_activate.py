"""Activate audited V200 science and V201 owned manuscript; preserve raw inputs."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v201_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
 v=read(O/'current_verification.json');d=read(O/'current_delivery_verification.json');visual=read(O/'visual_review.json');entry=v
 pdf=R.parents[1]/'paper/current/main.pdf';h=sha(pdf)
 assert all(a['status']=='pass' and a['pdf_sha256']==h for a in [v,d,visual,entry])
 assert v['main_and_references_pages']<=25 and v['total_pages']==d['total_pages']
 assert entry['main_entry']=='main.tex' and entry['all_pages_text_equal'] and entry['all_pages_render_equal']
 assert entry['team_original_preserved_byte_for_byte'] and not entry['server_compile_verified']
 proof=read(R/'results/task4_v200_transition/verification.json');assert proof['status']=='pass'
 for n,hsh in read(R/'design/task4_user_v200_snapshot.json')['source_sha256'].items():assert sha(R/n)==hsh,n
 for n,hsh in v['current_files_sha256'].items():assert sha(P/n)==hsh,n
 assert read(R/'design/task4_user_current_model.json')['version'] in ['V197','V200']
 assert read(R/'design/task4_user_current_review.json')['version'] in ['V198','V201']
 a=read(R/'design/task4_user_current_model.json');a.update(version='V200',module='task4_user_v200_revision',admissions='design/task4_user_v200_admissions.json',results='results/task4_user_v200_revision',snapshot='design/task4_user_v200_snapshot.json',source_policy='Original CSV values, years, flags, populations, weights, anchors and interval rules preserved; only Singapore pool lower refined from7 to25; other159cells and all160uppers unchanged',scope='25distinctsupplementedcity-indicatorkeys;112point37partial11unknown;Singapore25namedphysicalpublicvenues;fourpool-specificnoticesacrossthreevenuesandweeklymaintenancepreserved;22withholdingcaseisnotallopenorwholeclosureclaim;2026capturewithunstatedinventorydateanduser2024population6036900. Zurichconservative16possible0necessary.',activation_receipt='results/task4_v201_review/activation.json',frozen_bundle_metadata='Staged labels describe creation before paper integration; active registries govern current use')
 write(R/'design/task4_user_current_model.json',a)
 a=read(R/'design/task4_user_current_extensions.json');a.update(extension_version='V200',primary_evidence_version='V200',primary_snapshot='design/task4_user_v200_snapshot.json',independent_audit='results/task4_v200_transition/verification.json',audit_script='scripts/audit_task4_v200.py',manuscript_entry='../HiMCM-Overleaf/main.tex',root_review_entry='../HiMCM-Overleaf/main.tex',shared_main_entry='../HiMCM-Overleaf/main.tex',paper_verification='results/task4_v201_review/current_verification.json',supersedes='V197primary/extensions,V198ownedreviewanddelivery')
 for k,item in a['modules'].items():item.update(script='scripts/task4_v200_extensions.py '+k,results='results/task4_v200_'+k)
 write(R/'design/task4_user_current_extensions.json',a)
 review=dict(version='V201',primary_model='V200',primary_model_registry='research/2026-a/design/task4_user_current_model.json',review_workspace='HiMCM-Overleaf sibling repository',tex='main.tex',pdf='paper/current/main.pdf',pdf_workspace='HiMCM',source_mirror='paper/current/main.tex',root_entry='main.tex',shared_main_entry='main.tex',pdf_sha256=h,research_verification='research/2026-a/results/task4_v201_review/current_verification.json',role='Complete owned manuscript in current main; not final team submission',default_main_setting_changed=False,main_source_route_changed=True,teammate_original_archive='paper/history/overleaf_before_single_main_20261110/archive/team_main_before_owned_entry_20261110/main.tex',main_entry_verification='research/2026-a/results/task4_v201_review/current_verification.json',submission_ready=False,display_control_number='18213',display_number_provisional=True,actual_registered_number_verified=False,scope='V200 science and V201 owned paper consistent; physicalinventorynotaccess; adverse robustness and changed conditional choices included; frozenAI window unchanged')
 delivery=dict(version='V201',review_version='V201',primary_model='V200',pdf=review['pdf'],pdf_sha256=h,research_requirements='research/2026-a/results/task4_v201_review/requirements.csv',research_verification='research/2026-a/results/task4_v201_review/current_delivery_verification.json',paper_requirements=None,paper_verification=None,requirements=d['requirements'],pending_count=d['pending_count'],main_page_margin=25-v['main_and_references_pages'],submission_ready=False,server_compile_verified=False,role='Current scoped delivery evidence; local main build passed, team acceptance and contest submission remain pending')
 for name,value in [('review',review),('delivery',delivery)]:
  path=R/f'design/task4_user_current_{name}.json';write(path,value)
 activation=dict(status='active',primary='V200',extensions='V200',owned_review='V201',delivery='V201',pdf_sha256=h,scientific_snapshot_sha256=sha(R/'design/task4_user_v200_snapshot.json'),research_audit_sha256=sha(R/'results/task4_v200_transition/verification.json'),paper_audit_sha256=sha(O/'current_verification.json'),delivery_audit_sha256=sha(O/'current_delivery_verification.json'),visual_review_sha256=sha(O/'visual_review.json'),main_entry_verification_sha256=sha(O/'current_verification.json'),possible_champions=16,necessary_champions=0,conservative_recommendation='Zurich',education_priority='Singapore',fixed_resource_expansion='Singapore',submission_ready=False,goal_status='active')
 write(O/'activation.json',activation)
 print('Activated consistent V200/V201; goal remains active')
if __name__=='__main__':main()
