# 接手续做HiMCM：现行V130主数据／V131扩展与完整稿

长期goal active，所有新增／修改说明使用已安装指定anti-defensive-writing中英文技能。先读AGENTS.md、GUIDELINES.md、LONGTERM_GOAL.md、V131_COMPLETE_REVIEW.md、V132_RESEARCH_UPDATE.md、V133_RESEARCH_UPDATE.md及V134_RESEARCH_UPDATE.md。前一轮实际完成完整稿统一及现行入口激活，不再把V130/V131叫待迁移候选。

## 当前权威入口

- 主注册表`research/2026-a/design/task4_user_current_model.json`：V130，`task4_user_v130_revision.revised_bounds()`，16城×10指标，112点／32部分／16全缺失。扩展注册表`design/task4_user_v131_extensions.json`为active。
- 原CSV SHA仍430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c。既有值、人口、权重、锚点及矩形区间规则保持。累计20项原全缺失补充；最新Berlin100个A区metro复合体，131次线路出现去重，2026库存配原2025人口，上界1。
- fixed平均宽度16.107285572325→16.092069666942（本次0.094466%，累计14.4529%）；equal本次0.143583%。静态主序不变，Zurich保守／16可能／0必要冠军，教育优先Oslo。不是确定冠军。
- V131扩展总审`results/task4_v131_revision/audit.json`，真实旧新配对`paired_comparison.json`。9偏好MC、16确定性未来、3232扫描／32阈值、12shock MC、16weight MC、4方法及6份冻结历史案例通过。equal方法tau.6500、fixed.5000；中点／区间tau.583333/.6500；Berlin假设成本阈值38.0835%。频率为声明分布下条件结果，不是调查／预测／实际胜率。
- 完整独立稿`/data/projects/HiMCM-Overleaf/drafts/task4_v131_paper.tex/.pdf`：20页=18主文参考+2暂定AI页；新闻14–15，参考16–18，AI19–20。文档修订V134，PDF145443字节，SHA8d5d7f1079023430a77c6e39a522b1653bc48750f62c7e676f33c709c9981dd7。零编译警告、全20页渲染已核，新图字最终≥12.51pt。旧V128及更早稿保留。

## 环境、复现与冻结

root账户；研究/data/projects/HiMCM，论文相邻HiMCM-Overleaf。Python用`.venv-v120/bin/python`（3.11、numpy1.26、pandas2.3、scipy1.13）；tectonic0.17、Poppler。大原件放/data/datasets，临时/data/scratch。不要从零重建环境或误用legacy25主入口。

V130原`revision_audit.json`及`design/task4_user_v130_snapshot.json`是启用前科学冻结证据，不覆盖。现在复核用`scripts/audit_task4_v130_post_activation.py`，另写`post_activation_audit.json`，核原registry的Git cb2b121字节并保护当前registry；16静态／24组各10000同流MC及撤回通过。原`scripts/audit_task4_v130_revision.py`属于启用前历史context，不能直接拿其V127 registry快照断言当前。

V131全部55份科学输出已绑定，旧V128的55份保持。已通过的全量数学检查无新风险不重复。论文builder `drafts/build_task4_v131.py --research-root /data/projects/HiMCM/research/2026-a`校验主快照及扩展全部哈希，再生成表图／宏。编译捕获stdout/stderr，checker需`--compiler-output LOG`；全页实际查看后才加`--render-review-confirmed`。只改叙述/来源索引用`--refresh-manifest-only`，新PDF按PDF技能先标记artifact operation，每轮一次。

权重八项.1125、transport/pool各.05；收益x/(a+x)、成本a/(a+x)，锚点2/15/100/10/15/1/50/travel30/100/1。旅行exp(-t/30)，均值只Jensen界；分箱端点与未知质量／开放尾按既有规则。加权距离权重只乘一次，自排除竞争上界，minimax regret保守推荐；完整未知[0,1]，库存子集只提高下界。不要编造AHP调查、精确14vs18偏好、未来经验趋势或个人可达性。

## 协作、真实信息与下一阶段

GitHub仅研究、Overleaf仅论文及选定资产。队友main/ref/class保持，根main缺原framework.png历史问题未修；独立稿可编译。无连接文档会话，使用fetch后Git镜像并核push，不把它称实时浏览器视图。旧源包被准入表固定哈希，不在原包覆盖解释／获取状态，新证据另版本。

AI当前局部选集66条=4真实请求+53进度+9完整可见答复，13根turn标签gpt-6.1-sol，客户端0.166.0-alpha.5.1，截止2026-11-08 19:10:12UTC。原文仅仓库外私存，工具载荷／代码／附件／subagent及其他队员史不覆盖；不是完整团队AI报告。实际控制号仍PENDING，旧18213/18214冲突不猜；完整AI史和具体队友主稿整合需真实信息／授权。

GitHub PUBLIC发布选择仍待答，研究本地commit、暂缓新增公开push，不擅改可见性；Overleaf按授权同步，先fetch审diff不force。V132已完成现行V130的16缺失格采集诊断（旧V129仍冻结V127的17格），剩余单格主要信息值保持。下一阶段优先真正新匹配师资，Warsaw2025波次概要已确认但尚缺高中单程旅时原表；优先新匹配Dublin/Zurich教师FTE及Warsaw真实高中单程通学，失败跳过。V129 Paris/Madrid/Amsterdam拒收不重复；Vienna2001只历史案例、不移作当前。继续论文交付核对及可证实的改进，不因本轮完成结束长期goal。

V133新证据：Zurich SSP原件确认公私立全州调查覆盖，未取得同城同高中教学FTE／学生公开汇总；芬兰OPH称专项采集资料最新2019，另列就业职业报告，下一次必须核其学校所在地／居住地、学段／FTE口径，不据职业名填PTR。两条0准入，不重复旧公开全州财政支持图。当前readiness脚本核完整稿20页／实际PENDING页眉／旧新各55科学输出／保护文件，最后提交仍未完成；详见results/task4_v133_readiness。

V134仅改当前owned V131数据章及引用：Paris Henri-IV真实UAI／2025的794学生与153.65机构ETP，2026目录post-bac只是范围提示；比率仍不准入。新PDF20页已全页渲染／零warning复核，所有旧数值资产和宏与Git dbffa4e逐字节保持。旧V131/V133文档回执是旧PDF的历史捕获，当前以results/task4_v134_documentation与Overleaf qa.documentation_revision=V134为准。文件名仍V131，因为科学版本未改；不新建整套重复论文。
