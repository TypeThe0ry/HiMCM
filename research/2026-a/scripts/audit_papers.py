from pathlib import Path
import json,re,csv,collections
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT.parents[1]/'library'
rows=json.loads((LIB/'catalog.json').read_text())
patterns={'summary':r'\bsummary\b','assumptions':r'\bassumptions?\b','sensitivity':r'\bsensitiv\w*\b','validation':r'\bvalidat\w*\b|\bverification\b','limitations':r'\blimitations?\b|\bweakness\w*\b','references':r'\breferences\b|\bbibliography\b','AHP':r'\bAHP\b|analytic(?:al)? hierarchy','TOPSIS':r'\bTOPSIS\b','Monte_Carlo':r'\bMonte\s+Carlo\b','PCA':r'\bPCA\b|principal component','entropy':r'\bentropy\b','regression':r'\bregression\b'}
selected={'8554','8992','10550','10656','11135','14995','15041','15504','15926','16442','16738','16739'}
result=[];notes=[]
for row in rows:
 p=LIB/row['path'];name=p.stem;cache=LIB/'source_snapshots'/(name+'.txt')
 if cache.exists():text=cache.read_text();mode='archived_full_text'
 else:
  text='\n'.join((p.extract_text() or '') for p in PdfReader(p).pages);mode='pdf_extraction'
 text=text.replace('\x00','').replace('\u200b','')
 if len(text.strip())<100:
  ocr=LIB/'source_snapshots/user_finalist_17372_ocr.txt';text=ocr.read_text() if row['team']=='17372' and ocr.exists() else text;mode='first_page_OCR_only'
 out={k:row[k] for k in ['year','problem','team','award','pages','path']};out.update(extraction_mode=mode,characters=len(text))
 out.update({k:int(bool(re.search(pat,text,re.I))) for k,pat in patterns.items()});result.append(out)
 if row['team'] in selected:
  reader=PdfReader(p);snippets=[]
  for i,page in enumerate(reader.pages):
   t=(page.extract_text() or '').replace('\x00','').replace('\u200b','')
   if i<2:snippets.append(f'PDF PAGE {i+1}\n'+t[:7000])
   elif re.search(r'\bsensitiv\w*\b|\bvalidat\w*\b|\bweakness\w*\b',t,re.I):
    m=re.search(r'\bsensitiv\w*\b|\bvalidat\w*\b|\bweakness\w*\b',t,re.I);snippets.append(f'PDF PAGE {i+1}\n'+t[max(0,m.start()-150):m.start()+1500])
  notes.append(dict(year=row['year'],team=row['team'],path=row['path'],snippets=snippets))
with (ROOT/'paper_review/corpus_feature_audit.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
(ROOT/'paper_review/paper_reading_evidence.json').write_text(json.dumps(notes,ensure_ascii=False,indent=2))
summary={'n':len(rows),'extraction_modes':dict(collections.Counter(r['extraction_mode'] for r in result)),'keyword_presence':{k:sum(x[k] for x in result) for k in patterns},'warning':'Keyword mentions are not quality scores or evidence of award causation; scanned full text not audited.'}
(ROOT/'paper_review/audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False))
