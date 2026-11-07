"""Audit the preserved official-reader teacher row and rounded student transcription."""
from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent

def main():
    for item in json.loads((P/'manifest.json').read_text()):
        data=(P/item['file']).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    text=json.loads((P/'teachers_web_result.json').read_text())['result']
    line=next(x for x in text.splitlines() if '专任教师数（人）' in x)
    numbers=[int(x.replace(',','')) for x in re.findall(r'\b\d[\d,]*\b',line.split('专任教师数（人）',1)[1])]
    total,ordinary,vocational,technical,adult,attached=numbers[:6]
    assert [total,ordinary,vocational,technical,adult,attached]==[7273,4164,2344,317,59,389]
    assert ordinary+vocational+technical+adult+attached==total
    bulletin=json.loads((P/'bulletin_transcription.json').read_text())
    assert bulletin['vocational_students_10k']==10.9 and bulletin['ordinary_vocational_school_count']==64
    nlo,nhi=bulletin['conditional_rounding_closure_students']
    assert [nlo,nhi]==[108950,109050]
    teachers=total-adult
    all_students=[235542+nlo,235542+nhi]
    all_teachers=23999+teachers
    result=dict(main_admitted=False,year='2025',reported_vocational_teachers=total,
        teacher_categories=dict(ordinary_specialized=ordinary,vocational_high=vocational,technical=technical,adult_specialized=adult,attached_classes=attached),
        nonadult_teacher_pool=teachers,conditional_vocational_student_bounds=[nlo,nhi],
        conditional_combined_students=all_students,conditional_combined_teachers=all_teachers,
        conditional_utility_lower=15*all_teachers/(all_students[1]+15*all_teachers),
        conditional_utility_upper=15*all_teachers/(all_students[0]+15*all_teachers),
        admission='Conditional scope compatibility scenario only; retain canonical regular-high cell',
        conditions=['Rounded student total excludes adult-specialized programmes and covers the same nonadult categories, including technical and attached classes',
                    'Nonadult teacher pools are attributable to the same upper-secondary students; tertiary/adult teaching is not mixed',
                    'Two publications use compatible 2025 school-year snapshots and nearest 0.01 ten-thousand rounding'])
    (P/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
