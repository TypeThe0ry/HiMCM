# 接手续做HiMCM：V136主数据／V137扩展，文档V148

长期goal active；单轮完成不结束长期目标。所有新增／修改论文和研究说明必须使用指定已安装anti-defensive-writing中英文技能。先读AGENTS.md、GUIDELINES.md、[V149当前交付对照](V149_RESEARCH_UPDATE.md)、[V150最新补数核查](V150_RESEARCH_UPDATE.md)及[V148当前稿件交接](V148_RESEARCH_UPDATE.md)。现行已经启用，不再称待迁移，不回到旧25城主入口。

## 权威数据与结论

- 主入口research/2026-a/design/task4_user_current_model.json为V136，factory task4_user_v136_revision.revised_bounds()；16城×10指标，112点／33部分／15全缺失，21累计补充。扩展design/task4_user_v137_extensions.json active。启用证据见[V137完整稿](V137_COMPLETE_REVIEW.md)。
- 原CSV data/task4_v117_team_intake/city_indicators.csv SHA430e550093ef33bf8994b7d243ec6932bc7d4cc205e1ea81ac34c985157adf3c。已有值、人口／年份、权重、锚点和矩形规则保持；真实补数只准入空格，候选与正式准入分开。
- 接受原点值时fixed／equal均Zurich保守、16可能／0必要冠军；教育优先Oslo。fixed均宽16.089333559065736，equal18.914257170685545；累计真实补数收窄14.4675%。最新London仅59站／hub资源下界，2026库存配原2025人口，不能称2025普查或个体访问。
- V142独立验证16个分别构造的严格内点完成情景，每个目标在基准和等权下均第一；最小领先4.966／5.306。限于声明utility矩形，非概率或共同物理可实现性证明。
- V143来源政策诊断：112点64标2026、2标2025；撤回28非ok点为未知时Berlin／Paris，撤回64个2026点时仍Zurich但基准均宽16.09→48.43。日期和标记不是误差概率或自动排除规则。
- V144恢复具体原源：CBS2023发布的2022暂定Amsterdam单年受害者10，XLSX区域表68覆盖2018–2022；原340的来源仍未匹配。Zurich PKS2025第117页2024既遂1、2025既遂2是犯罪行为数，第118页定义独立于受害人数，未建立原0.14率分母。不制造替代率。
- V144只撤回Zurich凶杀点utility信息时基准Singapore／等权Oslo；Amsterdam单点撤回均仍Zurich，两点撤回Singapore／Oslo。单点其他159格不动，原48非点／21补充保持，全部8组16可能／0必要。主数据未改；不要把该试验说成对28点批量结果的唯一因果归因。

- V145区别有限点率变动：其他159格固定，假设点率x_Z的打平阈值基准0.2300179962（Singapore）、等权0.9047272573（Oslo）每10万人。原0.14及0.135／0.145邻近探针仍Zurich；后两者不是已知测量误差。两种数值方法及224城市情景／448得分界通过，唯一交点有单调性解释。非观测率／置信限／预测，原数据不变。新受害者范围排除90+、抑制<5、部分重复计数，8目录元数据未获匹配率，0准入；不反推小计或声称数据全无。

## 论文和复核

相邻/data/projects/HiMCM-Overleaf的drafts/task4_v137_paper.tex/.pdf是自有独立审阅稿，文档修订V148。24页=22正文参考+2暂定AI；新闻16–17，参考18–22，AI23–24。PDF161754字节，SHAf4e50119defd735828ca34d4427ff54f9bc8b58750ae9f3a87a3c3dca76eb6a8。零warning，24页95dpi实看、14页单独检查。139科学／66旧资产章节／74历史稿保护通过，6其他自有章节保持，23页像素保持。旧稿冻结。

