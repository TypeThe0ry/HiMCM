"""Verify two new primary originals and their limited geographic coverage."""
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader
HERE = Path(__file__).resolve().parent

def audit():
    manifest = json.loads((HERE/'manifest.json').read_text())
    for record in manifest:
        data = (HERE/record['file']).read_bytes()
        assert data.startswith(b'%PDF-')
        assert len(data) == record['bytes']
        assert hashlib.sha256(data).hexdigest() == record['sha256']
    pilot = PdfReader(HERE/'school_census_pilot2024.pdf')
    teachers = PdfReader(HERE/'teachers2025.pdf')
    assert len(pilot.pages) == 205 and len(teachers.pages) == 41
    text = ' '.join(pilot.pages[10].extract_text().split())
    match = re.search(r'Nairobi City Kibra Kibra ((?:\d+ ){6}\d+)', text)
    counts = list(map(int, match.group(1).split()))
    assert counts == [44, 51, 31, 11, 2, 0, 139]
    assert sum(counts[:-1]) == counts[-1]
    design = ' '.join(pilot.pages[9].extract_text().split())
    assert 'purposively' in design and 'purposefully selected zones' in design
    staff = ' '.join(pilot.pages[136].extract_text().split())
    assert all(term in staff for term in ('SF01:', '2023', '2024', 'TSC', 'BoM', 'Private School'))
    enrolment = ' '.join(pilot.pages[128].extract_text().split())
    assert all(term in enrolment for term in ('SD01:', '2023', 'Form 1', 'Form 4', 'Non-Kenyans'))
    national = ' '.join(teachers.pages[32].extract_text().split())
    match = re.search(r'Total 128960 55664 73296', national)
    assert match and 55664 + 73296 == 128960
    # Only addresses contain the literal Nairobi in this document; this is a
    # supporting check, not a general semantic proof of absent county tables.
    nairobi_pages = [i+1 for i,p in enumerate(teachers.pages) if 'Nairobi' in p.extract_text()]
    assert nairobi_pages == [5, 41]
    result = dict(pilot_pages=205, workforce_pages=41,
        pilot_nairobi_geography='Kibra subcounty / Kibra zone',
        pilot_nairobi_school_counts=dict(zip(['pre_primary','primary','junior','secondary','pre_vocational','international','total'],counts)),
        pilot_design='Purposive counties and zones; complete enumeration intended only within selected zones.',
        secondary_instrument_pdf_pages=dict(enrolment_2023=129,age_by_form_2023=130,staff_2023_2024=137),
        workforce_reference='June 2025; TSC-employed only',
        workforce_secondary_national_teachers=128960,
        workforce_nairobi_mentions_pdf_pages=nairobi_pages,
        workforce_scope_visual_check_pdf_page=16,
        main_admitted=False, admitted_cells_changed=0,
        reason='Pilot provides instruments and selected-zone school counts, not completed city pupil/staff data. Workforce audit gives national TSC totals, no Nairobi count; private and BoM teachers excluded.')
    (HERE/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    return result

if __name__ == '__main__':
    audit()
