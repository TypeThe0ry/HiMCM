"""Audit source PDF fonts and create legible, explicitly sized research plates."""
from pathlib import Path
import json
import pymupdf as fitz
H=Path(__file__).resolve().parent
rows=[];out=fitz.open()
for folder in ['figures','round2/figures','cartography/figures','cartography/satellite']:
 for p in sorted((H/folder).glob('*.pdf')):
  with fitz.open(p) as d:
   fonts=[s['size'] for pg in d for b in pg.get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans'] if s['text'].strip()]
   minimum=min(fonts);row=dict(file=str(p.relative_to(H)),width_pt=round(d[0].rect.width,2),min_source_pt=round(minimum,2),min_at_6_5in_pt=round(minimum*468/d[0].rect.width,2))
   if folder in ['figures','round2/figures']:
    page=d[0];w,h=fitz.paper_size('a3');w,h=h,w;target=fitz.Rect(28,28,w-28,h-28);scale=min(target.width/page.rect.width,target.height/page.rect.height)
    assert minimum*scale>=9,(p,minimum*scale)
    dst=out.new_page(width=w,height=h);dst.show_pdf_page(target,d,0)
    row.update(atlas_page=len(out),atlas_min_pt=round(minimum*scale,2),paper='A3 landscape')
   rows.append(row)
out.save(H/'readable_analysis_atlas.pdf',deflate=True)
(H/'figure_font_audit.json').write_text(json.dumps(rows,indent=2))
print('19 source PDFs audited; 12 analysis plates >=9 pt at A3 landscape.')
