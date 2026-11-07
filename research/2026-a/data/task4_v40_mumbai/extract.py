"""Verify published school-category totals; no grade-specific city admission."""
import hashlib,json,re,csv
from pathlib import Path
P=Path(__file__).resolve().parent
for m in json.loads((P/'manifest.json').read_text()):
    raw=(P/m['file']).read_bytes()
    assert len(raw)==m['bytes'] and hashlib.sha256(raw).hexdigest()==m['sha256']
records=[]
for name,schools,teachers,boys,girls,page in [('city',50,1074,27671,29854,118),('suburban',116,3767,104436,102262,104)]:
    text=(P/f'{name}2025.txt').read_text().split('\f')[page-1]
    assert '8.3' in text and '2024-25' in text
    pattern=r'\s+'.join(map(str,[schools,teachers,boys,girls,schools]))
    assert re.search(pattern,text), 'Published total row not found'
    records.append(dict(district=name,reference_year='2024/25',table='8.3',pdf_page=page,
        reported_schools=schools,reported_teachers=teachers,boys=boys,girls=girls,
        pupils=boys+girls,reported_category_pupils_per_teacher=(boys+girls)/teachers,
        main_admitted=False))
with (P/'reported_category_totals.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
print(json.dumps(records,indent=2))
