# V82：把推荐失效边界从粗括区间细化到0.001

当前V79数据下，仅扩张Singapore效用区间时，推荐首次失去保证的边界被括在 **(0.042, 0.043]**。此前V72检查只给出(0.025,0.05]。本轮括区间宽度由0.025减少为0.001，减少96%；这是稳健性诊断分辨率提升，没有缩小任何真实缺失区间，也不表示模型本身更抗误差。

| 检验 | 当前结果 |
| --- | --- |
| 真实数据排名 | 全部保持；Singapore第1、Tokyo第2、Cape Town第5、Phoenix第24 |
| 真实可能冠军 | 固定权重25城，连续偏好25城 |
| 全城同时扩张，ε≤0.20 | 48个认证矩形，均保持Singapore，未决0 |
| 只扩张Singapore，ε≤0.042 | 27个认证矩形，均保持Singapore，未决0 |
| ε=0.043、α=0.05 | Tokyo最大遗憾比Singapore低0.0222664，前两名交换 |
| 只扩张Singapore至ε=0.20 | 整个α范围推荐Tokyo |

在更细探索ε=0.0425时，最大深度14的证书有2个未决矩形；没有把它们判作通过或判作反例。因此发布下界取已完全认证的0.042。连续α范围为[0.05,0.20]；上界来自具体反例，不依赖遗憾差对ε单调的假设。既有V72的粗情景在V79输入重跑后相同，精度提升来自本轮细分与新增反例，而非Mumbai或Delhi实测修订改变了这个边界。

## 数据推进

[Phoenix新证据](../../data/task4_v82_phoenix/README.md)提供同年度学区学生与课堂教师FTE的对账结果，用于区分教师人数、FTE与含空缺岗位的预算口径。学区覆盖不能代替全城市覆盖，主模型仍保留Phoenix教育缺失区间。[Barcelona校级配置表](../../data/task4_v82_barcelona/README.md)明确教师跨学段未拆分，并有日期及合计差异；原件直连超时，仅归档阅读器转录。通学分支未取得新原始记录，本轮没有准入新的城市指标。

## 模型与本轮算法

通学效用 $u_t=\exp(-t/30)$；教学资源效用 $u_E=15T/(N+15T)$。八个主要指标各取 $w_j=(1-\alpha)/8$，两个辅助指标各取 $w_j=\alpha/2$。

$$S_i(u;\alpha)=100\frac{\sqrt{\sum_jw_ju_{ij}^2}}{\sqrt{\sum_jw_ju_{ij}^2}+\sqrt{\sum_jw_j(1-u_{ij})^2}},$$
$$L_i=S_i(l_i),\quad U_i=S_i(h_i),\quad R_i=\max(0,\max_{k\ne i}U_k-L_i),\quad i^*\in\arg\min_iR_i.$$

可能冠军为 $\mathcal C(\alpha)=\{i:U_i\ge\max_{k\ne i}L_k\}$。压力情景将指定行变为 $l^\epsilon=\max(0,l-\epsilon)$、$h^\epsilon=\min(1,h+\epsilon)$。算法在ε与α矩形上包络各城遗憾值，只有推荐城遗憾上界严格小于所有对手下界才认证；其他矩形继续细分，达到深度上限仍未知就保留未决。采用1e−9浮点保护与1e−8严格差距阈值，是数值认证而非形式化区间算术。全城同幅扩张不能代表任意来源偏差。

## 复现和核验

```sh
python3 research/2026-a/scripts/task4_joint_uncertainty_stress.py --output research/2026-a/results/task4_v82_joint_stress --targeted-prefix-max .042 --extra-epsilon .043
python3 -m unittest discover -s research/2026-a/scripts -p 'test_task4_joint_uncertainty_stress.py'
```

新增可重复的 `--extra-epsilon` 参数只增加明确列出的离散反例检查点，连续前缀仍由矩形证书验证。6项测试通过；独立longdouble计算核对1350行情景，最大遗憾差异小于3e−14，两个前缀矩形完整覆盖且内部不重叠。另一代理以独立公式复核全部矩形包络差距，差异小于2e−12，确认反例及括区间解释。

[摘要](summary.json) · [全部情景](scenario_ranks.csv) · [连续前缀证书](targeted_prefix_certificate.csv) · [独立核验](independent_check.json) · [真实基线](baseline/ranks.csv)

没有改动Overleaf论文。实测模型仍为V79，本轮更新其来源证据及稳健性诊断。
