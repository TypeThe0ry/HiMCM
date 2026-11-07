from pathlib import Path
import json,csv,re,html,collections,hashlib
import pymupdf as fitz
H=Path(__file__).resolve().parent;V=H.parent;ROOT=H.parents[3]
FONT=Path('/System/Library/Fonts/Supplemental/Arial Unicode.ttf')
rows=list(csv.DictReader((V/'award_atlas/index.csv').open(encoding='utf-8-sig')))
coverage=json.loads((V/'award_atlas/coverage.json').read_text())
selected=json.loads((V/'round2/style_selection.json').read_text());maps=json.loads((V/'maps/map_sources.json').read_text())
# Category labels represent page retrieval hints, not a manually verified inventory of figures.
rules={
 '地理地图':r'\bmap\b|geographical|geographic|bus line|transportation map|climate zones|bathymetric',
 '流程与模型框架':r'workflow|flow\s*chart|flow diagram|framework|model construction|model structure|hierarch|overview diagram|process framework',
 '机制与概念示意':r'life.cycle|schematic|mechanism|overview|transition diagram|diagram|concept',
 '排序与组间比较':r'rank|ranking|bar chart|scores?|comparison|compare|importance|weight',
 '趋势与拟合':r'curve|regression|growth|over time|trend|forecast|prediction|fit(?:ted|ting)?|time.series',
 '分布与残差':r'histogram|density|distribution|box\s*plot|boxplot|residual|frequency|probability|monte.carlo',
 '矩阵与相关性':r'heat\s*map|heatmap|correlation|loading|matrix',
 '敏感性与不确定性':r'sensitiv|uncertain|robust|interval|confidence|dependency|dependence|stability',
 '构成与权重流':r'pie chart|sankey|proportion|composition|energy structure|generation mix|weight distribution',
 '雷达与极坐标':r'radar|polar|semi.circle|spider',
 '模拟空间与三维图':r'dispersa|dispersion|spatial distribution|spread|3d|3-d|three.dimension|cellular automata|levy|lévy',
 '表格代码与非图形候选':r'source code|python code|chatgpt snapshot|variable definitions|baseline parameters'
}
manual={}
for r in maps:manual.setdefault((r['team'],int(r['pdf_page'])),set()).add('地理地图')
manual.update({('14995',4):{'流程与模型框架'},('13719',16):{'趋势与拟合','雷达与极坐标'},('13719',15):{'模拟空间与三维图'},('13719',22):{'排序与组间比较','敏感性与不确定性'},('15504',18):{'排序与组间比较'},('14632',8):{'机制与概念示意','趋势与拟合'},('16739',9):{'分布与残差','排序与组间比较','构成与权重流'},('16739',8):{'矩阵与相关性','排序与组间比较'},('16738',20):{'雷达与极坐标'}})
classified=[];counter=collections.Counter()
for r in rows:
 txt=r['captions'];cats=[];matched={}
 for cat,pat in rules.items():
  scan=re.sub(r'heat\s*map|heatmap','',txt,flags=re.I) if cat=='地理地图' else txt
  m=re.search(pat,scan,re.I)
  if m:cats.append(cat);matched[cat]=m.group(0)
 key=(str(r['team']),int(r['pdf_page']));reviewed=key in manual
 if reviewed:
  cats=sorted(set(cats)|manual[key]);basis='selected_reference_visual_check_plus_caption_rules'
 elif txt:basis='caption_keyword_rules_only'
 else:basis='no_readable_caption_unclassified'
 if not cats:cats=['未分类待复核']
 counter.update(cats)
 out={**r,'categories':' | '.join(cats),'classification_basis':basis,'review_status':'selected_reference_page_reviewed' if reviewed else 'not_individually_reviewed','matched_terms':json.dumps(matched,ensure_ascii=False),'preview_path':'../award_atlas/'+r['image']}
 classified.append(out)
