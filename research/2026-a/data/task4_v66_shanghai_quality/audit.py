"""Verify the official PDF and the year/scope that prevent mismatched admission."""
import hashlib,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
for item in json.loads((P/'manifest.json').read_text()):
    b=(P/item['file']).read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(P/'quality2025.pdf'),'-']).decode()
pages=text.split('\f')
compact=lambda s:re.sub(r'\s+','',s)
assert '2024年在校生数为9.59万人' in compact(pages[14])
assert '独立设置且招生' in compact(pages[13]) and '53所' in compact(pages[13])
assert '53所普通全日制中职学校' in compact(pages[61])
assert '1.4师资队伍' in compact(pages[24])
result=dict(pdf_pages=121,reported_student_year=2024,reported_student_count_ten_thousands=9.59,
    reporting_school_year=2025,reporting_schools=53,
    population='independently established, recruiting ordinary full-time secondary vocational schools',
    page_references_1based=dict(student_year=15,school_scope=[14,62],staff_section=25),
    new_admitted_model_cells=0,main_admitted=False,
    reason='No verified same-year full-city current upper-secondary student/teacher pair; retain existing bounds')
(P/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: original PDF hash, 2024 student year and restricted 53-school reporting scope')
