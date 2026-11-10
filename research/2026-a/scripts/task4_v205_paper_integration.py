"""Activate reviewed V205 sources and bind the single current manuscript locally."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
import task4_v198_reproduce as base
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';C=R/'results/current_paper_review';O=R/'results/task4_v205_paper_integration';B=Path('/data/scratch/himcm-v205-paper-build')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def checked_review():
 p=O/'independent_review.json';review=read(p);assert review['status'].startswith('pass')
 for name,h in review['reviewed_sha256'].items():assert sha(Path(name))==h,name
 for name,h in review['review_evidence_sha256'].items():assert sha(R/name)==h,name
 return p

def prepare():
 checked_review();O.mkdir(exist_ok=True)
 backups={'current_verification.json':C/'current_verification.json','delivery_verification.json':C/'delivery_verification.json','activation.json':C/'activation.json','model.json':R/'design/task4_user_current_model.json'}
 for n,p in backups.items():
  dest=O/('previous_v204_'+n)
  if not dest.exists():shutil.copyfile(p,dest)
 old=read(O/'previous_v204_current_verification.json');assert old['primary_model']=='V204'
 for n in ['mcmthesis.cls','ref.bib','figures/country_contrasts.pdf','figures/walktime_context.pdf']:assert sha(P/n)==old['current_files_sha256'][n],n
 for n in old['current_files_sha256']:
  dest=G/'paper/current'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/n,dest)
 shutil.copyfile(B/'main.pdf',G/'paper/current/main.pdf')
 path=R/'design/task4_user_current_model.json';d=read(path)
 d.update(version='V205',module='task4_user_v205_revision',admissions='design/task4_user_v205_admissions.json',results='results/task4_user_v205_revision',snapshot='design/task4_user_v205_snapshot.json',scientific_verification='results/task4_v205_transition/verification.json',operational_rebase='results/task4_v205_operational_rebase/verification.json',activation_status='active_science_and_locally_reviewed_paper',source_policy='Original CSV years flags populations weights anchors and interval rules retained; only Prague transit lower57to942source-definedscheduledbusnodes; other159lower/all160upper unchangedfromV204',scope='25distinctsupplementedkeys;112point37partial11unknown.942PraguePIDnodesreplace57metro,notadded;50ordinary+892publicdriver-requestwitnesses onservice_day20261110 withoriginal2025population1407084. Source-definedunitandprovideradministrativecityclassification;notphysical-sitecensus,actualoperationoruniversalaccess. FixedOslo/equalZurichconservative;16possible0necessary.',activation_receipt_status='V205 local scientific and paper activation bound; clean-HEAD reproduction and remote synchronization have separate receipts')
 write(path,d)
 path=R/'design/task4_user_current_extensions.json';d=read(path);d.update(extension_version='V205',primary_evidence_version='V205',primary_snapshot='design/task4_user_v205_snapshot.json',independent_audit='results/task4_v205_transition/verification.json',audit_script='scripts/audit_task4_v205.py',supersedes='V204 science and paper; historical staging labels describe generation time')
 for k in d['modules']:d['modules'][k]={'script':'scripts/task4_v205_extensions.py','results':'results/task4_user_v205_extensions/'+k}
 for key,folder,script in [('source_scope_addendum','task4_v205_commute_scope','task4_v205_commute_scope'),('point_uncertainty_addendum','task4_v205_point_error','task4_v205_point_error')]:
  d[key].update(script='scripts/'+script+'.py',results='results/'+folder,verification='results/'+folder+'/verification.json',verification_sha256=sha(R/'results'/folder/'verification.json'))
 d['point_uncertainty_addendum']['scope']='CurrentV205 expanded point-utility boxes with padded numerical enclosures/Decimal80 checks; not directed-rounding certification,rawerrorpercentage,calibrationor everyrealizeddataset.'
 d['source_diagnostics_addendum']={'script':'scripts/task4_v205_source_diagnostics.py','results':'results/task4_v205_source_diagnostics','verification':'results/task4_v205_source_diagnostics/verification.json','verification_sha256':sha(R/'results/task4_v205_source_diagnostics/verification.json'),'changes_primary_bounds':False}
 d['point_withdrawal_addendum'].update(script='scripts/task4_v205_operational_rebase.py',results='results/task4_v205_operational_rebase/point_withdrawal',verification='results/task4_v205_operational_rebase/verification.json',verification_sha256=sha(R/'results/task4_v205_operational_rebase/verification.json'))
 d['Prague_V205_scientific_staging']['current_registry_note']='Frozen pre-activation record; current science and locally reviewed manuscript nowV205.'
 d['historical_ai_paper_verification_context']='PriorV204AI-only update proof remains frozen; currentV205source/science verification is bound by current paper integration. AIselectioncutoffs unchanged and laterwork notcovered.'
 write(path,d)
 path=R/'design/task4_user_current_acquisition.json';d=read(path);d.update(primary_model='V205',active_primary_model='V205',role='V205 current acquisition/point-review calculations; historical followups remain frozen at generation scopes',results='results/task4_v205_operational_rebase/acquisition',script='scripts/task4_v205_operational_rebase.py',audit='results/task4_v205_operational_rebase/verification.json',source_followup_verification='results/task4_v205_commute_scope/verification.json',primary_admissions=1,actual_score_width_reduction={'fixed':0.14615082605197038,'equal':0.2872118754673494},science_and_paper_unchanged=False)
 d['current_operational_rebase']={'results':'results/task4_v205_operational_rebase','verification':'results/task4_v205_operational_rebase/verification.json','verification_sha256':sha(R/'results/task4_v205_operational_rebase/verification.json'),'point_withdrawal':'results/task4_v205_operational_rebase/point_withdrawal','point_source_ledger':'results/task4_v205_operational_rebase/point_source_ledger','scope':'CurrentV205risks/priorities; 112sourceclassifications/evidencefields fromcurrentZurichoverlay retained, including6reviewed-unresolved.'}
 ledger=R/'results/task4_v205_operational_rebase/point_source_ledger';d['current_point_source_ledger'].update(results=str(ledger.relative_to(R)),ledger=str((ledger/'ledger.csv').relative_to(R)),review_priority=str((ledger/'review_priority.csv').relative_to(R)),verification='results/task4_v205_operational_rebase/verification.json',verification_sha256=sha(R/'results/task4_v205_operational_rebase/verification.json'),primary_model='V205',scope='112currentV205riskrows with currentoverlayclassifications and allsource/evidencefieldsunchanged; scientific numerical assumptions notsourcecertification.')
 d['Prague_V205_scientific_staging']['current_registry_note']='Frozen pre-activation record; V205nowactive. Observedoperation/universalaccess/physicalcensus notcertified.'
 d['historical_registry_note']='NestedpreV205followups andsource_sha256 preservegeneration scope; currentcalculations usecurrent_operational_rebase andcurrent_point_source_ledger.'
 write(path,d)
 print('V205 active metadata and seven mirrored dependencies prepared; delivery/proof binding next')

def bind():
 independent=checked_review();old=read(O/'previous_v204_current_verification.json');pdf=G/'paper/current/main.pdf';assert sha(pdf)==sha(B/'main.pdf')
 names=list(old['current_files_sha256']);assert len(names)==7
 for n in names:assert sha(P/n)==sha(G/'paper/current'/n),n
 source=(P/'main.tex').read_text();aux=(B/'main.aux').read_text();pages=base.text_pages(pdf);assert len(pages)==27 and len(re.findall(r'\\bibitem\{',source))==63 and len(re.findall(r'\\bibcite\{',aux))==63
 label=lambda n:int(re.search(r'\\newlabel\{'+n+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1]);assert label('main-end')==25 and label('LastPage')==27
 log=(B/'main.log').read_text();assert all(s not in log for s in ['Overfull','undefined','LaTeX Warning']);assert log.count('Underfull')==3
 layout=base.layout(pdf,O,pages)
 snapshot=read(R/'design/task4_user_v205_snapshot.json');science={**snapshot['upstream_source_sha256'],**snapshot['source_sha256']};assert len(science)==773
 for n,h in science.items():assert sha(R/n)==h,n
 science_bundle=dict(science)
 for n in ['design/task4_user_v205_snapshot.json','design/task4_user_v205_admissions.json']:science_bundle[n]=sha(R/n)
 sensitivity={}
 for name in ['commute_scope','point_error','source_diagnostics']:
  for p in (R/'results'/('task4_v205_'+name)).rglob('*'):
   if p.is_file():sensitivity[str(p.relative_to(R))]=sha(p)
  for prefix in ['task4_v205_','audit_task4_v205_']:
   p=R/'scripts'/(prefix+name+'.py');sensitivity[str(p.relative_to(R))]=sha(p)
 inputs={}
 for folder in ['task4_v205_paper_assets','task4_v205_operational_rebase']:
  for p in (R/'results'/folder).rglob('*'):
   if p.is_file():inputs[str(p.relative_to(R))]=sha(p)
 for p in [Path(__file__),independent,R/'scripts/task4_v205_paper_assets.py',R/'scripts/task4_apply_v205_current_paper.py',R/'scripts/task4_v205_reproduce.py',R/'scripts/task4_v205_delivery.py']:inputs[str(p.relative_to(R))]=sha(p)
 inputs.update(sensitivity)
 verification=dict(status='pass',primary_model='V205',source_sha256=inputs,pdf_sha256=sha(pdf),main_sha256=sha(P/'main.tex'),total_pages=27,main_and_references_pages=25,reference_keys=63,preserved_shared_class_refbib_and_auxiliary_figures=True,approved_definition_preserved=True,minimum_new_figure_font_pt=10,visual_review='independent_review.json',**layout,scope='Source binding and locally reviewed layout. Full31case/223settingMCsource science review is frozen separately; clean-HEAD source/scalar/all-page reproduction follows separately. Noonlinecompile/wholeteamacceptance/submissionclaim.')
 write(O/'verification.json',verification)
 delivery=read(C/'delivery_verification.json');assert delivery['primary_model']=='V205' and delivery['pdf_sha256']==sha(pdf)
 proof=dict(old);proof.update(primary_model='V205',pdf_sha256=sha(pdf),main_source_sha256=sha(P/'main.tex'),total_pages=27,main_and_references_pages=25,underfull_counts=[3,3],current_files_sha256={n:sha(P/n) for n in names},independent_audit_sha256=sha(independent),delivery_audit_sha256=sha(C/'delivery_verification.json'),visual_review_sha256=sha(independent),science_bindings_verified=773,v205_science_sha256=science_bundle,v205_sensitivity_sha256=sensitivity,scope='V205Prague942source-definedscheduledbusnodeswithpublicdriver-requestcondition;27pages63references,sharedclass/refbib/auxfigs/definition preserved. Inheritedadditional77mapsremainhistorical; newcurrentV205sensitivity bundleexplicit. FullcleanHEADreproduction and remoteGitreceiptsseparate.',prague_942_scheduled_node_lower_admitted=True,v205_integration_verification='results/task4_v205_paper_integration/verification.json',v205_integration_verification_sha256=sha(O/'verification.json'),historical_ai_paper_verification_context='Frozen priorAI-onlyV204paper proof; currentselectioncutoffsunchanged, laterworkoutsidecapture. CurrentV205science/figure/sourcechangesverifiedbythisintegration.')
 write(C/'current_verification.json',proof)
 path=R/'design/task4_user_current_review.json';d=read(path);d.update(primary_model='V205',pdf_sha256=sha(pdf),scope='SingleV205main;27pages63references,fixedOslo/equalZurich16possible0necessary.',revision='OwnedV205data/numbers/twofigures/sourceconditions updated; templatesharedfiles,historicalcases,approveddefinitionandunrelatedteammatecontentpreserved.',target_primary_model='V205',target_science_snapshot='research/2026-a/design/task4_user_v205_snapshot.json',target_paper_assets='research/2026-a/results/task4_v205_paper_assets',target_reproduction_script='research/2026-a/scripts/task4_v205_reproduce.py',target_status='V205 localreview/sourcebound; cleanHEADreproductionandremoteGitreceiptsseparate.',v205_integration_verification='research/2026-a/results/task4_v205_paper_integration/verification.json',v205_integration_verification_sha256=sha(O/'verification.json'),current_independent_review='research/2026-a/results/task4_v205_paper_integration/independent_review.json',current_independent_review_sha256=sha(independent))
 write(path,d)
 activation=read(O/'previous_v204_activation.json');activation.update(primary='V205',core_bindings=773,primary_admissions=1,newly_filled_cells=0,refined_existing_partial_cells=1,actual_active_width_reduction=0.14615082605197038,equal_weight_width_reduction=0.2872118754673494,pdf_sha256=sha(pdf),source_sha256=sha(P/'main.tex'),change='Prague57metro lowerreplacedby942source-definedscheduledbusnodes;50ordinary+892driver-request. Other159lower/all160upper unchangedfromV204; countsnotadded.',request_withholding_lower_count=57,possible_champions=16,necessary_champions=0,clean_head_reproduction='pending separate receipt',remote_synchronization='pending separate receipt',latest_manuscript_change='V205 ownednumerical/source/figure migration; AIcapturewindowsunchanged')
 for k in ['clean_head_reproduction_sha256','paper_commit']:activation.pop(k,None)
 write(C/'activation.json',activation)
 path=R/'design/task4_user_current_delivery.json';d=read(path);d.update(primary_model='V205',pdf_sha256=sha(pdf),revision='V205source/figures/threecurrent-sensitivityproofs bound;48requirements/12pending preserved.',delivery_script='research/2026-a/scripts/task4_v205_delivery.py');write(path,d)
 path=R/'design/task4_user_current_extensions.json';d=read(path);d['current_paper_integration']={'verification':'results/task4_v205_paper_integration/verification.json','verification_sha256':sha(O/'verification.json'),'peer_review':'results/task4_v205_paper_integration/independent_review.json','peer_review_sha256':sha(independent),'delivery_verification':'results/current_paper_review/delivery_verification.json','delivery_verification_sha256':sha(C/'delivery_verification.json'),'scope':'CurrentV205localpaper; frozenpriorV204/AIonlyproofs remainhistorical.'};write(path,d)
 print(json.dumps({'status':'pass','primary':'V205','pages':27,'main_pages':25,'science_bindings':773,'pending':delivery['pending_count']}))

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--prepare',action='store_true');a=p.parse_args();prepare() if a.prepare else bind()
