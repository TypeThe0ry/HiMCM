# V193：V192科学、论文与交付统一启用

两城真实车站子集已完成全套扩展及论文一致性迁移，当前科学／扩展V192、自有稿V193、交付V193统一启用。旧V181科学、V189稿和V190定位清单冻结；不能再把V191候选或V192隔离研究当待执行阶段。

当前16城×10指标有25个累计补充，112点／37部分／11全未知（8师资、3旅时）。原权重平均区间宽度16.0493847924→16.0390700744，等权18.8379407431→18.8188134495；相对原输入的固定宽度累计收窄14.73465766%。原CSV、权重、人口、锚点和规则保持。Zurich仍为保守推荐，16可能／0必要；原权重Warsaw由12到11、Vienna由11到12。教育优先Kendall τ更新为0.716667，区间／中点固定τ为0.6，均秩证书4260明确／180未区分。

自有稿从V189衔接，保留其联合均值段、凶杀率／来源撤回诊断、公平性／成长阶段、原参考文献及AI范围。新增Tokyo目录38站、Warsaw21＋18合并38复合体的采集说明及3个引用，全部原53引用保留。Amsterdam说明压缩但39→35→32、100米名义筛选、两版市界、无精度保证和库存日未知等条件保持。Tokyo目录更新日未当库存观测日；Warsaw2026目录／2024地图／2025市域佐证分开。AI仅校验段两处科学版本改为V192，不扩写冻结选集或声称完整全队记录。

最终27页＝25正文参考＋2暂定AI，56引用，新闻18—19／AI26—27；0overfull、2条既有underfull。原生Letter／Palatino／12pt正文／11pt页眉／空页脚，显示暂用18213且实际注册仍未核。矩阵6.5英寸插入最小10pt、分数图12.5969pt；27页总览及7个关键页完整渲染实看，另12页与V189像素相同。独审核327科学绑定、816旧论文文件保持（3导航更新）、58限定范围锚点、47项状态及13项待办保持。

独立重建的首轮两个TeX入口均成功，但runner把两个入口的警告计数数组当整数，触发检查失败；原报告保存在`reproduction_initial_failure.json`。修复类型读取并测试整数／数组和异常输入后，使用新的空输出目录完整重建通过：160格／32案例、327绑定、两个27页入口逐页文字及72dpi灰度像素一致。没有修改论文来绕过该检查。该回执依赖本地工具和既有TeX缓存，不代表服务器编译、冷环境或比赛收件。

## 当前入口与验证

- 主注册表：`design/task4_user_current_model.json`，模块`task4_user_v192_revision`，工厂`revised_bounds()`；快照`design/task4_user_v192_snapshot.json`的327项均不可变，当前导航另行核对。
- 扩展：`design/task4_user_current_extensions.json`，`scripts/task4_v192_extensions.py preferences|future|method|diagnostics`。
- 自有稿：双仓当前review注册表一致，`drafts/task4_v193_paper.tex/.pdf`，根代理`task4_v193_review_entry.tex`。
- 交付：双仓当前delivery注册表一致，`results/task4_v193_review/requirements.csv`及`delivery_verification.json`。
- 论文审计：`scripts/audit_task4_v193.py --expect-active`；`results/task4_v193_review/verification.json`、`visual_review.json`、`activation.json`、`reproduction.json`、`sync.json`。
- 当前复现：`.venv-v120/bin/python research/2026-a/scripts/task4_v193_reproduce.py --output-dir /data/scratch/新的空目录`。环境名v120是既有Python环境，不是模型入口；runner只允许V192/V193及匹配双仓导航。

共享入口已实际只读重编，仍在main.tex第143行缺framework.png处停止；此前有破折号字形／headheight等警告，未越权修队友文件。记录shared_build_check.json及原日志shared_main.log。队友main.tex／ref.bib／mcmthesis.cls及默认Main保持。47项交付映射仍有13实质待办：真实注册、全队AI记录、最终共享稿选择／整合／构建和正式提交回执等仍需要实际证据，submission_ready=false。

下一轮优先将V183的48不确定格采集价值表重基到当前V192（96行、仍含37部分，不能删掉已得下界的Tokyo/Warsaw）。其后只追新同口径高价值来源，跳过已失败路线；原表Zurich凶杀率及工作代理的抄录链尚未完整核实，保留条件性和撤回诊断。不重复V192研究迁移、V193入稿或既有联合证明。长期goal active。
