# V8：连续偏好下的可能冠军与补数门槛

相同 V7 观测和缺失区间下，连续辅助权重范围 [0.05,0.20] 的可能冠军并集仍为 25 城。新增实测单元为 0，不能声称证据缩小了冠军集合。

本轮改善的是补数决策的可靠性：Istanbul 的通学效用排除门槛在辅助权重 0.10 时约为 0.352197；辅助权重升至 0.15 后，单独补通学数据无法保证排除。将通学效用假设为最差的 0，仍在 alpha ≥ 0.148173296 时存在夺冠的数据补全情景。该假设只用于诊断，不回写观测。后续补数需要同时考虑其他缺失指标，而不能把固定权重门槛当作稳健承诺。

## 当前公式

主指标集合 M 有 8 项，辅助集合 A 有 2 项：

w_j(alpha)=(1-alpha)/8 (j in M)，w_j(alpha)=alpha/2 (j in A)。

B_i(alpha)=sum_j w_j(alpha) u_ij^2，A_i(alpha)=sum_j w_j(alpha)(1-u_ij)^2。

S_i=100 sqrt(B_i)/(sqrt(A_i)+sqrt(B_i))；u_ij ∈ [l_ij,h_ij]。

固定权重的可能冠军满足 S_i(h_i) ≥ max_{k≠i} S_k(l_k)。连续偏好的可能冠军要求存在同一个 alpha ∈ [0.05,0.20]，对所有竞争城市 k 满足：

G_ik(alpha)=B_i(h_i,alpha) A_k(l_k,alpha)-B_k(l_k,alpha) A_i(h_i,alpha) ≥ 0。

A、B 对 alpha 为仿射函数，G 至多二次。程序按全部实根切分区间并检查区间内部及边界，避免采样网格遗漏狭窄可行情景。采用显式 1e-12 数值容差；这是浮点数值验证，不是符号精确证明。区间补全采用跨城市、指标独立的矩形集合；相关性约束尚未识别。偏好范围是敏感性假设，不是调查估计。

## 排名对比与验证

四个情景 alpha=0.05/0.10/0.15/0.20 中，最小最大遗憾决策排名的前两名均为 Singapore、Melbourne。前两个情景 Tokyo 第3、Copenhagen 第4；后两个情景互换。其余城市决策名次不变。连续冠军可行性已验证整个范围；这四个离散排名不能用来声称决策排名在整个连续范围恒定。

500 次分数差与多项式符号对照、平局和支配边界检查、40 组密网格交叉检查及可行见证检查通过。复现：`python3 research/2026-a/scripts/task4_v8_preferences.py`。原始结果见 summary.json、continuous_champions.json 与 rank_sensitivity.csv。

## Phoenix 后续证据入口

并行核查发现 [MAG 2026-02-25 区域委员会纪要](https://azmag.gov/LinkClick.aspx?fileticket=GYJPWYhmVAI%3D&mid=2494&portalid=0&tabid=413) 已讨论 2025 Household Travel Survey 结果；这更新了旧审计中的招募阶段信息，但没有提供可直接入模的 Phoenix 高中生时长交叉表。

[官方公开记录申请页](https://azmag.gov/About-Us/Public-Records-Requests) 是获取代码本、匿名 person/trip 表及权重说明的下一入口。需要城市居住地、高中在读、单程目的与时长、缺失编码、样本数和权重。页面要求联系方式与 CAPTCHA；本轮未提交申请。Phoenix 通学区间保持 [0,1]。
