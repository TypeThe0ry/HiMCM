# V40：新增高中学习结果原件，城市排名保持

本轮取得Toronto真实高中考试结果、Nairobi中学学生总量及Mumbai高等中学分类统计。城市评分新增准入单元为0：缺少考试人数、匹配教师或明确年级范围，不能把这些学校/地区资料直接当作全市可比指标。重新计算25城得分及决策序，与V38逐项一致：Singapore首选，Phoenix第24，可能冠军仍25城。

| 新证据 | 已解决的问题 | 尚缺的关键匹配 |
| --- | --- | --- |
| [Toronto学校级2024–25原件](../../data/task4_v40_toronto/README.md) | 155所四学区公立高中市内名录；数学108校、读写109校有实际成绩；缺失代码保留 | 各校应试分母与城市学生覆盖；各国测试达标标准也不等同 |
| [Nairobi KNBS2025原件](../../data/task4_v40_education/README.md) | 2024 Secondary学生129988，Junior另表、不混学段 | 同年同范围高中教师数；全国教师数不可替代 |
| [Mumbai两区2025年报](../../data/task4_v40_mumbai/README.md) | 表8.3真实学校、师生计数及原件；均参考2024–25 | 年级范围、混合学校教师分配、地理对齐；不是已核验的全市高中PTR |
| [Santiago官方整程说明](../../data/task4_v40_santiago/README.md) | 原调查时长为完整跨方式旅程，不是单个交通阶段 | 原问卷的当前高中身份语义、时期和地理限制仍未解决 |

Toronto已报告学校的等权成绩中位数为数学55.5%、读写84%，仅描述有报告的学校。没有用学校总在校生数充当年级应试人数，也没有把未报告学校填成零。TVO在线机构地址在Toronto，但单独列出，不混入155校。这批原件使后续教育质量研究有了可追溯的学校基础；尚未改善全市排名识别。

## 当前数学模型

主模型仍调用V38 `singapore_bounds()`，八主指标各0.1125、两辅助各0.05。师资效用为15/(15+PTR)，通学效用为exp(−t/30)，缺失项保留[0,1]；Singapore报告口径下的教师分配区间沿用V38。

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},\quad L_i=S(l_i),\quad U_i=S(h_i).$$

$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad \mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

推荐最小R的城市。本轮不改变指标、权重或数据界；[实际重算排名](ranks.csv)及[输入哈希和摘要](summary.json)提供对照。补数优先级仍参考[V39有限精度诊断](../task4_v39_finite_precision/README.md)，没有用新资料的存在代替其准入验证。

## 复核

运行 `python3 research/2026-a/scripts/task4_intake_v40.py` 核验原件哈希并重算排名。各数据目录的`extract.py`重建学校名录、学生数或原表总计。Mumbai表头和总计另经父agent及独立agent目视复核；Santiago只有官方网页读取证据，未将下载不完整的PDF冒充归档原件。论文未修改。
