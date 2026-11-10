"""Inspect archived NCSE allocation schema; never convert posts to employed FTE."""
from pathlib import Path
import csv,hashlib,io,json
O=Path(__file__).resolve().parent
receipts=json.loads((O/'retrievals.json').read_text())
for r in receipts:
 if r.get('sha256'):
  p=O/r['file']; assert p.stat().st_size==r['bytes']
  assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
rows=list(csv.DictReader(io.StringIO((O/'ncse_postprimary_allocations_original.csv').read_bytes().decode('cp1252'))))
assert len(rows)==722 and sum(r['County']=='Dublin' for r in rows)==183
out=dict(version='V194 Dublin source scope',routes=2,successful_original_responses=4,ncse=dict(encoding='cp1252 decoding (UTF-8 fails at byte754)',records=722,county_dublin_records=183,columns=list(rows[0]),reference_period='2024/2025',catalog_updated='2024-08-01',geographic_unit='County plus Dublin postal area codes; not a verified city-boundary join',measurement='Special-education hours/posts and SNA allocations; not total employed teaching FTE',admissible=False,reason='Allocated posts do not establish filled teaching workload. No total teacher or pupil counts, ISCED3 split or validated city-scope join.'),workforce_methodology=dict(catalog_time_coverage='2015-2023',catalog_updated='06-02-2026',pdf_scope='Payroll and allocation counts; current-school-year bulletins; county/national publication',admissible=False,reason='Methodology document provides no matching city-level upper-secondary pupil/teacher numeric envelope. Catalog historical coverage and current-bulletin example are distinct.'),primary_admissions=0,actual_score_width_reduction=0,model_edited=False)
(O/'findings.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
