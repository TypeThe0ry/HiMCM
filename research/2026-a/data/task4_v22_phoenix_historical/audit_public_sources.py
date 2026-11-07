"""Public unauthenticated source checks; does not request access or submit forms."""
import concurrent.futures, datetime, hashlib, json
from pathlib import Path
import requests
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parent
URLS={
 'nlr_search_phoenix':'https://data.nlr.gov/search?query=Phoenix',
 'nlr_mtsa':'https://www.nlr.gov/transportation/secure-transportation-data/tsdc-metropolitan-travel-survey-archive',
 'icpsr_35264':'https://www.icpsr.umich.edu/web/ICPSR/studies/35264/datadocumentation',
 'mag_documents':'https://azmag.gov/Documents/113',
 'mag_executive_summary':'https://azmag.gov/Portals/0/Documents/pdf/cms.resource/househould-travel-survey18728.pdf?ver=C1BBbirVV6exoHZW7tsHFg%3D%3D'
}
def check(item):
 name,url=item
 out={'source_id':name,'url':url,'accessed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  r=requests.get(url,timeout=30)
  out.update(status=r.status_code,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(r.content),sha256=hashlib.sha256(r.content).hexdigest())
  if r.status_code==200:
   ext='.pdf' if r.content.startswith(b'%PDF') else '.html'
   path=ROOT/(name+ext);path.write_bytes(r.content);out['raw_file']=path.name
   if ext=='.html':
    soup=BeautifulSoup(r.text,'html.parser')
    out['page_title']=soup.title.get_text() if soup.title else None
    out['candidate_links']=[{'text':a.get_text(' ',strip=True),'href':a.get('href')} for a in soup.select('a[href]') if any(w in (a.get_text(' ',strip=True)+' '+a['href']).lower() for w in ['phoenix','maricopa','household','2002','download'])][:40]
  else:out['failure']='HTTP failure; no data admitted'
 except Exception as e:out['failure']=str(e)
 return out
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex: records=list(ex.map(check,URLS.items()))
 (ROOT/'http_audit.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(records,indent=2))
