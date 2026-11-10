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
| 主分析 | [主模型登记](../../research/2026-a/design/task4_user_current_model.json)；`task4_user_v205_revision.revised_bounds()` |
| 科学冻结证据 | [V205 快照](../../research/2026-a/design/task4_user_v205_snapshot.json)；115 个新绑定及冻结的 V204 658 个上游绑定 |
| 扩展与受控诊断 | [扩展登记](../../research/2026-a/design/task4_user_current_extensions.json) |
| 采集及来源跟进 | [采集登记](../../research/2026-a/design/task4_user_current_acquisition.json)、[已核查路线](../../research/2026-a/design/task4_current_source_routes.csv) |
| 当前论文与交付 | [审阅登记](../../research/2026-a/design/task4_user_current_review.json)、[交付登记](../../research/2026-a/design/task4_user_current_delivery.json) |
| 文件绑定检查 | [当前完整性合同](../../research/2026-a/design/task4_current_research_integrity.json)；报告数随明确登记更新 |

## 必须保留的科学状态

主分析是 **16 城 × 10 指标、V205**：112 个点值、37 个部分区间、11 个完全未知，25 个不同补充键。原始 [用户 CSV](../../research/2026-a/data/task4_v117_team_intake/city_indicators.csv) 的 SHA256 为 `430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c`；数值、年份、标记、人口、权重、锚点和区间规则保持。

固定权重的保守选择为 **Oslo**，等权为 **Zurich**，仍有 **16 个可能冠军、0 个必要冠军**。固定权重为八项各 0.1125，交通／泳池各 0.05；等权各 0.1。TOPSIS 距离权重只乘一次，最大遗憾比较排除自身。保守选择不写成确定冠军，AHP 偏好不是学生调查，MC 条件频率不是现实夺冠概率，未来情景不是拟合趋势。

V203 相对 V202 只将 Oslo 交通下界从原来的 89 个地铁站子集，替换为 626 个来源定义的单模式公交组；其余 159 个下界和全部上界保持。该数不与 89 相加、不代表全部公共交通；撤回及 624／625／623／627 检查见 [当前模型说明](CURRENT_MODEL_UPDATE.md)。V204 在此基础上将 Vienna 交通下界的 99 个站区替换为 378 个来源定义、计划服务的站区；其余 159 个下界和全部上界保持。9 条线路的季节／预约／日期／绕行条件及实际执行尚未完全核实，撤回 36 个已选见证后仍有 342 个站区，选择不变。详见 [V204 科学证据](CURRENT_V204_SCIENTIFIC_STAGING.md)。V205进一步将Prague交通57地铁子集替换为942来源定义公交节点，服务日2026-11-10，50常规、另892公开请求停靠；47ID重叠不相加。撤回请求见证时保留原57地铁下界。其他159下界／全部160上界和原CSV保持，完整来源／科学／论文证据见[当前启用记录](CURRENT_V205_ACTIVATION.md)。当前工厂历史依赖保留；勿用旧25城入口。

## 恢复和验证

从研究仓库运行。优先使用 [锁定环境说明](../../research/2026-a/environment/current-check/README.md)；本机已验证解释器是 `/data/scratch/himcm-current-check-env/bin/python`。不要用普通系统 Python 或不匹配的 `.venv` 运行模型；`.venv-v120` 是仍保留的旧兼容环境，不是唯一恢复要求。

V205 完整复现需要最终论文证明、干净且已同步的论文 Git HEAD，以及位于两个仓库之外的**新空输出目录**；最终证明和独立复现须分别检查，不能由登记推断通过。例如，确认目录不存在后运行：

```bash
env -u PYTHONPATH PYTHONNOUSERSITE=1 PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python -s research/2026-a/scripts/task4_v205_reproduce.py --output-dir /data/scratch/himcm-restore-check-new
```

仅检查当前研究登记和文件绑定，可运行：

```bash
PYTHONDONTWRITEBYTECODE=1 /data/scratch/himcm-current-check-env/bin/python research/2026-a/scripts/audit_current_research_bindings.py
```

检查默认打印 JSON；保存或覆盖报告须显式指定。复现器校验当前登记、各报告的直接来源映射，并在结束时检查输入未变；上游历史报告按已声明边界保留。历史路线索引通过 Git 提交 `4baa23ec09bb15bc3eae5ef17f952ec17f6d9921` 校验，当前索引另行绑定，因此本地需有对应 Git 历史。Tectonic 使用已有缓存，不能据此声称全新机器或线上编译通过。详见 [复现覆盖说明](CURRENT_RESEARCH_INTEGRITY_UPDATE.md)。

## 论文及待交付事项

