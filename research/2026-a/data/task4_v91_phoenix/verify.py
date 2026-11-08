import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
for name,info in json.loads((p/'manifest.json').read_text()).items():
 b=(p/name).read_bytes();assert len(b)==info['bytes'] and hashlib.sha256(b).hexdigest()==info['sha256']
a=json.loads((p/'audit.json').read_text());f=a['frontend_endpoint_discovery'];assert hashlib.sha256((p/f['file']).read_bytes()).hexdigest()==f['sha256']
y=json.loads((p/'fiscal_years.json').read_text());assert [r['fiscalYear'] for r in y]==a['advertised_fiscal_years'];assert [r['fiscalYear'] for r in y if r['activeFiscalYear']]==[2025]
t=(p/'af_business_rules_2025.txt').read_text();assert 'Includes both FAY and non-FAY students' in t;assert 'cohort 2024' in t and 'cohort 2023' in t
assert 'getFiscalYearsList:function' in (p/f['file']).read_text()
print('Verified official fiscal-year metadata and linked A-F rules text export')
