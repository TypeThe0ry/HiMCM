# 新来源对照与 Zurich 泳池条件预览

本轮取得 Oslo 历史凶杀数量／比率的官方对照，并找到四处未计入的 Zurich 室外人工泳池候选。主分析保持 V205；本轮准入为 0，实际评分区间收窄为 0。

## Oslo：分子匹配，比率与原始来源仍待核

[来源包](../../research/2026-a/data/current_oslo_homicide_lineage/README.md)保存 Eurostat 两份原始 API 响应、方法指南与元数据。当前历史序列中，`NO001C`、2008 年的凶杀犯罪数量和被害人数量各为 12，两个独立统计概念的公布比率均为每十万人 2.14。原 CSV 为 1.71、2008、`STALE`、分子 12，保持原样。

分子数值一致不足以确定原始提取来源。当前标签为 greater city，不能据此确定 2008 年的精确边界或原比率分母；也不将另外给出的 2025 人口与 2008 分子相除后替换原值。独立复核确认四份原件的哈希、JSON-stat 维度解码及方法指南范围。[离线核验脚本](../../research/2026-a/scripts/audit_current_oslo_homicide_lineage.py)默认只输出报告；新增结果登记为来源补充，未改写冻结的 V205 点值台账。

## Zurich：四处季节性场馆候选

[泳池来源包](../../research/2026-a/data/current_zurich_outdoor_pool_route/README.md)保存市府目录、四候选及两个排除／暂缓场所详情、季节时间表和抓取记录。Allenmoos、Heuried、Letzigraben、Seebach 各有明确人工游泳池描述和不同于既有十二处的地址；同一场所的多个池不重复计数。Auhof 的维修关闭、计划 2029 年重开说明优先于仍留在网页中的旧季节时间表，因此暂缓；Zwischen den Hölzern 的联系地址为 Oberengstringen，按本轮市内邮址筛选排除。

四候选在捕获时均显示关闭；其中只有 Allenmoos 和 Letzigraben 的状态明确写出季末。2026 时间表可支持季节性名录预览，不能说明捕获日同时开放、全年开放或构成 2025 库存。邮址筛选、正式行政边界、实际运营和学生个人准入是不同的证据层级。所用 440,935／2025 人口按用户原输入保留。

## 隔离计算：候选不会自动进入主榜

[预览脚本](../../research/2026-a/scripts/task4_current_zurich_outdoor_preview.py)将 Zurich 场馆数从 12 条件性提高到 16，仅改变该格下界，另外 159 个下界和全部 160 个上界保持。所有权重、效用锚点及原 CSV 保持。

| 权重 | V205 均宽 | 候选均宽 | 若准入的均宽减少 | 保守选择 |
| --- | ---: | ---: | ---: | --- |
| 固定 | 15.63063190 | 15.61904727 | 0.01158463 | Oslo |
| 等权 | 18.01490896 | 17.99183124 | 0.02307772 | Zurich |

两种权重下仍有 16 个可能冠军、0 个必要冠军。上述减少是隔离预览的条件差值，当前主分析没有获得这部分实际改善。预览还按既定种子、三种集中度和每组 10,000 次共同权重抽样运行前后对照；这些模拟频率不代表现实获胜概率。结果见[预览核验记录](../../research/2026-a/results/current_zurich_outdoor_preview/verification.json)。

[独立复核](../../research/2026-a/results/current_zurich_outdoor_preview/peer_review.json)以不同 HTML 解析器确认来源范围，并重算 64 条城市标量结果和全部 12 组 MC 的 192 条城市汇总；来源、输出哈希及另外 159 个下界／全部上界保持检查通过。

复现时使用新输出目录，避免覆盖保存的结果：

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python -s \
  research/2026-a/scripts/task4_current_zurich_outdoor_preview.py \
  --output /data/scratch/himcm-zurich-outdoor-preview-replay
```

下一步先确定四处场馆的地理和季节供给口径能否与现有计数规则一致，再完成完整受控案例、扩展与独立核验，最后决定科学登记和必要自有稿件的迁移。当前预览不替代这一步，也不修改队友正文。
