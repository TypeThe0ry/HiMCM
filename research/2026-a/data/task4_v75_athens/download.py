import requests,json,hashlib,time,zipfile,datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'task4_v75_athens'
def download(name):
 meta=json.loads((ROOT/'task4_v74_athens'/f'{name}_metadata.json').read_text())['resources'][1]
 target=OUT/(name+'.zip');part=OUT/(name+'.zip.part');url=meta['url'];expected=meta['size'];etag=None;start=time.monotonic();attempts=[]
 if target.exists():
  cached=json.loads((OUT/(name+'_download.json')).read_text())
  assert cached['status']=='downloaded' and hashlib.sha256(target.read_bytes()).hexdigest()==cached['sha256']
  return cached
 part.write_bytes(b'')
 for attempt in range(12):
  offset=part.stat().st_size
  if offset==expected:break
  if time.monotonic()-start>180:break
  headers={'Range':f'bytes={offset}-{min(offset+131071,expected-1)}','Accept-Encoding':'identity'}
  if etag:headers['If-Range']=etag
  try:
   with requests.get(url,headers=headers,timeout=(15,20),stream=True) as r:
    entry=dict(attempt=attempt+1,offset=offset,status=r.status_code,content_range=r.headers.get('Content-Range'),etag=r.headers.get('ETag'))
    attempts.append(entry);print(name,entry,flush=True)
    if r.status_code!=206:raise RuntimeError('Server did not honor range; refusing ambiguous concatenation')
    expected_header=f'bytes {offset}-{min(offset+131071,expected-1)}/{expected}'
    if r.headers.get('Content-Range')!=expected_header:raise RuntimeError('Unexpected content range')
    new_etag=r.headers.get('ETag')
    if not new_etag or (etag is not None and new_etag!=etag):raise RuntimeError('Missing/changed object ETag')
    etag=new_etag
    data=r.content
    if len(data)!=min(131072,expected-offset):raise RuntimeError('Incomplete chunk')
    with part.open('ab') as f:f.write(data)
    print(name,'verified_bytes',part.stat().st_size,flush=True)
  except Exception as e:
   print(name,'attempt_failed',type(e).__name__,flush=True)
   if not isinstance(e,requests.RequestException):break
 if part.stat().st_size!=expected:
  result=dict(file=target.name,url=url,status='incomplete',received=part.stat().st_size,expected=expected,attempts=attempts)
 else:
  with zipfile.ZipFile(part) as z:
   assert z.testzip() is None
   print(name,'members',z.namelist(),flush=True)
  part.rename(target)
  result=dict(file=target.name,url=url,status='downloaded',bytes=expected,sha256=hashlib.sha256(target.read_bytes()).hexdigest(),etag=etag,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),attempts=attempts)
 (OUT/(name+'_download.json')).write_text(json.dumps(result,indent=2)+'\n')
 return result
with ThreadPoolExecutor(max_workers=2) as ex:
 results=list(ex.map(download,['minedu_students_school','minedu_schools']))
(OUT/'manifest.json').write_text(json.dumps(results,indent=2)+'\n')
