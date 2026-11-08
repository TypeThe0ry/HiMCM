"""Rebuild same-year LEA coverage audit; never impute missing school teachers."""
import csv, io, json, zipfile
from collections import Counter
from decimal import Decimal
from pathlib import Path
P=Path(__file__).resolve().parent
S=P.parent/'task4_v85_phoenix_public'
def write(name,rows):
    with (P/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with zipfile.ZipFile(P/'ccd_lea_059_2324_l_1a_073124.zip') as z:
    assert z.testzip() is None
    rows=list(csv.DictReader(io.StringIO(z.read('ccd_lea_059_2324_l_1a_073124.csv').decode('utf-8-sig'))))
az=[r for r in rows if r['ST']=='AZ'];assert all(r['SCHOOL_YEAR']=='2023-2024' for r in az)
write('arizona_staff.csv',az)
missing=list(csv.DictReader((S/'missing_staff_records.csv').open()))
schools=[r['attributes'] for f in sorted(S.glob('arizona_page_*.json')) for r in json.loads(f.read_text())['features']]
assert len({r['NCESSCH'] for r in schools})==len(schools)
totals={r['LEAID']:r for r in az if r['STAFF']=='Teachers'}
audit=[]
for lea in sorted({r['LEAID'] for r in missing}):
    group=[r for r in missing if r['LEAID']==lea]; allschool=[r for r in schools if r['LEAID']==lea];t=totals[lea]
    known=sum((Decimal(str(r['FTE'])) for r in allschool if r['FTE'] is not None and r['FTE']>=0),Decimal(0))
    count=Decimal(t['STAFF_COUNT']) if t['STAFF_COUNT'] else None
    audit.append(dict(LEAID=lea,LEA_NAME=t['LEA_NAME'],school_year=t['SCHOOL_YEAR'],missing_target_schools=len(group),explicit_hs_pupils=sum(int(r['target_enrollment_lower']) for r in group),lea_teachers_fte=t['STAFF_COUNT'],lea_flag=t['DMS_FLAG'],all_az_school_records=len(allschool),all_az_known_school_fte=str(known),arithmetic_residual='' if count is None else str(count-known),admission='not_admitted_missing_lea' if count is None else 'not_admitted_allocation_scope_unverified'))
write('target_lea_audit.csv',audit)
write('target_lea_staff.csv',[r for r in az if r['LEAID'] in {x['LEAID'] for x in audit}])
valid=[r for r in audit if r['lea_teachers_fte']]
summary=dict(school_year='2023-2024',az_staff_rows=len(az),az_teacher_leas=len(totals),target_leas=len(audit),target_schools=len(missing),target_explicit_hs_pupils=sum(r['explicit_hs_pupils'] for r in audit),numeric_target_leas=len(valid),numeric_target_schools=sum(r['missing_target_schools'] for r in valid),numeric_target_explicit_hs_pupils=sum(r['explicit_hs_pupils'] for r in valid),missing_target_leas=len(audit)-len(valid),missing_target_schools=sum(r['missing_target_schools'] for r in audit if not r['lea_teachers_fte']),numeric_cases=valid,admitted_teacher_bounds=0)
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
