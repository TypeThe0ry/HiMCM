"""Verify and extract DKI Jakarta rows from original Ministry 2025/26 PDFs."""
import hashlib,json,re,subprocess,tempfile
from pathlib import Path

P=Path(__file__).resolve().parent

def source_bytes(item):
    if 'parts' in item:
        data=[]
        for part in item['parts']:
            raw=(P/part['file']).read_bytes()
            assert len(raw)==part['bytes']
            assert hashlib.sha256(raw).hexdigest()==part['sha256']
            data.append(raw)
        raw=b''.join(data)
    else:raw=(P/item['file']).read_bytes()
    assert len(raw)==item['bytes']
    assert hashlib.sha256(raw).hexdigest()==item['sha256']
    return raw

def row(page):
    lines=[s for s in page.splitlines() if 'DKI Jakarta' in s]
    assert len(lines)==1
    return [int(x.replace('.','')) for x in lines[0].split('DKI Jakarta',1)[1].split()]

def main():
    manifest=json.loads((P/'manifest.json').read_text())
    files={x.get('file',x.get('reassembled_file')):source_bytes(x) for x in manifest}
    config={'sma':dict(student_page=23,staff_page=26,head_page=105,teacher_page=121,
                       expected=(510,186461,11983,453,11530,1188)),
            'smk':dict(student_page=25,staff_page=28,head_page=115,teacher_page=131,
                       expected=(553,194178,11519,525,10994,1621))}
    observations=[]
    for kind,c in config.items():
        with tempfile.TemporaryDirectory() as folder:
            pdf=Path(folder)/'source.pdf';pdf.write_bytes(files[kind+'2025_26.pdf'])
            text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-']).decode()
        assert '30 November 2025' in text
        pages=text.split('\f')
        students=row(pages[c['student_page']-1]);staff=row(pages[c['staff_page']-1])
        head=row(pages[c['head_page']-1]);teachers=row(pages[c['teacher_page']-1])
        assert 'Pendidik Induk' in pages[c['teacher_page']-1]
        assert 'Tabel pendidik selanjutnya hanya menggunakan data pendidik induk' in ''.join(pages[c['teacher_page']-3:c['teacher_page']])
        actual=(students[0],students[2],staff[0],head[-1],teachers[2],teachers[5])
        assert actual==c['expected'],(kind,actual)
        assert head[-1]+teachers[2]==staff[0]
        assert teachers[2]+teachers[5]==teachers[8]
        assert teachers[0]+teachers[1]==teachers[2]
        observations.append(dict(program=kind.upper(),academic_year='2025/2026',snapshot='2025-11-30',
            geography='DKI Jakarta',school_status='public+private',schools=students[0],students=students[2],
            headmasters_and_induk_teachers=staff[0],headmasters=head[-1],induk_teachers=teachers[2],
            noninduk_teacher_attachments=teachers[5],all_teacher_attachments=teachers[8],
            pdf_pages={k:c[k] for k in ['student_page','staff_page','head_page','teacher_page']},
            students_per_induk_teacher=students[2]/teachers[2],
            students_per_headmaster_and_induk_teacher=students[2]/staff[0]))
    result=dict(source_originals_verified=True,raw_pdf_snapshot='2025-11-30',observations=observations,
                combined_students=sum(x['students'] for x in observations),
                combined_induk_teachers=sum(x['induk_teachers'] for x in observations),
                combined_headmasters=sum(x['headmasters'] for x in observations),
                combined_headmasters_and_induk_teachers=sum(x['headmasters_and_induk_teachers'] for x in observations),
                coverage='Ministry SMA and SMK; MA/MAK and special/equivalency provision not established by these two books',
                count_unit='Home-assignment/induk headcount; not teaching FTE',main_model_modified=False)
    (P/'observation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
