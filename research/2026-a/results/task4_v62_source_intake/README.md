# V62：新增校级原件，保留未匹配区间

本轮取得12份官方原始文件，推进了三个缺失城市的学校编号、教师或学生计数匹配，尚未形成符合当前城市高中目标的新指标格。重跑全部250格及25城排名，与V61一致；可能冠军在固定α=0.10和连续α∈[0.05,0.20]下均为25城，连续推荐仍为Singapore，无未决区间。

| 城市 | 新取得的真实证据 | 尚缺什么 |
| --- | --- | --- |
| London | DfE2024/25院校教师原始CSV60,360行，按UKPRN匹配9家London院校667个Teacher主角色计数 | 高中阶段职责、跨校去重、同范围学生；总部位置不等于所有校区位置 |
| Copenhagen | DST2025校级高中在校人数；Rysensteen原始报告97名教师 | 97人对应2024Q2，1177名学生对应2025Oct；同日配对与城市完整范围未建立 |
| Cape Town | DBE2025名录，1093所开放城市学校；248所公立secondary全校学生275384、教师9254 | 当前10—12年级与师资分配；27所独立secondary中4校缺学生、3校缺教师 |
| Phoenix | 定位官方同届2024毕业工作簿及新技术手册地址 | 原件403，学校6287与学区6285差2仍未解释；不设重复人数预算 |

本轮改善的是数据可追溯性和下一步匹配基础，未实现排名或冠军集合收紧。新教师计数、同年标签、学校名称都不能单独证明同一高中总体。将这些资料直接变成师生比，会掩盖缺失分母、时间错配和阶段混合；当前算法保留这些未识别区间。本轮没有新增可准入的高中生通学时长。

## 当前模型与公式

仍使用[V61模型入口](../../scripts/task4_dhaka_role_revision.py)，以真实数据与明确边界构建效用上下界。教育资源效用为15T/(N+15T)，学生通学效用按原始旅时t（分钟）使用exp(−t/30)及各源未知记录边界。八个主指标权重各(1−α)/8、两个辅助指标各α/2。

$$S(u)=100\frac{\sqrt{\sum_jw_ju_j^2}}{\sqrt{\sum_jw_ju_j^2}+\sqrt{\sum_jw_j(1-u_j)^2}},\quad L_i=S(u_i^L),\quad U_i=S(u_i^U),$$
$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*=\arg\min_iR_i,\quad\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

推荐最小最大遗憾的城市，同时报告可能冠军集合。该集合来自当前条件区间，未证明一座城市必然最好。来源覆盖、时间及人员定义限制保留，main_admitted=false。

## 原件与复现

[London](../../data/task4_v62_london_colleges/README.md) · [Copenhagen](../../data/task4_v62_copenhagen_education/README.md) · [Cape Town](../../data/task4_v62_cape_school_roster/README.md) · [Phoenix](../../data/task4_v62_pxu_gap/README.md)。完整研究资料留在GitHub；论文未修改。

运行 `python3 research/2026-a/scripts/task4_v62_source_intake.py` 核验12份原件哈希、250格不变、排名数值一致及连续偏好证书。各数据目录的extract.py或audit.py重建源计数；连续证书使用数值容差，非形式区间算术。

[排名](ranks.csv) · [计算摘要](summary.json) · [推荐证书](recommendation_certificate.csv) · [复现脚本](../../scripts/task4_v62_source_intake.py)
