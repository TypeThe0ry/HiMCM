#!/usr/bin/env python3
"""Independent offline audit of current auxiliary spatial figure and manuscript."""
import hashlib,json,math,zipfile,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
R=Path('/data/projects/HiMCM/research/2026-a'); ROOT=R.parents[1]; V=R/'visuals/current_spatial'; P=Path('/data/projects/HiMCM-Overleaf'); PDF=Path('/data/scratch/himcm-current-spatial-final-build/main.pdf'); OUT=R/'results/current_spatial_review'; OUT.mkdir(exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(*args): return subprocess.check_output(args,text=True)
source=json.loads((R/'data/task4_access/manifest.json').read_text()); claimed=json.loads((V/'metrics.json').read_text()); metrics=[]
for city,code,lat,km in [('Singapore','8133',1.35,5),('Zurich','9808',47.38,2)]:
 f=R/'data/task4_access'/f'{code}_hexes.zip'; h=sha(f); assert h==next(x['sha256'] for x in source if x['file']==f.name)
 fs=json.loads(zipfile.ZipFile(f).read('hexes.geojson'))['features']; positives=[]; coords=[]
 for item in fs:
  pop=item['properties']['population']; assert pop is not None and math.isfinite(pop) and pop>=0
  for lon,latitude,*_ in item['geometry']['coordinates'][0]:
   coords.append((6378137*math.radians(lon),6378137*math.log(math.tan(math.pi/4+math.radians(latitude)/2))))
  if pop>0: positives.append((pop,item['properties']['c_f']))
 good=[(p,t) for p,t in positives if t is not None and math.isfinite(t) and t>0]; total=math.fsum(p for p,t in positives); valid=math.fsum(p for p,t in good); within=math.fsum(p for p,t in good if t<=30); x,y=zip(*coords); dx=max(x)-min(x);dy=max(y)-min(y);bounds=[min(x)-.06*dx,min(y)-.06*dy,max(x)+.06*dx,max(y)+.06*dy]
 c=next(a for a in claimed if a['city']==city); assert len(fs)==c['total_cells'] and len(positives)==c['populated_cells'] and abs(total-c['retained_residents'])<1e-6 and abs(within/valid-c['within_30_share_of_valid'])<1e-12 and all(abs(a-b)<1e-7 for a,b in zip(bounds,c['bounds_3857']))
 # WGS84 prime-vertical radius, correcting Web Mercator's spherical latitude scale.
 rad=math.radians(lat); N=6378137/math.sqrt(1-0.00669437999014*math.sin(rad)**2); approx=km*N/6378137
 metrics.append(dict(city=city,zip_sha256=h,total_cells=len(fs),positive_cells=len(positives),unknown_residents=total-valid,retained_residents=total,within30_residents=within,within30_share=within/valid,max_minutes=max(t for p,t in good),bounds_epsg3857=bounds,scale_bar_km_wgs84_approx=approx))
manifest_hashes={}; raw={}
for name in ('imagery_manifest.json','fallback_manifest.json'):
 p=V/name; manifest_hashes[name]=sha(p); rows=json.loads(p.read_text()); rows=rows if isinstance(rows,list) else [rows]
 for row in rows:
  f=V/row['path']; assert sha(f)==row['sha256']; raw[row['path']]=sha(f)
assert len(raw)==7
snap=R/'design/task4_user_v200_snapshot.json'; bindings=json.loads(snap.read_text())['source_sha256']; mismatches={name:{'expected':h,'actual':sha(R/name) if (R/name).is_file() else None} for name,h in bindings.items() if not (R/name).is_file() or sha(R/name)!=h}; assert len(bindings)==407 and not mismatches
figure=V/'city_walktime.pdf'; assert sha(figure)==sha(P/'figures/walktime_context.pdf'); text=(P/'main.tex').read_text(); assert len(re.findall(r'\\bibitem\{',text))==59
pages=run('pdftotext','-layout',str(PDF),'-').split('\f'); pages=[p for p in pages if p.strip()]; ai=next(i+1 for i,p in enumerate(pages) if 'Report on Use of AI Tools' in p and 'Documentation status:' in p); figpage=next(i+1 for i,p in enumerate(pages) if 'Walking time across retained city grids' in p); news=next(i+1 for i,p in enumerate(pages) if 'A city choice built around a student' in p); assert len(pages)<=27 and ai-1<=25 and len(pages)-ai+1==2
assert 'Summary Sheet' in ' '.join(pages[0].split()) and 'Choosing a City for High-School Life with Incomplete Evidence' in ' '.join(pages[0].split())
assert all('Team # 18213' in p and f'Page {i} of {len(pages)}' in p for i,p in enumerate(pages[1:],2))
xml=OUT/'figure_page.xml'; subprocess.run(['pdftohtml','-xml','-i','-f',str(figpage),'-l',str(figpage),str(PDF),str(xml)],check=True,stdout=subprocess.DEVNULL); tree=ET.parse(xml); specs={f.attrib['id']:int(f.attrib['size'])/1.5 for f in tree.findall('.//fontspec') if 'DejaVuSans' in f.attrib['family']}; used=[specs[t.attrib['font']] for t in tree.findall('.//text') if t.attrib['font'] in specs]; assert used and min(used)>=9; xml.unlink()
output=dict(status='pass',scope='Independent offline geometry/numeric/provenance and local compiled layout audit; original POI ground truth, individual access and online Overleaf compile not certified',pdf_sha256=sha(PDF),main_tex_sha256=sha(P/'main.tex'),total_pages=len(pages),main_reference_pages=ai-1,ai_pages=len(pages)-ai+1,figure_page=figpage,news_page=news,reference_count=59,header_and_footer='Pages 2 onward checked Team # 18213 and Page x of y; footer content not machine-certified; registration provisional',minimum_figure_font_pt_poppler_rounded=min(used),figure_pdf_sha256=sha(figure),figure_source_and_overleaf_identical=True,metrics=metrics,manifest_sha256=manifest_hashes,raw_imagery_sha256=raw,snapshot_sha256=sha(snap),science_bindings_checked=len(bindings),science_binding_mismatches=mismatches,figure_claims='Modelled grid mean to 20 generic Learning POIs, not student trips or pool access; snapshot 2026-11-07; source city dates unknown; Zurich WMS request date is not verified granule acquisition',limitations='Scale bars approximate WGS84 east-west distance at stated latitude; 3D heights and colors share 0–150 min; no physical elevation. Visual occlusion and full-page legibility require visual review.')
(OUT/'verification.json').write_text(json.dumps(output,indent=2)+'\n'); print(json.dumps(output,indent=2))
