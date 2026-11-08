# 当前模型统一复算入口（V96）

当前注册模型为 **V96**，最新审查为V100。Warsaw采用六类青年高中路径的同年度学生与教师资料，教师分配不明部分保留区间；Phoenix使用市内已观测PM2.5监测范围。默认决策排名Singapore第1、Warsaw第8、Phoenix第16，固定与连续偏好下可能冠军均为25城。

V100完成[新加坡官方记录替代情景](../task4_v100_singapore_source/README.md)，所有名次及可能冠军集合保持；分类对应尚未核实，未替换当前安全指标。

V99新增[单格撤回诊断](../task4_v99_cell_stress/README.md)与[Tokyo配对年份检验](../task4_v99_tokyo_year/README.md)，真实250格及排名保持。

本目录由注册表重算，核验250个效用区间及5城通学来源。最新[压力检验](../task4_v98_joint_stress/README.md)已使用V96输入；[共同补数能力分析](../task4_v97_joint_acquisition/README.md)同样基于V96。V91补数与精度阈值分析仍是历史结果，版本由注册表分别记录。

在仓库根目录运行：

```sh
python3 research/2026-a/scripts/task4_current_model.py
python3 research/2026-a/scripts/test_task4_current_model.py
```

[注册表](../../design/task4_current_model.json)明确当前数据函数、历史对照情景、权重范围和补数分析入口。[脚本](../../scripts/task4_current_model.py)先逐格核对250个区间，再核对排名、分数、遗憾与冠军标记，随后生成本目录的[排名](ranks.csv)、[效用区间](utility_bounds.csv)、[连续推荐证书](recommendation_certificate.csv)和[摘要](summary.json)。摘要记录注册表和基线哈希。可用 `--output` 指定独立结果目录；本目录随注册表更新，历史基线保留原位。

V65的工程改进是防止误用历史模型入口。测试包含“交换两个等权指标，分数不变但数据含义错误”的反例：仅检查排名会漏过，逐格身份与数值核查会拒绝。这个改进提高复算可核查性，没有带来新的实测精度或冠军集合缩小。

## 数据与版本入口

[Warsaw师资修订](../task4_v96_warsaw_revision/README.md) · [Phoenix监测修订](../task4_v91_phoenix_monitor/README.md) · [当前通学证据索引](travel_evidence.csv)。Cape Town使用GHS2025的182名14—18岁、当前10—12年级学生；旧验证码请求已不适用。

历史V65来源核查保留在各数据目录及Git历史中。研究更新不自动改写Overleaf论文。

## 当前公式

令城市i的十项效用满足 uᵢⱼ∈[lᵢⱼ,hᵢⱼ]。八项主指标权重为(1−α)/8，两项辅助指标为α/2，默认α=0.10。通学效用为 exp(−t/30)，t为单程分钟；高中师资效用为15T/(N+15T)，T、N为同范围教师和学生数。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_j w_j(\alpha)u_{ij}^2}}{\sqrt{\sum_j w_j(\alpha)u_{ij}^2}+\sqrt{\sum_j w_j(\alpha)(1-u_{ij})^2}}.$$

$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max\{0,\max_{k\ne i}U_k-L_i\},\quad i^*\in\arg\min_i R_i.$$

$$\mathcal C(\alpha)=\{i:U_i(\alpha)\ge\max_{k\ne i}L_k(\alpha)\}.$$

区间采用矩形外包；不同来源的年份、人群和城市覆盖条件仍需满足，`main_admitted=false`。因此可能冠军为外包下尚不能排除的城市，并非各城获胜概率。补数规划的连续权重公式与条件见[V64报告](../task4_v64_continuous_acquisition/README.md)。
