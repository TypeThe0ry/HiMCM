"""Retrieve the published cantonal chart's provenance chain; never execute remote JS."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, requests
D=Path(__file__).resolve().parent
BASE='https://www.zh.ch/de/bildung/bildungssystem/zahlen-fakten/entwicklung-des-schulpersonals-an-mittelschulen-und-berufsfachschulen'
SOURCES={
 'staff_page_original.html':BASE+'.html',
 'survey_page_original.html':'https://www.zh.ch/de/bildung/bildungssystem/studien-in-der-bildung/lehrpersonen-und-schulpersonal.html',
 'chart_snippet_original.html':BASE+'/_jcr_content/main/singlepageapplicatio_895902676.zhweb-spa-snippet.zhweb-cache.html',
 'chart_module_original.js':'https://api.observablehq.com/d/2ebdda3eb4cd0353.js?v=4',
 'chart_general_original.js':'https://api.observablehq.com/@bildungsplanungzh/general.js?v=4&resolutions=2ebdda3eb4cd0353@1488',
 'staff_data_original.json':'https://www.bista.zh.ch/basicapi/zhweb/p_entwicklung_der_anzahl_vollzeiteinheiten_an_mittelschulen_und_berufsfachschulen?refreshcache=false',
}
def get(item):
 name,url=item
 stamp=datetime.now(timezone.utc).isoformat()
 r=requests.get(url,timeout=40)
 r.raise_for_status()
 (D/name).write_bytes(r.content)
 return {'file':name,'url':url,'final_url':r.url,'retrieved_utc':stamp,'status':r.status_code,'content_type':r.headers.get('Content-Type'),'bytes':len(r.content),'sha256':hashlib.sha256(r.content).hexdigest()}
if __name__=='__main__':
 if any((D/name).exists() for name in SOURCES):
  raise SystemExit('Frozen originals already exist; use extract.py offline or retrieve a new version in a new directory.')
 with ThreadPoolExecutor(max_workers=6) as pool: rows=list(pool.map(get,SOURCES.items()))
 (D/'retrieval.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps([{'file':r['file'],'status':r['status'],'bytes':r['bytes']} for r in rows]))
