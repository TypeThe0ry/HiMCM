# 最新数据下，Phoenix仍需要多项证据才能排除冠军可能

本轮在V30真实高中通学模型上重算补数诊断，不新增城市观测，不改变任何得分界。Singapore仍为推荐，Cape Town第5，Phoenix第24，可能冠军仍25城。

## 补数到底需要做到什么程度

在辅助权重连续区间[0.05,0.20]内，Phoenix有25组最少四项的本城补数方案。即使高中师生比与通学两项同时取当前效用下界，其上界得分仍56.402679，高于竞争城市最高下界49.355873，仍不能排除。25城最少补数数量均与V27相同。

本轮增加“证据强度门槛”，使仅报最少项数的诊断更具体。对某个四项方案B，设假想的新上界为

$$h'_j(\lambda)=h_j-\lambda(h_j-l_j),\quad j\in B,\qquad 0\le\lambda\le1.$$

其他上界及全部下界不变。对每个方案寻找使Phoenix在整个权重范围内都不再可能夺冠的最小收缩比例。二分法保留一端仍可能、另一端已排除的区间；40次迭代后区间宽度小于1e-12。

25组方案的门槛都约为**97.145%**。相同门槛来自这些方案中未知指标的相同区间及权重结构，不代表其采集难度相同。这意味着“最少四项”依赖极强的不利测量结果；不能把它解释成收集四项数据就一定能缩小冠军集合。收缩比例是条件规划参数，不是估计值、采集成功概率或允许人为调整的实测区间。实际数据到来后仍按来源和误差构造区间。

## 验证与公式

25城的固定权重最少项数与连续权重区间退化为单点时完全一致；每个方案门槛两侧分别通过可能性与排除检验。基准排名和得分逐项复现V30，输入区间哈希写入summary.json。本轮没有把规划情景写入真实评分输入。

当前评分仍为

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S(l_i),\quad U_i=S(h_i).$$

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\quad R_i=\max(0,\max_{k\ne i}U_k-L_i).$$

八主指标各0.1125、两辅助各0.05；通学效用为exp(-t/30)。排名按最坏遗憾递增；来源条件和抽样限制继承[V30](../task4_v30_cape_town/README.md)。

[最少补数方案](minimal_bundles.csv) · [Phoenix强度门槛](phoenix_resolution_thresholds.csv) · [教育与通学诊断](education_travel_diagnostics.csv) · [排名](ranks.csv)。

复现：`python3 research/2026-a/scripts/task4_post_cape_acquisition.py`。

新增[Phoenix官方来源审计](source_audit.md)：MAG就业/TRP服务的人员数与通勤圈不提供高中生旅程，未准入任何数值。
