# 论文配图与证据表达规范

地图以真实地理为骨架，以研究指标为主体；图注直接说明读者应看到的结果及其计算口径。本页是本项目全部视觉规范的统一入口，也是当前出图验收标准。

## 全部规范与参考目录

| 内容 | 入口 | 用途 |
|---|---|---|
| 配图风格总指南 | [STYLE_GUIDE.md](style_guide/STYLE_GUIDE.md) · [PDF](style_guide/style_guide.pdf) · [图文版](style_guide/index.html) | 地图、模型图、比较图等的版式与参数 |
| 全库风格检索 | [catalog.html](style_guide/catalog.html) · [分类方法](style_guide/classification_summary.json) | 68 篇论文、998 个候选页面的索引 |
| 精选地图原例 | [地图摘录](maps/index.html) · [出处](maps/map_sources.json) | 比较全球定位、覆盖面与局部放大设计 |
| 候选城市与内部地图 | [地图集](cartography/index.html) · [数据与方法](cartography/README.md) | 25 城定位、四城内部地图、共同色标 |
| 卫星影像与多源数据 | [数据说明](cartography/satellite/README.md) | 影像产品、获取记录和专题叠加 |
| 底图获取与来源 | [矢量底图说明](cartography/vector_data/README.md) · [来源清单](cartography/vector_data/manifest.json) | 道路、水系、时间戳、文件哈希 |
| 第二轮分析图设计 | [设计说明](round2/README.md) · [图注](round2/CAPTIONS.md) | 流程、空间分布、机制、排名和不确定性 |
| 第一轮方案与选图 | [初版说明](README.md) · [精选原图](award_atlas/selected.html) | 设计演进与参考出处 |
| 学术写作技能 | [中文技能](guidelines/anti-defensive-writing/zh/SKILL.md) · [English skill](guidelines/anti-defensive-writing/en/SKILL.md) · [anti-defensive-writing 上游](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill) | 结果优先、主张与证据一致、紧凑叙述 |

研究指标定义另见 [模型设计](../design/task4_evaluation_model.md)、[指标规范](../design/task4_v5_indicator_spec.md) 与 [研究设计](../design/research_design.md)。图形应准确表达其对应版本的指标与结果。

## 字号与最终版面

以下是本队制作标准，按**插入论文后的实际尺寸**验收：

- 图例、刻度、说明和来源署名至少 **9 pt**；主标签 **10–11 pt**；面板标题 **11–12 pt**。
- 大图缩小时同时缩小文字。最终字号 = 输出字号 × 插入宽度 ÷ 输出宽度。例如宽 12 英寸图缩到 6 英寸，原 18 pt 才得到最终 9 pt。
- 信息拥挤时拆面板、增大占页面积或把方法说明放进正文图注；保持图内字号。
- 当前城市图画布宽 10.5 英寸、最小文字 11 pt，维持最终 9 pt 需要插入宽度至少 8.6 英寸。常规 A4 正文宽度不足时应拆成主图／局部图并重新排版，或提高源字号；不要直接缩成双栏小图。
- 每图一个主要结论，图内保留单位、图例、比例尺、位置名称与必要来源。长定义写进正常字号图注或方法段。
- 输出矢量 PDF 与 SVG；栅格部分按最终尺寸保证至少 300 dpi。实际尺寸预览用于检查文字、线条和图例，放大预览用于检查几何与影像。

## 多源地图的论证结构

| 图层 | 回答的问题 | 必须保留的证据 |
|---|---|---|
| 卫星影像 | 建成区、水体、植被在何处？ | 提供方、产品、影像日期或合成窗口、分辨率、覆盖区、许可 |
| 道路与水系 | 城市如何连通，地理阻隔在哪里？ | OSM 等来源、提取日期、道路筛选规则、坐标系 |
| 人口与设施 | 服务需求和供给如何分布？ | 年份、人口口径、设施类别、空间分辨率 |
| 可达性结果 | 指标在哪里较高或较低？ | 出行方式、目的地定义、计算模型、分级、人口权重 |
| 核验结果 | 可视模式是否支持文字主张？ | 可复算统计、来源一致性、必要的敏感性检查 |

卫星影像负责提供地表背景；交通时间和教育质量分别由对应模型与数据支持。跨城比较使用相同指标定义、分级和人口统计口径。不同尺度的地图各自标比例尺。各层记录自己的采集年份，读者能区分背景影像与模型输入的时点。

卫星纹理较密时，采用同域双面板：左侧影像和少量定位信息，右侧简洁底图和专题数据。确需叠加时压低影像饱和度，保持专题色块与道路层清晰。色彩或透明度变换写入方法记录，原影像保持可追溯。

## 结果优先的写法

依据已安装的 anti-defensive-writing 技能，每段先写有证据支持的结果，再给定义和解释。删除过程流水账、重复的自我辩解和与结论无关的比较。材料中的反例、关键不确定性和影响结论的条件应准确报告，并与它们支持的主张放在一起。

图注顺序：**对象与结果 → 指标及单位 → 比较口径 → 数据来源**。

示例：**Learning-facility accessibility in Shanghai.** Grid colours show modelled mean walking time to the nearest 20 learning POIs. Within the retained populated grids, 58.2% of residents have values at or below 30 minutes. Insets show neighbourhood detail; each panel has its own scale. Sources: archived accessibility model, OpenStreetMap and Natural Earth.

该数值来自 [city_map_audit.json](cartography/city_map_audit.json)，适用于其归档数据版本。图注使用源指标的“居民”“学习设施”“模型步行时间”等名称。

## 交付验收

1. 城市名单、原始值、单位与数据版本逐项对应；缺失值有单独表达。
2. 坐标参考系、影像覆盖、放大窗位置和比例尺通过核验。
3. 同类地图共享分级与符号；色彩含义与图例一致。
4. 所有可见文字满足最终字号要求，标签无重叠、无裁切。
5. 每项文字结论对应可复算数值或具体观察；空间叠加解释与数据能力一致。
6. 原始资料、来源记录、绘图脚本和输出文件可关联；图例与署名完整。OSM 原始查询响应以无损 gzip 副本进入 GitHub，解压恢复 JSON 后用于复现。

历史图册保留其原版内容；新制图与改版按本页标准执行。风格分类包含 998 个候选页面，其中 19 个精选参考页已逐页查看；候选页数与独立图片数分别记录。
