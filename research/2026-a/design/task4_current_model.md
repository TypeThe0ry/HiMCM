# 当前模型：V96 Warsaw六类高中路径师资修订（2026-11-08）

V99新增[单格证据撤回诊断](../results/task4_v99_cell_stress/README.md)：117个含信息单元各自放宽ε≤0.20仍推荐Singapore；完全撤回其凶杀率、PM2.5、生活成本或宽带一项可改变推荐。保留4个切换未决叶；该结果定位来源核查优先级，不是实际误差证据。[Tokyo2026速報配对情景](../results/task4_v99_tokyo_year/README.md)保持同口径2025/26排名；没有替换当前更广覆盖及教师职能口径。

V98将[压力检验证书](../results/task4_v98_joint_stress/README.md)更新到当前V96输入，并修正统一结果入口遗留的V79说明。全城共同扩张与单城扩张的结论保持：前者在ε≤0.20内推荐Singapore，后者ε=0.043、α=0.05出现Tokyo反例。该检验没有收缩真实缺失区间。

V97完成[共同补数情景的可达性证明](../results/task4_v97_intake/README.md)：24个当前V96案例的逐城市下界均由同一组揭示值达到；全城教育＋通学的模型内最小候选数为固定9、连续22。实际25城可能冠军及全部排名保持；Warsaw青年／成人FTE拆分尚缺官方数值，未准入二手数据。

V96以[同年度官方年鉴](../results/task4_v96_intake/README.md)将Warsaw教育由普通高中条件范围扩展为六类青年高中路径、公私立学校，保留成人教师分配界。Warsaw第12→8，其他249格保持、可能冠军仍25城；仅年份更新不改变排名。[补数下界](../results/task4_v96_acquisition_limits/README.md)同步更新至V96，其余已登记诊断仍标注V91历史输入。当前入口为 `task4_warsaw_resource_revision.warsaw_bounds()`。

V95以[Jakarta真实交叉表](../results/task4_v95_intake/README.md)将同一262人高中子群通学界宽度收窄16.85%，另单独识别14–18岁交集界；保留样本／全市范围区别。Phoenix未知测试人数显式传播，Warsaw高中通学流量原件与抑制残余归档。主模型V91、250格及25个可能冠军保持。

V94完成[Phoenix剩余12校身份桥接与Jakarta真实通学子群计算](../results/task4_v94_intake/README.md)，累计108校、319条高中成绩；未强行准入全市指标。[128组补数阈值](../results/task4_v94_precision_frontier/README.md)已更新到V91，区分空气实测上下界对补数情景的相反作用。250格、排名及25个可能冠军保持。

V93将[Phoenix高中成绩覆盖](../results/task4_v93_intake/README.md)扩展到100校、296条学校—学科记录；保留未知测试人数，不替换全市师资资源指标。[压力检验](../results/task4_v93_joint_stress/README.md)已更新至当前V91，推荐失效边界仍为(0.042,0.043]。真实排名、250格及25个可能冠军保持。

V92将[冠军补数能力分析](../results/task4_v92_acquisition_limits/README.md)更新到V91：教育＋通学＋PM2.5连续不可排除下界21→22，新增Phoenix；实际可能冠军仍25城。并扩展Phoenix官方11年级学校考试记录，保留受限值及范围缺口；主模型和排名未改。

V91取得[官方EPA市内监测数据](../results/task4_v91_phoenix_monitor/README.md)，Phoenix PM2.5效用由未知改为[0.564421,0.680536]，对应已观测合格监测网络的条件加权量，不是人口暴露界。Phoenix第24→16，得分界宽度缩小13.47%；25个可能冠军保持。严格撤回恢复V79。[连续补数分析](../results/task4_v91_current_acquisition/README.md)同步更新，其他V79诊断保留历史版本。

V90将[连续偏好补数分析](../results/task4_v90_current_acquisition/README.md)从V64/V63更新到当前V79，Phoenix最有利连续补数需求由4项变3项，Tokyo由2项变1项。585组合、444证书独立复核，真实排名及25城可能冠军不变。注册表已更新分析版本，旧结果作为历史对照保留。

V89完成[SIMCE等级比例条件区间与来源追查](../results/task4_v89_intake/README.md)：保留全零和质量标记学校，用人数总量及舍入约束计算区间，分母及舍入规则未完全确认，未准入主模型。Phoenix财政教师资料与课堂教师口径仍不同；主模型V79、排名和25城可能冠军保持。

V88完成[学习成果修订的名次分解](../results/task4_v88_coverage_attribution/README.md)：8个组合、6种执行顺序将指标替换与证据增减分别核算，避免把资料变化当作城市质量改善。另取得Chile2024高中二年级SIMCE原件并核查Santiago学校地域；不同考试尺度单独保留。主模型仍V79，真实排名及25个可能冠军保持。

