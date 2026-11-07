"""Auditable name linkage of historical pupil rows to an undated school directory.

This produces descriptive matched-school counts, not a city PTR observation.
"""
from pathlib import Path
from zipfile import ZipFile
from collections import Counter,defaultdict
import csv,hashlib,io,json,re,unicodedata
P=Path(__file__).resolve().parent
UPPER={'Λύκεια','Επαγγελματικά Λύκεια'}

def canonical(name):
    return ''.join(c for c in unicodedata.normalize('NFC',name) if not c.isspace() and not unicodedata.category(c).startswith('P'))

def load(name):
    manifest=next(r for r in json.loads((P/'manifest.json').read_text()) if r['file']==name+'.zip')
    data=(P/manifest['file']).read_bytes()
    assert len(data)==manifest['bytes'] and hashlib.sha256(data).hexdigest()==manifest['sha256']
    end=0
    for r in manifest['attempts']:
        assert r['status']==206 and r['offset']==end and r['etag']==manifest['etag']
        match=re.fullmatch(r'bytes (\d+)-(\d+)/(\d+)',r['content_range'])
        a,b,total=map(int,match.groups());assert a==end and total==len(data);end=b+1
    assert end==len(data)
    with ZipFile(io.BytesIO(data)) as z:
        assert z.testzip() is None
        raw=z.read('export_'+name+'.csv');package=json.loads(z.read('datapackage.json'))
        assert hashlib.md5(raw).hexdigest()==package['resources'][0]['hash']
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))

def derive():
    students=load('minedu_students_school');directory=load('minedu_schools')
    assert len(students)==27703 and len(directory)==14181
    assert {r['year'] for r in students}=={'2018','2019'}
    for r in students:
        assert all(r[c].isdigit() for c in ['registered_students_boys','registered_students_girls'])
    athens=[r for r in directory if r['municipal_unit']=='ΑΘΗΝΑΙΩΝ']
    assert len(athens)==468 and all(r['district']=='ΑΘΗΝΑΙΩΝ' for r in athens)
    assert len({r['municipality'] for r in athens})==7
    output=[];summary=[];unmatched=[]
    for label,key in [('exact',lambda s:s),('punctuation_only',canonical)]:
        lookup=defaultdict(list)
        for r in directory:lookup[key(r['school_name'])].append(r)
        for year in ['2018','2019']:
            matched=[]
            for r in students:
                if r['year']!=year or r['school_class'] not in UPPER:continue
                candidates=lookup[key(r['school_name'])]
                if len(candidates)!=1:continue
                d=candidates[0]
                if d['municipal_unit']!='ΑΘΗΝΑΙΩΝ':continue
                if d['school_type']!=r['school_class'] or d['school_subtype']!=r['school_type']:continue
                matched.append(dict(linkage=label,year=year,school_code=d['school_code'],student_school_name=r['school_name'],directory_school_name=d['school_name'],school_class=r['school_class'],school_type=r['school_type'],boys=int(r['registered_students_boys']),girls=int(r['registered_students_girls']),pupils=int(r['registered_students_boys'])+int(r['registered_students_girls'])))
            assert len({r['school_code'] for r in matched})==len(matched)
            summary.append(dict(linkage=label,year=year,matched_schools=len(matched),registered_pupils=sum(r['pupils'] for r in matched),by_class={cl:dict(schools=sum(r['school_class']==cl for r in matched),pupils=sum(r['pupils'] for r in matched if r['school_class']==cl)) for cl in sorted(UPPER)}))
            matched_ids={r['school_code'] for r in matched}
            unmatched.extend(dict(linkage=label,year=year,school_code=d['school_code'],school_name=d['school_name'],school_type=d['school_type'],school_subtype=d['school_subtype']) for d in athens if d['school_type'] in UPPER and d['school_code'] not in matched_ids)
            output.extend(matched)
    result=dict(new_admitted_cells=0,main_admitted=False,source_rows=dict(students=len(students),directory=len(directory)),observed_year_labels=['2018','2019'],academic_year_mapping_verified=False,directory_reference_year_known=False,athens_directory_records=len(athens),athens_ward_labels=sorted({r['municipality'] for r in athens}),age14_18_identified=False,current_city_teacher_count=None,scopes=summary,limitations='Historical enrolled counts matched to undated directory. Exact or punctuation-only unique names and identical school class/subtype; no word substitutions, no imputation for unmatched schools. Not full municipal coverage, resident pupils, current education quality or a matched-year PTR.')
    return result,output,unmatched

def main():
    result,output,unmatched=derive()
    for name,rows in [('matched_school_counts.csv',output),('unmatched_directory_schools.csv',unmatched)]:
        with (P/name).open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (P/'summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
