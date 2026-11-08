"""Reproduce the full-document field scan; OCR stays in a temporary workdir."""
import argparse,csv,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
P=Path(__file__).resolve().parent
SOURCE=P.parent/'task4_v114_istanbul_travel/istanbul_liseli_profili_2011.pdf'
TERMS={'duration_or_mode':r'\b(dakika|dakikada|otobüs|servis|yolculuk|mesafe)\b',
       'transport':r'ulaşım','school_residence':r'ikamet|nerede kalıyorsun',
       'age_or_grade':r'yaş|sınıf','geography':r'ilçe|mahalle|semt'}

def run(workdir,workers=6):
    audit=json.loads((P/'audit.json').read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==audit['source_sha256']
    workdir=workdir.resolve();workdir.mkdir(parents=True,exist_ok=True)
    prefix=['/usr/bin/arch','-arm64'] if sys.platform=='darwin' else []
    def one(n):
        base=workdir/f'page{n:03}'
        subprocess.run(prefix+[shutil.which('pdftoppm'),'-f',str(n),'-l',str(n),'-singlefile','-scale-to','1800','-png',str(SOURCE),str(base)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(prefix+[shutil.which('tesseract'),str(base)+'.png',str(base),'-l','tur','--psm','3'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,env={**os.environ,'OMP_THREAD_LIMIT':'1'})
        file=base.with_suffix('.txt');text=file.read_text().lower()
        row=dict(pdf_page=n,ocr_characters=len(text),ocr_sha256=hashlib.sha256(file.read_bytes()).hexdigest())
        row.update({k:len(re.findall(v,text)) for k,v in TERMS.items()})
        return row
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows=list(pool.map(one,range(1,127)))
    with (P/'page_scan.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
    print(json.dumps(dict(pages=len(rows),nonempty=sum(r['ocr_characters']>0 for r in rows),keyword_counts={k:sum(r[k] for r in rows) for k in TERMS}),indent=2))
    return rows

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--workdir',type=Path,default=Path(tempfile.mkdtemp(prefix='liseli115_')));parser.add_argument('--workers',type=int,default=6)
    args=parser.parse_args();run(args.workdir,args.workers)
