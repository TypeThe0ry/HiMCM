# 我负责的全部论文材料｜当前V198

标题、Summary、正文各主题、结论、新闻稿、图表与图注、参考文献及暂定AI说明均已包含在完整自有稿中。科学版本V197；完整PDF共27页。

**完整PDF：** `drafts/task4_v198_paper.pdf`

**当前完整编译入口：** `main.tex`（独立审阅入口 `task4_v198_review_entry.tex` 仍可用）

**内部LaTeX入口：** `drafts/task4_v198_paper.tex`

| 材料／主题 | 论文位置 | 源文件（均在drafts/） |
|---|---|---|
| 论文标题 | 第1页 | `task4_v198_paper.tex` 中的 `\title` |
| Summary／摘要、关键词 | 第1页 | `task4_v198_front.tex` 的 `abstract` 环境 |
| 背景、问题范围、假设、符号 | 第3—4页 | `task4_v198_front.tex` |
| 数据搜集、来源及口径 | 第4—8页 | `task4_v198_core.tex` 第4节 |
| 指标矩阵图及图注 | 第9页 | `task4_v198_evidence_figure.tex`、`task4_v198_assets/identification_matrix.pdf` |
| 权重、TOPSIS、评分与结果 | 第8—12页 | `task4_v198_core.tex` 第5节、`task4_v198_assets/` 表图 |
| 来源撤回、均值及联合扰动边界 | 第12—13页 | `task4_v198_vintage.tex` |
| 未来情景、偏好权重、蒙特卡洛 | 第13—15页 | `task4_v198_core.tex` 第6.1—6.3节、`task4_v198_generated.tex` |
| 城市内部公平性、成长阶段 | 第15—16页 | `task4_v198_core.tex` 第6.4节及引用的历史案例资产 |
| 同国城市对比及图注 | 第16—17页 | `task4_v198_core.tex` 第7节、`task4_v172_country_figure.tex` 及其图形资产 |
| 结论 | 第17页 | `task4_v198_conclusion.tex` |
| 新闻稿 | 第18—19页 | `task4_v198_news.tex` |
| 参考文献 | 第20—25页 | `task4_v198_references.tex`，另含generated文件中的案例引用 |
| AI使用说明（暂定版） | 第26—27页 | `task4_v198_ai.tex` |
| 数值、图表与验证材料 | 配套文件 | `task4_v198_generated.tex`、`task4_v198_assets/`、`task4_v198_verification/` |

所有章节标题、图注和表注也保留在这些LaTeX文件中。逐项文件哈希和标题清单见 `drafts/task4_v198_owned_upload_manifest.json`，可核对完整上传。

按用户2026-11-10要求，现有 `main.tex` 已连接完整自有稿，标题和Summary随整稿编译。队友原 `main.tex` 逐字节保存在 `archive/team_main_before_owned_entry_20261110/main.tex`；`ref.bib`、`mcmthesis.cls`保持。没有改变服务器Main document设置。实际根入口本地重建27页，逐页文字和渲染与完整自有PDF一致；在线重新编译尚未验证。AI说明仍为暂定版，真实注册控制号及完整团队记录的状态见当前交付清单。
