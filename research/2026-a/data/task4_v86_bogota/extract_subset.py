#!/usr/bin/env python3
"""Extract Bogotá's public-use PISA2022 records from the official OECD SPSS ZIP.
Raw ZIP/SAV stay outside this repository. Requires pandas, numpy, pyreadstat.
Usage: python extract_subset.py /path/to/STU_QQQ_SPSS.zip /tmp/pisa_extract
"""
import argparse, hashlib, json, platform, zipfile
from pathlib import Path
import pandas as pd
import pyreadstat

HERE = Path(__file__).resolve().parent
URL = 'https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip'
BASE = ['CNT','CNTRYID','CNTSCHID','CNTSTUID','REGION','STRATUM','ST001D01T','AGE','W_FSTUWT']
REPS = [f'W_FSTURWT{i}' for i in range(1,81)]
PVS = [f'PV{i}{s}' for s in ['MATH','READ','SCIE'] for i in range(1,11)]

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024), b''): h.update(b)
    return h.hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('archive',type=Path);p.add_argument('scratch',type=Path);a=p.parse_args()
    a.scratch.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(a.archive) as z:
        info=z.getinfo('CY08MSP_STU_QQQ.SAV')
        # Extraction reads the full member and verifies its ZIP CRC.
        sav=Path(z.extract(info,a.scratch))
    _,meta=pyreadstat.read_sav(sav,metadataonly=True)
    cols=BASE+REPS+PVS
    assert set(cols)<=set(meta.column_names),set(cols)-set(meta.column_names)
    # Read selected columns in a single pass; avoid repeated decompression by row chunks.
    frame,_=pyreadstat.read_sav(sav,usecols=cols)
    region=pd.to_numeric(frame.REGION,errors='coerce')
    country=frame.CNT.astype(str).str.strip()
    mask=(region==17001)&(country=='COL')
    strata=country.eq('COL')&frame.STRATUM.astype(str).str.strip().isin(['COL01','COL02','COL03'])
    assert mask.equals(strata),'REGION and STRATUM disagree'
    out=frame.loc[mask,cols].copy()
    assert len(out)==1986 and out.CNTSTUID.nunique()==1986
    target=HERE/'bogota_pisa2022_selected.csv.gz'
    out.to_csv(target,index=False,compression={'method':'gzip','mtime':0})
    manifest={
      'source_url':URL,'retrieved':'2026-11-08','archive_bytes':a.archive.stat().st_size,
      'archive_sha256':sha(a.archive),'member':info.filename,'member_bytes':info.file_size,
      'member_crc32':f'{info.CRC:08x}','member_sha256':sha(sav),
      'international_rows':len(frame),'colombia_rows':int(country.eq('COL').sum()),'bogota_rows':len(out),
      'selection':"CNT == 'COL' AND numeric(REGION) == 17001; checked equivalent STRATUM in COL01,COL02,COL03",
      'columns':cols,'column_labels':{k:meta.column_names_to_labels[k] for k in cols},
      'derived_file':target.name,'derived_sha256':sha(target),'derived_bytes':target.stat().st_size,
      'original_bytes_preserved':'Official archive and unmodified extracted SAV retained outside Git; this CSV is a derived row/column subset.',
      'validation_baseline':{n:sha(HERE.parent/'task4_v85_pisa_city'/n) for n in ['summary.json','annex_b2.xlsx','manifest.json']},
      'runtime':{'python':platform.python_version(),'pandas':pd.__version__,'pyreadstat':pyreadstat.__version__}}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['archive_sha256','international_rows','colombia_rows','bogota_rows','derived_bytes']},indent=2))

if __name__=='__main__':main()
