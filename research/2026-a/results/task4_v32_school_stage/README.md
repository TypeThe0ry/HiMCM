# 高中教育证据更新：Warsaw区间缩窄4.03分，排名未变

本轮新增Warsaw青年普通高中师资配置单侧界，并将Shanghai普通高中数据替换为2025学年同口径原表。保留Cape Town真实高中通学及所有其他原有数据。四个情景分别运行V30基准、仅上海、仅Warsaw、两者合并，分离两项证据的影响。

| 城市 | 修订前得分界 | 修订后得分界 | 决策名次前→后 |
| --- | --- | --- | --- |
| Shanghai | [35.395422,66.862893] | [35.412670,66.877647] | 6→6 |
| Warsaw | [33.406445,74.317458] | [33.406445,70.291549] | 13→13 |

25城排名均未变，Kendall tau=1；Singapore仍为最小最大遗憾推荐，Cape Town第5，Phoenix第24。固定权重及连续辅助权重[0.05,0.20]下可能冠军均25城。排名不变并不表示信息没有增加：Warsaw得分区间缩窄4.025909分，但其下界不变，竞争者最高上界不变，最坏遗憾因而不变。

## 分母不完整时保留什么信息

Warsaw2023/24青年普通高中学生87999人，全部普通高中教师6079 FTE包含成人学校。没有把两者直接相除写成青年高中点值；按教师集合包含关系，并为整FTE发布精度保留1 FTE，得到

$$0<T_y\le6080,\quad PTR_y\ge87999/6080,\quad u_y\in[0,15/(15+87999/6080)]=[0,0.5089314114].$$

这种单侧识别在青年教师分配未知时仍利用真实信息。新增界来自官方计数及明确集合关系，没有依据排名结果调窄区间。Warsaw是青年普通高中含特殊教育，未限定实际14—18岁；FTE与其他城市教师人数存在口径差异，仍属于条件比较。仅上海情景也展示撤回Warsaw条件后结果。

Shanghai2025高中学生235542、专任教师23999，PTR9.8146589441；只替换年份，不与2024取交集。两份完整官方PDF及16区加总检查改善了原教师数依赖索引转录的追溯性。

## 当前模型与复核

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S(l_i),\ U_i=S(h_i).$$

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*=\arg\min_iR_i.$$

八主指标各0.1125，两辅助各0.05；通学效用exp(-t/30)。程序检查除两城教育格外其余248格完全不变、效用界合法、计数与效用计算一致，记录输入哈希。两项原表均由独立agent查看表头与页脚。未解决的跨城地域、年份、教师定义差异继续标记main_admitted=false。

[上海原始数据](../../data/task4_v32_shanghai/README.md) · [Warsaw原始数据及推导](../../data/task4_v32_education/README.md) · [排名](ranks.csv) · [效用界](utility_bounds.csv) · [摘要](summary.json)。

入口为[school_bounds()](../../scripts/task4_school_stage_revision.py)。复现：`python3 research/2026-a/scripts/task4_school_stage_revision.py`。本轮研究更新未改动论文。

另定位[Bogotá EM2021真实当前年级与通学字段](../../data/task4_v32_travel/README.md)，尚未取得微数据，不纳入排名。
