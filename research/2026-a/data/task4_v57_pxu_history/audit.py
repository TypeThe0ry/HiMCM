"""Verify V57 programme evidence without changing cohort or city bounds."""
from pathlib import Path
import hashlib
import json
import subprocess

HERE = Path(__file__).resolve().parent
for item in json.loads((HERE / 'manifest.json').read_text()):
    raw = (HERE / item['file']).read_bytes()
    assert len(raw) == item['bytes'], item['file']
    assert hashlib.sha256(raw).hexdigest() == item['sha256'], item['file']
html = (HERE / 'specialty_schools.html').read_text()
assert 'graduate as part of the larger campus class' in html
assert 'Camelback Montessori and Maryvale Gifted and Talented Academy' in html
assert 'concurrently' in html and 'their' in html
application = subprocess.check_output(['pdftotext', '-layout', str(HERE / 'pxu_city_application2023_24.pdf'), '-'], text=True)
assert '2023-2024 Application for Enrollment' in application
assert 'in-person and online from any PXU campus' in application
assert '3839 W. Camelback Rd' in application
rows = json.loads((HERE / '../task4_v9_phoenix/school_outcomes/1001158.json').read_text())
all_rows = [r for r in rows if r['studentGroupDescription'] == 'All']
assert len(all_rows) == 1
row = all_rows[0]
assert row['fiscalYear'] == 2025 and row['educationOrganizationId'] == 1001158
assert row['numInCohort'] == 56 and row['numGraduated'] == -11 and row['gradRate'] == -11
out = {'verified_source_files': 5, 'pxu_city_existing_cohort': 56,
       'pxu_city_graduate_count_suppressed': True,
       'new_exclusion_applied': False, 'additional_exclusion_cap_identified': False,
       'city_bound_changed': False, 'main_admitted': False,
       'micro_graduation_guidance_is_current_not_cohort2024_extract': True}
(HERE / 'audit.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out))
