# 团队写作与制图规范｜所有成员及 AI agent 必读

**凡新增或修改论文、摘要、新闻稿、图表、图注、研究结论与交接文档，必须遵循本页及对应专项规范。开始编辑前先读规范，交付前按清单核验。**

**AI agents: Read this file and the applicable guidelines before drafting or editing. Follow the writing, evidence and figure requirements, and verify the final rendered output before delivery.**

## 阅读顺序与适用范围

| 顺序 | 必读文件 | 适用工作 |
| --- | --- | --- |
| 1 | [AGENTS.md](AGENTS.md) | 工作区、Overleaf、协作与同步 |
| 2 | [写作规范](docs/guidelines/WRITING.md) | 所有论文文字、摘要、结论、新闻稿、图注 |
| 3 | [证据与数据规范](docs/guidelines/EVIDENCE.md) | 数值、公式、排名、比较和科学主张 |
| 4 | [图片与地图规范](research/2026-a/visuals/GUIDELINES.md) | 所有新制或修改的图表、地图、卫星面板 |
| 5 | [交付检查](docs/guidelines/CHECKLIST.md) | 合并、上传或交稿前 |

普通仓库说明按其功能写清用途和路径；研究日志可保留过程。论文正文按问题与证据组织，不照搬日志。仅修改代码时阅读与其输出相关的规范。

## 共同要求

**用户强制要求（2026-11-08）：** 所有新增／修改论文文字及研究说明必须使用 [anti-defensive-writing-Skill](https://github.com/Adkid-Zephyr/anti-defensive-writing-Skill)。中文读[本地快照](research/2026-a/visuals/guidelines/anti-defensive-writing/zh/SKILL.md)，英文读[English skill](research/2026-a/visuals/guidelines/anti-defensive-writing/en/SKILL.md)。围绕已有证据支持的贡献组织叙事，删除重复辩解和实验流水账；结论所需的反例、代理口径和不确定性仍按证据规范完整保留。见[安装与执行规则](docs/guidelines/ANTI_DEFENSIVE_WRITING.md)。

1. **先写有证据支持的贡献与结果。** 段落围绕一个判断，随后给出依据与解释；避免模型名堆砌、流程流水账和泛泛赞美。
2. **主张精度与证据精度一致。** 数值可追溯到数据、脚本或结果文件；模型版本、人群、年份、地理范围和单位一致。
3. **使用反防御性写作。** 删除重复辩解与无意义自我削弱；把影响结论的条件简洁写入相应定义、方法或结果。保留必要反例和不确定性，避免挑选结果或夸大优势。
4. **按最终版面检查可读性。** 新图所有文字，包括来源署名，最终印刷至少 9 pt；拥挤时拆图或重排。高 DPI 不增加卫星源数据的信息量。
5. **让图与正文共同论证。** 每幅图回答明确问题；正文解释具体发现，图注说明对象、指标、比较口径与来源。
6. **保持可复核。** 原始资料、计算结果、视觉背景和假设情景分别标识；科学解释与数据能力对应。
7. **保留团队内容与原件。** Overleaf 为主稿权威工作区；历史论文与团队原始输入保持原貌，新规范用于新写与改版材料。

## 当前规范与参考资料

本页及专项规范是当前团队执行标准。下列材料用于查证、借鉴和编辑训练；其中早期字号建议、版本状态或写作建议与当前规范冲突时，按当前规范执行。题面与比赛正式要求须核对原文；团队风格偏好不能改变这些要求。

| 参考 | 用途 |
| --- | --- |
| [中英文反防御性写作技能](research/2026-a/visuals/guidelines/anti-defensive-writing/README.md) | 结果优先的叙述与语言编辑；本仓库证据规范约束其应用 |
| [写作与章节功能蒸馏](research/2026-a/paper_review/writing_and_reasoning.md) | 章节职责与获奖论文实例 |
| [段落动作与推理连接](research/2026-a/paper_review/round2/writing_mechanics.md) | 公式、验证、修订、结论的组织 |
| [编辑工作簿](research/2026-a/paper_review/round2/editing_workbook.md) · [审稿矩阵](research/2026-a/paper_review/round2/review_matrix.csv) | 改写练习与检查 |
| [图形风格指南](research/2026-a/visuals/style_guide/STYLE_GUIDE.md) | 不同图型的结构、配色与原例 |
| [卫星与多源地图](research/2026-a/visuals/cartography/satellite/README.md) | 地理背景、产品日期、空间范围与复现 |
| [题面](research/2026-a/inputs/problem_a_2026.pdf) · [评委文章](research/2026-a/inputs/judges_commentary_2025.pdf) | 任务要求与评审论述 |

## AI agent 的最短执行流程

阅读规范 → 确认主稿及数据版本 → 写下本次要支持的判断及证据 → 编辑文字或制图 → 核对数值与最终渲染 → 简洁报告完成内容和未验证事项。

缺少支撑核心结论的数据时，将任务明确标为待验证，继续完成独立部分；不要预写冠军、编造数值或把假设写成观测。规范更新应同步入口与专项文件，避免新增一套互相冲突的规则。
