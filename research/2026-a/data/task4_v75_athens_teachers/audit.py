"""Verify ELSTAT web extraction; do not claim an acquired original PDF."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent

def audit():
    for row in json.loads((P/'manifest.json').read_text()):
        if 'file' in row:
            raw=(P/row['file']).read_bytes()
            assert hashlib.sha256(raw).hexdigest()==row['sha256']
            assert len(raw)==row['bytes']
    result=json.loads((P/'general2019_20_web_extract.json').read_text())
    assert result['kind']=='web_tool_extraction_not_original_pdf'
    text=result['result']
    assert 'END OF SCHOOL YEAR 2019/2020' in text
    block=text.split('Table 4. School units and teaching staff')[1].split('Table 5. Pupils enrolled')[0]
    m=re.search(r'Attiki 385 385 0\.0 ([\d,]+) ([\d,]+) 2\.3',block)
    assert m and tuple(int(x.replace(',','')) for x in m.groups())==(8628,8823)
    assert '23,652 23,914 1.1' in block
    assert 'Absent teachers are also included' in block
    assert 'Ecclesiastical Schools are not included' in text
    assert 'TOTAL 164 164 0.0' in text
    report=dict(main_admitted=False,original_pdf_acquired=(P/'general2019_20.pdf').exists(),evidence_kind='web-reader extraction of official ELSTAT PDF',school_years=['2018/2019','2019/2020'],attiki_general_lyceum_teachers=[8628,8823],national_general_lyceum_teachers=[23652,23914],national_ecclesiastical_lower_and_upper_teachers=[164,164],teacher_definition='Includes fixed-post teachers absent over20days or seconded elsewhere; not active teaching FTE.',scope='General lyceum public/private staff, not Athens municipal and not complete all-upper-secondary staff. Ecclesiastical combined-stage staff separate; vocational/special coverage not completed.',student_year_link_verified=False,admission='No teacher bound admitted until student referenceperiod and covered schooltypes are reconciled; numeric year2019 does not itself select2018/19 or2019/20.')
    (P/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    return report
if __name__=='__main__':audit()
