# V88：解释学习成果模型的名次变化

上一轮把教师资源改为学习成果后，Dubai由第11到第2、London由第17到第6。本轮将这种变化拆成“撤去旧资源证据、替换共同城市的测量、加入新学习成果证据”，避免把资料和评价标准变化解释成城市实际改善。所有输入来自已核验V87结果，未人为改变缺失区间。

## 三项变化与实算结果

三项调整作用于互不重叠的城市集合：

- R：Warsaw、Istanbul、Mumbai、Delhi、Dhaka、Tokyo、Shanghai缺少对应学习成果，撤去原有资源信息，使教育列变为[0,1]。
- C：Singapore、Jakarta同时有两类证据，将资源效用换为数学达标率区间。
- L：Bogotá、London、Dubai原资源列未知，加入真实学习成果估计区间。

运行全部8个组合及6种执行顺序，对每一步的得分、最大遗憾和名次变化取平均，并保留顺序变化范围。混合资源与学习成果的中间状态只用于数值核算，不构成可推荐的城市评价模型。

| 城市 | 资源名次→学习名次 | R平均名次变化 | C平均名次变化 | L平均名次变化 |
| --- | ---: | ---: | ---: | ---: |
| Dubai | 11→2 | −1 | 0 | −8 |
| Bogotá | 10→4 | −1 | 0 | −5 |
| London | 17→6 | −1 | 0 | −10 |
| Jakarta | 18→20 | −1 | +3 | 0 |
| Tokyo | 2→5 | +2 | 0 | +1 |
| Shanghai | 6→15 | +7 | 0 | +2 |
| Phoenix | 24→24 | 0 | 0 | 0 |

负数表示名次上升。London的L贡献在不同顺序中为−11至−9，R为−2至0；平均值提供对执行顺序对称的核算，不隐藏非线性交互。新增学习成果证据的效果同时包含信息内容及不确定性变化，不能单独命名为纯覆盖效应。

本轮实际改善是让排名修订可解释：Shanghai退后9位中，平均7位来自其资源证据在新构念下撤回；这不表示Shanghai实际教育质量下降。主模型继续为V79，Singapore第1、Phoenix第24；8种诊断状态均保留25个可能冠军。

## 当前公式与解释性诊断

主模型保持资源效用 $u_E=15T/(N+15T)$、通学效用 $u_t=e^{-t/30}$，以及

$$S_i=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i).$$

最小R为稳健推荐，$U_i\ge\max_{k\ne i}L_k$表示可能冠军。8项主指标权重各为$(1-\alpha)/8$，2项辅助指标各为$\alpha/2$；默认α=0.1，连续范围[0.05,0.20]。学习成果替代检验仍使用V87的10项Bonferroni正态近似包络，保留PISA年龄、学校地域及抽样覆盖条件。

令 $f_i(A)$ 是执行调整集合A后的某个模型输出，$\Pi$为三项调整的六种排列，$P_\pi(k)$为排列中先于k的调整集合。本轮数值分解为

$$\phi_{ik}=\frac1{6}\sum_{\pi\in\Pi}\left[f_i(P_\pi(k)\cup\{k\})-f_i(P_\pi(k))\right],$$
$$\sum_{k\in\{R,C,L\}}\phi_{ik}=f_i(\{R,C,L\})-f_i(\varnothing).$$

这是有限三因素的Shapley核算。公式用于解释已发生的模型变化，不加入核心评分，也不表示因果效应。输出同时给出六种边际变化的最小与最大值。

## 数据补充与复现

[Chile官方SIMCE原件](../../data/task4_v88_pisa_regions/README.md)新增Santiago commune 13101的2024年高中二年级学习成果：64所学校，阅读考生6366人、数学6440人，官方commune均分分别256、264。保留1所非代表性标记学校；另1所学校等级百分比全为0却有考生，未把它当作真实零达标率。该commune不代表整个Santiago都市圈，SIMCE与PISA没有跨考试校准，故结果单独保留，不缩小主模型教育界。

同包核查其余20城的PISA公开地域字段：7城对应国家未出现在该2022发布文件，13城不能由已核查的REGION、STRATUM、SUBNATIO识别。省州、大区不能替代城市。

[Phoenix通学追查](../../data/task4_v88_phoenix_travel/README.md)未取得新的高中生旅时分布。官方学校计划列表不能替代学生调查结果，通学效用仍为[0,1]。

独立代理用直接公式重算8状态、200城次结果，最大差异1.42×10⁻¹⁴；300条归因记录复算一致，并逐项检验分解加总恒等式。主模型250格与V79基准逐一核对。所有论文和Overleaf文件保持原样。

```sh
python3 research/2026-a/scripts/task4_learning_coverage_attribution.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v88_intake
```

[各城名次分解](rank_attribution.csv) · [全部归因及顺序范围](attribution.csv) · [八种诊断状态](diagnostic_states.csv) · [核验摘要](summary.json) · [主模型重跑](../task4_v88_intake/summary.json)。
