# 当前模型：V23 条件基准与 V26 通学尺度检验（2026-11-07）

当前十指标基准推荐 Singapore：最小最大遗憾为 28.173588 分，25 城仍全部是可能冠军。这里的推荐是在现有证据区间下选择最坏遗憾最小的城市，尚未识别唯一绩效冠军。V23 基准平均得分区间宽度为 37.916339 分；V26 直接重算五个通学尺度后首选保持，但最多 11 城的决策名次改变。

基准入口为 [task4_roster_coverage_comparison.py](../scripts/task4_roster_coverage_comparison.py) 的 `current_bounds(nyc_scope='under19', include_outcome=False, sampling=True)`。它接续已有证据，并更新 NYC、Mexico City 和 Melbourne 通学界。V26 是该基准的参数敏感性分析，不替换其数据范围或评分方法。V7 及其采集阈值属于历史结果。

## 指标、效用与权重

评价 25 个候选城市。八项主指标为凶杀率、PM2.5、生活成本指数、房价收入比、高中学生／教师人数比、研究型高教机构密度、学生通学、固定宽带速度；两项辅助指标为公共交通密度和公共泳池密度。[评分实现](../scripts/task4_v5_model.py) 的 `SPEC` 保存方向与固定锚点，`weights()` 定义：

$$w_j=\begin{cases}(1-\alpha)/8,&j\text{ 为主指标},\\\alpha/2,&j\text{ 为辅助指标},\end{cases}\qquad \alpha=0.1.$$

即主指标各 0.1125、辅助指标各 0.05。除通学外，非负原值 $x$ 按指标锚点 $a>0$ 转为成本效用 $u^-(x)=a/(a+x)$ 或收益效用 $u^+(x)=x/(a+x)$。通学直接使用 $u(t;\tau)=\exp(-t/\tau)$，$t$ 为学生通学分钟数，基准 $\tau=30$；它不再经过上述收益变换。

每个城市—指标保留效用界 $[l_{ij},h_{ij}]\subseteq[0,1]$。完全未知保留 $[0,1]$；部分设施名录仅支持收益下界。部分辖区事件数 $d$、完整地域人口 $P$ 给风险率下界 $x_L=10^5d/P$，对应成本效用界 $[0,a/(a+x_L)]$。数据准入、地域与分母条件随原始证据保留。

## 通学区间与人群范围

对学生权重 $p_r$ 和个体效用界 $[l_r,h_r]$，已知成员的加权识别界为

$$\underline T=\frac{\sum_r p_r l_r}{\sum_r p_r},\qquad
\overline T=\frac{\sum_r p_r h_r}{\sum_r p_r}.$$

已观察时长直接取指数效用；时间箱 $[a_r,b_r]$ 转为 $[e^{-b_r/\tau},e^{-a_r/\tau}]$；未知时长保留 $[0,1]$。Mexico 另对可选成员资格取极值：已知成员权重 $N$、分子界 $[A,B]$，可选成员权重 $v_r$、效用界 $[a_r,b_r]$，则

$$\underline T=\min_{z_r\in\{0,1\}}\frac{A+\sum_r z_rv_ra_r}{N+\sum_r z_rv_r},\qquad
\overline T=\max_{z_r\in\{0,1\}}\frac{B+\sum_r z_rv_rb_r}{N+\sum_r z_rv_r}.$$

默认 NYC 为 under19、2010—11 年历史日记；Mexico 为 2020 年未成年条件范围，当前高中阶段依赖已完成学段／年级进阶假设；Melbourne 为 Greater Melbourne、Secondary 在读且 15—19 岁，尚未单独识别高中年级。Melbourne 名册中 170 名有个人权重者含 107 名有旅程和 63 名无旅程者，使用第一条教育旅程与 10 组官方个人重复权重。端点抽样包络采用

$$SE(\theta)=\sqrt{\frac{9}{10}\sum_{r=1}^{10}(\theta_r-\theta)^2},\qquad
[\max(0,\underline T-t_{9,.975}SE(\underline T)),\min(1,\overline T+t_{9,.975}SE(\overline T))].$$

