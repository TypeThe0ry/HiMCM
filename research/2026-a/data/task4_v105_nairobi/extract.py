"""Verify new KNBS aggregates; no county numerator/denominator imputation."""
from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as E
P=Path(__file__).resolve().parent
source=P/'KNBS2026_Education_Training.xlsx'
m=json.loads((P/'manifest.json').read_text());assert hashlib.sha256(source.read_bytes()).hexdigest()==m['sha256']
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(source) as z:
    strings=[''.join(x.itertext()) for x in E.fromstring(z.read('xl/sharedStrings.xml'))]
    def cells(n):
        d={}
        for c in E.fromstring(z.read(f'xl/worksheets/sheet{n}.xml')).findall('.//m:c',N):
            v=c.find('m:v',N)
            if v is not None:d[c.attrib['r']]=strings[int(v.text)] if c.get('t')=='s' else v.text
        return d
    student,teacher=cells(10),cells(13)
    assert 'Secondary Schools' in student['A1'] and student['AF3']=='2025*'
    assert 'Teacher Training Colleges' in teacher['A1'] and teacher['W3']=='2025*'
    assert float(teacher['Y8'])==sum(float(teacher[f'Y{i}']) for i in [5,6,7])==131501
    assert abs(sum(float(student[f'AH{i}']) for i in [6,7,8])-float(student['AH9']))<1e-6
    assert 'AH5' not in student
    out={'edition':2026,'data_year':2025,'provisional':True,'geography':'Kenya national','secondary_enrolment_thousands':float(student['AH9']),'enrolment_cell':'Table 15.8!AH9','Form1_2025_cell_status':'blank; not imputed zero','public_secondary_and_teacher_training_college_teacher_headcount':int(teacher['Y8']),'teacher_cell':'Table 15.11!Y8','teacher_scope_note':teacher['A12'],'FTE_established':False,'Nairobi_same_year_pair_available':False,'main_model_admission':False,'Nairobi_main_interval_retained':[0,1]}
(P/'summary.json').write_text(json.dumps(out,indent=2)+'\n')
print('Original hash, year headers, and national sums verified. No Nairobi ratio computed.')
