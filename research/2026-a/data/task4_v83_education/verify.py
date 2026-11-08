"""Verify selected reader transcription arithmetic, not underlying PDF authenticity."""
from pathlib import Path
import json, hashlib
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
    raw=(P/r['file']).read_bytes()
    assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
d=json.loads((P/'reader_observations.json').read_text());t=d['tables']
a,b=t['III.2_printed111'],t['III.3_printed112']
assert sum(a['public_form1_4_sex_cells'])==a['public_total']
assert sum(b['private_form1_4_sex_cells'])==b['private_total']
z=t['III.8_printed117'];r=t['III.9_printed118']
for name in ['public_tsc','public_bom','private']: assert sum(z[name+'_by_sex'])==z[name]
assert z['public_tsc']==r['public'] and z['private']==r['private']
assert r['public']+r['private']==r['all']
n=a['public_total']+b['private_total'];teachers=sum(z[k] for k in ['public_tsc','public_bom','private'])
assert (n,teachers,r['all'])==(106965,5465,4759)
result=dict(enrollment_total=n,teacher_category_sum=teachers,published_ptr_teacher_total=r['all'],excluded_bom=teachers-r['all'],arithmetic_ptr_published_definition=n/r['all'],arithmetic_ptr_all_reported_categories=n/teachers,main_admitted=False,interpretation='Arithmetic diagnostics only; private coverage gaps and estimated inputs have no error bounds')
(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
