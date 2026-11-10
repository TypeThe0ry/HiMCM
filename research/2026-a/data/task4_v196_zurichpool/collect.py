"""Capture the official directory response once, preserving original bytes."""
from pathlib import Path
import datetime,hashlib,json,urllib.request
P=Path(__file__).resolve().parent
url='https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder.html'
assert not any((P/n).exists() for n in ['directory_response_original.html','retrieval.json'])
r=dict(url=url,attempt_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-source-verification/1.0'}),timeout=25) as f:
  b=f.read(5000000);r.update(status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file='directory_response_original.html');(P/r['file']).write_bytes(b)
except Exception as e:r.update(error=str(e),file=None)
(P/'retrieval.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