V87完成[高中阶段编码与学习成果替代检验](../results/task4_v87_learning_stage/README.md)：取得5个学校地域的同年PISA微观结果，统一学段编码补回Singapore340人、Dubai96人。学习成果替代资源指标会改变决策排名；学段规则修正本身未改变名次，可能冠军均为25城。该检验保留PISA年龄及地域条件，主模型仍为V79。

V85完成[Phoenix同年公校数据与Bogotá学业结果核验](../results/task4_v85_intake/README.md)：取得2023/24历史公校原件，明确9—12年级72562人，Hope该年83人；104条教师FTE仍缺失。与私校年份对齐，但未替代全市指标。另取得Bogotá官方PISA均值与标准误，公布范围仍非高中专属。实际排名与25城可能冠军保持。

V84完成[私校高中教师分配的实测诊断](../results/task4_v84_intake/README.md)：同一6109名明确高中学生下，加入学段分配后资源效用界由仅工作档位情景[0.680454,0.690707]扩为[0.330722,0.690707]。这是纠正虚假精度，未准入全市；真实排名及25城可能冠军保持。

V83接入[Phoenix私校原始数据与教师档位](../results/task4_v83_intake/README.md)：33条市界内有高中学生的私校记录合计6109人，估算全学段FTE888.6，其工作档位外界为[867.25,909.50]。非响应、学段与跨年覆盖未解决，未代替全市缺失界；实际模型仍V79。

V82完成[当前输入的稳健性边界细化](../results/task4_v82_joint_stress/README.md)：Singapore单城扩张的首次失效括区间缩为(0.042,0.043]，宽度比旧检查减少96%，未改变真实缺失区间。Phoenix新获同年学区学生25800与课堂教师1349.60 FTE并完成校级对账，仍不能替代全市口径。实际排名和25城可能冠军保持，注册表压力证书已更新至V79输入。

V81完成[Phoenix及Barcelona来源审计与复算](../results/task4_v81_intake/README.md)：新增真实教育原件与问卷版本核验，未准入新指标。250格、排名、25城可能冠军与Singapore连续推荐均保持；模型仍为V79。

V80在当前V79上[重新验证补数能力](../results/task4_v80_acquisition_limits/README.md)：全城教育＋通学精确揭示后，连续偏好不可排除城市数下界21→22，新增Mumbai，变化来自V78实测修订。实际冠军集合仍25城；[Phoenix128组合阈值](../results/task4_v80_precision_frontier/README.md)重算不变。注册表已指向本轮证书，压力分析仍为V72历史输入。

V79完成[Delhi校级核验与分配修订](../results/task4_v79_delhi_allocation/README.md)：N=603437，D=26766，M=3420，零高中学生学校专任Z=105；按与Mumbai相同的名义资源约定T∈[D−Z,D+M]，教育效用[0.398579,0.428686]。Delhi由13变14、Santiago由14变13，其他排名及25城可能冠军保持。仅Delhi教育格变动，当前入口`task4_delhi_allocation_revision.delhi_bounds()`。这统一同源分配处理，不代表国际FTE统计统一；旧压力与补数证书仍对应历史输入。以下为历史记录。

V78使用[同源校级学生与教师分类](../results/task4_v78_mumbai_school/README.md)：N=280140，T∈[5848,6854]，教育效用[0.238460,0.268468]。仅Mumbai教育格改变，总分区间宽度减少17.6%；全部排名保持、25城仍可能第一。当前入口为`task4_mumbai_school_revision.mumbai_bounds()`，镜像字节一致性及统计覆盖条件仍保留。此前V72压力、V73补数下界、V76补数阈值为历史输入分析，本轮不沿用其证书。以下保留历史修订记录。

V77完成[Mumbai高中人数跨表对账](../results/task4_v77_sources/README.md)：明确11—12年级278,538人，发现城区学校类别人数少14,315人；全类别学生总数相符，教师覆盖仍待核实。未将条件教师池上界录入，主模型保持V72。

V76新增[Phoenix补数连续阈值](../results/task4_v76_precision_frontier/README.md)：在下端点附近的假想区间情景下，至少需5项；最佳5/6/7项ρ临界值约0.062202/0.259080/0.385401。阈值同时约束结果位置与宽度，不能当单纯测量精度。Athens补入历史校名证据，主模型仍V72、250格与全部排名不变。

V75取得[Athens完整校级原件与48校匹配子集](../results/task4_v75_sources/README.md)，但学年、目录时期与教师池仍未对齐；Phoenix补获校内项目官方说明。城市指标准入变化0，科学模型保持V72，250格与全部排名不变。

V74取得[Phoenix与Toronto学校级新原件并复算](../results/task4_v74_sources/README.md)：解释PXU目录数量差异、取得Toronto教师目录与分校预算；行政队列与实际高中教师分配仍未识别。Athens学校数据下载中断，未准入。科学模型仍V72，全部输入及排名保持。

V73重算[当前补数下界](../results/task4_v73_acquisition_limits/README.md)：全城教育＋通学即使精确测得，固定权重仍至少8城、连续权重并集至少21城无法排除；仅补Phoenix两项仍25城。科学模型继续V72，250格与全部排名不变。

