"""Rebuild the registered owned paper from isolated Git snapshots and check user16.

Run with the research environment Python and an empty output directory outside both
repositories. Requires installed scientific packages, Poppler, and cached TeX resources.
No model/paper inputs are written; no Monte Carlo simulations or server calls run.
"""
from pathlib import Path,PurePosixPath
from concurrent.futures import ThreadPoolExecutor
import argparse,csv,hashlib,importlib,importlib.metadata,json,math,os,re,shutil,subprocess,sys,tarfile,tempfile,time,unicodedata,xml.etree.ElementTree as E
sys.dont_write_bytecode=True

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def require(test,message):
 if not test:raise ValueError(message)
def command(args,cwd=None,timeout=120):
 p=subprocess.run([str(x) for x in args],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
 if p.returncode:raise RuntimeError(f'Command failed ({p.returncode}): {args}\n'+p.stdout.decode(errors='replace')[-1800:])
 return p.stdout.decode()
def git(repo,*args):return command(['git','-C',repo,*args]).strip()
def tracked_hashes(repo):
 names=command(['git','-C',repo,'ls-files','-z']).split('\0')[:-1]
 for name in names:require((repo/name).is_file() and not (repo/name).is_symlink(),f'Unsupported tracked input type: {name}')
 return {n:sha(repo/n) for n in names}
def norm(x):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',x)).split())
def text_pages(pdf):return [norm(x) for x in command(['pdftotext','-layout',pdf,'-']).split('\f') if x.strip()]
def check_pdf_identity(pdf,expected):require(sha(pdf)==expected,'Registered canonical PDF SHA256 mismatch; no build attempted')
def safe_output(value,research,paper):
 raw=Path(value).expanduser();require(not raw.is_symlink(),'Output directory itself cannot be a symlink')
 out=raw.resolve()
 for repo in [research,paper]:
  require(not out.is_relative_to(repo) and not repo.is_relative_to(out),'Output must be outside both repositories and cannot be their ancestor')
 require(not out.exists() or (out.is_dir() and not any(out.iterdir())),'Output directory must be new or empty')
 out.mkdir(parents=True,exist_ok=True);return out

def archive_snapshot(paper,destination,work):
 """Reject archives that differ from the exact tracked Git tree."""
 tree={}
 for item in command(['git','-C',paper,'ls-tree','-rz','--full-tree','HEAD']).split('\0'):
  if not item:continue
  meta,name=item.split('\t',1);mode,kind,oid=meta.split()
  require(kind=='blob' and mode in {'100644','100755'},f'Unsupported Git tree mode (symlink/gitlink): {name}')
  tree[name]=oid
 archive=work/'paper.tar';command(['git','-C',paper,'archive','--format=tar','--output',archive,'HEAD'])
 algo=git(paper,'rev-parse','--show-object-format');seen=set()
 with tarfile.open(archive) as tf:
  members=tf.getmembers()
  for member in members:
   path=PurePosixPath(member.name)
   require(not path.is_absolute() and '..' not in path.parts,'Unsafe archive path')
   require(member.isdir() or member.isfile(),'Archive links/devices are not accepted')
   if member.isdir():continue
   name=path.as_posix();require(name in tree,f'Unexpected archive file: {name}')
   raw=tf.extractfile(member).read()
   require(not raw.startswith(b'version https://git-lfs.github.com/spec/v1'),f'Unresolved Git LFS pointer: {name}')
   blob=hashlib.new(algo,b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
   require(blob==tree[name],f'Archive content differs from tracked blob (export-subst?): {name}')
   require((paper/name).read_bytes()==raw,f'Working file differs from archived HEAD (including hidden Git flags): {name}')
   require(name not in seen,'Duplicate archive member');seen.add(name)
  require(seen==set(tree),'Archive omits tracked files (export-ignore?)')
  tf.extractall(destination,filter='data')
 return dict(files=len(tree),git_blob_algorithm=algo,all_paths_and_blobs_match=True)

def independent_science(analysis,model):
 import numpy as np
 import pandas as pd
 require(model['version']=='V197' and model['primary_dataset']=='user-provided16-city CSV','Runner supports declared user16 V197 science only; no legacy fallback')
 require(model['module']=='task4_user_v197_revision' and model['factory']=='revised_bounds' and model['results']=='results/task4_user_v197_revision','Unexpected primary implementation or output path')
 require(model['source_csv']=='data/task4_v117_team_intake/city_indicators.csv' and model['fixed_auxiliary_weight_total']==.1,'Source or retained weights differ')
 sys.path.insert(0,str(analysis/'scripts'))
 module=importlib.import_module(model['module']);frame,lo,hi=module.revised_bounds()
 from task4_user_v181_revision import revised_bounds as prior_bounds
 from task4_user_v192_revision import revised_bounds as v192_bounds
 from task4_v5_model import SPEC
 from task4_v5_model import NAMES,weights
 require(lo.shape==hi.shape==(16,10),'Expected exactly16cities x10indicators')
 require(frame.city.nunique()==16 and frame.country.nunique()==16,'Primary city/country scope mismatch')
 require(sha(analysis/model['source_csv'])=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c','Original user CSV differs')
 prior,oldlo,oldhi=prior_bounds();v192,v192lo,v192hi=v192_bounds()
 require(frame.city.tolist()==prior.city.tolist()==v192.city.tolist(),'City order changed')
 j=NAMES.index('public_transport_density');expected_changes=set()
 admissions=read(analysis/'design/task4_user_v192_admissions.json')
 require(len(admissions['observations'])==2,'Expected exactly two V192 conditional observations')
 for row,(city,population,year) in zip(admissions['observations'],[('Tokyo',9983365,2026),('Warsaw',1863800,2024)]):
  require(row['city']==city and row['indicator']=='public_transport_density' and row['raw_count']==38,'Unexpected V192 count or criterion')
  require(row['population']==population and row['population_year']==year and row['lower_bound_only'],'Retained V192 denominator or scope changed')
  i=frame.city.tolist().index(city);require(frame.iloc[i].population==population and frame.iloc[i].population_year==year,'Source and original population differ')
  require(oldlo[i,j]==0 and oldhi[i,j]==v192hi[i,j]==1,'Original V192 missing cell or upper bound changed')
  utility=3800000/(50*population+3800000)
  np.testing.assert_allclose(v192lo[i,j],utility,atol=1e-16,rtol=0)
  np.testing.assert_allclose(row['utility_after'],[utility,1],atol=1e-16,rtol=0)
  if city=='Tokyo':require(row['inventory_reference_year'] is None,'Tokyo catalogue metadata cannot become an observation year')
  expected_changes.add((i,j))
 require(set(map(tuple,np.argwhere(v192lo!=oldlo)))==expected_changes,'V192 lower-cell changes are not exactly Tokyo/Warsaw')
 np.testing.assert_array_equal(v192hi,oldhi)
 pool=read(analysis/'design/task4_user_v197_admissions.json');require(len(pool['observations'])==1,'Expected one V197 refinement')
 row=pool['observations'][0];i=frame.city.tolist().index('Zurich');k=NAMES.index('public_pool_density')
 require(row['city']=='Zurich' and row['indicator']==NAMES[k] and row['raw_count_before']==7 and row['raw_count']==12 and row['lower_bound_only'],'Unexpected Zurich refinement')
 require(len(row['venues'])==len(set(row['venues']))==12 and len(row['additional_venues'])==len(set(row['additional_venues']))==5 and set(row['additional_venues'])<=set(row['venues']),'Unexpected venue subset')
 require(row['excluded_adult_only'] not in row['venues'],'Adult-only excluded venue entered the subset')
 require(row['population']==frame.iloc[i].population==440935 and row['population_year']==frame.iloc[i].population_year==2025,'Original Zurich denominator changed')
 require(pool['unique_supplemented_city_indicator_keys']==25 and pool['newly_filled_cells']==0 and pool['refined_existing_partial_cells']==1,'Incorrect refinement scope')
 d=12*100000/440935;u=d/(SPEC[k][2]+d)
 np.testing.assert_allclose([lo[i,k],hi[i,k]],row['utility_after'],atol=1e-16,rtol=0)
 np.testing.assert_allclose(lo[i,k],u,atol=1e-16,rtol=0)
 require(0<v192lo[i,k]<lo[i,k] and v192hi[i,k]==hi[i,k]==1,'Expected partial interval refinement')
 require(set(map(tuple,np.argwhere(lo!=v192lo)))=={(i,k)},'Other 159 lower cells changed')
 np.testing.assert_array_equal(hi,v192hi)
 _,a,b=module.revised_bounds(False);np.testing.assert_array_equal(a,v192lo);np.testing.assert_array_equal(b,v192hi)
 for tokyo,warsaw in [(False,False),(True,False),(False,True)]:
  _,a,b=module.revised_bounds(True,tokyo,warsaw);expected=oldlo.copy();expected[i,k]=lo[i,k]
  for city,include in [('Tokyo',tokyo),('Warsaw',warsaw)]:
   if include:expected[frame.city.tolist().index(city),j]=v192lo[frame.city.tolist().index(city),j]
  np.testing.assert_array_equal(a,expected);np.testing.assert_array_equal(b,oldhi)
 frozen=pd.read_csv(analysis/model['results']/'utility_bounds.csv');frozen=frozen[frozen.scenario=='after_conditional']
 require(len(frozen)==160 and not frozen.duplicated(['city','indicator']).any(),'Frozen matrix is not exactly160unique cells')
 for i,city in enumerate(frame.city):
  for k,indicator in enumerate(NAMES):
   row=frozen[(frozen.city==city)&(frozen.indicator==indicator)].iloc[0]
   np.testing.assert_allclose([lo[i,k],hi[i,k]],[row.lower,row.upper],atol=2e-15,rtol=0)
 ranks=pd.read_csv(analysis/model['results']/'current_ranks.csv');require(len(ranks)==32,'Expected32frozen city-weight rows');result=[]
 for reference,w in [('fixed',np.array([.1125]*6+[.05,.1125,.1125,.05])),('equal',np.full(10,.1))]:
  if reference=='fixed':np.testing.assert_array_equal(w,weights(.1))
  def score(matrix):
   values=[]
   for row in matrix:
    positive=math.sqrt(math.fsum(float(q)*float(x)**2 for q,x in zip(w,row)))
    negative=math.sqrt(math.fsum(float(q)*(1-float(x))**2 for q,x in zip(w,row)))
    values.append(100*positive/(positive+negative))
   return np.array(values)
  lower,upper=score(lo),score(hi);regret=[];possible=[];necessary=[]
  for i in range(16):
   others=[k for k in range(16) if k!=i]
   regret.append(max(0,float(upper[others].max()-lower[i])))
   possible.append(bool(upper[i]>=lower[others].max()-1e-12))
   necessary.append(bool(lower[i]>=upper[others].max()-1e-12))
  regret=np.array(regret);rank=1+(regret[None,:]<regret[:,None]-1e-12).sum(axis=1)
  old=ranks[ranks.weight_reference==reference].set_index('city').loc[frame.city]
  for name,value in [('score_lower',lower),('score_upper',upper),('max_regret',regret),('decision_rank',rank)]:np.testing.assert_allclose(value,old[name].to_numpy(),atol=3e-13,rtol=0)
  require(possible==old.possible_champion.tolist() and necessary==old.necessary_champion.tolist(),'Possible/necessary champion flags differ')
  result.append(dict(weight_reference=reference,city_cases=16,conservative_recommendation=frame.loc[rank==1,'city'].tolist(),possible_champions=sum(possible),necessary_champions=sum(necessary),mean_score_interval_width=float((upper-lower).mean())))
 return dict(utility_cells=160,deterministic_city_weight_cases=32,changed_pool_lower_cells=1,other159cells_and_all_uppers_exact=True,source_population_and_count_formulas_checked=True,zurich_withdrawal_restores_V192=True,V192_two_transport_changes_and_withdrawals_checked=True,independent_score_reduction='Scalar math.fsum squared distances with weights once',comparisons=result,MC_rerun=False,raw_source_semantics_reaudited=False)

def layout(pdf,folder,pages):
 bbox=folder/'bbox.html';command(['pdftotext','-bbox',pdf,bbox]);root=E.parse(bbox).getroot()
 nodes=root.findall('.//{http://www.w3.org/1999/xhtml}page');require(len(nodes)==len(pages),'Physical PDF page count differs from extracted text')
 for i,page in enumerate(nodes):
  require(float(page.get('width'))==612 and float(page.get('height'))==792,'Expected native Letter page geometry')
  words=page.findall('.//{http://www.w3.org/1999/xhtml}word')
  require(not any(float(w.get('yMin'))>745 for w in words),'Unexpected footer-region text')
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]
   require(any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top),'Native left running head missing')
   require(any(w.text=='18213' for w in top),'Expected provisional18213running head missing')
   require(any(w.text=='Page' and float(w.get('xMin'))>450 for w in top),'Native right running head missing')
   require(f'Page {i+1} of {len(pages)}' in pages[i],'Logical running page number differs')
 return dict(physical_pages=len(nodes),native_letter_and_headers_footers_checked=True)

def pixels(pdf,folder):
 folder.mkdir();command(['pdftoppm','-r','72','-gray',pdf,folder/'page'])
 images=sorted(folder.glob('page-*.pgm'));require(images,'No rendered pages generated')
 return [sha(x) for x in images]

def expected_underfull(expected,kind):
 value=expected['underfull_counts']
 if isinstance(value,list):
  require(len(value)==2 and all(type(n) is int and n>=0 for n in value),'Invalid per-entry underfull counts')
  value=value[{'direct':0,'root':1}[kind]]
 require(type(value) is int and value>=0,'Invalid underfull count')
 return value

def build_one(kind,base,work,out,registry,expected,canonical_pages,canonical_pixels):
 source=work/kind/'source';source.parent.mkdir();shutil.copytree(base,source)
 removed=[]
 for path in list(source.rglob('*')):
  if path.is_file() and (path.suffix in {'.aux','.toc','.out','.log','.fls','.xdv','.fdb_latexmk'} or path.name.endswith('.synctex.gz')):
   removed.append(str(path.relative_to(source)));path.unlink()
 for name in [registry['pdf'],str(Path(registry['root_entry']).with_suffix('.pdf'))]:
  path=source/name
  if path.exists():removed.append(name);path.unlink()
 folder=out/kind;folder.mkdir();fresh=work/kind/'compiled';fresh.mkdir()
 if kind=='direct':tex=source/registry['tex'];cwd=tex.parent;search=['-Z','search-path=..']
 else:tex=source/registry['root_entry'];cwd=source;search=[]
 args=['tectonic','--only-cached',*search,'--outdir',str(fresh),'--keep-logs','--keep-intermediates','--makefile-rules',str(folder/'dependencies.mk'),tex.name]
 process=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
 (folder/'stdout.txt').write_bytes(process.stdout)
 log_file=fresh/tex.with_suffix('.log').name
 if log_file.exists():shutil.copyfile(log_file,folder/'build.log')
 require(process.returncode==0,f'{kind} offline TeX build failed; see {folder}/stdout.txt and build.log')
 pdf=fresh/tex.with_suffix('.pdf').name;require(pdf.exists(),'No fresh rebuilt PDF produced')
 log=(fresh/tex.with_suffix('.log').name).read_text()
 (folder/'build.log').write_text(log)
 require('Overfull' not in log and 'undefined' not in log and 'LaTeX Warning' not in log,'Unexpected TeX warning/error')
 require(log.count('Underfull')==expected_underfull(expected,kind),'Underfull count differs from current reviewed draft')
 pages=text_pages(pdf);require(pages==canonical_pages,'Per-page normalized text differs from registered PDF')
 require(len(pages)==expected['total_pages'],'Page count differs from current review')
 aux=(fresh/tex.with_suffix('.aux').name).read_text()
 label=lambda name:int(re.search(r'\\newlabel\{'+name+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 require(label('main-end')==expected['main_and_references_pages'],'Main/reference page count differs')
 require(label('main-end')<=25,'Retained25-page main budget exceeded')
 require(label('news-start')==expected['news_pages'][0] and label('news-end')==expected['news_pages'][1],'News page labels differ')
 require(len(re.findall(r'\\bibcite\{',aux))==expected['compiled_references'],'Compiled references differ')
 checked=layout(pdf,folder,pages);rendered=pixels(pdf,work/(kind+'-render'))
 require(rendered==canonical_pixels,'Rebuilt72dpi grayscale pixels differ from registered PDF')
 shutil.copyfile(pdf,folder/'rebuilt.pdf');shutil.copyfile(fresh/tex.with_suffix('.aux').name,folder/'labels.aux')
 return dict(kind=kind,passed=True,pdf_sha256=sha(pdf),text_pages_equal=True,grayscale_72dpi_pages_equal=len(rendered),underfull_paragraphs=log.count('Underfull'),removed_snapshot_outputs=removed,command=args,**checked)

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--research-root',type=Path,default=Path(__file__).resolve().parents[3]);parser.add_argument('--paper-root',type=Path)
 parser.add_argument('--output-dir',type=Path,required=True);args=parser.parse_args()
 research=args.research_root.resolve();paper=(args.paper_root or research.parent/'HiMCM-Overleaf').resolve();analysis=research/'research/2026-a'
 out=safe_output(args.output_dir,research,paper);started=time.time();report=dict(status='running',iteration='V198',runner_sha256=sha(Path(__file__)))
 science={};paper_hashes={};navigation={};states={};failure=None
 try:
  states={str(p):dict(head=git(p,'rev-parse','HEAD'),status=git(p,'status','--porcelain')) for p in [research,paper]}
  require(not states[str(paper)]['status'],'Paper working tree must be clean for exact HEAD archival')
  snapshot=read(analysis/'design/task4_user_v197_snapshot.json')['source_sha256']
  navigation_paths=[analysis/'design'/name for name in ['task4_user_current_model.json','task4_user_current_extensions.json','task4_user_current_review.json','task4_user_current_delivery.json']]
  require(len(snapshot)==361 and not any(str(path.relative_to(analysis)) in snapshot for path in navigation_paths),'Expected361immutable scientific bindings without mutable navigation')
  active_model,active_extensions,registry,delivery=[read(path) for path in navigation_paths]
  require(active_model['version']=='V197' and active_model['module']=='task4_user_v197_revision','Wrong active primary navigation')
  require(active_model['snapshot']=='design/task4_user_v197_snapshot.json','Wrong active immutable snapshot')
  require(active_extensions['extension_version']==active_extensions['primary_evidence_version']=='V197','Wrong active extension navigation')
  require(set(active_extensions['modules'])=={'preferences','future','method','diagnostics'},'Expected four retained extension modules')
  require(all(v['script']=='scripts/task4_v197_extensions.py '+k and v['results']=='results/task4_v197_'+k for k,v in active_extensions['modules'].items()),'Wrong active extension paths')
  require(registry['version']=='V198' and registry['primary_model']=='V197','Expected currentV198owned review onV197science')
  require(registry==read(paper/'drafts/task4_current_review.json'),'Review registries differ')
  require(delivery['version']=='V198' and delivery['review_version']=='V198' and delivery['primary_model']=='V197','Wrong active delivery navigation')
  require(delivery==read(paper/'drafts/task4_current_delivery.json'),'Delivery registries differ')
  require(delivery['pdf']==registry['pdf'] and delivery['pdf_sha256']==registry['pdf_sha256'],'Delivery belongs to a different PDF')
  science=dict(snapshot)
  for name,digest in science.items():require(sha(analysis/name)==digest,f'Science snapshot hash mismatch: {name}')
  paper_hashes=tracked_hashes(paper)
  canonical=paper/registry['pdf'];check_pdf_identity(canonical,registry['pdf_sha256'])
  expected_path=research/registry['research_verification'];expected=read(expected_path)
  require(expected['status']=='pass' and expected['version']=='V198' and expected['pdf_sha256']==registry['pdf_sha256'],'Review verification belongs to different science or PDF')
  delivery_proof_path=research/delivery['research_verification'];delivery_proof=read(delivery_proof_path)
  require(delivery_proof['status']=='pass' and delivery_proof['pdf_sha256']==registry['pdf_sha256'],'Current delivery verification has not passed for this PDF')
  keys=expected['reference_keys'];review_ref_count=len(keys) if isinstance(keys,list) else keys
  require(type(review_ref_count) is int and review_ref_count==delivery_proof['compiled_references']==56,'Reference count evidence differs')
  expected=dict(expected,news_pages=delivery_proof['news_pages'],compiled_references=delivery_proof['compiled_references'])
  navigation={str(path):sha(path) for path in [*navigation_paths,expected_path,delivery_proof_path]}
  report.update(paper_version=registry['version'],primary_model='V197',delivery_version=delivery['version'],paper_head=states[str(paper)]['head'],research_head=states[str(research)]['head'],canonical_pdf_sha256=registry['pdf_sha256'],
   source_bindings_sha256={str(path.relative_to(research)):sha(path) for path in [*navigation_paths,analysis/'design/task4_user_v197_snapshot.json',expected_path,delivery_proof_path]})
  versions={name:command([name,'--version'] if name=='tectonic' else [name,'-v']).splitlines()[0] for name in ['tectonic','pdftotext','pdftoppm']}
  report['environment']=dict(python=sys.version.split()[0],executable=sys.executable,tools=versions,packages={x:importlib.metadata.version(x) for x in ['numpy','pandas','scipy','matplotlib']},tex_resources='Existing local Tectonic cache required;no resource-download fallback')
  (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('Inputs bound to current registries;isolating paper HEAD',flush=True)
  with tempfile.TemporaryDirectory(prefix='work-',dir=out) as temp:
   work=Path(temp);base=work/'snapshot';report['archive']=archive_snapshot(paper,base,work)
   canonical_pages=text_pages(canonical);layout(canonical,out,canonical_pages)
   canonical_pixels=pixels(canonical,work/'canonical-render')
   report['historical_snapshot_navigation_exceptions']=[]
   report['science']=independent_science(analysis,read(analysis/'design/task4_user_current_model.json'))
   print('Science160cells/32cases reproduced;building two isolated offline entries',flush=True)
   with ThreadPoolExecutor(max_workers=2) as pool:
    jobs=[(k,pool.submit(build_one,k,base,work,out,registry,expected,canonical_pages,canonical_pixels)) for k in ['direct','root']]
    report['builds']=[]
    for kind,job in jobs:
     try:report['builds'].append(job.result())
     except Exception as error:report['builds'].append(dict(kind=kind,passed=False,error=f'{type(error).__name__}: {error}'))
    require(all(x['passed'] for x in report['builds']),'At least one isolated offline build failed; see per-build evidence')
   report['status']='pass'
 except Exception as e:failure=e;report.update(status='fail',error=f'{type(e).__name__}: {e}')
 finally:
  changed=[]
  for n,h in science.items():
   if not (analysis/n).is_file() or sha(analysis/n)!=h:changed.append('science:'+n)
  for n,h in navigation.items():
   if not Path(n).is_file() or sha(Path(n))!=h:changed.append('navigation:'+n)
  for n,h in paper_hashes.items():
   if not (paper/n).is_file() or sha(paper/n)!=h:changed.append('paper:'+n)
  for repo,state in states.items():
   p=Path(repo)
   if git(p,'rev-parse','HEAD')!=state['head'] or git(p,'status','--porcelain')!=state['status']:changed.append('git:'+repo)
  report['input_protection']=dict(scientific_files_checked=len(science),paper_files_checked=len(paper_hashes),navigation_and_verification_files_checked=len(navigation),changed=changed)
  if changed:report.update(status='fail',error='Protected inputs or Git states changed');failure=RuntimeError(report['error'])
  report.update(elapsed_seconds=round(time.time()-started,3),scope='Local tools+existing TeX cache;source-defined deterministic model and exact text/72dpi rendering checks. No fresh-OS/no-cache guarantee,MC replay,source revalidation,server compile or submission-readiness claim.',submission_ready=False)
  (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(status=report['status'],report=str(out/'report.json'),elapsed_seconds=report['elapsed_seconds'])),flush=True)
 return 1 if failure else 0
if __name__=='__main__':raise SystemExit(main())
