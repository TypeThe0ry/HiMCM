# 候选城市与学习设施可达性地图

[已核验大字号图集](maps_with_captions.pdf)：插入示例已改为保留纸张尺寸；原始单图直接缩成正文宽可能低于 9 pt。竞赛正文需按允许纸张与页数重排，A3 图集用于可读审阅。

共 6 张地图：25 座候选城市全球分布、哥本哈根／多伦多／迪拜／上海内部可达性，以及四城比较。各图提供 PDF、SVG 和 300 dpi PNG。

## 制图语言
沿用获奖论文地图中的低饱和底色、细道路、分级覆盖面、局部放大与紧凑图例。全球图采用 Robinson 投影，欧洲另设放大图；城市图采用真实道路、水系和海岸线，并配独立比例尺。详细参考来源和参数见相邻 style_guide/style_guide.pdf。

## 指标与底图
城市颜色表示归档模型的最近 20 个 Learning POI 平均步行时间，使用有居民人口的网格；摘要按人口加权。这是学习设施可达性代理指标。评价学校质量、入学机会或学生实际通勤需要另行数据。
城市覆盖范围遵循原数据的城市区域，定位点亦来自作者城市索引。
道路与水系来自 2026-11-07 OpenStreetMap 查询；陆地与湖泊来自 Natural Earth。新底图用于地理定位，时间值保留原归档模型结果。城市图和局部图采用各自比例尺。

## 可复核文件
candidate_city_locations.csv：25 城坐标。
global_map_audit.json / city_map_audit.json：城市数量、数据覆盖和人口加权结果。
vector_data/manifest.json：OSM 请求、时间戳和哈希。
prepare_maps.py / draw_global.py / draw_city_maps.py：数据整理与绘图代码。
city_map_captions.json / figure_includes.tex：英文图注与 LaTeX 插图片段。

## 风格文档范围
68 篇论文、998 个候选页面已索引；19 个精选参考页面逐图查看。页面数不等于独立图片数；目录保留待分类页面，便于继续补充。

## 来源
- OpenStreetMap contributors: https://www.openstreetmap.org/copyright
- Natural Earth: https://www.naturalearthdata.com/
- Bruno et al., 15-minute city study: https://www.nature.com/articles/s44284-024-00119-4
- 数据项目：https://whatif.sonycsl.it/15mincity/

本次交付为本地配图和支持文档，未修改在线 Overleaf 正文。

## 印刷与复现

[实际字号印刷版](print_ready_maps.pdf)：全球图及单城图用 A4 横版，四城比较及卫星面板用 A3 竖版，全部文字经 PDF 检查至少 9 pt，详见 print_audit.json。避免直接缩成双栏；窄版正文可拆出局部面板。运行 prepare_print.py 可重新检查与排版。

[卫星与多源地理背景](satellite/README.md)提供同域卫星 RGB 参考及产品元数据。

## 带图注的可编译图集

在本目录执行 `tectonic maps_with_captions.tex` 可生成 8 页图集：7 页地图和 1 页正常字号图注。引用片段需要 `pdfpages`，每一张混合尺寸页面单独使用 `fitpaper=true`，以保持已核验字号。整页图集适合审阅；正式比赛版面按题面允许尺寸另行排版。

[本轮审阅记录](../FIGURE_REVIEW.md) · [原图字号审计](../figure_font_audit.json) · [最终渲染字号审计](../rendered_figure_audit.json)
