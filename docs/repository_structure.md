# 仓库结构与命名

当前项目：2026 HiMCM A。目录与文件使用ASCII英文名，说明文档以中文为主，论文PDF正文保持原样。

| 目录 | 职责 |
| --- | --- |
| `library/` | 历史论文、参考文件、原始副本和来源证据 |
| `research/2026-a/inputs/` | 当前题面、评委文章、外部方法文件、团队原始资料 |
| `research/2026-a/paper_review/` | 历史论文阅读与审计产出 |
| `research/2026-a/design/` | 研究定义、模型候选、创新方案、合成实验 |
| `research/2026-a/data/` | 规范化候选城市、指标模板、来源登记、数据表 |
| `research/2026-a/scripts/` | 可重跑的处理和实验程序 |
| `research/2026-a/logs/` | 决策、用户要求、AI用途与接力记录 |
| `docs/` | 跨目录导航、改名迁移、历史接力 |

## 命名约定

- 文件名采用`snake_case`，研究目录使用`2026-a`；README保留标准大写名称。
- 历史论文按年份、奖项、题号分类；文件名包括赛季、题号、奖项、队号。现有题号目录保留A/B，奖项目录小写。
- 带`original`或位于`inputs/team/`的文件是输入原件；主张不会因为被归档而变成已核实事实。
- `candidate`表示未冻结候选，`template`表示模板，`synthetic`表示合成实验，`parsed`表示从原文件提取的记录。
- 不覆盖原件进行实质编辑。后续指标修订稿另存至`design/`或`data/`，保留来源与理由。

## 两份新资料

| 原始名称 | 新路径 | 状态 |
| --- | --- | --- |
| `cities(1).csv` | `research/2026-a/inputs/team/city_candidates_original.csv` | 按字节保留；25城候选，未冻结 |
| `评价指标_王树轩_11071410.md` | `research/2026-a/inputs/team/indicator_sources_11_original.md` | 按字节保留；11项指标底稿，未逐项核验 |

规范化城市表为`research/2026-a/data/city_candidates_team_25.csv`，仅统一列名并新增状态标记。原有城市、地域、气候、收入组和入选理由保持原文。理由标为`author_hypothesis_unverified`，不是实证结论。

原始名称、导入日期及SHA-256记录在`inputs/team/provenance.json`。早期18城候选和216行空模板保留，不被25城名单自动覆盖。

## 迁移与历史

`docs/file_moves.csv`记录旧路径、新路径与字节摘要。迁移后摘要是迁移当时的快照；之后有意修订README、脚本和说明，以Git记录及当前文件为准。论文PDF与两份新输入原件的字节内容均保留。

工作区顶层的早期论文库副本和两个大型压缩包移入`_local_archive/`，不放进本仓库。它是本机备份，不是后续研究的编辑入口。活动仓库使用本机`HiMCM/`目录。

历史Release保持原样，路径仍是早期中文目录；本次不会将竞赛期间研究内容加入公开Release。
