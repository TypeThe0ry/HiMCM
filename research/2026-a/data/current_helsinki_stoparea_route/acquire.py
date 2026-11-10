#!/usr/bin/env python3
"""Inspect a frozen range-snapshot of HSL's GTFS ZIP; fail if its ETag changes."""
import datetime, hashlib, io, json, pathlib, requests, sys, zipfile
P=pathlib.Path(__file__).resolve().parent
URL='https://infopalvelut.storage.hsldev.com/gtfs/hsl.zip'
manifest=json.loads((P/'http_manifest.json').read_text()) if (P/'http_manifest.json').exists() else []
def safe_headers(headers):
    keep={'etag','last-modified','content-range','content-length','content-type','date'}
    return {k:v for k,v in headers.items() if k.lower() in keep}
def fetch(url, name, headers=None, required=True):
    for item in manifest:
        if item.get('url')==url and item.get('request_headers')==(headers or {}) and item.get('status') in (200,206,403) and item.get('body') and (P/item['body']).exists():
            class Cached: pass
            c=Cached(); c.content=(P/item['body']).read_bytes(); c.status_code=item['status']; c.headers=item['response_headers']; c.raise_for_status=lambda: None
            if not required or c.status_code<400: return c
    t=datetime.datetime.now(datetime.timezone.utc).isoformat()
    r=requests.get(url,headers=headers or {},timeout=45)
    (P/name).write_bytes(r.content)
    manifest.append({'utc':t,'url':url,'request_headers':headers or {},'status':r.status_code,'response_headers':safe_headers(r.headers),'body':name,'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content)})
    (P/'http_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    if required: r.raise_for_status()
    return r
fetch('https://www.hsl.fi/hsl/avoin-data','hsl_open_data.html',required=False)
fetch('https://digitransit.fi/en/developers/apis/','digitransit_api.html',required=False)
head=requests.head(URL,timeout=30); head.raise_for_status()
etag=head.headers['ETag']; size=int(head.headers['Content-Length'])
manifest.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':URL,'method':'HEAD','status':head.status_code,'response_headers':safe_headers(head.headers),'body':None})
class Remote(io.RawIOBase):
    def __init__(self): self.pos=0; self.n=0
    def readable(self): return True
    def seekable(self): return True
    def tell(self): return self.pos
    def seek(self,offset,whence=0):
        self.pos=offset if whence==0 else self.pos+offset if whence==1 else size+offset
        return self.pos
    def read(self,n=-1):
        if n<0: n=size-self.pos
        if not n or self.pos>=size:return b''
        end=min(size-1,self.pos+n-1)
        r=fetch(URL,f'range_{self.pos}_{end}.bin',{'Range':f'bytes={self.pos}-{end}','If-Match':etag})
        self.n+=1
        if r.status_code!=206 or r.headers.get('ETag')!=etag or len(r.content)!=end-self.pos+1: raise ValueError('Unexpected range or changing archive')
        self.pos=end+1
        return r.content
with zipfile.ZipFile(Remote()) as z:
    infos=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size,'crc32':f'{i.CRC:08x}'} for i in z.infolist()]
    (P/'zip_inventory.json').write_text(json.dumps({'etag':etag,'archive_size':size,'members':infos},indent=2)+'\n')
    print(json.dumps(infos,indent=2))
    members=['stops.txt','calendar.txt','calendar_dates.txt','feed_info.txt','routes.txt','areas.txt','stop_areas.txt']
    if '--trips' in sys.argv: members.append('trips.txt')
    for name in members:
        if name in z.namelist(): (P/name).write_bytes(z.read(name))
