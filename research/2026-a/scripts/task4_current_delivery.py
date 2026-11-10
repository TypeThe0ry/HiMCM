"""Scoped delivery evidence for the single current manuscript and spatial figure."""
import csv,hashlib,json,re,subprocess,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/current_spatial_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('–','-').replace('−','-').replace('—','-')
 return ' '.join(re.sub(r'-[ \t]*\n[ \t]*','-',s).split()).casefold()
def hit(m,s,line=False):return any(norm(x)==norm(m) for x in s.splitlines()) if line else re.search(r'(?<!\w)'+re.escape(norm(m))+r'(?!\w)',norm(s)) is not None
def main():
 pdf=Path('/data/scratch/himcm-current-spatial-final-build/main.pdf');raw=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f');assert not raw[-1].strip();pages=raw[:-1];aux=Path('/data/scratch/himcm-current-spatial-final-build/main.aux').read_text()
 def label(n):return int(re.search(r'\\newlabel\{'+n+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 total=len(pages);end=label('main-end');news=[label('news-start'),label('news-end')];assert end<=25 and total==end+2==label('LastPage')
 refs=[i+1 for i,p in enumerate(pages) if hit('References',p,True)];assert len(refs)==1;refs=refs[0]
 count=len(re.findall(r'\\bibcite\{',aux));assert count==59
 prior=R/'results/task4_v201_review/requirements.csv';rows=list(csv.DictReader(prior.open()));assert len(rows)==47;anchors=[]
 updates={
 'PA-sample':'Retained 16-city by 10-indicator primary sample and V200 ranking table',
 'U-perturbation':'V200 Dirichlet preference and bounded future shocks; joint mean-box boundaries 1.57080% fixed and 63.44548% equal; historical utility-only mass budgets',
 'PA-data':'25 supplemented city-indicator keys; Singapore 25 physical venues; withholding 3 notice-affected venues leaves 22; four pool-specific notices; Zurich school-session limits retained',
 'PA-references':f'{count} reference keys; two spatial/NASA references added; all prior keys retained',
 'U-preserve':'Original CSV preserved; Singapore pool inventory lower bound refined 7 to 25 venues from V197; other 159 cells and all upper bounds unchanged; weights and anchors unchanged',
 'U-source-quality':'V200source-diagnosticsandV201sourceaudit;Zurich12namedsubsetfromoriginalHTMLwithaccessrestrictions;112originalpointsnotfullycertified',
 'AI-verification':'V200fullresearchauditandV201ownedpaper/assetsaudit;source/numericprovenancebound;frozenAIcaptureunchanged',
 'U-MC-precision':'V200specifiedexportfamily2064means37settings;4440 pair intervals, 4259 certified, 181 unresolved, 17 unique minima;notalladditionalprimaryMCsettings',
 'U-matrix-visual':'Figure1V200160cells112point37partial11unknown;travelproxycaptionretained;minimum10ptat6.5in',
 'U-collection-compression':'OwnedsourcetextaddsZurichfivepublicschoolvenuesandlimits;25distinctkeys;conciseoriginal-inputcountandMCparagraphspreserveallmaterialconditions',
 'CI-budget':f'{end}main/reference+2provisionalAI;{25-end}page margin',
 'CI-file':f'{pdf.stat().st_size}bytes;oneV201ownedPDF',
 'TEAM-independent-entry':f'Single actual local main build; {total} pages; prior independent numerical audit and frozen AI window retained',
 'TEAM-shared-build':'Pending actual root main V201 compilation proof; online server compilation not verified'}
 proof_path=O/'verification.json'; proof=json.loads(proof_path.read_text()) if proof_path.exists() else {}
 shared=(proof.get('status')=='pass' and proof.get('pdf_sha256')==sha(pdf) and proof.get('main_tex_sha256')==sha(P/'main.tex') and proof.get('total_pages')==total and proof.get('main_reference_pages')==end)
 O.mkdir(exist_ok=True)
 if shared: updates['TEAM-shared-build']='Actual local root main V201 compilation matches final PDF text and rendered pages; online server compilation unverified'
 for row in rows:
  key=row['id'];markers=json.loads(row['passage_markers']);lo,hi=3,news[0]-1;line=False
  replacements={'PA-best':['conservative recommendation under the stated criteria and intervals','Zurich minimizes maximum regret'], 'U-model-count':['TOPSIS is the primary score','VIKOR'], 'PA-news':['largest possible shortfall','These are conditional model outcomes'], 'U-age':['shared unknown-age mass once','0.23842','not observed age effects'], 'U-MC-precision':['Numerical precision','2064 exported means','city mean-rank ordering remains unresolved']}
  if key in replacements: markers=replacements[key]; row['passage_markers']=json.dumps(markers)
  if key=='PA-summary':lo=hi=1
  if key=='PA-toc':lo=hi=2;line=True
  if key=='PA-news':lo,hi=news
  if key=='PA-references':lo=hi=refs;line=True
  if key in ['PA-ai-section','AI-tool-disclosure']:lo,hi=end+1,total
  if key=='U-MC-precision':
   where=[i+1 for i,p in enumerate(pages) if hit('Numerical precision can be quantified separately',p)];assert len(where)==1;lo=where[0];hi=min(lo+1,news[0]-1)
  found=set()
  for marker in markers:
   matches=[i for i in range(lo,hi+1) if hit(marker,pages[i-1],line)];assert matches,(key,marker)
   found.update(matches);anchors.append(dict(id=key,marker=marker,match_mode='line' if line else 'phrase',allowed_page_start=lo,allowed_page_end=hi,hit_pages=','.join(map(str,matches))))
  if markers:row['pdf_pages']=','.join(map(str,sorted(found)));row['page_basis']=f'Scoped whole-word anchors;pages{lo}-{hi}'
  if key=='PA-references':row['pdf_pages']=','.join(map(str,range(refs,end+1)));row['page_basis']='References heading throughmain-endbeforeAI'
  if key=='U-template-format':row['pdf_pages']=f'1-{total}'
  for field in ['evidence','scope_or_remaining_action']:
   row[field]=row[field].replace('V192','V200').replace('V196','V201')
  if key in updates:row['evidence']=updates[key]
  if key=='TEAM-shared-build' and shared: row['status']='technical_pass'; row['scope_or_remaining_action']='Local main entry verified; online server compilation and team integration remain unverified'
  if key=='U-preserve': row['scope_or_remaining_action']='V200 admits the Singapore physical-inventory refinement without changing original values or model rules'
  if key=='U-MC-precision': row['scope_or_remaining_action']='V200 simulation exports; IID within setting; no real-world winner probability or forecast calibration'
  if key=='CI-budget':row['scope_or_remaining_action']=f'{25-end}mainpagesremainunderretained25-pagebudget;notfinalsubmissioncertification'
 row=dict(rows[0]); row.update(id='U-spatial-visual',authority='User satellite and3D figure request,10November2026',requirement='Real satellite context and meaningful three-dimensional evidence figure',status='reviewed_scoped',evidence='Zurich NASA HLS context and both cities quantitative0–150minute extrusions; raw imagery archived and resident-weighted fractions independently recomputed',scope_or_remaining_action='Generic Learning-POI resident proxy; source city input dates unstated; no student or pool access, physical heights or primary-score revision')
 figpage=label('fig:walktime-context');row['pdf_pages']=str(figpage);markers=['Walking time across retained city grids','height is not terrain or buildings'];row['passage_markers']=json.dumps(markers);row['page_basis']=f'Scoped whole-word anchors;pages{figpage}-{figpage}'
 for marker in markers:
  assert hit(marker,pages[figpage-1]),marker
  anchors.append(dict(id=row['id'],marker=marker,match_mode='phrase',allowed_page_start=figpage,allowed_page_end=figpage,hit_pages=str(figpage)))
 rows.append(row)
 pending=[x['id'] for x in rows if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==(12 if shared else 13)
 assert not hit('Exa','example') and hit('Exa','Exa assistance')
 for name,records in [('requirements.csv',rows),('anchor_hits.csv',anchors)]:
  with (O/name).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
 report=dict(version='Current spatial manuscript delivery',status='pass',primary_model='V200',review_version='V201',pdf_sha256=sha(pdf),total_pages=total,main_and_references_pages=end,main_page_margin=25-end,news_pages=news,references_pages=list(range(refs,end+1)),AI_pages=[end+1,total],compiled_references=count,requirements=48,scoped_anchor_rows=len(anchors),all_scoped_anchors_found=True,prior_statuses_preserved_except_shared_build=True,shared_build_local_verified=shared,pending_count=len(pending),pending_ids=pending,source_sha256={str(p.relative_to(R)):sha(p) for p in [prior,Path(__file__)]+([proof_path] if shared else [])},output_sha256={n:sha(O/n) for n in ['requirements.csv','anchor_hits.csv']},submission_ready=False,server_compile_verified=False,scope='Current single main, spatial figure passage locations and preserved status gates; not proof of complete original-source validation, full-teamAI,registrationorcontestdelivery.')
 (O/'delivery_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','total_pages','main_and_references_pages','compiled_references','scoped_anchor_rows','pending_count']}))
if __name__=='__main__':main()
