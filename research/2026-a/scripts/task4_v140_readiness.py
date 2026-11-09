"""Current artifact/requirement evidence; never infer final submission from checks."""
from pathlib import Path
import csv,hashlib,json,re,subprocess,tempfile
import numpy as np
from PIL import Image,ImageChops
from task4_user_v136_revision import revised_bounds
ROOT=Path(__file__).resolve().parents[1];PAPER=ROOT.parents[2]/'HiMCM-Overleaf'
OUT=ROOT/'results/task4_v140_readiness';BASE='0ef72f8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    current=read(ROOT/'design/task4_user_current_model.json');assert current['version']=='V136'
    assert read(ROOT/'design/task4_user_v137_extensions.json')['activation_status']=='active'
    frame,lo,hi=revised_bounds();assert len(frame)==16 and lo.shape==hi.shape==(16,10)
    assert [int(np.sum(lo==hi)),int(np.sum((lo<hi)&~((lo==0)&(hi==1)))),int(np.sum((lo==0)&(hi==1)))]==[112,33,15]
    frozen={}
    for file,key in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(ROOT/file)[key])
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    source=ROOT/'data/task4_v140_ai_provenance';meta=read(source/'session_manifest.json');receipt=read(source/'verification.json')
    assert receipt['status']=='pass' and receipt['manifest_sha256']==sha(source/'session_manifest.json')
    assert receipt['extractor_sha256']==sha(ROOT/'scripts/task4_v126_ai_provenance.py')
    assert receipt['verifier_sha256']==sha(ROOT/'scripts/task4_v140_ai_provenance.py')
    assert meta['selected_message_counts']=={'user:None':4,'assistant:commentary':99,'assistant:final_answer':22}
    assert meta['recorded_turn_model_counts']=={'gpt-6.1-sol':28}
    assert not meta['complete_team_ai_history'] and receipt['predecessor_inventory_unchanged']
    assert meta['selected_message_inventory'][:66]==read(ROOT/'data/task4_v129_ai_provenance/session_manifest.json')['selected_message_inventory']
    assert receipt['private_directory_mode']=='0700' and receipt['private_file_mode']=='0600'
    assets=PAPER/'drafts/task4_v137_assets';qa=read(assets/'qa.json');manifest=read(assets/'manifest.json');pdf=PAPER/'drafts/task4_v137_paper.pdf'
    assert qa['documentation_revision']==manifest['documentation_revision']=='V140'
    assert qa['technical_checks']=='pass' and qa['all_pages_rendered_and_visually_reviewed']
    assert sha(pdf)==qa['pdf_sha256'] and qa['pdf_bytes']==pdf.stat().st_size<20_000_000
    assert qa['main_pages_including_news_and_references']==20 and qa['news_pages']==[15,16] and qa['ai_report_pages']==[21,22]
    assert sha(OUT/'compiler_stdout_stderr.txt')==qa['compiler_output_sha256']
    for name,digest in manifest['source_hashes'].items():assert sha(ROOT/name)==digest,name
    for name,digest in manifest['protected_files'].items():assert sha(PAPER/name)==digest,name
    for name,digest in manifest['manuscript_source_sha256'].items():assert sha(PAPER/'drafts'/name)==digest,name
    def old(name):return subprocess.check_output(['git','show',BASE+':'+name],cwd=PAPER)
    tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','drafts/task4_v137_assets'],cwd=PAPER,text=True).splitlines()
    retained=[name for name in tracked if Path(name).name not in {'README.md','manifest.json','qa.json','ai_session_manifest.json','ai_session_verification.json'}]
    retained+=['drafts/task4_v137_generated.tex',*[f'drafts/task4_v137_{k}.tex' for k in ['paper','front','core','conclusion','news','references']]]
    for name in retained:assert (PAPER/name).read_bytes()==old(name),name
    text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True);pages=[p for p in text.split('\f') if p.strip()];assert len(pages)==22
    for n,page in enumerate(pages,1):assert re.search(r'Team Control PENDING\s+Page '+str(n)+r' of 22',page)
    flat=' '.join(text.split());assert all(s in flat for s in ['28 saved turn','99 visible progress','22 complete visible final','03:17 UTC on 9 November 2026','incomplete review record'])
    rows=[]
    def item(key,authority,requirement,page,marker,status='covered',scope=''):
        assert marker.lower() in ' '.join(pages[page-1].split()).lower(),key
        rows.append(dict(id=key,authority=authority,requirement=requirement,status=status,pdf_pages=str(page),evidence=marker,scope_or_remaining_action=scope))
    item('summary','Problem A','One-page summary',1,'Summary Sheet','technical_pass')
    item('toc','Problem A','Contents',2,'Contents','technical_pass')
    item('city_count','Problem A','At least ten ranked cities',9,'Amsterdam','technical_pass','Primary factory verifies sixteen cities; no legacy25 main entry')
    item('best_definition','Problem A','Justify the preferred city',3,'conservative choice','covered','Minimax-regret definition; sixteen possible champions retained')
    item('criteria','Problem A','Explain included and omitted criteria',3,'language fit')
    item('model_budget','user','Keep scoring model count compact',3,'one main quality score','covered_scoped','TOPSIS primary and VIKOR comparison; AHP sets preferences and Monte Carlo tests sensitivity')
    item('data_sources','Problem A / user','Document actual collection and matching',7,'sample base of 22')
    item('revision','Problem A','Explain a significant model revision',10,'retaining uncertain evidence','covered','Same-evidence midpoint diagnostic versus intervals; not invented historical chronology')
    item('news','Problem A','Nontechnical news with modelling process',15,'common scoring yardsticks','technical_pass','Two pages 15-16; read as a scoped explanation')
    item('references','Problem A','Reference list',17,'References','technical_pass')
    item('baseline_weights','user','Weights and preference construction',7,'not estimated from a student survey')
    item('baseline_score','user','TOPSIS computation',8,'TOPSIS scoring calculation')
    item('baseline_results','user','Explain ranking results',9,'maximum regret')
    item('future','user','Future conditions',11,'forecast date','covered_scoped','Declared hypothetical changes, no fitted empirical trend')
    item('preferences','user','Subjective preference scenarios',12,'Education priority','covered_scoped','Analyst-selected priorities; no student survey or precise age-specific weights')
    item('perturbation','user','Perturb model inputs/weights',12,'Dirichlet','covered_scoped','Frequencies condition on declared distributions')
    item('fairness','user','Distinguish facilities from access',13,'Citywide facilities per resident','covered_scoped','Shanghai district case is separate; main city totals do not identify individual access')
    item('ages','user','Distinguish growth stages',13,'2012 broad groups','covered_scoped','Historical Istanbul groups; no exact 14 versus 18 inference')
    item('country','user','Compare cities within a country',14,'Every primary city belongs to a different country','covered_scoped','Separate frozen legacy25 US/India pairs; not a within-country main16 estimate')
    item('ai_appendix','COMAP instructions','Append AI-use report',21,'incomplete review record','partial','125 selected root-session messages; tools/subagents/other team history not covered')
    rows += [dict(id=k,authority=a,requirement=r,status=s,pdf_pages=p,evidence=e,scope_or_remaining_action=nextstep) for k,a,r,s,p,e,nextstep in [
      ('original_inputs','user','Preserve original CSV and scientific rules','technical_pass','','Frozen CSV/factory/anchors hashes and actual 16x10 bounds verified','No original point or partial entry re-resolved'),
      ('page_budget','COMAP instructions','Main solution page budget','technical_pass','1-20','20 main/reference pages; AI pages follow','Technical property only'),
      ('file_size','COMAP instructions','One PDF below size limit','technical_pass','1-22',str(pdf.stat().st_size)+' bytes','Final control-number filename remains unverified'),
      ('font','COMAP instructions / team','Readable text and figure size','technical_pass','all','12pt class; minimum inserted plot label 12.51297pt','Declaration and actual render checked; mathematical scripts follow TeX sizing'),
      ('team_identity','COMAP instructions','Actual control number and anonymity','unverified','all','All headers contain PENDING; no PDF author field','Obtain actual registration control number and team identity review'),
      ('full_AI_history','COMAP AI policy','Reconcile all actual AI use','unverified','21-22','Appendix explicitly incomplete; no raw/private transcript published','Team review of all tools and actual saved input/output records, with stated policy exceptions'),
      ('final_manuscript','team workflow','Choose and authorize final manuscript integration','awaiting_team','','Independent draft; shared main unchanged','Specific authorization for any teammate prose integration'),
      ('registration','COMAP instructions','Registration and eligibility evidence','unverified','','No receipt established by these artifacts','Use actual team/advisor registration records; no claim of nonregistration'),
      ('submission','COMAP instructions','Final upload and receipt','unverified','','No upload performed or receipt established','Finalize identity/history and selected PDF; stop 2026-11-18 09:00 Singapore, upload by 10:00; actual authorized submission and receipt required'),
      ('public_push','team workflow','Public research publishing choice','awaiting_team','','Existing unanswered publishing choice','No public push or visibility change inferred from this audit')]]
    original=old('drafts/task4_v137_paper.pdf');assert hashlib.sha256(original).hexdigest()=='ca0a9b3dea527386fb32a6af9f2f415f6f5dddf584f4f80da07d10ba35b4a291'
    with tempfile.TemporaryDirectory(prefix='himcm_v140_compare_',dir='/data/scratch') as tmp:
        p=Path(tmp);(p/'original.pdf').write_bytes(original)
        for name,path in [('before',p/'original.pdf'),('after',pdf)]:subprocess.run(['pdftoppm','-r','95','-png',str(path),str(p/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        a=sorted(p.glob('before-*.png'));b=sorted(p.glob('after-*.png'));assert len(a)==len(b)==22
        changed=[i for i,(x,y) in enumerate(zip(a,b),1) if ImageChops.difference(Image.open(x).convert('RGB'),Image.open(y).convert('RGB')).getbbox()]
    assert changed==[21,22],changed
    rules=read(ROOT/'data/task4_v123_contest_requirements/source_manifest.json')
    for source_row in rules['sources']:assert sha(ROOT/'data/task4_v123_contest_requirements'/source_row['file'])==source_row['sha256']
    for name,digest in frozen.items():assert sha(ROOT/name)==digest,name
    OUT.mkdir(exist_ok=True)
    with (OUT/'requirements.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for name in ['qa.json','manifest.json']:(OUT/('paper_'+name)).write_bytes((assets/name).read_bytes())
    result=dict(technical_verification='pass',content_review_scope='Requirement locations checked against actual PDF; scoped cases are not new main-city/individual-access estimates',final_submission_ready=False,primary='V136',extensions='V137',documentation_revision='V140',total_pages=22,main_pages=20,news_pages=[15,16],AI_pages=[21,22],selected_AI_messages=125,predecessor_AI_messages=66,added_AI_messages=59,complete_team_ai_history=False,pdf_bytes=pdf.stat().st_size,pdf_sha256=sha(pdf),changed_PDF_pages_vs_V139=changed,pixel_identical_main_and_reference_pages=20,protected_scientific_files=len(frozen),unchanged_previous_assets_and_sections=len(retained),protected_historical_manuscript_files=len(manifest['protected_files']),requirements_reviewed=len(rows),requirement_status_counts={s:sum(x['status']==s for x in rows) for s in sorted({x['status'] for x in rows})},requirements_csv_sha256=sha(OUT/'requirements.csv'),paper_manifest_sha256=sha(OUT/'paper_manifest.json'),paper_qa_sha256=sha(OUT/'paper_qa.json'),official_archive_originals_verified=len(rules['sources']),live_official_pages_retrieved=True,live_rule_check_scope='Official instructions and Problem A retrieved with web tool this iteration; no byte-equality assertion against archived originals',submission_receipt_established=False)
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