with (H/'page_style_index.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(classified[0]));w.writeheader();w.writerows(classified)
(H/'page_style_index.json').write_text(json.dumps(classified,ensure_ascii=False,indent=2))
summary={'paper_count':len(coverage),'candidate_page_count':len(rows),'selected_reference_pages':sum(r['review_status']=='selected_reference_page_reviewed' for r in classified),'category_page_counts_nonexclusive':dict(counter),'method':'Multi-label caption keyword retrieval, augmented by explicit labels for selected visually reviewed reference pages. No image classifier or exhaustive visual review. Counts are candidate pages, not individual figures.','input_sha256':hashlib.sha256((V/'award_atlas/index.csv').read_bytes()).hexdigest()}
(H/'classification_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
# Specific examples retain the original image and provenance; generated art is not treated as evidence.
refs=[]
for r in maps[:8]:refs.append(dict(title=r['title'],team=r['team'],year=r['year'],page=r['pdf_page'],source=r['source'],image='../maps/'+r['image'],note=r['note']))
for r in selected:refs.append(dict(title=r['title'],team=r['team'],year=r['year'],page=r['pdf_page'],source=r['source'],image='../round2/'+r['crop'],note=r['principle']+' '+r['transfer']))
for team,year,page,title,note in [('16739',2025,8,'矩阵：图例范围与数值编码','相关矩阵与指标分数矩阵要使用不同的色标逻辑；原文的正负相关可以使用以零为中心的双色标。'),('16739',2025,9,'箱线与残差：统计量的定义先于样式','原图将残差、系数与排序并排。箱体和须必须有真实分布支持，不能把单个城市分数伪装成分布。'),('16738',2025,20,'雷达图：可作画像，不作精确排名','少量城市叠加可看轮廓，但轴顺序和面积容易改变印象；本题25城不用一张雷达图堆叠。')]:
 r=next(r for r in rows if r['team']==team and int(r['pdf_page'])==page);refs.append(dict(title=title,team=team,year=year,page=page,source=r['source_pdf'],image='../award_atlas/'+r['image'],note=note))
(H/'reviewed_reference_cards.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2))
sections=[
('地图 1｜25座城市的全球分布', '13719 / 2023 / PDF p.7；16738 / 2025 / PDF p.9', '../maps/excerpts/05_13719_p07.png', [
'目的：先交代研究对象在哪里；不把一张定位图强行做成排名、气候、收入、人口四合一。25城必须全部出现，图上名称须与候选CSV一一对应。',
'底图：真实海岸线、陆地和国界；全球图不需要街道。选适合全球展示的投影，避免直接用经纬度散点坐标轴冒充地图。正文标注底图来源和下载版本。',
'版面：全球主图占约三分之二至四分之三画面；欧洲、南亚、东亚点位密集时用放大窗或编号索引。放大窗框出母图范围，不能让读者以为是另一组样本。',
'视觉：海洋用很浅的蓝灰，陆地用暖白，边界为细灰线；候选城市用一种强调色，选中的内部地图案例再用另一种点形。不要让深色地形或密集地名盖过25个点。',
'标注：同一字体，城市名与点保持稳定距离；必要时用细引线。不要为了避让把点移到错误的地理位置。跨日界线的投影应保证东京、墨尔本等不被切开。',
'本题图注：25座候选城市的地理分布，点表示源数据采用的城市参考坐标，不代表精确行政中心或统一都市区边界。城市候选身份不等于最终评估结果。']),
('地图 2｜城市内部可达性', '13904 / 2023 / PDF pp.11、20–22；16742 / 2025 / PDF p.12', '../maps/excerpts/01_13904_p11.png', [
'目的：让读者看见城市内部“哪些位置更容易到达学习设施”，并解释平均值为什么可能遮蔽不便利地区。地图必须有地理参照，不能只展示悬空六边形轮廓。',
'层次：底层放真实海岸、水域和主要道路；中层放可达性网格；最上层保留少量地名、比例尺、图例与指北方向。底图应淡，网格是主角，道路仍可辨认。',
'网格：直接用归档GeoJSON几何，坐标系正确转换后再绘制。颜色编码时间或效用二选一，并明确方向。时间高=较难到达；效用高=较易到达，不能混用。',
'空白：保留网格外区域不涂成“低可达性”；无效时间不涂成最好。未覆盖、零人口、无效数据与真实低效用要在图注或图例区分。',
'放大窗：借鉴13904的局部放大，展示中心区道路与网格。窗口里可重新设置比例尺，但不能独立拉伸色标。主图与放大窗都要说明范围。',
'本题限制：当前Learning字段是到邻近20个同类POI的模型时间，人口是全年龄居民。图中不写“高中生通学时间”“教育质量”或“最近高中”，也不凭空补学校位置。']),
('地图 3｜同域对照与地理小多图', '13904 / 2023 / PDF p.21；16742 / 2025 / PDF p.12', '../maps/excerpts/03_16742_p12.png', [
'同城对照：前后或两种方案必须使用同一范围、投影、底图、色标和图层顺序。不能让自动缩放制造“改善很大”的印象。',
'跨城对照：若地图范围不同，每幅独立标比例尺并在图注直说。城市面积差异很大时，可提供统一物理尺度的局部图作为补充，而不是只统一画框大小。',
'面板：两到四幅大地图通常比六幅小邮票更易读；统一左上角(a)(b)(c)和城市名。共用色标放在整组下方，不为每幅重复占位。',
'色标：时间建议有明确单位和阈值的连续或分级色标；效用固定0–1。分级阈值属于分析选择，应在说明中记录。',
'不要误用：这类专题地图属于地图，即使颜色表达数值；相关矩阵不是地图。模型散点若没有真实地理定位，也不能写成实际城市底图。']),
('框架｜四分区模型总览', '14995 / 2024 / PDF p.4，Figure 1', '../round2/references/01_14995_p04.png', [
'学的是结构：按任务划分四个区域，每区一种功能色，内部按输入→处理→输出连接。不是把整篇摘要拆成六个一样的大框。',
'本题四区：候选城市与代理指标；基准评价；网格可达性与低尾；修订检验及未知教育证据。两个实验应分开画，不用一条箭头混成同一个结论。',
'框中文字：每个节点只表达一个操作或结果，约一至两行；公式保留能解释机制的核心关系，不写段落。',
'线与边框：分区外框可用0.6–0.8pt细虚线，内部实线0.5–0.7pt。箭头贴近被连接的框，避免线压字、无起点和装饰性循环。',
'颜色：珊瑚、浅金、淡紫、薄荷按任务分工，填色轻、文字深。不要在同一框里叠渐变、阴影、图标和高光。']),
('机制｜把模型对象画出来', '14632 / 2023 / PDF p.8，Figure 4', '../round2/references/06_14632_p08.png', [
'参考图的可取之处是把环境输入、空间对象与演化过程放在同一图中，使读者能看到变量作用在哪里。蒲公英插画不属于本题，不照搬。',
'本题可以画居民网格→时间t→效用exp(-t/30)→人口加权均值与最差20%→综合Q。若放地图小窗，它应来自真实城市数据。',
'机制图可含示意格子，但须标“示意”；示意不能与实测地图拼接后不给边界。所有数字例子须说明是推导、假设或实证。',
'优先用形状承担解释：一个网格代表一个空间单元、箭头表示计算方向、括号表示聚合；不要放没有解释意义的电脑、云朵、城市天际线。']),
('比较｜排名、分组与构成', '13719 / 2023 / PDF p.22；15504 / 2024 / PDF p.18；16739 / 2025 / PDF p.9', '../round2/references/05_15504_p18.png', [
'城市名较长时使用横向条或点图；完整25城的排名应完整呈现，重点城市用颜色或注释强调，不因美观任意删除。',
'柱状图从零开始。条尾直接标数值时保留合理精度，通常一位或两位小数；避免用3D高光改变长度感知。',
'分组柱的组内顺序固定，颜色只表示同一个统计量。跨图同一颜色若代表城市，其他面板不要又用它表示均值。',
'不同单位的代理指标不能随意堆叠。百分比构成需有共同分母；Sankey宽度必须对应可相加的数量或权重，不能凭视觉随意画粗细。',
'排名变动最好同时保留基准、只加均值、再加低尾三个阶段；图注说明模型发生变化，不宣称城市现实变好。']),
('曲线｜趋势、拟合与敏感性', '13719 / 2023 / PDF p.16；14632 / 2023 / PDF p.8', '../round2/references/02_13719_p16.png', [
'借鉴细轴框、Times字形、藏蓝/玫红/金黄三条清楚的线。给每条线额外的点形或线型，灰度打印仍能辨认。',
'时间序列、经验拟合和解析函数要分清：原始点用散点，拟合用线，模型假设的参数扫描明确称“敏感性”。不能把人为参数曲线写成观测趋势。',
'阴影带必须有数学定义：置信区间、标准差范围或情景边界。当前没有重复实验误差时，不为好看仿画原图误差带。',
'同组面板尽量共享单位和刻度；只保留轻网格或不用网格。每幅小图短标题说明变量，整张图的解释放图注。',
'本题低尾权重λ变化是规范性选择，不是时间变化；固定其他输入后画Q(λ)，图中标主情景λ=0.3。']),
('分布｜箱线、残差与累积分布', '16739 / 2025 / PDF p.9；13719 / 2023 / PDF p.16', '../award_atlas/pages/himcm_2025_b_outstanding_16739_p09.jpg', [
'箱线和直方图需要一组观测或明确的模型抽样；每城只有一个总分时，不得制造箱体。须与异常点规则必须说明。',
'居民网格的时间或效用可画人口加权累积分布，比只画平均值更能呈现内部差异。注明分母是保留人口，不是学生样本数。',
'各城分布比较使用同一横轴范围和同一权重规则。若时间长尾很长，截轴或对数轴要明确写出，不能默默裁掉。',
'最低20%人口的聚合应按人口质量而不是网格个数计算，分位边界可使用部分权重。地图面积分布不等于人口分布。']),
('矩阵｜相关性与指标画像', '16739 / 2025 / PDF p.8，Figures 1–3', '../award_atlas/pages/himcm_2025_b_outstanding_16739_p08.jpg', [
'相关系数用以0为中心的双色标，范围固定[-1,1]；0–1收益方向分数用单向色标。不能用同一色谱暗示它们数学含义一样。',
'行列标签、排序规则和色标三者齐全。25城×5项可横排为5行，放横向附录；正文缩小后文字小于9pt时应拆成分组图。',
'单元格数字要克制精度，深色格用浅字、浅色格用深字，网格线细白即可。缺失值用独立灰色或符号，不涂成零。',
'相关性用于诊断重复信息或结构，不是因果证据。不要只因获奖论文用了PCA热图就给本题增加无作用的PCA图。']),
('不确定性｜界限、区间与可行集合', '13719 / 2023 / PDF p.16（视觉参照）；本题归档可行区间分析', '../round2/figures/05_evidence_uncertainty.png', [
'本题使用“可行分数区间”：未知指标在允许范围内变化得到的边界，不是统计置信区间，也不是城市胜率。样式可借鉴细线区间，措辞必须忠于计算。',
'同一城市补证据前后的区间可粗灰底线＋细深色线叠放；前后模型和权重相同才能把区间收缩归因于信息增加。',
'可能冠军用空心点或额外符号标注，不能仅依赖红绿配色。明确“可能”不是“必然”，当前教育质量仍未知。',
'代理误差的横轴写“假设误差宽度”，不要写“实测标准误”。在允许误差扩大时可能冠军集合如何变化，可单独用小面板说明。']),
('多面板｜用排列建立证据链', '13719 / 2023 / PDF pp.15–16、22；16742 / 2025 / PDF p.12', '../round2/references/03_13719_p15.png', [
'每个面板承担一个问题：地图显示哪里，分布显示多少人口，机制曲线显示为什么。避免把互不相关的漂亮图拼成一页。',
'先确定最终印刷宽度，再决定2、3还是4个面板。城市地图通常2–3幅；25城排名一幅完整长图；五指标矩阵适合横向页面。',
'同类面板边框、标题位置、标签间距一致。只共用真正可比的色标和坐标；不同尺度面板必须在图注说明。',
'地图缩略图与局部放大图用框和引线标关系；局部图不应覆盖最关键的主图区域。不同城市放大区的选择要有解释。']),
('备选｜雷达、极坐标与三维', '16738 / 2025 / PDF p.20；13719 / 2023 / PDF p.16', '../award_atlas/pages/himcm_2025_b_outstanding_16738_p20.jpg', [
'雷达图只适合少数城市的同尺度多指标画像；轴顺序改变面积，重叠多时读不清，不能用多边形面积直接排名。25城全部放一张雷达图不采用。',
'极坐标只有角度真有意义时采用，例如方向性风、出行方向；仅为造型把城市排成圆环会增加阅读成本。',
'三维图只有第三维承载必要量时采用；表面遮挡、透视与颜色须可解释。二维位置＋颜色已经够用时不加3D。',
'原图图片、插画、代码截图、表格截图在图库中可能被检测为图页。它们不能自动算作已确认的科学图形，也不能从获奖身份推断质量。'])
]
(H/'style_sections.json').write_text(json.dumps([{'title':t,'reference':r,'image':im,'rules':rr} for t,r,im,rr in sections],ensure_ascii=False,indent=2))
intro=f'''# 获奖论文图片风格蒸馏与本题制图规范

2026-11-07。目标：把具体获奖论文的视觉做法转成能用于本题的地图、模型图与分析图规范，而不是套一个统一“AI论文模板”。本文件为研究附件，未替换论文正文。

## 范围与证据等级

- 全库索引覆盖 **{len(coverage)}篇馆藏论文、{len(rows)}个候选图页**；候选页不等于独立图片，可能包含表格、装饰、扫描页或多个图。
- 全部候选页已经生成可复现的多标签类别索引。类别由图题关键词匹配，部分精选参考页补充人工视觉标签。**没有声称998页均已逐图人工审美审阅。**
- 前轮通过联系表浏览50页；本指南以已有精选地图、8份重绘参考及补充检查的矩阵/残差/雷达页作为具体视觉依据。本指南收录{len(refs)}张来源卡，跨{summary['selected_reference_pages']}个精选参考页在索引内标记。
- 评价“值得参考”是本题的设计判断，不是获奖因果，也不表示获奖论文的每张图都好。Outstanding、Finalist等奖项以原始索引为准。

[图文版](index.html) · [便携PDF](style_guide.pdf) · [全库分类检索](catalog.html) · [分类CSV](page_style_index.csv) · [分类JSON](page_style_index.json) · [方法与数量](classification_summary.json)

## 本题先采用的视觉路线

**地图优先跟13904队：浅灰真实底图、彩色数据层、清楚的局部放大。全球定位参考13719队，多指标地理面板参考16742队；框架跟14995队，统计线图跟13719队。** 不要求每张图长得一样，只要求同一种视觉编码全篇保持含义一致。

第一版的问题不是“不够花哨”，而是无地理参照的空间图、大号宣传式标题、统一卡片构图和过多图内说明。第二版改善了字体与结构；这轮真实底图必须补齐海岸、道路等地理语境，同时保持数据层可读。

## 全库分类结果（页级，多标签）

| 类别 | 候选页数 | 解释 |
|---|---:|---|
'''
for c,n in counter.most_common():intro+=f'| {c} | {n} | '+('无可识别类别，需人工复核' if c=='未分类待复核' else '图题规则命中或精选参考人工补充；不是独立图片数量')+' |\n'
intro+='\n同一页可以出现地图、折线、流程图，因此类别数量不能相加当作总图数。无图题页保留为未分类，不依据文件存在就猜测其风格。\n'
md=intro
for title,ref,img,rr in sections:
 md+='\n## '+title+'\n\n参考：'+ref+'。\n\n!['+title+']('+img+')\n\n'+'\n\n'.join(f'{i+1}. {x}' for i,x in enumerate(rr))+'\n'
ending='''
## 统一制作参数：这是本队建议，不是从原图精确测得

| 元素 | 建议值／做法 |
|---|---|
| 字体 | 英文Times New Roman或与正文字体协调的衬线体；同一图不混用多套英文字体 |
| 最终字号 | 图例、说明、刻度和署名至少9pt；主标签10–11pt；面板标题11–12pt；按插入论文后的尺寸检查 |
| 线宽 | 坐标与行政边界0.4–0.7pt；关键曲线1.0–1.4pt；地图道路层随级别细分，不能全用粗线 |
| 分析线色 | 藏蓝 #46566F、玫红 #B33561、金黄 #E9A33B；同时用点形或线型区分 |
| 底图 | 水域浅蓝灰、陆地暖白、边界淡灰；道路清晰但不抢过数据层 |
| 顺序色标 | 一项连续量由浅到深；跨地图固定范围；不要给高低值随机彩虹色 |
| 文件 | 矢量PDF为论文主文件、SVG供编辑、300dpi PNG供预览；地图底图若为栅格应按最终印刷尺寸保证分辨率 |
| 文件命名 | 名称说明内容和版本；不要用final_final。源数据、脚本、图注与输出放在相邻目录 |

## 地图出图前的八项检查

1. 城市参考点与25城原始名单一一对应，未混入10城试点或别名重复。
2. 原始坐标、底图和叠加图层的坐标参考系正确；比例尺单位和长度合理。
3. 底图来源、数据来源、许可署名完整；署名不能被裁切或被放大窗遮住。
4. 网格颜色的范围、单位、好坏方向一致；缺失值不冒充零值或最好值。
5. 主要道路、海岸、水域仍可读；底图地名不与城市标签或数据层打架。
6. 局部放大区在主图上有定位；跨城显示范围不同已明确说明。
7. 原始CSV和ZIP不覆盖，输出能从脚本和来源记录复现；保留文件哈希与下载日期。
8. 以论文实际尺寸查看，而不是只在全屏看；地图、图例和署名缩小后仍可辨认。

## 图注模板

全球图：**Geographical distribution of the 25 candidate cities.** Points indicate the reference locations used for matching city-level records. Basemap: [provider and dataset/version].

内部地图：**Modelled walking accessibility to learning facilities in [city].** Grid colour represents [time in minutes / dimensionless utility]; values are derived from the archived source model and retained all-age population. Blank or uncoloured areas [define explicitly]. Basemap: [provider]; accessibility data: [source snapshot].

同域对照：**Spatial comparison under [two settings].** Both panels use the same extent, projection, basemap and colour scale. [Explain what changes and what remains fixed.] Differences show modelled accessibility under the stated settings.

## 数据与知识边界

地图的好看不能替代证据。当前学习可达性来自研究作者发布的空间模型，源人口并非14–18岁，设施类别并非已识别高中。源网格覆盖范围也不等于统一行政边界。不能把没有学生调查、学位和质量数据的地图改写为“最适合高中生上学的区域”。

原获奖论文地图可能引用地图平台或第三方底图；本指南只保留原图出处用于研究参考，不把它当作本题可自由复用的底图。正式重绘应使用独立取得并正确署名的真实地理资料。地图图层与许可由实际绘图版本的来源记录负责。

## 索引生成方式与维护

`build_guide.py`只读既有获奖图页索引和选图来源，输出分类CSV/JSON、图文指南与PDF。自动分类是图题关键词检索，不是视觉模型评分；可能误判、漏判或把正文提及词误当图型。未分类页保留，不能从类别数量推断论文质量。

新增人工检查后，在脚本的`manual`页级标签中补充队号与PDF页码，并在来源卡记录选择理由。PDF页码可能与正文印刷页码不同，统一用PDF页码定位。检查脚本同时验证998行无重复丢失、参考图存在、源PDF存在及HTML相对链接有效。
'''
current_maps='''
## 本轮真实底图地图的对应规范

本轮地图工作目录为 `../cartography/`。全球定位点读取已有 `city_index.json`，是作者都市区域的参考定位点，不是独立核验的市政中心；与25城候选表逐项匹配。

底图使用 **OpenStreetMap公开矢量道路／河流 + Natural Earth海岸线、湖泊与世界底图**。曾尝试的CARTO请求虽然返回HTTP 200，但图像实际是“API KEY REQUIRED”占位内容，已被拒绝作为底图。下载成功不等于数据可用：每种底图必须视觉检查。

对应文件名称：`01_global_candidates`、`02_copenhagen_access`、`03_toronto_access`、`04_dubai_access`、`05_shanghai_access`、`06_city_access_comparison`。最终输出与来源以cartography目录的交付清单为准。

内部图的颜色表达 **c_f：到邻近20个Learning类POI的平均模型步行分钟**，使用共同时间分级；不是最近高中距离，不是实测通学。主图保留原网格范围，中心区放大窗显示道路和网格细节。OpenStreetMap底图道路仅作真实地理参照，本轮没有重新沿这些道路计算可达性。底图获取时间与可达性源模型时间可能不同，应保留各自来源记录。

[查看25城匹配坐标](../cartography/candidate_city_locations.csv) · [查看地图范围](../cartography/map_viewports.json)
'''
md+=ending+current_maps;(H/'STYLE_GUIDE.md').write_text(md)
# HTML is rendered from structured content rather than depending on a Markdown package.
css='body{max-width:1120px;margin:40px auto;padding:0 24px;color:#2b2b2b;background:#fff;font:16px/1.8 Georgia,"Songti SC",serif}h1{font-size:32px}h2{font-size:25px;margin-top:40px}h3{font-size:19px}a{color:#375a73}img{display:block;max-width:100%;max-height:600px;margin:20px auto}section{padding:22px 0;border-top:1px solid #ccc}.ref{font-size:14px;color:#696969}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ddd;padding:8px;text-align:left}nav{padding:15px 0}.counts{columns:2}code{font-size:13px}.sourcecards{display:grid;grid-template-columns:repeat(2,1fr);gap:24px}.sourcecards img{max-height:320px}@media(max-width:800px){.sourcecards{display:block}}'
parts=['<!doctype html><meta charset="utf-8"><title>获奖论文配图风格指南</title><style>'+css+'</style><h1>获奖论文图片风格蒸馏</h1>',f'<p>全库：{len(coverage)}篇论文、{len(rows)}个候选图页。全部做可复现分类检索；精选参考做视觉蒸馏。<b>19个精选参考页面已逐页查看。</b></p><nav><a href="../GUIDELINES.md">统一规范与字号标准</a> · <a href="STYLE_GUIDE.md">完整Markdown文档</a> · <a href="style_guide.pdf">PDF手册</a> · <a href="catalog.html">全库分类检索</a> · <a href="page_style_index.csv">分类CSV</a> · <a href="classification_summary.json">统计与方法</a></nav><p>地图跟13904队的浅灰真实底图、彩色数据层与局部放大；全球定位参考13719队；框架参考14995队；统计线图参考13719队。统一编码含义，不强行把所有图套成一种构图。</p>']
for title,ref,img,rr in sections:
 parts.append('<section><h2>'+title+'</h2><p class="ref">参考：'+ref+'</p><img loading="lazy" src="'+img+'"><ol>'+''.join('<li>'+html.escape(s)+'</li>' for s in rr)+'</ol></section>')
parts.append('<section><h2>本轮真实底图版本</h2><p>全球图使用Natural Earth；城市底图使用OpenStreetMap公开矢量道路／河流与Natural Earth海岸线、湖泊。颜色是Learning类邻近20处POI的平均模型步行分钟，不是最近高中或实测通学。地图位置来自已有city_index中的作者都市区域参考点。</p><p>CARTO尝试返回的是API KEY REQUIRED占位图，已拒绝使用；不将HTTP成功当作真实底图证据。底图道路仅作地理参照，没有重新计算可达性。</p><p><a href="../cartography/candidate_city_locations.csv">25城坐标匹配</a> · <a href="../cartography/map_viewports.json">地图范围记录</a></p></section>')
parts.append('<section><h2>全部精选来源卡</h2><p>点击原文链接回到对应PDF页。以下是视觉参考，不是当前队伍的数据或结果。</p><div class="sourcecards">')
for r in refs:
 parts.append(f'<article><h3>{r["title"]}</h3><p class="ref">{r["year"]} · Team {r["team"]} · PDF p.{r["page"]}</p><img loading="lazy" src="{r["image"]}"><p>{r["note"]}</p><a href="../../../../{r["source"]}#page={r["page"]}">原始论文</a></article>')
parts.append('</div></section><p>参数规范、地图验收清单、图注模板与数据边界见 <a href="STYLE_GUIDE.md">完整文档</a>。原图许可不等于本题重绘底图许可；正式地图应从独立来源取得并正确署名。</p>')
(H/'index.html').write_text(''.join(parts))
# Lightweight searchable page-level catalog; thumbnails are optional and lazy loaded only when toggled.
js="""function filter(){let q=document.querySelector('#q').value.toLowerCase(),c=document.querySelector('#cat').value;let n=0;document.querySelectorAll('tbody tr').forEach(r=>{let ok=(!c||r.dataset.cats.includes(c))&&r.textContent.toLowerCase().includes(q);r.hidden=!ok;if(ok)n++});document.querySelector('#n').textContent=n}function preview(a){let r=a.closest('tr'),im=r.querySelector('img');if(im){im.remove();return}im=document.createElement('img');im.src=a.dataset.src;im.style.maxHeight='500px';a.parentNode.appendChild(im)}"""
trs=[]
for r in classified:
 source='../../../../'+r['source_pdf']+'#page='+r['pdf_page']
 trs.append('<tr data-cats="'+html.escape(r['categories'])+'"><td>'+r['year']+' / '+r['award']+'<br>Team '+r['team']+' / PDF p.'+r['pdf_page']+'</td><td>'+r['categories']+'<br><small>'+r['review_status']+'</small></td><td>'+html.escape(r['captions'][:450] or '未识别图题；候选页可能含表格、装饰或扫描内容')+'<br><a href="'+source+'">原文</a> · <a href="#" onclick="preview(this);return false" data-src="'+r['preview_path']+'">展开图页</a></td></tr>')
opts=''.join('<option>'+c+'</option>' for c in sorted(counter))
(H/'catalog.html').write_text('<!doctype html><meta charset="utf-8"><title>全库图页分类索引</title><style>'+css+'input,select{padding:9px;margin:8px}small{font-size:11px}td{vertical-align:top}</style><h1>全库候选图页分类索引</h1><p>这是自动检索入口，不是998页人工评分。类别可重叠；仅精选参考页带人工核对标记。<a href="index.html">返回指南</a></p><input id="q" oninput="filter()" placeholder="队号／年份／图题关键词"><select id="cat" onchange="filter()"><option value="">全部类别</option>'+opts+'</select><span id="n">'+str(len(rows))+'</span> 页<table><thead><tr><th>出处</th><th>检索类别与核对状态</th><th>图题／预览</th></tr></thead><tbody>'+''.join(trs)+'</tbody></table><script>'+js+'</script>')
# A compact PDF handbook: fixed A4 pages with CJK fonts, original images and rules.
pdf=fitz.open()
def titlepage(title,body):
 p=pdf.new_page(width=595,height=842);p.insert_text((40,56),title,fontname='guide',fontfile=str(FONT),fontsize=19,color=(.17,.20,.23));n=p.insert_textbox(fitz.Rect(40,95,555,780),body,fontname='guide',fontfile=str(FONT),fontsize=11,lineheight=1.65);assert n>=0,(title,n);return p
body=f'''范围：{len(coverage)}篇馆藏论文、{len(rows)}个候选图页。\n\n所有候选页已生成可复现类别索引；精选参考做视觉核对与风格蒸馏。19个精选参考页面已逐页查看。分类统计是页级、多标签，不是独立图片数量。\n\n本题采用路线\n地图：13904队，浅灰真实底图、彩色路网、局部放大。\n全球定位：13719队；地理小多图：16742队。\n框架：14995队，四分区与功能色。\n统计：13719队，细线、Times字体、紧凑面板。\n\n本手册为研究参考，原图保留出处。只复用视觉规则与布局，不将获奖原图当成本队结果。正式底图需独立取得并正确署名。\n\n配套文件\nSTYLE_GUIDE.md：完整规范、图注模板和验收清单。\nindex.html：图文指南与可点击出处。\ncatalog.html：全部998候选页分类检索。\npage_style_index.csv / .json：分类结果。\n\n2026-11-07；本地研究附件，未修改论文正文。'''
titlepage('获奖论文配图风格指南',body)
for title,ref,img,rr in sections:
 p=pdf.new_page(width=595,height=842);p.insert_text((35,43),title,fontname='guide',fontfile=str(FONT),fontsize=15);p.insert_text((35,66),ref,fontname='guide',fontfile=str(FONT),fontsize=9,color=(.4,.4,.4));p.insert_image(fitz.Rect(35,85,560,345),filename=str((H/img).resolve()),keep_proportion=True)
 content='\n\n'.join(f'{i+1}. {s}' for i,s in enumerate(rr));remaining=p.insert_textbox(fitz.Rect(35,365,560,795),content,fontname='guide',fontfile=str(FONT),fontsize=10,lineheight=1.32)
 assert remaining>=0,(title,remaining)
 p.insert_text((35,823),f'原图仅作风格参考 | PDF手册第 {len(pdf)} 页',fontname='guide',fontfile=str(FONT),fontsize=9,color=(.5,.5,.5))
titlepage('地图与论文配图交付检查', '1. 全球25城与原始名单一一对应，不能混入试点城市。\n\n2. 底图与网格坐标系一致，比例尺、图例和单位正确。\n\n3. 底图来源、作者署名、获取日期和许可记录完整。\n\n4. 地图空白、零人口、无效值、低效用分别处理。\n\n5. 主图与放大窗有定位关系；不同城市范围不同须说明。\n\n6. 论文实际尺寸下，图例及说明至少9pt，主标签10–11pt；必要时拆图或使用横向附录。\n\n7. 单向色标与正负双色标按数据含义选择，不让配色暗示不存在的关系。\n\n8. 可行区间不是置信区间；模型可达性不是教育质量或实测学生通学。\n\n9. 地理地图使用真实地理资料；示意图明确标示意，不能与实测图混淆。\n\n10. 输出PDF、SVG和PNG，并保存脚本、数据来源和图注。\n\n完整分类、来源链接、参数建议与图注模板见同目录STYLE_GUIDE.md和index.html。')
titlepage('本轮真实底图地图的对应规范', '交付目录：visuals/cartography/。\n\n全球图：Natural Earth真实世界底图。25个位置来自已有city_index中的作者都市区域参考定位点，并非独立核验的市政中心。\n\n城市图：OpenStreetMap公开矢量道路、河流，配合Natural Earth海岸线与湖泊。底图道路只作地理参照，本轮没有重新沿这些道路计算可达性。\n\n数据颜色：c_f，到邻近20个Learning类POI的平均模型步行分钟。使用共同分级，不能解释为最近高中、学生实测通学或学校教学质量。\n\n版面：主图保留原网格范围，中心区用放大窗显示道路与网格细节。比例尺、缺失值、图例与署名必须保留。\n\n覆盖城市：全球25城；内部地图包括Copenhagen、Toronto、Dubai、Shanghai。最终文件名称与源数据以cartography目录交付清单为准。\n\n底图检查教训：曾尝试的CARTO请求返回HTTP 200，但实际图像是API KEY REQUIRED占位内容，已拒绝使用。不能仅凭下载成功就声称获得真实底图。\n\n实际图层获取时间可能不同于可达性模型源数据时间，分别保留来源、日期和版本。')
pdf.subset_fonts();pdf.save(H/'style_guide.pdf',garbage=4,deflate=True)
# Focused validation.
assert len(classified)==998 and len(coverage)==68
assert len({(r['source_pdf'],r['pdf_page']) for r in classified})==len(classified)
for r in refs:assert (H/r['image']).exists() and (ROOT/r['source']).exists()
for name in ['index.html','catalog.html']:
 for link in re.findall(r'(?:src|href|data-src)="([^"]+)"',(H/name).read_text()):
  if link=='#' or '://' in link:continue
  assert (H/link.split('#')[0]).exists(),(name,link)
print(json.dumps(summary,ensure_ascii=False));print('PDF pages:',len(pdf));print('All local references and 998 unique index rows verified.')