V72将Mexico City通学筛选改为14—18岁，保留未知资格和学段重建条件；仅1格改变，其他249格及全部排名保持，25城仍可能第一。[修订与排名](../results/task4_v72_mexico_age/README.md) · [当前压力检验](../results/task4_v72_joint_stress/README.md)。当前入口为`task4_mexico_age_revision.mexico_bounds()`；最新压力结论已在V72重跑，单城扩张首次失效括区间为(0.025,0.05]。以下为历史记录。

V71完成[四地新来源核查与当前通学索引](../results/task4_v71_intake/README.md)，科学模型仍V70。统一入口现在在写结果前核对5城有信息通学界与显式来源登记；20城保持[0,1]，250格与全部排名不变。NYC当前使用V21真实RHTS旅程，历史NYU路线估计不再是当前输入。

当前入口为[revised_bounds()](../scripts/task4_population_role_revision.py)。[V70数据与六情景对照](../results/task4_v70_population_roles/README.md)撤回Singapore不适用的整组通学均值界，恢复高中子群[0,1]；Tokyo按官方岗位和60名专攻科所在地/所有制，修订教学岗位资源界T∈[17817,25178]。只有两格变化、其余248格保持，全部名次不变、25城仍可能第一。新增分箱子群算法可以接入未来同总体子群人数，避免把全体均值直接移作高中生的界。V69压力阈值与V68补数数量界为历史输入结论，本轮未重新认证。

V69历史入口为[tokyo_special_bounds()](../scripts/task4_tokyo_special_revision.py)。[V69原件与对照](../results/task4_v69_tokyo/README.md)补入特教高中本科学生界[5808,6017]，保留国私立专攻科与全学段教师分配未知。仅Tokyo教育格变化，效用[0.482443,0.564467]；全部排名保持、25城仍可能第一。[V69重跑压力检验](../results/task4_v69_joint_stress/README.md)中均匀扩张ε≤0.20仍推荐Singapore；只扩张推荐城时首次失效阈值位于(0.05,0.075]。这是指定假设情景，非实测误差。

V68历史入口为[singapore_stage_bounds()](../scripts/task4_singapore_stage_revision.py)。[V68原件与对照](../results/task4_v68_singapore_stage/README.md)依据UIS学制映射撤回Pre-U代理，改用MOE高中课程学生界与全部报告教师池的条件界。Singapore教育效用由[0.541549,0.587187]改为[0,0.849407]；其他249格不变。全部决策排名保持、可能冠军仍25城，连续偏好下仍推荐Singapore。范围和实际授课分配尚未完整识别，`main_admitted=false`。下列V63—V67结果为历史基线；其中旧扩张阈值与补数最小项数没有在V68上重证。

V67新增[联合扩张与连续偏好检验](../results/task4_v67_joint_stress/README.md)：均匀扩张ε≤0.20保持Singapore；仅该城扩张的首次失效阈值位于(0.10,0.15]，ε=0.20时连续α范围推荐Tokyo。这是指定假设情景，不修改V63实测输入。

V66完成[四城新来源核查与复算](../results/task4_v66_intake/README.md)。上海2025年报引用2024年中职学生数；Phoenix新学生调查仅3—8年级；London和Bogotá仍缺可用联合记录。全部250格、排名和可能冠军保持，当前数据模型仍为V63。

V65提供[统一复算入口与本轮来源核查](../results/task4_current/README.md)，由[注册表](task4_current_model.json)选择V63数据函数并核对全部250格。Phoenix、London、Bogotá本轮新增可准入高中生通学观测为0；现有区间、排名和25城可能冠军保持。

V64新增[连续偏好补数规划](../results/task4_v64_continuous_acquisition/README.md)：在现有矩形效用外包、仅测本城且观测足够有利的条件下，Phoenix要在整个α∈[0.05,0.20]获得推荐，最少指标数由固定权重的3增为4，Shanghai由2增为3。全25城1024组合经失败见证或区间证书检查，无未决组合。此为采集可行性诊断，不是实测结果或保证获胜；V63实际250格、名次和25城可能冠军保持。

V63历史条件入口为[cape_2025_bounds()](../scripts/task4_cape_2025_revision.py)。Cape Town以GHS2025的182名14—18岁当前10—12年级学生更新通学，216PSU/14层重算近似抽样包络[0.3922371575,0.7798278718]。其他249格保持，全部排名不变（Cape Town第5、Phoenix第24），固定及连续偏好下可能冠军25城，Singapore连续推荐证书通过。不将两年区间相交，不把考试考生通过率混成毕业队列或教师资源。[完整对照与公式](../results/task4_v63_cape_2025/README.md)。