当前本地已核的 V205 稿为 **27 页 = 25 页正文／参考文献 + 2 页暂定 AI 报告，63 条引用**。V205 已完成必要自有稿件和两张数值图整合，独立页面审查与交付定位通过。使用原 mcmthesis 类，原生 Summary Sheet、Team #／Page x of y 页眉及空页脚；18213 为用户允许的暂用控制号，真实注册号未核实。原类、参考库和队友原稿均保留。当前论文提交和远程状态见同步回执；每次仍须重新检查远程。

[48 项交付清单](../../research/2026-a/results/current_paper_review/requirements.csv) 仍有 12 项待办：完整团队 AI 披露／记录、原始点值的来源质量、真实控制号及相关页眉、身份匿名核对、最终团队稿接受、注册／资格／导师记录、最终文件名、正式上传和导师门户回执。技术排版或文件哈希通过不等于这些事项已完成；不重复索要用户已说明暂缺的 Oslo 名单或 Zurich 凶杀率来源。

本轮 V205 整合、实际改善及复现证据见 [当前启用记录](CURRENT_V205_ACTIVATION.md)；旧V204记录保持。

## 最近研究增量与下一步

- [Oslo 凶杀来源对照／Zurich 四泳池候选](CURRENT_SOURCE_CANDIDATES.md)：Eurostat 当前2008序列数量12匹配，但率2.14不匹配原1.71；历史边界／原分母未定，原值保持。四处人工泳池季节性候选与既有12地址不同；Auhof整修暂缓，Oberengstringen排除。隔离16场馆预览固定／等权均宽可减少0.01158463／0.02307772，选择仍Oslo／Zurich、16可能／0必要；本轮0准入、0实际收窄，V205与论文保持。下一步核地理／季节供给口径及完整受控迁移，不把条件预览当已更新主榜。

- [TBZ 教学工作量路线](../../research/2026-a/data/current_zurich_tbz_workload_route/README.md)：官方 2024 年报 pp.33–34 的 173 为教师人数（含部门负责人），未给实际教学 FTE 或匹配的 2024/25 统计日。原 PDF、完整提取及独立核对已保存，0 准入、0 实际收窄，V205 和论文保持。没有新的匹配工作量证据，不重复此报告或换算人数。队友整理修改时可使用[团队定稿空表](TEAM_FINALIZATION.md)，按所核论文提交／PDF 对应现有 12 项待办；填表本身不关闭门槛或授权提交，填写后的身份及原始记录私存。

- **V205已启用并完成本地论文迁移**：见[启用记录](CURRENT_V205_ACTIVATION.md)。773科学绑定、31主案例／186主MC／37扩展MC、当前三组敏感性及操作优先级已核；干净论文HEAD的27页文本／灰度复现通过。67→74份登记报告随新增证明核对。下一轮从V205继续，不重做已完成Prague资格／暂存；固定Oslo／等权Zurich、16可能／0必要，仍12交付待办。

- （启用前记录，现已迁移）[Prague V205科学暂存完成](CURRENT_V205_SCIENTIFIC_STAGING.md)：前轮942候选的单位／带日期公众服务资格已完成，勿重抓。官方GTFS完整原ZIP已入研究仓库；942节点均有2026-11-10服务日见证，50常规、另892公开请求停靠，保留司机协调条件。独立重算31主案例／186组主MC及37组扩展MC、2,064均值界和4,440名次比较通过；115新科学绑定＋658上游冻结。暂存固定／等权均宽可收窄0.1461508261／0.2872118755，选择仍Oslo／Zurich、16可能／0必要。撤回请求证据时用原57地铁下界，不能相加或降为50。主入口／论文仍V204，0当前准入／0实际当前收窄；下一轮从已完成科学暂存评估研究登记、自有稿件和交付证明迁移，不重做已通过的来源资格。

- （历史候选，资格已完成）[Prague公交节点条件候选](../../research/2026-a/results/current_prague_bus_candidate_preview/README.md)：复用V127的21份市内目录响应，归档9份新PID官方响应，精确按node＋组名＋显示线路号对照后得到942个待审来源节点；47个与原57地铁节点重叠，预览用替换而非相加。独立重解析7,326链接、全交叉表及64城市对照通过；假如后续资格成立，固定／等权均宽分别可收窄0.1461508261／0.2872118755，选择仍Oslo／Zurich、16可能／0必要。节点不是自动的实体设施，11月9日目录和11月10日JSON跨快照，isNight缺省保留未知；两个时刻表请求仅得相同通用壳。故0准入／0实际收窄、主科学与论文保持。下一步用已明确的单位、去重、市域分类和带日期的公众上下客服务证据资格审查；GTFS的zone_region_type为行政分类，勿用票价区或重取已完成目录。

