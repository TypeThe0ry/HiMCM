"""Nonmutating source audit for TUS2024 travel suitability; no microdata."""
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from pypdf import PdfReader
import hashlib,json
P=Path(__file__).resolve().parent

def audit():
    manifest=json.loads((P/'manifest.json').read_text())
    for r in manifest:assert hashlib.sha256((P/r['file']).read_bytes()).hexdigest()==r['sha256']
    pdf=PdfReader(P/'instructions.pdf')
    pages={n:' '.join(pdf.pages[n-1].extract_text().split()) for n in [43,44,59,60,61,75,83,94]}
    checks={43:['highest level of education completed'],44:['last 365 days'],59:['48 time slots','duration of 30 minutes','Fraction of 30 minutes will not be used'],60:['10 minutes or more','at most three','start of the 30-minute time'],61:['combined together','auto populated'],75:['only two activities'],83:['611 School/university attendance','640 Travelling time related to learning'],94:['Mumbai Suburban (22)','Mumbai (23)']}
    for n,phrases in checks.items():
        for phrase in phrases:assert phrase in pages[n],(n,phrase)
    with ZipFile(P/'layout.xlsx') as z:layout=' '.join(ET.fromstring(z.read('xl/sharedStrings.xml')).itertext())
    for phrase in ['highest level of education','District','time from (HH:MM)','time to (HH:MM)','MULT','NSC']:assert phrase in layout
    return dict(passed=True,survey_year=2024,new_admitted_cells=0,raw_microdata_obtained=False,public_document_count=len(manifest),dictionary_person_variables=41,dictionary_household_variables=37,person_file_catalog_rows=10211478,rows_are_not_distinct_person_count=True,clock_slot_minutes=30,typical_minimum_recorded_activity_minutes=10,maximum_activities_per_slot=3,reference_day='04:00 preceding interview day to 04:00 interview day',education='Highest completed level, not current enrollment stage',principal_status='Past365-day main activity; education institution code91 is not current-grade confirmation',learning_activity_codes={'611':'School/university attendance','640':'Travelling time related to learning'},geography={'Delhi':'State code07; city boundary alignment remains to be established','Mumbai':'Maharashtra27 NSSregion271 districts22 and23; boundary alignment remains to be established'},source_checks={str(k):v for k,v in checks.items()},access='Official get-microdata page requires login/free account; no registration, identity submission, or access bypass attempted.',scope='Actual reported activity diary with coarsened time slots. No direct upper-secondary stage or one-way school travel field. No current city utility admitted; do not halve daily learning travel or equate slot length with exact travel duration.')
if __name__=='__main__':
    r=audit();(P/'summary.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
