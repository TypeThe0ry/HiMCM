"""Verify new school originals without promoting programme labels to cohort data."""
from pathlib import Path
from pypdf import PdfReader
import hashlib,json
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
    raw=(P/r['file']).read_bytes()
    assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
reader=PdfReader(P/'arch_newsletter.pdf')
assert len(reader.pages)==10 and 'Fall 2024' in reader.pages[0].extract_text()
text=' '.join(reader.pages[8].extract_text().split())
assert 'micro-school within the larger campus' in text
maryvale=(P/'maryvale_gifted.html').read_text()
assert 'school within a school at Maryvale High School' in maryvale
assert 'Admissions For the 2024-2025 School Year' in maryvale
notes=json.loads((P/'methodology_search_notes.json').read_text())
assert notes['full_original_acquired'] is False and notes['numeric_admission'] is False
summary={'new_originals':2,'arch_newsletter_year':2024,'arch_pdf_page':9,'maryvale_school_within_school_explicit':True,'arch_micro_school_within_campus_explicit':True,'cohort_unique_membership_proved':False,'teacher_allocation_proved':False,'numeric_observations_admitted':0,'methodology_minutes_originals_acquired':False}
(P/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
