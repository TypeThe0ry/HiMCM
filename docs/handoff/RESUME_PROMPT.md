# 接手续做 HiMCM：当前权威状态

长期goal **active**：持续优化论文及论文材料。所有新增／修改叙述必须使用已安装的 [anti-defensive-writing-Skill](../guidelines/ANTI_DEFENSIVE_WRITING.md)。先读 [AGENTS.md](../../AGENTS.md)、[GUIDELINES.md](../../GUIDELINES.md)、[长期计划](LONGTERM_GOAL.md)和[V129交接](V129_RESEARCH_UPDATE.md)。V128完整稿与主V127继续冻结不变。

## 当前入口与结论

**主分析是16城×10指标V127；扩展与完整独立稿为V128。旧25城入口只作独立历史案例，不用于当前主榜。**

- 主注册表：`research/2026-a/design/task4_user_current_model.json`，应指向`task4_user_v127_revision.revised_bounds()`。
- 主结果：[V127](../../research/2026-a/results/task4_user_v127_revision/README.md)，112点／31部分／17全缺失。原CSV SHA `430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`。
- 原表已有值、人口、权重、锚点与区间规则全部保留。最近只补Vienna交通99个公共地铁站区、Prague交通57个市内复合体；141格已有信息不变。
- 固定平均得分宽度16.150020917288→16.107285572325，收窄0.264615%；Vienna名次12→11、Warsaw11→12。等权顺序不变。
- **Zurich仍为保守推荐，16城仍可能冠军，无必要冠军。** 教育优先改推荐Oslo，不是确定冠军或实测学生偏好。
- 扩展入口：[V128总审](../../research/2026-a/results/task4_v128_revision/README.md)、`design/task4_user_v128_extensions.json`。教育tau .716667、方法equal tau .666667、修订fixed tau .583333；不能沿用旧.700/.750/.600。教育k100 Prague条件推荐频率5.34%→8.71%，不是实际胜率。
- Overleaf当前完整独立稿：`/data/projects/HiMCM-Overleaf/drafts/task4_v128_paper.tex/.pdf`，20页＝18主文＋2暂定AI页。V125及更旧稿保留各自冻结证据，不覆盖。
- V129支持材料已同步Overleaf`9a4b259`；当前17缺失格诊断及Berlin100站源审查完成，0格正式准入。131次A区线路出现去重100站，不是初步误加的141；候选效用[.0512744653,1]，若启用fixed平均宽度预计再窄0.0945%，Zurich/16可能不变。候选与已启用结果分开。

## 环境与复现

工作区为`/data/projects/HiMCM`，论文为相邻`HiMCM-Overleaf`；使用root账户。已有环境：`.venv-v120/bin/python`，Python3.11.18、numpy1.26.4、pandas2.3.1、scipy1.13.1；图表另用matplotlib3.9.2，PDF提取需Poppler，编译用tectonic0.17.0。

先检查两个Git工作区并fetch各自origin，不覆盖用户/线上变更。不要为复核从零重建环境或改原CSV。必要复现命令：

```bash
.venv-v120/bin/python research/2026-a/scripts/task4_user_v127_revision.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v127_revision.py
.venv-v120/bin/python research/2026-a/scripts/audit_task4_v128_extensions.py
```

新主审计在注册表V127下另写`post_activation_audit.json`，不覆盖原启用前审计和`design/task4_user_v127_snapshot.json`。已通过的全量数学检查不重复运行，除非新变更、失败或未解决风险需要。

论文新建/数值改动的构建（在Overleaf根目录，激活上述环境）：

```bash
python drafts/build_task4_v128.py --research-root /data/projects/HiMCM/research/2026-a
tectonic --keep-logs --keep-intermediates drafts/task4_v128_paper.tex > /data/scratch/himcm-v128-build.log 2>&1
python drafts/check_task4_v128.py --compiler-output /data/scratch/himcm-v128-build.log
```

