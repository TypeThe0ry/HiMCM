"""Extract scope witnesses from newly retrieved education publications, not PTRs."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def text(p,page):return subprocess.check_output(['pdftotext','-f',str(page),'-l',str(page),'-layout',str(p),'-'],text=True)
def run():
 retrieval=json.loads((ROOT/'retrieval.json').read_text())
 for r in retrieval['responses']:
  p=ROOT/r['file'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes'] and r['status']==200
 z=text(ROOT/'zurich_2025_26_original.pdf',15);h=text(ROOT/'helsinki_2025_original.pdf',158)
 for name,body in [('zurich_page15_extracted.txt',z),('helsinki_page158_extracted.txt',h)]:(ROOT/name).write_text(body)
 assert 'Anstellungen von Lehrpersonen an öffentlichen Schulen 2025' in z
 assert re.search(r'Mittelschule 3\s+2 812\s+1271\s+1 541',z)
 assert re.search(r'Mittelschule\s+63.0 %\s+1 771.6',z)
 assert re.search(r'Mittelschulen\s+3 617\s+2 179\s+2 227',z)
 assert 'ohne Schulleiter' in z and 'Anzahl Anstellungsverhältnisse per 31. Dezember 2025' in z
 assert 'Beschäftigungsumfang des jeweiligen Rechnungsjahres' in z and 'im Kanton Zürich' in z
 assert re.search(r'2024\s+61 008\s+18 661\s+47 520\s+25 684\s+37 075',h)
 assert 'Adult education centres' in h and '2000–2021' in h and 'Opettajien antamat opetustunnit' in h
 landing=(ROOT/'zurich_publication_original.html').read_text();assert 'Juli 2026' in landing and '2025/2026' in landing
 result=dict(research_iteration='V147',primary_data_admissions=0,observations=[],candidates=[
  dict(city='Zurich',indicator='upper_secondary_ptr',source_file='zurich_2025_26_original.pdf',pdf_page=15,printed_pages=[28,29],reference_year=2025,publication_month='2026-07',geography='Kanton Zurich; no municipality allocation in the inspected tables',teaching_appointments_mittelschule=2812,teaching_fte_mittelschule=1771.6,education_department_mittelschulen_employment_fte=2227,appointments_exclude_heads=True,department_employment_period='accounting-year employment volume; appointment count at 31 December',status='not_admitted',reason='Canton public-school teaching appointments and teaching FTE do not identify all-provider city upper-secondary FTE. Separate department employment volume is another population/period, not a replacement teaching denominator.',next_required='A city/school allocation for upper-stage teaching FTE and matched pupils, including provider coverage.'),
  dict(city='Helsinki',indicator='upper_secondary_ptr',source_file='helsinki_2025_original.pdf',pdf_page=158,printed_page=157,table='7.14',latest_row_year=2024,general_upper_secondary_students=18661,vocational_students=47520,adjacent_table='7.15 adult education centres 2000-2021',adjacent_teacher_variable='teaching hours, not teachers or FTE',status='not_admitted',reason='This page supplies students at different levels but no matched upper-secondary teaching FTE. The adjacent adult-education teaching hours cannot be used as that denominator; no hours-to-FTE conversion or ratio is constructed.',next_required='Matched city upper-secondary teaching FTE, year, provider universe and general/vocational stage definition.')],scope='Claims concern these specific publication pages; they do not prove suitable data are unavailable elsewhere. Original user entries and V136 admission policy remain unchanged.',source_sha256={r['file']:r['sha256'] for r in retrieval['responses']},extractor_sha256=sha(Path(__file__)))
 (ROOT/'scope_audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Two new publication pages extracted; real values and incompatible denominators distinguished; zero admissions.')
if __name__=='__main__':run()
