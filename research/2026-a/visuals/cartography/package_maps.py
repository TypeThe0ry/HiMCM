"""Refresh map collection and compact delivery archive."""
from pathlib import Path
import zipfile,json
import pymupdf as fitz
H=Path(__file__).resolve().parent
pdfs=sorted((H/'figures').glob('*.pdf'))
doc=fitz.open()
for p in pdfs:
 with fitz.open(p) as d:doc.insert_pdf(d)
doc.save(H/'maps_collection.pdf');doc.close()
items=pdfs+sorted((H/'figures').glob('*.png'))
items += [H/n for n in ['README.md','figure_includes.tex','candidate_city_locations.csv','city_map_audit.json','global_map_audit.json','city_map_captions.json','maps_collection.pdf','print_ready_maps.pdf','print_audit.json']]
with zipfile.ZipFile(H/'maps_and_style_guide.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in items:z.write(p,p.relative_to(H))
 for p in (H/'satellite').glob('*'):
  if p.is_file() and (p.suffix in ['.md','.json','.pdf'] or p.name.startswith('0')):z.write(p,p.relative_to(H))
 z.write(H.parent/'style_guide/style_guide.pdf','style_guide.pdf')
 z.write(H.parent/'GUIDELINES.md','GUIDELINES.md')
print('Refreshed map collection and delivery archive.')
