"""Bind the current owned review to frozen science and artifact-specific gates."""
from pathlib import Path
from collections import Counter
import csv,hashlib,json,re,subprocess,tempfile,xml.etree.ElementTree as ET
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[1];P=Path('/data/projects/HiMCM-Overleaf');O=R/'results/task4_v160_review';T=Path('/data/scratch')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',s).split())
def pdftext(p):return subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
def table(name,rows):
 with (O/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def main():
 pdf=P/'drafts/task4_v160_paper.pdf';s=read(R/'results/task4_v158_joint_gap/summary.json');oldready=read(R/'results/task4_v156_readiness/summary.json')
 for name,h in s['source_sha256'].items():assert sha(R/name)==h,name
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for name,h in snapshot.items():assert sha(R/name)==h,name
 guard=O/'protected_files.json'
 if guard.exists():protected=read(guard)['manuscript']
 else:
  names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0');protected={n:sha(P/n) for n in names if n}
 for n,h in protected.items():
  if n!='AGENTS.md':assert sha(P/n)==h,n
 original_agents=subprocess.check_output(['git','-C',str(P),'show','3fc53cf:AGENTS.md'],text=True)
 expected_agents=original_agents.replace('synchronized with the complete independent review `drafts/task4_v154_paper.tex/.pdf`','with the current complete independent review registered in `drafts/task4_current_review.json` (V160; primary science V154)').replace('use the V154 entry for the current review','use the current review registry for the independent manuscript; V154 is the frozen preceding review')
 assert (P/'AGENTS.md').read_text()==expected_agents
 core=(P/'drafts/task4_v160_core.tex').read_text();oldcore=(P/'drafts/task4_v159_core.tex').read_text()
 a=oldcore.index('Citywide facilities per resident');z=oldcore.index('\\clearpage',a)
 assert core[:a]==oldcore[:a] and core[core.index('\\clearpage',a):]==oldcore[z:]
 for preserved in ['\\EquityCase','\\AgeCase','\\input{task4_v154_assets/age_joint.tex}']:assert core.count(preserved)==oldcore.count(preserved)==1
 joint=next(x for x in s['rows'] if x['alpha']==.2)
 for k in ['sharp_joint_lower','witness_mean','witness_lower_tail']:assert f'{joint[k]:.6f}' in core
 for marker in ['W=499950','N_{\\max}=681503','unknown utilities in $[0,1]$','optional membership uncertain']:assert marker in core,marker
 text=pdftext(pdf);pages=[norm(x) for x in text.split('\f') if x.strip()];assert len(pages)==24
 proxy=T/'himcm_v160_proxy/task4_v160_review_entry.pdf';assert norm(text)==norm(pdftext(proxy))
 changed=[]
 for i in range(1,25):
  a=Image.open(T/f'himcm_v159_render/final-{i:02}.png').convert('RGB');b=Image.open(T/f'himcm_v160_render/page-{i:02}.png').convert('RGB')
  if a.size!=b.size or ImageChops.difference(a,b).getbbox():changed.append(i)
 assert changed==[14],changed
 oldpages=[norm(x) for x in pdftext(P/'drafts/task4_v159_paper.pdf').split('\f') if x.strip()]
 for i in range(24):
  if i!=13:assert oldpages[i]==pages[i],i+1
 for path in [O/'direct_build.log',O/'proxy_build.log']:assert not re.search('Warning|Overfull|Underfull|undefined',path.read_text())
 aux=(T/'himcm_v160_build/task4_v160_paper.aux').read_text()
 for name,page in [('news-start',16),('news-end',17),('main-end',22),('LastPage',24)]:assert int(re.search(r'\\newlabel\{'+name+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))==page
 assert len(re.findall(r'\\bibcite\{',aux))==47
 for i,p in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 24',p),i
 rows=list(csv.DictReader((R/'results/task4_v156_readiness/requirements.csv').open()))
 for row in rows:
  hits=[]
  for marker in json.loads(row['passage_markers']):
   found=[i for i,p in enumerate(pages,1) if norm(marker).lower() in p.lower()];assert found,(row['id'],marker);hits.extend(found)
  if hits:row['pdf_pages']=','.join(map(str,sorted(set(hits))))
  if row['id']=='U-fairness':row['evidence']='Shanghai district resources plus Istanbul2012 joint sharp lower-tail gap with shared completion'
  if row['id']=='CI-font':row['scope_or_remaining_action']='V160 actual PDF font inventory and rendered review; mathematical scripts remain separately disclosed'
  if row['id']=='TEAM-independent-entry':row['evidence']='V160 direct and root-proxy builds:24 pages, zero warnings, normalized text identical'
  if row['id']=='AI-verification':row['evidence']='Frozen V154 scientific audits and 22-supplement chain; V158 joint bound and V160 manuscript audit'
 rows.append(dict(id='U-fairness-joint',authority='User fairness follow-up / retained historical evidence',requirement='Joint gap states weights, completion set and finite attaining witness',status='reviewed_scoped',pdf_pages='14',evidence='W499950 / Nmax681503; unknown utilities[0,1]; optional membership; sharp gap0.226686,45-minute witness',scope_or_remaining_action='Istanbul2012 retained aggregate set from portal projection, not current facility use or population CI',passage_markers=json.dumps(['0.226686','499950','681503','45 minutes'])))
 table('requirements.csv',rows)
 statuses={r['id']:r['status'] for r in rows};oldrows=list(csv.DictReader((R/'results/task4_v156_readiness/requirements.csv').open()))
 assert all(statuses[x['id']]==x['status'] for x in oldrows)
 pending=[x['id'] for x in oldrows if x['status'] in {'partial','unverified','awaiting_team','not_ready','not_performed'}];assert len(pending)==14
 with tempfile.TemporaryDirectory(dir='/data/scratch',prefix='himcm-v160-font-') as tmp:
  prefix=Path(tmp)/'font';subprocess.run(['pdftohtml','-xml','-i','-zoom','1','-fontfullname',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  xml=ET.parse(prefix.with_suffix('.xml')).getroot();fonts={};seen=Counter();small=[]
  for page in xml.findall('page'):
   for font in page.findall('fontspec'):fonts[font.get('id')]=font.attrib
   for t in page.findall('text'):
    value=''.join(t.itertext()).strip()
    if not value:continue
    f=fonts[t.get('font')];family=re.sub(r'^[A-Z]{6}\+','',f['family']);size=int(f['size']);seen[size,family]+=1
    if size<12:small.append(dict(pdf_page=int(page.get('number')),rounded_size=size,font_family=family,text=value))
 assert small and all(x['rounded_size']==8 and x['font_family'] in {'CMR8','CMMI8','CMSY8'} for x in small)
 table('font_inventory.csv',[dict(rounded_size=k[0],font_family=k[1],text_spans=v) for k,v in sorted(seen.items())]);table('math_script_spans.csv',small)
 assert 'framework.png' in (O/'shared_main_stdout.txt').read_text()
 for n,h in oldready['authority_source_sha256'].items():assert sha(R/n)==h,n
 for n,h in oldready['admission_source_hashes'].items():assert sha(R/n)==h,n
 registry=read(R/'design/task4_user_current_review.json');assert registry['version']=='V160' and registry['pdf_sha256']==sha(pdf) and registry['primary_model']=='V154'
 assert read(P/'drafts/task4_current_review.json')==registry
 report=dict(status='pass',version='V160',primary_model='V154',review='V160 independent; default shared main unchanged',total_pages=24,main_and_references_pages=22,news_pages=[16,17],provisional_AI_pages=[23,24],compiled_references=47,pdf_sha256=sha(pdf),pdf_bytes=pdf.stat().st_size,changed_pages_vs_V159=changed,pixel_identical_pages=23,all24_pages_visually_reviewed=True,page14_full_size_reviewed=True,root_proxy_text_equal=True,server_compile_verified=False,LaTeX_warnings=0,requirements=len(rows),status_counts=dict(Counter(x['status'] for x in rows)),prior40_statuses_preserved=True,pending_gates_preserved=pending,submission_ready=False,actual_control_number='PENDING',AI_history_complete=False,fonts=dict(ordinary_minimum_integer_rounded=12,small_math_spans=len(small),smallest_integer_rounded=8,not_an_all_glyph_size_certificate=True),scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(protected)-1,authorized_pointer_file='AGENTS.md current-review reference only',source_responses_refreshed=False,authority_source_sha256=oldready['authority_source_sha256'],primary_data_admissions=0,primary_score_width_change=0,verifier_sha256=sha(Path(__file__)))
 (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':protected},indent=2)+'\n');(O/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:report[k] for k in ['status','requirements','status_counts','fonts','scientific_files_unchanged','manuscript_files_unchanged','submission_ready']},indent=2))
if __name__=='__main__':main()
