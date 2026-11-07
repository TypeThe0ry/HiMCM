# V68：修正Singapore高中学段，撤回虚假精度

Singapore原教育输入使用Pre-U学生和教师；新取得的[UIS官方映射及提取](../../data/task4_v68_singapore/README.md)将Secondary 3–4 Express、Secondary 3–5 Normal列为ISCED 343，而Junior Colleges列为444。这证明原Pre-U代理不能直接解释为高中阶段师资。V68改用MOE报告的相应年级学生和教师总池，保留课程归属、教师分配及学校覆盖条件。

## 实际修订与排名

| 项目 | V63（V67仍采用） | V68 |
| --- | ---: | ---: |
| Singapore教育效用界 | [0.541549, 0.587187] | [0, 0.849407] |
| Singapore总分界 | [49.292136, 66.703329] | [45.062720, 68.900436] |
| Singapore最大遗憾 | 28.237325 | 32.466741 |
| Singapore / Tokyo / Cape Town / Phoenix决策名次 | 1 / 2 / 5 / 24 | 1 / 2 / 5 / 24 |
| 可能冠军数（固定α及允许范围内的并集） | 25 / 25 | 25 / 25 |

只改Singapore教育一格，其他249格逐项验证相等，所有决策排名保持、Kendall τ=1。连续α∈[0.05,0.20]推荐证书仍为Singapore，未决区间0。得分界扩大约6.43分，反映已发现的口径问题；排名不变不能证明旧数据正确。

主情景用学生数 $N=81569-q$，其中 $0\le q\le2838$ 是Specialised学校全Secondary学生池给出的未识别课程混入上限。因此 $N\in[78731,81569]$。教师按任教或受训学段分类，无法只用Secondary分类教师包住目标课程授课人数；采用全部报告学校Teacher总池，$T\in[0,29605]$。同一学校池内的课程分配仍未知：

$$u_E=\frac{15T}{N+15T}\in\left[0,\frac{15\times29605}{78731+15\times29605}\right]=[0,0.849406854550].$$

这是MOE表内学校和课程的条件资源外包，不是实际教师FTE或全城国际学校覆盖界，也未实施14—18岁筛选。UIS映射参考年2023、MOE观测年2024，课程对应条件保留。`main_admitted=false`。

另跑三种敏感性：只限Secondary分类池（上界0.701806）、全部N(T)课程归属均未识别（上界0.860739）、完全撤回Singapore教育证据[0,1]。三者均保持原决策排名、25城可能冠军和连续Singapore推荐。全部情景保存在[摘要](summary.json)、[排名](ranks.csv)、[逐格效用](utility_bounds.csv)与[连续证书](recommendation_certificate.csv)。

## 为什么继续补教育、通学仍不足以识别冠军

复用已有[V45补数极限算法](../../scripts/task4_acquisition_limits.py)，在**V68**输入上重新计算：假设所有25城的教育、通学共50格均得到原区间内的精确观测，其余指标不变。对每座城市构造最有利于排除它的完成情况：本城被测格取原下界、其他城市被测格取原上界。令测量掩码为 $M$：

$$\bar u_{ij}^{\mathrm{worst}}=\begin{cases}l_{ij}&M_{ij}=1\\h_{ij}&M_{ij}=0\end{cases},\qquad
\underline u_{kj}^{\mathrm{best}}=\begin{cases}h_{kj}&M_{kj}=1\\l_{kj}&M_{kj}=0\end{cases}.$$

若某个允许的α使该城最坏剩余上分仍不低于所有对手最好剩余下分，则同一个α见证它在**任何**这些格的精确完成下都仍可能第一。由于评分逐项单调，该极值检验覆盖整个完成区间；连续α比较由二次多项式根分段完成，不靠随机抽样。

[逐城证书](acquisition_limits.csv)给出：默认α=0.10至少17城不可排除；允许α∈[0.05,0.20]时至少24城不可排除，仅Istanbul不在这个必留集合中。24是连续偏好并集的数量下界，17是固定权重数量下界；没有声称这些下界可同时达到，也没有把极端完成当成真实观测。结论只适用于原区间内精确补数、其余区间和定义不变的条件。它为后续补数提供实际约束：教育和通学仍应补，但缩小冠军集合还需要其他指标证据。

## Phoenix新原件

[ASDB官方报告及审计](../../data/task4_v68_phoenix/README.md)提供Phoenix Day School for the Deaf的K–12学生193、教师29.25 FTE，并明确十个月员工从0.71改记为1 FTE的统计变化。尚无高中专属分母和教师分配，不能据此改善Phoenix教育分数；通学缺失区间继续保留。

## 当前评分与复现

八项主指标权重为 $(1-\alpha)/8$，两项辅助指标为 $\alpha/2$，默认α=0.10；通学效用为 $\exp(-t/30)$，$t$为通常单程分钟。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

连续推荐使用1e-9分数数值余量、1e-8严格遗憾差；多项式比较容差1e-12。它们是浮点数值证书，并非有向舍入区间算术证明。矩形效用界不是250格联合置信区域。

```sh
python3 research/2026-a/data/task4_v68_singapore/extract.py
python3 research/2026-a/data/task4_v68_phoenix/audit.py
python3 research/2026-a/scripts/task4_singapore_stage_revision.py
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/test_task4_current_model.py
```

本轮改进是用国际学段映射发现并修正输入口径，保留教师分配未知，再量化补数能否改变决策；没有新增模型名称或人为收紧区间。V64补数最小项数、V67联合扩张阈值属于V63历史分析，尚未在V68重新认证。论文文件未修改。
