# V77：Mumbai高中人数对账与当前排名复算

本轮新增的是可复核的学段核验，主模型仍为V72。两名agent分别核对原始PDF，未修改论文。

## 真实数据补充

[Mumbai来源核验包](../../data/task4_v77_mumbai/README.md)明确2024–25年11—12年级人数：City 71,840，Suburban 206,698，合计278,538。Suburban的学校类别表与逐年级表一致；City的类别表少14,315人。两地全部三类学校学生总数又分别与全年级人数完全相符，因此不能把某一学校类别直接等同于高中年级。

全部学校类别教师合计54,723。只有在这些教师覆盖全部对应高中生的条件下，才能推导教育效用上界0.7466415253；现有资料未确认这一教师覆盖关系，主模型Mumbai教育区间保留[0,1]。这一核验避免了直接拿不匹配的学生数与教师数相除，并没有形成实际缩区间。

Phoenix未取得可准入的高中生实际通学联合记录。Jakarta调查还需区分跨行政区通学与市内通学；本轮没有录入新的通学观测。Cape Town继续使用已取得的GHS2025高中生通学数据，见[来源与抽样处理](../task4_v63_cape_2025/README.md)，无需重下载GHS2023。

## 修订前后

统一入口复算核对全部250个指标区间与V72基线。具体排名见[CSV](baseline/ranks.csv)，连续权重核验见[摘要](baseline/summary.json)。

| 指标 | 本轮前 | 本轮后 |
| --- | ---: | ---: |
| 实际变更的城市指标区间 | — | 0 |
| Singapore决策排名 | 1 | 1 |
| Tokyo决策排名 | 2 | 2 |
| Cape Town决策排名 | 5 | 5 |
| Phoenix决策排名 | 24 | 24 |
| 固定权重可能冠军数 | 25 | 25 |
| 连续偏好范围可能冠军并集 | 25 | 25 |

本轮没有缩小可能冠军范围。有效进展是识别并定位人口与教师统计的匹配问题；要收紧Mumbai教育区间，仍需教师池完整覆盖的填报定义。此前[连续补数阈值算法](../task4_v76_precision_frontier/README.md)仍用于判断哪些补数组合可能排除Phoenix，不将假想观测当成真实改善。

## 当前公式

令效用区间为 $u_{ij}\in[\ell_{ij},h_{ij}]$。教育效用 $u_E=15T/(N+15T)$，通学效用 $u_t=\exp(-t/30)$（分钟）。8项主指标权重各 $(1-\alpha)/8$，2项辅助指标各 $\alpha/2$，$\alpha\in[0.05,0.20]$。

$$S_i(u,\alpha)=100\frac{\sqrt{\sum_jw_j u_{ij}^2}}{\sqrt{\sum_jw_j u_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}}.$$

$$L_i=S_i(\ell_i,\alpha),\quad U_i=S_i(h_i,\alpha),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\}.$$

按 $R_i$ 由小到大给出决策排名；可能冠军条件为 $U_i\ge\max_{k\ne i}L_k$。这是当前矩形证据范围下的可能性，非夺冠概率。连续偏好下仍推荐Singapore，无未决认证区间；25城均未被排除。

复算命令：

```sh
python3 research/2026-a/data/task4_v77_mumbai/verify.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v77_sources/baseline
```
