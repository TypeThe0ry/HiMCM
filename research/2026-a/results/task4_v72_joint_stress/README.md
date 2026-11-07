# V72：用当前高中口径重新检验推荐稳定性

V72墨西哥城年龄口径修订后，真实输入下仍推荐Singapore，Tokyo第2、Phoenix第24，25城仍可能第一。相较V70，249格保持、通学1格改变；当前250格与冻结V72基线逐格相同。本轮重新计算压力情景，发现推荐对单城区间扩张比V69更敏感；此前V69阈值不能沿用于当前模型。

| 检验 | V69输入 | 当前V72输入 |
| --- | --- | --- |
| 全城同幅扩张，ε∈[0,0.20]、α∈[0.05,0.20] | Singapore | Singapore；48个已认证矩形，未决0 |
| 只扩张Singapore，首次失效的已证括区间 | (0.05,0.075] | (0.025,0.05] |
| 默认α=0.10的已检验失效情景 | ε=0.10时Tokyo | ε=0.075时Tokyo |
| 只扩张Singapore至ε=0.20、连续α范围 | Tokyo | Tokyo；3个已认证区间，未决0 |

当前已证明ε≤0.025、整个α范围保持Singapore（7个矩形，保守差距下界0.111652）；ε=0.05、α=0.05时Tokyo的最大遗憾比Singapore小0.396917，二者交换第1/2名。这一反例给出括区间上端，并不假定推荐差距随ε单调，也不代表精确临界值。42个离散压力情景中可能冠军均为25城。

与[本轮修订前V70冻结检验](../task4_v72_pre_revision_stress/README.md)相比，上述推荐、失效反例与认证差距相同。因此比V69更早失效来自V70人口/岗位修订，不能归因于本轮墨西哥城年龄调整。

## 数学含义

对指定城市行，把效用端点改为

$$l_{ij}^{\epsilon}=\max(0,l_{ij}-\epsilon),\qquad h_{ij}^{\epsilon}=\min(1,h_{ij}+\epsilon).$$

ε是无量纲效用端点扩大量。全城扩张与仅推荐城扩张分别计算；它们是明确指定的假设情景，没有被写回真实证据矩阵。均匀扩张下推荐稳定，不推出任意来源误差下稳定。

核心模型保持

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

八项主指标各取(1−α)/8，两项辅助指标各取α/2；默认α=0.10，检验[0.05,0.20]。通学效用exp(−t/30)，教育岗位资源效用15T/(N+15T)。区间及人口、时期、岗位条件保留，`main_admitted=false`。

## 实际改善与验证

本轮把“推荐仍第一”与“推荐能承受多大指定扰动”分开，找到了当前输入下更早的推荐翻转。没有新增观测、缩小缺失界或宣称冠军已识别。矩形认证采用端点包络、1e−9浮点保护和1e−8严格差距阈值；它是数值认证，不是形式化区间算术。

[完整情景](scenario_ranks.csv) · [摘要](summary.json) · [真实基线排名](baseline/ranks.csv) · [全城认证](uniform_prefix_certificate.csv) · [单城前缀认证](targeted_prefix_certificate.csv) · [历史V69对照](../task4_v69_joint_stress/README.md)

复现：

```sh
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py --output research/2026-a/results/task4_v72_joint_stress --targeted-prefix-max .025
python3 -m unittest discover -s research/2026-a/scripts -p 'test_task4_joint_uncertainty_stress.py'
```

未修改Overleaf论文。
