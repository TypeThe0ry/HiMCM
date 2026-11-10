# V199：按V197重排补数优先级

全部48个不确定格进入双权重筛查，共96行；11全未知／37部分区间保持。Zurich泳池已从7处细化至12处，其剩余区间仍参与比较，不因获得更多下界而被视为完整观测。

固定权重下，完整精确识别一个指标效用时，Dublin师资的条件保证遗憾改善仍为1.066798分；Dublin旅时为0.424075，Zurich师资与旅时各为0.364245。保证值以完整精确效用识别为条件，不适用于一般目录、旅时均值或任意部分统计。等权下所有单格保证改善为0，但Zurich师资的最佳可能改善为8.582435分。端点和这些上限不表示可取得的真实观测或数据可得概率。

相对V194，96个键及信息分类保持，只有Zurich泳池的两条权重行下界改变。7行保证改善、35行最佳可能改善及3行端点冠军排除上限改变。Zurich师资在等权最有利端点的排除上限由1城变3城；原权重上限仍5城。这是模型信息条件的变化，不是已经排除了城市。当前仍Zurich保守、16可能／0必要。

`all_uncertain_priority.csv`、`endpoints.csv`和`lower_only_refinements.csv`分别保存96个精确包络、192个端点和480个单侧细化情景。单侧情景保留原上界，不能借用精确识别的保证。与V194逐键比较见`V194_comparison.csv`；独立标量审计见`verification.json`。

另有`pool_count_thresholds.json`与探针表：在其他159格、全部上界和权重不变的条件下，Singapore泳池下界数量达到27，才会在原权重下使Singapore严格优于其他城市的保守遗憾选择；等权对应179。连续并列边界分别26.377779和178.147027。它们是**条件采集阈值，不是观测数量或政策预测**；来源团队独立提取计数，不以达到阈值为筛选目标。原人口6036900／2024保持。独审见`pool_threshold_verification.json`。

本轮诊断不改变任何科学输入，0准入、0本轮实际评分区间收窄。当前科学V197／论文V198保持，用户CSV、原值、权重、区间规则及队友内容保持。

复现（研究仓库根）：

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v199_priority.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v199_priority.py
.venv-v120/bin/python research/2026-a/scripts/task4_v199_pool_threshold.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v199_pool_threshold.py
```
