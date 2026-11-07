# 2026 HiMCM A

**The City Showdown: Modeling the Best City to Live In**

本仓库用于2026年HiMCM A题的全球城市研究：整理资料、蒸馏历史获奖论文、设计指标和模型、记录修订与检验，并逐步形成可复核的城市比较。

**当前仍处于研究与数据准备阶段，没有真实城市最终排名。全部2026研究在本次整理后合并到本地 `main`；按约定，比赛结束前不推送。**

## 从这里开始

| 想了解什么 | 入口 |
| --- | --- |
| A题原文 | [problem_a_2026.pdf](research/2026-a/inputs/problem_a_2026.pdf) |
| 2025评委文章 | [judges_commentary_2025.pdf](research/2026-a/inputs/judges_commentary_2025.pdf) |
| 研究总览 | [研究工作台](research/2026-a/README.md) |
| 最新团队候选城市 | [25城规范表](research/2026-a/data/city_candidates_team_25.csv) |
| 新增11项指标底稿 | [原始指标稿](research/2026-a/inputs/team/indicator_sources_11_original.md) |
| 模型主线与重大修订设计 | [研究设计](research/2026-a/design/research_design.md) |
| 写作、结构与论证经验 | [论文蒸馏](research/2026-a/paper_review/writing_and_reasoning.md) |
| 创新方向与检验 | [创新路线](research/2026-a/design/innovation_routes.md) |
| 全球数据口径与来源 | [数据可行性](research/2026-a/data/data_feasibility.md) · [来源登记](research/2026-a/data/source_registry.csv) |
| 历史获奖论文 | [总目录](library/catalog.csv) · [离线索引](library/index.html) · [论文文件夹](library/papers/) |

## 研究主线

比较高中生真正能到达、负担、进入和使用的城市机会。先公开界定人群、城市边界和“最好”的含义，再建立透明基准模型；用具体反例或数据诊断推动一次重大修订，最后检验推荐在不同偏好、年份与数据误差下是否成立。

主要关注学习机会、独立出行与安全、健康环境、课外成长和日常负担能力。维度、指标及权重尚未最终冻结；新增11项指标底稿是团队提供的候选方案，其中的数值、来源与判断尚未由本次整理逐项核实。

## 当前进度

| 项目 | 状态 |
| --- | --- |
| 历史论文库 | 68篇独立获奖论文，已与官方名单核对；62 Outstanding、4 Finalist、1 Meritorious、1 Honorable Mention |
| 论文规律提取 | 68篇文本特征扫描；12篇摘要、结构及检验相关段落的重点阅读 |
| 城市样本 | 新增25城团队候选；早期18城方案保留作历史版本，最终样本未冻结 |
| 指标方案 | 团队11项指标底稿已归档；既有12项候选模板仍保留，待统一取舍 |
| 数据矩阵 | 既有216行模板来自18城×12候选指标，数值栏全部为空；不是25城实测数据 |
| 方法实验 | 合成反例与五项结构检查已完成；不构成真实城市结论 |
| 实证结果 | 尚未完成取数、真实排序、重大修订的真实数据对照、新闻稿和最终参赛稿 |

历史论文库还附84份参考PDF。2018—2023年Outstanding共50篇已收齐，其余年份与奖项仍有缺口；详见[论文库说明](library/README.md)。

## 目录结构

```text
.
├── README.md                     # 当前项目入口
├── requirements.txt              # 论文文本审计依赖
├── docs/                         # 结构说明、迁移记录、历史论文接力
├── scripts/verify_repository.py   # 路径、清单、原件与论文完整性核验
├── library/                      # 历史获奖论文与来源
│   ├── papers/                   # 年份 / 奖项 / 题号
│   ├── references/               # 名单、题目、点评、其他赛事附件
│   ├── originals/                # 用户最初提供文件的保留副本
│   ├── source_snapshots/         # 来源网页与提取文本
│   ├── catalog.json              # 论文路径、来源与SHA-256
│   ├── catalog.csv
│   └── index.html                # 在本地浏览器中打开
├── research/2026-a/
│   ├── inputs/                   # 题面、评委文章、方法资料、团队原件
│   ├── paper_review/             # 写作蒸馏与审计依据
│   ├── design/                   # 研究方案、创新路线、合成实验输出
│   ├── data/                     # 候选城市、指标模板、来源登记
│   ├── scripts/                  # 文本审计、合成实验
│   └── logs/                     # 用户要求、AI用途与交接记录
└── .githooks/pre-push             # 比赛结束前阻挡推送
```

详细命名和资料状态约定见[仓库结构说明](docs/repository_structure.md)。旧路径与新路径对应见[文件迁移表](docs/file_moves.csv)。

## 使用与复现

阅读资料无需运行程序。下载或克隆后直接打开Markdown、CSV、PDF。`library/index.html`需要在本地浏览器打开才能筛选并访问本地论文，GitHub文件预览不会执行它。

在仓库根目录运行：

```sh
python3 -m pip install -r requirements.txt
python3 research/2026-a/scripts/audit_papers.py
python3 research/2026-a/scripts/revision_lab.py
python3 scripts/verify_repository.py
```

文本审计会更新`paper_review/`的派生记录；合成实验会更新`design/synthetic_results.json`和说明文件。合成数据、参数和偏好抽样分布均为演示设定，不能写成城市实测结果或学生民调。

新增城市或指标后，先核实原始来源、边界、实际观测年份、年龄口径和单位，再建立单独的实测长表。不要将旧空模板直接称作已经完成的25城数据。

## 本地合并与发布约定

研究分支 `research/2026-a-local` 的内容在本次整理后合并到本地 `main`；分支保留供追溯。此次没有推送、更新Release或创建定时发布。

本地启用推送阻挡：

```sh
git config core.hooksPath .githooks
```

按[COMAP官方赛期](https://www.contest.comap.com/highschool/contests/himcm/instructions.html)，停止修改参赛稿为 **2026-11-18 09:00（新加坡时间）**，提交截止为 **10:00**。钩子在10:00前阻挡推送；到期只解除时间阻挡，不自动推送。其他克隆需要自行启用钩子；它不覆盖GitHub网页/API等发布方式。

既有[历史论文Release](https://github.com/TypeThe0ry/HiMCM/releases/tag/v2026.11.06-68papers)仍保留早期目录结构，本次未更新；其中不包含本轮A题研究与新材料。

## 接力与引用

接下来先核验25城候选和11项指标稿的来源及可比性，统一指标与数据模板，再冻结V0、记录诊断并实施V1。已知设计、数据障碍及AI使用记录见[研究交接](research/2026-a/logs/research_handoff.md)；历史论文补齐工作见[论文库接力](docs/paper_library_handoff.md)。

所有候选、主张、核实数据和合成实验须区分标注。引用数据和已有方法时回到原始来源；AI辅助使用应记录并按官方要求另附报告。论文及第三方出版物版权归原作者与权利人所有，本仓库未授予新的第三方材料许可。

最近整理：2026-11-07，Asia/Singapore。
