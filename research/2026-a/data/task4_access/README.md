# 学习设施空间可达性：原始数据、映射与边界

访问日期：2026-11-07（Asia/Singapore）。本次已检查GitHub origin/main（5269e73）及分支/Release；其中没有用户所述的教育/学生可达性实测矩阵。附件中的CSV和两份MD与已存原件逐字节相同；Numbers文件为10城试点名单。故本轮另从研究发布者的公开平台取数，没有声称这些ZIP来自团队GitHub。

## 数据来源

- 研究：Bruno等，A universal framework for inclusive 15-minute cities（2024）。[论文](https://www.nature.com/articles/s44284-024-00119-4)，[作者预印本及方法](https://arxiv.org/html/2408.03794v1)。
- 原始平台：https://whatif.sonycsl.it/15mincity/。
- 城市索引：load_city_ranking.php。
- 当前城市网格：data/{city_id}/hexes.zip，内含hexes.geojson。**不使用data/{city_id}/{scenario}/目录下的理想化模拟城市。**
- URL、文件名、SHA256、大小、网格数量和访问日期逐文件记录在manifest.json。
- 底层来源归属：OpenStreetMap贡献者、WorldPop及上述研究作者。保留原始来源，不把第三方数据宣称为团队原创。

29座城市包括原25城及试点新增Zurich、Vienna、Wuhan、Detroit。逐城市匹配索引名称和地理坐标；New York使用6245而非6246，Melbourne使用5662而非3046；Detroit对应Detroit (greater)，不能当作底特律市域。Delhi最后通过大小写及方括号别名Delhi [New Delhi]、经纬度匹配到10043。

## 使用字段

仅使用population、c_f（Learning步行）、c_b（Learning骑行）。页面中旧注释、当前地图标题和柱状图的若干类别标签存在不一致，但c在各版本都对应Learning；因此本轮不使用有歧义的运动/文化字段。platform_page.html和bar_chart.js保存了审计依据。

作者方法为到邻近20个同类POI的模型化平均时间，不能称到最近一所高中所需时间；不提供高中学段识别、学位容量、教学质量、入学资格、收费或放学后开放时间。总体人口不是14—18岁学生人口。

基于公开网格计算的是数据中保留区域的居民可达性代理。作者方法可能略去没有附近POI的网格，因此保留人口不自动代表全部市域人口。除Vienna外本轮网格人口和平台索引人口基本一致，但这不是覆盖完备性的独立验证；Vienna约95.74%，在试点表中明确保留两种人口数。

## 时间与空间口径

论文引用OSM 2023及WorldPop 2020等来源，但下载的平台文件没有逐城版本时间戳。只能称2026-11-07获取的作者发布空间数据快照，不能擅自认定全部输入恰好为2023或2026。与Numbeo 2025版叠加时存在时间和城市边界不完全一致的局限。

地图索引的avg_foot有显示截断，不能直接拿30当真实均值。计算使用ZIP内未截断的c_f/c_b。

## 无效值处理

人口非有限或为负直接拒绝；零人口网格不参与人口权重。正人口网格的时间非有限或≤0时，不认为学习设施完美可达，而把该网格效用保留为[0,1]，传播成城市可达性上下界。Delhi、Jakarta、Mexico City存在很小的此类人口份额，见派生测量表。没有均值填补，也没有把整个城市排除。

## 复现

仓库根执行：

```
python3 research/2026-a/scripts/task4_fetch_access.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/task4_access_revision.py
```

下载脚本对已归档城市ZIP直接复用；研究主结果以manifest哈希对应的文件为准。分析离线完成。已有城市索引和页面也是访问时快照；重新下载新快照需另建版本并比较，而不应默默覆盖证据。

这是学习设施空间可达性数据，**没有完成对高中教育质量、入学资格及实际青少年通学行为的采集**。所有结论必须保留此边界。
