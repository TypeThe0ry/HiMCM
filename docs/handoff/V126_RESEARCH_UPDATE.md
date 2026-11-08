# V126：论文追溯修复与当前缺项优先级

科学基准保持**16城×10指标V124**，V125偏好／未来／方法／受控修订结果保留；本轮没有新增准入数据。原CSV、权重、锚点、160格界与已有数值论文资产均未改。Zurich仍是基准保守推荐，16城仍可能冠军；教育优先推荐Oslo。长期goal保持active，所有新增文字使用指定中英文anti-defensive-writing技能。

## 实际改善

- **AI披露从未知标签推进到真实记录。** 一个明确任务的本地日志前缀记录Codex Desktop客户端`0.166.0-alpha.5.1`、十条`gpt-6.1-sol`模型标识。52条真实可见消息逐条独立核对，通过前缀／行／导出哈希与原文字段核验。只提交元数据清单；原文在仓库外，未公开。标识不等于不可变服务build，也不证明所有并发agent模型／全队历史。Exa实际读取与提取已有回执，内部模型及服务版本未记录。
- **同国案例引用闭合。** 四城Numbeo2025成本／房价收入比、Mumbai/Delhi的WHO2021空气均值共十项输入，逐项与冻结V117 utility一致；论文加了冻结案例与提供方引用。没有重算或改变历史案例，更没有将25城入口混回主模型。
- **补数诊断使用当前19个全缺失格。** 旧V124_priority实际基于V121的21格。新诊断删除已补Madrid交通与Tokyo泳池，保留141格已有信息，完成38组单格信息价值和2741次独立分数／遗憾／冠军核对。Dublin、Zurich PTR的条件信息价值最高；“保证改善”只在完整精确识别utility的假设下成立，不能套在清单下界或旅行均值Jensen界上。
- **完整交付按证据逐项检查。** 34项要求区分已证明、未完成、证据不足。已有公平／历史年龄案例不冒充精确14vs18实测或个体可达性；未完成项未被重新定义成已完成。

## 入口与验证

- [AI元数据包](../../research/2026-a/data/task4_v126_ai_provenance/README.md)、[Exa使用证据](../research/task4_v126_ai_tool_evidence.md)。原可见消息只在`/data/scratch/himcm_v126_ai_provenance/visible_records.jsonl`，不能自动当完整提交记录。
- [同国来源索引](../../research/2026-a/data/task4_v126_country_sources/README.md)，脚本`extract.py`检查十项冻结输入。
- [当前19格采集诊断](../../research/2026-a/results/task4_v126_priority/README.md)，脚本`research/2026-a/scripts/task4_v126_priority.py`，无MC或随机缺失值填充。
- [文档验收收据](../../research/2026-a/results/task4_v126_delivery_audit/README.md)保存当前QA及无警告编译输出，哈希对应。
- [完整要求核对](../research/task4_v126_requirements_audit.md)末尾记录最终PDF字节／SHA，早期快照保留历史标签。

Overleaf当前仍用`drafts/task4_v125_paper.tex/.pdf`，这是**V126文档修订，科学版本V124/V125**。20页＝18主文（含摘要、目录、两页新闻、参考）＋2暂定AI页；新闻14–15、参考16–18、AI19–20。最终PDF SHA-256 `84ba59b8fd1bf8bd2d85335067380b280258d8c4a9e9ce4bdb4769361620bf32`，137456字节。20页总览及变化页细读通过，12pt正文及最终图12.51pt保留。TeX日志和编译stdout/stderr均无警告；新拒绝门的定向负例确认能拦截PDF后端警告。既有成功数值审计未无故重复。

独立稿已提交并推送Overleaf `bff8644`，fetch后HEAD与origin/main一致且工作区干净；研究改动按审diff后本地提交。共享`main.tex/ref.bib/mcmthesis.cls`及旧独立稿hash保护通过；共享main实际编译仍在143行缺`framework.png`，未擅改队友正文。没有连接的文档控制会话，使用fetch后的Git工作区，并分别验证远端同步。

## 下一轮及待真实信息

按新诊断做有界采集：优先真正新匹配的城市／学段／提供方教师分母；已明确不公开或尺度不符的旧路线跳过。官方Prague2025运营方年报、London NaPTAN当前产品可检查原件及站点层级，别把站台／access points直接当站点。Vienna已有2001历史通学报告须先离线核资格、分母和分箱；如可用，只能作明确历史代理与撤回臂，且原件禁止网上再分发，不提交Git。

真实控制号、完整团队AI工具与输入／输出、共享主稿具体整合授权／最终稿选择、正式报名和提交回执仍待真实资料。GitHub再次确认PUBLIC且origin没有新提交；赛期发布选择未收到答复，仍暂缓新增公开push，不改变仓库可见性。Overleaf保持已授权同步。不能以本轮完成将长期goal标完成。
