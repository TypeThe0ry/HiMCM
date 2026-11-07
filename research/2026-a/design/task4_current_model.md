# 当前模型：V48 实际高中年龄对齐（2026-11-07）

V51新增[证据撤回审计](../results/task4_v51_evidence_withdrawal/README.md)：固定α=0.10下撤回任意单个有信息单元仍推荐Singapore，6555对中12对切换为Tokyo，最小撤回数为2。允许α∈[0.05,0.20]时，撤回Singapore凶杀率在α=0.05即可切换，最小数为1。该假设检验不认定资料错误；实际数据及25城可能冠军均不变。

V50新增[连续推荐证书](../results/task4_v50_continuous_recommendation/README.md)：当前主模型在α∈[0.05,0.20]整个范围内唯一推荐Singapore，遗憾包络的保守分离余量4.0466285分，25城可能冠军不变。[Phoenix同年1180人学区上界](../results/task4_v50_phoenix_cap/README.md)在独立公校FTE目标下使Phoenix由第23至第20；保留学区包含关系条件，不替换当前主模型的第24或其教育定义。

V49新增[年份与行程目的审计](../results/task4_v49_evidence_audit/README.md)：Phoenix取得2023–24历史人数83，未用于填补2024–25；São Paulo的15条未知行程均有工作或私人事务停留，可恢复0条。重算全部名次与可能冠军不变，当前公式及V48入口继续适用。

当前条件入口为[saopaulo_age_bounds()](../scripts/task4_saopaulo_age_revision.py)：在V47上将São Paulo从全年龄高中生调整为实际14—18岁当前高中在读者。原始年龄筛选得到1690人，1489人有核验通学、201人未知；同一配对家庭重抽样得到通学包络[0.4417949654,0.6071350870]。São Paulo仍第7，Singapore第1、Tokyo第2、Phoenix第24，可能冠军25城；其余249格不变。镜像来源与探索性抽样条件保留，不称设计有效置信区间。详见[V48对照](../results/task4_v48_saopaulo_age/README.md)。

V47历史条件入口为[tokyo_coverage_bounds()](../scripts/task4_tokyo_coverage_revision.py)：在V46上纳入Tokyo六年制中等教育学校高中部3435名学生，学生总数306903；全校555名本务教师的高中部归属未知，保留H∈[0,555]。教育效用为15(19446+H)/(306903+15(19446+H))∈[0.4872927014,0.4943254278]。Tokyo仍第2、Singapore第1、Phoenix第24，可能冠军25城；其他249格不变。见[V47覆盖及范围对照](../results/task4_v47_tokyo_coverage/README.md)。通信制等其他课程未全部纳入，跨城范围条件保留。全城教育与通学完美补数证书在V47下仍为固定权重至少20城、连续偏好25城必然保留。

V46历史条件入口为[tokyo_bounds()](../scripts/task4_tokyo_official_revision.py)：Tokyo高中师资更新为2025年303468名学生/19446名本务教师；143所获认可大学总部与同日人口形成高教资源效用下界0.500804807，上界仍1。接受总部定位规则时，Tokyo第3→第2，Singapore仍第1，Phoenix第24，可能冠军25城。原有真实高中生通学和缺失区间保留，其他248格不变。[V46对照](../results/task4_v46_tokyo/README.md)分开报告年份、资源及撤回情景，继续保留跨城范围条件。变量代码research_he_density沿用历史名称，指标不限定研究型大学，也不测科研质量。

V45补数证书在V46输入下重算：全25城教育与通学精确补数后，固定α=0.10至少20城必然保留，连续α∈[0.05,0.20]仍保留25城。下面V45的共同权重余量及V44、V23数据均为相应历史版本结果。

V45新增[补数能力证书](../results/task4_v45_acquisition_limits/README.md)，在其V44基准上：即使所有25城的教育与通学单元都在现有区间内精确测定，允许辅助权重α∈[0.05,0.20]时仍不能排除任何城市。α=0.20提供共同见证，最小正余量为0.049194分。固定α=0.10时至少20城必然保留。继续补这两类数据有助于得分和名次，但缩小当前冠军集合还需要其他维度的证据或经验证的结构修订；不应为了减少候选而直接改权重。

V44历史条件入口为 [melbourne_bounds()](../scripts/task4_melbourne_observed_travel.py)：在V38上新增实际停靠记录核验，将7个未明确中学终点的通学效用恢复为[0,1]。同一线性jackknife规则下，Melbourne通学界由[0.278896,0.781095]改为[0.239800,0.792787]，仍第4；Singapore仍为最坏遗憾首选，Phoenix仍第24，可能冠军仍25城。其余249格保持V38。详见[V44同口径对照](../results/task4_v44_melbourne/README.md)。下列V23—V39数值与入口保留为历史对照。

