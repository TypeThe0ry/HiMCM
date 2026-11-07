from pathlib import Path
import json,html
import pymupdf as fitz
from PIL import Image,ImageDraw,ImageFont
H=Path(__file__).resolve().parent;ROOT=H.parents[3];(H/'excerpts').mkdir(exist_ok=True)
items=[
('13904',2023,11,(.13,.23,.87,.552),'首选：斯德哥尔摩公交网络','道路与站点地图','灰色海岸与行政边界作底，线路和站点着色，右下角放大中心区。适合本题展示学校、公共设施与交通可达性。'),
('13904',2023,21,(.04,.70,.96,.91),'首选：上海不同阶段公交网络','同域对照地图','两张图保持地理范围与底图一致，颜色表达线路状态；适合修订前后或不同通学阈值的覆盖对照。'),
('16742',2025,12,(.115,.435,.885,.79),'首选：六项指标的美国城市地图','多指标地理小多图','相同底图、城市点位与共用色标。适合25城指标的空间分布。原图文字较小，本题应扩大面板、减少底图地名。'),
('16738',2025,9,(.065,.25,.96,.58),'推荐：美国城市树冠覆盖','城市点位专题地图','浅色底图与单一绿色色标，城市位置清楚。适合城市分布或单一指标的空间概览。'),
('13719',2023,7,(.09,.065,.91,.385),'推荐结构：全球14个研究地点','全球定位地图','世界底图标出研究点。适合候选城市总览；底图色彩和地名较密，正式重绘宜降低饱和度。'),
('16738',2025,8,(.08,.745,.92,.95),'补充：拉斯维加斯与纽约交通图','城市街道路网','真实道路、河流与路况着色；可参考道路细节，但不直接把原截图当成本题新数据。'),
('14076',2023,14,(.10,.222,.90,.545),'补充：巴西与印度气候区','分区设色地图','用类别色标区分气候区，含地点、指北针和比例尺。适合解释城市环境背景，不宜照搬过多高饱和色。'),
('13904',2023,20,(.035,.66,.97,.885),'补充：芝加哥公交改造','同域对照地图','规则道路网配浅灰底图，局部放大显示细节。适合城市级出行或设施服务范围对比。'),
('13904',2023,22,(.035,.065,.97,.29),'补充：上海后期公交改造','同域对照地图','延续相同底图和图例，便于跨阶段比较；这里只摘地图，不收录下方折线图。'),
('12384',2021,6,(.27,.075,.70,.445),'特殊用途：湖泊等深线','地形等值线地图','黑白等值线、指北针、比例尺。地理表达清楚，但与本题城市比较的直接关联较弱。'),
]
rows=[];doc=fitz.open();font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',22)
cat=json.loads((ROOT/'library/catalog.json').read_text())
for k,(team,year,page,box,title,kind,note) in enumerate(items,1):
 item=next(r for r in cat if str(r['team'])==team);src=ROOT/'library'/item['path'];d=fitz.open(src);p=d[page-1];w,h=p.rect.width,p.rect.height
 out=f'excerpts/{k:02d}_{team}_p{page:02d}.png';p.get_pixmap(matrix=fitz.Matrix(2.5,2.5),clip=fitz.Rect(box[0]*w,box[1]*h,box[2]*w,box[3]*h)).save(H/out)
 row=dict(team=team,year=year,award=item['award'],pdf_page=page,title=title,type=kind,note=note,source=str(src.relative_to(ROOT)),image=out,clip_fraction=box);rows.append(row)
 q=doc.new_page(width=842,height=595);q.insert_text((30,30),f'{year} / {item["award"]} / Team {team} / PDF p.{page} / Map excerpt {k}',fontname='tiro',fontsize=12);q.insert_image(fitz.Rect(30,50,812,550),filename=str(H/out),keep_proportion=True);q.insert_text((30,575),'Original map excerpt for style reference. Not the current team\'s data or analysis.',fontname='tiro',fontsize=9)
doc.save(H/'maps_only.pdf');(H/'map_sources.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
css='body{max-width:1150px;margin:35px auto;padding:0 24px;font-family:Georgia,"Songti SC",serif;line-height:1.7;color:#252525}img{max-width:100%;max-height:760px;display:block;margin:20px auto}section{border-top:1px solid #aaa;padding:24px 0}a{color:#36576f}h1{font-size:30px}h2{font-size:21px}.meta{color:#777}'
sections=[]
for r in rows:
 sections.append(f'<section><h2>{r["title"]}</h2><p class="meta">{r["year"]} · {r["award"]} · Team {r["team"]} · PDF p.{r["pdf_page"]} · {r["type"]}</p><a href="{r["image"]}"><img loading="lazy" src="{r["image"]}"></a><p>{r["note"]}</p><a href="../../../../{r["source"]}#page={r["pdf_page"]}">原始论文及页码</a></section>')
(H/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>获奖论文地图专项摘录</title><style>'+css+'</style><h1>只看地理地图</h1><p>从馆藏论文中筛选：实际地理位置、海岸、道路、行政分区或等深线。排除统计图、热力矩阵、流程图和没有地理底图的模拟散点图。本轮精选10份地图区域，部分包含多幅地图；不是全库地图穷尽清单。</p><p><a href="maps_only.pdf">地图专项PDF</a> · <a href="map_sources.json">来源与裁剪记录</a></p>'+''.join(sections))
canvas=Image.new('RGB',(1800,1650),'#F1F0ED');dr=ImageDraw.Draw(canvas)
for j,r in enumerate(rows[:6]):
 im=Image.open(H/r['image']).convert('RGB');im.thumbnail((850,470));x=j%2*900+(900-im.width)//2;y=j//2*550+55;canvas.paste(im,(x,y));dr.text((j%2*900+25,j//2*550+15),f"{r['year']} / Team {r['team']} / PDF p.{r['pdf_page']}",font=font,fill='#444')
canvas.save(H/'map_preview.jpg',quality=94)
print('10 map excerpts, map-only PDF and source-linked gallery generated.')
