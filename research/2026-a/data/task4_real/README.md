# 25城真实代理数据：来源与适用边界

访问日期：2026-11-07（Asia/Singapore）。来源：[Numbeo Quality of Life Index by City 2025](https://www.numbeo.com/quality-of-life/rankings.jsp?title=2025)。网页HTTP下载成功，原始HTML归档；SHA256由分析脚本写入results/task4_real/summary.json。

此处使用发布者的2025版历史表，不称为2025全年单年观测或2026实时数据。源数据是城市条目，尚未统一到GHSL边界；问卷样本不代表当地全体居民或14—18岁学生。2026访问的方法说明用于理解指标，不能据此证明历史版本算法从未变化。

按团队25城候选表逐个精确匹配城市与国家，无缺失填补、无挑选冠军后的样本调整。特别区分London, United Kingdom与London, Canada，以及Santiago, Chile与墨西哥同名条目。保留source_city、来源URL、版次与访问日期。未采用发布者的综合生活质量分数，避免拿已有榜单当标准答案。

| 输入字段 | 模型方向 | 固定参照转换 | 含义及限制 |
| --- | --- | --- | --- |
| Safety Index | 正向 | x/100 | 用户安全感指数；不是警方凶杀率 |
| Pollution Index | 负向 | 1-x/100 | 污染感知指数；不是PM2.5浓度 |
| Property Price to Income Ratio | 负向 | clip(1-x/40,0,1) | 发布者住房负担代理；不是学生日常开支 |
| Traffic Commute Time Index | 负向 | clip(1-x/90,0,1) | 通勤时间代理（分钟）；不是学生通学、不是固定10km开车时间 |

100是指数尺度；房价收入比40与通勤90分钟是本轮明确的分析参照假设，不是政策标准或数据估计。另测试30/60与50/120。原始值完整保留；Lagos房价收入比46.8在主转换中截断为0，报告该饱和。尺度在计算排名前写入代码且在所有城市间固定，未因结果调整。

与五指标原稿不同：本轮采用四项同源可用代理，尚无宽带、直接教育或课外成长测量。医疗没有因数据方便而悄悄补入。因此这是一轮真实城市数据上的模型机制比较，不能直接作为完整高中生宜居榜发布。

方法来源：
- [安全指数](https://www.numbeo.com/crime/indices_explained.jsp)：用户调查；本轮不使用其推断真实犯罪率。
- [污染指数](https://www.numbeo.com/pollution/indices_explained.jsp)：主要为感知测量，不能替代空气监测。
- [交通指数](https://www.numbeo.com/traffic/indices_explained.jsp)：用户贡献数据，时间项为单程通勤分钟。
- [房价收入比](https://www.numbeo.com/property-investment/indicators_explained.jsp)：其假设包括90平方米、中心/外围均价和1.5倍平均净工资的家庭收入代理。原五指标稿关于仅市中心和直接中位家庭收入的描述不能套用于本数据。

复现：在HiMCM仓库根目录执行 `OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/task4_real_analysis.py`。脚本离线读取归档HTML，重建CSV、图表和结果。Python依赖版本见runtime_versions.json。
