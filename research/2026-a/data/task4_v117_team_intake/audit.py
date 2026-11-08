"""Read-only CSV audit. Outputs audit artifacts; never edits submitted CSV."""
from pathlib import Path
import csv,json,hashlib
from decimal import Decimal
P=Path(__file__).resolve().parent
SOURCE=P/'city_indicators.csv'
FIELDS=['homicide_per_100k','pm25_ugm3','cli','pir','pupil_teacher_ratio','he_per_million','transit_share_pct','commute_min','broadband_mbps','pools_per_100k','early_leavers_pct']
def run():
 before=hashlib.sha256(SOURCE.read_bytes()).hexdigest()
 rows=list(csv.DictReader(SOURCE.open(encoding='utf-8-sig',newline='')))
 issues=[];counts={}
 def add(city,field,issue,reported='',computed='',detail=''):
  issues.append(dict(city=city,field=field,issue=issue,reported=reported,computed=computed,detail=detail))
 for r in rows:
  city=r['city'];pop=Decimal(r['population'])
  for field,num,scale in [('homicide_per_100k','homicide_numerator',100000),('pools_per_100k','pool_count',100000),('he_per_million','he_count',1000000)]:
   if r[field] and r[num]:
    value=Decimal(r[num])*scale/pop; shown=Decimal(r[field]);tol=Decimal(10)**shown.as_tuple().exponent/2
    if abs(value-shown)>tol:
     add(city,field,'not_reproducible_from_supplied_population',r[field],str(value),'Not proof of source error: an unreported historical/geographic denominator may differ. Source denominator required.')
    if r[field+'_year']!=r['population_year']:add(city,field,'reference_year_mismatch',r[field+'_year'],r['population_year'],'Rate year differs from supplied population year.')
  present=sum(bool(r[f]) for f in FIELDS)
  usable=sum(bool(r[f]) and r[f+'_flag'] not in {'NA','STALE','SUSPECT','NATIONAL'} for f in FIELDS)
  if present!=int(r['indicators_present']):add(city,'indicators_present','count_mismatch',r['indicators_present'],present)
  if usable!=int(r['usable_present']):add(city,'usable_present','flag_count_mismatch',r['usable_present'],usable)
  counts[city]={'present':present,'flag_usable_count':usable}
  for f in ('transit_share_pct','commute_min','early_leavers_pct'):
   if r[f]:add(city,f,'not_directly_mappable',r[f],detail={'transit_share_pct':'Mode share is not physical stop density.','commute_min':'Mean commute is not current-high-school one-way journey-time distribution.','early_leavers_pct':'Not one of the current ten indicators; not PTR.'}[f])
 add('ALL','source','missing_source_urls',detail='No source URLs, title/table/cell, denominator lineage or extraction methods. ok flags are contributor labels, not validation.')
 add('Tokyo','pupil_teacher_ratio','verified_wrong_stage','15.22','15.65','Statistics Bureau2026 PDFp62 printedp38: 15.22 lower secondary;15.65 upper secondary. Both Tokyo-to FY2024, not23wards. Correct value remains candidate pending teacher scope review.')
 add('Singapore','pupil_teacher_ratio','verified_whole_secondary','12.7',detail='MOE ESD2025 tableB printedxvi:2024wholeSecondary; cannot isolateupper-secondary.')
 add('Singapore','broadband_mbps','verified_mean_not_median','667.71','476.02','ExistingV100 originalOokla JSON audit identifies667.71asfixedMean and476.02asfixedMedian of samegroup.')
 add('Tokyo','population','geography_mismatch','9983365',detail='Contributor23ward city geography differs from modelTokyo-to. Do not apply23warddenominator to Tokyo-to numerator.')
 with (P/'issues.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['city','field','issue','reported','computed','detail'],lineterminator='\n');w.writeheader();w.writerows(issues)
 out={'rows':len(rows),'columns':len(rows[0]),'source_sha256':before,'candidate_overlap':['London','Warsaw','Singapore','Tokyo'],'new_out_of_sample_cities':sorted({r['city'] for r in rows}-{'London','Warsaw','Singapore','Tokyo'}),'rate_arithmetic_mismatches':sum(x['issue']=='not_reproducible_from_supplied_population' for x in issues),'counts':counts,'issues_total':len(issues),'automatic_model_admissions':0}
 (P/'audit_summary.json').write_text(json.dumps(out,indent=2)+'\n')
 assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==before
 print(json.dumps(out,indent=2))
if __name__=='__main__':run()
