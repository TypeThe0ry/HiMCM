# V143：推荐对保留输入信息的依赖

现行V136的Zurich保守推荐以接受用户点值为条件。本轮将特定点值的utility信息撤回为[0,1]，检验年份／来源标记政策变化的后果；原CSV、112个输入数值、所有补充证据、权重和现行注册表均不修改。每次保持原48个非点界不动。日期／标记是诊断分类，不是误差大小、错误概率或新的自动准入规则。

| 撤回的点值组 | 格数 | 基准推荐 | 等权推荐 | 基准平均区间宽度 |
| --- | ---: | --- | --- | ---: |
| 无（现行） | 0 | Zurich | Zurich | 16.08933 |
| 年份早于2020 | 13 | Singapore | Zurich | 21.16464 |
| 年份晚于2025（实际均2026） | 64 | Zurich | Zurich | 48.43148 |
| 非ok标记 | 28 | Berlin | Paris | 29.13846 |
| 上述并集（去重） | 95 | Singapore | Singapore | 68.80419 |

每个情景仍16可能／0必要冠军。区间扩大表示撤回信息，不表示城市实际恶化；替代保守选择也不是确定冠军。非ok包括MODELLED16、STALE8、SUSPECT3、NATIONAL1，各有不同含义，不一概判作错误。112个保留点值中64标注2026、2标注2025、46更早，标签来自原表，未由本轮重新认证。该试验只按提交点值分类，保留所有补充与非点界，不能称为仅2025数据模型或真实跨年趋势。

复现（仓库根目录）：

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v143_vintage.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v143_vintage.py
```

submitted_points.csv逐格保存112个原标签及utility；withdrawn_cells.csv保存200个“情景×撤回格”记录（组间有重叠），ranks.csv保存5组×2权重×16城。独立verifier用Python csv直接读原件，按冻结V136 after_conditional边界重构掩码，以math.fsum标量TOPSIS重算320个得分界、160个城市情景、最大遗憾及推荐，并检查112标签和200撤回记录。原始verification.json保留，重放另写recheck_verification.json。source_sha256绑定139份原科学保护集合及额外依赖。

论文只在Overleaf自有稿加入5.5来源信息依赖、对照表，并同步摘要／结论／新闻的重要条件。没有额外评价模型，也没有改变主V136／扩展V137或补数准入。本轮Dublin／Zurich有界教师检索尚未取得新匹配城市高中教学FTE原表；不重复把地区统计或分配岗位填入城市比率。
