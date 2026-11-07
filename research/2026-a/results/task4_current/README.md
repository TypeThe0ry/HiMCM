# 当前模型统一复算入口（截至V66核查）

最新一轮为[V66来源核查](../task4_v66_intake/README.md)，新增合格模型观测0，当前数据仍为V63。

当前数据模型仍为 **V63**；V64提供连续偏好补数规划，V65新增三城来源核查和统一运行入口。重算确认250个效用区间、全部排名与V63一致，可能冠军仍为25城。Singapore在辅助权重 α∈[0.05,0.20] 内保持最小最大遗憾推荐；这不表示它已被证明是唯一最佳城市。

在仓库根目录运行：

```sh
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/test_task4_current_model.py
```

[注册表](../../design/task4_current_model.json)明确当前数据函数、历史对照情景、权重范围和补数分析入口。[脚本](../../scripts/task4_current_model.py)先逐格核对250个区间，再核对排名、分数、遗憾与冠军标记，随后生成本目录的[排名](ranks.csv)、[效用区间](utility_bounds.csv)、[连续推荐证书](recommendation_certificate.csv)和[摘要](summary.json)。摘要记录注册表和基线哈希。可用 `--output` 指定独立结果目录；本目录随注册表更新，历史基线保留原位。

本轮工程改进是防止误用历史模型入口。测试包含“交换两个等权指标，分数不变但数据含义错误”的反例：仅检查排名会漏过，逐格身份与数值核查会拒绝。这个改进提高复算可核查性，没有带来新的实测精度或冠军集合缩小。

## 新来源核查

| 城市 | 取得或定位的资料 | 对模型的影响 |
| --- | --- | --- |
| Phoenix | [MAG公开TRP服务字段审计](../../data/task4_v65_phoenix_public_trp/README.md)：2022员工通勤均值，没有学生年龄或年级字段 | 新准入高中生观测0，保持缺失区间 |
| London | [LTDS工作簿及三份官方原件](../../data/task4_v65_london_ltds/README.md)：30表，没有目标年龄、当前高中学段与到校时间联合表 | 保持区间；微观数据仍待取得与核验 |
| Bogotá | [EODH2023官方问卷和数据入口](../../data/task4_v65_bogota_eodh/README.md)：下载受阻，未取得原问卷 | 当前年级定义仍待核验，保持区间 |

Cape Town已采用[2025年原始微观数据](../../data/task4_v63_cape_travel/README.md)，182名14—18岁当前10—12年级学生。早先GHS2023网页验证请求不影响此轮复算。Cape Town仍第5，Phoenix仍第24。所有本队论文材料继续在Overleaf维护，本轮没有修改论文。

## 当前公式

令城市i的十项效用满足 uᵢⱼ∈[lᵢⱼ,hᵢⱼ]。八项主指标权重为(1−α)/8，两项辅助指标为α/2，默认α=0.10。通学效用为 exp(−t/30)，t为单程分钟；高中师资效用为15T/(N+15T)，T、N为同范围教师和学生数。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_j w_j(\alpha)u_{ij}^2}}{\sqrt{\sum_j w_j(\alpha)u_{ij}^2}+\sqrt{\sum_j w_j(\alpha)(1-u_{ij})^2}}.$$

$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_i R_i.$$

$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

区间采用矩形外包；不同来源的年份、人群和城市覆盖条件仍需满足，`main_admitted=false`。因此可能冠军为外包下尚不能排除的城市，并非各城获胜概率。补数规划的连续权重公式与条件见[V64报告](../task4_v64_continuous_acquisition/README.md)。