V23十指标基准推荐 Singapore：最小最大遗憾为 28.173588 分，25 城仍全部是可能冠军。这里的推荐是在现有证据区间下选择最坏遗憾最小的城市，尚未识别唯一绩效冠军。V23 基准平均得分区间宽度为 37.916339 分；V26 直接重算五个通学尺度后首选保持，但最多 11 城的决策名次改变。

基准入口为 [task4_roster_coverage_comparison.py](../scripts/task4_roster_coverage_comparison.py) 的 `current_bounds(nyc_scope='under19', include_outcome=False, sampling=True)`。它接续已有证据，并更新 NYC、Mexico City 和 Melbourne 通学界。V26 是该基准的参数敏感性分析，不替换其数据范围或评分方法。V7 及其采集阈值属于历史结果。

## 指标、效用与权重

评价 25 个候选城市。八项主指标为凶杀率、PM2.5、生活成本指数、房价收入比、高中学生／教师人数比、经核验高等教育机构密度、学生通学、固定宽带速度；两项辅助指标为公共交通密度和公共泳池密度。[评分实现](../scripts/task4_v5_model.py) 的 `SPEC` 保存方向与固定锚点，`weights()` 定义：

$$w_j=\begin{cases}(1-\alpha)/8,&j\text{ 为主指标},\\\alpha/2,&j\text{ 为辅助指标},\end{cases}\qquad \alpha=0.1.$$

即主指标各 0.1125、辅助指标各 0.05。除通学外，非负原值 $x$ 按指标锚点 $a>0$ 转为成本效用 $u^-(x)=a/(a+x)$ 或收益效用 $u^+(x)=x/(a+x)$。通学直接使用 $u(t;\tau)=\exp(-t/\tau)$，$t$ 为学生通学分钟数，基准 $\tau=30$；它不再经过上述收益变换。

每个城市—指标保留效用界 $[l_{ij},h_{ij}]\subseteq[0,1]$。完全未知保留 $[0,1]$；部分设施名录仅支持收益下界。部分辖区事件数 $d$、完整地域人口 $P$ 给风险率下界 $x_L=10^5d/P$，对应成本效用界 $[0,a/(a+x_L)]$。数据准入、地域与分母条件随原始证据保留。

## 通学区间与人群范围

对学生权重 $p_r$ 和个体效用界 $[l_r,h_r]$，已知成员的加权识别界为

$$\underline T=\frac{\sum_r p_r l_r}{\sum_r p_r},\qquad
\overline T=\frac{\sum_r p_r h_r}{\sum_r p_r}.$$

已观察时长直接取指数效用；时间箱 $[a_r,b_r]$ 转为 $[e^{-b_r/\tau},e^{-a_r/\tau}]$；未知时长保留 $[0,1]$。Mexico 另对可选成员资格取极值：已知成员权重 $N$、分子界 $[A,B]$，可选成员权重 $v_r$、效用界 $[a_r,b_r]$，则

$$\underline T=\min_{z_r\in\{0,1\}}\frac{A+\sum_r z_rv_ra_r}{N+\sum_r z_rv_r},\qquad
\overline T=\max_{z_r\in\{0,1\}}\frac{B+\sum_r z_rv_rb_r}{N+\sum_r z_rv_r}.$$

默认 NYC 为 under19、2010—11 年历史日记；Mexico 为 2020 年未成年条件范围，当前高中阶段依赖已完成学段／年级进阶假设；Melbourne 为 Greater Melbourne、Secondary 在读且 15—19 岁，尚未单独识别高中年级。Melbourne 名册中170名有个人权重者含107名有旅程和63名无旅程者。V44进一步核验其中100个中学终点，另外7人的终点未明确，连同63名无旅程者保留[0,1]。使用第一条教育旅程与10组官方个人重复权重。端点抽样包络采用

$$SE(\theta)=\sqrt{\frac{9}{10}\sum_{r=1}^{10}(\theta_r-\theta)^2},\qquad
[\max(0,\underline T-t_{9,.975}SE(\underline T)),\min(1,\overline T+t_{9,.975}SE(\overline T))].$$