只改叙述/元数据时，builder可加`--refresh-manifest-only`；必须检查最终渲染，再用`--render-review-confirmed`记录实际检查。捕获stdout/stderr以检查PDF后端警告，不能只看TeX日志。

## 数学及数据边界

八个主指标权重各.1125，交通与泳池各.05；等权各.1。收益效用`x/(a+x)`、成本效用`a/(a+x)`；锚点依次2、15、100、10、15、1、50、旅行30分钟、100、1。旅行效用`exp(-t/30)`；均值只给Jensen界，分箱用端点与未知质量，不取中点或给开放尾段造上限。

`S(u)=100*sqrt(sum(w*u²))/(sqrt(sum(w*u²))+sqrt(sum(w*(1-u)²)))`，权重只乘一次。`L=S(lo), U=S(hi)`；`R_i=max(0,max_{k!=i}U_k-L_i)`，按最小最大遗憾保守推荐。可能冠军满足`U_i>=max_{k!=i}L_k`。矩形区间是条件数据界，不是置信区间。

- 清单子集只给下界，上界保留1；模式份额不替代物理设施密度。
- Vienna1695个广义对象计数已拒收，其中车库/非乘客资格未证；只计经既有站层逐项核实的99metro站区。Prague61线路出现与58登记复合体不同，当前57名单按2026闭站处理，不混成2025运营数。
- Vienna2001通学只历史派生案例，不能迁移为当前旅行值；官方编辑/估补误差另明示。其原PDF限制再分发，保留仓库外。
- 教育新查Dublin提问及Amsterdam多campus机构数据，0准入；旧已拒收的公共/区域/混学段分母不重复替代。
- 不编造AHP调查、精确14vs18需求、时间趋势或真实夺冠概率。历史同国、区级公平、宽年龄案例始终与主16城和个人可达性分开。

## 权限、AI与同步

GitHub保存研究材料；Overleaf保存论文、LaTeX与选定资产。保留队友`main.tex/ref.bib/mcmthesis.cls`；没有具体授权不修改/替换正文，不自动更改项目主文件。共享main仍在143行缺`framework.png`，独立稿可编译。无连接文档会话时，只报告fetch后的Git镜像与实际push状态。

论文头`Team Control PENDING`，真实号码仍待确认；全队AI史仍未完整。V129把同任务私有可见选集52→66条，13个根turn模型标签已核验，截止2026-11-08 19:10:12UTC；原V126前缀及52条清单保持。V128稿继续准确声明旧17:26UTC范围，新记录另附支持材料。原文在仓库外，不自动公开，也不冒称完整AI披露。Exa提取表示与原始HTTP分开，未猜底层模型版本。

当前GitHub仍PUBLIC，赛期公开发布选择未收到答复，暂缓新增公开push，不擅改可见性；本地commit正常，Overleaf按授权同步。push前重新核实际可见性、fetch并审diff，不能force。不要提交凭据、环境、缓存或56.6MB外部年报。

## 下一轮

V129已按V127的17个全缺失格更新诊断；旧V126 priority仍固定V124的19格。优先把已通过独立源审查的Berlin100站候选做成下一套受控准入：保留原CSV和143个已有信息格，上界1；做单独准入／撤回、主模型MC及所有偏好／未来／方法扩展，再统一新完整稿后激活。候选包尚未被正式准入表冻结，采用时固定源哈希；不改旧V127/V128产物。继续真正新匹配的Dublin／Zurich教师分母与Warsaw真实高中通学；V129 Paris／Madrid师资和Amsterdam交通均0准入，不重复已失败口径。并行agent因服务配额终止，父级已接手最终核验；重用前先确认工具实际可用，不把旧运行意图当live进程。控制号、完整团队AI史、队友稿具体整合授权及发布选择需要真实信息；单轮完成不把长期goal标完成。

历史恢复过程与旧版本结果见V120–V126各交接文件；本页当前入口优先，旧“当时最新”状态不覆盖本页。
