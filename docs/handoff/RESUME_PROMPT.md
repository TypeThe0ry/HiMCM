# 接手续做HiMCM：现行V136主数据／V137扩展与完整稿

长期goal active；所有新增／修改说明必须使用已安装指定anti-defensive-writing中英文技能。先读AGENTS.md、GUIDELINES.md、LONGTERM_GOAL.md及[V137完整稿与启用记录](V137_COMPLETE_REVIEW.md)、[V140当前交付核对](V140_RESEARCH_UPDATE.md)。完整稿已迁移、当前入口已启用，不再把V136/V137叫待迁移候选。

## 当前权威入口

- `research/2026-a/design/task4_user_current_model.json`：V136，`task4_user_v136_revision.revised_bounds()`，16城×10指标，112点／33部分／15全缺失。扩展索引`design/task4_user_v137_extensions.json` active。
- 原CSV SHA仍`430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`。保留已有值、人口、权重、锚点及矩形规则。累计21项补充；最新London59个原生站／hub实体，November2026 TfL库存配原2025人口9122909，只提高原全未知交通下界至.012769306569299622，上界1。
- fixed平均宽度16.092069666942→16.089333559066，本次收窄0.017003%，相对原表累计14.4675%；equal本次0.027035%。所有静态排名保持，Zurich保守／16可能／0必要冠军，教育优先Oslo。基准k100 London均rank13.7863→13.7607，推荐频率不变；不是确定冠军或真实胜率。
- V137扩展独立总审`results/task4_v137_revision/audit.json`固定55输出；实际V131→V137八类配对在同目录。9偏好MC、16确定性未来、3232扫描／32阈值、12shock MC、16weight MC、4方法及6份历史CSV保持检查通过。equal方法tau .633333、fixed .5000；中点／区间tau .583333/.6500；Berlin假设成本阈值38.0835%保持。频率与情景不是调查／经验预测。
- 完整独立稿`/data/projects/HiMCM-Overleaf/drafts/task4_v137_paper.tex/.pdf`：22页=20主文参考+2暂定AI；新闻15–16，参考17–20，AI21–22。文档修订V140，PDF148545字节，SHA`bc48b20359d13dcbcfff9a2f0448e68e8eef4659d770cfae51a187a8390009f8`。零warning，最终22页95dpi渲染、六张总览及单独图页实际检查完成，图字最终≥12.51pt。旧V131（文档V134）及更早稿冻结，74份旧稿／资产对照Git eacb1fb核字节。

## 环境与复现

root账户；研究`/data/projects/HiMCM`，论文相邻`HiMCM-Overleaf`。Python `.venv-v120/bin/python`（3.11、numpy1.26、pandas2.3、scipy1.13），tectonic0.17、Poppler；大原件/data/datasets，临时/data/scratch。不要重建环境或误用旧25城主模型。

V136原`revision_audit.json`和`design/task4_user_v136_snapshot.json`冻结；`scripts/audit_task4_v136_revision.py`以固定V130 factory为before，支持live入口推进后重放，另写`recheck_audit.json`，原审计不覆盖。启用后16静态／24组各10000同流MC及撤回已再次通过，无新风险不要重复全量数值检查。

V137 builder `HiMCM-Overleaf/drafts/build_task4_v137.py --research-root /data/projects/HiMCM/research/2026-a`先核主快照10项及55扩展哈希再生成表图／宏。编译须捕获stdout/stderr，checker加`--compiler-output LOG`，实际检查全部渲染后才能加`--render-review-confirmed`。只改叙述或来源索引用`--refresh-manifest-only`。新PDF按PDF技能在每轮首次authoring前执行一次marker。V137初始交付回执`scripts/audit_task4_v137_delivery.py`及`results/task4_v137_delivery_audit/`冻结原PDF；当前交付核验用`scripts/task4_v140_readiness.py`及results/task4_v140_readiness，核139科学文件、37原资产／宏／其他章节、74旧稿与当前PDF／编译／QA。V140相对V139仅AI21／22页变，20主文参考页像素相同；30项技术／内容／有限案例／待核事项分别列出，final_submission_ready=false，不重写历史回执。未跟踪aux/log不再纳入新manifest的可恢复保护清单。

