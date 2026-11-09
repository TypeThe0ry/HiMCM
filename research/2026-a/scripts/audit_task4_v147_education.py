"""Independently read PDF word coordinates and verify unchanged V136 science."""
from pathlib import Path
import hashlib,json,subprocess,xml.etree.ElementTree as ET
import numpy as np
from task4_user_v136_revision import revised_bounds
from task4_v5_model import NAMES
R=Path(__file__).resolve().parents[1];D=R/'data/task4_v147_education_refresh';O=R/'results/task4_v147_education';P=R.parents[2]/'HiMCM-Overleaf'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def words(file,page):
 raw=subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-bbox',str(D/file),'-'])
 root=ET.fromstring(raw);node=next(x for x in root.iter() if x.tag.endswith('page'))
 return float(node.get('width')),[(w.text,float(w.get('xMin')),float(w.get('yMin'))) for w in node if w.tag.endswith('word')]
def line(ws,label,side=None,width=0,contains=None):
 candidates=[w for w in ws if w[0]==label and (side is None or (w[1]<width/2)==(side=='left'))]
 rows=[' '.join(w[0] for w in sorted([v for v in ws if abs(v[2]-a[2])<1 and (side is None or (v[1]<width/2)==(side=='left'))],key=lambda x:x[1])) for a in candidates]
 if contains:rows=[r for r in rows if contains in r]
 assert len(rows)==1,(label,rows);return rows[0]
def main():
 O.mkdir(exist_ok=True);s=read(D/'scope_audit.json');assert s['observations']==[] and s['primary_data_admissions']==0
 for n,h in s['source_sha256'].items():assert sha(D/n)==h,n
 assert sha(D/'extract.py')==s['extractor_sha256']
 wz,z=words('zurich_2025_26_original.pdf',15);wh,h=words('helsinki_2025_original.pdf',158)
 teaching=line(z,'Mittelschule','left',wz,'63.0');assert '63.0 % 1 771.6' in teaching
 appointments=line(z,'Mittelschule','left',wz,'812');assert '2 812 1271 1 541' in appointments
 employment=line(z,'Mittelschulen','right',wz);assert '3 617 2 179 2 227' in employment
 students=line(h,'2024');assert '2024 61 008 18 661 47 520 25 684 37 075'==students
 # The printed percentage is rounded to one decimal percentage point.
 assert abs(1771.6/2812*100-63.0)<.05
 a,b=s['candidates'];assert (a['teaching_appointments_mittelschule'],a['teaching_fte_mittelschule'],a['education_department_mittelschulen_employment_fte'])==(2812,1771.6,2227)
 assert (b['latest_row_year'],b['general_upper_secondary_students'],b['vocational_students'])==(2024,18661,47520)
 frozen={}
 for n,k in [('design/task4_user_v136_snapshot.json','source_sha256'),('results/task4_v137_revision/audit.json','result_sha256'),('results/task4_v138_priority/summary.json','source_sha256')]:frozen.update(read(R/n)[k])
 for n,digest in frozen.items():assert sha(R/n)==digest,n
 csv=R/'data/task4_v117_team_intake/city_indicators.csv';assert sha(csv)=='430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c'
 frame,lo,hi=revised_bounds();unknown=(lo==0)&(hi==1);points=lo==hi;counts=dict(point=int(points.sum()),partial=int((~points&~unknown).sum()),unknown=int(unknown.sum()));assert counts==dict(point=112,partial=33,unknown=15)
 for city in ['Zurich','Helsinki']:assert (lo[list(frame.city).index(city),NAMES.index('upper_secondary_ptr')],hi[list(frame.city).index(city),NAMES.index('upper_secondary_ptr')])==(0,1)
 manifest=read(P/'drafts/task4_v137_assets/manifest.json');qa=read(P/'drafts/task4_v137_assets/qa.json');assert manifest['documentation_revision']==qa['documentation_revision']=='V146'
 protected={str((P/'drafts'/n).relative_to(P)):v for n,v in manifest['manuscript_source_sha256'].items()};protected.update(manifest['protected_files']);protected['drafts/task4_v137_paper.pdf']=qa['pdf_sha256']
 for n,digest in protected.items():assert sha(P/n)==digest,n
 for prefix,file in [('zurich','zurich_2025_26_original.pdf'),('helsinki','helsinki_2025_original.pdf')]:assert (D/file).read_bytes().startswith(b'%PDF')
 scope_files={str(p.relative_to(R)):sha(p) for p in D.iterdir() if p.is_file() and p.name not in ['verification.json','README.md']}
 result=dict(status='pass',iteration='V147',source_pages_checked=[dict(source='zurich_2025_26_original.pdf',pdf_page=15,printed_pages=[28,29]),dict(source='helsinki_2025_original.pdf',pdf_page=158,printed_page=157)],independent_extraction='PDF word coordinates grouped by row and half-page; independently of layout-text assertions',extracted_rows=dict(teaching=teaching,appointments=appointments,department_employment=employment,helsinki_2024_students=students),primary_data_admissions=0,interval_width_reduction=0,current_counts=counts,protected_scientific_files=len(frozen),scientific_file_sha256=frozen,manuscript_files_unchanged_sha256=protected,current_documentation_revision='V146',primary_evidence='V136 user16',extensions='V137',no_new_rank_simulation='Frozen primary rankings verified by hash; this source review admits no bounds and does not rerun Monte Carlo.',source_sha256=scope_files,verifier_sha256=sha(Path(__file__)),visual_review=dict(original_source_pages_reviewed=True,files=['zurich_page15_review.png','helsinki_page158_review.png']),next_action='Seek a new matched teaching-FTE allocation rather than reuse these mismatched aggregates; do not infer global nonexistence.')
 (O/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
 selected={k:v for k,v in result.items() if k not in ['scientific_file_sha256','manuscript_files_unchanged_sha256','source_sha256']};(D/'verification.json').write_text(json.dumps(selected,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','primary_data_admissions','current_counts','protected_scientific_files','current_documentation_revision']},indent=2))
if __name__=='__main__':main()
