"""Offline source-hash validation and reproducible conditional PTR extraction.

Istanbul: raw PDF -> pdftotext -> table 2.11 paired panels.
Jakarta: documented manual transcription of official PDF web renderer;
full source PDF unavailable locally (download timeout), not raw-PDF extraction.
"""
from pathlib import Path
import csv, hashlib, json, re, subprocess
P=Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def numbers(line):
    # Turkish grouped integers contain one space, table columns >=2 spaces.
    return [int(x.replace(' ','')) for x in re.split(r'\s{2,}',line.strip()) if re.fullmatch(r'[\d ]+',x)]

def main():
    for r in json.loads((P/'manifest.json').read_text()):
        if 'sha256' in r: assert digest(P/r['file'])==r['sha256'],r['file']
    text=subprocess.check_output(['pdftotext','-layout',str(P/'turkey2026.pdf'),'-']).decode()
    pages=text.split('\f'); left=pages[184];right=pages[185]
    assert '2.11 ' in left and '2.11.' in right
    block=left.split('TR100 İstanbul',1)[1]
    line=next(s for s in block.splitlines() if s.startswith('Genel') and 'Toplam' in s)
    n=numbers(line)
    assert n[:6]==[987,612016,293804,318212,28436,17435],n
    general_total=n[1];teacher_total=n[4];public_students=n[7]
    rline=next(s for s in right.splitlines() if '98 815' in s and 'General' in s and 'Total' in s)
    m=numbers(rline)
    assert m[:11]==[17573,8660,632,98815,51640,47175,10863,8775,203536,110123,93413],m
    enrolled=general_total-m[8]
    assert enrolled==public_students+m[3]==408480
    assert teacher_total==m[0]+m[6]==28436
    rows=[dict(city='Istanbul',indicator='upper_secondary_ptr',value=enrolled/teacher_total,year=2026,
       unit='students_per_teacher_headcount',source_url='https://sgb.meb.gov.tr/istatistik_2026/2526.pdf',
       scope='Istanbul TR100 province; general upper-secondary public+private; open-education pupils excluded using same table; excludes vocational and Imam Hatip schools; permanent+contractual teacher headcount; not FTE; 2025/26',
       status='observed_general_upper_secondary_scope_conditional',students=enrolled,teachers=teacher_total,
       lower_bound_only=False,source_locator='Table 2.11, printed154–155, PDF185–186',extraction='raw_pdf_pdftotext')]
    with (P/'jakarta_sma2024_web_transcription.csv').open() as f: regional=list(csv.DictReader(f))
    for key in list(regional[0])[1:]:
        assert sum(int(r[key]) for r in regional[:-1])==int(regional[-1][key])
    for r in regional:
        for k in ['students','teachers']:
            assert int(r[k+'_public'])+int(r[k+'_private'])==int(r[k+'_total'])
    j=regional[-1]; students=int(j['students_total']); teachers=int(j['teachers_total'])
    rows.append(dict(city='Jakarta',indicator='upper_secondary_ptr',value=students/teachers,year=2024,
       unit='students_per_teacher_including_headmaster_headcount',
       source_url='https://jakarta.bps.go.id/id/publication/2025/02/28/30874e042a98939928603ee5/provinsi-dki-jakarta-dalam-angka-2025.html',
       scope='DKI Jakarta province all6 regency/municipalities; public+private SMA under education ministry; includes headmasters in teacher count; excludes vocational SMK, religious MA and overseas schools; 2024/25',
       status='observed_general_upper_secondary_manual_source_scope_conditional',students=students,teachers=teachers,
       lower_bound_only=False,source_locator='Table4.1.7 printed201–202; web-rendered official BPS PDF',extraction='manual_official_web_pdf_transcription_raw_pdf_unavailable'))
    with (P/'observations.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (P/'istanbul_source_rows.json').write_text(json.dumps(dict(left_source_line=line,right_source_line=rline,
       general_including_open=general_total,open_students=m[8],general_in_person=enrolled,
       public_students=public_students,private_students=m[3],teacher_total=teacher_total),ensure_ascii=False,indent=2)+'\n')
    for r in rows:print(r['city'],r['students'],r['teachers'],r['value'])
if __name__=='__main__':main()
