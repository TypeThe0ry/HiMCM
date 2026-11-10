"""Archive cited Milanosport tariff original without overwriting evidence."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
P=Path(__file__).resolve().parent
url='https://www.milanosport.it/workspace/uploads/nuovi-tariffari-1-giugno-2025-agg-9-10-2025.pdf'
for name in ['tariff_original.pdf','retrieval.json']:
 if (P/name).exists():raise FileExistsError(name)
record=dict(url=url,attempt_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-source-verification/1.0'}),timeout=30) as r:
  b=r.read(10000001)
  if len(b)>10000000:raise ValueError('Download cap exceeded')
  record.update(status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  if not b.startswith(b'%PDF'):raise ValueError('Response is not a PDF')
  (P/'tariff_original.pdf').write_bytes(b)
except Exception as e:record['error']=str(e)
(P/'retrieval.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
