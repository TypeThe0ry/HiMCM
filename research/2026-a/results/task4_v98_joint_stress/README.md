# V98：在当前V96输入上验证推荐的误差边界

主模型V96的全部250格保持不变。本轮将仍使用V91输入的压力检验重新运行，并保存独立的V96证书，避免用旧输入的稳定性结论支撑当前排名。

| 假设区间扩张 | 连续权重范围 | 结果 |
| --- | --- | --- |
| 全部城市，ε∈[0,0.20] | α∈[0.05,0.20] | 48个矩形证书均推荐Singapore |
| 仅Singapore，ε∈[0,0.042] | 同上 | 27个矩形证书均推荐Singapore |
| 仅Singapore，ε=0.043 | α=0.05 | Tokyo最大遗憾低0.022266分，推荐改变 |
| 仅Singapore，ε=0.20 | α∈[0.05,0.20] | 3个区间证书均推荐Tokyo |

以上四项诊断与V93/V91输入完全一致。Warsaw师资修订改善了其资源覆盖与排名，但没有改变这里的推荐失效证据。全城同步扩大区间的稳定性不能代替单城误差检验。

扩张定义为

$$l'_{ij}=max(0,l_{ij}-epsilon),qquad h'_{ij}=min(1,h_{ij}+epsilon).$$

仅对指定城市应用。ε是效用端点的假设放宽量，不是已测数据误差或概率。首次可能失效的已验证括区间仍为(0.042,0.043]；不据此声称所有更大ε都失效。区间端点与α端点的单调性给出各矩形内遗憾上下界，以1e−9数值余量和1e−8严格差值认证；并非形式化区间算术。

独立长双精度审计从保存的250格重算1350行、54个场景与78个连续证书叶，验证域覆盖且内部不重叠。代码不导入模型评分函数。六项现有压力算法测试通过。未改变任何真实区间，实际可能冠军仍25城。

复现：

```sh
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py --output research/2026-a/results/task4_v98_joint_stress --targeted-prefix-max .042 --extra-epsilon .043
python3 research/2026-a/results/task4_v98_joint_stress/audit.py
```

[摘要](summary.json) · [全部情景排名](scenario_ranks.csv) · [独立检查](independent_check.json) · [基线排名](baseline/ranks.csv)。
