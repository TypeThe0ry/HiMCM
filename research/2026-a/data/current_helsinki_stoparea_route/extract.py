#!/usr/bin/env python3
"""Rebuild selected members from locally recorded frozen HTTP ranges, offline."""
import hashlib, io, json, pathlib, sys, zipfile
P=pathlib.Path(__file__).resolve().parent
inventory=json.loads((P/'zip_inventory.json').read_text())
size=inventory['archive_size']; etag=inventory['etag']
records=json.loads((P/'http_manifest.json').read_text())
class Frozen(io.RawIOBase):
 def __init__(self): self.pos=0
 def readable(self): return True
 def seekable(self): return True
 def tell(self): return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else self.pos+offset if whence==1 else size+offset
  return self.pos
 def read(self,n=-1):
  if n<0:n=size-self.pos
  if not n or self.pos>=size:return b''
  start=self.pos; end=min(size-1,start+n-1); expected=f'bytes={start}-{end}'
  for r in records:
   h={k.lower():v for k,v in r.get('response_headers',{}).items()}
   if r.get('request_headers',{}).get('Range')==expected and r.get('request_headers',{}).get('If-Match')==etag and r['status']==206 and h.get('etag')==etag and h.get('content-range')==f'bytes {start}-{end}/{size}':
    b=(P/r['body']).read_bytes()
    if hashlib.sha256(b).hexdigest()!=r['sha256'] or len(b)!=end-start+1:raise ValueError('Corrupt range')
    self.pos=end+1; return b
  raise ValueError('No verified frozen range: '+expected)
with zipfile.ZipFile(Frozen()) as z:
 names=['stops.txt','calendar.txt','calendar_dates.txt','feed_info.txt','routes.txt','areas.txt','stop_areas.txt']
 for name in names:(P/name).write_bytes(z.read(name))
 if '--trips' in sys.argv:
  out=pathlib.Path('/data/scratch/himcm_hsl_gtfs_trips.txt'); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(z.read('trips.txt')); print(out)
