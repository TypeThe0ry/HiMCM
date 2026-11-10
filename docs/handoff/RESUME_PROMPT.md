# HiMCM 当前恢复入口

长期目标保持 **active**。先读 [AGENTS.md](../../AGENTS.md)、[GUIDELINES.md](../../GUIDELINES.md) 和 [持续工作计划](LONGTERM_GOAL.md)。新增或修改文字必须读取对应语言的 anti-defensive-writing 技能；简单子任务默认 Luna，复杂建模及独立科学审查用 Terra6.1。历史入口按需追溯，不从零重建。

## 当前工作区和权威入口

- 研究仓库：`/data/projects/HiMCM`，远程 `TypeThe0ry/HiMCM`，使用 `main`。
- 论文仓库：`/data/projects/HiMCM-Overleaf`，跟踪 [Overleaf 项目](https://www.overleaf.com/project/6aeec16f3ea7a24e3d91e894)。其最新 `main.tex` 为论文权威入口；只有同一份当前 main 和必要资源，版本由 Git 管理。
- GitHub 的 `paper/current/` 镜像七个编译依赖及当前 PDF；完整研究数据和历史材料保留在 GitHub，不整树上传 Overleaf。
- 队友持续编辑。每轮论文工作前、提交前分别 fetch；先检查本地改动，干净时才 fast-forward。已有修改不得自动 stash、reset 或覆盖。保护 Git 状态的审计运行期间不 pull、编辑或提交。
- 队友的新正文必须保留。研究结果不自动授权改稿；按实际修订文档和具体范围修改，提交前审 exact diff。Git 同步不代表服务器编译或在线预览已验证。

| 事项 | 当前入口（均在研究仓库） |
| --- | --- |
| 主分析 | [主模型登记](../../research/2026-a/design/task4_user_current_model.json)；`task4_user_v203_revision.revised_bounds()` |
| 科学冻结证据 | [V203 快照](../../research/2026-a/design/task4_user_v203_snapshot.json)；548 个绑定，继承 V202 的 476 个 |
| 扩展与受控诊断 | [扩展登记](../../research/2026-a/design/task4_user_current_extensions.json) |
| 采集及来源跟进 | [采集登记](../../research/2026-a/design/task4_user_current_acquisition.json)、[已核查路线](../../research/2026-a/design/task4_current_source_routes.csv) |
| 当前论文与交付 | [审阅登记](../../research/2026-a/design/task4_user_current_review.json)、[交付登记](../../research/2026-a/design/task4_user_current_delivery.json) |
| 文件绑定检查 | [当前完整性合同](../../research/2026-a/design/task4_current_research_integrity.json)；报告数随明确登记更新 |

## 必须保留的科学状态

主分析是 **16 城 × 10 指标、V203**：112 个点值、37 个部分区间、11 个完全未知，25 个不同补充键。原始 [用户 CSV](../../research/2026-a/data/task4_v117_team_intake/city_indicators.csv) 的 SHA256 为 `430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`；数值、年份、标记、人口、权重、锚点和区间规则保持。

固定权重的保守选择为 **Oslo**，等权为 **Zurich**，仍有 **16 个可能冠军、0 个必要冠军**。固定权重为八项各 0.1125，交通／泳池各 0.05；等权各 0.1。TOPSIS 距离权重只乘一次，最大遗憾比较排除自身。保守选择不写成确定冠军，AHP 偏好不是学生调查，MC 条件频率不是现实夺冠概率，未来情景不是拟合趋势。

V203 相对 V202 只将 Oslo 交通下界从原来的 89 个地铁站子集，替换为 626 个来源定义的单模式公交组；其余 159 个下界和全部上界保持。该数不与 89 相加、不代表全部公共交通；撤回及 624／625／623／627 检查见 [当前模型说明](CURRENT_MODEL_UPDATE.md)。当前工厂的历史依赖正常保留；不要将旧 25 城运行入口当成主分析。

## 恢复和验证

从研究仓库运行。优先使用 [锁定环境说明](../../research/2026-a/environment/current-check/README.md)；本机已验证解释器是 `/data/scratch/himcm-current-check-env/bin/python`。不要用普通系统 Python 或不匹配的 `.venv` 运行模型；`.venv-v120` 是仍保留的旧兼容环境，不是唯一恢复要求。

完整复现需要干净、已同步的论文 Git HEAD，以及位于两个仓库之外的**新空输出目录**。例如，确认目录不存在后运行：

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python -s research/2026-a/scripts/task4_current_reproduce.py --output-dir /data/scratch/himcm-restore-check-new
```

仅检查当前研究登记和文件绑定，可运行：

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/audit_current_research_bindings.py
```

检查默认打印 JSON；保存或覆盖报告须显式指定。复现器校验当前登记、各报告的直接来源映射，并在结束时检查输入未变；上游历史报告按已声明边界保留。历史路线索引通过 Git 提交 `4baa23ec09bb15bc3eae5ef17f952ec17f6d9921` 校验，当前索引另行绑定，因此本地需有对应 Git 历史。Tectonic 使用已有缓存，不能据此声称全新机器或线上编译通过。详见 [复现覆盖说明](CURRENT_RESEARCH_INTEGRITY_UPDATE.md)。

## 论文及待交付事项

当前已核稿为 **27 页 = 25 页正文／参考文献 + 2 页暂定 AI 报告，63 条引用**。使用原 mcmthesis 类，原生 Summary Sheet、Team #／Page x of y 页眉及空页脚；18213 为用户允许的暂用控制号，真实注册号未核实。原类、参考库和队友原稿均保留。最近验证针对论文提交 `1cbec98`；每次仍须重新检查远程，不把该提交固定成永远最新。

[48 项交付清单](../../research/2026-a/results/current_paper_review/requirements.csv) 仍有 12 项待办：完整团队 AI 披露／记录、原始点值的来源质量、真实控制号及相关页眉、身份匿名核对、最终团队稿接受、注册／资格／导师记录、最终文件名、正式上传和导师门户回执。技术排版或文件哈希通过不等于这些事项已完成；不重复索要用户已说明暂缺的 Oslo 名单或 Zurich 凶杀率来源。

## 最近研究增量与下一步

- [Oslo DBH 计数定义](CURRENT_OSLO_DBH_UPDATE.md)：临时 23／25／26／27 代码方案；固定均为 Oslo，等权在 26／27 下为 Oslo。它们不是实际高校数的严格界限。
- [DBH／NOKUT 身份桥接](CURRENT_OSLO_DBH_IDENTITY_UPDATE.md)：27 个登记代码中匹配 25 个，1404／1405 未核；身份匹配的 23 与授课类型筛选的 23 是不同名单。112 点来源台账只更新证据说明，没有修改值、效用或认证等级。
- [新的教师岗位一手资料](CURRENT_NEW_STAFF_SOURCES_UPDATE.md)：Wirtschaftsschule KV Zürich 年报约 134 个教师全职岗位；近似误差、历史学段／校址和匹配学生数未落实，不构造硬界限。Helsinki 的旧 2019 教师收集事实复用原件，不当成新数据。
- [PM 整列撤回](CURRENT_PM_BLOCK_WITHDRAWAL_UPDATE.md)：临时将 16 个 PM 点扩为 `[0,1]`，其余 144 格保持；固定 Oslo 转 Zurich，等权仍 Zurich，所有案例仍 16／0。它是信息撤回压力测试，不是污染误差范围、概率或主推荐更新。新版 OECD 两个接口 403，没有取得新浓度数据；15 对代码映射仅来自旧元数据。
- [Oslo2026 居住区调查](CURRENT_OSLO_YOUTH2026_UPDATE.md)：四份官方分学段报告核对全15区表；90格初中描述值保留、90格高中隔离，Søndre高中本区图例与封面区名错配。体育参与、供给感受和费用障碍分别记录，不据此增加公平性罚分、作跨学段或精确年龄推断。主模型／论文保持。
- [Oslo2026 主报告](CURRENT_OSLO_YOUTH_MAIN_UPDATE.md)：72格组织活动／青年俱乐部原因和意愿；学校年级体育参与74%至31%，未到访者条件意愿及非互斥原因分别解释，不作纵向／精确年龄或泳池推断。主报告2018组成加权与区报告不同，不能据此修复前轮高中本区身份错配；主模型／论文保持。

这些增量的主数据准入和实际主模型区间收窄均为 0。下一轮先读采集登记与已核路线，再选可能改变结论的新匹配证据或明确的论文／交付任务。失败快速跳过；没有具体授权，不向机构人员发送消息。源绑定或路线索引有意改变时同步更新完整性合同，不改写冻结报告以消除历史差异。

更早的研究、同国／年龄／公平性案例仍在各自证据入口；历史 25 城不能混入主榜单，居民／通用 POI 可达性不能表述为学生或泳池实际使用。历史恢复日志保留在 [本次整理前的 Git 版本](https://github.com/TypeThe0ry/HiMCM/blob/9c7b59d264a72c017901979111f9c3ca7a77095c/docs/handoff/RESUME_PROMPT.md)，需要具体历史时再读取。
