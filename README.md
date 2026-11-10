# HiMCM城市评价研究与论文材料

当前主分析：**16城×10指标，V203科学与受控扩展；当前自有论文current**。固定权重下Oslo、等权下Zurich为保守推荐，可能冠军仍为16城，没有确定冠军。112点／37部分／11全未知，25个不同补充城市—指标键。见[当前恢复入口](docs/handoff/RESUME_PROMPT.md)和[当前模型与论文验证](docs/handoff/CURRENT_MODEL_UPDATE.md)。

## 当前论文

[Overleaf](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894)只维护一份根 `main.tex` 和必需资源。标题、Summary及全部自有主题均在实际主入口。用户已要求版本历史放GitHub，后续不再向Overleaf上传多套版本稿。

- [当前LaTeX](paper/current/main.tex) · [完整PDF](paper/current/main.pdf)：27页，含25页正文参考与2页暂定AI，61引用。
- [当前资源](paper/current/)：与相邻 `HiMCM-Overleaf` 的七个编译依赖逐字节同步。
- [精简前历史](paper/history/overleaf_before_single_main_20261110/) · [归档manifest](paper/history/overleaf_before_single_main_20261110_manifest.json)：985个文件完整保存，包括队友原稿；以后使用Git提交追踪当前稿修改。

原生页眉页脚沿用用户格式。显示控制号18213仍为暂定，真实注册与完整全队AI记录尚未核实；当前不宣称完成比赛提交。服务器预览与本地编译分别验证。

## 研究入口

[主模型注册](research/2026-a/design/task4_user_current_model.json)、[扩展注册](research/2026-a/design/task4_user_current_extensions.json)、[论文注册](research/2026-a/design/task4_user_current_review.json)、[交付注册](research/2026-a/design/task4_user_current_delivery.json)指向当前证据。完整代码、原件、计算结果和历史参考保存在 `research/2026-a/` 与 `library/`；旧25城仅为冻结辅助案例。

Singapore已有26处条件场馆保持；本轮只将Oslo交通供应下界由89地铁站子集替换为626个来源定义的纯路边公交组，不相加。数据为2026登记库存，人口仍为原2025口径727797；Tveten bru因待停用疑问预防性排除，未断言关闭。112点／37部分／11未知及25个不同补充键保持。固定均宽15.9558204759降至15.8223269533，实际缩小0.133494分，累计缩小15.89%。

开始写作或制图前，阅读[AGENTS.md](AGENTS.md)、[GUIDELINES.md](GUIDELINES.md)并使用规定的反防御性写作技能。保留用户原值、权重、区间和队友内容。真实卫星及定量3D图已接入第16页，见[当前地图及验收](docs/handoff/CURRENT_SPATIAL_UPDATE.md)；V202数据采集价值已重基，持续目标见[长期计划](docs/handoff/LONGTERM_GOAL.md)。

[当前采集表](research/2026-a/design/task4_user_current_acquisition.json)的数值优先级仍计算于V202，需要以V203重基后用于下一轮，不能沿用旧Zurich优先排序。本轮626子集、原始身份／服务查询与独审见[来源记录](research/2026-a/data/current_oslo_bus_subset/observations.json)及[完整研究审查](research/2026-a/results/task4_v203_transition/verification.json)。

偏好两方案均选Oslo；固定未来三情景也均选Oslo，等权依次为Oslo、Zurich、Oslo。这些是分析者偏好与假想变化，不是调查结果或预测。主基准仍16可能／0必要冠军，VIKOR与中点评分的差异保持公开。当前单稿27页（25+2）、61引用，在线编译未核。下一步按V203重基采集价值，不重复本轮公交子集提取及未能匹配的历史来源。
