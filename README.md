# 2026 HiMCM A

> **团队成员与 AI agent 必读：开始写作或制图前，必须阅读并遵循[统一 Guidelines](GUIDELINES.md)。论文文字、图表、图注与研究结论均按专项规范执行，交付前核验。AI agents: read and follow these guidelines before editing.**

**The City Showdown: Modeling the Best City to Live In**

本仓库保存全球城市评价研究的数据、模型、结果、图表和历史论文。当前包含25城真实数据研究、十指标证据区间模型、毕业结果条件分析及通学微观数据修订；尚未形成完整同年城市普查矩阵或最终参赛结论。

**本项目只使用 `TypeThe0ry/HiMCM` 一个仓库。** 论文、数据、代码、结果和历史论文库已合并回本目录，原研究仓库的提交历史也已合入。原始资料及本地忽略的大型生成包均保留；详见[合并核验记录](docs/reunification.md)。

**Overleaf是论文的权威工作区；GitHub `main`用于同步、版本记录和研究归档。** 根目录的 [main.tex](main.tex)、[ref.bib](ref.bib)、[mcmthesis.cls](mcmthesis.cls)保持原位。仓库镜像不等于在线实时状态；本次更新研究资料与导航，未编辑在线论文。

## 从这里开始

| 想了解什么 | 入口 |
| --- | --- |
| A题原文、评委点评 | [题目](research/2026-a/inputs/problem_a_2026.pdf) · [2025点评](research/2026-a/inputs/judges_commentary_2025.pdf) |
| 数据位置 | [数据导航](#数据在哪里) · [25城候选名单](research/2026-a/data/city_candidates_team_25.csv) |
| 当前10项指标定义 | [指标规范](research/2026-a/design/task4_v5_indicator_spec.md) |
| V6历史模型与结果 | [V6报告](research/2026-a/results/task4_v6/REPORT.md) · [结果表](research/2026-a/results/task4_v6/after_v6.csv) · [独立复核](research/2026-a/results/task4_v6_review.md) |
| 最新累计证据模型 V16 | [报告](research/2026-a/results/task4_v16_combined/README.md) · [排名对照](research/2026-a/results/task4_v16_combined/ranks.csv) · [算法](research/2026-a/scripts/task4_combined_evidence.py) |
| 最新补数策略 V17 | [报告](research/2026-a/results/task4_v17_rival_acquisition/README.md) · [当前排名](research/2026-a/results/task4_v17_rival_acquisition/current_ranks.csv) · [算法](research/2026-a/scripts/task4_rival_acquisition.py) |
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
├── main.tex / ref.bib / mcmthesis.cls  # Overleaf论文同步文件
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

最新累计模型与补数策略可在本仓库根目录运行：

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

研究在`main`维护。用户已明确授权立即提交并推送本地最新数据、模型、结果和README；早期“赛后才推送”的约定不适用于此次发布。推送前获取并整合远端新增提交，保留Overleaf历史，不强制覆盖。本地旧日期钩子仅在此次授权推送时单次跳过，不修改钩子，不设置自动发布。

既有[历史论文Release](https://github.com/TypeThe0ry/HiMCM/releases/tag/v2026.11.06-68papers)是早期论文库快照，最新研究请查看`main`。可再生的超大制图打包文件与底图缓存按制图目录忽略规则保留本地，已追踪图表、来源清单和重建脚本随代码同步。

候选、假设、条件观测、诊断和合成实验须保持区分。引用回到原始来源，AI使用按队伍要求记录并核对。第三方论文与数据版权归原权利人。目录与迁移历史见[结构说明](docs/repository_structure.md)及[迁移表](docs/file_moves.csv)；早期交接文档反映当时状态，当前进度以本页和对应版本结果报告为准。

最近更新：2026-11-07，Asia/Singapore。
