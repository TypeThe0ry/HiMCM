# V101：在V96输入上重算连续偏好的补数条件

本轮将仍使用V91输入的补数分析更新到当前V96，重新核对25城。最少有利精确补数项数、全部可行组合身份和判定均保持：Singapore为0、Tokyo为1、Lagos为3，其余城市为2。这里的目标是使该城在整个偏好范围获得最小最大遗憾推荐，不是证明实际表现第一。

Phoenix仍有6个连续认证的二项组合，其中包括教育＋通学。它们假设新观测恰好位于现有区间上端；取得这两项数据本身并不保证推荐Phoenix。全体真实区间、排名及25城可能冠军均未改变。

## Warsaw真实修订的影响

V91→V96只改变Warsaw教育格，教学资源覆盖扩展使其下界提高、上界略降。在共同α=.05、.10、.20上独立重算全部组合，只有Warsaw的22个组合裕量变化：

- 不选择教育的16个组合，在已检查共同权重点上的推荐裕量增加约1.1202—1.9693分；新教育下界提高该城保守分数。
- 选择教育的6个组合，裕量减少约0.0268—0.0372分；最乐观精确揭示使用新上界，不能继续采用旧的略高上界。

所有判定均未跨越临界线。真实信息同时约束过度悲观与过度乐观，不能仅看下界上升就断言所有补数情景都更有利。[独立检查](independent_check.json)保存22组逐项变化。这些共同点差值不冒充全连续区间的极值。

## 公式与认证

对目标城市i和待测指标集B，假设揭示值为现有上端：

$$l'_{ij}=h_{ij}\quad(j\in B),\qquad l'_{ij}=l_{ij}\quad(j\notin B),\qquad h'_i=h_i.$$

定义推荐裕量

$$g_i(B,\alpha)=\min_{k\ne i}R_k(B,\alpha)-R_i(B,\alpha).$$

上端揭示对每个α都最有利：相对于其他允许的精确揭示，目标遗憾不增，竞争者遗憾不减。只有覆盖α∈[0.05,0.20]的全部证书叶均给出正裕量，才认证该组合。若有负裕量见证则排除；未决仍保留。逐项枚举所有更小组合，证明外包模型内的最少项数。闭区间端点不保证真实指标能共同达到，计数也不是数据文件数或采集成本。

550个组合包括335个负裕量反例和215个认证组合；420个连续证书叶、未决0。独立longdouble审计不导入模型评分函数，验证全部组合与连续域覆盖，另枚举475个固定偏好组合。最大差异低于4×10⁻¹⁴。证书分区数量变化只反映数值证明分区，不代表经验精度提升。

通用脚本新增两项保护：拒绝覆盖不同模型／输入的历史结果；拒绝将旧结果标成错误模型版本。两项回归测试分别确认拒绝发生在搜索和写入之前。未增加评分指标或改变主公式。

```sh
python3 research/2026-a/scripts/task4_registered_continuous_acquisition.py --output research/2026-a/results/task4_v101_current_acquisition --prior-results research/2026-a/results/task4_v91_current_acquisition --prior-model V91
python3 research/2026-a/results/task4_v101_current_acquisition/audit.py
python3 research/2026-a/scripts/test_task4_registered_continuous_acquisition.py
```

[最少项数](minimum_bundles.csv) · [全部组合](bundle_evaluations.csv) · [连续证书](bundle_certificates.csv) · [对照](comparison_prior.csv) · [摘要](summary.json)。
