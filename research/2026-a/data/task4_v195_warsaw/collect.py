"""Bounded new Warsaw source acquisition; preserve every response without interpretation."""
import datetime,hashlib,json,urllib.request
from pathlib import Path
P=Path(__file__).resolve().parent
sources={'wbr2025_presentation_response_original.bin':'https://um.warszawa.pl/documents/39703/62400386/WBR+Prezentacja+-04.15+FINAL.pptx/849bf442-0644-0264-c92a-c807cdeb8bec', 'wbr2015_model_response_original.bin':'https://transport.um.warszawa.pl/documents/62470/8560273/WBR_2015._Etap_IV._Raport_z_budowy_modelu_ruchu.pdf/fa542843-0c97-93e5-ba08-7797d5c0d696?t=1634498736983'}
assert not (P/'retrievals.json').exists()
assert not any((P/n).exists() for n in sources)
rows=[]
for name,url in sources.items():
 r=dict(url=url,file=name,attempt_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 HiMCM source research'}),timeout=25) as x:
   b=x.read(20000001)
   if len(b)>20000000: raise ValueError('20MB acquisition cap; not archived')
   (P/name).write_bytes(b)
   r.update(status=x.status,content_type=x.headers.get('Content-Type'),final_url=x.url,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:r.update(error=str(e),file=None)
 rows.append(r)
(P/'retrievals.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
