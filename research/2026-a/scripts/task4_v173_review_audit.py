"""Validate owned collection compression, retained scope and current delivery facts."""
from pathlib import Path
from collections import Counter
import csv,json,re,xml.etree.ElementTree as E
from task4_v172_review_audit import norm,pdftext,rows,read,sha
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v173_collection_review';T=Path('/data/scratch')
def table(name,data):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
def citation_keys(s):return sorted({k for group in re.findall(r'\\cite\{([^}]+)\}',s) for k in group.split(',')})
def main():
 science=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in science.items():assert sha(R/n)==h,n
 protected=read(O/'protected_files.json')['manuscript']
 for n,h in protected.items():
  if n!='drafts/task4_current_review.json':assert sha(P/n)==h,n
 D=P/'drafts';old=(D/'task4_v172_core.tex').read_text();new=(D/'task4_v173_core.tex').read_text();section=(D/'task4_v173_collection.tex').read_text()
 a=old.index('\\subsection{Collection problems and their resolution}');b=old.index('Figure~\\ref{fig:identification-matrix}')
 assert new==old[:a]+section+old[b:]
 assert citation_keys(old[a:b])==citation_keys(section)
 m=read(D/'task4_v173_manifest.json');assert sha(D/'task4_v172_core.tex')==m['base_core_sha256'] and sha(D/'task4_v173_collection.tex')==m['collection_sha256']
 assert m['before_whitespace_tokens']==1482 and m['after_whitespace_tokens']==976
 assert m['shared_class_sha256']==sha(P/'mcmthesis.cls')
 assert (D/'task4_v173_paper.tex').read_text()==(D/'task4_v172_paper.tex').read_text().replace('% V172 owned review;','% V173 owned review;').replace('task4_v172_core.tex','task4_v173_core.tex')
 facts={
 'facility_bounds':['89','186','446','235','19 Helsinki','11 in Espoo','[d/(a+d),1]','uncounted providers unknown'],
 'boundary_entities':['city boundary','28079','191','unverified depot objects','99 metro','U-Bahn subset','other modes uncounted','Milano name and code 015146','104','Paddington','December 2025 London-region'],
 'vintage_and_status':['16 October 2024','RATP 2021 and Apur 2022','not relabelled','November 2026','Paris\'s 2023','Dublin\'s 2022','Singapore\'s 2024','Heiwadai','February--May 2027','not a current closure','not basins or lanes'],
 'education_scope':['full-time equivalents (FTE)','80,073','6,877.1','8,748','737.8','71,325','rounding envelope','6139.2,6139.4','adult and non-daytime','upper-secondary years 1--3','all ownership types','15 October','16.42091405','16.35,16.45','119,740','six youth school routes','adult-inclusive','2,487--8,148','unit-rounding assumption'],
 'unmatched_denominators':['794','153.65','without upper-stage allocation','post-baccalaureate','post-primary vocational','411.8','376.1','not a payroll ceiling','one-sided error envelope','All three city PTRs remain unknown'],
 'retained_rates':['numerator 340','ten provisional victims','one completed offence in 2024 and two in 2025','independently of victims','rate 0.14','Both original entries remain'],
 'unobserved_travel':['no midpoints','artificial open-tail cap','1,811','989','1,635','not complete headcounts','Uncovered mass retains $[0,1]$','interval convex hull','0.21048,0.61884','2020 school-stage proxy','not an identified 2025','2023 plan','issued in 2024','sample base 22','15 and above','travel utility remains unknown']}
 flat=norm(section)
 for category,markers in facts.items():
  for marker in markers:assert norm(marker) in flat,(category,marker)
 (O/'semantic_coverage.json').write_text(json.dumps(dict(categories=facts,source_review='education independently reviewed old and new prose;required scope restored and Berlin mode/zone ambiguity corrected',model_values_changed=False,omitted_material='Repeated caveats and selected extraction subtotals;frozen sources retain all raw records',citations_preserved=citation_keys(section)),indent=2)+'\n')
 pdf=D/'task4_v173_paper.pdf';text=pdftext(pdf);assert norm(text)==norm(pdftext(T/'himcm_v173_proxy/task4_v173_review_entry.pdf'))
 pages=[norm(x) for x in text.split('\f') if x.strip()];assert len(pages)==26
 aux=(T/'himcm_v173_build/task4_v173_paper.aux').read_text()
 for label,page in [('fig:identification-matrix',8),('fig:country-contrasts',17),('news-start',18),('news-end',19),('main-end',24),('LastPage',26)]:assert int(re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])==page
 assert len(re.findall(r'\\bibcite\{',aux))==49
 assert 'Figure 2:' in pages[10] and 'Conservative baseline decision ranks' in pages[9]
 bbox=E.parse(T/'himcm_v173_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(bbox)==26
 for i,page in enumerate(bbox):
  assert float(page.get('width'))==612 and float(page.get('height'))==792
  words=page.findall('.//{http://www.w3.org/1999/xhtml}word');assert not [w for w in words if float(w.get('yMin'))>745]
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]
   assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
   assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
   assert f'Page {i+1} of 26' in pages[i]
 logs=[(O/n).read_text() for n in ['direct_build.log','proxy_build.log']]
 assert all('Overfull' not in x and 'undefined' not in x and 'LaTeX Warning' not in x for x in logs)
 assert [x.count('Underfull') for x in logs]==[2,2]
 requirements=rows(R/'results/task4_v172_country_review/requirements.csv');statuses={x['id']:x['status'] for x in requirements}
 update={
 'PA-sample':'Unchanged16x10 primary model;ranking table p10',
 'PA-data':'Owned section4.2 compressed1482->976 whitespace tokens with all original citation keys;matrixFigure1 p8;source scope retained',
 'PA-news':'News18-19;unchanged scoped conservative recommendation',
 'PA-references':'References20-24;49 compiled entries',
 'PA-ai-section':'Incomplete AI appendix25-26 after24 main/reference pages',
 'U-country':'Section7 p16/Figure3 p17;frozen auxiliary fourcity cases,20 contrasts,7 sign-identified;unchanged',
 'CI-budget':'24 main/reference pages;2 additional provisional AI pages;1 main-page margin',
 'CI-file':f'{pdf.stat().st_size} bytes;one current owned PDF',
 'CI-font':'12pt body,11pt native heads;unchanged country min9.5pt and matrix10pt at6.5in;small inherited math separately inventoried',
 'CI-headers':'Native summary banner p1;Team # PENDING / Page x of26 onp2-26;empty footers',
 'TEAM-independent-entry':'V173 direct/root normalized text equal;26pages;0overfull/2 inherited reviewed underfull',
 'AI-verification':'FrozenV154 scientific checks;V172 all20 contrasts;V173 exact prose boundary,citation-set andcritical-fact review',
 'U-template-format':'Read-only class preserved;26Letter pages;native heads andempty footers checked',
 'U-matrix-visual':'Figure1 p8;112point/34partial/14unknown;unchanged160cells,Travel burden mixedproxy scope,min10pt at6.5in',
 'U-country-visual':'Figure3 p17;unchanged20differences,7excludezero,4oldscore ranges;min9.5pt/source scope unchanged',
 }
 for x in requirements:
  hits=[]
  # The compressed but preserved source fact has a more direct actual-text locator.
  if x['id']=='U-source-quality':x['passage_markers']=json.dumps(['numerator 340','rate 0.14'])
  for marker in json.loads(x['passage_markers']):
   found=[i for i,p in enumerate(pages,1) if norm(marker).lower() in p.lower()];assert found,(x['id'],marker);hits+=found
  if hits:x['pdf_pages']=','.join(map(str,sorted(set(hits))))
  if x['id'] in update:x['evidence']=update[x['id']]
  if x['id']=='CI-budget':x['scope_or_remaining_action']='One main page remains under retained25-page limit;final integration can change pagination;not submission certification'
  explicit={'PA-news':'18-19','PA-references':'20-24','PA-ai-section':'25-26','U-country':'16-17','U-template-format':'1-26','U-matrix-visual':'7-8','U-country-visual':'16-17'}
  if x['id'] in explicit:x['pdf_pages']=explicit[x['id']]
 requirements.append(dict(id='U-collection-compression',authority='User data-collection chapter and minimal owned edit scope',requirement='Explain genuine collection problems compactly while preserving source meanings',status='reviewed_scoped',pdf_pages='5-7',evidence='Only owned4.2 rewritten;1482->976 whitespace tokens;all original citekeys;critical scope checks and independent review;1mainpage saved',scope_or_remaining_action='Presentation improvement;no new empirical data,model or certainty;all prior data-quality limits remain',passage_markers=json.dumps(['Count city facilities','upper-secondary years 1-3'])))
 requirements[-1]['passage_markers']=json.dumps(['Count city facilities','not complete headcounts'])
 for marker in json.loads(requirements[-1]['passage_markers']):assert any(norm(marker).lower() in p.lower() for p in pages)
 assert len(requirements)==46 and all(x['status']==statuses[x['id']] for x in requirements if x['id'] in statuses)
 pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==14
 table('requirements.csv',requirements)
 xml=E.parse(T/'v173_fonts.xml').getroot();fonts={};counts=Counter();small=[]
 for page in xml.findall('page'):
  for f in page.findall('fontspec'):fonts[f.get('id')]=f.attrib
  for t in page.findall('text'):
   value=''.join(t.itertext()).strip()
   if not value:continue
   f=fonts[t.get('font')];size=int(f['size']);family=re.sub(r'^[A-Z]{6}\+','',f['family']);counts[size,family]+=1
   if size<12:small.append(dict(pdf_page=int(page.get('number')),top=int(t.get('top')),extractor_size=size,font_family=family,text=value))
 table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Extractor glyph sizes are not source nominalfontsize;inherited figure assets unchanged') for k,v in sorted(counts.items())]);table('small_spans.csv',small)
 pixels=read(O/'body_pixel_comparison.json');assert pixels['new_pdf_sha256']==sha(pdf) and pixels['identical_body_pages']==14
 visual=read(O/'visual_review.json');assert visual['all26_pages_layout_reviewed'] and visual['pdf_sha256']==sha(pdf)
 repro=read(O/'reproduction.json');assert repro['all_byte_identical'] and repro['generated_files']==4
 registry=read(R/'design/task4_user_current_review.json');assert registry==read(D/'task4_current_review.json') and registry['version']=='V173' and registry['pdf_sha256']==sha(pdf)
 result=dict(status='pass',version='V173',primary_model='V154 unchanged',total_pages=26,main_and_references_pages=24,main_page_margin=1,news_pages=[18,19],references_pages=[20,24],AI_pages=[25,26],compiled_references=49,matrix_figure_page=8,country_figure_page=17,scientific_files_unchanged=len(science),existing_manuscript_files_unchanged=len(protected)-1,owned_pointer_files_changed=['drafts/task4_current_review.json'],shared_main_ref_class_unchanged=True,unchanged_outside_collection=True,collection_citation_keys_preserved=True,collection_whitespace_tokens_before=1482,collection_whitespace_tokens_after=976,collection_token_reduction_fraction=1-976/1482,body_pixel_identical_pages=14,all26_pages_layout_reviewed=True,direct_root_text_equal=True,native_header_footer_checked=True,overfull_boxes=0,underfull_paragraphs_per_build=2,requirements=46,prior45_statuses_preserved=True,pending_gates_preserved=pending,primary_data_admissions=0,primary_score_width_change=0,MC_rerun=False,font_or_margin_changed=False,submission_ready=False,AI_history_complete=False,server_compile_verified=False,default_main_setting_changed=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
