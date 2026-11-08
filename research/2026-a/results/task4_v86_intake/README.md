# V86：直接识别高中年级的学习成果

本轮把 Bogotá 教育成果从混合年级推进到真实10—11年级微观数据；Phoenix 学区教师核查和 Barcelona 通学测量诊断分别保留缺失与覆盖限制。新增可准入主模型的城市指标格为0，未人为缩短区间。

## 真实数据与修订对照

[OECD原件与可复算子集](../../data/task4_v86_bogota/README.md)含 Bogotá 1986名学生、56所学校；当前10—11年级1399人、55所学校，加权占67.69%。实际年龄15.33—16.33岁，不能推广为全部14—18岁高中生。

| 科目 | 混合年级均值 | 高中年级均值（标准误） | 配对差值95%近似区间 |
| --- | ---: | ---: | ---: |
| 数学 | 422.67 | 439.12（4.77） | 11.24—21.65 |
| 阅读 | 462.15 | 482.07（5.44） | 13.38—26.45 |
| 科学 | 459.16 | 477.60（5.00） | 12.28—24.60 |

这项改善是目标人群识别准确度的提升。差值反映年级构成及升留级选择，不能解释为教学质量因果提升。学习成果也不能直接替换师生资源比；其他城市尚缺匹配的年龄、年级与测量尺度。

[Phoenix同年学区原件](../../data/task4_v86_phoenix_lea/README.md)匹配104条缺失学校教师记录涉及的76个学区。其中73个学区教师总量仍缺失；另外3个学区的已知学校教师合计恰等于学区总量。零余额不证明缺失学校实际教师为零，因此没有据此伪造教师上界。

[Barcelona公开GPS汇总](../../data/task4_v86_travel/README.md)覆盖市内8所学校48条保留步行轨迹，学校人数加权平均记录时长由隐私截短前约8.54分钟变为截短后7.85分钟，减少约41.79秒。该差异说明测量处理会改变通学结果；样本为14—16岁ESO学生、步行志愿者，未当作全市高中全方式估计。没有入库个人GPS轨迹。

## 排名与可能冠军

重跑核对全部250格与V79基准一致；全部决策排名不变：Singapore第1、Tokyo第2、Cape Town第5、Phoenix第24。默认权重及连续权重范围内均仍有25个可能冠军；连续推荐为Singapore，未决区间0。真实高中学习成果已经取得，但本轮证据不足以缩小冠军范围。保留5城真实通学信息及其原有区间。

## 当前数学公式

教育资源效用为 $u_E=15T/(N+15T)$，通学效用为 $u_t=\exp(-t/30)$。各城市效用范围为 $u_{ij}\in[l_{ij},h_{ij}]$：

$$S_i=100\frac{\sqrt{\sum_j w_j u_{ij}^2}}{\sqrt{\sum_j w_j u_{ij}^2}+\sqrt{\sum_j w_j(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i).$$

按最小 $R_i$ 推荐；可能冠军条件为 $U_i\ge\max_{k\ne i}L_k$。8项主指标各权重 $(1-\alpha)/8$，2项辅助指标各 $\alpha/2$；默认 $\alpha=0.1$，连续检验 $[0.05,0.20]$。

本轮学习成果估计对每科10个合理值分别计算加权均值 $\theta_m$ 和80个复制权重均值 $\theta_{mr}$：

$$\bar\theta=\frac1{10}\sum_{m=1}^{10}\theta_m,\quad
\widehat V=\frac1{10}\sum_{m=1}^{10}\frac4{80}\sum_{r=1}^{80}(\theta_{mr}-\theta_m)^2+
\frac{1.1}{9}\sum_{m=1}^{10}(\theta_m-\bar\theta)^2.$$

高中组减总体的差值先在每个合理值和复制权重内配对相减，再使用同一方差公式，保留重叠样本协方差。区间为各项 $\bar\theta\pm1.96\sqrt{\widehat V}$，并非联合置信区间。

## 验证与复现

官方ZIP完整下载并记录哈希及SAV校验；仓库只保存约319KB的城市派生子集，大原件留在临时目录。计算前校验子集与V85公布基准哈希。全年级三科均值及标准误复现OECD结果至约 $2\times10^{-13}$；独立代理逐项循环复算9组均值与标准误，误差小于 $10^{-10}$。

```sh
python3 research/2026-a/data/task4_v86_bogota/analyse.py
python3 research/2026-a/data/task4_v86_phoenix_lea/extract.py
python3 research/2026-a/data/task4_v86_travel/summarize.py
python3 research/2026-a/scripts/task4_current_model.py --output research/2026-a/results/task4_v86_intake
```

[排名](ranks.csv) · [250格区间](utility_bounds.csv) · [运行摘要](summary.json)。论文及Overleaf未修改。