- [Zurich条件采集门槛](../../research/2026-a/results/current_zurich_acquisition_targets/README.md)：独立608城市案例／10阈值核对通过。仅提高Zurich一个下界、其他上下界与权重保持时，固定权重PTR效用约0.11552655为推荐交叉，而约0.61982940才首次排除Amsterdam；出行效用推荐交叉约0.39190998。63,925州学生若另证为有效上界，则严格超过556.642636的匹配市内教学FTE下界是向上取整后的条件采集目标，不是已取得教师数或已准入界；首次缩小冠军集合需更强证据。新职业学校和通学路线11份原始响应均已离线复核，但人数／岗位计划不是实际FTE，教育目的旅程包含返程／大学／课程，未得到同人群单程分布。0准入／0实际收窄，主科学与论文保持。继续寻找互不重复、日期和学段匹配的教学工作量，不重复这些原件。

- [Helsinki／Dublin交通路线与采集上限](../../research/2026-a/results/current_two_city_transit_ceiling/README.md)：HSL原生area表完成ETag／范围／CRC和ID完整性核对，但物理站区含义、市界和逐日服务尚未成立；Dublin两个官方GTFS链接403后跳过。34份原始响应、离线复现及658科学文件绑定核对通过，0准入／0实际收窄。独立128城市案例及单调性证明：只提高这两城交通下界，即使同时放宽至效用1，固定Oslo／等权Zurich、16可能／0必要均保持；不是有限站数或实际改善。减少这两项的后续采集投入，优先匹配的教育和出行证据；主模型与队友稿件保持。

- [第三段我方AI记录](../../research/2026-a/data/current_ai_continuation2/README.md)：固定截止10Nov20:32:42.716UTC（11Nov04:32SG），新增51根上下文、239选中可见记录、1,367顶层输入；三段累计167／762／4,604。仅新元数据和指纹／哈希公开，精确导出私存；旧选择器前缀不抹去、不声称匿名化。自有AI报告已同步这些范围，正文前25页及六资源保持，27页／63引用和12待办维持。最新干净论文提交复现见`results/current_ai_continuation2_paper/reproduction/report.json`；不是完整团队或子agent历史。

- [Zurich交通地理和标识核对](../../research/2026-a/data/current_zurich_transit_boundary_followup/README.md)：官方市镇261多边形下旧WFS为478条内含460条有线路，名称筛选存在3条几何不一致；国家同市镇有序六页579条、旧市界内474条完整DiDok编号对应。独立复核通过，商业／物理站区去重与446单位可比仍未建立，0准入／0实际收窄。不要再把cname当市界证据、把unique/parent当商业站合并，也不要定时轮询供应方定位为手工查询的FOT列表。

- [V204 成组信息撤回](../../research/2026-a/results/current_v204_source_block_stress/README.md)：成本／住房32点、宽带16点、PM16点的八子集完成独立标量和三项重算哈希后的负控。固定单撤成本或PM转Zurich，等权单撤宽带转Oslo、再联合撤回其他组转回Zurich；不是共同误差模型或现实失效概率。256城市×权重案例、1,280区间和658科学文件及两份论文依赖核对通过，主与稿件保持。

- [Zurich 来源与职业路径补充](CURRENT_ZURICH_SOURCE_FOLLOWUPS.md)：高教23的算术及八条认证范围、州SekII学生63,925与教师不匹配、学徒交通16条辅助摘录完成独立审查。0主准入／0实际收窄；当前点值台账仅将Zurich HE更新为已查但来源链未解决，风险和优先次序保持。新完整性合同为44报告／1,164绑定。

