from urllib.request import Request,urlopen
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import re,json,html,hashlib
out=Path('research/2026-a/data/city_matrix_25_audit/sources')
jobs=[]
for kind in ['cost-of-living','property-investment']:
 for ver,tail in [('current','rankings_current.jsp'),('mid','rankings.jsp'),('2026','rankings.jsp?title=2026')]: jobs.append((kind,ver,f'https://www.numbeo.com/{kind}/{tail}'))
def f(job):
 kind,ver,url=job; p=out/f'{kind}_{ver}.html'
 try:
  data=p.read_bytes() if p.exists() else urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30).read();p.write_bytes(data)
  txt=data.decode(); rows=[]
  for tr in re.findall(r'<tr\b[^>]*>(.*?)</tr>',txt,re.S):
   cells=[html.unescape(re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<td\b[^>]*>(.*?)</td>',tr,re.S)]
   if len(cells)>2:
    try: val=float(cells[2])
    except:continue
    rows.append({'city':cells[1],'value':val})
  return {'kind':kind,'version':ver,'url':url,'title':re.findall(r'<h1[^>]*>(.*?)</h1>',txt,re.S),'sha256':hashlib.sha256(data).hexdigest(),'rows':rows}
 except Exception as e:return {'kind':kind,'version':ver,'url':url,'error':str(e)}
with ThreadPoolExecutor(max_workers=4) as ex:result=list(ex.map(f,jobs))
Path('research/2026-a/data/city_matrix_25_audit/numbeo_comparison_sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
original=json.load(open('research/2026-a/data/city_matrix_25_audit/original_extracted.json'))[0]['rows']
for i,r in enumerate(original[21:],22):
 for j,kind in [(5,'cost-of-living'),(7,'property-investment')]:
  if r[j] is None:continue
  variants=[]
  for x in result:
   if x['kind']!=kind:continue
   found=[a for a in x.get('rows',[]) if a['city'].split(',')[0] in [r[0],'Tel Aviv-Yafo'] and (r[0]!='London' or a['city'].endswith('United Kingdom'))]
   variants.append((x['version'],found))
  print(i,r[0],kind,round(r[j],3),variants)
