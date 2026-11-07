"""Independent public-mirror aggregate consistency check; not official authentication."""
from pathlib import Path
from collections import defaultdict
import gzip,hashlib,json,tempfile
import numpy as np
import openpyxl
from dbfread import DBF
P=Path(__file__).resolve().parent

def main():
    metadata=json.loads((P/'aggregate_manifest.json').read_text());book=P/metadata['filename']
    assert hashlib.sha256(book.read_bytes()).hexdigest()==metadata['sha256']
    raw=gzip.decompress((P/'Banco2023_divulgacao_190225.dbf.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==json.loads((P/'microdata_manifest.json').read_text())['files'][0]['sha256']
    sums=defaultdict(lambda:np.zeros(12));seen=set()
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'raw.dbf';f.write_bytes(raw)
        for r in DBF(str(f),encoding='latin1'):
            if r['F_PESS']!=1:continue
            assert r['ID_PESS'] not in seen;seen.add(r['ID_PESS'])
            age=r['IDADE'];k=next((i for i,limit in enumerate([3,6,10,14,17,22,29,39,49,59]) if age<=limit),10)
            sums[r['ZONA']][k]+=r['FE_PESS'];sums[r['ZONA']][-1]+=r['FE_PESS']
    sheet=openpyxl.load_workbook(book,read_only=True,data_only=True)['Tab2'];errors=[];blanks=[];zones=[]
    for row in sheet.values:
        if isinstance(row[0],int) and 1<=row[0]<=527:
            zones.append(row[0])
            for k,v in enumerate(row[1:13]):
                if isinstance(v,(int,float)):errors.append(abs(sums[row[0]][k]-v))
                else:blanks.append(float(sums[row[0]][k]))
    result=dict(people=len(seen),zones=len(zones),numeric_cells=len(errors),max_absolute_weighted_person_difference=max(errors),cells_exceeding_001=int(sum(e>.001 for e in errors)),non_numeric_cells=len(blanks),non_numeric_cells_with_nonzero_microdata=sum(v!=0 for v in blanks),official_authentication=False)
    assert len(zones)==527 and len(set(zones))==527 and max(errors)<.001 and all(v==0 for v in blanks)
    (P/'population_crosscheck.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
