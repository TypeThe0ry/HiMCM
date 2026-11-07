from pathlib import Path
import json,html
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent;ROOT=H.parents[3];A=H/'references';A.mkdir(exist_ok=True)
items=[
('14995',2024,4,(.117,.125,.912,.475),'首选 · 四分区模型总览','框架图','四个虚线分区；每区一种功能色；内部大小框有层级，箭头只表达依赖。','新版01保留四分区与分支结构，使用真正的研究步骤和公式。缩短标签、加大字号、减少无用节点。','01_framework'),
('13719',2023,16,(.094,.068,.91,.317),'首选 · 双面板细线曲线','机制与敏感性','Times字形、细黑全边框、无背景网格；藏蓝／玫红／金黄明确区分三组。','新版03沿用字体、轴框和三色关系。由于没有重复实验误差，不能仿画原图阴影带。','03_access_mechanism'),
('13719',2023,15,(.19,.072,.83,.572),'首选 · 空间小多图','城市内部差异','统一面板边框和排列，空间细节本身构成视觉重点，尺度写清楚。','新版02用三个真实城市的六边形网格，统一色标、独立比例尺；没有捏造底图或地标。','02_spatial_access'),
('13719',2023,22,(.145,.075,.84,.515),'推荐 · 排序条形图组','排名与对照','排序形成阅读顺序，颜色编码类别，图形紧凑，说明放在图下。','新版04保留全部25城，条形后直接给分数，并列展示三阶段排名；去掉装饰性大标题。','04_city_ranking'),
('15504',2024,18,(.057,.485,.945,.838),'推荐 · 分组柱与直接数值','均值／低尾／综合效用','每组重复同样的颜色次序；柱顶数值让读者不用猜。','新版03b沿用组内顺序和直接标数，采用蓝灰、浅绿、青灰，去掉原图立体高光。','03_access_mechanism'),
('14632',2023,8,(.075,.52,.875,.85),'推荐 · 机制示意而非口号框','测量机制','输入、空间对象和演化过程连成关系；图形承担解释任务。','新版01第三分区直接画居民网格、效用映射、均值与低尾的汇合；不复用蒲公英插图。','01_framework'),
('16739',2025,9,(.27,.53,.77,.785),'备选 · 横向条形与数值','结果排名','横向标签易读，条尾给数值，轴刻度明确。','新版04沿用横向条形和数值，但减少网格、将颜色留给三个机制案例。','04_city_ranking'),
('14632',2023,8,(.185,.19,.82,.44),'备选 · 三联函数图','参数影响','同一坐标结构重复三次；浅色带只标有数学含义的区间。','新版03采用同高三面板。没有适用区间证据时不增加背景阴影。','03_access_mechanism'),
]
entries=[];book=fitz.open();font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
for k,(team,year,page,bbox,title,kind,principle,transfer,new) in enumerate(items,1):
 src=next((ROOT/'library/papers'/str(year)).rglob(f'*_{team}.pdf'));pdf=fitz.open(src);p=pdf[page-1];r=p.rect;clip=fitz.Rect(bbox[0]*r.width,bbox[1]*r.height,bbox[2]*r.width,bbox[3]*r.height)
 fn=f'{k:02d}_{team}_p{page:02d}.png';p.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=clip).save(A/fn)
 entry=dict(id=k,team=team,year=year,pdf_page=page,title=title,kind=kind,principle=principle,transfer=transfer,crop='references/'+fn,source=str(src.relative_to(ROOT)),new_figure=new,clip_fraction=bbox);entries.append(entry)
 q=book.new_page(width=842,height=595);q.insert_text((35,30),f'Style reference {k} | {year} Team {team} | PDF page {page}',fontsize=12,fontname='tiro');q.insert_image(fitz.Rect(35,48,807,550),filename=str(A/fn),keep_proportion=True);q.insert_text((35,575),'Original excerpt: reference material, not the current team\'s result. Original watermarks retained.',fontsize=9,fontname='tiro')
