"""Offline verification of acquired provider coverage documentation."""
import hashlib
import json
import re
from pathlib import Path
from pypdf import PdfReader

P = Path(__file__).resolve().parent


def main():
    manifest = json.loads((P/'manifest.json').read_text())
    for row in manifest:
        data = (P/row['file']).read_bytes()
        assert len(data) == row['bytes']
        assert hashlib.sha256(data).hexdigest() == row['sha256']
        assert data.startswith(b'%PDF')
    reader = PdfReader(P/'edc_technical_documentation_v3_1.pdf')
    text = re.sub(r'\s+', ' ', reader.pages[6].extract_text())
    assert len(reader.pages) == 59
    assert 'SADR currently limits data to Grades 3-8.' in text
    checks = json.loads((P/'access_checks.json').read_text())
    for row in checks[:2]:
        assert row['status'] == 403 and row['bytes'] == 4551
        assert row['content_type'].startswith('text/html')
    summary = dict(main_admitted=False, original_documents_acquired=len(manifest),
        coverage_document_pages=59, provider_scope='Grades 3-8', grade11_records_added=0,
        fy2025_assessment_workbooks_acquired=False, model_cells_changed=0,
        raw_pdf_hash_verified=True)
    (P/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
