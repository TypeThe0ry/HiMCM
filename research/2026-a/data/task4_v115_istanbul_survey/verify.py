from pathlib import Path
import csv,json,hashlib
P=Path(__file__).resolve().parent
s=json.loads((P/'audit.json').read_text())
source=P/s['source_file']
assert hashlib.sha256(source.read_bytes()).hexdigest()==s['source_sha256']
rows=list(csv.DictReader((P/'page_scan.csv').open()))
assert [int(r['pdf_page']) for r in rows]==list(range(1,127))
assert sum(int(r['ocr_characters'])>0 for r in rows)==s['ocr_nonempty_pages']
for key,value in s['keyword_counts'].items():
    assert sum(int(r[key]) for r in rows)==value
assert not s['admitted'] and s['new_model_observations']==0 and s['travel_interval']==[0,1]
result=dict(status='passed',source_unchanged=True,pages_indexed=126,ocr_nonempty_pages=s['ocr_nonempty_pages'],new_admitted_observations=0,scope='Saved OCR coverage and source integrity, not proof that OCR detects every possible field. Targeted rendered pages support the substantive limitations.')
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
