"""Bounded seven original retained pool detail pages for cross-group deduplication."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
P=Path(__file__).resolve().parent
slugs=['altstetten','blaesi','bungertwies','city','leimbach','oerlikon','kaeferberg']
assert not any((P/n).exists() for n in ['existing_retrievals.json',*[s+'_original.html' for s in slugs]])
def get(s):
 u='https://www.stadt-zuerich.ch/de/stadtleben/sport-und-erholung/sport-und-badeanlagen/hallenbaeder/'+s+'.html'
 r=dict(slug=s,url=u,attempt_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'HiMCM-source-verification/1.0'}),timeout=25) as f:
   b=f.read(5000000);r.update(status=f.status,final_url=f.url,content_type=f.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),file=s+'_original.html');(P/r['file']).write_bytes(b)
 except Exception as e:r.update(error=str(e),file=None)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:rows=list(ex.map(get,slugs))
(P/'existing_retrievals.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
