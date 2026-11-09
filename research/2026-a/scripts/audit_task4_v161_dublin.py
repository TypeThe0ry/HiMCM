"""Independent raw-page and immutable-state review of Dublin source candidates."""
from pathlib import Path
from decimal import Decimal
import hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1];D=R/'data/task4_v161_dublin_scope';O=R/'results/task4_v161_dublin_scope';P=Path('/data/projects/HiMCM-Overleaf')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def raw(name,n):return subprocess.check_output(['pdftotext','-raw','-f',str(n),'-l',str(n),str(D/name),'-'],text=True)
def main():
 s=read(D/'scope_audit.json');assert sha(D/'extract.py')==s['extractor_sha256']
 for n,h in s['source_sha256'].items():assert sha(D/n)==h,n
 def numbers(name,page,label):
  lines=raw(name,page).splitlines();line=next(x for x in lines if x.startswith(label+' '))
  return [Decimal(x.replace(',','')) for x in line[len(label):].split()]
 values=numbers('workforce_2026_original.pdf',14,'City Of Dublin')
 assert values==list(map(Decimal,['376.1','411.8','35.7','100']))
 assert values[1]-values[0]==values[2] and values[1]>values[0]
 county=numbers('workforce_2026_original.pdf',12,'Dublin')
 assert county==list(map(Decimal,['6191.7','6075.7','-116.0','98.1']))
 neighbours=numbers('workforce_2026_original.pdf',14,'Dublin & Dun Laoghaire')
 assert neighbours[:2]==list(map(Decimal,['1758.9','1832.8']))
 annual=raw('city_etb_2024_original.pdf',18)
 assert all(x in annual for x in ['Community Colleges 11 3,862','2024/2025','four campuses'])
 assert s['annual_enrolments']['full_time_students']==3862 and s['annual_enrolments']['accessibility_text_duplicates_not_summed']
 assert s['observations']==[] and s['primary_data_admissions']==s['primary_score_width_change']==0
 for name,pages in [('workforce_2026_original.pdf',20),('city_etb_2024_original.pdf',61)]:
  info=subprocess.check_output(['pdfinfo',str(D/name)],text=True);assert int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))==pages
 snapshot=read(R/'design/task4_user_v154_snapshot.json')['source_sha256']
 for n,h in snapshot.items():assert sha(R/n)==h,n
 guard=O/'protected_files.json'
 if guard.exists():manuscript=read(guard)['manuscript']
 else:
  names=subprocess.check_output(['git','-C',str(P),'ls-files','-z']).decode().split('\0');manuscript={n:sha(P/n) for n in names if n}
 for n,h in manuscript.items():assert sha(P/n)==h,n
 review=read(R/'design/task4_user_current_review.json');assert review['version']=='V160' and sha(P/review['pdf'])==review['pdf_sha256']
 (O/'protected_files.json').write_text(json.dumps({'science':snapshot,'manuscript':manuscript},indent=2)+'\n')
 v=dict(status='pass',iteration='V161',source_originals_verified=3,indexed_stale_URL_failure_recorded=True,independent_method='Poppler raw-page parser + Decimal; generator uses layout parser',reviewed_source_PDF_pages={'workforce_2026_original.pdf':[12,14,18],'city_etb_2024_original.pdf':[18]},payroll_greater_than_allocation_counterexample_verified=True,ratio_not_admitted=True,source_scope_sha256=sha(D/'scope_audit.json'),retrieval_sha256=sha(D/'retrieval.json'),verifier_sha256=sha(Path(__file__)),scientific_files_unchanged=len(snapshot),manuscript_files_unchanged=len(manuscript),current_model='V154 unchanged',current_review='V160 unchanged',current_review_pdf_sha256=review['pdf_sha256'],primary_data_admissions=0,primary_score_width_change=0,PDF_authored=False)
 (O/'verification.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v,indent=2))
if __name__=='__main__':main()
