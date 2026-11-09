# V177：两份新官方来源的口径记录

新增保存两份HTTP200原HTML：市府发布的Zurich年末2024人口448664，以及CSO《Measuring Ireland’s Progress 2026》Background Notes。原始URL、实际访问UTC、返回状态、长度与SHA见[retrievals.json](retrievals.json)。未重新抓取或改写V144/V145旧犯罪统计原件。

- [Zurich人口原发布](https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2025/02/fast-450000-einwohnerinnen-in-der-stadt-zuerich.html)及[原HTML](zurich_population2024_original.html)：明确人口是年末2024、Stadt Zürich，不是2025新观测。用于对照两个特定人口分母，不认证其为用户凶杀率或警方计数的适配分母；用户2025人口440935保持。
- [CSO原方法页](https://www.cso.ie/en/releasesandpublications/ep/p-mip/measuringirelandsprogress2026/backgroundnotes/)及[原HTML](ireland_mip2026_notes_original.html)：2026为出版年，各指标使用自身最新可用年份。第4.3节说明Ireland的ISCED3在该表含ISCED2；不能将其直接写为Dublin市纯高中PTR。混合学段的教师总量原则上仍可能是合法superset，当前页面未提供匹配城市总量上界及学生下界，未建立该包络。

Zurich与Dublin师资路线分别限定两次定向检索。前者只命中已查路径／旧手册索引摘要，未将摘要当新原件；后者得到上述新方法说明但没有匹配数值，均停止并记录0准入。生成与核验见研究scripts/task4_v177_source_reconciliation.py及audit_task4_v177_source_reconciliation.py，结果在[reconciliation](../../results/task4_v177_source_reconciliation/README.md)。用户CSV、科学V154及论文V176保持。
