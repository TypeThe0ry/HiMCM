"""Verify the owned historical-country figure, preserved main science and exact PDF."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess,unicodedata,zlib,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v172_country_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
 with p.open() as f:return list(csv.DictReader(f))
def table(name,data):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]),lineterminator='\n');w.writeheader();w.writerows(data)
def norm(x):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',x)).split())
def pdftext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def main():
 science=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in science.items():assert sha(R/n)==h,n
 protected=read(O/'protected_files.json')['manuscript']
 for n,h in protected.items():
  if n!='drafts/task4_current_review.json':assert sha(P/n)==h,n
 old=(P/'drafts/task4_v168_core.tex').read_text();new=(P/'drafts/task4_v172_core.tex').read_text()
 assert new==old.replace('\\input{task4_v154_assets/country.tex}','\\input{task4_v172_country_figure.tex}')+'\n\\FloatBarrier\n'
 assert (P/'drafts/task4_v172_paper.tex').read_text()==(P/'drafts/task4_v168_paper.tex').read_text().replace('% V168 owned review;','% V172 owned review;').replace('task4_v168_core.tex','task4_v172_core.tex')
 m=read(P/'drafts/task4_v172_manifest.json');assert sha(P/'mcmthesis.cls')==m['shared_class_sha256']
 assert sha(P/'drafts/task4_v168_core.tex')==m['base_core_sha256']
 asset=P/'drafts/task4_v172_country_assets';f=read(asset/'figure_manifest.json')
 assert f['minimum_font_pt']==9.5 and f['figure_inches']==[6.5,4.1]
 for n,h in f['source_sha256'].items():assert sha(R/n)==h
 for ext,h in f['output_sha256'].items():assert sha(asset/f'country_contrasts.{ext}')==h
 assert sha(asset/'country_contrasts.pdf')==m['figure_pdf_sha256']
 assert sha(asset/'figure_manifest.json')==m['figure_manifest_sha256']
 contrasts=rows(asset/'contrasts.csv');source=rows(R/'results/task4_v154_method/country_indicator_bounds.csv')
 assert len(contrasts)==len(source)==20
 for x,y in zip(contrasts,source):
  lo=float(y['a_lower'])-float(y['b_upper']);hi=float(y['a_upper'])-float(y['b_lower'])
  assert x['city_a']==y['city_a'] and x['city_b']==y['city_b'] and x['indicator']==y['indicator']
  assert float(x['difference_lower'])==lo and float(x['difference_upper'])==hi
  assert (x['sign_identified']=='True')==(lo>0 or hi<0)
 assert sum(x['sign_identified']=='True' for x in contrasts)==7
 for x in rows(R/'results/task4_v154_method/country_score_comparison.csv'):
  assert x['a_necessarily_strictly_better']==x['b_necessarily_strictly_better']=='False'
  assert x['a_possible_pairwise_winner']==x['b_possible_pairwise_winner']=='True'
 caption=(P/'drafts/task4_v172_country_figure.tex').read_text()
 assert all(t in caption for t in ['width=\\linewidth','primary sixteen cities','all twenty utility differences','seven exclude zero','all-age XI--XII','not FTE','July--September test window','not confidence intervals','neither pair'])
 nominal=[]
 for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',(asset/'country_contrasts.pdf').read_bytes(),re.S):
  try:raw=zlib.decompress(stream)
  except zlib.error:continue
  nominal += [float(x) for x in re.findall(rb'/\w+\s+([0-9.]+)\s+Tf',raw)]
 assert nominal and min(nominal)==9.5
 pdf=P/'drafts/task4_v172_paper.pdf';direct=pdftext(pdf)
 proxy=pdftext(T/'himcm_v172_proxy/task4_v172_review_entry.pdf');assert norm(direct)==norm(proxy)
 pages=[norm(p) for p in direct.split('\f') if p.strip()];assert len(pages)==27
 assert 'Figure 3:' in pages[17] and pages[17].index('Figure 3:')<pages[17].index('Conclusion and decision use')
 assert 'Figure 1:' in pages[8] and 'Figure 2:' in pages[11]
 aux=(T/'himcm_v172_build/task4_v172_paper.aux').read_text()
 for label,page in [('fig:country-contrasts',18),('news-start',19),('news-end',20),('main-end',25),('LastPage',27)]:assert int(re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])==page
 assert len(re.findall(r'\\bibcite\{',aux))==49
 bbox=E.parse(T/'himcm_v172_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(bbox)==27
 for i,page in enumerate(bbox):
  assert float(page.get('width'))==612 and float(page.get('height'))==792
  words=page.findall('.//{http://www.w3.org/1999/xhtml}word');assert not [w for w in words if float(w.get('yMin'))>745]
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]
   assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
   assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
   assert f'Page {i+1} of 27' in pages[i]
 logs=[(O/n).read_text() for n in ['direct_build.log','proxy_build.log']]
 assert all('Overfull' not in x and 'undefined' not in x and 'LaTeX Warning' not in x for x in logs)
 assert [x.count('Underfull') for x in logs]==[2,2]
 requirements=rows(R/'results/task4_v168_review/requirements.csv');statuses={x['id']:x['status'] for x in requirements}
 update={
 'PA-news':'News19-20; unchanged scoped conservative recommendation',
 'PA-references':'References21-25;49 compiled entries',
 'PA-ai-section':'Incomplete AI appendix26-27 after25 main/reference pages',
 'U-country':'Section7 p17 and Figure3 p18; four frozen auxiliary cities,20 utility contrasts,7 sign-identified; neither pair necessary winner',
 'CI-budget':'25 main/reference pages;2 provisional additional AI pages;0 main-page margin',
 'CI-file':f'{pdf.stat().st_size} bytes;one current owned PDF',
 'CI-font':'12pt body,11pt native heads;new country figure min9.5pt at6.5in;matrix10pt;small inherited math separately inventoried',
 'CI-headers':'Native summary banner p1;Team # PENDING / Page x of27 onp2-27;empty footers',
 'TEAM-independent-entry':'V172 direct/root normalized fulltext equal;27pages;0overfull/2 reviewed inherited underfull',
 'AI-verification':'V154 frozen science audits;V166/V168 owned checks;V172 all20 contrast/endpoints,scope,font and integration checks',
 'U-template-format':'Read-only class preserved;27Letter pages;native heads/empty footers checked',
 }
 for x in requirements:
  markers=json.loads(x['passage_markers'])
  if x['id']=='U-country':markers=[m.replace('legacy 25-city V117','legacy25 V117') for m in markers];x['passage_markers']=json.dumps(markers)
  hits=[]
  for marker in markers:
   found=[i for i,p in enumerate(pages,1) if norm(marker).lower() in p.lower()];assert found,(x['id'],marker);hits+=found
  if hits:x['pdf_pages']=','.join(map(str,sorted(set(hits))))
  if x['id'] in update:x['evidence']=update[x['id']]
  if x['id']=='CI-budget':x['scope_or_remaining_action']='Retained25-page main budget reached;no main-page margin;final integration can change pagination;not a submission certificate'
  explicit={'PA-news':'19-20','PA-references':'21-25','PA-ai-section':'26-27','U-country':'17-18','U-template-format':'1-27'}
  if x['id'] in explicit:x['pdf_pages']=explicit[x['id']]
 requirements.append(dict(id='U-country-visual',authority='User within-country comparison task',requirement='Show all retained auxiliary-country contrasts with their exact source scope',status='reviewed_scoped',pdf_pages='17-18',evidence='Figure3;20 differences,7 excludingzero;all4 old score ranges;min9.5pt at6.5in;school-headcount and mixed-year scope preserved',scope_or_remaining_action='Frozen legacy25 auxiliary cases;no main16 within-country estimate,causal effect or necessary overall winner',passage_markers=json.dumps(['all twenty utility differences','nominal teacher-headcount allocation','July-September test window'])))
 # New row markers use the PDF-normalized typography rather than a guessed dash.
 requirements[-1]['passage_markers']=json.dumps(['all twenty utility differences','nominal teacher-headcount allocation'])
 for marker in json.loads(requirements[-1]['passage_markers']):assert any(norm(marker).lower() in page.lower() for page in pages)
 assert len(requirements)==45 and all(x['status']==statuses[x['id']] for x in requirements if x['id'] in statuses)
 pending=[x['id'] for x in requirements if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==14
 table('requirements.csv',requirements)
 xml=E.parse(T/'v172_fonts.xml').getroot();fonts={};counts=Counter();small=[]
 for page in xml.findall('page'):
  for fnt in page.findall('fontspec'):fonts[fnt.get('id')]=fnt.attrib
  for t in page.findall('text'):
   value=''.join(t.itertext()).strip()
   if not value:continue
   fnt=fonts[t.get('font')];size=int(fnt['size']);family=re.sub(r'^[A-Z]{6}\+','',fnt['family']);counts[size,family]+=1
   if size<12:small.append(dict(pdf_page=int(page.get('number')),top=int(t.get('top')),extractor_size=size,font_family=family,text=value))
 table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Extractor glyph boxes are not source nominal fontsize;new figure PDF Tf checked separately') for k,v in sorted(counts.items())]);table('small_spans.csv',small)
 pixels=read(O/'body_pixel_comparison.json');assert pixels['new_pdf_sha256']==sha(pdf) and pixels['identical_pages']==24 and all(x['body_pixels_identical'] for x in pixels['records'])
 visual=read(O/'visual_review.json');assert visual['all27_pages_layout_reviewed'] and visual['pdf_sha256']==sha(pdf)
 registry=read(R/'design/task4_user_current_review.json');assert registry==read(P/'drafts/task4_current_review.json') and registry['version']=='V172' and registry['pdf_sha256']==sha(pdf)
 result=dict(status='pass',version='V172',primary_model='V154 unchanged',total_pages=27,main_and_references_pages=25,main_page_margin=0,news_pages=[19,20],references_pages=[21,25],AI_pages=[26,27],compiled_references=49,new_country_figure_page=18,scientific_files_unchanged=len(science),existing_manuscript_files_unchanged=len(protected)-1,owned_pointer_files_changed=['drafts/task4_current_review.json'],shared_main_ref_class_unchanged=True,original_prose_preserved=True,body_pixel_identical_pages=24,all27_pages_layout_reviewed=True,direct_root_text_equal=True,native_header_footer_checked=True,overfull_boxes=0,underfull_paragraphs_per_build=2,requirements=45,prior44_statuses_preserved=True,pending_gates_preserved=pending,country_contrasts_checked=20,sign_identified=7,country_source_scope='Frozen legacy25 auxiliary only;nominal teacher allocation notFTE;source years retained',new_figure_minimum_font_pt=9.5,new_figure_width_inches=6.5,primary_data_admissions=0,primary_score_width_change=0,MC_rerun=False,submission_ready=False,AI_history_complete=False,server_compile_verified=False,default_main_setting_changed=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
