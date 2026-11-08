"""Verify actual directory-vintage change; never backfill suppressed membership."""
from pathlib import Path
import hashlib,json,re
from html import unescape
HERE=Path(__file__).resolve().parent

def text(name):
    return ' '.join(unescape(re.sub('<[^>]+>',' ',(HERE/name).read_text())).split())

def extract():
    for r in json.loads((HERE/'manifest.json').read_text()):
        b=(HERE/r['file']).read_bytes()
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    s=text('hope_school.html');d=text('hope_district.html')
    assert 'NCES School ID: 040386003535' in s
    assert 'Directory Information (2025-2026 school year)' in s
    assert 'Physical Address: 1938 E Apache Blvd Tempe' in s
    assert 'School Details (2024-2025 school year)' in s
    assert re.search(r'Total Students:\s*‡',s)
    assert re.search(r'Classroom Teachers \(FTE\):\s*4.00',s)
    assert 'NCES District ID: 0403860' in d
    assert 'District Details (2024-2025 school year;' in d
    assert re.search(r'Total Students:\s*‡',d)
    assert 'do not meet NCES data quality standards' in s and 'do not meet NCES data quality standards' in d
    rows=[]
    for ref in json.loads((HERE/'reused_sources.json').read_text()):
        f=HERE.parent/ref['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==ref['sha256']
        rows.extend(x['attributes'] for x in json.loads(f.read_text())['features'] if x['attributes']['NCESSCH']=='040386003535')
    assert len(rows)==1
    old=rows[0]
    assert old['LCITY']=='PHOENIX' and old['LSTREET1']=='6401 S 16TH ST'
    assert all(old[k]==-9 for k in ['MEMBER','G09','G10','G11','G12']) and old['FTE']==4
    result=dict(nces_school_id='040386003535',old_school_record_year=old['SURVYEAR'],old_physical_address='6401 S 16TH ST, PHOENIX',new_directory_year='2025-2026',new_physical_address='1938 E Apache Blvd, Tempe',membership_staff_year='2024-2025',school_membership_quality_suppressed=True,district_membership_quality_suppressed=True,school_teacher_fte=4.0,finite_school_student_upper_bound_obtained=False,geography_vintages_differ=True,main_admitted=False,interpretation='The newer directory cannot retrospectively remove the school from the archived 2024/25 physical-city roster. Both same-year school and district membership remain quality-suppressed; no finite containment cap was obtained.')
    (HERE/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
if __name__=='__main__':print(json.dumps(extract(),indent=2))
