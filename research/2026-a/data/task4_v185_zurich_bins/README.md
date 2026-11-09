# V185：Swiss工作旅时方法和分布范围核查

本轮取得四份新官方原响应，未取得能缩窄原39.9分钟条件区间的匹配时长分布，0准入、0基线收窄。原CSV、V181模型、V184自有稿及注册表保持。

BFS旧City Statistics交互表覆盖2011—2020年，说明参考年x对应结构调查x−1年末，调查总体为常住私人住户15岁以上人员；工作通勤者须有住宅以外固定工作地点，缺失旅程信息者不纳入。2021年发布起采用流入及内部工作通勤者，排除流出者；该旧表均值置信区间以分钟列示。这些历史方法说明不能自动证明2024年Eurostat39.9记录的精确调查实现。

新《瑞士城市统计2026》官方SDMX数据给政治市镇261 Zürich在31.12.2023的工作旅时均值34.22050361分钟，发布于28.04.2026，市镇边界状态06.04.2025。它并不匹配原39.9／2024 greater-city记录，未证明同人群／期窗。其CI行数值1.949499193，当前结构字典明确单位PT为Percent、操作CI为Confidence interval(+/-)；本轮未核其置信水平或相对／绝对换算方式，不把旧表“分钟”规则套用，也不把抽样CI当确定性误差包络。

原HTML、SDMX数据及结构文件保持完整字节；来源、HTTP状态、访问UTC、长度与SHA见retrievals.json。两次派生旧API入口400／404失败，响应正文未保存，未冒称取得JSON元数据。四次搜索限定两条路线；查不到同口径分箱后停止。

运行`.venv-v120/bin/python research/2026-a/data/task4_v185_zurich_bins/extract.py`可离线复核城市字典、四行市镇观测、单位及原件身份，输出extraction.json。完整范围和拒收理由见findings.json。

来源：[旧BFS City Statistics表](https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-2105000000_206/px-x-2105000000_206/px-x-2105000000_206.px)；[BFS／瑞士城市协会2026资产36503367](https://statistik.admin.ch/de/asset/36503367)。新资产标明OPEN-BY，来源署名为Bundesamt für Statistik／Schweizerischer Städteverband；原件仅作研究记录。
