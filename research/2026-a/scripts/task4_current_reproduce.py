"""Reproduce active user16 V203 / the current manuscript from clean paper Git HEAD.

Uses local scientific packages, Poppler and the existing Tectonic cache. Builds
the sole current main.tex from an isolated exact Git snapshot. Does not contact Overleaf or claim final submission readiness.
"""
from pathlib import Path
import argparse, hashlib, importlib.metadata, json, math, shutil, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor
import task4_v198_reproduce as base
sys.dont_write_bytecode=True
sha,read,require,command,git=base.sha,base.read,base.require,base.command,base.git

from task4_v201_reproduce import science_check as prior_science_check

def v202_science_check(analysis,model):
 import numpy as np
 import pandas as pd
 require(model['version']=='V202' and model['module']=='task4_user_v202_revision' and model['factory']=='revised_bounds','Expected explicit user16 V202')
 require(model['results']=='results/task4_user_v202_revision' and model['snapshot']=='design/task4_user_v202_snapshot.json','Unexpected V202 paths')
 inherited=prior_science_check(analysis,dict(model,version='V200',module='task4_user_v200_revision',results='results/task4_user_v200_revision',snapshot='design/task4_user_v200_snapshot.json'))
 from task4_user_v200_revision import revised_bounds as previous
 from task4_user_v202_revision import revised_bounds
 from task4_v5_model import NAMES,weights,SPEC
 frame,lo,hi=revised_bounds();old,oldlo,oldhi=previous()
 require(frame.equals(old),'User frame changed')
 i=frame.city.tolist().index('Singapore');k=NAMES.index('public_pool_density')
 require(set(map(tuple,np.argwhere(lo!=oldlo)))=={(i,k)},'Expected only Singapore pool lower refinement')
 np.testing.assert_array_equal(hi,oldhi)
 admissions=read(analysis/'design/task4_user_v202_admissions.json');row=admissions['observations'][0]
 require(len(admissions['observations'])==1 and row['raw_count_before']==25 and row['raw_count']==26 and row['notice_withholding_count']==22,'Unexpected inventory refinements')
 require(row['population']==frame.iloc[i].population==6036900 and row['population_year']==frame.iloc[i].population_year==2024,'Retained population changed')
 require(row['inventory_reference_date'] is None and row['lower_bound_only'],'Inventory date/access scope changed')
 require(len(set(row['venues']))==26 and len(set(row['old_notice_venues']))==3,'Inventory identity count differs')
 require(admissions['unique_supplemented_city_indicator_keys']==25 and admissions['newly_filled_cells']==0,'New keys/cells unexpectedly introduced')
 def utility(count):
  density=count*100000/6036900
  return density/(SPEC[k][2]+density)
 np.testing.assert_allclose(lo[i,k],utility(26),rtol=0,atol=1e-16)
 _,a,b=revised_bounds(False);np.testing.assert_array_equal(a,oldlo);np.testing.assert_array_equal(b,oldhi)
 _,a,b=revised_bounds(withhold_notice_venues=True)
 expected=lo.copy();expected[i,k]=utility(22)
 np.testing.assert_array_equal(a,expected);np.testing.assert_array_equal(b,hi)
 for kwargs,count in [({'withhold_existing_notice_venues':True},23),({'include_sg_pool':False},8),({'include_sportshub':False,'include_sg_pool':False},7)]:
  _,a,b=revised_bounds(**kwargs);expected=lo.copy();expected[i,k]=utility(count);np.testing.assert_array_equal(a,expected);np.testing.assert_array_equal(b,hi)
 frozen=pd.read_csv(analysis/model['results']/'utility_bounds.csv');frozen=frozen[frozen.scenario=='after_conditional']
 require(len(frozen)==160 and not frozen.duplicated(['city','indicator']).any(),'Expected160unique frozen cells')
 for j,city in enumerate(frame.city):
  for t,indicator in enumerate(NAMES):
   r=frozen[(frozen.city==city)&(frozen.indicator==indicator)].iloc[0]
   np.testing.assert_allclose([lo[j,t],hi[j,t]],[r.lower,r.upper],atol=2e-15,rtol=0)
 ranks=pd.read_csv(analysis/model['results']/'current_ranks.csv');require(len(ranks)==32,'Expected32frozen city-weight rows');cases=[]
 for reference,w in [('fixed',weights(.1)),('equal',np.full(10,.1))]:
  def score(matrix):
   values=[]
   for v in matrix:
    positive=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,v)))
    negative=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,v)))
    values.append(100*positive/(positive+negative))
   return np.array(values)
  lower,upper=score(lo),score(hi);regret=[];possible=[];necessary=[]
  for j in range(16):
   others=[h for h in range(16) if h!=j]
   regret.append(max(0,float(upper[others].max()-lower[j])))
   possible.append(bool(upper[j]>=lower[others].max()-1e-12));necessary.append(bool(lower[j]>=upper[others].max()-1e-12))
  regret=np.array(regret);rank=1+(regret[None,:]<regret[:,None]-1e-12).sum(axis=1)
  saved=ranks[ranks.weight_reference==reference].set_index('city').loc[frame.city]
  for name,value in [('score_lower',lower),('score_upper',upper),('max_regret',regret),('decision_rank',rank)]:np.testing.assert_allclose(value,saved[name].to_numpy(),atol=3e-13,rtol=0)
  require(possible==saved.possible_champion.tolist() and necessary==saved.necessary_champion.tolist(),'Champion flags differ')
  cases.append(dict(reference=reference,recommendation=frame.loc[rank==1,'city'].tolist(),possible=sum(possible),necessary=sum(necessary),mean_width=float((upper-lower).mean())))
 return dict(inherited_V200_checks=inherited,utility_cells=160,scalar_city_weight_cases=32,other159_lower_and_all_uppers_exact=True,inventory_formula_and_23_22_sensitivities_checked=True,withdrawal_restores_V200=True,comparisons=cases,MC_replayed=False,source_semantics_reaudited=False)

