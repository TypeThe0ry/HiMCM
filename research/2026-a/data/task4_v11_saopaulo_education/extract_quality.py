"""Preserve national assessment scale and public-network scope, without main admission."""
from pathlib import Path
import zipfile,xml.etree.ElementTree as E,json,hashlib
P=Path(__file__).resolve().parent
NS={'t':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','o':'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
def cells(row):
    out=[]
    for c in row.findall('t:table-cell',NS):
        raw=c.get('{'+NS['o']+'}value');v=float(raw) if raw is not None else ''.join(c.itertext())
        out.extend([v]*min(100,int(c.get('{'+NS['t']+'}number-columns-repeated','1'))))
    return out

def main():
    f=P/'divulgacao_ensino_medio_municipios_2023.ods';blob=f.read_bytes();m=json.loads((P/'manifest.json').read_text())
    assert hashlib.sha256(blob).hexdigest()==m['sha256']
    assert hashlib.md5(blob).hexdigest()==m['md5'] and m['md5'] in (P/'checksums.md5').read_text()
    root=E.fromstring(zipfile.ZipFile(f).read('content.xml'));header=None;rows=[]
    for row in root.findall('.//t:table-row',NS):
        values=cells(row)
        if 'VL_OBSERVADO_2023' in values:header=values
        if 3550308.0 in values and 'São Paulo' in values:
            assert header is not None
            rows.append({str(k):v for k,v in zip(header,values) if k and (str(k).endswith('2023') or '2023_' in str(k) or k in header[:4])})
    assert len(rows)==4
    (P/'quality_rows.json').write_text(json.dumps({'city_code':3550308,'school_stage':'Ensino Medio Regular','main_admitted':False,'rows':rows},ensure_ascii=False,indent=2)+'\n');print(json.dumps(rows,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
