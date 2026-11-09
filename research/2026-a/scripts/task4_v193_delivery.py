"""Scoped delivery evidence for the owned V193 PDF, preserving all readiness gates."""
import csv,hashlib,json,re,subprocess,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v193_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('–','-').replace('−','-').replace('—','-')
 return ' '.join(re.sub(r'-[ \t]*\n[ \t]*','-',s).split()).casefold()
def hit(m,s,line=False):return any(norm(x)==norm(m) for x in s.splitlines()) if line else re.search(r'(?<!\w)'+re.escape(norm(m))+r'(?!\w)',norm(s)) is not None
def main():
 pdf=P/'drafts/task4_v193_paper.pdf';raw=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True).split('\f');assert not raw[-1].strip();pages=raw[:-1];aux=Path('/data/scratch/himcm_v193_build/task4_v193_paper.aux').read_text()
 def label(n):return int(re.search(r'\\newlabel\{'+n+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])
 total=len(pages);end=label('main-end');news=[label('news-start'),label('news-end')];assert end<=25 and total==end+2==label('LastPage')
 refs=[i+1 for i,p in enumerate(pages) if hit('References',p,True)];assert len(refs)==1;refs=refs[0]
 count=len(re.findall(r'\\bibcite\{',aux));assert count==56
 prior=R/'results/task4_v190_delivery/requirements.csv';rows=list(csv.DictReader(prior.open()));assert len(rows)==47;anchors=[]
 updates={
 'PA-data':'Owned collection explains conditional Tokyo38/Warsaw38subsets plus priorAmsterdam; retainedsourcepopulation/yearlimitations',
 'PA-references':f'{count}compiledreferences;prior53keysplus3verifiedstation-sourcekeys',
 'U-preserve':'OriginalCSVpreserved;Tokyo/Warsawtransportlowerboundsaddedonly;other158cells/alluppers/weights/anchors/intervalrulesunchanged',
 'U-source-quality':'V192source-diagnosticsrecomputecommutewithdrawals/singlemean/jointbox;newtwostationdirectoriesmatchdeclaredgeographies;original112pointsnotfullycertified',
 'AI-verification':'V192fullresearchauditandV193ownedpaper/assetsaudit;source/numericprovenancebound;frozenAIcaptureunchanged',
 'U-MC-precision':'V192specifiedexportfamily2064means37settings;4440pairintervals4260clear180unresolved22uniqueminima;notalladditionalprimaryMCsettings',
 'U-matrix-visual':'Figure1V192160cells112point37partial11unknown;travelproxycaptionretained;minimum10ptat6.5in',
 'U-collection-compression':'OwnedcollectionaddsTokyo/Warsawreal-directorysourcesandcompressesAmsterdamwordingwithoutchangingitscounts/year/screenconditions',
 'CI-budget':f'{end}main/reference+2provisionalAI;{25-end}page margin',
 'CI-file':f'{pdf.stat().st_size}bytes;oneV193ownedPDF',
 'TEAM-independent-entry':f'V193direct/rootlocalbuilds;{total}pages;frozenAIandteamfilespreserved',
 'TEAM-shared-build':'FreshV193read-onlysharedmainlocalcheckfailsatmain.tex143missingframework.png;unchangedteamsources;shared_build_check.jsonandshared_main.log'}
 for row in rows:
  key=row['id'];markers=json.loads(row['passage_markers']);lo,hi=3,news[0]-1;line=False
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
   row[field]=row[field].replace('V181','V192').replace('V189','V193').replace('V190','V193')
  if key in updates:row['evidence']=updates[key]
  if key=='CI-budget':row['scope_or_remaining_action']=f'{25-end}mainpagesremainunderretained25-pagebudget;notfinalsubmissioncertification'
 pending=[x['id'] for x in rows if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==13
 assert not hit('Exa','example') and hit('Exa','Exa assistance')
 for name,records in [('requirements.csv',rows),('anchor_hits.csv',anchors)]:
  with (O/name).open('w') as f:
   w=csv.DictWriter(f,fieldnames=list(records[0]),lineterminator='\n');w.writeheader();w.writerows(records)
 report=dict(version='V193delivery',status='pass',primary_model='V192',review_version='V193',pdf_sha256=sha(pdf),total_pages=total,main_and_references_pages=end,main_page_margin=25-end,news_pages=news,references_pages=list(range(refs,end+1)),AI_pages=[end+1,total],compiled_references=count,requirements=47,scoped_anchor_rows=len(anchors),all_scoped_anchors_found=True,statuses_preserved=True,pending_count=13,pending_ids=pending,source_sha256={str(p.relative_to(R)):sha(p) for p in [prior,Path(__file__),O/'shared_build_check.json',O/'shared_main.log']},output_sha256={n:sha(O/n) for n in ['requirements.csv','anchor_hits.csv']},submission_ready=False,server_compile_verified=False,scope='Scoped passage locations and preserved status gates; not proof of complete original-source validation, full-teamAI,registrationorcontestdelivery.')
 (O/'delivery_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','total_pages','main_and_references_pages','compiled_references','scoped_anchor_rows','pending_count']}))
if __name__=='__main__':main()
