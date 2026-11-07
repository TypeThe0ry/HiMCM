# V4：高中教育结果与学生通学证据驱动的修订

日期：2026-11-07（Asia/Singapore）。已运行并归档；不是完整、同年、精确14—18岁、全市所有学校的最终榜单。

## 这次真正补到了什么

| 城市 | 新证据 | 实际数值 | 如何使用 |
|---|---|---|---|
| Melbourne | 官方VISTA 2024–25，大墨尔本15—19岁Secondary工作日上学旅程 | 108旅程、107人、93户；加权21.0284分钟，45分钟以内93.0252% | 旅程效用均值0.553543进入条件情景；家庭bootstrap另检验 |
| New York | 官方Grade 9入学届四年August高中毕业结果 | 2021届至2025年，58,660/72,283=81.1532% | 非charter公校学历完成代理；不称教学增值 |
| Toronto | Ontario官方两英语公费教育局四年高中毕业结果 | 2020–21入学届至2023–24年：TDSB81.8%，CDSB88.4% | 权重未知，使用两局混合与取整包络[0.8175,0.8845]；不称全市全校率 |
| Singapore | 2020人口普查按学段的实际通学时间分组 | Secondary172,487人、post-secondary non-tertiary55,674人 | 分别求分组效用上下界，再做未知学段混合的条件情景 |
| New York | NYU研究，2013–14九年级学生住址—实际学校匹配 | 步行/公交估计单程平均31分钟 | 只用均值推出效用界，不伪造旅行分布；历史迁移单列 |
| Copenhagen | 2022年15—19岁到最近高中设施的公共交通可达性 | STx15分钟92%、30分钟100%（整数百分比） | 留作高中设施证据；未含容量和录取，拒绝替代实际通学 |
| Singapore | 官方2024 A-Level考试结果 | 3H2及GP/KI通过率94.2% | 属高中阶段结果，但分母为考生；拒绝与入学届毕业率混算 |
| Melbourne | VCAA2025高中学校VCE/VM/VPC结果表 | 已归档原表 | 未完成地理及分母对齐，不假造城市四年毕业率 |

