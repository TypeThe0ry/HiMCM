"""Retain official responses, status and UTC retrieval evidence; no model writes."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,html,json,re,urllib.request,urllib.error
O=Path(__file__).resolve().parent
SOURCES={
 'methodology_original.pdf':'https://nationaldata.ie/media/NationalDataie/MethodologyDocumentation/Department_of_Education_%26_Youth_Workforce_Data_Methodology.pdf',
 'quality_original.pdf':'https://nationaldata.ie/media/NationalDataie/MethodologyDocumentation/Teacher_Workforce_Data_Quality_Report.pdf',
 'hub_original.html':'https://nationaldata.ie/Standards/NationalDataMethodologyHub/DepartmentofEducationandYouth/TeacherWorkforceData/',
 'registration_search_original.json':'https://data.gov.ie/api/3/action/package_search?q=2025%20Q4%20Teacher%20Registration%20Statistics&rows=5',
}
def fetch(item):
 name,url=item;record=dict(file=name,url=url,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'HiMCM-source-verification/1.0'})
  with urllib.request.urlopen(req,timeout=40) as response:
   raw=response.read();record.update(status=response.status,final_url=response.url,content_type=response.headers.get('Content-Type'))
  (O/name).write_bytes(raw);record.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
 except Exception as e:record.update(error=str(e))
 return record
if __name__=='__main__':
 if (O/'retrieval.json').exists():
  raise SystemExit('Original source package already exists; retain its bytes and retrieval receipt. Use a separate directory for a new retrieval.')
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:result=list(pool.map(fetch,SOURCES.items()))
 if (O/'registration_search_original.json').exists():
  search=json.loads((O/'registration_search_original.json').read_text())
  dataset=next(x for x in search['result']['results'] if x['name']=='2025-q4-teacher-registration-statistics')
  index=fetch(('registration_index_original.html',dataset['resources'][0]['url']));result.append(index)
  if index.get('status')==200:
   urls=[html.unescape(u) for u in re.findall('href="([^"]+)"',(O/'registration_index_original.html').read_text()) if 'Q4-2025.xlsx' in u]
   assert len(urls)==1
   result.append(fetch(('registration_q4_2025_original.xlsx',urls[0])))
 (O/'retrieval.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result))