Sao Paulo在V48使用实际14—18岁当前高中在读，保留镜像来源及探索性抽样条件，Singapore 保留阶段混合条件。NYC 和 Sao Paulo 的家庭重抽样为探索性；Melbourne 为近似端点推断。城市年份、地域和学段不统一，未构造全城市联合置信区域；V23 与 V26 输出均标记 `main_admitted=false`。具体来源与审计见 [V23 报告](../results/task4_v23_roster_coverage/README.md) 和 [V26 报告](../results/task4_v26_direct_travel_scale/README.md)。

## 评分与决策

对效用向量 $u_i$，以固定理想点 1、负理想点 0 计算

$$D_i^+=\sqrt{\sum_jw_j(1-u_{ij})^2},\qquad
D_i^-=\sqrt{\sum_jw_ju_{ij}^2},\qquad
S_i=100\frac{D_i^-}{D_i^++D_i^-}.$$

评分对各收益方向效用单调；在矩形不确定性集合（允许端点同时实现）下，城市得分界为 $L_i=S(l_i)$、$U_i=S(h_i)$。可能冠军集合、最大遗憾和推荐为

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\qquad
R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad
\mathcal I^*=\arg\min_iR_i.$$

决策名次按 $R_i$ 从小到大排列，并列取最小名次；它不是已识别的真实绩效名次。[区间决策实现](../scripts/task4_interval_decision.py) 与 [V23 排名](../results/task4_v23_roster_coverage/ranks.csv) 可复核结果。

## 当前结果与敏感性边界

V23 默认十指标情景对应输出筛选 `model=v16_ten_criteria`、`nyc_age_scope=under19`、`scenario=both_sampling_envelope`。250 个效用单元中 111 个较完全未知区间有信息；Singapore、Melbourne、Phoenix 的决策名次分别为 1、4、24。完整 [效用界](../results/task4_v23_roster_coverage/utility_bounds.csv) 与 [摘要及输入哈希](../results/task4_v23_roster_coverage/summary.json) 记录基准。

[V26 脚本](../scripts/task4_direct_travel_scale.py) 在 $\tau\in\{15,20,30,45,60\}$ 分钟下，从现有学生时长和原始分箱直接重算五城通学界，保留成员资格、个人权重与原抽样方法；其余 20 城通学未知区间及所有非通学单元保持不变。30 分钟逐单元复现 V23，无新增观测。

| 通学尺度（分钟） | 首选 | Phoenix 决策名次 | 相对 30 分钟改变名次的城市数 | 可能冠军数 |
| --- | --- | ---: | ---: | ---: |
| 15 | Singapore | 24 | 9 | 25 |
| 20 | Singapore | 24 | 7 | 25 |
| 30 | Singapore | 24 | 0 | 25 |
| 45 | Singapore | 24 | 9 | 25 |
| 60 | Singapore | 24 | 11 | 25 |

表中固定 $\alpha=0.1$；连续 $\alpha\in[0.05,0.20]$ 的可能冠军可行性检验也保留全部 25 城。该结果不证明连续 $\tau$ 范围内首选始终不变。数据见 [V26 排名](../results/task4_v26_direct_travel_scale/ranks.csv)、[通学界](../results/task4_v26_direct_travel_scale/travel_bounds.csv) 与 [摘要](../results/task4_v26_direct_travel_scale/summary.json)。

`include_outcome=True` 是另列的十一指标情景：原十项权重乘以 $1-\beta$，毕业结局效用 $q$ 以权重 $\beta=0.1$ 加入同一距离公式。该情景最小最大遗憾为 32.898359，Melbourne 第 5；它不属于上述十指标基准或 V26 检验。

## V29：最新教育年份替换情景

[同口径年份更新](../results/task4_v29_education_year/README.md)将Jakarta的SMA师生比替换为2025/26学年的186461/11983，教育效用为0.4908302977。入口为[updated_bounds()](../scripts/task4_education_year_update.py)，其余249个单元及上述公式保持。Jakarta仍第17，Singapore仍为推荐，可能冠军25城。旧基准函数保留，两个年份不取交集；来源仍是明确标记的官方索引表转录，未增加城市指标覆盖，也未据此改动论文。

## V30：真实高中通学及抽样设计修订

最新条件入口为 [cape_bounds()](../scripts/task4_cape_town_revision.py)，在V29上只更新Cape Town通学一格。官方GHS2023实际包含159名14—18岁、当前10—12年级且非远程学生。保留时间分箱，并用完整217个PSU、14层计算比率端点的Taylor标准误，零目标学生的PSU也参与方差计算。端点采用Bonferroni调整后的近似联合95%包络：

$$[\max(0,\underline T-t_{203,.9875}SE(\underline T)),\min(1,\overline T+t_{203,.9875}SE(\overline T))] = [0.4067375294,0.7977951321].$$

