from pathlib import Path
import json,html
import pymupdf as fitz
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'award_atlas';(OUT/'selected').mkdir(exist_ok=True)
# Fractions refer to visually inspected original PDF pages; retain captions and watermarks.
items=[
('2025','16739',8,(.16,.299,.88,.61),'相关矩阵：完整色标、数值与图题','我们的指标矩阵使用单向色标；相关矩阵才使用以零为中心的双色标。'),
('2025','16739',8,(.12,.648,.87,.862),'双子图：共享叙事、分别标注','把同一问题的两个侧面并列，避免把不同尺度画在一条轴上。'),
('2024','14995',6,(.115,.21,.915,.43),'并列统计图：白底、细线、浅网格','可借鉴多面板结构与统一字体；不照搬原图的双轴。'),
('2025','16738',4,(.07,.065,.94,.40),'模型流程：分组框与层次结构','借鉴任务分组，改为低饱和配色，减少装饰。'),
('2025','16442',4,(.12,.045,.88,.55),'流程图：阶段分区和路径','让箭头表达先后关系，框中文字短而具体。'),
('2025','16442',9,(.17,.32,.84,.545),'横向排序：长标签易读','本题25城适合横排；用点和区间呈现不确定性。'),
('2024','15504',7,(.04,.56,.96,.84),'多类别对比：横向分组','适合类别少的构成比较；本题不同代理不直接堆叠为总量。'),
('2024','15041',11,(.058,.189,.535,.535),'黑白层次图：细边框与文字','黑白打印仍可辨识，适合模型步骤和公式链。'),
]
manifest=[];doc=fitz.open();thumbs=[]
for k,(year,team,page,box,title,lesson) in enumerate(items,1):
 src=next((ROOT/'library/papers'/year).rglob(f'*_{team}.pdf'));pdf=fitz.open(src);p=pdf[page-1];rect=p.rect;clip=fitz.Rect(box[0]*rect.width,box[1]*rect.height,box[2]*rect.width,box[3]*rect.height)
 fn=f'selected/{k:02d}_{team}_p{page:02d}.png';p.get_pixmap(matrix=fitz.Matrix(2,2),clip=clip).save(OUT/fn)
 manifest.append(dict(title=title,lesson=lesson,year=year,team=team,pdf_page=page,source=str(src.relative_to(ROOT)),crop=fn,clip_fraction=box))
 q=doc.new_page(width=595,height=842);q.insert_text((35,35),f'Reference {k:02d} | {year} | Team {team} | PDF page {page}',fontsize=11);q.insert_image(fitz.Rect(35,65,560,780),filename=str(OUT/fn),keep_proportion=True);q.insert_text((35,815),'Original paper excerpt. Style reference only; not results of the current team.',fontsize=8)
 im=Image.open(OUT/fn).convert('RGB');im.thumbnail((620,400));thumbs.append((im,f'{year} / Team {team} / PDF p.{page}'))
doc.save(OUT/'selected_styles.pdf');(OUT/'selected_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1320,1840),'#F4F3EF');d=ImageDraw.Draw(sheet)
for j,(im,label) in enumerate(thumbs):
 x=(j%2)*660+20;y=(j//2)*460+40;sheet.paste(im,(x,y));d.text((x,y-25),label,fill='#334455')
sheet.save(OUT/'selected_styles.jpg',quality=92)
body=''.join(f'<section><h2>{html.escape(r["title"])}</h2><p>{r["year"]} / Team {r["team"]} / PDF 第{r["pdf_page"]}页</p><img src="{r["crop"]}"><p>{r["lesson"]}</p></section>' for r in manifest)
(OUT/'selected.html').write_text('<meta charset="utf-8"><title>精选原图样式</title><style>body{max-width:1000px;margin:40px auto;font-family:serif;color:#26343d}img{max-width:100%}section{border-top:1px solid #ddd;padding:24px 0}p{line-height:1.7}</style><h1>获奖论文原图样式摘录</h1><p>8份具体图形摘录；保留出处、原图内容和水印。获奖不等于每张图都值得模仿，下面仅提取适用的排版原则。</p><a href="index.html">全部68篇候选图页图库</a>'+body)
print('8 curated excerpts created')
