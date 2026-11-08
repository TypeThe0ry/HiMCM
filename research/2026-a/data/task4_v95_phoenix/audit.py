"""Verify definition provenance and unchanged grade11 source semantics offline."""
import csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent
D=P.parent

def main():
 for f,h in json.loads((P/'reused_sources.json').read_text()).items():
  assert hashlib.sha256((D/f).read_bytes()).hexdigest()==h
 for r in json.loads((P/'manifest.json').read_text()):
  b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 text=(D/'task4_v91_phoenix/af_business_rules_2025.txt').read_text()
 for phrase in ['ACT ELA scores are the average','valid score on all 3','Cohort 2026','FAY at more than one school','not a measure of the percentage of students who were proficient','April 8, 2024']:
  assert phrase in text,phrase
 files=['task4_v92_phoenix/verified_grade11_observations.csv','task4_v93_phoenix/grade11_observations.csv','task4_v94_phoenix/grade11_observations.csv']
 rows=[]
 for f in files:
  with (D/f).open() as inp:rows+=list(csv.DictReader(inp))
 assert len(rows)==319 and len({(r['nces_id'],r['subject']) for r in rows})==319
 assert all(r['fiscalYear']=='2025' and r['grade']=='11' and r['fayType']=='ALL ENROLLED' and r['type']=='1' and r['subgroups']=='All' for r in rows)
 extreme=sum(float(r['percentagePassed']) in [0,1,99,100] for r in rows if r['percentagePassed'])
 assert extreme==0
 result=dict(main_admitted=False,source_rows_checked=319,source_schools=len({r['nces_id'] for r in rows}),api_brand_crosswalk_verified=False,rounding_verified=False,exact_suppression_codes_verified=False,extreme_display_percent_rows=extreme,public_performance_denominator_not_replaced=True,accountability_programme_verified_from_sameyear_rules=True,source_date_inconsistency_preserved=True)
 (P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
