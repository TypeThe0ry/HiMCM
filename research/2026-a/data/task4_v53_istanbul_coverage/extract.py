"""Expand actual upper-secondary student coverage, retaining teacher allocation bounds."""
from pathlib import Path
import hashlib,json,re,subprocess
P=Path(__file__).resolve().parent
OLD=P.parent/'task4_v6_education'

def cells(line):
    return [None if x=='-' else int(x.replace(' ','')) for x in re.split(r'\s{2,}',line.strip()) if x=='-' or re.fullmatch(r'[\d ]+',x)]

def utility(n,t):return 15*t/(n+15*t)

def main():
    pdf=OLD/'turkey2026.pdf'
    prior=json.loads((OLD/'manifest.json').read_text())
    expected=next(r for r in prior if r.get('file')=='turkey2026.pdf')
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==expected['sha256']
    pages=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode().split('\f')
    left,right=pages[184],pages[185]
    lblock=left.split('TR100 İstanbul',1)[1].split('TR211 Tekirdağ',1)[0]
    rlines=right.splitlines();start=next(i for i,l in enumerate(rlines) if 'İstanbul TR100' in l)
    rblock='\n'.join(rlines[start:start+12])
    definitions=pages[64]
    assert 'lower secondary schools operating within imam hatip high' in definitions
    assert 'counted under the respective imam hatip high schools' in definitions
    vlines=pages[123].splitlines();vindex=next(i for i,l in enumerate(vlines) if 'Meslek Ortaokulu' in l)
    vocational_lower='\n'.join(vlines[vindex:vindex+4])
    assert re.search(r'27\s+556\s+305\s+251\s+-',vocational_lower)
    article=(P/'vocational_lower_school_article.html').read_text()
    assert 'mesleki ve teknik Anadolu liseleri bünyesinde açılacak' in article
    programs={}
    for name,lname,rname in [('general','Genel','General'),('vocational','Mesleki ve teknik','Vocational and technical'),('imam_hatip','İmam Hatip Liseleri','Imam Hatip High Schools')]:
        ll=next(l for l in lblock.splitlines() if l.startswith(lname) and 'Toplam' in l)
        rr=next(l for l in rblock.splitlines() if 'Total' in l and rname in l)
        a,b=cells(ll),cells(rr)
        assert len(a)==10 and len(b)==11
        total,teachers,public=a[1],a[4],a[7]
        private=0 if b[3] is None else b[3]
        private_t=0 if b[6] is None else b[6]
        open_students=b[8]
        assert total-open_students==public+private
        assert teachers==b[0]+private_t
        programs[name]=dict(total_including_open=total,open_students=open_students,
            non_open_students=total-open_students,public_students=public,private_students=private,
            reported_teacher_pool=teachers,public_teachers=b[0],private_teachers=private_t,
            left_line=ll,right_line=rr)
    assert [programs[k]['non_open_students'] for k in programs]==[408480,271015,72103]
    assert [programs[k]['reported_teacher_pool'] for k in programs]==[28436,20156,9871]
    n=sum(r['non_open_students'] for r in programs.values());assert n==751598
    assert sum(r['total_including_open'] for r in programs.values())==984758
    assert sum(r['open_students'] for r in programs.values())==233160
    assert sum(r['reported_teacher_pool'] for r in programs.values())==58463
    result=dict(city='Istanbul',year='2025/26',source='Existing V6 official MEB PDF, no new survey',
        geography='TR100 province; allsettlement rows coincide withcity row in source',
        student_scope='Non-open general, vocational/technical and Imam Hatip upper-secondary categories; not exact age14-18',
        students=n,students_upper_nonopen=n,general_teachers=28436,imam_teacher_pool=9871,known_general_teachers=28436,vocational_teacher_pool=20156,imam_hatip_teacher_pool=9871,
        teacher_lower=28436,teacher_upper=58463,utility_lower=utility(n,28436),utility_upper=utility(n,58463),
        old_general_students=408480,old_general_teachers=28436,old_general_utility=utility(408480,28436),
        general_vocational_students=679495,
        conditional_all_vocational_upper_teachers=dict(teacher_lower=48592,teacher_upper=58463,
             utility_lower=utility(n,48592),utility_upper=utility(n,58463),assumption='All vocational teacher pool attributable to upper-secondary; not independently verified'),
        allocation_notes=['ImamHatip upper school teacher counts explicitly include lower-stage school teachers.',
            'National table records27 vocational lower-secondary schools with556students and dashedteacherfields; officialMEB curriculum article locates this new program within vocational highschools.',
            'No city-specific vocational upper/lower teacher allocation established. V in[0,20156] retained, without claiming all Istanbul vocational teachers teach lowersecondary.',
            'General28436 is inherited stage-specific reportedheadcount; all counts are permanent+contractual headcount, notFTE.'],
        programs=programs,main_admitted=False)
    (P/'observation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    excerpts='PDF185 / printed154\n'+lblock+'\nPDF186 / printed155\n'+rblock+'\nPDF65 / printed34 teacherallocationnote\n'+'\n'.join(l for l in definitions.splitlines() if 'Note 3.' in l or 'schools are counted under' in l or 'upper secondary education level when' in l)+'\nPDF124 / printed93 vocational lowerstage\n'+vocational_lower+'\n'
    (P/'source_excerpts.txt').write_text(excerpts)
    sources=[dict(file='../task4_v6_education/turkey2026.pdf',url='https://sgb.meb.gov.tr/istatistik_2026/2526.pdf',reused_original=True),dict(file='vocational_lower_school_article.html',url='https://mtegm.meb.gov.tr/www/meslek-ortaokulu-ve-yeni-acilacak-alanlara-ait-program-gelistirme-calistaylarimiz-devam-ediyor/icerik/3698',reused_original=False)]
    for r in sources:
        raw=(P/r['file']).read_bytes();r.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    (P/'manifest.json').write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='programs'},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
