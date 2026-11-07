"""Build print-size pages and audit every embedded text span."""
from pathlib import Path
import json
import pymupdf as fitz
H=Path(__file__).resolve().parent
out=fitz.open();audit=[]
for f in sorted((H/'figures').glob('*.pdf'))+sorted((H/'satellite').glob('07*.pdf')):
 with fitz.open(f) as src:
  p=src[0];compare=f.stem.startswith(('06','07'))
  w,h=fitz.paper_size('a3' if compare else 'a4')
  if not compare:w,h=h,w
  target=fitz.Rect(28,28,w-28,h-28);scale=min(target.width/p.rect.width,target.height/p.rect.height)
  fonts=[s['size'] for b in p.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
  minimum=min(fonts)*scale
  assert minimum>=9,(f.name,minimum)
  q=out.new_page(width=w,height=h);q.show_pdf_page(target,src,0)
  audit.append(dict(file=f.name,paper='A3 portrait' if compare else 'A4 landscape',minimum_print_font_pt=round(minimum,2),scale=round(scale,4)))
out.save(H/'print_ready_maps.pdf',deflate=True)
(H/'print_audit.json').write_text(json.dumps(audit,indent=2))
print(audit)
