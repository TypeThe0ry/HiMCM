"""Verify owned template-format review, content boundaries and actual PDF gates."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess,tempfile,unicodedata,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];P=Path('/data/projects/HiMCM-Overleaf');O=R/'results/task4_v164_review';T=Path('/data/scratch');ATT=Path('/root/.codex/attachments/97d9e95b-50df-48d6-b25d-32380bff3894/已粘贴的文本.txt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',unicodedata.normalize('NFKC',s)).split())
def ptext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def table(n,rows):
 with (O/n).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 pdf=P/'drafts/task4_v164_paper.pdf';manifest=read(P/'drafts/task4_v164_manifest.json');fmt=read(P/'drafts/task4_v164_format_reference.json')
 assert manifest['format_reference_sha256']==fmt['source_attachment_sha256'] and sha(P/'mcmthesis.cls')==manifest['shared_class_sha256']
 if ATT.exists():
  assert sha(ATT)==manifest['format_reference_sha256']
  assert 'tcn = 18213' in ATT.read_text() and 'Team \\#18214' in ATT.read_text()
 for n,h in manifest['source_sha256'].items():assert sha(R/n)==h,n
 for folder in ['task4_v161_dublin_scope','task4_v163_helsinki_envelope']:
  s=read(R/'data'/folder/'scope_audit.json')
  for n,h in s['source_sha256'].items():assert sha(R/'data'/folder/n)==h,n
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 guard=O/'protected_files.json'
 if guard.exists():protected=read(guard)['manuscript']
 else:
  names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0');protected={n:sha(P/n) for n in names if n}
 for n,h in protected.items():
  if n not in {'AGENTS.md','drafts/task4_current_review.json'}:assert sha(P/n)==h,n
 original=subprocess.check_output(['git','-C',str(P),'show','39e5a04:AGENTS.md'],text=True)
 assert (P/'AGENTS.md').read_text()==original.replace('(V160; primary science V154)','(primary science V154; current version in the registry)')
 old=(P/'drafts/task4_v160_core.tex').read_text();core=(P/'drafts/task4_v164_core.tex').read_text();a=old.index('For Henri-IV (Paris');z=old.index('\\textbf{Rates require',a)
 expected_suffix=old[z:].replace('\\clearpage\n\\section{Comparing cities within the same country}','\\section{Comparing cities within the same country}')
 assert core[:a]==old[:a] and core[core.index('\\textbf{Rates require',a):]==expected_suffix
 refs=(P/'drafts/task4_v164_references.tex').read_text();prior=(P/'drafts/task4_v154_references.tex').read_text();assert refs.startswith(prior[:prior.index('\\end{thebibliography}')])
 assert set(re.findall(r'\\bibitem\{([^}]+)\}',refs))-set(re.findall(r'\\bibitem\{([^}]+)\}',prior))=={'irelandpayroll','finlandfte'}
 front=(P/'drafts/task4_v164_front.tex').read_text();oldfront=(P/'drafts/task4_v154_front.tex').read_text();assert front[front.index('\\clearpage\n\\tableofcontents'):]==oldfront[oldfront.index('\\clearpage\n\\tableofcontents'):]
 paper=(P/'drafts/task4_v164_paper.tex').read_text();assert '\\documentclass{mcmthesis}' in paper and 'tcn=PENDING' in paper and '\\graphicspath{{./}{drafts/}}' in paper
 text=ptext(pdf);pages=[norm(x) for x in text.split('\f') if x.strip()];assert len(pages)==25
 for marker in ['Problem Chosen','Team Control Number','Summary','Keywords']:assert marker in pages[0],marker
 assert 'Page 1 of' not in pages[0]
 for i,p in enumerate(pages[1:],2):assert re.search(r'Team\s*#\s*PENDING',p) and f'Page {i} of 25' in p,i
 assert norm(text)==norm(ptext(T/'himcm_v164_final_proxy/task4_v164_review_entry.pdf'))
 aux=(T/'himcm_v164_format/task4_v164_paper.aux').read_text()
 for label,page in [('news-start',17),('news-end',18),('main-end',23),('LastPage',25)]:assert int(re.search(r'\\newlabel\{'+label+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))==page
 assert len(re.findall(r'\\bibcite\{',aux))==49
 assert '\\bibcite{irelandpayroll}{48}' in aux and '\\bibcite{finlandfte}{49}' in aux
 ns={'h':'http://www.w3.org/1999/xhtml'}
 bbox=ET.parse(T/'himcm_v164_bbox.html').getroot().findall('.//h:page',ns);assert len(bbox)==25
 for i,page in enumerate(bbox):
  assert float(page.get('width'))==612 and float(page.get('height'))==792
  words=page.findall('.//h:word',ns);assert not [w for w in words if float(w.get('yMin'))>745],i+1
  if i:
   top=[w for w in words if float(w.get('yMin'))<65]
   assert any(w.text=='Team' and 70<float(w.get('xMin'))<74 for w in top)
   assert any(w.text=='Page' and float(w.get('xMin'))>450 for w in top)
 logs=[(O/n).read_text() for n in ['direct_build.log','proxy_build.log']]
 assert all('Overfull' not in x and 'undefined' not in x and 'LaTeX Warning' not in x for x in logs)
 underfull=[len(re.findall('Underfull',x)) for x in logs];assert underfull==[2,2],underfull
 assert 'framework.png' in (O/'shared_main_stdout.txt').read_text()
 rows=list(csv.DictReader((R/'results/task4_v160_review/requirements.csv').open()));base={r['id']:r['status'] for r in rows}
 for row in rows:
  hits=[]
  for marker in json.loads(row['passage_markers']):
   found=[i for i,p in enumerate(pages,1) if norm(marker).lower() in p.lower()];assert found,(row['id'],marker);hits+=found
  if hits:row['pdf_pages']=','.join(map(str,sorted(set(hits))))
  if row['id']=='CI-headers':row.update(evidence='Native mcmthesis summary banner on p1; Team # PENDING and Page x of25 on p2-25; empty footers',scope_or_remaining_action='User format matched; real registered control number remains unverified; native summary has no running page number')
  if row['id']=='CI-font':row.update(evidence='12pt mcmthesis Palatino body; template running heads11pt and smaller math scripts listed separately',scope_or_remaining_action='Not an all-glyph size certificate; user template keeps native header sizing, no official exception inferred')
  if row['id']=='TEAM-independent-entry':row['evidence']='V164 native-format direct and root-proxy builds;25 pages; normalized text equal; no overfull boxes, two reviewed underfull paragraphs'
  if row['id']=='AI-verification':row['evidence']='V154 scientific audits; V158/V162 historical gap diagnostics; V161/V163 collection-case audits; V164 content/format verification'
 rows.append(dict(id='U-template-format',authority='User pasted mcmthesis format, current turn',requirement='Use native summary, Team # / Page x of y heads and empty footers only in owned review',status='technical_pass',pdf_pages='1-25',evidence='Existing shared class SHA preserved;25 letter pages; header/footer bbox checks; visual review',scope_or_remaining_action='No teammate main/ref/class edited, default online main unchanged, conflicting sample IDs not treated as registered identity',passage_markers='[]'))
 assert all(r['status']==base[r['id']] for r in rows if r['id'] in base)
 pending=[r['id'] for r in rows if r['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==14
 table('requirements.csv',rows)
 with tempfile.TemporaryDirectory(dir='/data/scratch',prefix='himcm-v164-font-') as td:
  prefix=Path(td)/'font';subprocess.run(['pdftohtml','-xml','-i','-zoom','1','-fontfullname',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  xml=ET.parse(prefix.with_suffix('.xml')).getroot();fonts={};seen=Counter();small=[]
  for page in xml.findall('page'):
   for f in page.findall('fontspec'):fonts[f.get('id')]=f.attrib
   for t in page.findall('text'):
    val=''.join(t.itertext()).strip()
    if not val:continue
    f=fonts[t.get('font')];size=int(f['size']);family=re.sub(r'^[A-Z]{6}\+','',f['family']);seen[size,family]+=1
    if size<12:small.append(dict(pdf_page=int(page.get('number')),top=int(t.get('top')),rounded_size=size,font_family=family,text=val,role='template_header' if int(t.get('top'))<65 and int(page.get('number'))>1 else 'math_script'))
 assert all(x['rounded_size']==11 for x in small if x['role']=='template_header')
 assert all(x['rounded_size']==8 for x in small if x['role']=='math_script')
 table('font_inventory.csv',[dict(rounded_size=k[0],font_family=k[1],text_spans=v) for k,v in sorted(seen.items())]);table('small_spans.csv',small)
 registry=read(R/'design/task4_user_current_review.json');assert registry==read(P/'drafts/task4_current_review.json') and registry['version']=='V164' and registry['pdf_sha256']==sha(pdf)
 result=dict(status='pass',version='V164',primary_model='V154 unchanged',total_pages=25,main_and_references_pages=23,news_pages=[17,18],AI_pages=[24,25],compiled_references=49,paper_format='Existing mcmthesis; Letter612x792pt;1in margins;Palatino;native summary',normal_running_head='Team # PENDING | Page x of25',footers_empty=True,summary_running_head_absent_by_template=True,shared_main_ref_class_unchanged=True,scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(protected)-2,owned_pointer_files_changed=['AGENTS.md','drafts/task4_current_review.json'],all25_pages_visually_reviewed=True,full_size_visual_pages=[2,16,25],direct_root_text_equal=True,overfull_boxes=0,underfull_paragraphs_per_build=2,underfull_visually_reviewed=True,requirements=len(rows),status_counts=dict(Counter(x['status'] for x in rows)),prior41_statuses_preserved=True,pending_gates_preserved=pending,actual_control_number='PENDING; pasted sample IDs18213/18214 conflict',template_header_small_spans=sum(x['role']=='template_header' for x in small),math_script_small_spans=sum(x['role']=='math_script' for x in small),submission_ready=False,AI_history_complete=False,server_compile_verified=False,default_main_setting_changed=False,primary_data_admissions=0,primary_score_width_change=0,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),format_reference_sha256=fmt['source_attachment_sha256'],format_reference_original_available=ATT.exists(),shared_class_sha256=sha(P/'mcmthesis.cls'),verifier_sha256=sha(Path(__file__)))
 (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':protected},indent=2)+'\n');(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
