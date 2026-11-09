# V142：为16城可能领先给出可复算的严格内点情景

本轮把论文原先的单城反例替换为16座城市分别获胜的构造。同一个目标情景在基准和等权下均使该城市严格第一，最小领先分别4.965729、5.305594分（Amsterdam目标）。每个情景112点值不动、48不确定格严格处于原区间内部。独立标量复算通过32组、512得分、2560个utility值。这说明16可能冠军不是只依赖闭区间极端端点；结论仍限于既定utility矩形，不证明各维度共同物理可实现，也不赋予情景概率。

## 数据与论文的实际变化

- Madrid／Helsinki教师检索0准入：Helsinki工作地点／机构覆盖元数据原件HTTP200并lossless归档，但缺匹配城市高中学生分母的教学FTE；Madrid系列单位Número不等于FTE，两次原件连接各超时10秒，不取数。详见[data包](../../research/2026-a/data/task4_v142_education/README.md)。
- 主科学保持V136，扩展V137：112点／33部分／15全缺失，21累计补数。fixed平均宽度16.089333559066不变。本轮宽度缩小0；累计14.4675%来自此前真实补数。Zurich保守、16可能、0必要冠军；教育优先Oslo。原CSV SHA仍430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c。
- 自有独立稿文件名继续drafts/task4_v137_paper.tex/.pdf，文档修订V142；只改生成的修订段落及绑定回执，7个自有章节、数值表图和宏逐字节保持。队友main/ref/class及主文件设置未动。新增选定witness三文件供复核，完整矩阵留研究。
- 新PDF148811字节，SHA4c0ab92fe2ca4571107a60e5957a79179274f3c03cb2c35f1290b4276b7bd886；22页=20主文参考+2暂定AI，新闻15–16页，零warning。22页95dpi渲染六张总览和改变页单独检查完成。与Overleaf d309b11相比10／11／12页改变，其余19页像素相同。
- 139科学文件、39原资产／章节及74历史稿文件保护通过。审计results/task4_v142_documentation/audit.json；旧V140交付核对及PDF哈希是历史回执，不覆盖成新结果。

## 复现与边界

研究Python仍.venv-v120；运行scripts/task4_v142_witnesses.py，再audit_task4_v142_witnesses.py。首次verification.json保留，复核另写recheck_verification.json。文档交付审计audit_task4_v142_documentation.py核对现行PDF与Overleaf d309b11基线并独立比较22页；compiler_stdout_stderr.txt、paper_manifest.json及paper_qa.json归档于对应results目录。只需新增结果核验，无新科学变化无需重复旧24组MC。

采用指定中英文anti-defensive-writing技能，按已验证贡献组织修订段。125条局部AI选集及03:17UTC截止保持，后续消息未混入旧capture；全队史仍不完整。实际控制号PENDING、最终稿具体整合授权、全队AI记录和正式提交回执仍待真实信息；本稿不是最终参赛交付。

长期goal active。下一轮优先新匹配教师分母／实际高中单程旅时源或有目标学生权重的空间可达性证据，失败跳过；不反复用已拒收的Número、全龄旅时或潜在路由试填。GitHub公开发布选择仍待答，仅本地研究commit；Overleaf独立稿按既有授权正常push，完成回执另存sync.json。不更改仓库可见性、不force、不动队友正文。
