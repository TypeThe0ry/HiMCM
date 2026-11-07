#!/usr/bin/env python3
"""Audit source-labeled 2025 Dhaka madrasa upper-secondary subset bounds."""
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / 'task4_v59_secondary_sources/bangladesh_education2025.pdf'
EXPECTED = '14deea1e6379de7e6e9141f8bb8f2f4b713a772905cfdd1d99579ad7911010f8'
assert hashlib.sha256(RAW.read_bytes()).hexdigest() == EXPECTED
pages = subprocess.check_output(['pdftotext', '-layout', str(RAW), '-'], text=True).split('\f')
selected = {342:309,385:352,387:354,392:359,422:389}
(HERE/'source_extract.txt').write_text('\n\n'.join(f'PDF PAGE {p}; PRINTED PAGE {printed}\n{pages[p-1]}' for p, printed in selected.items()))
# Transcription checked against original tables. Institution type is NOT student stage.
# City values: Table5.1.10.1; national stage values: Tables5.3.5 and5.3.7.
rows = [
    dict(type='Dakhil',management='Private',city_students=7246,city_girls=3480,city_teachers=534,national_students=1434749,national_alim=1562,national_alim_girls=915),
    dict(type='Alim',management='Private',city_students=12332,city_girls=4288,city_teachers=572,national_students=494083,national_alim=94028,national_alim_girls=50931),
    dict(type='Fazil (pass and honours combined)',management='Private',city_students=2507,city_girls=775,city_teachers=131,national_students=3736+588959,national_alim=723+109162,national_alim_girls=516+57843),
    dict(type='Kamil',management='Private',city_students=24945,city_girls=7076,city_teachers=657,national_students=311513,national_alim=57661,national_alim_girls=21520),
    dict(type='Kamil',management='Public',city_students=3410,city_girls=0,city_teachers=50,national_students=7057,national_alim=1204,national_alim_girls=157),
]
# Confirm key source strings against pdftotext output, not only hardcoded arithmetic.
city=' '.join(pages[341].split())
for expected in ['534 215 40.26 7246 3480', '572 217 37.94 12332 4288', '131 48 36.64 2507 775', '657 261 39.73 24945 7076', '50 9 18.00 3410 0']:
    assert expected in city, expected
stage=' '.join(pages[384].split())
for expected in ['1076 620 486 295 1562 915', '667 89 537 68 1204 157']:
    assert expected in stage, expected
for r in rows:
    r['alim_lower']=max(0,r['city_students']-(r['national_students']-r['national_alim']))
    r['alim_upper_without_gender']=min(r['city_students'],r['national_alim'])
    r['alim_upper']=min(r['city_girls'],r['national_alim_girls'])+min(r['city_students']-r['city_girls'],r['national_alim']-r['national_alim_girls'])
assert sum(r['city_students'] for r in rows)==50440
assert sum(r['city_teachers'] for r in rows)==1944
assert sum(r['alim_upper'] for r in rows)==42393
assert sum(r['alim_lower'] for r in rows)==0
out={
 'source_label_year':2025,
 'geography':'Dhaka City Corporation as labeled by BANBEIS; not Dhaka district/division; north/south boundary mapping unverified',
 'population':'Alim grades11–12 enrolled in post-primary madrasas; not all ages14–18 residents',
 'date_caveat':'2025 publication tables; methods report survey collection20Oct2024–21Nov2024. Possible carry-forward typo unresolved.',
 'interpretation':'National margins constrain city subsets; no national-share imputation. Administrative teacher counts lack stage allocation and FTE definition.',
 'rows':rows,
 'added_alim_students_interval':[0,sum(r['alim_upper'] for r in rows)],
 'added_alim_students_interval_without_gender':[0,sum(r['alim_upper_without_gender'] for r in rows)],
 'added_teachers_interval':[0,sum(r['city_teachers'] for r in rows)],
 'remaining_scope':'General HSC+Alim remains incomplete for technical/vocational uppersecondary; no direct city-stage counts established.',
 'technical_national_only':{'source':'Table7.3 printed389/PDF422','higher_secondary_students':263578,'higher_secondary_teachers':11074,'mixed_technical_school_college_students':169462,'mixed_technical_school_college_teachers':7373},
}
(HERE/'audit.json').write_text(json.dumps(out,indent=2)+'\n')
manifest={'reuse_path':str(RAW.relative_to(HERE.parent.parent.parent.parent)), 'sha256':EXPECTED,'bytes':RAW.stat().st_size,'publisher':'BANBEIS','title':'Bangladesh Education Statistics2025','publication_page':'https://banbeis.gov.bd/pages/files/annual-education-statistics-2026-6iav4j-6abb61ee54b917a30a16991c','raw_url':'https://objectstorage.ap-dcc-gazipur-1.oraclecloud15.com/n/axvjbnqprylg/b/V2Ministry/o/office-banbeis/2026/8/3ad8a7f7-d233-4753-b8cc-7a6f69f4e80e.pdf','audit_date':'2026-11-07','original_unchanged':True,'pages':selected}
(HERE/'raw_reuse_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ('added_alim_students_interval','added_alim_students_interval_without_gender','added_teachers_interval')}))
