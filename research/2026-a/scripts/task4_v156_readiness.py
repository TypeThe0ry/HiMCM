"""Current artifact/requirement map; never equate passage matches with compliance."""
from pathlib import Path
from collections import Counter,defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo
import csv,hashlib,json,re,subprocess,tempfile,xml.etree.ElementTree as ET
from task4_user_v154_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];P=R.parents[2]/'HiMCM-Overleaf';O=R/'results/task4_v156_readiness';D=R/'data/task4_v156_requirements_refresh'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def norm(s):return ' '.join(re.sub(r'(?<=\w)-[ \t]*\n[ \t]*(?=\w)','',s).split())
def table(n,rows):
 with (O/n).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def main():
 O.mkdir(exist_ok=True);pdf=P/'drafts/task4_v154_paper.pdf';assets=P/'drafts/task4_v154_assets';q=read(R/'results/task4_v154_transition/verification.json');m=read(assets/'manifest.json')
 assert q['version']==m['version']=='V154' and sha(pdf)==q['pdf_sha256']
 assert q['status']=='pass' and q['all_pages_visually_reviewed'] and not q['submission_ready']
 sources={}
 for r in read(D/'retrieval.json')['responses']:
  assert r['status']==200 and sha(R/r['archived_original'])==r['sha256'];sources[r['archived_original']]=r['sha256']
 assert len(sources)==4 and all(r['same_bytes_as_v123'] for r in read(D/'retrieval.json')['responses'])
 for n,h in m['source_sha256'].items():assert sha(R/n)==h,n
 old=read(R/'results/task4_v151_shared_entry/verification.json');protected=dict(old['manuscript_files_unchanged_sha256'])
 for folder,key in [('task4_v151_shared_entry','support_file_sha256'),('task4_v152_tail_access','selected_file_sha256'),('task4_v153_milan_proposal','selected_file_sha256'),('task4_v154_transition','selected_file_sha256'),('task4_v155_priority','selected_file_sha256')]:protected.update(read(R/'results'/folder/'delivery.json')[key])
 for n,h in protected.items():assert sha(P/n)==h,n
 frame,lo,hi=revised_bounds();assert (len(frame),len(NAMES))==(16,10)
 counts=dict(point=int((lo==hi).sum()),unknown=int(((lo==0)&(hi==1)).sum()));counts['partial']=160-counts['point']-counts['unknown'];assert counts==dict(point=112,unknown=14,partial=34)
 text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);pages=[norm(x) for x in text.split('\f') if x.strip()];aux=(P/'drafts/task4_v154_paper.aux').read_text()
 def label(k):return int(re.search(r'\\newlabel\{'+k+r'\}\{\{[^}]*\}\{(\d+)\}',aux).group(1))
 main_end=label('main-end');ns,ne=label('news-start'),label('news-end');assert len(pages)==24 and main_end==22 and (ns,ne)==(16,17)
 assert main_end<=25 and 1<=ne-ns+1<=2 and pdf.stat().st_size<20_000_000
 for i,p in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(i)+r' of 24',p),i
 # The PDF-derived font inventory is rounded to integer sizes by Poppler.
 # Smaller math scripts are reported explicitly, not silently labelled 12pt.
 with tempfile.TemporaryDirectory(prefix='himcm-v156-font-',dir='/data/scratch') as tmp:
  prefix=Path(tmp)/'font';subprocess.run(['pdftohtml','-xml','-i','-zoom','1','-fontfullname',str(pdf),str(prefix)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  xml=ET.parse(prefix.with_suffix('.xml')).getroot();fonts={};seen=Counter();small=[]
  for page in xml.findall('page'):
   for f in page.findall('fontspec'):fonts[f.get('id')]=f.attrib
   for t in page.findall('text'):
    value=''.join(t.itertext()).strip()
    if not value:continue
    font=fonts[t.get('font')];family=re.sub(r'^[A-Z]{6}\+','',font['family']);size=int(font['size']);seen[(size,family)]+=1
    if size<12:small.append(dict(pdf_page=int(page.get('number')),rounded_size=size,font_family=family,text=value))
 inventory=[dict(rounded_size=size,font_family=family,text_spans=n) for (size,family),n in sorted(seen.items())];table('font_inventory.csv',inventory);table('math_script_spans.csv',small)
 expected={'(', '(14)', '(18)', ')', '+', '.', '2', '3', '30', '5', '=', 'N', 'Z', 'b', 'c', 'd', 'i', 'ij', 'j', 'jk', 'k', 'max', 'q', 'r', 's', 't/', '¯', '̸', '′', '−', '∗'}
 assert small and set(x['text'] for x in small)<=expected
 assert all(x['rounded_size']==8 and x['font_family'] in {'CMMI8','CMR8','CMSY8'} for x in small)
 rows=[]
 def add(key,authority,requirement,status,evidence,scope,markers=(),window=None):
  window=window or (3,main_end);found=[]
  for marker in markers:
   hits=[i for i,p in enumerate(pages,1) if window[0]<=i<=window[1] and norm(marker).lower() in p.lower()]
   assert hits,(key,marker);found.extend(hits)
  rows.append(dict(id=key,authority=authority,requirement=requirement,status=status,pdf_pages=','.join(map(str,sorted(set(found)))),evidence=evidence,scope_or_remaining_action=scope,passage_markers=json.dumps(markers)))
 add('PA-summary','Problem A p1','One-page summary','technical_pass','Page 1 summary and first-page boundary verified','Technical one-page property; content judgement separately scoped',['Summary Sheet'],(1,1))
 add('PA-toc','Problem A p1','Contents page','technical_pass','Page 2 TOC includes news, references and AI section','Actual PDF text checked',['Contents'],(2,2))
 add('PA-sample','Problem A p1','Rank at least ten cities','technical_pass','Current factory verifies 16 cities x 10 indicators; primary ranking table page 9','Inherited sample is not representative of all world cities',['Conservative baseline decision ranks'])
 add('PA-criteria','Problem A p1','Explain included and omitted criteria','reviewed_scoped','Criteria rationale and omitted attributes are discussed in 1.2','No claim that the selected ten exhaust student needs',['language fit','one main quality score'])
 add('PA-best','Problem A p1','Define and justify the preferred city','reviewed_scoped','Definition and maximum-regret decision correspond to current results','Zurich is a conditional conservative recommendation; 16 possible, zero necessary champions',['conservative choice under these ten criteria','Zurich minimizes maximum regret'])
 add('PA-data','Problem A p1','Gather and cite relevant data','reviewed_scoped','Data section, source examples and 47 references; 22 supplements explicitly cited','Supplied points are not all independently validated; collection completeness cannot be certified',['A traceable city','Some supplied values lack original source URLs'])
 add('PA-limits','Problem A p1','Discuss relevant limitations','reviewed_scoped','Measurement, missingness and source-policy consequences stated','Conditional intervals are not sampling confidence intervals or joint physical feasibility',['not sampling confidence intervals','28 flagged points'])
 add('PA-revision','Problem A p1','Explain a significant model revision','reviewed_scoped','Same-input midpoint versus interval diagnostic with explicit decision change','Controlled formulation comparison, not invented historical chronology',['A significant revision','0.650'])
 add('PA-news','Problem A p1','One-to-two-page nontechnical news including modelling process','reviewed_scoped','News occupies pages 16-17 and explains evidence ranges and common scoring yardsticks','Assistant review finds modelling process and scoped recommendation; nontechnical quality is not machine-certified',['common scoring yardsticks'],(ns,ne))
 add('PA-references','Problem A p1','Reference list','technical_pass','Actual references follow news and end on main page 22','Citation presence does not certify every source or original submitted value',['References'],(18,main_end))
 add('PA-ai-section','Problem A p1 / AI policy p2','AI-use report after main solution','partial','Appendix starts page 23 and is explicitly incomplete','Placement verified; full actual team AI history is not established',['Report on Use of AI Tools','incomplete review record'],(main_end+1,len(pages)))
 add('U-baseline','User task 2 / task 4 writing','Weights, TOPSIS calculation and result interpretation','reviewed_scoped','Sections 5.1-5.3 and primary results align','Weights are retained analyst choices, not a fabricated student AHP survey',['Determining indicator weights','TOPSIS scoring calculation','Scoring results and interpretation'])
 add('U-model-count','User task 2','Keep evaluation models compact','reviewed_scoped','TOPSIS primary; VIKOR contrast; AHP preference construction; MC sensitivity','No Borda/PageRank or new unrelated ranking model added',['one main quality score','VIKOR'])
 add('U-future','User revision 1','Consider future conditions','reviewed_scoped','Declared shocks, duration transformations and decision thresholds','No fitted multi-year trend or prediction of an actual future year',['forecast date','uncalibrated distribution'])
 add('U-preference','User revision 2','Consider different priorities','reviewed_scoped','Education and independent-living profile scenarios','No representative survey or exact-age weights',['Education priority','not representative student opinion'])
 add('U-perturbation','User revision 3','Perturb weights and inputs','reviewed_scoped','Separate Dirichlet preference and bounded future-shock experiments','Reported frequencies condition on declared distributions and retained intervals',['Dirichlet','conditional stress frequencies'])
 add('U-country','User same-country task','Compare cities in one country','reviewed_scoped','Separate US and India historical pairs in section 7','Each main16 city is in a different country; legacy25 cases are separate, not current main16 within-country estimates',['Every primary city belongs to a different country','legacy 25-city V117'])
 add('U-fairness','User fairness follow-up','Distinguish facility supply from access fairness','reviewed_scoped','Shanghai district resources and bottom-20% pupil-mass calculation','District-homogeneous school-location resource case, not individual access; primary city totals cannot identify fairness',['Citywide facilities per resident','0.580954'])
 add('U-age','User age follow-up','Examine growth-stage differences','reviewed_scoped','Historical groups plus retained V148 joint feasibility proof and finite witnesses','Not present-day exact ages 14 and 18, preference evidence or causal age effects',['shared-membership constraint','0.23842','not observed age effects'])
 add('U-preserve','User data constraints','Preserve original CSV, weights and interval rules','technical_pass','Original CSV/factory/source hashes verified; current 112/34/14 matrix retained','This review admits no data or change of model',[])
 add('U-vintage','User baseline-year discussion / retained data rules','Record actual years around nominal 2025 baseline','reviewed_scoped','Mixed-vintage explanation and source-policy withdrawal diagnostic','64 submitted point entries carry 2026 labels; no relabelling as same-year 2025 measurements',['nominal reference year is 2025','64 are labelled 2026'])
 add('U-source-quality','User genuine-data constraint','Retain source uncertainty and avoid invented measurements','partial','Flags, unmatched original homicide rates and source-specific tests disclosed','112 accepted points are not a fully independently certified measurement matrix',['numerator 340','rate of 0.14 still lacks a verified'])
 add('U-writing-skill','User mandatory skill','Use the specified anti-defensive-writing skill','reviewed_scoped','Installed skill and repository policy used for current explanatory prose','Result-first structure does not permit suppressing contrary evidence',[])
 add('CI-budget','Instructions VI','Main-page allowance including references','technical_pass','22 main/reference pages; two additional provisional AI pages','Three main pages remain under the current 25-page limit',[])
 add('CI-file','Instructions VI / submission guide p3','Single PDF below 20 MB','technical_pass',str(pdf.stat().st_size)+' bytes; one current owned PDF','This checks the current draft, not an uploaded final file',[])
 add('CI-font','Instructions IV.13','Readable English text at nominal 12pt or larger','technical_scoped','12pt article; PDF inventory shows normal text >=12 after Poppler rounding; actual smaller mathematical spans listed separately','Integer-rounded font inventory and V154 render review; math scripts reported separately, not a blanket all-glyph-size certificate',[])
 add('CI-headers','Instructions VI','Control and page number in all page headers','partial','All 24 actual headers show page x of 24 and PENDING','Actual registered team control number is still unverified',[])
 add('CI-control','Instructions IV.4 / submission guide p1','Use the actual registration control number','unverified','No verified registration number in current artifacts','Obtain the real number; do not choose between conflicting historical placeholders',[])
 add('CI-anonymity','Instructions IV.12','Remove team and institution identifying information','unverified','PDF author metadata empty; draft uses anonymous PENDING headers','Full identity review needs actual team/institution identities; references to source authors are not team identifiers',[])
 add('AI-tool-disclosure','AI policy p2 / Instructions IV.9','Disclose actual tools/models and purposes with citations','partial','Appendix records a bounded Codex/Exa prefix with references','Does not cover all later continuations, tools, other chats or team members',['gpt-6.1-sol','Exa'],(main_end+1,len(pages)))
 add('AI-complete-record','AI policy p2','Reconcile actual query/output records with applicable disclosure examples','unverified','Appendix openly states incomplete coverage; fixed prefix is not expanded by reconstruction','Use actual saved records; document translation/completion exceptions where applicable. Do not fabricate historical prompts or outputs',[])
 add('AI-verification','AI policy p2','Check AI-assisted content and citations','reviewed_scoped','Primary scientific audits, source-scope audits, 22-supplement citation chain and independent V154 check','Selected audits support specified calculations; they do not certify all original points or complete team authorship',[])
 add('TEAM-integration','User ownership / team workflow','Select and authorize the final shared manuscript','awaiting_team','Current PDF is a self-owned independent review; shared main preserved','Specific authorization for teammate-text integration remains necessary',[])
 add('TEAM-independent-entry','User owned-review workflow','Current independent review and root proxy compile locally','technical_pass','V154 retained direct/root build receipts:24 pages, zero warnings, page text matches; hashes preserved','Local build evidence only; default online Main document and server compiler state are unverified',[])
 add('TEAM-shared-build','User AGENTS workflow','Shared entry compiles with its assets','not_ready','Last actual build log stops at existing missing framework.png','No teammate prose or asset replaced without authorization; owned independent PDF compiles',[])
 add('REG-eligibility','Instructions I / IV','Verify registration, affiliation, eligibility and advisor records','unverified','This workspace contains no verified current registration receipt','Not evidence of nonregistration; use actual team/advisor records',[])
 add('SUB-filename','Submission guide p3','Name final PDF with the registered control number','awaiting_team','Current file is an owned review filename, not a verified control-number filename','After actual identity and final artifact selection, prepare the exact final attachment',[])
 add('SUB-upload','Instructions VI / submission guide p1-3','Submit the selected PDF through the official form','not_performed','No upload or form submission performed','Requires actual control/advisor identifiers, problem A selection, AI statement and final artifact authorization',[])
 add('SUB-confirmation','Instructions VI / submission guide p3','Verify receipt through advisor portal','unverified','No submission/portal receipt established; guide says no email confirmation','Check actual advisor-portal receipt after an authorized upload; do not wait for an email',[])
 add('PUB-sharing','Instructions IV.7 / existing user choice','Resolve public research publishing during contest window','awaiting_team','Existing publishing choice remains unanswered; public push held','No permission inferred, no public push or visibility change performed',[])
 # A current supplement/citation bridge adds Milan while preserving the21 prior rows.
 old_sources=list(csv.DictReader((R/'results/task4_v146_source_coverage/admitted_sources.csv').open()))
 bridge=[];source_checks={}
 core=(P/'drafts/task4_v154_core.tex').read_text()
 citations={key.strip() for block in re.findall(r'\\cite\{([^}]+)\}',core) for key in block.split(',')}
 for entry in old_sources:
  for n,h in json.loads(entry['source_hashes']).items():assert sha(R/n)==h,n;source_checks[n]=h
  bridge.append({k:entry[k] for k in ['city','indicator','admission_version','bibkey','admission_manifest','utility_lower','utility_upper']})
 milan=read(R/'design/task4_user_v154_admissions.json')
 for n,h in milan['source_hashes'].items():assert sha(R/n)==h,n;source_checks[n]=h
 bridge.append(dict(city='Milan',indicator='public_transport_density',admission_version='V154',bibkey='milanmetro',admission_manifest='design/task4_user_v154_admissions.json',utility_lower=milan['observations'][0]['utility_after'][0],utility_upper=1))
 assert len(bridge)==22 and len({(x['city'],x['indicator']) for x in bridge})==22
 for x in bridge:
  i=frame.city.tolist().index(x['city']);j=NAMES.index(x['indicator'])
  assert abs(float(x['utility_lower'])-lo[i,j])<1e-12 and abs(float(x['utility_upper'])-hi[i,j])<1e-12
  assert x['bibkey'] in citations
 table('supplement_citation_bridge.csv',bridge)
 table('requirements.csv',rows)
 deadlines={k:datetime(2026,11,day,hour,tzinfo=ZoneInfo('America/New_York')).astimezone(ZoneInfo('Asia/Singapore')).isoformat() for k,day,hour in [('stop_work',17,20),('upload_by',17,21),('recommended_portal_receipt_check',18,20)]}
 report=dict(iteration='V156',paper_documentation_revision='V154',primary_evidence='V154 user16',extensions='V154',submission_ready=False,scope='Current artifact/requirement mapping and technical checks, not a COMAP compliance certificate. Passage markers locate assistant-reviewed content; they do not prove scientific or writing quality. No new model, data, manuscript or PDF authored.',requirements=len(rows),status_counts=dict(Counter(r['status'] for r in rows)),total_pages=len(pages),main_pages=main_end,news_pages=[ns,ne],ai_pages=list(range(main_end+1,len(pages)+1)),pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),current_counts=counts,admitted_supplement_citations=22,admission_source_hashes=source_checks,source_responses_refreshed=4,source_bytes_unchanged=True,authority_source_sha256=sources,manuscript_files_unchanged_sha256=protected,main_remaining_page_allowance=25-main_end,font_inventory=dict(integer_rounded_by='Poppler pdftohtml -zoom 1',smaller_math_script_spans=len(small),smaller_font_families=['CMMI8','CMR8','CMSY8'],minimum_math_script_rounded_pt=8,prose_minimum_rounded_pt=12,not_a_blanket_all_glyph_size_certificate=True),deadlines_asia_singapore=deadlines,primary_data_admissions=0,primary_score_interval_width_reduction=0,compiler_rerun=False,unchanged_paper_render_evidence='V154 final rendered review bound by current PDF SHA256',remaining_external_gates=['Actual control number and identity review','Complete actual team AI record','Authorized final shared-paper integration and missing asset','Verified registration and advisor identifiers','Final file naming, authorized upload and portal receipt','Existing public publishing choice'],generator_sha256=sha(Path(__file__)),result_sha256={str(p.relative_to(R)):sha(p) for p in [O/'requirements.csv',O/'font_inventory.csv',O/'math_script_spans.csv',O/'supplement_citation_bridge.csv']})
 (O/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['requirements','status_counts','total_pages','main_pages','submission_ready']},indent=2))
if __name__=='__main__':main()
