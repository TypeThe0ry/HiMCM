"""Check the official indexed-table transcription, not an original-byte archive."""
import csv,hashlib,json
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
    with (P/'ma_municipal_transcription.csv').open() as f:rows=list(csv.DictReader(f))
    for r in rows:
        for k in list(r)[1:]:r[k]=int(r[k])
        for item in ['schools','staff','students']:
            assert r[item+'_public']+r[item+'_private']==r[item+'_total']
    province=rows[-1]
    for k in list(province)[1:]:assert sum(r[k] for r in rows[:-1])==province[k]
    assert [province[k] for k in ['schools_total','staff_total','students_total']]==[100,2008,24672]
    meta=json.loads((P/'provenance.json').read_text())
    assert meta['school_year']=='2025/2026' and meta['report_cutoff']=='2025-12-31'
    result=dict(municipal_rows=6,all_component_and_geographic_sums_match=True,schools=100,
                reported_headmasters_and_teachers=2008,students=24672,
                teacher_only_count_identified=False,original_source_bytes_archived=False,
                source_type='Official indexed table transcription',school_year=meta['school_year'],cutoff=meta['report_cutoff'])
    (P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[]
    for name in ['ma_municipal_transcription.csv','provenance.json']:
        raw=(P/name).read_bytes();files.append(dict(file=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),kind='derived transcription/provenance, not raw original'))
    (P/'manifest.json').write_text(json.dumps(files,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
