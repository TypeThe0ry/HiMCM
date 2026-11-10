"""Reproduce active V205 and the single current paper from clean paper Git HEAD.

Local cached TeX, source-bound numerical checks and per-page comparisons only;
no network, online Overleaf compilation, or submission-readiness claim.
"""
from pathlib import Path
import argparse, importlib.metadata, json, math, sys, tempfile, time
sys.dont_write_bytecode = True
import task4_v198_reproduce as base
sha, read, require, command, git = base.sha, base.read, base.require, base.command, base.git

def science_check(analysis, model):
 import numpy as np
 import pandas as pd
 from task4_user_v204_revision import revised_bounds as previous
 from task4_user_v205_revision import revised_bounds
 from task4_v5_model import NAMES, SPEC, weights
 require(model['version']=='V205' and model['module']=='task4_user_v205_revision' and model['factory']=='revised_bounds', 'Expected explicit V205 factory')
 require(model['results']=='results/task4_user_v205_revision' and model['snapshot']=='design/task4_user_v205_snapshot.json' and model['admissions']=='design/task4_user_v205_admissions.json', 'V205 paths differ')
 original='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 require(sha(analysis/model['source_csv'])==original, 'Original CSV differs')
 admissions=read(analysis/model['admissions']);require(admissions['input_sha256']==original and len(admissions['source_hashes'])==29, 'Admissions source binding differs')
 for name,h in admissions['source_hashes'].items():require(sha(analysis/name)==h, 'Admissions hash differs: '+name)
 require(len(admissions['observations'])==1, 'Expected one observation')
 row=admissions['observations'][0]
 for key,value in dict(city='Prague', indicator='public_transport_density',raw_count_before=57,raw_count=942,population=1407084,population_year=2025,anchor=50,service_day='20261110',counts_not_added=True,public_request_stop_condition_retained=True,source_defined_scheduled_supply_supported=True,actual_operation_verified=False).items():
  require(row[key]==value,'Admission differs: '+key)
 ids=set(row['native_node_ids']); request=set(admissions['request_only_node_ids'])
 require(len(ids)==942 and len(request)==892 and request <= ids and len(ids-request)==50, 'Node witness counts differ')
 require(admissions['request_withhold_count_before_retained_floor']==50 and admissions['request_withhold_retained_metro_floor']==57, 'Withdrawal floor differs')
 peer=analysis/admissions['source_peer_review'];require(sha(peer)==admissions['source_peer_review_sha256'], 'Peer review hash differs')
 frame,lo,hi=revised_bounds(); old,oldlo,oldhi=previous();require(frame.equals(old),'User frame changed')
 i=frame.city.tolist().index('Prague');k=NAMES.index('public_transport_density')
 require(frame.iloc[i].population==1407084 and frame.iloc[i].population_year==2025 and SPEC[k][2]==50,'Population or anchor differs')
 require(set(map(tuple,np.argwhere(lo!=oldlo)))=={(i,k)}, 'Expected only Prague lower refinement')
 np.testing.assert_array_equal(hi,oldhi)
 def utility(n):
  density=n*100000/1407084
  return density/(50+density)
 np.testing.assert_allclose([oldlo[i,k],lo[i,k]],[utility(57),utility(942)],rtol=0,atol=1e-16)
 _,a,b=revised_bounds(include_prague_bus=False);np.testing.assert_array_equal(a,oldlo);np.testing.assert_array_equal(b,oldhi)
 _,a,b=revised_bounds(withhold_prague_request_stops=True);np.testing.assert_array_equal(a,oldlo);np.testing.assert_array_equal(b,oldhi)
 summary=read(analysis/model['results']/'summary.json');prior=read(analysis/'results/task4_user_v203_revision/summary.json')
 require([summary[x] for x in ['point_cells','partial_cells','fully_missing_cells']]==[112,37,11] and prior['cumulative_supplements']==25, 'Cell metadata differs')
 frozen=pd.read_csv(analysis/model['results']/'utility_bounds.csv');frozen=frozen[frozen.scenario=='after_conditional'];require(len(frozen)==160 and not frozen.duplicated(['city','indicator']).any(),'Expected 160 unique bounds')
 for j,city in enumerate(frame.city):
  for t,indicator in enumerate(NAMES):
   r=frozen[(frozen.city==city)&(frozen.indicator==indicator)].iloc[0];np.testing.assert_allclose([lo[j,t],hi[j,t]],[r.lower,r.upper],atol=2e-15,rtol=0)
 ranks=pd.read_csv(analysis/model['results']/'current_ranks.csv');require(len(ranks)==32 and not ranks.duplicated(['weight_reference','city']).any(), 'Expected 32 unique scalar cases')
 comparisons=[]
 for reference,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  def score(matrix):
   out=[]
   for v in matrix:
    positive=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,v)));negative=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,v)));out.append(100*positive/(positive+negative))
   return np.array(out)
  lower,upper=score(lo),score(hi);regret=[];possible=[];necessary=[]
  for j in range(16):
   others=[h for h in range(16) if h!=j];regret.append(max(0,float(upper[others].max()-lower[j])));possible.append(bool(upper[j]>=lower[others].max()-1e-12));necessary.append(bool(lower[j]>=upper[others].max()-1e-12))
  regret=np.array(regret);rank=1+(regret[None,:]<regret[:,None]-1e-12).sum(axis=1);saved=ranks[ranks.weight_reference==reference].set_index('city').loc[frame.city]
  for name,value in [('score_lower',lower),('score_upper',upper),('max_regret',regret),('decision_rank',rank)]:np.testing.assert_allclose(value,saved[name].to_numpy(),atol=3e-13,rtol=0)
  require(possible==saved.possible_champion.tolist() and necessary==saved.necessary_champion.tolist(),'Champion flags differ')
  comparisons.append(dict(reference=reference,recommendation=frame.loc[rank==1,'city'].tolist(),possible=sum(possible),necessary=sum(necessary)))
 return dict(utility_cells=160,scalar_city_weight_cases=32,other159_lower_and_all_uppers_exact=True,off_restores_V204=True,request_withholding=57,source_hashes=29,comparisons=comparisons,source_defined_scheduled_supply_supported=True,actual_operation_verified=False,MC_replayed=False,source_semantics_reaudited=False)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--research-root',type=Path,default=Path(__file__).resolve().parents[3]);parser.add_argument('--paper-root',type=Path);args=parser.parse_args()
 research=args.research_root.resolve();paper=(args.paper_root or research.parent/'HiMCM-Overleaf').resolve();analysis=research/'research/2026-a';sys.path.insert(0,str(analysis/'scripts'))
 out=base.safe_output(args.output_dir,research,paper);start=time.time();report=dict(status='running',version='Single current main on V205',runner_sha256=sha(Path(__file__)))
 states={};protected={};science={};failure=None
 try:
  states={str(p):dict(head=git(p,'rev-parse','HEAD'),status=git(p,'status','--porcelain')) for p in [research,paper]}
  require(not states[str(paper)]['status'],'Paper tree must be clean for exact Git archival')
  paths=[analysis/f'design/task4_user_current_{x}.json' for x in ['model','extensions','review','delivery','acquisition']]
  model,extensions,registry,delivery,acquisition=[read(p) for p in paths]
  require(model['version']==extensions['extension_version']==extensions['primary_evidence_version']=='V205','Active science/extension versions differ')
  require(acquisition['primary_model']==acquisition['active_primary_model']==model['version'],'Acquisition primary version differs')
  require(registry['version']==delivery['version']==delivery['review_version']=='current' and registry['primary_model']==delivery['primary_model']=='V205','Current owned review/delivery versions differ')
  require(registry['tex']==registry['root_entry']==registry['shared_main_entry']=='main.tex','Expected one current manuscript entry')
  require(registry['pdf']=='paper/current/main.pdf', 'Canonical PDF path differs')
  require(registry['pdf_workspace']=='HiMCM' and registry['source_mirror']=='paper/current/main.tex','Expected GitHub-managed current source/PDF mirror')
  require(all(v['script']=='scripts/task4_v205_extensions.py' and v['results']=='results/task4_user_v205_extensions/'+k for k,v in extensions['modules'].items()) and set(extensions['modules'])=={'preferences','future','method','diagnostics'},'Extension paths differ')
  require(delivery['pdf']==registry['pdf'] and delivery['pdf_sha256']==registry['pdf_sha256'],'Delivery PDF differs')
  snapshot=read(analysis/model['snapshot'])
  new=snapshot['source_sha256']; upstream=snapshot['upstream_source_sha256']
  require(len(new)==115 and len(upstream)==658 and not (set(new)&set(upstream)), 'V205 snapshot binding counts differ')
  prior=analysis/'design/task4_user_v204_snapshot.json'
  require(sha(prior)==snapshot['upstream_snapshot_digest'] and {**read(prior)['upstream_source_sha256'],**read(prior)['source_sha256']}==upstream, 'Upstream snapshot differs')
  science={**upstream,**new}
  for path in paths:require(str(path.relative_to(analysis)) not in science,'Mutable registry in immutable science')
  for name,h in science.items():require(sha(analysis/name)==h,'Science hash differs: '+name)
  audit=read(analysis/'results/task4_v205_transition/verification.json')
  require(audit['status']=='pass' and audit['primary_bound_cases']==31 and audit['primary_MC_settings_replayed']==186 and audit['draws_per_setting']==10000, 'Frozen scientific audit scope differs')
  protected={str(p):sha(p) for p in paths}
  protected[str(Path(__file__).resolve())]=report['runner_sha256']
  from task4_current_research_bindings import verify_current_research
  research_integrity,research_protected=verify_current_research(analysis)
  for name,h in research_protected.items():
   require(name not in protected or protected[name]==h,'Research binding changed during capture: '+name)
   protected[name]=h
  report['registered_research_integrity']=research_integrity
  for n,h in base.tracked_hashes(paper).items():protected[str(paper/n)]=h
  proof_path=research/registry['research_verification'];delivery_path=research/delivery['research_verification']
  expected=read(proof_path);d=read(delivery_path)
  require(expected['primary_model']=='V205' and expected['main_entry']=='main.tex' and expected['single_current_tex_entry'] is True, 'Paper proof is not V205 single main')
  require(len(expected['current_files_sha256'])==7, 'Expected seven source dependencies')
  require(sum(len(expected[k]) for k in ['additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256','additional_point_error_inputs_sha256'])==77 and len(expected['withdrawal_source_sha256'])==10 and len(expected['edition_source_sha256'])==24, 'Paper proof input inventory differs')
  require({'design/task4_user_v205_snapshot.json','design/task4_user_v205_admissions.json'} <= set(expected['v205_science_sha256']), 'V205 proof provenance incomplete')
  sensitivity=expected['v205_sensitivity_sha256']
  required={f'scripts/{name}.py' for name in ['task4_v205_commute_scope','audit_task4_v205_commute_scope','task4_v205_point_error','audit_task4_v205_point_error','task4_v205_source_diagnostics','audit_task4_v205_source_diagnostics']}
  for folder in ['task4_v205_commute_scope','task4_v205_point_error','task4_v205_source_diagnostics']:
   required.update(str(p.relative_to(analysis)) for p in (analysis/'results'/folder).iterdir() if p.is_file())
   audit=read(analysis/'results'/folder/'verification.json');require(audit['status'].lower().startswith('pass'), 'V205 sensitivity audit failed: '+folder)
  require(required <= set(sensitivity), 'V205 sensitivity bundle incomplete')
  for bundle in ['v205_science_sha256','v205_sensitivity_sha256','additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256','additional_point_error_inputs_sha256','withdrawal_source_sha256','edition_source_sha256']:
   for n,h in expected.get(bundle,{}).items():
    require(sha(analysis/n)==h,'Additional reviewed input differs: '+n);protected[str(analysis/n)]=h
  require(expected['status']==d['status']=='pass' and expected['pdf_sha256']==d['pdf_sha256']==registry['pdf_sha256'],'Current paper/delivery checks not bound')
  require(expected['reference_keys']==d['compiled_references'], 'Reference count differs between proofs')
  require(expected['main_source_sha256']==expected['current_files_sha256']['main.tex'], 'Main source proof differs')
  expected=dict(expected,news_pages=d['news_pages'],compiled_references=d['compiled_references'])
  for n,h in expected['current_files_sha256'].items():
   require(sha(paper/n)==sha(research/'paper/current'/n)==h,'Current paper mirror differs: '+n)
   protected[str(research/'paper/current'/n)]=h
  canonical=research/registry['pdf'];base.check_pdf_identity(canonical,registry['pdf_sha256']);protected[str(canonical)]=sha(canonical)
  for p in [proof_path,delivery_path,analysis/model['snapshot'],prior]:protected[str(p)]=sha(p)
  require([str(p.relative_to(paper)) for p in paper.rglob('*.tex') if '.git' not in p.parts]==['main.tex'],'Expected only one .tex in Overleaf')
  require(not (paper/'drafts').exists(),'Historical drafts remain in current paper tree')
  original=research/registry['teammate_original_archive'];require(sha(original)=='40a63df3cb2b0e2524fbbe4f7fd19d904851bc4e2e3b7b99d50d477a4da7f0c1','Original teammate archive changed')
  protected[str(original)]=sha(original)
  report.update(primary='V205',canonical_pdf_sha256=registry['pdf_sha256'],paper_head=states[str(paper)]['head'],research_head=states[str(research)]['head'],environment=dict(python=sys.version.split()[0],executable=sys.executable,tools={n:command([n,'--version'] if n=='tectonic' else [n,'-v']).splitlines()[0] for n in ['tectonic','pdftotext','pdftoppm']},packages={n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','matplotlib']},TeX='Existing local cache only'))
  print('Current V205 science and single manuscript bound; isolating paper Git HEAD',flush=True)
  with tempfile.TemporaryDirectory(prefix='work-',dir=out) as temp:
   work=Path(temp);snapshot=work/'snapshot';report['archive']=base.archive_snapshot(paper,snapshot,work)
   pages=base.text_pages(canonical);require(len(pages)==expected['total_pages'], 'Canonical physical page count differs');base.layout(canonical,out,pages);pixels=base.pixels(canonical,work/'canonical-render')
   report['science']=science_check(analysis,model)
   report['builds']=[base.build_one('root',snapshot,work,out,registry,expected,pages,pixels)]
   report['status']='pass'
 except Exception as e:failure=e;report.update(status='fail',error=f'{type(e).__name__}: {e}')
 finally:
  changed=[]
  for n,h in science.items():
   if not (analysis/n).is_file() or sha(analysis/n)!=h:changed.append('science:'+n)
  for n,h in protected.items():
   if not Path(n).is_file() or sha(n)!=h:changed.append(n)
  for n,state in states.items():
   if git(n,'rev-parse','HEAD')!=state['head'] or git(n,'status','--porcelain')!=state['status']:changed.append('git:'+n)
  report['input_protection']=dict(science_files=len(science),paper_and_navigation_files=len(protected),changed=changed)
  if changed:failure=RuntimeError('Protected inputs changed');report.update(status='fail',error=str(failure))
  report.update(elapsed_seconds=round(time.time()-start,3),submission_ready=False,server_compile_verified=False,scope='Single current main from exact tracked paper HEAD, local cached-TeX build, all-page text/render equality and 160 cells/32 scalar cases with V204 withdrawal control; registered research file-integrity/one-hop report bindings checked separately, including an explicit historical Git version. No fresh-machine,MC/source semantic revalidation or online compile claim.')
  (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(status=report['status'],report=str(out/'report.json'),error=report.get('error'))),flush=True)
 return int(failure is not None)
if __name__=='__main__':raise SystemExit(main())
