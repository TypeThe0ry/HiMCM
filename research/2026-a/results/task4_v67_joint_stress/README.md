# V67：相同扩张上限，误差落点改变推荐

**均匀放宽所有城市的区间，Singapore仍推荐；只放宽Singapore的区间，推荐可以变成Tokyo。** 本轮新增连续偏好与区间扩张的联合检验，补上“均匀压力测试稳定”不足以代表一般证据误差稳健性的缺口。实际数据没有改动，V63全部250格及原始排名保持，实际可能冠军仍25城。

## 已运行结果

ε是每个效用区间端点最多扩张的无量纲幅度，不是原始分钟或人数的百分比；两个情景使用相同每格上限，平均扩张量不同。α为两项辅助指标的总权重。

| 扩张结构 | ε范围 | α范围 | 数值证书／见证 |
| --- | --- | --- | --- |
| 所有25城同时扩张 | 连续[0,0.20] | 连续[0.05,0.20] | 12块全部通过；Singapore保持唯一最小最大遗憾推荐 |
| 仅Singapore十项扩张 | 连续[0,0.10] | 连续[0.05,0.20] | 5块全部通过；Singapore保持推荐 |
| 仅Singapore十项扩张 | 0.15 | 0.05 | Tokyo遗憾比Singapore低2.47804分，形成明确失效见证 |
| 仅Singapore十项扩张 | 0.20 | 连续[0.05,0.20] | 3个区间全部通过；Tokyo保持推荐 |

因此，在“仅Singapore对称扩张”这个指定情景族内，首次可能失去唯一推荐的ε位于 **(0.10,0.15]**，尚未求精确阈值。这个结论由整个前缀的证书和一个失败点共同支持，没有假设推荐差随ε单调。

默认α=0.10下，定向ε=0.15使Singapore与Tokyo交换前两名；ε=0.20改变4城决策名次。扩张情景中可能冠军仍25城。完整[情景排名](scenario_ranks.csv)分别标注结构、ε与α；[摘要](summary.json)将同α基线的名次变化和固定α=0.10基线的变化分开，避免把偏好变化归因于ε。

这些是假设信息集变宽后的决策响应，不是发现Singapore实测更差，也不证明该误差幅度在现实中可信。均匀扩张稳定不能替代非均匀来源偏差检验；下一步应核验推荐城市的关键证据，同时继续补Phoenix的缺失项。

## 数学定义与证书

保持原来的固定锚点效用、权重及评分：

$$w_j(\alpha)=\begin{cases}(1-\alpha)/8,&j\text{为主指标},\\\alpha/2,&j\text{为辅助指标},\end{cases}$$

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}}.$$

给定城市集合G（全部城市或仅Singapore），扩张定义为：

$$l_{ij}^{\varepsilon,G}=\max(0,l_{ij}-\varepsilon\mathbf1\{i\in G\}),\quad h_{ij}^{\varepsilon,G}=\min(1,h_{ij}+\varepsilon\mathbf1\{i\in G\}).$$

$$L_i^{\varepsilon,G}=S_i(l_i^{\varepsilon,G}),\quad U_i^{\varepsilon,G}=S_i(h_i^{\varepsilon,G}),\quad R_i^{\varepsilon,G}=\max\{0,\max_{k\ne i}U_k^{\varepsilon,G}-L_i^{\varepsilon,G}\}.$$

推荐取最小R。可能冠军仍按 \(U_i\ge\max_{k\ne i}L_k\) 判断。通学效用exp(−t/30)，高中师资效用15T/(N+15T)，未识别记录继续保留区间。

在矩形[ε₀,ε₁]×[α₀,α₁]内，下界得分随ε不增、上界得分随ε不减；固定ε时，平方距离均为α的仿射函数，其比值单调或恒定，因此每个得分的极值可由角点包络。将角点得分上下界传播到R，若所有竞争者R下界均高于指定城市R上界，则整个矩形通过；否则递归划分，达到深度仍不能证明的块保留未决。

[均匀12块证书](uniform_prefix_certificate.csv)最小保守遗憾差0.269664291；[定向前缀5块](targeted_prefix_certificate.csv)最小差0.001924210；[定向ε=0.20证书](targeted_epsilon02_certificate.csv)选择Tokyo。浮点padding为1e−9，严格间隔阈值1e−8；这是数值包络证书，不是带定向舍入的形式化证明。

## 新原件与复算

- [Phoenix官方交通规划及公开会议入口](../../data/task4_v67_phoenix/README.md)：取得县域2015学生距离原文，未取得Phoenix高中生时间分布；缺失区间保持。FY2005图书馆页面普通浏览器遇到安全验证，未取得原件。
- [Santiago CASEN2024问卷与手册](../../data/task4_v67_santiago/README.md)：核验当前高中学段、当前年级，但o28a问去主要工作地点的时间，不能当通学。未将不同调查人员统计匹配成同一个学生。
- Bogotá SIMUR已知官方入口本轮普通Chrome返回 `ERR_SOCKET_NOT_CONNECTED`，未取得数据包。此前[入口记录](../../data/task4_v66_bogota/README.md)保留，不重复请求或当作数据缺失证明。

新增可准入实际观测0。实际[基线排名](baseline/ranks.csv)、[250格](baseline/utility_bounds.csv)及[基线摘要](baseline/summary.json)由统一入口再次核对V63，`main_admitted=false`；情景输出单独存储，未覆盖实际输入。Overleaf论文未修改。

```sh
python3 research/2026-a/scripts/test_task4_joint_uncertainty_stress.py
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py
```

三个测试覆盖随机矩形内600个遗憾向量、边界截断、定向扩张不改其他行、精确并列不误判、明显支配情景和无效输入。独立agent另外核验全部证书叶块恰好覆盖目标域、角点间隔和失败见证，无遗漏或内部重叠。
