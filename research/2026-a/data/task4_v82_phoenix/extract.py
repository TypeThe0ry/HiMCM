"""Cross-check a same-year NCES district total against previously archived school records."""
from pathlib import Path
import hashlib, json, csv, re
from html import unescape
from decimal import Decimal
HERE=Path(__file__).resolve().parent

def extract():
    for r in json.loads((HERE/'manifest.json').read_text()):
        raw=(HERE/r['file']).read_bytes()
        assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
    text=unescape(re.sub('<[^>]+>',' ',(HERE/'nces_district.html').read_text()))
    text=' '.join(text.split())
    assert '2024-2025' in text and '0406330' in text
    assert re.search(r'Total Students:\s*25,800',text)
    assert re.search(r'Classroom Teachers \(FTE\):\s*1,349.60',text)
    rows=[]
    for ref in json.loads((HERE/'reused_sources.json').read_text()):
        f=HERE.parent/ref['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==ref['sha256']
        rows.extend(x['attributes'] for x in json.loads(f.read_text())['features'] if x['attributes']['LEAID']=='0406330')
    assert len(rows)==21 and len({r['NCESSCH'] for r in rows})==21
    assert all(r['MEMBER']>=0 for r in rows)
    assert sum(r['MEMBER'] for r in rows)==25800
    known=[r for r in rows if r['FTE']>=0];missing=[r for r in rows if r['FTE']<0]
    total=sum(Decimal(str(r['FTE'])) for r in known)
    assert total==Decimal('1349.60')
    assert len(missing)==1 and missing[0]['NCESSCH']=='040633003806' and missing[0]['MEMBER']==0
    virtual=[r for r in rows if r['VIRTUAL']=='Full Virtual']
    assert len(virtual)==1 and virtual[0]['NCESSCH']=='040633003578'
    assert virtual[0]['MEMBER']==70 and Decimal(str(virtual[0]['FTE']))==Decimal('27.8')
    subset=[r for r in known if r['VIRTUAL']=='Not Virtual']
    n=sum(r['MEMBER'] for r in subset);t=sum(Decimal(str(r['FTE'])) for r in subset)
    assert (len(subset),n,t)==(19,25730,Decimal('1321.8'))
    with (HERE/'school_crosscheck.csv').open('w',newline='') as f:
        cols=['NCESSCH','SCH_NAME','SURVYEAR','MEMBER','FTE','VIRTUAL'];w=csv.DictWriter(f,cols,lineterminator='\n');w.writeheader();w.writerows({k:r[k] for k in cols} for r in rows)
    report=dict(district='Phoenix Union High School District',nces_leaid='0406330',membership_staff_year='2024-2025',directory_year='2025-2026',district_students=25800,district_classroom_teacher_fte=1349.6,district_reported_ratio=19.12,district_resource_utility=float(15*total/(Decimal(25800)+15*total)),district_computed_ratio=float(Decimal(25800)/total),school_records=21,known_staff_school_records=20,known_staff_fte_sum=float(total),school_membership_matches_district=True,known_school_fte_matches_district=True,missing_fte_school=missing[0]['NCESSCH'],missing_fte_sentinel=-1,missing_fte_school_students=0,nonvirtual_known_staff_subset=dict(schools=19,students=n,teacher_fte=float(t)),main_admitted=False,limitation='District is not whole Phoenix. Known school FTE sum matches rounded published district total; this does not convert missing school FTE into an observed zero. Teacher and student figures are not restricted to ages14-18; virtual and private coverage differ from city target.')
    (HERE/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
if __name__=='__main__': print(json.dumps(extract(),indent=2))
