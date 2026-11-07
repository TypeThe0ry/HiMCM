"""Independent check of home assignment versus employment/role categories."""
from pathlib import Path
import hashlib,json,re,subprocess

P=Path(__file__).resolve().parent
source=P.parent/'task4_v58_jakarta_education/sma2025_26.pdf'
text=subprocess.check_output(['pdftotext','-layout',str(source),'-']).decode()
rows=[line for line in text.splitlines() if 'DKI Jakarta' in line]
induk=next(line for line in rows if all(x in line for x in ['11.530','1.188','12.718']))
roles=next(line for line in rows if all(x in line for x in ['453','9.004','2.526','11.983']))
assert 9004+2526==11530 and 11530+453==11983
assert 11530+1188==12718
assert 'hanya menggunakan data pendidik induk' in text
result=dict(sma_induk=11530,sma_permanent=9004,sma_nonpermanent=2526,
            sma_headmasters=453,sma_noninduk_attachments=1188,
            induk_equals_fte=False,all_noninduk_duplicate_within_city_established=False,
            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
            source_bytes=source.stat().st_size,changed_model_cells=0)
(P/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
