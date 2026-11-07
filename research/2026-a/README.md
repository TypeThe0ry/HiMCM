# 2026 HiMCM A：研究工作台

> **团队成员与 AI agent 必读：开始写作或制图前，必须阅读并遵循[统一 Guidelines](../../GUIDELINES.md)。论文文字、图表、图注与研究结论均按专项规范执行，交付前核验。AI agents: read and follow these guidelines before editing.**

最新论文蒸馏已细化到13篇重点正文选段与36张证据卡，附同题O/F案例比较、段落编辑工作簿和18项审稿矩阵：[第二轮入口](paper_review/round2/README.md)。本轮不改动Overleaf正文。

> 新增资料：已接收[五指标简化稿](inputs/team/indicator_sources_5_original.md)，与11指标原稿并存，尚未替换最终方案。见[接收与待确认事项](design/simplified_indicators_intake.md)。截图中的四位成员生活城市目前仅明确上海，另外三座待补充。

> 2026-11-07更新：当前已完成25城真实数据分析及V5/V6的10指标证据区间模型。数据位置、结果和复现命令见[仓库README](../../README.md)，详细结论见[V6报告](results/task4_v6/REPORT.md)。下文18城/12指标等内容保留为早期研究背景；当前研究在main维护，GitHub按最新用户授权同步。

新增入口：[25城规范表](data/city_candidates_team_25.csv) · [原始指标稿](inputs/team/indicator_sources_11_original.md) · [原件来源记录](inputs/team/provenance.json)。

日期：2026-11-07。范围：**全球城市**。已产生真实数据上的条件分析与决策排序；V6有107/250个有信息单元，仍有25个可能冠军，未识别唯一真实冠军。论文状态以最新Overleaf为准。

## 当前判断

建议的研究问题是：**哪座城市让普通高中生在日常时间与预算内，真正享有学习、安全出行、健康环境和课外成长的机会，而且这种判断对不同偏好仍然可信？**

最值得打磨的主线是「实际可用的机会 + 城市内部差异 + 不确定性下的排名」。先完成简单、透明的基准，再用有证据的失败案例推动一次重大修订。个人偏好分析是对结论适用范围的解释，最后仍需给出题目要求的城市排序和有条件的首选。

本阶段产物：

1. [获奖论文的写作、逻辑与结构蒸馏](paper_review/writing_and_reasoning.md)
2. [A题研究设计与数学框架](design/research_design.md)
3. [大胆创新清单与取舍](design/innovation_routes.md)
4. [全球数据可行性与口径](data/data_feasibility.md)
5. [执行与交接记录](logs/research_handoff.md)

另有68篇文本特征审计CSV、12篇重点论文的阅读依据、候选城市表和来源登记表。审计中的关键词命中不代表论文质量，也不能解释获奖因果。

## Git与研究边界

早期研究曾使用本地分支`research/2026-a-local`；当前已合并到`main`。用户最新指令明确授权立即提交并推送研究数据、模型和结果，旧的赛后推送约定不再阻止此次同步。历史论文库及既有Release保持原样。

官方2026赛期的停止修改时间换算为新加坡时间 **2026-11-18 09:00**，提交截止 **10:00**。本地旧日期钩子曾按提交时间设置，不会自动发布；本次明确授权推送可单次跳过该钩子，赛期说明不因此改变。日期来源：[COMAP官方说明](https://www.contest.comap.com/highschool/contests/himcm/instructions.html)。

题目要求1—2页非技术新闻稿、至少10座城市、至少一次重大修订，主报告最多25页；AI报告另附。原始题目见[inputs/problem_a_2026.pdf](inputs/problem_a_2026.pdf)。AI辅助用途和本轮产出索引见工作记录，最终AI报告仍需由队伍核对并保存完整对话。
