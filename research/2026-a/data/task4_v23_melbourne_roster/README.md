# V23 Melbourne：保留未观察通学的在读学生

旧版仅使用已有教育旅程的 15—19 岁中学生，得到 108 条旅程、107 人。完整官方 Persons 名册中，同地域、同工作日、同年龄组的当前中学生共有 171 人：170 人有官方个人权重，107 人有教育旅程、63 名有权重者没有教育旅程；另 1 人拒填或缺少日记且无个人权重。

修订保留无教育旅程者的效用区间 [0,1]，把统计对象从“已发生的旅程”改为“官方个人权重支持的当前中学生”。没有观察到旅程可能来自当天未到校、无相应旅程或资料缺失，不能当作零分钟，也不能凭原因未知删去。该处理是对未观察通学效用的区间化，不宣称这些学生当天实际发生了通学。

## 可直接复用的结果

| 口径 | 有权重人数 | 已观察首个旅程 | 无旅程人数 | 个人权重效用识别区间 | 名义 jackknife 抽样包络 |
|---|---:|---:|---:|---|---|
| 当前 Secondary 且 15—19 岁组 | 170 | 107 | 63 | [0.362247, 0.709798] | [0.278896, 0.781095] |
| 当前 Secondary、全部年龄 | 317 | 205 | 112 | [0.331635, 0.697033] | [0.251476, 0.791576] |

15—19 岁组已观察者的个人权重平均效用为 0.555211；旧版旅程权重平均为 0.553543。两者接近，主要修订来自保留未观察旅程者，而非权重数值替换。抽样包络宽于识别区间，是加入抽样不确定性后的结果。

`summary.json` 的 `scopes.secondary_15_19` 和 `scopes.secondary_all_ages` 均提供：`utility_lower`、`utility_upper`、`sampling_lower`、`sampling_upper`、`observed_only_person_weighted_utility`。`variants` 另存官方 elapsed 与仅运输停靠两种定义；本样本先取每人最早旅程后，两定义结果相同。

## 学段、地理及覆盖

官方 Persons 字典将 `studying` 定义为当前学生状态（Level or None），`Secondary` 与 Primary、TAFE/Uni、No Study 分开。它直接识别中学在读状态，但没有具体年级；15—19 岁组也不能精确识别 14—18 岁或仅 11—12 年级。因此这是“当前中学在读且年龄 15—19”条件口径，不是已经核实全部高中年级。

地域为 `homeregion_ASGS == Greater Melbourne` 的 GCCSA。Household 文件可连接 `homelga`，但行政 City of Melbourne 仅 2 名工作日中学生、同一户，不能把大墨尔本数据宣传为该行政市估计。

有 1 名 15—19 岁学生、全年龄中学生合计 5 名缺少个人权重，原记录保留于审计文件。官方说明 §3.4 包括家庭非应答调整，个人权重再校准至 Census 的性别、年龄、Studying 和职业类别目标。无权重记录数量不等于未覆盖人口数量；本次不为其填权重，也不把它们额外加为另一份人口。外推依赖官方抽样、非应答和校准假设。

## 旅程与权重定义

官方 Journey to Education 定义为最后一次离家至首次到达教育地点，`journey_elapsed_time` 包括出行和途中停留。每个人先按数值 `start_time` 选最早一条 JTE，再检查途中用途；所有选中的 107/205 条均符合 Education、Change Mode、Accompany Someone、Pick-up or Drop-off Someone 白名单。一个含 Personal Business、Social 的 68 分钟旅程是当事人的第二条，已因最早旅程规则排除。不能先删活动旅程、再选更晚的旅程冒充首次通学。

官方 general elapsed 定义允许其他活动停留，与 NYC 的运输停靠专用规则并非先验等价；本轮列出两种定义的实际筛查结果，不据此宣称所有城市测量已经统一。

对有官方个人权重者，已观察首个旅程赋值 `u=exp(-elapsed_minutes/30)`，未观察赋区间 [0,1]。使用 `perspoststratweight` 计算：

`L=Σw_i l_i/Σw_i，U=Σw_i h_i/Σw_i`。

每个端点分别以 10 组 `perspoststratweight_GROUP_1 ... GROUP_10` 重复计算。官方说明 §3.5.2 给出：

`Var(theta)=(R−1)/R Σ_r(theta_r−theta)^2，R=10`。

采用 `t_(9,0.975)=2.262157`，报告 `[max(0,L−t SE_L), min(1,U+t SE_U)]`。两个端点各使用名义 2.5% 单侧尾部，以组合成名义 95% 包络。这是本项目应用官方重复权重方法得到的近似抽样包络，不是官方发布的区间；它不覆盖学段、覆盖、地理转移、测量误差或旅程定义的误差。无需假装旅程文件具有重复权重，重复权重来自个人文件。

工作日总量需按官方说明乘 7/5；本项目只计算比值，两端点及每个重复估计的该因子均相消。

## 文件与复核

- [提取脚本](extract_roster.py)：读取已归档的官方原文件，不修改旧数据。
- [汇总结果](summary.json)：原件 URL、SHA256、两个年龄口径及方法。
- [完整中学生名册审计](roster_audit.csv)：包括无权重、无旅程记录。
- [个人效用上下界](person_utility_bounds.csv)：仅官方有权重分析行，两种旅程定义均保留。
- [测试](test_extract.py)：核验缺失权重不被静默忽略、未观察效用保留、工作日比例缩放、官方方差系数、真实名册及首次旅程选择。

复跑：`python3 research/2026-a/data/task4_v23_melbourne_roster/extract_roster.py`；测试同目录 `test_extract.py`。源文件位于 [既有 VISTA 数据目录](../task4_school_commute_extra/README.md)，哈希逐一验证，未重新下载或改写原件。
