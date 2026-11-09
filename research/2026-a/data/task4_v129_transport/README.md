# V129：Berlin内城100个公共地铁站候选

**原生BVG站点标识支持100个内城地铁复合体的条件库存下界。** 九条U-Bahn官方线路页分别给出站名、站点slug、分站票区和换乘线路。筛选每站明确的A区字段后，131次线路出现合并为100个独立slug；归一化站名与slug一一对应，每个跨线路重复都由原记录的换乘声明核对。线路出现数按U1–U9为13、23、16、5、13、14、22、15、10。

BVG[票区定义](https://www.bvg.de/de/abos-und-tickets/tarifzonen-und-tarifbestimmungen)把A区明定为Berlin内城至S-Bahn环线。本候选只取该已明确位于城市内部的子集，不把运营网络或广域票区总数套作全市，也不声称做过行政边界polygon overlay。B/C、站台、出口及其他交通模式均未新增计数。

原件为`berlin_u1.html`至`berlin_u9.html`和`berlin_zone_definition.html`；[manifest.json](manifest.json)保存来源URL、SHA-256、原生字段路径与逐线路检查。[berlin_stations.json](berlin_stations.json)逐站列出标识、具名复合体、线路及原文定位；其中站点查找URL由slug推导，未逐站访问。原始HTTP响应头未随最初采集保存，原件中的canonical URL与声明来源逐一核对；不补造当时的响应头或精确秒级访问时刻。

使用原表固定人口3,700,577（2025），100站对应每10万人至少2.70228129个，交通效用候选为`[0.051274465290648025,1]`。来源是2026-11-09访问时发布的静态线路站表，不能改标2025观测。该表不等同逐站实时运营、持续开放、学生资格或个人可达性核验。其他城区和模式未计，上界保留1；必要时可撤回至未知。

**此包仍是候选，主注册表和正式排名继续为V127。** 父级[独立审查](../../results/task4_v129_candidate_review/audit.json)使用另一HTML解析器复算原生标识、站名、票区、换乘和源哈希，并独立核对只读预评估。若后续正式准入，fixed平均区间宽度预计16.10728557→16.09206967（约收窄0.0945%），Berlin仍第7，Zurich保守推荐及16个可能冠军不变。这些是候选条件计算，不是本轮已经改变主模型的效果。下一阶段须完成正式准入／撤回、主计算及全部扩展和论文数值迁移，才能启用新基准。

```sh
.venv-v120/bin/python research/2026-a/data/task4_v129_transport/extract.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v129_berlin_candidate.py
```

## Amsterdam路线：未准入

[amsterdam_nonadmission.json](amsterdam_nonadmission.json)保存市地图页面、配置和图例的来源哈希，以及父级实际复查GVB页面的HTTP403响应。地图配置本身未建立可复核的当前市内站点复合体清单，不能从页面标题或线路总数补格。

市府《Atlas van Stationskwartieren》标为2024-12-12定稿，历史区域规划图同样没有在本轮形成当前市界和实体去重证据。99,647,617字节原PDF置于仓库外`/data/datasets/HiMCM/source_archives/task4_v129_transport/amsterdam_atlas_2024.pdf`，收据列原件SHA和重新定位的[官方PDF URL](https://openresearch.amsterdam/image/2025/2/12/atlas_van_stationskwartieren_def-42732341.pdf)。原始下载响应头未保存；仓库内是第1、3、16页派生文字，不声称视觉核验或完整PDF已入Git。Amsterdam无观测准入。