V62取得12份官方原件并重跑核验，当前模型仍为V61。London、Copenhagen、Cape Town新增校级数据尚未对齐高中阶段、时间或总体；Phoenix毕业差2仍未解决。全部250格、排名及25城可能冠军集合保持，连续推荐证书通过。[本轮原件与复算](../results/task4_v62_source_intake/README.md)。

V61历史条件入口为[dhaka_role_bounds()](../scripts/task4_dhaka_role_revision.py)。原表965个非校长角色不能保证965名独立授课教师；保留职责与去重未知，Dhaka教育外包改为[0,0.5987270617]（非最紧识别集）。其他249格不变，Dhaka第21→22、New York第22→21，Singapore仍推荐、Phoenix第24；固定及连续偏好下可能冠军25城，连续推荐证书通过。原件前言2024与详细方法2025采集日期矛盾已完整记录。[完整对照与公式](../results/task4_v61_dhaka_roles/README.md)。

V60历史条件入口为[dhaka_madrasa_bounds()](../scripts/task4_dhaka_madrasa_revision.py)。Dhaka补入Alim阶段，N∈[140342,469293]、T∈[965,13960]，教育效用15T/(N+15T)∈[0.0299213673,0.5987270617]。全国类别与性别边际仅约束城市子集合上限；技术职业高中及原表日期、地域条件仍未解决。其他249格不变，全部名次与V59一致，Dhaka第21、Phoenix第24；固定和连续偏好下可能冠军25城，Singapore连续推荐证书通过。[完整对照及公式](../results/task4_v60_dhaka_madrasa/README.md)。

V59历史条件入口为[dhaka_stage_bounds()](../scripts/task4_dhaka_stage_bounds.py)。在V58上仅将Dhaka教育格由[0,1]改为[0.0327952421,0.5622274488]：BANBEIS市级学院计数与全国同类别混入上限给出高中学生N∈[140342,426900]、教师角色T∈[965,12016]，效用15T/(N+15T)。全国数只作城市子集合的污染上限，不代填全国均值。原表Dhaka City Corporation范围及2025版/方法页2024日期矛盾保留为条件，不称同日普查或完整居民覆盖。其他249格和通学界不变；Dhaka第22→21、New York21→22，Singapore仍第1、Phoenix第24；可能冠军25城，连续α∈[0.05,0.20]推荐证书通过。[完整对照](../results/task4_v59_dhaka_stage/README.md)。

V58历史条件入口为[jakarta_coverage_bounds()](../scripts/task4_jakarta_staffing_revision.py)。V58在V53基础上仅修订Jakarta教育格：SMA、SMK和MA同学年公布学生N=405311；主归属教学人员T=22524+H+M，H∈[0,978]为未识别校长教学角色，M∈[0,2008]为MA额外不同教师。教育效用15T/(N+15T)∈[0.4546194617,0.4856204812]。Induk不等于FTE；noninduk任教关系按主归属目标排除，而非断言全部已在本市重复。SMA/SMK原始PDF已核验，MA仍为官方索引转录，11月/12月截面不是同日普查。其余249格和真实学生通学界保持，全部名次不变：Jakarta第18、Singapore第1、Phoenix第24；可能冠军25城，连续α∈[0.05,0.20]推荐证书通过。[本轮完整对照](../results/task4_v58_jakarta_staffing/README.md)。以下各轮说明为历史记录。

V57完成[同届学校与学区人数核对](../results/task4_v57_school_union/README.md)：重取22份毕业响应后，已知实体学校5802加Digital485仍为6287，超过学区6285两人。新增必要一致性检查拦住未对账的学校集合求和；候选界虽可让毕业扩展中Phoenix第24→23，实际城市界、十指标排名及25城可能冠军均保持原样。净差2不能当作重复人数上界。

V56完成[PXU名册与排除队列对照](../results/task4_v56_pxu_exclusion/README.md)：24个历史名称与21个NCES实体的差异来自3个共址项目，后续23项另涉及2024关闭。历史毕业责任人员仍未完全对齐；实际城市毕业界不收紧。条件B=0时，以整个Digital队列485人为排除上限得到毕业界[0.176164,0.986883]，在独立毕业扩展中Phoenix第24→23；这不是主模型已确认改善。当前十指标输入、排名及25城可能冠军不变。

V55新增[推荐相关采集诊断](../results/task4_v55_recommendation_acquisition/README.md)：固定α=0.10，仅测本城时，Phoenix最少3格、Tokyo最少2格的有利精确结果才可能让该城唯一获推荐；教育＋通学对这两城均不足。这里的有利端点不是实测值。新增PXU学区毕业6285人中4813人的记录保留其含线上学校的范围条件；实际主模型仍V53，排名及25城可能冠军不变。

V54完成[名单完整性与分母范围核查](../results/task4_v54_scope_intake/README.md)：新取得的Istanbul12校名单不能证明完整27校总体中当地为零；Shanghai中职学生与教师范围仍未配对；Phoenix校车系统没有公开城市旅时统计。主模型仍为下述V53，重算排名及25城可能冠军均不变。

