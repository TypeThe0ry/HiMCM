"""Inspect historical identity evidence; do not admit new city observations."""
import csv,hashlib,importlib.util,json
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v75',P.parent/'task4_v75_athens/extract.py')
v75=importlib.util.module_from_spec(spec);spec.loader.exec_module(v75)
for r in json.loads((P/'manifest.json').read_text()):
    if 'file' not in r:continue
    raw=(P/r['file']).read_bytes()
    assert len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256']
for name,page in [('school_codes2014.pdf',0),('school_codes2020.pdf',9)]:
    t=PdfReader(P/name).pages[page].extract_text()
    assert '551010' in t and '551040' in t
mapping={
 '540752':'10ο ΗΜΕΡΗΣΙΟ ΕΠΑ.Λ. ΑΘΗΝΩΝ',
 '551010':'2ο ΠΕΙΡΑΜΑΤΙΚΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΘΗΝΑΣ',
 '551040':'1ο ΠΕΙΡΑΜΑΤΙΚΟ ΓΕΝΙΚΟ ΛΥΚΕΙΟ ΑΘΗΝΩΝ - ΓΕΝΝΑΔΕΙΟ'}
students=v75.load('minedu_students_school');directory=v75.load('minedu_schools');out=[]
for code,name in mapping.items():
    ds=[r for r in directory if r['school_code']==code];assert len(ds)==1
    for year in ['2018','2019']:
        ss=[r for r in students if r['year']==year and r['school_name']==name];assert len(ss)==1
        r=ss[0]
        out.append(dict(candidate_school_code=code,source_year_label=year,student_name=name,directory_name=ds[0]['school_name'],student_type=r['school_type'],directory_type=ds[0]['school_subtype'],boys=int(r['registered_students_boys']),girls=int(r['registered_students_girls']),pupils=int(r['registered_students_boys'])+int(r['registered_students_girls']),status='identity_supported_across_2014_2020_but_contemporaneous_original_missing' if code!='540752' else 'abbreviation_crosswalk_unverified',admitted=False))
with (P/'candidate_rows.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]),lineterminator='\n');w.writeheader();w.writerows(out)
result=dict(new_admitted_cells=0,academic_year_mapping_verified=False,directory_reference_year_known=False,retained_v75_punctuation_linked_schools=48,originals_downloaded=2,identity_supported_codes=['551010','551040'],unverified_abbreviation_code='540752',candidate_pupils_by_source_label={year:sum(r['pupils'] for r in out if r['source_year_label']==year) for year in ['2018','2019']},core_bounds_changed=False)
(P/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
