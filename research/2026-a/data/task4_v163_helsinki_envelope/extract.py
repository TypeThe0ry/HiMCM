"""Read national FTE and municipal pupil sources; do not assume an estimate is an upper bound."""
from pathlib import Path
import hashlib,itertools,json,re,subprocess
from openpyxl import load_workbook
D=Path(__file__).resolve().parent;R=D.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(s):
 categories=[sorted(s['dimension'][d]['category']['index'],key=s['dimension'][d]['category']['index'].get) for d in s['id']]
 rows=[]
 for i,coords in enumerate(itertools.product(*categories)):
  r=dict(zip(s['id'],coords));values=s['value'];r['value']=values[i] if isinstance(values,list) else values.get(str(i));r['flag']=s.get('status',{}).get(str(i));rows.append(r)
 return rows

def main():
 receipts=json.loads((D/'retrieval.json').read_text());assert len(receipts)==8
 for r in receipts:assert r['status']==200 and sha(D/r['file'])==r['sha256'],r['file']
 teachers={}
 for year in [2023,2024]:
  rows=decode(json.loads((D/f'FI_ED3_{year}_original.json').read_text()));selected={r['sector']:{'value':r['value'],'flag':r['flag']} for r in rows if r['worktime']=='TOT_FTE' and r['sex']=='T'}
  assert selected['TOT_SEC']['value']=={2023:19586,2024:19825}[year]
  assert selected['PRV_IND']['value'] is None and selected['PRV_IND']['flag']=='m'
  selected['published_public_private_sum_minus_total']=selected['PUB']['value']+selected['PRV']['value']-selected['TOT_SEC']['value'];teachers[str(year)]=selected
 w=load_workbook(D/'FI_annexIII_original.xlsx',read_only=True,data_only=True);cell=w['15.2.2']['F10'].value
 assert 'The new estimate is based' in cell and 'other variables than full-time/part-time participation and FTE numbers' in cell
 assert w['18.1']['B29'].value=='Employment statistics/register data of Statistics Finland.'
 pupils=decode(json.loads((D/'FI_11c4_students_original.json').read_text()));counts={r['timeperiod_y']:r['value'] for r in pupils}
 assert counts=={'2022':17789,'2023':18177,'2024':18661}
 for r in pupils:assert r['alue_23_20250101']=='KU091' and r['ksektori_4_20150101']=='20' and r['contentscode']=='op_4a'
 prior=R/'data/task4_v147_education_refresh/helsinki_2025_original.pdf'
 text=subprocess.check_output(['pdftotext','-layout','-f','158','-l','158',str(prior),'-'],text=True)
 assert re.search(r'2022\s+55 579\s+18 177',text) and re.search(r'2023\s+59 581\s+18 177',text)
 result=dict(iteration='V163',status='New sources reviewed; no city teacher envelope admitted',national_teacher_FTE=teachers,
  teacher_selection=dict(dataset='educ_uoe_perp02',geo='FI',isced11='ED3',sex='T',worktime='TOT_FTE',unit='NR'),
  municipal_students=dict(dataset='11c4',region_code='KU091',region_classification='2025',sector='20 general upper secondary education',measure='op_4a Students total',reference='20September of the statistical year; qualification-syllabus students',counts=counts,geography='Location of education, not residents'),
  authoritative_variable_specific_method=dict(workbook='FI_annexIII_original.xlsx',cell='15.2.2!F10',cell_text_sha256=hashlib.sha256(cell.encode()).hexdigest(),short_evidence='other variables than full-time/part-time participation and FTE numbers',conclusion='Full-time/part-time and FTE figures use estimation from wage/salary and private-provider sources; not only untransformed register totals'),
  yearbook_comparison=dict(reused_file=str(prior.relative_to(R)),sha256=sha(prior),pdf_page=158,year_2022=18177,native_API_year_2022=17789,year_2023=18177,native_API_year_2023=18177,reason_for_2022_difference_not_inferred=True),
  failed_bound_reason='Published national FTE estimate has no verified one-sided error envelope, so national estimate >= actual Helsinki target FTE is not established; adding an arbitrary rounding unit does not bound estimation error',
  temporal_rule='API time, UOE collection year, school-year start/end and census date must be distinguished; no2025 transfer assumed',
  national_teacher_upper_superset_verified=False,city_PTR_bound=None,observations=[],primary_data_admissions=0,primary_score_width_change=0,current_model='V154 unchanged',current_paper='V160 unchanged',
  source_sha256={r['file']:r['sha256'] for r in receipts},extractor_sha256=sha(Path(__file__)))
 (D/'scope_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'teacher_FTE_2024':teachers['2024']['TOT_SEC'],'students':counts,'bound_admitted':False},indent=2))
if __name__=='__main__':main()