V53历史条件入口为[istanbul_coverage_bounds()](../scripts/task4_istanbul_coverage_revision.py)。Istanbul非开放教育普通、职业技术及Imam Hatip高中学生合计751598；教师T=28436+V+H，V∈[0,20156]、H∈[0,9871]，教育效用界[0.3620458724,0.5384843999]。相对原普通高中范围，第10→第15；同一扩大范围相对该项未知则第18→第15。其余249格不变，Singapore仍推荐、Phoenix第24、可能冠军25城，连续α∈[0.05,0.20]推荐证书重新通过。详见[V53对照](../results/task4_v53_istanbul_coverage/README.md)。以下版本说明保留为历史记录。

V52新增[含特许学校的NYC毕业结果诊断](../results/task4_v52_nyc_county_outcomes/README.md)：五县毕业届78918人、63878名文凭毕业生、56名未分类残差。独立毕业维度β=0.10时，同目标结果未知→纳入官方计数使NYC第21→第4，可能冠军仍25城；旧不含特许学校表在此情景亦第4。该地方文凭与教育问责范围保持条件分析，十指标主模型及NYC第21不变。Phoenix新增三校11年级成绩不替代教师人数比。

V51新增[证据撤回审计](../results/task4_v51_evidence_withdrawal/README.md)：固定α=0.10下撤回任意单个有信息单元仍推荐Singapore，6555对中12对切换为Tokyo，最小撤回数为2。允许α∈[0.05,0.20]时，撤回Singapore凶杀率在α=0.05即可切换，最小数为1。该假设检验不认定资料错误；实际数据及25城可能冠军均不变。

V50新增[连续推荐证书](../results/task4_v50_continuous_recommendation/README.md)：当前主模型在α∈[0.05,0.20]整个范围内唯一推荐Singapore，遗憾包络的保守分离余量4.0466285分，25城可能冠军不变。[Phoenix同年1180人学区上界](../results/task4_v50_phoenix_cap/README.md)在独立公校FTE目标下使Phoenix由第23至第20；保留学区包含关系条件，不替换当前主模型的第24或其教育定义。

V49新增[年份与行程目的审计](../results/task4_v49_evidence_audit/README.md)：Phoenix取得2023–24历史人数83，未用于填补2024–25；São Paulo的15条未知行程均有工作或私人事务停留，可恢复0条。重算全部名次与可能冠军不变，当前公式及V48入口继续适用。

V48历史条件入口为[saopaulo_age_bounds()](../scripts/task4_saopaulo_age_revision.py)：在V47上将São Paulo从全年龄高中生调整为实际14—18岁当前高中在读者。原始年龄筛选得到1690人，1489人有核验通学、201人未知；同一配对家庭重抽样得到通学包络[0.4417949654,0.6071350870]。São Paulo仍第7，Singapore第1、Tokyo第2、Phoenix第24，可能冠军25城；其余249格不变。镜像来源与探索性抽样条件保留，不称设计有效置信区间。详见[V48对照](../results/task4_v48_saopaulo_age/README.md)。

V47历史条件入口为[tokyo_coverage_bounds()](../scripts/task4_tokyo_coverage_revision.py)：在V46上纳入Tokyo六年制中等教育学校高中部3435名学生，学生总数306903；全校555名本务教师的高中部归属未知，保留H∈[0,555]。教育效用为15(19446+H)/(306903+15(19446+H))∈[0.4872927014,0.4943254278]。Tokyo仍第2、Singapore第1、Phoenix第24，可能冠军25城；其他249格不变。见[V47覆盖及范围对照](../results/task4_v47_tokyo_coverage/README.md)。通信制等其他课程未全部纳入，跨城范围条件保留。全城教育与通学完美补数证书在V47下仍为固定权重至少20城、连续偏好25城必然保留。

V46历史条件入口为[tokyo_bounds()](../scripts/task4_tokyo_official_revision.py)：Tokyo高中师资更新为2025年303468名学生/19446名本务教师；143所获认可大学总部与同日人口形成高教资源效用下界0.500804807，上界仍1。接受总部定位规则时，Tokyo第3→第2，Singapore仍第1，Phoenix第24，可能冠军25城。原有真实高中生通学和缺失区间保留，其他248格不变。[V46对照](../results/task4_v46_tokyo/README.md)分开报告年份、资源及撤回情景，继续保留跨城范围条件。变量代码research_he_density沿用历史名称，指标不限定研究型大学，也不测科研质量。

V45补数证书在V46输入下重算：全25城教育与通学精确补数后，固定α=0.10至少20城必然保留，连续α∈[0.05,0.20]仍保留25城。下面V45的共同权重余量及V44、V23数据均为相应历史版本结果。

V45新增[补数能力证书](../results/task4_v45_acquisition_limits/README.md)，在其V44基准上：即使所有25城的教育与通学单元都在现有区间内精确测定，允许辅助权重α∈[0.05,0.20]时仍不能排除任何城市。α=0.20提供共同见证，最小正余量为0.049194分。固定α=0.10时至少20城必然保留。继续补这两类数据有助于得分和名次，但缩小当前冠军集合还需要其他维度的证据或经验证的结构修订；不应为了减少候选而直接改权重。

