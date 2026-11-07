# V71：补查四地资料，并把通学来源校验接入复算

本轮取得新的官方原件，但没有新增可准入的城市通学观测。当前科学模型保持V70：250格输入、25城全部决策排名和可能冠军集合均未改变；Singapore第1、Tokyo第2、Phoenix第24，固定及连续α∈[0.05,0.20]的可能冠军仍25城。连续推荐仍为Singapore，未决区间0。[本轮冻结复算](baseline/summary.json)、[排名](baseline/ranks.csv)保留检查结果。

## 新资料改变了哪些判断

| 地点 | 新原件与可核验事实 | 准入结论 |
| --- | --- | --- |
| Singapore | [MOE年级×年龄完整表及国会答复](../../data/task4_v71_singapore/README.md)：2020 Sec3–5共82198人，年初14–17岁82000人；国际生不足5% | 统计日、居民范围、课程及不通学者排除未与Census对齐，不能把该数当高中通学子群人数下界；保持[0,1] |
| Phoenix | [Valley Metro官方高中公交研究](../../data/task4_v71_phoenix/README.md)：41所公立高中，ACS社区人口与公交供给指标 | 文中去回各10分钟是节时算例，非学生观测；保持缺失界 |
| New York | [NYMTC新调查采购材料、2026学生问卷及NYSDOT2017分析](../../data/task4_v71_nyc/README.md) | 采购不等于数据已发布，安全感不等于时长，公共SCHTYP不等于高中年级；保留现有真实RHTS旅程 |
| Mexico City | [ENUT2024与ENIGH2024官方问卷、字典、手册](../../data/task4_v71_mexico/README.md) | 一项有周往返时间但已完成学段，另一项有当前就读学段但混合学习时间；不能把独立调查拼成个人高中通学记录 |

以上都没有被填成新分数；原始问卷、表格、API或官方网页与哈希保留在各证据包。

## 当前究竟用了哪些通学数据

新增[当前证据索引](currenttravel_evidence.csv)逐一核对当前工厂输出与来源摘要的端点，结果为5城有条件的信息区间、20城[0,1]。五城为New York、Mexico City、Sao Paulo、Cape Town、Melbourne。这里“有信息”不等于完整识别14—18岁高中生、近期城市总体或无条件置信覆盖；CSV分别保留年龄、学段、地域、年份、通学观测类型及限制。

尤其是New York，当前采用V21的2010—2011 RHTS真实高中旅程与交通停靠链，早期NYU路线估计并非当前输入。Mexico City仍带已完成年级推断当前学段的条件；Melbourne仍为15—19岁Secondary且有缺失人员权重条件。Singapore另外登记V70撤回原因。历史资料存在不等于当前模型正在采用。

[索引程序](../../scripts/task4_travel_evidence_index.py)现已接入[统一运行入口](../../scripts/task4_current_model.py)，在任何结果文件写入前执行：

1. 当前有信息城市集合必须与显式登记相等；新增城市或陈旧登记均拒绝。
2. 城市效用端点必须与指定来源摘要及指定人群一致，容差1e-12；不根据“最新文件名”猜来源。
3. 原始资料路径必须存在，输出记录摘要、索引和注册表哈希。

它验证当前数据与来源声明的一致性，不自动证明源调查代表性或原始采集质量。两套focused测试共9项通过，包括从登记中移除New York后主程序拒绝运行且不产生输出目录的集成反例。独立审查另用标准库核对25城全部端点及五城来源，不依赖新索引实现。

## 本轮改进与剩余缺口

工程改进阻止把历史代理或新调查计划误用为当前输入，未制造精度或排名提升。Singapore的同总体子群人数、Phoenix的高中身份×地域×实际时间联合记录，仍是明确缺口；当前5城有条件信息的范围差异也继续保留。没有修改论文。

## 当前数学模型

令城市i各效用为uᵢⱼ∈[lᵢⱼ,hᵢⱼ]；八项主指标权重(1−α)/8，两项辅助指标α/2，默认α=0.10。通学效用exp(−t/30)，t为通常单程分钟；教育资源效用15T/(N+15T)，其岗位与学段条件见V70。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

区间为条件矩形外包，`main_admitted=false`；可能冠军不是胜出概率。V69压力阈值、V68补数数量界仍属于历史输入，本轮未重新认证。

```sh
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/task4_travel_evidence_index.py
python3 research/2026-a/scripts/test_task4_current_model.py
python3 research/2026-a/scripts/test_task4_travel_evidence_index.py
```