方差公式与抽样范围见[数据说明](../data/task4_v30_cape_town/README.md)。权重、评分和决策公式不变，其余249格不变。Cape Town得分界由[33.019656,73.255944]变为[35.638820,72.191687]，最坏遗憾决策名次13→5；9城名次变化，Kendall tau=0.946667。Singapore仍为推荐，Phoenix仍第24，可能冠军仍25城。全年龄当前高中生189人的敏感性情景同样得到Cape Town第5。

这是2023年调查覆盖总体下、固定校准权重的近似推断，不覆盖学生宿舍等集体住户，也不是全城市联合置信保证；`main_admitted=false`保留。[完整前后对照](../results/task4_v30_cape_town/README.md)记录来源哈希和复现命令。证据改善了通学界与决策信息，尚未缩小可能冠军集合。

## V32：高中师资分母界与年份替换

最新条件入口为[school_bounds()](../scripts/task4_school_stage_revision.py)。Shanghai以2025学年235542名普通高中学生/23999名专任教师替换旧年份。Warsaw青年普通高中87999名学生的教师分配未知，但不超过全部普通高中6080 FTE（含1 FTE发布精度保护），因此教育效用界为[0,15/(15+87999/6080)]。青年与成人教师分配保留未知，FTE与人数口径差异明确保留。

两项修订只影响对应教育格。Warsaw得分上界74.317458→70.291549，排名仍13；Shanghai仍6。Singapore推荐、Cape Town第5、Phoenix第24和25个可能冠军不变。公式及权重保持上述定义，详见[V32对照](../results/task4_v32_school_stage/README.md)。

## V34：Delhi当前高中任课教师人数

当前条件入口为[delhi_bounds()](../scripts/task4_delhi_school_revision.py)。新增2024/25官方11–12年级学生603437/参与高中教学教师30186的精确人数比19.990624793，教育效用0.4286862578。教师含跨学段任教者，不是FTE。另以26766+3420c、c∈[0,1]作为分母检验兼教教师贡献假设，主模型仍使用实际任课人数。

Delhi得分界由[30.035171,67.970666]变为[32.868011,63.895479]，决策名次18→14；兼教贡献敏感性为第15。Singapore推荐、Phoenix第24及25个可能冠军保持。其余249格和上述评分公式不变。[完整对照](../results/task4_v34_delhi_school/README.md)保留范围、验证与原件链接。


## V38：Singapore预科学生覆盖与教师分配

[官方原件及提取器](../data/task4_v38_singapore/README.md)确认2024年预科学生25130人，其中748名专门独立学校学生未进入旧匹配子集。报告将该类学校404名教师列在中学栏，允许按任教学段或受训学段分类。保留原1979名报告预科教师口径，对新增学生对应的教师分配量设：

$$H\in[0,404],\qquad u_E(H)=\frac{15(1979+H)}{25130+15(1979+H)}\in[0.5415488461,0.5871868583].$$

这是报告教师人数条件下的分配区间，包含兼职，不是FTE或完整教师分类误差界。只替换Singapore教育格，通学数据、其他249格、权重和评分公式保持不变。旧匹配子集与扩展总体单列对照，不以两者相交缩窄区间。

Singapore得分界从[49.355873,66.310978]变为[49.292136,66.703329]，决策排名仍1；可能冠军仍25。撤回其教育证据、恢复[0,1]时，Singapore仍是首选，得分界[45.062720,69.668819]。本轮改善了学生覆盖和不确定性的表达，并未缩小冠军集合。详细对照见[V38结果](../results/task4_v38_singapore/README.md)。

[Toronto官方同年财务报表](../data/task4_v38_toronto/README.md)取得四学区高中学生与教师FTE，但法语学区跨市、人口及教师口径尚待统一，未准入城市单元。[Copenhagen当前高中生筛选变量](../data/task4_v38_travel/README.md)已核对，尚无城市通学估计，缺失界保持。


## V39：采集精度与所需指标数

主模型仍为V38，真实排名及可能冠军集合不变。[有限精度诊断](../results/task4_v39_finite_precision/README.md)将Phoenix所选指标的假想区间设为[l,l+ρ(h−l)]，对连续辅助权重[0.05,0.20]枚举最少采集集合。残余宽度0—2.5%的已检验情景需4项，5%、10%、20%需5项；50%时全部7个未知指标仍不足以排除其冠军可能。ρ同时限定结果位置与剩余宽度，不是采集成功概率、原始单位误差或置信水平。原有精确下端点方案属于ρ=0特例；所有情景不写回证据矩阵。
