"""Verify district-hosted AFR, preserving year/snapshot distinctions."""
from pathlib import Path
import hashlib,json
from pypdf import PdfReader
P=Path(__file__).resolve().parent
for r in json.loads((P/'manifest.json').read_text()):
 b=(P/r['file']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
assert '/s/2025-AFR-Board-Docs-gdbj.pdf' in (P/'governance.html').read_text()
pages=[' '.join(p.extract_text().split()) for p in PdfReader(P/'afr2025.pdf').pages]
assert '070199000' in pages[9]
assert 'Number of FTE-certified teachers 9' in pages[9]
assert 'Number of FTE-contract teachers 39' in pages[9]
assert '2025' in pages[9]
assert '1,145.5429' in pages[12] and 'Avg. Daily Membership' in pages[12]
assert not any('1,180' in p or '1180' in p for p in pages)
result=dict(source='District FY2025 Annual Financial Report',district_ctds='070199000',
 certified_teacher_fte=9,contract_teacher_fte=39,source_pdf_page=10,
 arithmetic_sum=48,assignment='District finance report categories; not reconciled to fall CCD4 FTE or individual school assignments',
 adm=1145.5429,adm_pdf_page=13,adm_is_fall_headcount=False,
 fall_2024_headcount_1180_verified_in_this_original=False,
 hope_inclusion_in_fall_headcount_verified=False,main_admitted=False,
 limitation='No October1 enrollment ceiling established. Teacher category definitions and end-of-year snapshot require reconciliation before any bound use; categories retained individually.')
print(json.dumps(result,indent=2))
