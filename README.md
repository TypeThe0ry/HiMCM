# 2026 HiMCM A

> **团队成员与 AI agent 必读：开始写作或制图前，必须阅读并遵循[统一 Guidelines](GUIDELINES.md)。论文文字、图表、图注与研究结论均按专项规范执行，交付前核验。AI agents: read and follow these guidelines before editing.**

**The City Showdown: Modeling the Best City to Live In**

本仓库保存全球城市评价研究的数据、模型、结果、图表和历史论文。当前包含25城真实数据研究、十指标证据区间模型、毕业结果条件分析及通学微观数据修订；尚未形成完整同年城市普查矩阵或最终参赛结论。

**研究与论文分开维护。** GitHub `TypeThe0ry/HiMCM` 保存研究代码、原始数据、模型结果、图表与历史论文库；所有本队论文草稿、LaTeX、参考文献和论文模板移至相邻的 `HiMCM-Overleaf` 工作区。原始资料及本地忽略的大型生成包保留在研究仓库。

**[Overleaf 项目](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894)是论文的权威工作区。** `main.tex`、`ref.bib`、`mcmthesis.cls`位于该工作区根目录，任务4正文主线位于`drafts/task4_paper_core.md`。两边分别同步各自远端；GitHub研究仓库不再作为整棵Overleaf镜像。旧GitHub论文版本保存在Overleaf的`archive/github_before_split/`中，迁移路径见[拆分记录](docs/migration/overleaf_split_2026-11-07.json)。

## 从这里开始

