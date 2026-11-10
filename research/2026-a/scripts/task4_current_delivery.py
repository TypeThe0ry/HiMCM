"""Scoped delivery evidence for the single current manuscript and spatial figure."""
import csv,hashlib,json,re,subprocess,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/current_paper_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('–','-').replace('−','-').replace('—','-')
 return ' '.join(re.sub(r'-[ \t]*\n[ \t]*','-',s).split()).casefold()
def hit(m,s,line=False):return any(norm(x)==norm(m) for x in s.splitlines()) if line else re.search(r'(?<!\w)'+re.escape(norm(m))+r'(?!\w)',norm(s)) is not None
def main():
 pdf=Path('/data/scratch/himcm-current-main-build/main.pdf');raw=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f');assert not raw[-1].strip();pages=raw[:-1];aux=Path('/data/scratch/himcm-current-main-build/main.aux').read_text()
 def label(n):return int(re.search(r'\\newlabel\{'+n+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 model_path=R/'design/task4_user_current_model.json';model=json.loads(model_path.read_text());assert model['version']=='V203'
 ranks_path=R/model['results']/'current_ranks.csv';ranks=list(csv.DictReader(ranks_path.open()))
 choices={w:[r['city'] for r in ranks if r['scenario']=='after_conditional' and r['weight_reference']==w and int(r['decision_rank'])==1] for w in ['fixed','equal']}
 assert choices=={'fixed':['Oslo'],'equal':['Zurich']}
 country_number=re.search(r'\\newlabel\{fig:country-contrasts\}\{\{([^}]+)\}',aux)[1];country_page=label('fig:country-contrasts')
 country_text_pages=[i+1 for i,p in enumerate(pages) if hit('The primary sample has one city per country',p)];assert len(country_text_pages)==1
 assert sha(pdf)==sha(R.parents[1]/'paper/current/main.pdf') and sha(P/'main.tex')==sha(R.parents[1]/'paper/current/main.tex')
 total=len(pages);end=label('main-end');news=[label('news-start'),label('news-end')];assert end<=25 and total==end+2==label('LastPage')
 refs=[i+1 for i,p in enumerate(pages) if hit('References',p,True)];assert len(refs)==1;refs=refs[0]
 count=len(re.findall(r'\\bibcite\{',aux));assert count==62
 prior=R/'results/current_spatial_review/requirements.csv';rows=list(csv.DictReader(prior.open()));assert len(rows)==48;anchors=[]
 updates={
 'AI-tool-disclosure':'KnownCodexandExa; preservedV178prefix plus bounded continuation42rootcontexts/197visible/1372top-levelinputs;78spawnrequests28Terra/7Luna/43omitted; requestlabels not attested servingversions',
 'AI-complete-record':'Two authenticated windows of one root session; selected private exports are not submission transcripts; team and later-cutoff records incomplete',
 'U-age': 'Retained Istanbul2012 joint feasibility proof and finite witnesses; Oslo2023 reported grade8/Vg3 meeting-place provision66/41percent and monthly sports-club activity70/32percent; cross-sectional student evidence, not exact ages',
 'U-country':f'Section7 on page{country_text_pages[0]}; Figure{country_number} on page{country_page}; frozen auxiliary four-city cases,20 contrasts,7 sign-identified; unchanged',
 'U-country-visual':f'Figure{country_number} on page{country_page}; unchanged20differences,7excludezero,4oldscore ranges;min9.5pt/source scope unchanged',
 'PA-sample':'Retained 16-city by 10-indicator primary sample and V203 ranking table',
 'U-perturbation':'V203 Dirichlet preference and bounded future shocks; joint mean-box boundaries15.60633% fixed-Oslo and0.64834% equal-Zurich;112pointutility boxes expanded with48otherintervalsfixed;epsilon.05retainsOslo/Zurich;fixedchangebandnear.08135733;equalZurich0-.2;single-pointignorance112casesperweightchanges10fixed/35equal;countsnoterrorprobabilities;historicalmassbudgets',
 'PA-data':'25supplementedkeys;Singapore26physicalvenues(25ActiveSG+oneOCBC);old3noticewithholding23/all4withholding22;OCBCpublicper-entry,age,hoursandclosureconstraints;Zurichschool-sessionlimitsretained',
 'PA-references':f'{count} reference keys; all61prior reference keys retained; Entur source retained',
 'U-preserve':'Original CSV preserved; Oslo transit lower bound refined89to626single-modebusgroups;other159lowercellsandalluppersunchanged;weightsandanchorsunchanged',
 'U-source-quality':'Oslo2009Eurostatvalue/yearmatchnotprovenCSVlineage;Oslo-onlycommutewithdrawalZurichboth;V203626single-modebusinventory;Tvetenbruomittedprecautionarily;primaryfixedOslo/equalZurich;829all-modealternativeand89withdrawalkeptdistinct;112originalpointsnotfullycertified',
 'AI-verification':'V203fullresearchauditandcurrent-main-and-assetsaudit;source/numericprovenancebound;frozenAIcaptureunchanged',
 'U-MC-precision':'V203specifiedexportfamily2064means37settings;4440 pair intervals, 4271 certified, 169 unresolved, 23 unique minima;notalladditionalprimaryMCsettings',
 'U-spatial-visual':'Oslo99.18%andZurich99.97%retained-residentgenericLearningPOIgrids;Oslogeo-only3transparentNASAresponses;ZRrawcloudsatellite;min9ptat6.5in;notstudents/highschools/poolaccess',
 'U-matrix-visual':'Figure1V203160cells112point37partial11unknown;travelproxycaptionretained;minimum10ptat6.5in',
 'U-collection-compression':'OwnedsourcetextaddsZurichfivepublicschoolvenuesandlimits;25distinctkeys;conciseoriginal-inputcountandMCparagraphspreserveallmaterialconditions',
 'CI-budget':f'{end}main/reference+2provisionalAI;{25-end}page margin',
 'CI-file':f'{pdf.stat().st_size}bytes;one current owned PDF',
 'TEAM-independent-entry':f'Single actual local main build; {total} pages; prior independent numerical audit and frozen AI window retained',
 'TEAM-shared-build':'Pending actual root current main compilation proof; online server compilation not verified'}
 proof_path=O/'verification.json'; proof=json.loads(proof_path.read_text()) if proof_path.exists() else {}
 shared=(proof.get('status')=='pass' and proof.get('pdf_sha256')==sha(pdf) and proof.get('main_sha256')==sha(P/'main.tex') and proof.get('total_pages')==total and proof.get('main_and_reference_pages')==end)
 O.mkdir(exist_ok=True)
 if shared: updates['TEAM-shared-build']='Actual local root current main compiles to the independently audited PDF; clean Git rendering reproduction is recorded separately; online server compilation unverified'
 for row in rows:
  key=row['id'];markers=json.loads(row['passage_markers']);lo,hi=3,news[0]-1;line=False
  replacements={'U-perturbation':['Dirichlet','conditional stress frequencies','critical radii','112 point utilities','expanded uncertainty box','111 points and 48 existing intervals','neither measurement errors nor error probabilities'], 'U-spatial-visual':['Walking time across retained city grids','height is not terrain','99.18%'], 'U-country':['The primary sample has one city per country','outside the sixteen-city ranking'], 'U-source-quality':['numerator 340','rate 0.14','626'], 'PA-best':['conservative recommendation under the stated criteria and intervals','Oslo minimizes maximum regret'], 'U-model-count':['TOPSIS is the primary score','VIKOR'], 'PA-news':['largest possible shortfall','Trying different priorities'], 'U-age':['shared unknown-age mass once','0.23842','not observed age effects','local provision of youth meeting places','sports-club activity'], 'U-MC-precision':['2.38 percentage points','exported means','23 of 37 settings']}
  if key in replacements: markers=replacements[key]; row['passage_markers']=json.dumps(markers)
  if key=='PA-summary':lo=hi=1
  if key=='PA-toc':lo=hi=2;line=True
  if key=='PA-news':lo,hi=news
  if key=='PA-references':lo=hi=refs;line=True
  if key=='U-spatial-visual':lo=hi=label('fig:walktime-context')
  if key in ['PA-ai-section','AI-tool-disclosure']:lo,hi=end+1,total
  if key=='U-MC-precision':
   where=[i+1 for i,p in enumerate(pages) if hit('exported means',p)];assert len(where)==1;lo=where[0];hi=min(lo+1,news[0]-1)
  found=set()
  for marker in markers:
   matches=[i for i in range(lo,hi+1) if hit(marker,pages[i-1],line)];assert matches,(key,marker)
   found.update(matches);anchors.append(dict(id=key,marker=marker,match_mode='line' if line else 'phrase',allowed_page_start=lo,allowed_page_end=hi,hit_pages=','.join(map(str,matches))))
  if markers:row['pdf_pages']=','.join(map(str,sorted(found)));row['page_basis']=f'Scoped whole-word anchors;pages{lo}-{hi}'
  if key=='U-country':
   row['pdf_pages']=','.join(map(str,sorted(found|{country_page})));row['page_basis']='Narrative phrase anchors and compiled country-figure label'
  if key=='PA-references':row['pdf_pages']=','.join(map(str,range(refs,end+1)));row['page_basis']='References heading throughmain-endbeforeAI'
  if key=='U-template-format':row['pdf_pages']=f'1-{total}'
  for field in ['evidence','scope_or_remaining_action']:
   row[field]=row[field].replace('V192','V203').replace('V196','V201')
  if key in updates:row['evidence']=updates[key]
  if key=='TEAM-shared-build' and shared: row['status']='technical_pass'; row['scope_or_remaining_action']='Local main entry verified; online server compilation and team integration remain unverified'
  if key=='PA-best':row['scope_or_remaining_action']=f"Fixed weights: {', '.join(choices['fixed'])}; equal weights: {', '.join(choices['equal'])}; conditional conservative recommendations,16 possible and zero necessary champions"
  if key=='TEAM-integration':
   row['evidence']='Single current owned main is active; teammate original is preserved in the GitHub archive'
   row['scope_or_remaining_action']='Final team acceptance and any specifically authorized teammate-text integration remain unverified'
  if key=='TEAM-independent-entry':row['requirement']='Current single main compiles locally'
  if key=='U-template-format':row['scope_or_remaining_action']='Original teammate text is archived; shared class and bibliography preserved; actual registration and online compiler settings unverified'
  if key=='U-age':row['scope_or_remaining_action']='Oslo school-grade comparisons have unstated item/grade denominators; reported provision and participation are not causal age effects, objective access or elicited weights; original2012model remains historical'
  if key=='U-preserve': row['scope_or_remaining_action']='V203 admits only the626source-definedbusinventorylowerrefinement;otherinputsandrulespreserved'
  if key=='U-MC-precision': row['scope_or_remaining_action']='V203 simulation exports; IID within setting; no real-world winner probability or forecast calibration'
  if key=='CI-budget':row['scope_or_remaining_action']=f'{25-end}mainpagesremainunderretained25-pagebudget;notfinalsubmissioncertification'
 pending=[x['id'] for x in rows if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==(12 if shared else 13)
 assert not hit('Exa','example') and hit('Exa','Exa assistance')
 for name,records in [('requirements.csv',rows),('anchor_hits.csv',anchors)]:
  with (O/name).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
 report=dict(version='Current manuscript delivery',status='pass',primary_model='V203',review_version='current',pdf_sha256=sha(pdf),total_pages=total,main_and_references_pages=end,main_page_margin=25-end,news_pages=news,references_pages=list(range(refs,end+1)),AI_pages=[end+1,total],compiled_references=count,requirements=48,scoped_anchor_rows=len(anchors),all_scoped_anchors_found=True,prior_statuses_preserved_except_shared_build=True,shared_build_local_verified=shared,pending_count=len(pending),pending_ids=pending,source_sha256={str(p.relative_to(R)):sha(p) for p in [prior,Path(__file__),model_path,ranks_path]+([proof_path] if shared else [])},output_sha256={n:sha(O/n) for n in ['requirements.csv','anchor_hits.csv']},compiled_aux_sha256=sha(Path('/data/scratch/himcm-current-main-build/main.aux')),derived_recommendations=choices,derived_country_figure=dict(number=country_number,page=country_page,text_page=country_text_pages[0]),submission_ready=False,server_compile_verified=False,scope='Current single main, spatial figure passage locations and preserved status gates; not proof of complete original-source validation, full-teamAI,registrationorcontestdelivery.')
 (O/'delivery_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','total_pages','main_and_references_pages','compiled_references','scoped_anchor_rows','pending_count']}))
if __name__=='__main__':main()
