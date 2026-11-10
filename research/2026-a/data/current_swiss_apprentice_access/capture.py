"""Fetch bounded public EHB sources; preserve every received response body."""
from pathlib import Path
import concurrent.futures, datetime, hashlib, json, urllib.request, urllib.error
D=Path(__file__).resolve().parent
SOURCES={
 'mobility2024.pdf':'https://www.ehb.swiss/sites/default/files/2024-07/TIF_Pendelzeiten_DE_0.pdf',
 'mobility2024.html':'https://www.ehb.swiss/news/mobilitaetsmuster-von-lernenden-der-dualen-beruflichen-grundbildung',
 'access2026.html':'https://www.ehb.swiss/news/der-wohnort-beeinflusst-den-zugang-zu-lehrstellen',
 'access2026.pdf':'https://www.ehb.swiss/sites/default/files/2026-01/Trend-im-Fokus-Regionale-Unterschiede-im-Zugang-zu-dualen-Lehrstellen.pdf'}
def fetch(item):
 name,url=item
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'HiMCM-research/1.0'})
  try: response=urllib.request.urlopen(req,timeout=30)
  except urllib.error.HTTPError as error: response=error
  with response:
   body=response.read();status=response.status;ctype=response.headers.get('Content-Type');final=response.url
  if name.endswith('.pdf') and not body.startswith(b'%PDF-'):name=name+'.response'
  (D/name).write_bytes(body)
  return dict(file=name,url=url,final_url=final,status=status,content_type=ctype,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 except Exception as error:return dict(file=None,url=url,error=f'{type(error).__name__}: {error}',access_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
def main():
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: receipts=list(pool.map(fetch,SOURCES.items()))
 (D/'retrievals.json').write_text(json.dumps(receipts,indent=2)+'\n')
 print(json.dumps(receipts,indent=2))
if __name__=='__main__':main()