V44历史条件入口为 [melbourne_bounds()](../scripts/task4_melbourne_observed_travel.py)：在V38上新增实际停靠记录核验，将7个未明确中学终点的通学效用恢复为[0,1]。同一线性jackknife规则下，Melbourne通学界由[0.278896,0.781095]改为[0.239800,0.792787]，仍第4；Singapore仍为最坏遗憾首选，Phoenix仍第24，可能冠军仍25城。其余249格保持V38。详见[V44同口径对照](../results/task4_v44_melbourne/README.md)。下列V23—V39数值与入口保留为历史对照。

V23十指标基准推荐 Singapore：最小最大遗憾为 28.173588 分，25 城仍全部是可能冠军。这里的推荐是在现有证据区间下选择最坏遗憾最小的城市，尚未识别唯一绩效冠军。V23 基准平均得分区间宽度为 37.916339 分；V26 直接重算五个通学尺度后首选保持，但最多 11 城的决策名次改变。

基准入口为 [task4_roster_coverage_comparison.py](../scripts/task4_roster_coverage_comparison.py) 的 `current_bounds(nyc_scope='under19', include_outcome=False, sampling=True)`。它接续已有证据，并更新 NYC、Mexico City 和 Melbourne 通学界。V26 是该基准的参数敏感性分析，不替换其数据范围或评分方法。V7 及其采集阈值属于历史结果。

## 指标、效用与权重

评价 25 个候选城市。八项主指标为凶杀率、PM2.5、生活成本指数、房价收入比、高中学生／教师人数比、经核验高等教育机构密度、学生通学、固定宽带速度；两项辅助指标为公共交通密度和公共泳池密度。[评分实现](../scripts/task4_v5_model.py) 的 `SPEC` 保存方向与固定锚点，`weights()` 定义：

$$w_j=\begin{cases}(1-\alpha)/8,&j\text{ 为主指标},\\\alpha/2,&j\text{ 为辅助指标},\end{cases}\qquad \alpha=0.1.$$

即主指标各 0.1125、辅助指标各 0.05。除通学外，非负原值 $x$ 按指标锚点 $a>0$ 转为成本效用 $u^-(x)=a/(a+x)$ 或收益效用 $u^+(x)=x/(a+x)$。通学直接使用 $u(t;\tau)=\exp(-t/\tau)$，$t$ 为学生通学分钟数，基准 $\tau=30$；它不再经过上述收益变换。

每个城市—指标保留效用界 $[l_{ij},h_{ij}]\subseteq[0,1]$。完全未知保留 $[0,1]$；部分设施名录仅支持收益下界。部分辖区事件数 $d$、完整地域人口 $P$ 给风险率下界 $x_L=10^5d/P$，对应成本效用界 $[0,a/(a+x_L)]$。数据准入、地域与分母条件随原始证据保留。

## 通学区间与人群范围

对学生权重 $p_r$ 和个体效用界 $[l_r,h_r]$，已知成员的加权识别界为

$$\underline T=\frac{\sum_r p_r l_r}{\sum_r p_r},\qquad
\overline T=\frac{\sum_r p_r h_r}{\sum_r p_r}.$$

已观察时长直接取指数效用；时间箱 $[a_r,b_r]$ 转为 $[e^{-b_r/\tau},e^{-a_r/\tau}]$；未知时长保留 $[0,1]$。Mexico 另对可选成员资格取极值：已知成员权重 $N$、分子界 $[A,B]$，可选成员权重 $v_r$、效用界 $[a_r,b_r]$，则

$$\underline T=\min_{z_r\in\{0,1\}}\frac{A+\sum_r z_rv_ra_r}{N+\sum_r z_rv_r},\qquad
\overline T=\max_{z_r\in\{0,1\}}\frac{B+\sum_r z_rv_rb_r}{N+\sum_r z_rv_r}.$$

默认 NYC 为 under19、2010—11 年历史日记；Mexico 为 2020 年未成年条件范围，当前高中阶段依赖已完成学段／年级进阶假设；Melbourne 为 Greater Melbourne、Secondary 在读且 15—19 岁，尚未单独识别高中年级。Melbourne 名册中170名有个人权重者含107名有旅程和63名无旅程者。V44进一步核验其中100个中学终点，另外7人的终点未明确，连同63名无旅程者保留[0,1]。使用第一条教育旅程与10组官方个人重复权重。端点抽样包络采用

$$SE(\theta)=\sqrt{\frac{9}{10}\sum_{r=1}^{10}(\theta_r-\theta)^2},\qquad
[\max(0,\underline T-t_{9,.975}SE(\underline T)),\min(1,\overline T+t_{9,.975}SE(\overline T))].$$

