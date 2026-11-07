from pathlib import Path
import fitz,json,re,html,csv
from PIL import Image,ImageOps,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent/'award_atlas'; OUT.mkdir(exist_ok=True)
(OUT/'pages').mkdir(exist_ok=True)
rows=[]; coverage=[]; picked=[]
for item in json.loads((ROOT/'library/catalog.json').read_text()):
 p=ROOT/'library'/item['path']; doc=fitz.open(p); n=0
 for i,page in enumerate(doc):
  txt=page.get_text(); blocks=page.get_text('blocks')
  caps=[b[4].strip().replace('\n',' ') for b in blocks if re.match(r'^\s*(?:Figure|Fig\.?|图)\s*\d+',b[4],re.I)]
  images=[x for x in page.get_image_info() if (x['bbox'][2]-x['bbox'][0])*(x['bbox'][3]-x['bbox'][1])>6000]
  drawings=page.get_drawings()
  # A page-level archive preserves vector plots, legends and original captions.
  if not caps and not images and len(drawings)<35: continue
  # Exclude ordinary tables detected only as vector rules; caption/image candidates remain.
  if not caps and not images and re.search(r'\bTable\s*\d+',txt) and len(drawings)<80: continue
  key=p.stem+f'_p{i+1:02d}'; filename='pages/'+key+'.jpg'
  pix=page.get_pixmap(matrix=fitz.Matrix(1.3,1.3),alpha=False)
  pix.pil_save(str(OUT/filename),format='JPEG',quality=83)
  reason='caption' if caps else 'image' if images else 'vector_candidate'
  row=dict(year=item['year'],award=item['award'],team=item['team'],pdf_page=i+1,source_pdf=str(p.relative_to(ROOT)),image=filename,captions=' | '.join(caps),detection=reason)
  rows.append(row);n+=1
  if item['team'] in {'14995','15041','15504','15926','16442','16738','16739'} and caps and len([r for r in picked if r['team']==item['team']])<3: picked.append(row)
 coverage.append(dict(team=item['team'],source=item['path'],pages=len(doc),candidate_pages=n,has_text=any(p.get_text().strip() for p in doc)))
with (OUT/'index.csv').open('w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2))
styles='body{font-family:Georgia,serif;background:#f6f4ef;color:#26343d;margin:30px}h1{font-size:28px}input{padding:12px;width:65%;margin:15px 0}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:20px}.card{background:white;padding:14px;border:1px solid #ddd}img{width:100%}p{font-size:13px;line-height:1.5}a{color:#315b70}'
cards=[]
for r in rows:
 label=f"{r['year']} · {r['award']} · Team {r['team']} · PDF p.{r['pdf_page']}"
 source='../../../../'+r['source_pdf']+f"#page={r['pdf_page']}"
 cards.append(f'<article class="card"><h3>{label}</h3><a href="{r["image"]}"><img loading="lazy" src="{r["image"]}"></a><p>{html.escape(r["captions"] or "无可识别图题：图像或矢量候选页，需人工复核")}</p><a href="{source}">原始 PDF 与页码</a><p>检测方式：{r["detection"]}</p></article>')
(OUT/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>获奖论文图页参考库</title><style>'+styles+'</style><h1>获奖论文 · 原图页参考库</h1><p>本地研究参考，保留原文图题与版式；不是本队结果。自动检索所有馆藏论文，候选页可能含表格或装饰，也可能漏掉无图题的矢量图。禁止将原图当作本队结果。</p><p>'+f'{len(coverage)}篇论文 · {len(rows)}个候选图页'+'</p><input placeholder="搜索年份、队号、Figure、关键词" oninput="document.querySelectorAll(\'.card\').forEach(x=>x.hidden=!x.innerText.toLowerCase().includes(this.value.toLowerCase()))"><div class="grid">'+''.join(cards)+'</div>')
thumbs=picked[:21]; sheet=Image.new('RGB',(4*330,((len(thumbs)+3)//4)*470),'#f5f3ee');d=ImageDraw.Draw(sheet)
for j,r in enumerate(thumbs):
 im=Image.open(OUT/r['image']);im.thumbnail((310,425));x=(j%4)*330+10;y=(j//4)*470+30;sheet.paste(im,(x,y));d.text((x,y-20),f"{r['year']} / {r['team']} / p.{r['pdf_page']}",fill='#26343d')
sheet.save(OUT/'style_contact_sheet.jpg',quality=90)
print(json.dumps({'papers':len(coverage),'candidate_pages':len(rows),'contact_sheet':str(OUT/'style_contact_sheet.jpg'),'zero_candidate':[x for x in coverage if x['candidate_pages']==0]},ensure_ascii=False))
