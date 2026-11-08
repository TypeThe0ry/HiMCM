"""Check saved provider text identity and the declared non-admission decision."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
source=P.parent/'task4_v116_tbmm/provider_extraction.json'
r=json.loads(source.read_text())
text='\n'.join(c['text'] for c in r['result']['content'] if c['type']=='text')
for phrase in ['7/34663','Istanbul ilinde eğitim gören','%36','%46','60 dakikayı aşan']:
    assert phrase in text, phrase
a=json.loads((P/'audit.json').read_text())
assert not a['admitted'] and a['new_model_observations']==0 and a['travel_interval']==[0,1]
result=dict(status='passed_saved_text_scope_checks',source_file=str(source.relative_to(P.parent)),
    provider_capture_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    extracted_text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    audit_sha256=hashlib.sha256((P/'audit.json').read_bytes()).hexdigest(),
    original_pdf_bytes_verified=False,independent_visual_ocr=False,
    limitation='Token checks verify source identity/anchors; scope interpretation is the documented human-readable audit, not a statistical completeness proof.')
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
