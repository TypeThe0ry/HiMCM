# 连续偏好下的最小补数集合

固定 V7 观测及其缺失区间，枚举每城不确定指标子集，并检验该子集在取现有下界的假设情景下，能否对所有 alpha∈[0.05,0.20] 排除该城。相较固定 alpha=0.10，20 城的最少项数增加一项。Istanbul 从1项增至2项；Phoenix仍为4项，共25组最小集合。

这些是有利于排除的假设结果下的必要项数，不保证采集这些数据就会排除城市，也不是采集成本或预期信息收益估计。保持其他城市下界固定，只允许补本城；跨城联合采集不在此最小化问题内。真实调查通常提供区间而非精确值，因此实际需求可能更多。

## 公式及算法

评分沿用 S_i=100 sqrt(B_i)/(sqrt(A_i)+sqrt(B_i))，B_i=sum_j w_j u_ij²，A_i=sum_j w_j(1-u_ij)²。八个主指标权重为(1-alpha)/8，两个辅助指标为alpha/2。

给定补数集合 J，定义 h_i^J 的第j项在 j∈J 时为 l_ij，否则为 h_ij。求最小 |J|，使：

对每个 alpha∈[0.05,0.20]，存在 k≠i，满足 S_i(h_i^J,alpha)<S_k(l_k,alpha)。

利用评分对效用的单调性，下界是该集合最有利于排除的补全结果。连续偏好检验调用二次多项式全部实根分区，数值容差1e-12。严格不等号保留平局为可能冠军。该方法适用于本模型的矩形缺失集合与分组等权假设。

## 输出与验证

minimum_measurements.csv 对比固定权重和连续范围的最小项数；minimal_bundles.csv 保存全部最小集合。Istanbul 的6组为 homicide_rate+public_transport_density、homicide_rate+travel、homicide_rate+public_pool_density、public_transport_density+travel、public_transport_density+public_pool_density、travel+public_pool_density。

25城退化范围 alpha=0.10 与既有固定权重算法逐城一致；连续范围最小项数未降低；输入数组逐元素不变。本轮无新增准入观测，排名和25城可能冠军集合沿用相同输入的 V8 重跑结果。复现：python3 research/2026-a/scripts/task4_robust_acquisition.py。

## 新教育数据线索（尚未准入）

Arizona 官方 [数据入口](https://cms.azed.gov/accountability-research/data) 链接学校毕业率 [2024 cohort XLSX](https://cms.azed.gov/sites/default/files/2025/04/4Y-GradRate-Cohort2024.xlsx) 和 [2025 math/ELA XLSX](https://cms.azed.gov/sites/default/files/2025/10/math_ela_assessmentsfy25.xlsx)。这些成果指标比师生比更直接衡量教育结果，但尚需核实学校ID、分母、掩码、学校覆盖和城市聚合口径。2026-11-07直接下载毕业率文件返回HTTP403、HTML4556字节，没有伪装保存为XLSX或提取数值。下一步是取得实际文件后与市界内学校清单匹配；不将学区结果代替全市结果。
