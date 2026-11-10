"""Archive two bounded new official routes without changing the model."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,urllib.request
P=Path(__file__).resolve().parent
sources={
 'oph_vos_reports_original.html':'https://vos.oph.fi/rap/raportti.html',
 'parliament_HE143_2025_original.html':'https://www.eduskunta.fi/asiat-ja-aanestykset/valtiopaivaasiat/asiakirjat/edktunnus/EDK-2025-AK-60592',
}
assert not (P/'retrievals.json').exists()
assert not any((P/n).exists() for n in sources)
rows=[]
for name,url in sources.items():
 row=dict(url=url,attempt_utc=datetime.now(timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'HiMCM-source-research/1.0'}),timeout=20) as r:
   b=r.read(); row.update(file=name,status=r.status,final_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest());(P/name).write_bytes(b)
 except Exception as e: row.update(file=None,error=str(e))
 rows.append(row)
(P/'retrievals.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
