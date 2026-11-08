"""Verify primary CRDC instruments; no empty form field becomes an observation."""
import csv,hashlib,json
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent

def audit():
    for r in json.loads((P/'manifest.json').read_text()):
        b=(P/r['file']).read_bytes();assert b.startswith(b'%PDF')
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
    form=PdfReader(P/'school_form2023_24.pdf');elements=PdfReader(P/'elements2023_24.pdf')
    assert len(form.pages)==133 and len(elements.pages)==14
    text=lambda r,i:' '.join(r.pages[i-1].extract_text().split())
    dates=text(form,61);fte=text(form,62);fields=text(form,63);overview=text(elements,14)
    assert 'entire regular school year' in dates and 'not including intersession or summer' in dates
    assert 'Do not report a “0” for data not collected' in dates
    assert 'Leave a field blank if the LEA does not know' in dates
    assert 'full-time equivalency of assignment' in fte and 'hundredths place' in fte
    assert 'STAF-1:' in fte and 'preschool and grades K-12' in fte
    assert 'Total number of full-time equivalent (FTE) teachers' in fields
    assert 'Number of teachers (preschool-12) employed' in overview
    prior=P.parent/'task4_v85_phoenix_public/missing_staff_records.csv'
    with prior.open(newline='') as f:missing=list(csv.DictReader(f))
    assert len(missing)==104 and len({r['NCESSCH'] for r in missing})==104
    result=dict(primary_instrument_pages=dict(school_form=133,elements=14),staff_module_pdf_pages=[61,62,63],
        target_field='STAF-1 total FTE teachers; PUF variable name/codes not yet verified',
        period='Entire regular 2023-24 school year, excluding intersession and summer',
        unit='Assignment FTE, two decimal places; not race/sex teacher headcount',
        stage='Preschool, K-12 and comparable ungraded; secondary assignment not separately identified',
        current_v85_missing_school_fte_records=len(missing),
        current_v85_strict_hs_only_missing_records=sum(r['strict_hs_only']=='True' for r in missing),
        current_v85_missing_roster_sha256=hashlib.sha256(prior.read_bytes()).hexdigest(),
        new_observed_teacher_values=0,main_admitted=False,admitted_cells_changed=0,
        next_gate='Obtain actual 2023-24 PUF staff and school-characteristic files plus NCES crosswalk/reserve-code manual, match dates and roles before any CCD replacement.')
    (P/'audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    return result

if __name__=='__main__':audit()
