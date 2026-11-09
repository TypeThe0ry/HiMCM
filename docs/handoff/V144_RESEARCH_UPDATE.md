# V144：具体来源核查揭示单格信息依赖

本轮从V143的批量来源标记压力测试推进到原始记录：取得CBS 2023发布的2022暂定城市单年受害者表、配套XLSX，以及Zurich PKS2025完整原报告。CBS Amsterdam单年10与2018–2022总数68明确分开；均不匹配原表numerator340，原数真正定义仍未追到。Zurich表的2024既遂1／2025既遂2为注册犯罪行为数，第118页明确独立于受害人数；未建立原0.14率的分母，不将行为数除以原人口冒充受害者率。详情见[data来源核查](../../research/2026-a/data/task4_v144_homicide/README.md)。

## 实际发现

| 撤回的点utility信息 | 变化格 | 基准推荐 | 等权推荐 | 基准均宽 |
| --- | ---: | --- | --- | ---: |
| 无（现行V136） | 0 | Zurich | Zurich | 16.089334 |
| Amsterdam凶杀点 | 1 | Zurich | Zurich | 16.720516 |
| Zurich凶杀点 | 1 | Singapore | Oslo | 16.602168 |
| 两点 | 2 | Singapore | Oslo | 17.233350 |

单点试验其余159格固定，两点试验158格固定；原48非点、所有补充和权重不动。全部8组仍16可能／0必要冠军。该结果说明保留原点值的推荐依赖具体一项未核实来源，不是声称已找到28点批量撤回结果的唯一原因。原CSV已有值及主V136／扩展V137完全保持，新增模型准入0，原平均宽度本轮收窄0；官方新人数／行为数只用于来源核查，不作替代率或未来趋势。

## 验证与稿件

- 原XLSX／两HTML／6,989,421字节完整PDF的HTTP200原件已归档，gzip可精确恢复。提取器核workbook关系、原表、暂定标记、2018–2022合计及行为单位。独立audit_task4_v144_homicide.py再核原XML指定单元格、原HTML2022行和PDF117／118／120页逐字节复抽，并标量复算128城市情景／256得分界、遗憾与全部排名／冠军标记，全部通过。原verification冻结，重放另写recheck。
- 自有稿新增真实搜集口径案例、Section5.5单点撤回，摘要／结论／新闻同步其信息条件，补CBS／PKS两引用。原V143批量测试、V142内点验证和原表图／数值宏保留。队友main/ref/class与项目main设置保持，Overleaf入口AGENTS旧V140文档标签已更新V144。
- 当前稿仍drafts/task4_v137_paper.tex/.pdf，文档V144；154783字节，SHA3caf1fa59d423c99bd78082899149de8adc686d9d635ae48751e3e1adcd94580。23页=21主文参考+2暂定AI，新闻16–17、参考18–21、AI22–23；编译0warning。全部23页95dpi／六张总览及新增第7／11页单独实际检查完成。与Overleaf39b6a35相比变化页1、7、8、11、12、13、15、16、17、21，其余13页像素相同。
- 当前文档审计audit_task4_v144_documentation.py保护139科学文件、42原资产／章节和74历史稿；8份选定源／审计副本精确匹配。compiler_stdout_stderr、paper_manifest、paper_qa、audit在results/task4_v144_documentation。checker修复PDF行末断词引起的文本比对误报，没有为检查改写正文。
- 按Overleaf AGENTS本轮亦尝试编译共享main，仍因原有framework.png缺失失败；日志单独归档，不改图或正文、不把独立稿技术通过称全项目通过。指定中英文anti-defensive-writing持续用于说明与论文。

## 下一项与边界

优先追溯Zurich原凶杀率真正分母／统计单位及匹配的城市受害者记录，再查真正新匹配教师／高中实际通学源；保留原表，任何新率只能独立受控对照，不自动替换。CBS2022暂定表不是最新修订终值，0.14未认证也不等于本轮证明原作者错误，不猜来源。

长期goal active。GitHub公开发布选择仍待答，研究本地commit；Overleaf自有稿按授权正常push，sync.json记录结果，无force。无connected session，使用已fetch Git镜像。真实控制号PENDING、完整全队AI史、最终稿具体整合和正式提交回执仍缺真实资料；125条根会话局部AI选集及其固定截止保持，不混入新消息或私有原文。
