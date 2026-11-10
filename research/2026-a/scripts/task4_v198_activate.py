"""Activate the independently checked V197/V198 pair; no scientific data edits."""
from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v198_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 v=read(O/'verification.json');d=read(O/'delivery_verification.json')
 assert v['status']==d['status']=='pass' and v['pdf_sha256']==d['pdf_sha256']==sha(P/'drafts/task4_v198_paper.pdf')
 assert v['total_pages']==d['total_pages']==27 and v['main_and_references_pages']==d['main_and_references_pages']==25
 for n,h in read(R/'design/task4_user_v197_snapshot.json')['source_sha256'].items():assert sha(R/n)==h,n
 for n,h in v['tex_source_sha256'].items():assert sha(P/n)==h,n
 assert read(R/'design/task4_user_current_model.json')['version'] in ['V192','V197']
 assert read(R/'design/task4_user_current_review.json')['version'] in ['V196','V198']
 visual=dict(status='pass',pdf_sha256=v['pdf_sha256'],all27pages_layout_contact_sheets_viewed=True,full_page_visual_checks=[6,10,13,14,15,24,27],render_dpi=96,notes='Poolrestrictions,correctedarithmetic,single/jointmeans,futurestressandpreferences,meanrankguarantee,ZurichreferenceandfrozenAIchecked;nooverlap/clippingobserved',figure_font_inserted_pt=[10,12.596899224806203],body_and_header_pt=[12,11],native_letter=True,empty_footers=True,provisional_control='18213',server_compile_verified=False,scope='All-page layout overview and7selected full pages; not exhaustive manual source certification')
 write(O/'visual_review.json',visual)
 a=read(R/'design/task4_user_current_model.json');a.update(version='V197',module='task4_user_v197_revision',admissions='design/task4_user_v197_admissions.json',results='results/task4_user_v197_revision',snapshot='design/task4_user_v197_snapshot.json',source_policy='OriginalCSVvalues/years/flags,populations,weights,anchorsandintervalrulespreserved;onlyexistingZurichpoollowerrefined7to12;other159cells/all160uppersunchanged',scope='25distinctsupplementedcity-indicatorkeys;112point37partial11unknown;12Zurichvenueswith5limited-public-session schoolpools;adult-onlyKügelilooexcluded;2026captureinventorydateunstatedwithretained2025population;facilitysupplynotuniversalteenaccess. Zurichconservative16possible0necessary.',activation_receipt='results/task4_v198_review/activation.json',frozen_bundle_metadata='V197stagedlabelsrecordcreationbeforeV198paperintegration;currentregistriesgovernactivation')
 write(R/'design/task4_user_current_model.json',a)
 a=read(R/'design/task4_user_current_extensions.json');a.update(extension_version='V197',primary_evidence_version='V197',primary_snapshot='design/task4_user_v197_snapshot.json',independent_audit='results/task4_v197_transition/verification.json',audit_script='scripts/audit_task4_v197.py',manuscript_entry='../HiMCM-Overleaf/drafts/task4_v198_paper.tex',root_review_entry='../HiMCM-Overleaf/task4_v198_review_entry.tex',paper_verification='results/task4_v198_review/verification.json',supersedes='V192primary/extensions,V196ownedreviewanddelivery')
 for k,entry in a['modules'].items():entry.update(script='scripts/task4_v197_extensions.py '+k,results='results/task4_v197_'+k)
 write(R/'design/task4_user_current_extensions.json',a)
 for name in ['review','delivery']:
  path=R/f'design/task4_user_current_{name}.json';a=read(path)
  a=json.loads(json.dumps(a).replace('V196','V198').replace('v196','v198').replace('V192','V197'));a['pdf_sha256']=v['pdf_sha256']
  if name=='review':a['scope']='CurrentV197scienceandV198ownedreview;necessaryevidence,numericalresultsandsourceconditionsupdated;frozenAIwindowpreserved'
  else:a.update(research_verification='research/2026-a/results/task4_v198_review/delivery_verification.json',paper_verification='drafts/task4_v198_verification/delivery_verification.json')
  write(path,a);shutil.copy2(path,P/f'drafts/task4_current_{name}.json')
 for path in [R.parents[1]/'AGENTS.md',P/'AGENTS.md']:
  s=path.read_text().replace('**user16 V192**','**user16 V197**').replace('with V192 controlled extensions','with V197 controlled extensions').replace('are user16 V192','are user16 V197').replace('(primary science V192;','(primary science V197;')
  if path==P/'AGENTS.md':s=s.replace('V193 is the frozen preceding review. V196 corrects only the printed Milan tariff update month; its body and science remain unchanged.','V196 is the frozen preceding review. V198 integrates the verified V197 pool refinement and retains the September tariff-date correction.')
  path.write_text(s)
 activation=dict(status='active',primary='V197',extensions='V197',owned_review='V198',delivery='V198',pdf_sha256=v['pdf_sha256'],scientific_snapshot_sha256=sha(R/'design/task4_user_v197_snapshot.json'),research_audit_sha256=sha(R/'results/task4_v197_transition/verification.json'),paper_audit_sha256=sha(O/'verification.json'),delivery_audit_sha256=sha(O/'delivery_verification.json'),unique_supplement_keys=25,refined_existing_cells=1,newly_filled_cells=0,possible_champions=16,necessary_champions=0,conservative_recommendation='Zurich',submission_ready=False,goal_status='active')
 write(O/'activation.json',activation)
 target=P/'drafts/task4_v198_verification';target.mkdir(exist_ok=True)
 for n in ['verification.json','delivery_verification.json','requirements.csv','anchor_hits.csv','visual_review.json','source_check.json','matrix_figure_audit.json']:shutil.copy2(O/n,target/n)
 print('V197/V198active;scientificdataandteammatecontentunchanged')
if __name__=='__main__':main()