- [Oslo DBH 计数定义](CURRENT_OSLO_DBH_UPDATE.md)：临时 23／25／26／27 代码方案；固定均为 Oslo，等权在 26／27 下为 Oslo。它们不是实际高校数的严格界限。
- [历史 DBH／NOKUT 身份桥接](CURRENT_OSLO_DBH_IDENTITY_UPDATE.md)：当时27 个登记代码中匹配25 个、1404／1405 未核；身份23与授课类型23不同。该历史结果保持冻结，两项身份已由下述完成补充解决，原数值和认证等级仍保持。
- [新的教师岗位一手资料](CURRENT_NEW_STAFF_SOURCES_UPDATE.md)：Wirtschaftsschule KV Zürich 年报约 134 个教师全职岗位；近似误差、历史学段／校址和匹配学生数未落实，不构造硬界限。Helsinki 的旧 2019 教师收集事实复用原件，不当成新数据。
- [PM 整列撤回](CURRENT_PM_BLOCK_WITHDRAWAL_UPDATE.md)：临时将 16 个 PM 点扩为 `[0,1]`，其余 144 格保持；固定 Oslo 转 Zurich，等权仍 Zurich，所有案例仍 16／0。它是信息撤回压力测试，不是污染误差范围、概率或主推荐更新。新版 OECD 两个接口 403，没有取得新浓度数据；15 对代码映射仅来自旧元数据。
- [Oslo2026 居住区调查](CURRENT_OSLO_YOUTH2026_UPDATE.md)：四份官方分学段报告核对全15区表；90格初中描述值保留、90格高中隔离，Søndre高中本区图例与封面区名错配。体育参与、供给感受和费用障碍分别记录，不据此增加公平性罚分、作跨学段或精确年龄推断。主模型／论文保持。
- [Oslo2026 主报告](CURRENT_OSLO_YOUTH_MAIN_UPDATE.md)：72格组织活动／青年俱乐部原因和意愿；学校年级体育参与74%至31%，未到访者条件意愿及非互斥原因分别解释，不作纵向／精确年龄或泳池推断。主报告2018组成加权与区报告不同，不能据此修复前轮高中本区身份错配；主模型／论文保持。
- [Swiss 师资原件复用](CURRENT_SWISS_STAFF_REUSE_UPDATE.md)：BFS完整公私教师表与SSP手册均为V170／V171已有原件，当前路线表已补索引。上限覆盖／参考日／单侧出版精度仍未证实；不以旧Eurostat警告或T9分类缺项否定T10总量。0新观测，Zurich生师比效用仍`[0,1]`。
- [历史公平性端点证书](CURRENT_TAIL_ENDPOINT_UPDATE.md)：同一质量松弛的完整阈值由1227简化为51，七原结果保持；357LP与七新见证尾部LP、三文件重现通过。支持原2012条件差距，不升级原CSV来源或整记录／现实错误率认证；不新增城市评分模型或改稿。
- [Oslo HE 身份完成与地域标记](CURRENT_OSLO_HE_IDENTITY_COMPLETION.md)：两项新官方桥接使27代码身份全对应，每期25正值代码均对应；新两者是课程获批而非机构认证。Gestalt的DBH Oslo校区与Bærum／Sandvika来源有待核差异，未剔除或纠正计数。台账只更新Oslo HE三项证据字段，主值／分类／优先级与论文保持。
- [Oslo HE 地点差异与条件24检验](CURRENT_OSLO_HE_LOCATION_UPDATE.md)：旧DBH共22条0301历史记录与其自身Sandvika机构地址有差异；新2026报告沿用地点背景，质量工作认可不等于机构认证。临时计数24、密度33.0时所有决策名次保持，固定Oslo／等权Zurich、16／0；未修正原25或主模型。2019访谈原件403，不采纳搬迁年份。
- [Paris 全市教师／学生连接](CURRENT_PARIS_TEACHER_JOIN_UPDATE.md)：154个学生UAI匹配153个教师记录；27个GT／PRO交集须防止重复计入1,870.52机构FTE。名录6个多校址编码、4个混合高中后课程标记保留候选集合，3个类型漏项经精确查询找到EREA记录。当前标记与2025学段分配／完整提供者覆盖仍有区别，PTR保持`[0,1]`，主值与论文保持。
- [初始Vienna GTFS候选](CURRENT_VIENNA_GTFS_CANDIDATE.md)：378个站区通过结构核查，候选固定／等权均宽减少0.04554／0.08969分，选择仍Oslo／Zurich、16／0。该阶段的资格待办已由下一条V204科学工作完成，初始回执保持；主分析已登记为378。
- [V204科学暂存完成](CURRENT_V204_SCIENTIFIC_STAGING.md)：公开乘客目录覆盖全部88见证线路，已补齐供给口径的公众性质证据；14文档响应均为HTML非PDF，具体条件保留。V204已完成29案例／174组MC、全部扩展和独立审计，9条件线路36已选见证撤回后仍342站区、选择保持。研究入口和自有论文均已整合V204；最终复现和远程状态以本轮回执为准，不重找已完成资格证据。

上述各轮记录保留生成时的准入状态。当前V205已新增Prague部分区间细化，固定／等权均宽本轮实际收窄0.14615／0.28721分；此前V204的Vienna改善0.04554／0.08969分分别保留。下一轮先读采集登记与已核路线；请求前再按URL、资产号、文件名和提供方关键词检索历史数据／口径，当前路线表不是穷尽目录。再选可能改变结论的新匹配证据或明确的论文／交付任务。失败快速跳过；没有具体授权，不向机构人员发送消息。源绑定或路线索引有意改变时同步更新完整性合同，不改写冻结报告以消除历史差异。

更早的研究、同国／年龄／公平性案例仍在各自证据入口；历史 25 城不能混入主榜单，居民／通用 POI 可达性不能表述为学生或泳池实际使用。历史恢复日志保留在 [本次整理前的 Git 版本](https://github.com/TypeThe0ry/HiMCM/blob/9c7b59d264a72c017901979111f9c3ca7a77095c/docs/handoff/RESUME_PROMPT.md)，需要具体历史时再读取。
