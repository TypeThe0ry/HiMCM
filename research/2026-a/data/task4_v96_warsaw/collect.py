"""Acquire/cache official yearbook originals without modifying their bytes."""
import hashlib,json,ssl,urllib.request,zipfile
from pathlib import Path
import certifi
P=Path(__file__).resolve().parent
SOURCES={
 'yearbook2025.pdf':'https://new.stat.gov.pl/sites/default/files/2026-06/Rocznik_Warszawy_2025_INTERNET.pdf',
 'yearbook2025_excel.zip':'https://new.stat.gov.pl/sites/default/files/2026-06/Dane%20w%20formacie%20Excel.zip'}
def main():
 rows=[]
 for f,u in SOURCES.items():
  q=P/f
  if not q.exists():q.write_bytes(urllib.request.urlopen(u,timeout=40,context=ssl.create_default_context(cafile=certifi.where())).read())
  b=q.read_bytes();assert b.startswith(b'%PDF' if f.endswith('.pdf') else b'PK')
  rows.append(dict(file=f,url=u,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
 (P/'manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
 z=zipfile.ZipFile(P/'yearbook2025_excel.zip');assert z.testzip() is None
 member=next(n for n in z.namelist() if n.endswith('/08_Edukacja.xlsx'))
 (P/'education2025.xlsx').write_bytes(z.read(member))
if __name__=='__main__':main()