def science_check(analysis,model):
 import numpy as np
 import pandas as pd
 require(model['version']=='V203' and model['module']=='task4_user_v203_revision' and model['factory']=='revised_bounds','Expected explicit user16 V203')
 require(model['results']=='results/task4_user_v203_revision' and model['snapshot']=='design/task4_user_v203_snapshot.json','Unexpected V203 paths')
 inherited=v202_science_check(analysis,dict(model,version='V202',module='task4_user_v202_revision',results='results/task4_user_v202_revision',snapshot='design/task4_user_v202_snapshot.json'))
 from task4_user_v202_revision import revised_bounds as previous
 from task4_user_v203_revision import revised_bounds
 from task4_v5_model import NAMES,weights,SPEC
 frame,lo,hi=revised_bounds();old,oldlo,oldhi=previous();require(frame.equals(old),'Original user frame changed')
 i=frame.city.tolist().index('Oslo');k=NAMES.index('public_transport_density')
 require(set(map(tuple,np.argwhere(lo!=oldlo)))=={(i,k)},'Expected only Oslo transport lower refinement')
 np.testing.assert_array_equal(hi,oldhi)
 admission=read(analysis/'design/task4_user_v203_admissions.json');row=admission['observations'][0]
 require(len(admission['observations'])==1 and row['raw_count_before']==89 and row['raw_count']==len(set(row['native_root_ids']))==626,'Bus group count differs')
 require(row['population']==frame.iloc[i].population==727797 and row['population_year']==frame.iloc[i].population_year==2025,'Population changed')
 require(row['sourceyear']==2026 and row['lower_bound_only'],'Source-year/lower-bound scope changed')
 def utility(n):
  density=n*100000/727797;return density/(SPEC[k][2]+density)
 np.testing.assert_allclose(lo[i,k],utility(626),rtol=0,atol=1e-16)
 _,a,b=revised_bounds(False);np.testing.assert_array_equal(a,oldlo);np.testing.assert_array_equal(b,oldhi)
 for kwargs,count in [({'withhold_rail_replacement':True},624),({'withhold_no_calls_bus':True},625),({'withhold_rail_replacement':True,'withhold_no_calls_bus':True},623),({'include_questioned_stop':True},627)]:
  _,a,b=revised_bounds(**kwargs);expected=lo.copy();expected[i,k]=utility(count);np.testing.assert_array_equal(a,expected);np.testing.assert_array_equal(b,hi)
 frozen=pd.read_csv(analysis/model['results']/'utility_bounds.csv');frozen=frozen[frozen.scenario=='after_conditional'];require(len(frozen)==160 and not frozen.duplicated(['city','indicator']).any(),'Expected160frozen cells')
 for j,city in enumerate(frame.city):
  for t,indicator in enumerate(NAMES):
   r=frozen[(frozen.city==city)&(frozen.indicator==indicator)].iloc[0];np.testing.assert_allclose([lo[j,t],hi[j,t]],[r.lower,r.upper],atol=2e-15,rtol=0)
 ranks=pd.read_csv(analysis/model['results']/'current_ranks.csv');require(len(ranks)==32,'Expected32city-weight rows');cases=[]
 for reference,w,choice in [('fixed',weights(.1),'Oslo'),('equal',np.full(10,.1),'Zurich')]:
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
  require(possible==saved.possible_champion.tolist() and necessary==saved.necessary_champion.tolist(),'Champion flags differ');require(frame.loc[rank==1,'city'].tolist()==[choice],'Current recommendation differs')
  cases.append(dict(reference=reference,recommendation=[choice],possible=sum(possible),necessary=sum(necessary),mean_width=float((upper-lower).mean())))
 return dict(inherited_V202_checks=inherited,utility_cells=160,scalar_city_weight_cases=32,other159_lower_and_all_uppers_exact=True,source_defined_626_bus_group_formula_and_624_625_623_627_withholdings_checked=True,withdrawal_restores_V202=True,comparisons=cases,MC_replayed=False,source_semantics_reaudited=False)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True);parser.add_argument('--research-root',type=Path,default=Path(__file__).resolve().parents[3]);parser.add_argument('--paper-root',type=Path);args=parser.parse_args()
 research=args.research_root.resolve();paper=(args.paper_root or research.parent/'HiMCM-Overleaf').resolve();analysis=research/'research/2026-a';sys.path.insert(0,str(analysis/'scripts'))
 out=base.safe_output(args.output_dir,research,paper);start=time.time();report=dict(status='running',version='Single current main on V203',runner_sha256=sha(Path(__file__)))
 states={};protected={};science={};failure=None
 try:
  states={str(p):dict(head=git(p,'rev-parse','HEAD'),status=git(p,'status','--porcelain')) for p in [research,paper]}
  require(not states[str(paper)]['status'],'Paper tree must be clean for exact Git archival')
  paths=[analysis/f'design/task4_user_current_{x}.json' for x in ['model','extensions','review','delivery']]
  model,extensions,registry,delivery=[read(p) for p in paths]
  require(model['version']==extensions['extension_version']==extensions['primary_evidence_version']=='V203','Active science/extension versions differ')
  require(registry['version']==delivery['version']==delivery['review_version']=='current' and registry['primary_model']==delivery['primary_model']=='V203','Current owned review/delivery versions differ')
  require(registry['tex']==registry['root_entry']==registry['shared_main_entry']=='main.tex','Expected one current manuscript entry')
  require(registry['pdf_workspace']=='HiMCM' and registry['source_mirror']=='paper/current/main.tex','Expected GitHub-managed current source/PDF mirror')
  require(all(v['script']=='scripts/task4_v203_extensions.py '+k and v['results']=='results/task4_v203_'+k for k,v in extensions['modules'].items()) and set(extensions['modules'])=={'preferences','future','method','diagnostics'},'Extension paths differ')
  require(delivery['pdf']==registry['pdf'] and delivery['pdf_sha256']==registry['pdf_sha256'],'Delivery PDF differs')
  science=read(analysis/model['snapshot'])['source_sha256'];require(len(science)>476 and read(analysis/model['snapshot'])['bindings']==len(science) and read(analysis/model['snapshot'])['inherited_bindings']==476,'Expected explicit V203 bindings inheriting476');prior_bindings=read(analysis/'design/task4_user_v202_snapshot.json')['source_sha256'];require(all(science.get(n)==h for n,h in prior_bindings.items()),'Inherited476bindings differ')
  for path in paths:require(str(path.relative_to(analysis)) not in science,'Mutable registry in immutable science')
  for name,h in science.items():require(sha(analysis/name)==h,'Science hash differs: '+name)
  protected={str(p):sha(p) for p in paths}
  for n,h in base.tracked_hashes(paper).items():protected[str(paper/n)]=h
  proof_path=research/registry['research_verification'];delivery_path=research/delivery['research_verification']
  expected=read(proof_path);d=read(delivery_path)
  for bundle in ['additional_source_scope_sha256','additional_figure_inputs_sha256','additional_student_inputs_sha256','additional_ai_inputs_sha256']:
   for n,h in expected.get(bundle,{}).items():
    require(sha(analysis/n)==h,'Additional reviewed input differs: '+n);protected[str(analysis/n)]=h
  require(expected['status']==d['status']=='pass' and expected['pdf_sha256']==d['pdf_sha256']==registry['pdf_sha256'],'Current paper/delivery checks not bound')
  expected=dict(expected,news_pages=d['news_pages'],compiled_references=d['compiled_references'])
  for n,h in expected['current_files_sha256'].items():
   require(sha(paper/n)==sha(research/'paper/current'/n)==h,'Current paper mirror differs: '+n)
   protected[str(research/'paper/current'/n)]=h
  canonical=research/registry['pdf'];base.check_pdf_identity(canonical,registry['pdf_sha256']);protected[str(canonical)]=sha(canonical)
  for p in [proof_path,delivery_path]:protected[str(p)]=sha(p)
  require([str(p.relative_to(paper)) for p in paper.rglob('*.tex') if '.git' not in p.parts]==['main.tex'],'Expected only one .tex in Overleaf')
  require(not (paper/'drafts').exists(),'Historical drafts remain in current paper tree')
  original=research/registry['teammate_original_archive'];require(sha(original)=='40a63df3cb2b0e2524fbbe4f7fd19d904851bc4e2e3b7b99d50d477a4da7f0c1','Original teammate archive changed')
  report.update(primary='V203',canonical_pdf_sha256=registry['pdf_sha256'],paper_head=states[str(paper)]['head'],research_head=states[str(research)]['head'],environment=dict(python=sys.version.split()[0],executable=sys.executable,tools={n:command([n,'--version'] if n=='tectonic' else [n,'-v']).splitlines()[0] for n in ['tectonic','pdftotext','pdftoppm']},packages={n:importlib.metadata.version(n) for n in ['numpy','pandas','scipy','matplotlib']},TeX='Existing local cache only'))
  print('Current V203 science and single manuscript bound; isolating paper Git HEAD',flush=True)
  with tempfile.TemporaryDirectory(prefix='work-',dir=out) as temp:
   work=Path(temp);snapshot=work/'snapshot';report['archive']=base.archive_snapshot(paper,snapshot,work)
   pages=base.text_pages(canonical);base.layout(canonical,out,pages);pixels=base.pixels(canonical,work/'canonical-render')
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
  report.update(elapsed_seconds=round(time.time()-start,3),submission_ready=False,server_compile_verified=False,scope='Single current main from exact tracked paper HEAD, local cached-TeX build, all-page text/render equality and160cells/32scalarcases plus inherited controls; no fresh-machine,MC/source revalidation or online compile claim.')
  (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(status=report['status'],report=str(out/'report.json'),error=report.get('error'))),flush=True)
 return int(failure is not None)
if __name__=='__main__':raise SystemExit(main())