| 想了解什么 | 入口 |
| --- | --- |
| V104测量精度 | [四城理想结论的精度边界；宽0.01时最少5城](research/2026-a/results/task4_v104_intake/README.md) |
| V103算法与证据 | [共享补数最优集合4城的证明；实际仍25城](research/2026-a/results/task4_v103_intake/README.md) |
| V102实际补数修订 | [Copenhagen下界提高2.319分；排名和25城候选保持](research/2026-a/results/task4_v102_intake/README.md) |
| A题原文、评委点评 | [题目](research/2026-a/inputs/problem_a_2026.pdf) · [2025点评](research/2026-a/inputs/judges_commentary_2025.pdf) |
| 数据位置 | [数据导航](#数据在哪里) · [25城候选名单](research/2026-a/data/city_candidates_team_25.csv) |
| 任务4精简正文主线 | [Overleaf：drafts/task4_paper_core.md](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894) |
| 通学尺度直接重算 | [原始时长与分箱：五个尺度下的排名](research/2026-a/results/task4_v26_direct_travel_scale/README.md) · [上一轮保守检验](research/2026-a/results/task4_v25_travel_scale/README.md) |
| V80当前补数能力复核 | [教育＋通学补齐后仍至少22城可能第一；Phoenix阈值已重证](research/2026-a/results/task4_v80_acquisition_limits/README.md) |
| V79同源教师分配修订 | [Delhi校级核验，统一兼教分配规则后由第13变第14](research/2026-a/results/task4_v79_delhi_allocation/README.md) |
| V78校级教育修订 | [Mumbai真实人数形成资源分配区间，总分区间缩窄17.6%](research/2026-a/results/task4_v78_mumbai_school/README.md) |
| V77高中人数对账 | [Mumbai逐年级统计核验与排名复算](research/2026-a/results/task4_v77_sources/README.md) |
| V76补数连续阈值 | [Phoenix128组合诊断，识别粗网格遗漏的七项可行情景](research/2026-a/results/task4_v76_precision_frontier/README.md) |
| V75完整原件与学校匹配 | [Athens两份原件校验通过、48校学生子集与Phoenix项目核查](research/2026-a/results/task4_v75_sources/README.md) |
| V74学校级来源核查 | [Phoenix目录差异与Toronto分校师资资料；保留缺失并复算](research/2026-a/results/task4_v74_sources/README.md) |
| V73补数能力下界 | [当前模型下补齐教育与通学仍至少21城可能第一（连续偏好）](research/2026-a/results/task4_v73_acquisition_limits/README.md) |
| V72年龄修订与稳定性 | [墨西哥城14—18岁真实记录重提取、排名与当前压力对照](research/2026-a/results/task4_v72_mexico_age/README.md) |
| V71补数核查与来源校验 | [四地新官方资料；五城当前通学界逐源校验并接入统一运行](research/2026-a/results/task4_v71_intake/README.md) |
| V70高中子群与岗位口径 | [撤回整组通学均值代理；以官方交叉计数限定教师分配未知](research/2026-a/results/task4_v70_population_roles/README.md) |
| V69特教高中覆盖与复核 | [Tokyo新增真实本科计数界；重算压力阈值并保护历史实验](research/2026-a/results/task4_v69_tokyo/README.md) |
| V68高中学段修订 | [纠正Singapore预科学段代理，扩大真实未知范围；排名与25城候选保持](research/2026-a/results/task4_v68_singapore_stage/README.md) |
| V67联合不确定性检验 | [均匀扩张仍推荐Singapore，定向扩张可转Tokyo；连续范围证书](research/2026-a/results/task4_v67_joint_stress/README.md) |
| V66原件与人群核查 | [上海年报年份、Phoenix真实学生调查及London/Bogotá新入口；排名不变](research/2026-a/results/task4_v66_intake/README.md) |
| 当前模型一键复算 · V102 | [统一入口、250格基线校验与当前证据](research/2026-a/results/task4_current/README.md) |
| 全偏好范围补数规划 V64 | [Phoenix最小有利补数3→4项；避免固定权重下的乐观规划](research/2026-a/results/task4_v64_continuous_acquisition/README.md) |
| 真实高中通学更新 V63 | [Cape Town采用2025微观数据；182名学生与抽样包络重算](research/2026-a/results/task4_v63_cape_2025/README.md) |
| 校级原件补充 V62 | [新增London、Copenhagen、Cape Town学校数据；保持未匹配区间](research/2026-a/results/task4_v62_source_intake/README.md) |
| 教师人数审计 V61 | [撤回未核验的965人下界；Dhaka第21→22，保留来源上界](research/2026-a/results/task4_v61_dhaka_roles/README.md) |
| 宗教高中覆盖 V60 | [Dhaka补入Alim计数界，排名不变；Phoenix与Lagos保留未知](research/2026-a/results/task4_v60_dhaka_madrasa/README.md) |
| 高中阶段计数界 V59 | [Dhaka用同类总数约束学段混入；第22→21，保留未知分配](research/2026-a/results/task4_v59_dhaka_stage/README.md) |
| 高中覆盖与师资 V58 | [Jakarta补入职业及宗教高中；校长与教师归属保留区间](research/2026-a/results/task4_v58_jakarta_staffing/README.md) |
| 人数核对 V57 | [同届学校合计超过学区2人；拦住未对账的排名提升](research/2026-a/results/task4_v57_school_union/README.md) |
| 队列对账 V56 | [PXU名册差异已解释；历史排除人数保留未知](research/2026-a/results/task4_v56_pxu_exclusion/README.md) |
| 补数优先级 V55 | [Phoenix实际学区毕业结果；本城测量改变推荐的最少组合](research/2026-a/results/task4_v55_recommendation_acquisition/README.md) |
| 范围核查 V54 | [完整名单、同口径分母与Phoenix新通学渠道；区间不收紧](research/2026-a/results/task4_v54_scope_intake/README.md) |
| 高中覆盖修订 V53 | [Istanbul新增两类高中项目，教师分配保留区间，第10→15](research/2026-a/results/task4_v53_istanbul_coverage/README.md) |
| 实际教育结果 V52 | [NYC含特许学校毕业汇总与条件排名对照](research/2026-a/results/task4_v52_nyc_county_outcomes/README.md) · [Phoenix11年级成绩及通学准入](research/2026-a/results/task4_v52_intake/README.md) |
| 证据撤回审计 V51 | [穷举115个单元及6555对：推荐依赖哪些证据](research/2026-a/results/task4_v51_evidence_withdrawal/README.md) |
| 同年证据与连续推荐 V50 | [Phoenix有日期的人数条件上界](research/2026-a/results/task4_v50_phoenix_cap/README.md) · [Singapore整个偏好区间推荐证书](research/2026-a/results/task4_v50_continuous_recommendation/README.md) |
| 证据审计 V49 | [Phoenix历史83名学生与São Paulo15条行程核验，排名及25城候选不变](research/2026-a/results/task4_v49_evidence_audit/README.md) |
| 真实年龄修订 V48 | [São Paulo对齐1690名14—18岁高中生，保留201名未知](research/2026-a/results/task4_v48_saopaulo_age/README.md) |
| 高中覆盖修订 V47 | [Tokyo新增3435名高中部学生；教师分配保留区间](research/2026-a/results/task4_v47_tokyo_coverage/README.md) |
| 官方资源修订 V46 | [Tokyo高中更新、大学总部下界与排名3→2](research/2026-a/results/task4_v46_tokyo/README.md) |
| 补数能力边界 V45 | [即使全城教育与通学精确，连续偏好下仍保留25城](research/2026-a/results/task4_v45_acquisition_limits/README.md) |
| 通学终点修订 V44 | [Melbourne核验7条未明确记录；分开数据与推断效果](research/2026-a/results/task4_v44_melbourne/README.md) |
| Phoenix同年学区核查 V43 | [227条人数记录均被抑制；排名与冠军集合不变](research/2026-a/results/task4_v43_lea_audit/README.md) |
| Phoenix完整名录 V42 | [公校师资下界与唯一未封顶分母](research/2026-a/results/task4_v42_phoenix_public/README.md) |
| 最新匹配证据 V41 | [Toronto考试分母与Phoenix实际教师记录](research/2026-a/results/task4_v41_matched_evidence/README.md) |
| 最新高中原件 V40 | [Toronto学校成绩、Nairobi学生及Mumbai分类统计](research/2026-a/results/task4_v40_intake/README.md) |
| 有限精度补数 V39 | [Phoenix：5%残余区间下至少需5项](research/2026-a/results/task4_v39_finite_precision/README.md) |
| 最新覆盖修订 V38 | [Singapore纳入748名预科学生并保留教师分配区间](research/2026-a/results/task4_v38_singapore/README.md) |
| 校级资源诊断 V37 | [学生加权指标与缺失学校界](research/2026-a/results/task4_v37_school_resources/README.md) |
| 最新补数诊断 V36 | [Delhi门槛4→3；London校级匹配](research/2026-a/results/task4_v36_acquisition/README.md) |
| 数据准入审计 V35 | [London原件与不可采纳的教师上界](research/2026-a/results/task4_v35_admission/README.md) |
| 最新高中补数 V34 | [Delhi真实师资计数：排名18→14](research/2026-a/results/task4_v34_delhi_school/README.md) |
| 分区聚合检验 V33 | [真实16区数据检验汇总偏差](research/2026-a/results/task4_v33_district_resources/README.md) |
| 最新教育修订 V32 | [Warsaw真实分母界与Shanghai新学年](research/2026-a/results/task4_v32_school_stage/README.md) |
| 最新补数可行性 V31 | [Phoenix四项方案的证据强度门槛](research/2026-a/results/task4_v31_acquisition/README.md) |
| 最新高中通学修订 V30 | [Cape Town：真实学生、抽样误差与排名13→5](research/2026-a/results/task4_v30_cape_town/README.md) |
| 最新教育年份对照 | [Jakarta 2025/26：分数更新与来源撤回检验](research/2026-a/results/task4_v29_education_year/README.md) |
| 当前数学公式与补数方向 | [当前模型](research/2026-a/design/task4_current_model.md) · [当前连续偏好的补数条件](research/2026-a/results/task4_v101_current_acquisition/README.md) |
| 历史条件基准 V23 | [覆盖修订与排名](research/2026-a/results/task4_v23_roster_coverage/README.md) · [算法入口 current_bounds](research/2026-a/scripts/task4_roster_coverage_comparison.py) |
| 当前10项指标定义 | [指标规范](research/2026-a/design/task4_v5_indicator_spec.md) |
| V6历史模型与结果 | [V6报告](research/2026-a/results/task4_v6/REPORT.md) · [结果表](research/2026-a/results/task4_v6/after_v6.csv) · [独立复核](research/2026-a/results/task4_v6_review.md) |
| 累计证据基准 V16 | [报告](research/2026-a/results/task4_v16_combined/README.md) · [排名对照](research/2026-a/results/task4_v16_combined/ranks.csv) · [算法](research/2026-a/scripts/task4_combined_evidence.py) |
| 补数策略 V17 | [报告](research/2026-a/results/task4_v17_rival_acquisition/README.md) · [当前排名](research/2026-a/results/task4_v17_rival_acquisition/current_ranks.csv) · [算法](research/2026-a/scripts/task4_rival_acquisition.py) |
| V18高中毕业队列条件分析 | [报告](research/2026-a/results/task4_v18_cohort_outcomes/README.md) · [官方NYC来源](research/2026-a/data/task4_v18_nyc_quality/README.md) · [排名与权重对照](research/2026-a/results/task4_v18_cohort_outcomes/ranks.csv) |
| V19 Phoenix分组重叠边界 | [报告](research/2026-a/results/task4_v19_partition_outcomes/README.md) · [真实分组人数与见证](research/2026-a/data/task4_v19_phoenix_partitions/README.md) |
| V20 NYC真实通学日记 | [报告](research/2026-a/results/task4_v20_nyc_reported_travel/README.md) · [2010–2011高中生记录](research/2026-a/data/task4_v20_nyc_travel/README.md) · [2024调查未成年人覆盖审计](research/2026-a/data/task4_v20_nyc_school_survey/README.md) |
| V21 通学链恢复 | [同口径前后对照](research/2026-a/results/task4_v21_nyc_chains/README.md) · [真实行程与筛选规则](research/2026-a/data/task4_v21_nyc_chains/README.md) |
| V5补数前后对照 | [V5报告](research/2026-a/results/task4_v5/REPORT.md) · [独立复核](research/2026-a/results/task4_v5_review.md) |
| 历史设计与研究迭代 | [研究工作台](research/2026-a/README.md) · [研究设计](research/2026-a/design/research_design.md) |
| 图表、地图与制图规范 | [制图入口](research/2026-a/visuals/README.md) · [规范](research/2026-a/visuals/GUIDELINES.md) · [地图](research/2026-a/visuals/cartography/README.md) |
| 写作与论证经验 | [论文阅读](research/2026-a/paper_review/README.md) · [第二轮证据卡](research/2026-a/paper_review/round2/README.md) |
| 历史获奖论文 | [目录](library/catalog.csv) · [离线索引](library/index.html) · [说明](library/README.md) |

## 仓库逻辑

```text
HiMCM/
├── research/2026-a/
│   ├── inputs/       # 题面、队员原件与外部方法资料
│   ├── data/         # 原始数据、来源清单、提取器、整理后的观测
│   ├── design/       # 指标定义、模型方案、早期合成实验
│   ├── scripts/      # 数据分析、模型、回归检查
│   ├── results/      # 各版本结果、敏感性、证据准入与复核
│   ├── visuals/      # 图表、地图、风格参考与插图包
│   ├── paper_review/ # 历史论文阅读与写作分析
│   └── logs/         # 决策、AI用途与研究交接
├── library/          # 历史论文原件、目录及来源证据
├── docs/             # 结构说明与迁移记录
└── scripts/verify_repository.py  # 路径、原件与目录完整性校验

HiMCM-Overleaf/                  # 相邻的独立论文工作区
├── main.tex / ref.bib / mcmthesis.cls
├── drafts/task4_paper_core.md    # 任务4正文主线
├── research/2026-a/visuals/      # LaTeX插图片段与选用的论文资产
└── archive/github_before_split/ # 拆分前GitHub论文版本
```

研究流程是：**原始资料 → 提取与口径核验 → 观测及效用区间 → 模型 → 结果和图表 → 团队选用到Overleaf论文**。原始附件按字节保留，派生结果另存；历史版本不会被新模型覆盖。

## 数据在哪里

以下路径均位于`research/2026-a/`。

| 数据 | 入口 | 内容与状态 |
| --- | --- | --- |
| 候选城市 | [data/city_candidates_team_25.csv](research/2026-a/data/city_candidates_team_25.csv) | 25城身份和地区等；不是指标数值矩阵 |
| 团队原始材料 | [inputs/team/](research/2026-a/inputs/team/) | 11指标、5指标、新版10指标和试点附件，保留原件及来源记录 |
| 早期真实四指标 | [data/task4_real/](research/2026-a/data/task4_real/README.md) · [CSV](research/2026-a/data/task4_real/city_indicators_2025.csv) | Numbeo 2025版25城安全感、污染感知、房价收入比、通勤代理；不等于凶杀率、PM2.5或学生通学 |
| 生活成本、住房等 | [data/task4_v5_core/](research/2026-a/data/task4_v5_core/README.md) · [观测](research/2026-a/data/task4_v5_core/observations.csv) | 25城CLI和PIR，另含新加坡凶杀率及公交名录证据 |
| PM2.5 | [data/task4_v5_air/](research/2026-a/data/task4_v5_air/README.md) · [观测](research/2026-a/data/task4_v5_air/observations.csv) | WHO来源，22城条件观测；实际观测年与发布年分开记录 |
| 高中师生比 | [data/task4_v5_education/](research/2026-a/data/task4_v5_education/README.md) · [V6新增](research/2026-a/data/task4_v6_education/README.md) | 东京、上海、新加坡；V6新增Istanbul、Jakarta，保留学段及范围限制 |
| 宽带与高教资源 | [data/task4_v5_resources/](research/2026-a/data/task4_v5_resources/README.md) · [观测](research/2026-a/data/task4_v5_resources/observations.csv) | 23城固定宽带和新加坡核验高校名录下界 |
| 学习设施空间可达性 | [data/task4_access/](research/2026-a/data/task4_access/README.md) | 城市网格、人口、Learning步行/骑行模型数据；不是学校质量或实际通学 |
| 学生通学与教育结果 | [data/task4_school/](research/2026-a/data/task4_school/README.md) · [墨尔本通学](research/2026-a/data/task4_school_commute_extra/README.md) · [补充教育结果](research/2026-a/data/task4_school_quality_extra/README.md) | 新加坡、纽约、墨尔本等学段证据，具体限制见各目录 |
| V6新增通学 | [data/task4_v6_commute/](research/2026-a/data/task4_v6_commute/README.md) · [效用界](research/2026-a/data/task4_v6_commute/bounds.csv) | Mexico City保守下界；Tokyo资料保留作诊断，未准入主模型 |
| Phoenix学校审计 | [data/task4_v6_phoenix/](research/2026-a/data/task4_v6_phoenix/README.md) | 官方学校记录与市界匹配；完整公校FTE子群不冒充全市教师人数口径 |
| 国家—年份补充资料 | [data/country_year_homicide_education/](research/2026-a/data/country_year_homicide_education/) | World Bank凶杀率与中学生师比；国家级资料不能直接填入城市高中指标 |
| 旧空模板 | [data/indicator_matrix_template.csv](research/2026-a/data/indicator_matrix_template.csv) | 初期18城×12指标共216行，数值为空，保留作历史版本 |

各数据目录的`README.md`解释口径，`manifest.json`或来源清单记录URL、年份、下载状态与SHA-256，`extract_*.py`从归档原件重建`observations.csv`。下载失败、人工转录、部分名录与诊断数据分别标记。早期[source_registry.csv](research/2026-a/data/source_registry.csv)是来源规划；最新取数以各目录清单和模型准入表为准。

**目前没有一张填满的25城×10指标实测矩阵。** 主模型汇合多份观测及既有学生通学证据：未知效用保留为[0,1]，部分名录提供单侧界。[V6效用长表](research/2026-a/results/task4_v6/utility_bounds.csv)列出250格更新前后的端点。[V5准入表](research/2026-a/results/task4_v5/source_admission.csv)与[V6新增准入表](research/2026-a/results/task4_v6/source_admission.csv)说明哪些证据被采用或拒绝。

## 当前进度与结论

V23补回 Melbourne 名册中的未观察通学者，并为 Mexico 在读未知者保留可选成员区间。固定 NYC under19 口径，Melbourne 十指标决策排名2→4、含毕业结局情景2→5；Phoenix仍24，可能冠军仍25。区间变宽反映原有覆盖不足，不能解释为城市条件恶化。完整人口、年份与权重限制见[本轮报告](research/2026-a/results/task4_v23_roster_coverage/README.md)。

V16将 Mexico City 2020年通学资料与 São Paulo 2023年高中通学资料作条件合并：São Paulo决策排名14→6、Mexico City 21→20、Phoenix仍为24；平均得分区间宽度38.0831→37.8657。仍有25个可能冠军，Singapore仍是最小最大遗憾推荐（28.1736）。来源、年份和学段条件保留，不能将决策排名解释为已确定的真实表现排名。

V17在相同观测矩阵上计算竞争城市补数策略，实际排名与冠军集合不变。所有假设观测仅用于补数诊断。完整对照与验证见上方V16、V17入口。

V18新增官方NYC四年毕业队列人数，保留未知结局，作为附加毕业结果维度的条件分析。该维度权重为10%时，补数使纽约决策排名18→4；可能冠军仍为25城，整体区间仍宽于原十指标模型。学段完成结果不等于教学因果质量，且不同城市归属口径尚未统一；[详见V18报告](research/2026-a/results/task4_v18_cohort_outcomes/README.md)。

V19利用Phoenix已归档96校的真实分组人数，计算允许学校记录重复的分组下界，并显式检验跨校标签一致性条件。稳定标签情景下得分区间仅缩窄约0.059分，Phoenix仍第24，可能冠军仍25；不限制标签变化时保留旧宽区间。

V20取得官方2010–2011年NYC家庭出行微观记录，以当前9–12年级识别学生，并保留缺失行程、未知成员和抽样敏感性。小于19岁的条件替代情景使纽约十指标决策排名18→22、含毕业结果模型4→5，可能冠军仍25；这是历史报告行程与旧路线估计的替换对照，不是跨年趋势。2024公开调查的成人日记不能替代未成年高中生，覆盖审计已归档。

V21在同一份纽约日记中恢复7名已知高中生和1名可选成员的交通停留链，只接受换乘、接客和下客；包含工作等活动的15条链保持未知。小于19岁情景的通学效用区间缩窄约7.28%，十指标纽约排名22→21，冠军集合仍25城；原有402条直接行程全部保留。

### 早期版本进度快照（V5/V6）

| 项目 | 状态 |
| --- | --- |
| 历史论文 | 68篇独立获奖论文、84份参考PDF；第二轮有13篇重点选段及36张证据卡 |
| 早期真实分析 | 已完成25城四项代理、学习设施可达性修订、学段证据修订与缺失维度检验 |
| V5 | 10指标固定权重、区间TOPSIS、最坏遗憾决策；同模型补数后有信息单元28→104/250 |
| V6 | 新增3个有信息单元，104→107/250；平均得分区间宽度39.83594→39.23998（100分尺度） |
| 冠军识别 | V6仍有25个可能冠军、0个必然冠军；各城表现名次界仍1–25 |
| 稳健决策 | 最坏遗憾规则下选择Singapore，最小最坏遗憾35.96038；不是证明其为真实表现冠军 |
| 采集决策 | 已输出最少补数方案、单项排除阈值和36组V6敏感性结果 |
| 图表与地图 | 分析图、真实底图、卫星参考及插图包已归档；须按各自模型版本引用 |
| 论文 | 研究报告与配图供团队选用；最终正文、新闻稿和AI使用报告由Overleaf工作区核对完成 |

V6沿用8项主指标各0.1125、公交和泳池两项辅助各0.05的规范权重。跨年、城市边界、年龄学段和来源可比性仍有限制；点值也不代表测量无误。早期合成实验在`design/synthetic_results*`中，不能写成真实城市结果。

优先查看：

- [after_v6.csv](research/2026-a/results/task4_v6/after_v6.csv)：得分界、名次界、冠军资格、最坏遗憾和决策序。`decision_rank`是行动选择排序，`best_rank`/`worst_rank`是允许证据下的表现名次范围。
- [rank_changes.csv](research/2026-a/results/task4_v6/rank_changes.csv)：V5→V6同模型信息更新对照。
- [acquisition_certificate_after.csv](research/2026-a/results/task4_v6/acquisition_certificate_after.csv) / [minimal_bundles_after.csv](research/2026-a/results/task4_v6/minimal_bundles_after.csv)：最少采集数量与并列方案。
- [sensitivity.csv](research/2026-a/results/task4_v6/sensitivity.csv)：锚点、辅助权重和新增来源筛选对照。

## 使用与复现

当前条件模型可运行 `python3 research/2026-a/scripts/task4_singapore_coverage_revision.py`。历史累计模型与补数策略可在本仓库根目录运行：

```sh
python3 research/2026-a/scripts/task4_combined_evidence.py
python3 research/2026-a/scripts/task4_rival_acquisition.py
python3 research/2026-a/scripts/test_task4_rival_acquisition.py
```

以下保留原完整README的早期版本复现步骤。

阅读CSV、Markdown和PDF无需运行程序。`library/index.html`等交互索引需在本地浏览器打开，GitHub文件预览不会执行它们。

在仓库根目录运行，可离线重建V6新增观测和模型输出并执行检查：

```sh
python3 -m pip install -r requirements-research.txt
python3 research/2026-a/data/task4_v6_education/extract_education.py
python3 research/2026-a/data/task4_v6_phoenix/extract_phoenix.py
python3 research/2026-a/data/task4_v6_commute/extract_commute.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/task4_v6_model.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/test_task4_v5.py
OPENBLAS_NUM_THREADS=1 python3 research/2026-a/scripts/test_task4_v6.py
python3 scripts/verify_repository.py
```

教育PDF提取另需系统命令`pdftotext`（Poppler）。[研究依赖](requirements-research.txt)依据已归档的[runtime_versions.json](research/2026-a/data/task4_real/runtime_versions.json)；论文文本审计另用根目录`requirements.txt`。国家—年份Excel导出另见其数据目录的`requirements.txt`。V5观测重建步骤见[V5报告](research/2026-a/results/task4_v5/REPORT.md)；主模型复用已归档学生通学结果，无需重新联网取数。

## 同步、版本与引用

研究在`main`维护。用户已明确授权立即提交并推送本地最新数据、模型、结果和README；早期“赛后才推送”的约定不适用于此次发布。推送前获取并整合远端新增提交，保留各自历史，不强制覆盖；论文在`HiMCM-Overleaf`单独同步，不把研究仓库整体推入Overleaf。本地旧日期钩子仅在此次授权推送时单次跳过，不修改钩子，不设置自动发布。

既有[历史论文Release](https://github.com/TypeThe0ry/HiMCM/releases/tag/v2026.11.06-68papers)是早期论文库快照，最新研究请查看`main`。可再生的超大制图打包文件与底图缓存按制图目录忽略规则保留本地，已追踪图表、来源清单和重建脚本随代码同步。

候选、假设、条件观测、诊断和合成实验须保持区分。引用回到原始来源，AI使用按队伍要求记录并核对。第三方论文与数据版权归原权利人。目录与迁移历史见[结构说明](docs/repository_structure.md)及[迁移表](docs/file_moves.csv)；早期交接文档反映当时状态，当前进度以本页和对应版本结果报告为准。

最近更新：2026-11-07，Asia/Singapore。

- [V22：可能冠军的有利假设门槛与 Phoenix 来源核验](research/2026-a/results/task4_v22_optimism/README.md)