- 研究Python .venv-v120/bin/python（3.11、numpy1.26、pandas2.3、scipy1.13）；tectonic0.17、Poppler。root账户，项目/data/projects，大原件/data/datasets，临时/data/scratch；不重建环境。
- V136 snapshot10项、原revision_audit及V137 audit55输出冻结。启用后16静态／24×10000同流MC和撤回已通过，无新科学风险不重复全量跑。复核老审计另写recheck，不覆盖原capture。
- 新源data/task4_v144_homicide/extract.py可从Git内原XLSX／HTML和完整lossless PDF复抽。scripts/task4_v144_homicide_sensitivity.py生成情景，audit_task4_v144_homicide.py独立核128城市情景／256得分界、全部排名、原表单位／期间。原verification保留。
- 当前文档审计scripts/audit_task4_v148_documentation.py保护139科学／66旧资产章节／74历史稿；results/task4_v148_documentation存QA／manifest／编译／sync回执。新age_joint段及3回执由builder绑定，原V146来源覆盖21/21保持。旧交付哈希为历史，不检验当前PDF。
- Overleaf builder build_task4_v137.py先核冻结源和新审计；只改叙述／来源用--refresh-manifest-only，不重生主图／宏。新PDF每轮首次authoring按PDF技能marker一次，编译捕获stdout/stderr，checker --compiler-output LOG，实际看完全部渲染才加--render-review-confirmed。
- 权重8×.1125，transport／pools各.05；equal各.1。收益x/(a+x)，成本a/(a+x)，锚点2/15/100/10/15/1/50/travel30/100/1。travel exp(-t/30)，均值只Jensen界，分箱／未知／开尾按原规则；距离权重只乘一次。自排除竞争上界、minimax regret保守决策。MC为条件频率，偏好非学生调查，未来情景非经验趋势。

## 权限和持续任务

GitHub仅研究，Overleaf仅稿件和选定资产；分别fetch并审确切diff，正常main提交，无force。无connected文档session时只称Git镜像；当前无session。用户待答的GitHub公开发布选择仍未解决，研究仅本地commit、不改可见性；Overleaf按授权push。队友main.tex／ref.bib／mcmthesis.cls及项目主文件设置保持。共享main本轮实际编译仍缺原framework.png，日志已归档，不修队友正文。

实际控制号PENDING，旧18213/18214冲突不猜；全队AI史、最终整合具体授权、提交回执仍待真实资料。125条根会话局部选集及03:17UTC/2026-11-09固定截止保持，不能称完整史；私有原文不入仓库，不把后续消息塞进旧capture。

下一轮只尝试真正新的匹配教师FTE／高中实际单程旅时／原率来源，或当前整稿交付要求核对；不重复V145已查8目录项和已确认的抑制／单位不匹配路线。Dublin／Zurich教师仍有高信息价值，但旧地区汇总／岗位不填；Warsaw广义学校、Tokyo全周工作学校合计、Vienna潜在最近学校路由均不替代高中实际旅时。V141完整47MB ÖROK原PDF外置，新clone需另取；V144完整原件已在Git。保留原表，失败跳过，持续按可验证改进推进，不结束长期goal。

## V147新源核查

新取Zurich 2025/2026学校统计及Helsinki 2025年鉴完整PDF和出版说明，0新准入。州公立教学FTE1771.6与部门雇员FTE2227不同；Helsinki学生最新行仍2024，相邻成人课时不作师资。完整原件／指定页渲染／提取器在data/task4_v147_education_refresh；独立词坐标审计scripts/audit_task4_v147_education.py核139科学／82稿件文件。Overleaf仅新增drafts/task4_v147_source_review支持回执，论文仍V146、原PDF字节保持；不重复这两页试填，下一轮需要新的匹配分母路线。

## V148年龄联合约束

既有2012年龄组差值闭包[-0.23330,0.26325]，共享612未知年龄质量只计一次；两个有限旅时构造给+0.23842／-0.20848。源仍data/task4_v116_ibb/aggregate_results.json，原汇总／边际案例保持；scripts/task4_v148_age_contrast.py及独立audit核解析符号、5151分配点和2见证。只增自有6.4，非今天精确14／18岁、非偏好调查或抽样置信区间，0准入／0主得分收窄。

## V149当前交付对照

results/task4_v149_readiness含39项对照、字体表、数学脚标表与独立verification；源刷新data/task4_v149_requirements_refresh。四个2026官方响应与V123原件哈希一致；论文仍V148原PDF，未新编译／渲染／写作。技术项与范围受限／部分／未核实分开，submission_ready=false。控制号、完整AI史、最终整合、注册标识和上传／advisor入口收件仍需真实证据。字体表整数舍入12pt正文，167个8pt数学脚标单列，不作全字形证书。若后续改稿，生成新的当前对照，不拿旧哈希认证新稿。

## V150 Madrid师资候选

1902424取得20列2005–2024，按原注映射2004/05–2023/24；最新市1008／区域1922。三层区域／分区／市镇重复同一总体，20年汇总相等，平铺末年会得5766，不能累计当教师。Número和Bachillerato计数未建立城市全上阶段教学FTE及学生匹配；区域Régimen-General FTE比12.6也不填，0准入。provider表示有原件／图表局限，完整捕获和代码在data/task4_v150_madrid_education，独立审核results/task4_v150_madrid_education。139科学／82稿件文件保持，V136/V137及V148PDF不变，V149对照仍适用；下一轮查新匹配分母，勿重复用1008或12.6试填。
