# V69：学段修订后的联合不确定性检验

更新Singapore学段和Tokyo特教高中部覆盖后，旧V67的定向扩张稳定范围不能继续沿用。本轮以注册表选择的 **V69** 全部250格和同一权重范围重算：均匀扩张仍稳定，但仅扩大推荐城市Singapore的不确定性时，首次失去唯一推荐的阈值现位于 **(0.05,0.075]**，而V63输入上的旧证书区间为(0.10,0.15]。这是不同数据版本的同类压力情景比较，不能把变化单独归因于Tokyo新增数据。

## 运行结果

| 检验 | V69结果 |
| --- | --- |
| 全城市均匀扩张，ε∈[0,0.20]、α∈[0.05,0.20] | Singapore唯一推荐；36个矩形叶，0未决；最小保守遗憾差0.068245分 |
| 仅Singapore扩张，ε∈[0,0.05]、同一α范围 | Singapore唯一推荐；9个矩形叶，0未决；最小保守遗憾差0.259255分 |
| 仅Singapore扩张，ε=0.075、α=0.05 | Tokyo推荐；Singapore相对最优对手的遗憾差为−0.900258分，2城名次变化 |
| 仅Singapore扩张，ε=0.10、默认α=0.10 | Tokyo推荐；遗憾差−1.299502分，2城名次变化 |
| 仅Singapore扩张，ε=0.20、整个α范围 | Tokyo唯一推荐；2个连续α叶，0未决 |

因此，旧的“定向ε≤0.10连续偏好范围内稳定”在V69已经有明确反例，不是仅因数值证书未完成。ε=0.075时默认α=0.10仍推荐Singapore；失败发生在α=0.05，说明固定权重检查会漏掉这个反例。

所有42个抽查情景仍有25个可能冠军。连续矩形证书用于推荐稳定性，42点情景表只描述对应点的排名和候选集合，不能把点表当作完整二维证书。压力情景不修改实际数据；真实基准仍推荐Singapore、Phoenix第24。[基准](baseline/summary.json)、[情景排名](scenario_ranks.csv)、[摘要](summary.json)记录输入和结果。

## 数学定义与边界

对指定城市集合G，按同一效用端点扩张幅度ε设置：

$$l_{ij}^{\epsilon,G}=\max(0,l_{ij}-\epsilon\mathbf1_{i\in G}),\qquad h_{ij}^{\epsilon,G}=\min(1,h_{ij}+\epsilon\mathbf1_{i\in G}).$$

均匀情景的G为全部城市，定向情景的G仅为Singapore。ε是无量纲效用端点扩张，不是原始人数、时间或百分比误差；两种结构具有相同单格扩张上限，但总扰动量不同。评分和决策继续使用当前TOPSIS与最大遗憾公式：

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$R_i=\max\{0,\max_{k\ne i}S_k(h_k^{\epsilon,G};\alpha)-S_i(l_i^{\epsilon,G};\alpha)\},\qquad i^*\in\arg\min_iR_i.$$

八项主指标权重为(1−α)/8，两项辅助指标为α/2。评分关于固定效用下的α单调或恒定，区间扩张使下分不增、上分不减；利用这些性质构造每个ε×α矩形的遗憾界，再递归细分。保留所有未决叶，不假设推荐遗憾差对ε单调。上述首次失效阈值区间来自整个[0,0.05]前缀证书和ε=0.075失败见证，不是精确临界点。

分数余量1e-9，严格推荐差阈值1e-8；这是浮点数值证书，不是有向舍入区间算术证明。均匀扩张稳定也不代表任意城市、任意指标误差下稳定，且没有从数据估计实际源误差分布。

## 修复历史输出覆盖问题

[运行脚本](../../scripts/task4_joint_uncertainty_stress.py)现提供`run(out)`及`--output`；默认输出目录随当前数据模型版本命名，避免继续硬写V67历史目录。写入前核对已有输出的模型版本、全部输入区间哈希、固定权重和连续权重范围；不同基准直接拒绝写入。旧输出无区间哈希时读取其保存的基准CSV和注册表核验。

测试包含历史模型拒绝且文件字节不变、同版本数据变更拒绝、同版本权重变更拒绝，以及原有区间包络、平局和定向扩张检查，共5项通过。对真实V67目录的拒绝试验确认10个文件SHA256全部不变。

```sh
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py --output research/2026-a/results/task4_v69_joint_stress --targeted-prefix-max 0.05
python3 research/2026-a/scripts/test_task4_joint_uncertainty_stress.py
```

[均匀前缀证书](uniform_prefix_certificate.csv) · [定向前缀证书](targeted_prefix_certificate.csv) · [定向ε=0.20证书](targeted_epsilon02_certificate.csv) · [V67历史报告](../task4_v67_joint_stress/README.md)。本轮没有改动论文。
