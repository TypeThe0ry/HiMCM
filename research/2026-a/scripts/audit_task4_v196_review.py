"""Audit the one-word owned bibliography correction against frozen V193."""
import csv,hashlib,json,re,subprocess,tempfile
from pathlib import Path
from task4_v5_model import ROOT
from task4_v193_delivery import hit
P=ROOT.parents[2]/'HiMCM-Overleaf';O=ROOT/'results/task4_v196_review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pages(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True).split('\f')[:-1]
def main():
 snap=json.loads((ROOT/'design/task4_user_v192_snapshot.json').read_text())['source_sha256']
 for n,h in snap.items():assert sha(ROOT/n)==h,n
 baseline=json.loads((ROOT/'results/task4_v196_references/verification.json').read_text())
 for n,h in baseline['source_sha256'].items():assert sha(P/n)==h,n
 old=(P/'drafts/task4_v193_references.tex').read_text();new=(P/'drafts/task4_v196_references.tex').read_text()
 assert old.replace('updated 9 October 2025.','updated 9 September 2025.')==new
 previous=(P/'drafts/task4_v193_paper.tex').read_text()
 assert previous.replace('% V193 owned review;','% V196 owned review;').replace('task4_v193_references.tex','task4_v196_references.tex')==(P/'drafts/task4_v196_paper.tex').read_text()
 pdf=P/'drafts/task4_v196_paper.pdf';oldpdf=P/'drafts/task4_v193_paper.pdf';a,b=pages(oldpdf),pages(pdf)
 assert len(a)==len(b)==27
 changed=[i+1 for i,(x,y) in enumerate(zip(a,b)) if x!=y];assert changed==[24]
 assert re.sub(r'\s+','',a[23].replace('9 October 2025','9 September 2025'))==re.sub(r'\s+','',b[23])
 proxy=Path('/data/scratch/himcm_v196_proxy/task4_v196_review_entry.pdf');assert pages(proxy)==b
 pixel_identical=[]
 with tempfile.TemporaryDirectory(prefix='himcm-v196-pixels-',dir='/data/scratch') as tmp:
  q=Path(tmp)
  for label,source in [('old',oldpdf),('new',pdf),('proxy',proxy)]:
   subprocess.run(['pdftoppm','-r','72','-gray',str(source),str(q/label)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  for i in range(1,28):
   x=(q/f'old-{i:02}.pgm').read_bytes();y=(q/f'new-{i:02}.pgm').read_bytes()
   assert y==(q/f'proxy-{i:02}.pgm').read_bytes()
   if x==y:pixel_identical.append(i)
 assert pixel_identical==[i for i in range(1,28) if i!=24]
 aux=Path('/data/scratch/himcm_v196_build/task4_v196_paper.aux').read_text()
 assert len(re.findall(r'\\bibcite\{',aux))==56
 for name in ['himcm_v196_build/task4_v196_paper.log','himcm_v196_proxy/task4_v196_review_entry.log']:
  log=(Path('/data/scratch/himcm_v196_build').parent/name).read_text();assert 'Overfull' not in log and log.count('Underfull')==2
 oldrows=list(csv.DictReader((ROOT/'results/task4_v193_review/requirements.csv').open()))
 anchors=list(csv.DictReader((ROOT/'results/task4_v193_review/anchor_hits.csv').open()))
 for row in anchors:
  lo,hi=int(row['allowed_page_start']),int(row['allowed_page_end'])
  found=[i for i in range(lo,hi+1) if hit(row['marker'],b[i-1],row['match_mode']=='line')]
  assert found==list(map(int,row['hit_pages'].split(',')))
 rows=[]
 for row in oldrows:
  row=dict(row)
  row['evidence']=row['evidence'].replace('V193','V196')
  if row['id']=='TEAM-shared-build':row['evidence']='FreshV196read-onlysharedmainbuildfailsatmissingframework.png;oldteamsourcespreserved;shared_main.log'
  if row['id']=='CI-file':row['evidence']=f'{pdf.stat().st_size}bytes;oneV196ownedPDF'
  if row['id']=='PA-references':row['evidence']='56references;allkeys/URLsretained;MilanprintedSeptemberdatecorrectedfromoriginalPDF'
  rows.append(row)
 assert len(rows)==47 and sum(r['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'} for r in rows)==13
 for name,data in [('requirements.csv',rows),('anchor_hits.csv',anchors)]:
  with (O/name).open('w') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
 log=Path('/data/scratch/himcm_v196_shared/main.log').read_text();assert 'framework.png' in log
 (O/'shared_main.log').write_text(log)
 out=dict(status='pass',version='V196',primary_model='V192',previous_review='V193',scope='Only printed Milan tariff update month corrected. Prior science/prose/assets and team content preserved; not full-team final submission.',pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,total_pages=27,main_and_references_pages=25,compiled_references=56,changed_text_pages=changed,pixel_identical_old_pages=pixel_identical,direct_proxy_all27text_and72dpi_pixels_equal=True,overfull=0,underfull_per_entry=2,scoped_anchors=58,requirements=47,pending_count=13,submission_ready=False,server_compile_verified=False,immutable_science_bindings=len(snap),display_control_number='18213 provisional',actual_registered_number_verified=False,initial_direct_build_failure='Classsearchpathomitted;fixedusingexisting-Zsearch-path=..command;failurelogretained',source_sha256={str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),ROOT/'data/task4_v196_milanpool/verification.json',ROOT/'results/task4_v193_review/verification.json',ROOT/'results/task4_v196_references/verification.json']},paper_sha256={str(p.relative_to(P)):sha(p) for p in [pdf,P/'drafts/task4_v196_references.tex',P/'drafts/task4_v196_paper.tex',P/'drafts/build_task4_v196.py',P/'task4_v196_review_entry.tex',P/'main.tex',P/'ref.bib',P/'mcmthesis.cls']})
 (O/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['source_sha256','paper_sha256']},indent=2))
if __name__=='__main__':main()
