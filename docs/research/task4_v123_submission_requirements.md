# V123：2026 HiMCM提交要求与AI使用记录

核验日期：**2026-11-09，Asia/Singapore**。本说明依据当日COMAP官方2026入口及其直接链接文件，不是论文、AI使用报告正文或可提交声明。[原件与SHA256清单](../../research/2026-a/data/task4_v123_contest_requirements/source_manifest.json)已归档。

## 版式与Problem A交付

| 项目 | 核实要求／实施边界 |
|---|---|
| 首页 | 一页Summary Sheet，使用真实控制号及Problem A；官方通用模板的1111及多题选项是占位内容。 |
| 页数 | 主解答共≤25页，**包括**摘要页、目录、新闻稿、参考文献、注释及附录；摘要后最多24页。 |
| 目录 | 通用instructions称鼓励；**2026 Problem A明确列入应交内容**，故本题按应有目录执行。 |
| 页眉 | 每页顶部列队伍控制号和页码；规则给出的总页数形式是示例，不据此虚构额外格式要求。 |
| 文字 | 英文、可读字体至少12pt。官方模板采用Times New Roman，但规则没有限定必须该字体。规则未在该条给出图内文字的9pt豁免。 |
| 匿名 | 解答任何页不得出现学生、指导教师、学校／机构姓名；唯一队伍标识为控制号。 |
| Problem A | 至少排10城；解释选择与排除的指标、数据与限制；给出有理由的结论；记录至少一次重大模型修订及理由。 |
| 新闻 | **1–2页非技术news article**，面向COMAP，包含建模过程；计入25页。 |
| 文件 | 一个Adobe PDF，以核实后的控制号命名，**小于20MB**；不随交程序、数据库等其他文件。 |

来源：[2026 instructions](https://www.contest.comap.com/highschool/contests/himcm/instructions.html)，IV.12–14、VI“Preparing a Solution Document”1–5及“Submitting a Solution Document”；[2026 Problem A原题](https://www.contest.comap.com/highschool/contests/himcm/2026_Problems/2026_HiMCMProblem_A.pdf)，唯一页的任务与交付清单；[官方通用摘要模板](https://www.contest.comap.com/highschool/contests/himcm/flyers/HiMCM_Summary.docx)。

当前研究16城达到数量门槛，不等于全部交付要求通过。论文需明确初始模型、修订及其作用，不能只以版本号或补数格数代替“重大模型修订”的论证。团队图中文字≥9pt是内部最低制图要求，不能据此宣称已满足官方≥12pt规定。以上两句是本项目实施判断，不是新增COMAP条款。

## AI披露：硬性要求与官方示例分别处理

现行2026 instructions链接的AI政策原件标注**v102025**；其路径位于MCM目录，但这是HiMCM当前官方入口直接采用的共同政策，不是自行套用其他赛事旧政策。

- 披露范围包括研究、模型开发与代码、写作、翻译及嵌入式AI。解答需说明所用模型与用途，用行内引用，并在25页内的参考文献列出所有AI工具。
- 在主解答末尾追加标题为 **Report on Use of AI Tools** 的部分；该部分不限页，**不计入25页**，仍随同一PDF提交。
- 团队负责核实AI生成内容及引用的准确性、有效性与适用性并纠错；不能以工具名称列表替代对实际用途的披露。

政策第2页的生成式对话示例展示工具／版本日期、模型、逐字输入和**完整输出**。这为可恢复对话的记录提供了具体格式；原文把它们称为示例，并非一条对所有工具无例外的逐次日志句。**翻译有明确例外**：无需完整输入，按示例陈述使用方式；代码补全示例采用工具／版本日期及用途描述。例外不能扩张成研究、建模或写作对话都可省略真实输入输出。

来源：[COMAP现行AI政策，v102025，第1–2页](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)；[2026 instructions](https://www.contest.comap.com/highschool/contests/himcm/instructions.html)IV.9与VI“Preparing a Solution Document”4。官方[提交操作指南](https://www.contest.comap.com/highschool/contests/himcm/flyers/HiMCM-MidMCM_SubProcess.pdf)版本V20251103，亦由当前入口链接，列有AI使用Yes／No项；本轮未操作提交表。

## 现在可执行的记录整理

本节是研究工作流，不是已经完成的AI报告：

1. 按真实工具逐项列提供方、工具名、界面显示模型／版本、使用日期、用途、影响的代码／图／段落、原始日志定位及人工核验记录。区分聊天生成、代码补全、翻译、检索或其他嵌入式AI。
2. 对保存下来的生成式交互，导出真实输入与完整输出；保留历史原记录，另标最终采用内容和验证方式。不要以事后概述冒充逐字输入，也不要把只选取的有利输出称为完整输出。
3. 界面版本、日期或旧日志缺失时明确标为待核实。Git提交能证明文件变更，不能恢复原提示词、所有未采用输出或全部工具使用史。无需为填满示例而编造记录。
4. 由队伍核对本文档及所有使用史后，再组织行内引用、参考文献与附加报告。目前**完整使用史尚未确认**，不写“已经完整披露”或“可直接提交”。

任务交接指出模板中存在18213／18214不一致；本轮没有从注册账户核实，**不任选其中一个**。控制号、模型版本及所有历史AI记录的缺口由真实记录／用户确认解决；本说明不生成论文LaTeX、PDF或AI报告正文。

## 时限与比赛期间发布约束

官方停止修改时点为2026-11-17 20:00 EST，提交截止21:00 EST；对应新加坡时间分别为**2026-11-18 09:00和10:00**。两者不同：提交窗口末一小时不是继续修改时间。[2026 instructions](https://www.contest.comap.com/highschool/contests/himcm/instructions.html)IV.14及VI“Submitting a Solution Document”1–3。

同页IV.7禁止比赛期间以任何形式发布或分享题面、解题过程及部分／完整作品，并限制向队外人员寻求解题帮助。普通Git push授权不能作为符合比赛发布规则的证明。本轮只核对条文、未评判此前仓库可见性、未推送或提交比赛文件；后续动作应由队伍结合真实状态核对该规则。

## 归档与复核

[证据目录](../../research/2026-a/data/task4_v123_contest_requirements/)只保存官方原件、来源清单及离线核验脚本。运行：

```sh
.venv-v120/bin/python research/2026-a/data/task4_v123_contest_requirements/verify_sources.py
```

脚本核验下载字节哈希、2026入口、题面条款、当前链接AI政策版本及输入／输出示例和翻译例外、摘要模板结构与时区换算。它不核验队伍控制号、完整AI使用史或最终论文是否合规；[核验结果](../../research/2026-a/data/task4_v123_contest_requirements/verification.json)明确保留这些未确认项。
