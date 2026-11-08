# V76：把Phoenix补数诊断从几个测试点推进到连续阈值

当前V72输入下，只对Phoenix补数时，任何0—4项指标组合都不能在全部α∈[0.05,0.20]偏好下排除它的冠军可能，即使测得各自当前下端点的精确值。至少需要5项；最佳五项组合只在下端点附近的窄区间情景中有效。真实250格输入没有改变，排名仍Singapore第1、Tokyo第2、Phoenix第24，可能冠军仍25城。

本轮枚举Phoenix七个非点值指标的全部128个子集，并计算连续的剩余区间阈值，保留不能排除、并列和数值边界。它回答“什么样的补数结果才可能改变判断”，不预测真实测量值。

| 补数指标数 | 最佳情景的ρ临界值约为 | 一个最佳组合 |
| --- | ---: | --- |
| 0—4 | 不存在有效情景 | 即使ρ=0也不能排除 |
| 5 | 0.062202 | PM2.5、教育、高校资源、公共交通、通学 |
| 6 | 0.259080 | 上述五项＋固定宽带 |
| 7 | 0.385401 | 所有七项未知指标 |

五项有11个数值上无法区分的最佳组合，六项有2个，不应把展示的一个组合误称为唯一选择。未估算采集成本；“项”是模型指标，不是调查或文件数量。

## 情景与算法

对所选集合B，仅把Phoenix的区间设为

$$[l_{ij},\,l_{ij}+\rho(h_{ij}-l_{ij})],\quad j\in B,\qquad 0\le\rho\le1.$$

ρ同时限定不利结果的位置和剩余宽度，不能只解释成测量误差或采集精度。相同宽度若位于上端点附近，Phoenix仍可能第一。其余城市及未选指标保持原样。

定义

$$P_B(\rho)=\mathbf1\{\exists\alpha\in[0.05,0.20]:S_i(h_i^{B,\rho};\alpha)\ge\max_{k\ne i}S_k(l_k;\alpha)\}.$$

随着ρ增加，候选上界每个坐标都不下降，故P_B单调不减。先判断ρ=0与1，再二分40次；每个ρ内部仍按全部比较二次多项式的实根检查连续α，不用权重网格替代。输出每个组合的“仍可排除”下界与“已可能第一”上界，括区间宽度≤2⁻⁴⁰。数值容差1e−12，非形式化区间算术；临界并列保留为可能冠军，不把舍入后的阈值当严格边界。

## 相比旧方法实际改善了什么

[同一V72输入的旧粗网格重跑](same_input_coarse_grid.csv)只检查ρ=0、0.01、0.025、0.05、0.10、0.20、0.50、1：低ρ需要5项，ρ=0.10/0.20需要6项，ρ=0.50已无有效组合。它漏掉了“需要7项仍可排除”的中间范围。

连续阈值揭示约0.259080至0.385401之间存在七项方案；六项方案已不足。这是同输入下更细、完整的决策诊断，真实冠军集没有因此缩小。历史V39在旧输入下ρ=0需要4项，当前需5项；这另一个差异来自多年版本中的竞争城市输入修订，不能归因于本轮二分算法。

## 本轮来源核查

[Athens两份新官方原件](../../data/task4_v76_athens/README.md)支持两个历史学校代码跨名称/类型变化的连续性；同期原件和学生`year`定义仍未补齐，保留V75的48校匹配子集及主模型缺失界。候选853名学生没有被新增到已准入城市统计中。

Phoenix未取得新的同口径人数。[EDFacts 2024–25目录](https://www.ed.gov/data/edfacts-initiative/edfacts-resources/edfacts-file-specifications/edfacts-file-specifications-sy-2024-25)列出当前Staff FTE规格，但原件下载403。历史规则中的跨校FTE分摊示例不能证明当前Arizona记录执行情况；共享教师也不应自动等同于重复FTE。Hope缺失及现有条件继续保留。

## 当前模型公式

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}}{\sqrt{\sum_jw_j(\alpha)u_{ij}^2}+\sqrt{\sum_jw_j(\alpha)(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i,$$
$$\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

八项主指标各权重(1−α)/8，两项辅助指标各α/2，默认α=0.10。通学效用exp(−t/30)，教育岗位资源效用15T/(N+15T)。来源限制、缺失区间和`main_admitted=false`不变。

## 验证

4项测试覆盖可解析的ρ=0.5边界、并列/已被支配、非法输入、连续偏好单调性及不同分析/城市输出覆盖拒绝。独立agent从冻结CSV重建比较多项式并核验全部128组合，确认每个数值括区间和两侧±1e−7状态。输入数组未改变，统一模型核对250格与冻结排名；全部真实排名保持。

[逐组合阈值](bundle_thresholds.csv) · [最优诊断](frontier.csv) · [摘要](summary.json) · [真实排名](baseline/ranks.csv)。未修改论文。

```sh
python3 research/2026-a/scripts/task4_precision_frontier.py --output research/2026-a/results/task4_v76_precision_frontier
python3 -m unittest discover -s research/2026-a/scripts -p 'test_task4_precision_frontier.py'
```
