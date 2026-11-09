"""Extract selected published staffing facts; no ratio is admitted."""
from pathlib import Path
from decimal import Decimal
from html.parser import HTMLParser
import hashlib,json,re,subprocess
D=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def page(name,n,raw=False):return subprocess.check_output(['pdftotext','-raw' if raw else '-layout','-f',str(n),'-l',str(n),str(D/name),'-'],text=True)
def row(text,label):
 match=re.search(r'^\s*'+re.escape(label)+r'\s+([\d,.]+)\s+([\d,.]+)\s+(-?[\d,.]+)\s+([\d,.]+)\s*$',text,re.M)
 assert match,label
 return dict(zip(['allocated_FTE','payroll_FTE','difference_FTE','reported_cover_percent'],[float(x.replace(',','')) for x in match.groups()]))

def main():
 receipts=json.loads((D/'retrieval.json').read_text());success=[x for x in receipts if x.get('status')==200]
 assert len(success)==3 and len(receipts)==4
 for x in success:assert sha(D/x['file'])==x['sha256']
 class Links(HTMLParser):
  def __init__(self):super().__init__();self.links=[]
  def handle_starttag(self,tag,attrs):
   if tag=='a':self.links.extend(v for k,v in attrs if k=='href')
 links=Links();links.feed((D/'city_etb_publications_original.html').read_text())
 assert any(x.endswith('/media/City-of-Dublin-ETB-Annual-Report-2024.pdf') for x in links.links)
 table10=page('workforce_2026_original.pdf',14)
 city=row(table10,'City Of Dublin');neighbour=row(table10,'Dublin & Dun Laoghaire')
 county=row(page('workforce_2026_original.pdf',12),'Dublin')
 assert city['payroll_FTE']==411.8 and city['allocated_FTE']==376.1
 assert Decimal(str(city['payroll_FTE']))-Decimal(str(city['allocated_FTE']))==Decimal('35.7')
 assert neighbour['payroll_FTE']==1832.8 and county['payroll_FTE']==6075.7
 definitions=' '.join(page('workforce_2026_original.pdf',18).split())
 assert 'excludes staff that are wholly employed by private schools' in definitions
 assert 'further education and training centres (FET)' in definitions
 annual=page('city_etb_2024_original.pdf',18,raw=True)
 matches=re.findall(r'^Community Colleges\s+(\d+)\s+([\d,]+)\s*$',annual,re.M)
 assert matches and set(matches)=={('11','3,862')}
 assert 'Year2024/2025' in annual or 'Year 2024/2025' in annual
 result=dict(iteration='V161',status='source scope reviewed; no admission',successful_original_responses=3,failed_indexed_URLs=1,
  payroll_reference='Last payroll runs in November2025;2025/26 school year; report April2026',
  workforce_table10=dict(pdf_page=14,geography='ETB employer/catchment, not an all-provider municipal total',school_scope='Post Primary Vocational',city_of_dublin=city,dublin_and_dun_laoghaire=neighbour),
  workforce_table9=dict(pdf_page=12,geography='County Dublin',school_scope='Post Primary Secondary, Community & Comprehensive; vocational ETB separate',dublin=county),
  annual_enrolments=dict(pdf_page=18,printed_page=16,academic_year='2024/2025',community_college_locations=11,full_time_students=3862,scope='City of Dublin ETB Community Colleges, not all city upper-secondary pupils',accessibility_text_duplicates_not_summed=True),
  provider_exclusion='Staff wholly employed by private schools are excluded from government/ETB payroll workforce',
  FET_rule='Recognised post-primary-school employer required; FET-centre employed teachers excluded from this workforce definition',
  admission_gaps=['No upper-secondary teaching-stage workload split','ETB subset and county table are not a matched all-provider city denominator','2024/25 pupil table not same school year as November2025 payroll','Wholly privately employed staff excluded; all-provider teacher superset unproven'],
  allocation_counterexample=dict(payroll_minus_allocation=35.7,payroll_exceeds_allocation=True,calculated_payroll_over_allocation_percent=100*411.8/376.1,published_cover_percent=100,claim='Allocated posts cannot be assumed to upper-bound actual payroll FTE in this source; no unreported capping algorithm inferred'),
  observations=[],primary_data_admissions=0,primary_score_width_change=0,current_model='V154 unchanged',current_paper='V160 unchanged',
  source_sha256={x['file']:x['sha256'] for x in success},extractor_sha256=sha(Path(__file__)))
 (D/'scope_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'city_ETB':city,'county':county,'enrolments':3862,'admissions':0},indent=2))
if __name__=='__main__':main()
