# 当前模型：V6（2026-11-07）

当前可复现入口为 `../scripts/task4_v6_model.py`，结果在 `../results/task4_v6/`。V6沿用10指标和固定权重：8项主指标各0.1125，公交、泳池各0.05。

## 评价公式

成本效用与收益效用：

$$u^-(x)=a/(a+x),\qquad u^+(x)=x/(a+x).$$

真实学生单程通学：

$$T=\mathbb E[e^{-t/30}],\quad t\text{以分钟计}.$$

由证据得到各效用区间[l,h]，未识别格为[0,1]。部分资源名录只给下界。

$$D_i^+=\sqrt{\sum_j w_j(1-u_{ij})^2},\quad D_i^-=\sqrt{\sum_jw_ju_{ij}^2},\quad S_i=100\frac{D_i^-}{D_i^++D_i^-}.$$

$$L_i=S(l_i),\quad U_i=S(h_i),\quad \mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\}.$$

$$R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad i^*=\arg\min_iR_i.$$

## V6新增公式

对存在图例对应不确定性及缺失时长的高中分箱调查：

$$\underline T=\min_{\pi\in\Pi}\frac{\sum_kn_{\pi(k)}e^{-b_k/30}}{N+M},\qquad \overline T=1.$$

其中Π枚举允许的分箱对应，b为往返时间上端；单程不超过往返。Mexico City条件下界为0.0182157874，M取同母体全部未报时长人数。

固定竞争者下界H_i=max_{k≠i}L_k，令v_i(A)在拟采集指标A中取现有下界，其他格取现有上界。城市本地最少可能排除采集量为：

$$m_i=\min\{|A|:S(v_i(A))<H_i\}.$$

这是采集门槛分析。v只用于假设结果枚举，不写回观测；实际能否排除由采集结果决定。

## 本轮验证结果

- 新增Istanbul、Jakarta普通高中师生比和Mexico City高中通学条件界。
- Phoenix64所完整公校FTE记录保存在诊断层，全市headcount及真实通学继续未知。
- 107/250格有信息；平均得分区间宽度39.23998068；可能冠军25城；稳健选择Singapore。
- Phoenix最少可能排除采集量4；Istanbul为2；Jakarta为3。
- 三个来源提取器通过hash/结构/加总核验；V6回归和采集枚举测试通过。
- 已检查输出图；独立代码复核提出的布尔准入与阈值语义问题已修复。

V6数据、程序与完整报告已归档于提交`621e7c4`（共享工作区并发提交）。本文件固定本轮模型入口和公式，供下一轮对照。后续优先推进Phoenix高中生通学、完整教师分母，以及Istanbul两项组合证据。