权重八项.1125、transport/pool各.05；收益x/(a+x)、成本a/(a+x)，锚点2/15/100/10/15/1/50/travel30/100/1。旅行exp(-t/30)，均值只Jensen界；分箱端点、未知质量和开放尾按原规则。加权距离权重只乘一次，自排除竞争上界，minimax regret保守推荐。矩形不是采样CI，库存子集只提高下界。不编造AHP调查、精确14vs18偏好、经验未来趋势或个体可达性。

## 来源与权限

London V135源包已被V136准入哈希冻结，不改原capture／README／candidate audit记录新状态。TfL1751混合对象→272站级→62严格Zone1→省Monument与同名EdgwareRoad一项→60ID按Paddington共享hub合并59实体；省略后者是保守同名处理，不声称确为同一付费复合体。全部代表点通过ONS2025 BFC全分辨率coastline-clipped边界，Thames岸线距离不当行政外界距。16.2MB原件的399962字节lossless gzip已入研究Git，缺外置原件也可复算。论文三份源副本保留V135候选状态，正式准入看V136表。

Paris Henri-IV同UAI2025的794学生与153.65机构FTE，缺学段工作量；2026目录post-bac仅范围提示，0准入。Dublin公开学校roll FTE仍缺，Zurich SSP全州公私覆盖不等于城市同学段汇总；芬兰2019专项教师采集与其他职业就业报告不混用。Warsaw2025概要是6+全龄都会区／全天出行，不能当高中单程通学；202空响应／超时与provider表示分开归档。失败跳过。

GitHub仅研究，Overleaf仅论文及选定资产。修改前fetch，先审确切diff，正常main提交，不force。GitHub PUBLIC发布选择仍待答，研究本地commit，暂缓新增公开push，不擅改可见性；Overleaf按既有授权同步。当前无连接文档session，使用已fetch Git镜像，不称实时浏览器视图。队友main/ref/class和项目主文件设置保持，根main历史缺framework.png问题未修。

实际控制号仍PENDING，旧18213/18214冲突不猜。AI报告局部125条=4真实请求+99进度+22完整可见答复，28根turn标签gpt-6.1-sol，CLI0.166.0-alpha.5.1，截止2026-11-09 03:17:15UTC。源data/task4_v140_ai_provenance，原V12966条与V12652条保留；重放不扩大截止，原verification保留，后续另写recheck。私有原文不入仓库，不覆盖其他队员／subagent／工具载荷等，不称完整团队AI报告。最终整合队友正文须具体授权；真实控制号、完整AI史及正式提交回执仍待资料。

## 下一项

V138已按V136的15格完成当前采集诊断，3373核对／140文件保护通过；V132旧16格冻结。剩余30单格行的信息价值保持，Dublin／Zurich匹配教师FTE仍优先。详见[V138交接](V138_RESEARCH_UPDATE.md)。Warsaw2022原报告从旧V121超时恢复为完整141页及3.6MB lossless gzip；城市学校样本基数22、公布均27分钟，但缺高中／14–18分母，0准入，不再重复试填。下一轮只查真正新匹配教师或高中旅时源；失败跳过。V139已将Warsaw恢复来源与学段不匹配理由写入数据章、补官方引用，科学结果不变，当前AI附录已按V140更新至125条局部选集，PDF以本页V140字节为准。继续论文材料及真实交付信息核对，长期goal不因单轮完成结束。

V141新来源复核见[V141交接](V141_RESEARCH_UPDATE.md)：Tokyo2024年鉴原表实为2021全周日均工作／学校合并62分钟，不可除二得高中单程；Tokyo-to与用户city proper地域未匹配。Vienna ÖROK2024/2023模型8.2分钟为最近ISCED3目标潜在可达性，非实际通学，不导出Jensen界。3份完整官方响应／七页原文／两图页审计通过，67科学与11稿件入口保持，0准入。47MB原PDF在/data/datasets/HiMCM/source_archives/task4_v141_travel/oerok_original.pdf，新clone需另取得，不从选页重构。主V136／扩展与完整稿V137文档V140及125条AI选集保持；下一步仅新匹配教师／高中实际旅时或有细分空间权重的潜在访问案例，不反复试填已判不匹配数据。
