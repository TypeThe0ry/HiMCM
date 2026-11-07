"""Rebuild Shanghai 2025 high-school counts from official PDF rows."""
import hashlib,json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def extract():
    for m in json.loads((ROOT/'manifest.json').read_text()):
        assert hashlib.sha256((ROOT/m['file']).read_bytes()).hexdigest()==m['sha256']
    tables={}
    for name,ncols in [('teachers',11),('students',6)]:
        text=subprocess.check_output(['pdftotext','-layout',str(ROOT/(name+'.pdf')),'-'],text=True)
        rows=[]
        for line in text.splitlines():
            cols=line.split()
            if cols and (cols[0]=='全市合计' or cols[0].endswith('区')):
                values=[int(x.replace(',','')) for x in cols[1:]]
                assert len(values)==ncols,(name,cols)
                rows.append(dict(district=cols[0],values=values))
        assert len(rows)==17
        assert [sum(r['values'][j] for r in rows[1:]) for j in range(ncols)]==rows[0]['values']
        tables[name]=rows
    assert [r['district'] for r in tables['students']]==[r['district'] for r in tables['teachers']]
    for r in tables['students']:assert r['values'][2]==sum(r['values'][3:])
    for r in tables['teachers']:assert r['values'][-3]==sum(r['values'][-2:])
    students=tables['students'][0]['values'][2];teachers=tables['teachers'][0]['values'][-1]
    assert (students,teachers)==(235542,23999)
    result=dict(city='Shanghai',year=2025,students=students,teachers=teachers,ptr=students/teachers,utility=15/(15+students/teachers),scope='Municipality regular senior-secondary students and full-time teacher headcount; excludes vocational programmes; not teacher FTE.',tables=tables)
    (ROOT/'extracted.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result
if __name__=='__main__':print({k:v for k,v in extract().items() if k!='tables'})