来源：[VISTA](https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista)、[NYC毕业结果](https://infohub.nyced.org/reports/academics/graduation-results)、[Ontario](https://data.ontario.ca/dataset/school-board-achievements-and-progress)、[新加坡通学](https://data.gov.sg/datasets/d_e87b21cfebae1a77150eccded58ab116/view)、[NYU研究](https://steinhardt.nyu.edu/research-alliance/research/spotlight-nyc-schools/how-far-do-nyc-students-travel-get-school)、[丹麦报告](https://www.regioner.dk/media/23883/danske-regioner-rejsetid-til-ungdomsuddannelser.pdf)。原始文件、字典和SHA256均在三个task4_school数据目录。

## 模型说人话

评价内容现在明确问：城市基础条件如何、学生能否完成本地高中学历、上学实际花多少时间。就近设施与实际通学分开；教学质量没有被“学校很多”替代。毕业率也只是教育结果代理，受到选择、家庭背景和各地毕业制度影响，不是国际统一知识标准。

原四项代理各占20%，高中学历完成E占10%，学生通学T占10%。原四项仍含成人通勤，因此另做删除成人通勤消融。权重是分析选择，未通过调参追求冠军变化。

T=E[exp(-t/30)]，30分钟是效用衰减参数，不是政策规定。

分组时间只能给区间：T下界=Σp_b exp(-b_b/30)，上界=Σp_b exp(-a_b/30)。最后“超过60分钟”组的最大时间为无穷，不强填75或90分钟；对应效用下确界0。新加坡Secondary得[0.370252,0.614811]，post-secondary non-tertiary得[0.244826,0.419224]。两组未知混合包络为[0.244826,0.614811]。

这个包络只覆盖两个完整学段总体的任意混合，**不保证覆盖其中精确14—18岁子群**。主结果明确接受学段迁移；严格不接受迁移时重新保持未知。墨尔本也仅能筛15—19岁，中学生不能进一步分出只有11—12年级。

纽约只有均值，由Jensen不等式得T≥exp(-31.5/30)=0.349938，上确界1；31.5含整数均值取整假设。不把exp(-31/30)当真实平均效用，也不从均值猜最差20%。墨尔本有实际旅程分布，可计算完整均值及低尾，独立数据报告保留这些结果。

使用原固定理想点TOPSIS：D负=sqrt(Σw_j z_ij²)，D正=sqrt(Σw_j(1-z_ij)²)，C=D负/(D负+D正)。对缺失E、T保留[0,1]，单调端点给出得分[L_i,U_i]。未随机补数，未用全国PISA代替城市高中结果。

## 修订前后，实际改变多少

必须分开两种对照：

1. **V3→V4换了评价对象**：V3的全年龄Learning POI代理退出学校通学维度，改成上述学生实际通学和学历完成。原来3城可能冠军的结论不能直接延续；V4为12城。这不等于城市变差，也不是统计置信区间变宽。
2. **同一V4补数前→补数后**：前后均保持原四项80%、E10%、T10%；只将本轮观测加入约束，才能衡量证据的作用。

| 城市 | 补数前可行名次 | 补数后可行名次 | 最小最大后悔决策顺序（前→后） |
|---|---|---|---|
| Copenhagen | 1–12 | 1–12 | 1→1 |
| Melbourne | 1–17 | 1–13 | 3→2 |
| Toronto | 1–24 | 1–14 | 8→3 |
| Dubai | 1–15 | 1–15 | 2→4 |
| New York | 1–24 | 1–16 | 12→5 |
| Singapore | 1–23 | 1–19 | 7→6 |

完整25城见ranking_comparison.csv。决策顺序是按最坏后悔排列的行动建议，**不是声称城市真实名次已确定**，更不能把纽约12→5写成教育质量升了7名。11城决策顺序变化，Kendall tau-b=0.8933；15城可行名次端点变化，部分变化来自其他城市下界上升。

平均得分区间宽度17.1029→15.8427，缩小约7.37%。可能冠军前后均为12城：Toronto、Phoenix、New York、Copenhagen、Barcelona、Warsaw、Athens、Cape Town、Dubai、Tokyo、Singapore、Melbourne。没有必要冠军。

哥本哈根仍为最小最大后悔建议，但最坏后悔前后均14.5979分，**本轮没有改善最终首选的最坏决策损失，也没有缩小冠军集合**。改善集中在部分城市的可行名次与证据对象匹配，不能宣传为准确率提升。

## 算法的实质新增：让模型决定下一项证据查哪里

固定权重、独立城市区间下，最大后悔可精确算：

R_i=max(0,max_{h≠i}U_h−L_i)，R*=min_i R_i。

候选i可能第一当且仅当U_i≥max_{h≠i}L_h；允许并列，必要第一与必然唯一第一在代码中分开。开口端点使用保守闭包。精确性针对给定矩形不确定集；有跨城共享参数或额外联合限制时只是外包络。

对城市k某一未知指标x，假设下一次把它精确测出，其他缺口仍保留。选择k的后悔A(x)随x下降，其他城市的最佳后悔B(x)随x上升。因此补数后的min(A(x),B(x))在交点或端点取得最坏值，二分即可求解：

保证补数价值=R*−max_x min(A(x),B(x))。

这比给所有缺失值随意设均匀分布再做Monte Carlo更有可解释依据：不需要假造数据分布，给出明确的条件和可检验的边界。数学构件来自区间决策和信息价值思想，不声称全球首次。

本轮实算：优先查哥本哈根E或T，在理想“精确测量且其他设定不变”条件下，各自保证降低最优最坏后悔约1.1373分，最好可能降低8.3617分；迪拜相应保证值为0、最好可能5.2783分。详见evidence_acquisition_priority.csv。

这是**未来精确观测的潜在价值，不是本轮已经实现的改善**。实际只能取得区间时收益更低；未计数据采集成本，不能称成本最优采集政策。

## 敏感性与尚缺什么

- 墨尔本93户做2000次家庭聚类bootstrap，均值效用探索性范围[0.503907,0.601583]；不是完整调查设计校正置信区间。使用此范围，12城集合不变。
- 两个学校维度分别5%、10%、20%的9组权重情景见weight_sensitivity.csv，表中不隐藏设定变化。
- 对已纳入效用再放宽±0.05、±0.10、±0.20，见scope_and_time_stress.json；这些是压力假设，不是实测误差率。
- 删除成人通勤并把原三项总权重固定80%，可能冠军变为9城。由于模型改变，这不算补数据产生的排除。
- 若要求2025/2026、精确14—18岁、全市全学校且拒绝未验证迁移，则本轮学校维度仍不能构造完整城市矩阵。strict_scope_rank_intervals.csv对此不假装精确。
- NYC历史九年级出行、Toronto部分教育局、Singapore学段混合、Melbourne15—19岁抽样人群均存在边界。没有任何一条可推导完整城市教学质量因果排序。

尚缺优先项：哥本哈根与迪拜可比的高中入学届完成数据、实际就读学校通学调查；以及跨城年龄/部门/年份口径。新增来源可再次收缩集合，无需改变算法或为缺失编数。

## 文件与验证

主脚本：../../scripts/task4_school_revision.py；决策模块：../../scripts/task4_interval_decision.py；独立审核：../task4_school_review/review.md。

复现（仓库根）：

```sh
python3 research/2026-a/data/task4_school_quality_extra/extract_quality.py
python3 research/2026-a/data/task4_school_commute_extra/derive_melbourne.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/task4_school_revision.py
python3 research/2026-a/scripts/task4_interval_decision.py
```

检查包括原始文件哈希、教育局/表头/入学届匹配、纽约人数与百分比一致性、新加坡分组人数、分组上下界可行分布检查、Jensen检查、信息区间嵌套、20组角点枚举的精确名次/后悔检验、20组非线性补数的密网格对照，以及墨尔本连接/权重/首次旅程敏感性。仅更新本地研究归档，未改Overleaf正文。