Sao Paulo在V48使用实际14—18岁当前高中在读，保留镜像来源及探索性抽样条件，Singapore 保留阶段混合条件。NYC 和 Sao Paulo 的家庭重抽样为探索性；Melbourne 为近似端点推断。城市年份、地域和学段不统一，未构造全城市联合置信区域；V23 与 V26 输出均标记 `main_admitted=false`。具体来源与审计见 [V23 报告](../results/task4_v23_roster_coverage/README.md) 和 [V26 报告](../results/task4_v26_direct_travel_scale/README.md)。

## 评分与决策

对效用向量 $u_i$，以固定理想点 1、负理想点 0 计算

$$D_i^+=\sqrt{\sum_jw_j(1-u_{ij})^2},\qquad
D_i^-=\sqrt{\sum_jw_ju_{ij}^2},\qquad
S_i=100\frac{D_i^-}{D_i^++D_i^-}.$$

评分对各收益方向效用单调；在矩形不确定性集合（允许端点同时实现）下，城市得分界为 $L_i=S(l_i)$、$U_i=S(h_i)$。可能冠军集合、最大遗憾和推荐为

$$\mathcal C=\{i:U_i\ge\max_{k\ne i}L_k\},\qquad
R_i=\max(0,\max_{k\ne i}U_k-L_i),\qquad
\mathcal I^*=\arg\min_iR_i.$$

决策名次按 $R_i$ 从小到大排列，并列取最小名次；它不是已识别的真实绩效名次。[区间决策实现](../scripts/task4_interval_decision.py) 与 [V23 排名](../results/task4_v23_roster_coverage/ranks.csv) 可复核结果。

## 当前结果与敏感性边界

V23 默认十指标情景对应输出筛选 `model=v16_ten_criteria`、`nyc_age_scope=under19`、`scenario=both_sampling_envelope`。250 个效用单元中 111 个较完全未知区间有信息；Singapore、Melbourne、Phoenix 的决策名次分别为 1、4、24。完整 [效用界](../results/task4_v23_roster_coverage/utility_bounds.csv) 与 [摘要及输入哈希](../results/task4_v23_roster_coverage/summary.json) 记录基准。

[V26 脚本](../scripts/task4_direct_travel_scale.py) 在 $\tau\in\{15,20,30,45,60\}$ 分钟下，从现有学生时长和原始分箱直接重算五城通学界，保留成员资格、个人权重与原抽样方法；其余 20 城通学未知区间及所有非通学单元保持不变。30 分钟逐单元复现 V23，无新增观测。

| 通学尺度（分钟） | 首选 | Phoenix 决策名次 | 相对 30 分钟改变名次的城市数 | 可能冠军数 |
| --- | --- | ---: | ---: | ---: |
| 15 | Singapore | 24 | 9 | 25 |
| 20 | Singapore | 24 | 7 | 25 |
| 30 | Singapore | 24 | 0 | 25 |
| 45 | Singapore | 24 | 9 | 25 |
| 60 | Singapore | 24 | 11 | 25 |

表中固定 $\alpha=0.1$；连续 $\alpha\in[0.05,0.20]$ 的可能冠军可行性检验也保留全部 25 城。该结果不证明连续 $\tau$ 范围内首选始终不变。数据见 [V26 排名](../results/task4_v26_direct_travel_scale/ranks.csv)、[通学界](../results/task4_v26_direct_travel_scale/travel_bounds.csv) 与 [摘要](../results/task4_v26_direct_travel_scale/summary.json)。

`include_outcome=True` 是另列的十一指标情景：原十项权重乘以 $1-\beta$，毕业结局效用 $q$ 以权重 $\beta=0.1$ 加入同一距离公式。该情景最小最大遗憾为 32.898359，Melbourne 第 5；它不属于上述十指标基准或 V26 检验。

## V29：最新教育年份替换情景

[同口径年份更新](../results/task4_v29_education_year/README.md)将Jakarta的SMA师生比替换为2025/26学年的186461/11983，教育效用为0.4908302977。入口为[updated_bounds()](../scripts/task4_education_year_update.py)，其余249个单元及上述公式保持。Jakarta仍第17，Singapore仍为推荐，可能冠军25城。旧基准函数保留，两个年份不取交集；来源仍是明确标记的官方索引表转录，未增加城市指标覆盖，也未据此改动论文。

## V30：真实高中通学及抽样设计修订

最新条件入口为 [cape_bounds()](../scripts/task4_cape_town_revision.py)，在V29上只更新Cape Town通学一格。官方GHS2023实际包含159名14—18岁、当前10—12年级且非远程学生。保留时间分箱，并用完整217个PSU、14层计算比率端点的Taylor标准误，零目标学生的PSU也参与方差计算。端点采用Bonferroni调整后的近似联合95%包络：

$$[\max(0,\underline T-t_{203,.9875}SE(\underline T)),\min(1,\overline T+t_{203,.9875}SE(\overline T))] = [0.4067375294,0.7977951321].$$

