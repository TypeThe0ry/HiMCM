# V69：补入Tokyo特教高中部，保留专攻科和教师分配未知

[新官方学校统计、学校明细和UIS映射](../../data/task4_v69_tokyo/README.md)补上原Tokyo教育输入遗漏的特教高中部。公立高等部5854人包含46名专攻科学生；专攻科在UIS映射中属于更高学段，因此明确的高中本科学生为5808人。所有制总数与公立数的差额209人尚无本科／专攻科分拆，保留新增学生界[5808,6017]。

学校明细与地址对应显示，原CSV星号所涉三所都外区立学校的高中部均为0，故不把该区全部高中学生误删。原普通高中和六年制中等教育学校是不同法定学校类别，特教学校另列；本轮不按人数比例猜教师分配。

## 新旧结果

| 项目 | V68 | V69 |
| --- | ---: | ---: |
| Tokyo覆盖学生数 | 306903 | [312711,312920] |
| Tokyo条件本务教师人数 | [19446,20001] | [19446,27019] |
| Tokyo教育效用 | [0.487293,0.494325] | [0.482443,0.564467] |
| Tokyo总分界 | [40.357789,70.060216] | [40.313586,70.899255] |
| Tokyo最大遗憾 | 37.171671 | 37.215874 |
| Tokyo决策名次 | 2 | 2 |
| Singapore / Cape Town / Phoenix名次 | 1 / 5 / 24 | 1 / 5 / 24 |
| 固定及连续偏好可能冠军数 | 25 / 25 | 25 / 25 |

其他249格逐项保持，全部名次不变，Kendall τ=1；连续α∈[0.05,0.20]仍推荐Singapore，未决区间0。完全撤回Tokyo教育证据[0,1]的情景使其退至第3，说明该条件证据仍有决策作用，但并未识别唯一冠军。

新增特教全学段本务教师池7018人，分配至高中本科的数量未知。沿用旧六年制学校教师分配H∈[0,555]，新增K∈[0,7018]：

$$N\in[306903+5808,306903+6017],\qquad T=19446+H+K\in[19446,27019],$$
$$u_E=\frac{15T}{N+15T}\in\left[\frac{15\times19446}{312920+15\times19446},\frac{15\times27019}{312711+15\times27019}\right].$$

这是按本务学校归属的报告人数资源界，沿用官方教员定义，含校长、副校长、教头、养护及营养教员；休职者及其代替者也可能同时计入。它不是课堂授课人数、FTE或学习质量；极值只构成保守外包，不声称所有教师同时教高中本科。通信制、高专低年级、专修学校高等课程等仍未完整纳入，未实施14—18岁筛选。新旧人口范围不同，不将区间取交集来制造精度。`main_admitted=false`。

[排名](ranks.csv) · [效用界](utility_bounds.csv) · [摘要](summary.json) · [连续推荐证书](recommendation_certificate.csv)。

## Phoenix与算法复核

[Valley Metro 2023 OD官方原件](../../data/task4_v69_phoenix/README.md)提供新的公交乘客调查资料，但只有K–12学生类别、粗年龄段和出发时钟；不能从反向行程出发时刻推算家到校时长。未准入Phoenix高中生通学观测，缺失界保持。

[本轮联合压力测试](../task4_v69_joint_stress/README.md)使用V69重新计算；V67历史原件保留。脚本现在按输入版本选择输出目录，并在写入前校验已有结果的模型、数据及权重，防止用新输入覆盖旧实验。压力测试仍是指定效用扩张情景，不是实测误差。

## 当前公式

八项主指标权重为(1−α)/8，两项辅助指标为α/2；默认α=0.10，检验[0.05,0.20]。通学效用为exp(−t/30)，t为单程分钟。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

逐格区间采用矩形外包，不构成全城市联合置信区域；连续推荐为有数值余量的浮点证书。

```sh
python3 research/2026-a/data/task4_v69_tokyo/extract.py
python3 research/2026-a/scripts/task4_tokyo_special_revision.py
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py --output research/2026-a/results/task4_v69_joint_stress
```

本轮把遗漏的真实高中群体纳入条件比较，排除已识别的更高学段，并让剩余未知显式进入结果。没有改动论文。
