# HiMCM 论文工作区

## 当前全部自有材料：V198／科学V197

标题、Summary、所有自有正文主题、结论、新闻稿、图表与图注、参考文献及暂定AI说明的完整清单见 [OWNED_MATERIALS.md](OWNED_MATERIALS.md)。完整PDF为 `drafts/task4_v198_paper.pdf`，当前编译入口为 `main.tex`，独立审阅入口为 `task4_v198_review_entry.tex`；当前版本以 `drafts/task4_current_review.json` 为准。以下旧版本说明保留历史状态。

此仓库直接同步 Overleaf 项目。2026-11-10按用户要求将根 `main.tex` 接到完整自有城市评价稿；队友原入口逐字节保存在 `archive/team_main_before_owned_entry_20261110/main.tex`。`ref.bib`、`mcmthesis.cls`保持。以下迁移记录描述历史状态。

- `drafts/`：从研究仓库迁入的写作稿，尚未合入正文。
- `research/2026-a/visuals/`：论文可选图册及 LaTeX 插入片段，保持来源路径；尚未接入当前正文。
- `statistics/`：论文可用的结果快照；模型代码、原始数据、生成过程仍在 [GitHub HiMCM](https://github.com/TypeThe0ry/HiMCM)。版本、人群及假设见相应 summary.json 和研究报告。
- `archive/github_before_split/`：GitHub 原有论文源文件的逐字节副本，与当前线上主稿有差异，不能自动覆盖主稿。
- `migration_manifest.json`：迁移路径、SHA256 和缺失图片清单。

编译检查目前被原有缺失图片 `framework.png` 阻断。其余旧正文图片也未在源仓库中找到；不使用无关研究图补位。详情见 [MIGRATION.md](MIGRATION.md)。

论文存在旧赛事主题与当前题目混用，属于待编辑内容，本次只整理仓库并保留原稿。图册中的历史模型图也不能自动视为最终论文结果。

## 2026-11-08 阶段进展

已将当前城市评价阶段结果作为独立新节接入主稿，旧正文和共享文献保留。可直接阅读 [3页阶段进展PDF](task4_stage_progress_preview.pdf)，或单独编译 `task4_stage_progress_preview.tex`。数据来源和验证见 [快照说明](statistics/task4_progress_2026-11-08/README.md)。完整主稿仍受原有缺图影响。

## 历史独立完整审阅稿：V154（冻结）

[完整审阅PDF](drafts/task4_v154_paper.pdf)及[LaTeX入口](drafts/task4_v154_paper.tex)统一16城V154主数据与受控扩展；[生成与核验](drafts/task4_v154_assets/README.md)。根入口task4_v154_review_entry.tex可供具体选稿时使用，未更改项目默认设置。

Milan104座站／枢纽的历史库存下界使矩阵成为112点／34部分／14全未知，累计22项补充。固定平均评分区间宽度16.06144，累计收窄14.62%；Zurich保守、16可能／0必要冠军。24页（22主文参考+2暂定AI），47编译引用、零警告、全部页实看。旧稿、队友main/ref/class保持；真实控制号、完整AI史和最终整合／提交仍待完成。

## 历史独立完整审阅稿：V137／文档V148（冻结）

[完整审阅 PDF](drafts/task4_v137_paper.pdf)与[LaTeX 入口](drafts/task4_v137_paper.tex)使用16城 V136 主数据及 V137 受控扩展，24页（主文和参考22页、暂定AI记录2页）。累计21项补数，矩阵112点／33部分／15全缺失；Zurich为保守推荐，16城仍都可能夺冠。数据来源章增加London原生站／hub库存及ONS边界核验，保留Paris教师分母不匹配的真实案例。

[构建、来源与核验说明](drafts/task4_v137_assets/README.md)。旧V131／文档V134及更早稿保留。共享main/ref/class和项目主文件设置保持；真实控制号、完整全队AI史及授权整合仍待完成。

文档修订V139已把恢复的Warsaw 2022真实旅时来源及学段不匹配原因写入当前V137数据章，并补官方引用；主科学V136/V137及数值资产保持，仍22页。旧V137 PDF保留于Git d8ba697，当前字节与检查见资产目录QA。

文档修订V140将AI局部选集扩至125条并同步附录；20页主文参考与V139像素一致。当前30项交付核对及待核实事项见[drafts/task4_v140_support](drafts/task4_v140_support/README.md)，最终可提交状态仍为false。

## V199：下一轮研究支持（尚未准入）

补数优先级、Singapore25处名录候选、使用／关闭范围及独立验证见[drafts/task4_v199_support/README.md](drafts/task4_v199_support/README.md)。当前完整自有稿仍V198，科学V197；标题、Summary与正文入口见OWNED_MATERIALS.md。