方差公式与抽样范围见[数据说明](../data/task4_v30_cape_town/README.md)。权重、评分和决策公式不变，其余249格不变。Cape Town得分界由[33.019656,73.255944]变为[35.638820,72.191687]，最坏遗憾决策名次13→5；9城名次变化，Kendall tau=0.946667。Singapore仍为推荐，Phoenix仍第24，可能冠军仍25城。全年龄当前高中生189人的敏感性情景同样得到Cape Town第5。

这是2023年调查覆盖总体下、固定校准权重的近似推断，不覆盖学生宿舍等集体住户，也不是全城市联合置信保证；`main_admitted=false`保留。[完整前后对照](../results/task4_v30_cape_town/README.md)记录来源哈希和复现命令。证据改善了通学界与决策信息，尚未缩小可能冠军集合。

## V32：高中师资分母界与年份替换

最新条件入口为[school_bounds()](../scripts/task4_school_stage_revision.py)。Shanghai以2025学年235542名普通高中学生/23999名专任教师替换旧年份。Warsaw青年普通高中87999名学生的教师分配未知，但不超过全部普通高中6080 FTE（含1 FTE发布精度保护），因此教育效用界为[0,15/(15+87999/6080)]。青年与成人教师分配保留未知，FTE与人数口径差异明确保留。

两项修订只影响对应教育格。Warsaw得分上界74.317458→70.291549，排名仍13；Shanghai仍6。Singapore推荐、Cape Town第5、Phoenix第24和25个可能冠军不变。公式及权重保持上述定义，详见[V32对照](../results/task4_v32_school_stage/README.md)。

## V34：Delhi当前高中任课教师人数

当前条件入口为[delhi_bounds()](../scripts/task4_delhi_school_revision.py)。新增2024/25官方11–12年级学生603437/参与高中教学教师30186的精确人数比19.990624793，教育效用0.4286862578。教师含跨学段任教者，不是FTE。另以26766+3420c、c∈[0,1]作为分母检验兼教教师贡献假设，主模型仍使用实际任课人数。

Delhi得分界由[30.035171,67.970666]变为[32.868011,63.895479]，决策名次18→14；兼教贡献敏感性为第15。Singapore推荐、Phoenix第24及25个可能冠军保持。其余249格和上述评分公式不变。[完整对照](../results/task4_v34_delhi_school/README.md)保留范围、验证与原件链接。


## V38：Singapore预科学生覆盖与教师分配

[官方原件及提取器](../data/task4_v38_singapore/README.md)确认2024年预科学生25130人，其中748名专门独立学校学生未进入旧匹配子集。报告将该类学校404名教师列在中学栏，允许按任教学段或受训学段分类。保留原1979名报告预科教师口径，对新增学生对应的教师分配量设：

$$H\in[0,404],\qquad u_E(H)=\frac{15(1979+H)}{25130+15(1979+H)}\in[0.5415488461,0.5871868583].$$

这是报告教师人数条件下的分配区间，包含兼职，不是FTE或完整教师分类误差界。只替换Singapore教育格，通学数据、其他249格、权重和评分公式保持不变。旧匹配子集与扩展总体单列对照，不以两者相交缩窄区间。

Singapore得分界从[49.355873,66.310978]变为[49.292136,66.703329]，决策排名仍1；可能冠军仍25。撤回其教育证据、恢复[0,1]时，Singapore仍是首选，得分界[45.062720,69.668819]。本轮改善了学生覆盖和不确定性的表达，并未缩小冠军集合。详细对照见[V38结果](../results/task4_v38_singapore/README.md)。

[Toronto官方同年财务报表](../data/task4_v38_toronto/README.md)取得四学区高中学生与教师FTE，但法语学区跨市、人口及教师口径尚待统一，未准入城市单元。[Copenhagen当前高中生筛选变量](../data/task4_v38_travel/README.md)已核对，尚无城市通学估计，缺失界保持。


## V39：采集精度与所需指标数

主模型仍为V38，真实排名及可能冠军集合不变。[有限精度诊断](../results/task4_v39_finite_precision/README.md)将Phoenix所选指标的假想区间设为[l,l+ρ(h−l)]，对连续辅助权重[0.05,0.20]枚举最少采集集合。残余宽度0—2.5%的已检验情景需4项，5%、10%、20%需5项；50%时全部7个未知指标仍不足以排除其冠军可能。ρ同时限定结果位置与剩余宽度，不是采集成功概率、原始单位误差或置信水平。原有精确下端点方案属于ρ=0特例；所有情景不写回证据矩阵。


## V86：高中学习成果与缺失核查

[本轮对照](../results/task4_v86_intake/README.md)取得Bogotá当前10—11年级1399人的真实PISA微观结果，保留10个合理值和80个重复权重。Phoenix同年学区总量仍不能识别缺失教师上界；Barcelona步行GPS汇总只作隐私截短诊断。主模型仍为V79，250格、全部排名及25个可能冠军不变。