Sao Paulo 保留全年龄当前高中在读与镜像来源条件，Singapore 保留阶段混合条件。NYC 和 Sao Paulo 的家庭重抽样为探索性；Melbourne 为近似端点推断。城市年份、地域和学段不统一，未构造全城市联合置信区域；V23 与 V26 输出均标记 `main_admitted=false`。具体来源与审计见 [V23 报告](../results/task4_v23_roster_coverage/README.md) 和 [V26 报告](../results/task4_v26_direct_travel_scale/README.md)。

## 评分与决策

对效用向量 $u_i$，以固定理想点 1、负理想点 0 计算

$$D_i^+=\sqrt{\sum_jw_j(1-u_{ij})^2},\qquad
D_i^-=\sqrt{\sum_jw_ju_{ij}^2},\qquad
S_i=100\frac{D_i^-}{D_i^++D_i^-}.$$

评分对各收益方向效用单调；在矩形不确定性集合（允许端点同时实现）下，城市得分界为 $L_i=S(l_i)$、$U_i=S(h_i)$。可能冠军集合、最大遗憾和推荐为

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\qquad
R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad
\mathcal I^*=\arg\min_iR_i.$$

决策名次按 $R_i$ 从小到大排列，并列取最小名次；它不是已识别的真实绩效名次。[区间决策实现](../scripts/task4_interval_decision.py) 与 [V23 排名](../results/task4_v23_roster_coverage/ranks.csv) 可复核结果。

## 当前结果与敏感性边界

V23 默认十指标情景对应输出筛选 `model=v16_ten_criteria`、`nyc_age_scope=under19`、`scenario=both_sampling_envelope`。250 个效用单元中 111 个较完全未知区间有信息；Singapore、Melbourne、Phoenix 的决策名次分别为 1、4、24。完整 [效用界](../results/task4_v23_roster_coverage/utility_bounds.csv) 与 [摘要及输入哈希](../results/task4_v23_roster_coverage/summary.json) 记录基准。

[V26 脚本](../scripts/task4_direct_travel_scale.py) 在 $\tau\in\{15,20,30,45,60\}$ 分钟下，从现有学生时长和原始分箱直接重算五城通学界，保留成员资格、个人权重与原抽样方法；其余 20 城通学未知区间及所有非通学单元保持不变。30 分钟逐单元复现 V23，无新增观测。

| 通学尺度（分钟） | 首选 | Phoenix 决策名次 | 相对 30 分钟改变名次的城市数 | 可能冠军数 |
| --- | --- | ---: | ---: | ---: |
| 15 | Singapore | 24 | 9 | 25 |
| 20 | Singapore | 24 | 7 | 25 |
| 30 | Singapore | 24 | 0 | 25 |
| 45 | Singapore | 24 | 9 | 25 |
| 60 | Singapore | 24 | 11 | 25 |

表中固定 $\alpha=0.1$；连续 $\alpha\in[0.05,0.20]$ 的可能冠军可行性检验也保留全部 25 城。该结果不证明连续 $\tau$ 范围内首选始终不变。数据见 [V26 排名](../results/task4_v26_direct_travel_scale/ranks.csv)、[通学界](../results/task4_v26_direct_travel_scale/travel_bounds.csv) 与 [摘要](../results/task4_v26_direct_travel_scale/summary.json)。

`include_outcome=True` 是另列的十一指标情景：原十项权重乘以 $1-\beta$，毕业结局效用 $q$ 以权重 $\beta=0.1$ 加入同一距离公式。该情景最小最大遗憾为 32.898359，Melbourne 第 5；它不属于上述十指标基准或 V26 检验。

## V29：最新教育年份替换情景

[同口径年份更新](../results/task4_v29_education_year/README.md)将Jakarta的SMA师生比替换为2025/26学年的186461/11983，教育效用为0.4908302977。入口为[updated_bounds()](../scripts/task4_education_year_update.py)，其余249个单元及上述公式保持。Jakarta仍第17，Singapore仍为推荐，可能冠军25城。旧基准函数保留，两个年份不取交集；来源仍是明确标记的官方索引表转录，未增加城市指标覆盖，也未据此改动论文。
