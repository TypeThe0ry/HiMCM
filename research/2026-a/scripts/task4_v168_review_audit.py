"""Verify owned matrix integration, travel scope, native format and current delivery facts."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess,tempfile,unicodedata,zlib
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v168_review';T=Path('/data/scratch')
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',s)).split())
def text(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def table(n,rows):
 with (O/n).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 protected=read(O/'protected_files.json')['manuscript']
 for n,h in protected.items():
  if n!='drafts/task4_current_review.json':assert sha(P/n)==h,n
 manifest=read(P/'drafts/task4_v168_manifest.json')
 assert sha(P/'drafts/task4_v166_core.tex')==manifest['base_core_sha256']
 assert sha(P/'mcmthesis.cls')==manifest['shared_class_sha256']
 old=(P/'drafts/task4_v166_core.tex').read_text();new=(P/'drafts/task4_v168_core.tex').read_text()
 marker='The current 160 cells comprise 112 point values, 34 partial intervals and'
 expected=old.replace(marker,'Figure~\\ref{fig:identification-matrix} locates the remaining uncertainty.\n'+marker).replace('\\section{Establishing the baseline evaluation model}','\\input{task4_v168_evidence_figure.tex}\n\n\\section{Establishing the baseline evaluation model}')
 assert new==expected
 snippet=(P/'drafts/task4_v167_evidence_assets/figure.tex').read_text().replace('task4_v167_evidence_assets/identification_matrix.pdf','task4_v168_evidence_assets/identification_matrix.pdf').replace('confidence intervals. Cities follow','confidence intervals. Travel entries retain school-travel and general-commute proxy scopes. Cities follow').replace('% Optional owned figure; not input by the current V166 review.','% Owned identification figure integrated in V168.')
 assert (P/'drafts/task4_v168_evidence_figure.tex').read_text()==snippet
 assert '\\includegraphics[width=\\linewidth]' in snippet
 paper=(P/'drafts/task4_v168_paper.tex').read_text()
 assert paper==(P/'drafts/task4_v166_paper.tex').read_text().replace('% V166 owned review;','% V168 owned review;').replace('task4_v166_core.tex','task4_v168_core.tex')
 asset=P/'drafts/task4_v168_evidence_assets';fm=read(asset/'figure_manifest.json')
 assert sha(asset/'identification_matrix.pdf')==manifest['figure_pdf_sha256']==fm['output_sha256']['pdf']
 assert sha(asset/'figure_manifest.json')==manifest['figure_source_manifest_sha256']
 for ext,h in fm['output_sha256'].items():assert sha(asset/f'identification_matrix.{ext}')==h
 rows=list(csv.DictReader((asset/'matrix.csv').open()));prior=list(csv.DictReader((R/'results/task4_v167_evidence/matrix.csv').open()))
 assert len(rows)==len(prior)==160
 for row,base in zip(rows,prior):
  assert all(row[k]==base[k] for k in row if k!='plot_label')
  assert row['plot_label']==('Travel burden' if row['indicator']=='travel' else base['plot_label'])
 assert Counter(x['state'] for x in rows)=={'point':112,'partial':34,'unknown':14}
 svg=ET.parse(asset/'identification_matrix.svg').getroot()
 labels=[''.join(t.itertext()) for t in svg.findall('.//{http://www.w3.org/2000/svg}text')]
 assert 'Travel burden' in labels and 'School trip' not in labels
 sizes=[];raw=(asset/'identification_matrix.pdf').read_bytes()
 for stream in re.findall(rb'stream\r?\n(.*?)\r?\nendstream',raw,re.S):
  try:decoded=zlib.decompress(stream)
  except zlib.error:continue
  sizes.extend(float(v) for v in re.findall(rb'/F\d+\s+([\d.]+)\s+Tf',decoded))
 assert set(sizes)=={10,12} and fm['figure_width_inches']==fm['intended_insertion_width_inches']==6.5
 pdf=P/'drafts/task4_v168_paper.pdf';txt=text(pdf);pages=[norm(p) for p in txt.split('\f') if p.strip()]
 assert len(pages)==26 and norm(txt)==norm(text(T/'himcm_v168_proxy/task4_v168_review_entry.pdf'))
 assert all(x in pages[0] for x in ['Problem Chosen','Team Control Number','Summary','Keywords']) and 'Page 1 of' not in pages[0]
 for i,page in enumerate(pages[1:],2):assert re.search(r'Team\s*#\s*PENDING',page) and f'Page {i} of 26' in page,i
 assert all(x in pages[8] for x in ['Figure 1:','Identification ranges in the retained','general-commute proxy scopes'])
 assert 'Figure 1 locates the remaining uncertainty' in pages[7]
 assert 'Figure 2:' in pages[11]
 aux=(T/'himcm_v168_build/task4_v168_paper.aux').read_text()
 for label,page in [('fig:identification-matrix',9),('news-start',18),('news-end',19),('main-end',24),('LastPage',26)]:assert int(re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux)[1])==page
 assert len(re.findall(r'\\bibcite\{',aux))==49
 bbox=ET.parse(T/'himcm_v168_bbox.html').getroot().findall('.//{http://www.w3.org/1999/xhtml}page');assert len(bbox)==26
 for i,page in enumerate(bbox):
  assert float(page.get('width'))==612 and float(page.get('height'))==792
  words=page.findall('.//{http://www.w3.org/1999/xhtml}word');assert not [w for w in words if float(w.get('yMin'))>745]
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]
   assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
   assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
 logs=[(O/n).read_text() for n in ['direct_build.log','proxy_build.log']]
 assert all('Overfull' not in x and 'undefined' not in x and 'LaTeX Warning' not in x for x in logs)
 assert [x.count('Underfull') for x in logs]==[2,2]
 prior_rows=list(csv.DictReader((R/'results/task4_v166_review/requirements.csv').open()));statuses={r['id']:r['status'] for r in prior_rows}
 updates={
 'PA-sample':'Unchanged16x10 factory; primary ranking table page11',
 'PA-data':'Data section,source cases,49references and160-cell matrix Figure1,p9;22supplements retained',
 'PA-news':'News occupies pages18-19 and explains evidence ranges and common scoring yardsticks',
 'PA-references':'References occupy pages20-24;49compiled entries',
 'PA-ai-section':'Incomplete AI appendix starts page25 after24 main/reference pages',
 'CI-budget':'24 main/reference pages;two additional provisional AI pages',
 'CI-file':f'{pdf.stat().st_size} bytes;one current owned PDF',
 'CI-font':'12pt body;11pt template heads;matrix source text10pt atfull6.5in;8pt math scripts separately listed',
 'CI-headers':'Native summary banner p1;Team # PENDING / Page x of26 onp2-26;empty footers',
 'TEAM-independent-entry':'V168 direct/root builds;26pages;normalized fulltext equal;0overfull/2reviewed underfull',
 'AI-verification':'V154 scientific audits;V162 frozen certificate;V166 witness checks;V167/V168160-cell source/label/integration checks',
 'U-template-format':'Read-only shared class preserved;26Letter pages;native heads and empty footers checked',
 }
 for row in prior_rows:
  hits=[]
  for marker in json.loads(row['passage_markers']):
   found=[i for i,p in enumerate(pages,1) if norm(marker).lower() in p.lower()];assert found,(row['id'],marker);hits+=found
  if hits:row['pdf_pages']=','.join(map(str,sorted(set(hits))))
  if row['id'] in updates:row['evidence']=updates[row['id']]
  if row['id']=='CI-budget':row['scope_or_remaining_action']='One main page remains under retained25-page limit;not a submission-readiness certificate'
  if row['id']=='U-template-format':row['pdf_pages']='1-26'
  if row['id']=='PA-news':row['pdf_pages']='18-19'
  if row['id']=='PA-references':row['pdf_pages']='20-24'
  if row['id']=='PA-ai-section':row['pdf_pages']='25-26'
 prior_rows.append(dict(id='U-matrix-visual',authority='User M-city,N-indicator and genuine-data tasks',requirement='Locate all160 retained ranges and preserve the mixed travel source scope',status='reviewed_scoped',pdf_pages='8-9',evidence='Figure1,p9;112point/34partial/14unknown;8PTR unknown;all160values unchanged;Travel burden label and commute-proxy caption;10pt source text atfull6.5in',scope_or_remaining_action='Point assumptions are not independent provenance certification;identification bounds are not confidence intervals or a ranking',passage_markers=json.dumps(['Travel entries retain','general-commute proxy scopes'])))
 assert len(prior_rows)==44 and all(r['status']==statuses[r['id']] for r in prior_rows if r['id'] in statuses)
 pending=[r['id'] for r in prior_rows if r['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==14
 table('requirements.csv',prior_rows)
 with tempfile.TemporaryDirectory(dir=T,prefix='himcm-v168-font-') as td:
  pref=Path(td)/'font';subprocess.run(['pdftohtml','-xml','-i','-zoom','1','-fontfullname',str(pdf),str(pref)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  xml=ET.parse(pref.with_suffix('.xml')).getroot();fonts={};counts=Counter();small=[]
  for page in xml.findall('page'):
   for f in page.findall('fontspec'):fonts[f.get('id')]=f.attrib
   for t in page.findall('text'):
    value=''.join(t.itertext()).strip()
    if not value:continue
    f=fonts[t.get('font')];size=int(f['size']);family=re.sub(r'^[A-Z]{6}\+','',f['family']);counts[size,family]+=1
    if size<12:small.append(dict(pdf_page=int(page.get('number')),top=int(t.get('top')),extractor_size=size,font_family=family,text=value))
 table('font_inventory.csv',[dict(extractor_size=k[0],font_family=k[1],text_spans=v,interpretation='Type3 matrix bbox sizes are not nominal sizes;matrix sourceTf10/12pt atscale1') for k,v in sorted(counts.items())]);table('small_spans.csv',small)
 visual=read(O/'visual_review.json');assert visual['all26_pages_reviewed'] and visual['pdf_sha256']==sha(pdf)
 registry=read(R/'design/task4_user_current_review.json');assert registry==read(P/'drafts/task4_current_review.json') and registry['version']=='V168' and registry['pdf_sha256']==sha(pdf)
 result=dict(status='pass',version='V168',primary_model='V154 unchanged',total_pages=26,main_and_references_pages=24,news_pages=[18,19],references_pages=[20,24],AI_pages=[25,26],compiled_references=49,new_matrix_figure_page=9,
  scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(protected)-1,owned_pointer_files_changed=['drafts/task4_current_review.json'],shared_main_ref_class_unchanged=True,
  changed_prose='One owned figure-reference sentence,figure input and caption source-scope clarification',all26_pages_visually_reviewed=True,direct_root_text_equal=True,native_header_footer_bbox_checked=True,
  overfull_boxes=0,underfull_paragraphs_per_build=2,requirements=44,prior43_statuses_preserved=True,pending_gates_preserved=pending,all160_figure_values_unchanged=True,travel_label='Travel burden;retained commute/stage proxies',
  matrix_nominal_min_font_pt=10,matrix_insertion_width_inches=6.5,figure_integrated=True,primary_data_admissions=0,primary_score_width_change=0,submission_ready=False,AI_history_complete=False,server_compile_verified=False,default_main_setting_changed=False,
  pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),verifier_sha256=sha(Path(__file__)))
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
