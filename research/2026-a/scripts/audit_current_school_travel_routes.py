"""Read-only bounded route/evidence checks; no school-duration observation is admitted."""
from pathlib import Path
import hashlib,html,json,re,subprocess,sys,xml.etree.ElementTree as E,zipfile
from task4_audit_output import audit_parser,check_output,emit_report
R=Path(__file__).resolve().parents[1];G=R.parents[1];P=G.parent/'HiMCM-Overleaf';D=R/'data';O=R/'results/current_school_travel_review/verification.json'
a=audit_parser(__doc__).parse_args();check_output(a,O,G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def text(p):return ' '.join(html.unescape(re.sub('<[^>]*>',' ',p.read_text())).split())
sources=[];success=0
v=D/'current_vienna_school_commuting'
for row in read(v/'retrievals.json'):
 raw=(v/row['file']).read_bytes();assert row['status']==200 and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];success+=1
selected=read(v/'selected_scope.json');assert json.loads(subprocess.check_output([sys.executable,str(v/'extract.py')],text=True))==selected
assert selected['selected_year']==2024 and len(selected['selected_rows'])==12 and not selected['contains_Wien_row']
assert selected['header'][1]=='Schüler:innen und Studierende am Wohnort' and 'Auspendler:innen' in selected['header'][3]
assert selected['primary_admissions']==0 and 'Record Swapping' in selected['source_note']
w=D/'current_warsaw_school_travel';failed=0
for p in sorted(w.glob('*.receipt.json')):
 row=read(p)
 if row['file']:
  raw=(w/row['file']).read_bytes();assert row['status']==200 and len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'];success+=1
 else:
  assert row['status']==202 and row['bytes']==0 and row['sha256']==hashlib.sha256(b'').hexdigest();failed+=1
announcement=text(w/'wbr2025_announcement.html');assert 'Ankieterzy' in announcement and 'godzin' in announcement.lower()
assert '2024/25' in text(w/'student_flows_2024_25.html')
t=D/'current_tokyo_school_travel';attempts=read(t/'retrievals.json');assert len(attempts)==3
for row in attempts:assert row['status'] is None and row['bytes']==0 and row['sha256'] is None and row['cookies_sent'] is False
scope=read(t/'scope.json');assert scope['availability']['duration_cell_or_weights_obtained'] is False and scope['availability']['admitted'] is False
assert 'raw handbook/category/survey-scope retrievals failed TLS' in scope['evidence_basis']
assert success==4 and failed==1
core=read(R/'design/task4_user_v203_snapshot.json')['source_sha256'];current=read(R/'results/current_paper_review/current_verification.json');extra={}
for key,val in current.items():
 if key.startswith('additional_') and key.endswith('_sha256'):extra.update(val)
assert len(core)==548 and len(extra)==77
for n,h in {**core,**extra,**current['withdrawal_source_sha256']}.items():assert sha(R/n)==h,n
for n,h in current['current_files_sha256'].items():assert sha(P/n)==sha(G/'paper/current'/n)==h,n
from task4_user_v203_revision import revised_bounds
from task4_v5_model import NAMES
frame,lo,hi=revised_bounds()
for city in ['Vienna','Warsaw','Tokyo']:
 i=frame.city.tolist().index(city);j=NAMES.index('travel');assert lo[i,j]==0 and hi[i,j]==1
for directory in [v,w,t]:sources.extend(sorted(p for p in directory.iterdir() if p.is_file()))
sources.extend([Path(__file__),R/'scripts/task4_audit_output.py'])
report={'status':'pass scoped route check','successful_archived_responses':4,'empty_HTTP202_responses':1,'pre_HTTP_TLS_failures':3,'Vienna_national_2024_count_rows':12,'target_travel_cells_unchanged':['Vienna','Warsaw','Tokyo'],'primary_admissions':0,'actual_primary_width_reduction':0,'core_bindings_checked':548,'supplemental_bindings_checked':77,'withdrawal_evidence_entries_checked':len(current['withdrawal_source_sha256']),'paper_dependencies_each_copy':7,'source_sha256':{str(p.relative_to(R)):sha(p) for p in sources},'scope':'Verifies saved bodies, factual workbook scope, failure receipts and unchanged target cells. It does not certify index-only2015Warsaw report numbers or Tokyo handbook categories from unavailable originals, or claim that no qualifying data exists anywhere.'}
emit_report(report,a,O,G)