book.save(H/'selected_reference_book.pdf');(H/'style_selection.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2))
# Three direct source / redraw comparisons, with unambiguous provenance.
for idx in [0,1,2]:
 e=entries[idx];ref=Image.open(H/e['crop']).convert('RGB');new=Image.open(H/'figures'/(e['new_figure']+'.png')).convert('RGB')
 ref.thumbnail((1050,780));new.thumbnail((1500,940));w=1600;hh=ref.height+new.height+170;canvas=Image.new('RGB',(w,hh),'#F2F0EC');dr=ImageDraw.Draw(canvas)
 dr.text((40,24),f'REFERENCE  |  {e["year"]} Team {e["team"]}, PDF p.{e["pdf_page"]}',font=font,fill='#444444');canvas.paste(ref,((w-ref.width)//2,65))
 yy=ref.height+105;dr.text((40,yy),'REDRAW  |  Current project data and model',font=font,fill='#444444');canvas.paste(new,((w-new.width)//2,yy+40));canvas.save(H/f'comparison_{idx+1:02d}.jpg',quality=94)
css='body{max-width:1120px;margin:42px auto;padding:0 24px;color:#282828;font-family:Georgia,"Songti SC",serif;line-height:1.7;background:#fff}h1{font-size:30px;font-weight:normal}h2{font-size:21px}h3{font-size:17px}a{color:#6e4561}img{display:block;max-width:100%;max-height:650px;margin:18px auto}section{padding:25px 0;border-top:1px solid #bbb}.pair{display:grid;grid-template-columns:1fr 1.3fr;gap:28px;align-items:center}small{color:#666}p{max-width:1000px}.tag{color:#8b4b61;font-size:14px}table{border-collapse:collapse}td,th{text-align:left;border-bottom:1px solid #ddd;padding:10px} @media(max-width:850px){.pair{display:block}}'
sections=[]
for e in entries:
 source='../../../../'+e['source']+f'#page={e["pdf_page"]}'
 sections.append(f'<section><p class="tag">{e["kind"]} · {e["year"]} · Team {e["team"]} · PDF p.{e["pdf_page"]}</p><h2>{e["title"]}</h2><div class="pair"><div><a href="{source}"><img src="{e["crop"]}" loading="lazy"></a><small>原论文摘录（点击查看原文）</small></div><div><a href="figures/{e["new_figure"]}.pdf"><img src="figures/{e["new_figure"]}.png" loading="lazy"></a><small>本题重绘（点击打开矢量PDF）</small></div></div><p><b>值得学：</b>{e["principle"]}</p><p><b>这次怎么改：</b>{e["transfer"]}</p></section>')
figs=json.loads((H/'figure_manifest.json').read_text());gallery=''.join(f'<section><h3>{r["name"]}</h3><img src="figures/{r["name"]}.png" loading="lazy"><p>{html.escape(r["caption"])}</p><p><a href="figures/{r["name"]}.pdf">PDF</a> · <a href="figures/{r["name"]}.svg">SVG</a> · <a href="figures/{r["name"]}.png">PNG</a></p></section>' for r in figs)
(H/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>获奖原图对照与第二版制图</title><style>'+css+'</style><h1>从具体获奖原图出发，重新制图</h1><p>本轮通过5张联系表浏览50个图页，放大检查关键原图，选出8份参考摘录。以下审美取舍是本次设计判断，不是获奖原因或质量评分。原文PDF页码与印刷页码可能不同。</p><p><a href="redesigned_figures.pdf">六张新版图 PDF</a> · <a href="selected_reference_book.pdf">精选原图 PDF</a> · <a href="../award_atlas/index.html">全部候选图页库</a> · <a href="README.md">数据边界和使用说明</a></p><h2>原图 → 本题重绘</h2>'+''.join(sections)+'<h2>六张新版图</h2>'+gallery)
print('Selected reference book, 3 direct comparisons and local gallery created.')
