# V184：工作通勤原记录核实与来源政策检验

当前科学／既有扩展V181保持，自有独立稿已更新为V184。新取得与Dublin28.8分钟／2011、Zurich39.9分钟／2024精确匹配的Eurostat原始记录，指标TT1019V为工作旅程均值。当前标签均为greater city，Zurich带e（estimated），同响应的60.41公共交通份额亦匹配原表。原始CSV未提供抄录链，数值相同不证明用户来源传递链、历史市界或高中学生分布；人口字段city proper也不能说明每项指标的地理范围。用户均值、年份、标记及全部160效用界均保持，没有把ok静默改为e，没有准入新数值或收窄基线。

## 会改变推荐的来源政策

独立计算五组情景、两个权重参考，共160城市评分行及800效用界行：

| 诊断情景 | 原权重保守推荐 | 等权保守推荐 |
| --- | --- | --- |
| 保留原输入 | Zurich | Zurich |
| 仅撤回Zurich工作通勤代理 | Singapore | Zurich |
| 仅撤回Dublin工作通勤代理 | Zurich | Zurich |
| 撤回两项代理 | Singapore | Zurich |
| 撤回全部12项用户通勤均值 | Singapore | Zurich |

撤回是把所选旅时效用设为[0,1]，其余格保持；更广的12项检验保留Singapore独立的2020学段分布代理，未选择性删除它。所有情景仍16可能／0必要冠军。基线仍是Zurich保守推荐，固定均宽16.049384792、等权18.837940743，23补充、112点／35部分／13全缺失。新结果揭示接受通勤代理的决策后果，不能说Singapore是新的确定冠军，也不能把撤回当成官方替代值。

## 原件与未准入数据

`data/task4_v184_dublin_commute`保留Eurostat IE001C/2011原JSON与2004官方手册；手册仅为历史方法背景，不证明2011实际调查实现。`data/task4_v184_zurich_commute`保留CH002C/2024、全市字典和初次CH001C响应；当前CH001C实际为Bern，必须按响应字典核名，不能沿用旧代码表。CH002C=39.9e，无匹配时长分箱，仍不识别高中通学。

Helsinki2024年报教学人员684+103=787是人数，不是教学FTE；脚注含休假／替代等、排除兼职小时教师。学生9374/1377是20.1与20.9加权数；98人年属于青年工作坊而非教师。该新路线与OPH人数导航均未形成匹配市域教师分母，0准入。三包共8份HTTP200原件的长度／SHA已核，不将身份核验冒充口径可用证明。

## 稿件与复现

Overleaf自有入口`drafts/task4_v184_paper.tex/.pdf`、根代理`task4_v184_review_entry.tex`，由`build_task4_v184.py`基于冻结V182构建。只更新来源段、同节来源政策检验及相应摘要／结论／新闻稿和一条Eurostat参考；图表／既有数值资产保持。AI仅把已知Codex使用日期延伸至8—10日，固定捕获窗口、74旧上下文、326可见／1865工具输入及全队历史不完整状态保持。

27页=25正文参考+2暂定AI，53引用、新闻18—19／AI26—27、主文余量0。原生mcmthesis摘要及Team # PENDING左页眉／Page x of27右页眉／空页脚保持，默认Main和队友main/ref/class未改。零overfull、两处继承underfull已实看。47项交付映射保留13项实质待办，不称最终参赛完成。

研究结果及核验在`results/task4_v184_source_review/`；运行`task4_v184_commute_withdrawal.py`、`audit_task4_v184.py --expect-active`复核，均用仓库`.venv-v120/bin/python`且脚本前加`research/2026-a/scripts/`。新稿编译的scratch路径与视觉核验见verification.json。既有`task4_v182_reproduce.py`按当前注册表动态重建V181科学基础上的当前稿，可用于V184；其runner版本字段不等同论文版本。双仓同步与隔离重建回执完成后记录于本目录。

下一轮不要重复寻找28.8/39.9的数值匹配，也不要把CH001C当Zurich。继续只找匹配人群／年份的时长分布或市域实际教学FTE；没有新口径证据就跳过。控制号、全队AI原记录、最终团队整合与在线编译／比赛提交回执仍需真实证据。长期goal active。

隔离重建已通过：从Overleaf载荷08dfde6的735个Git文件／blob核验生成两个隔离副本，已有本地工具和TeX缓存离线编译；27页逐页文本及72dpi灰度像素与登记PDF一致。独立复算当前160格／32权重城市案例，输入保护243科学／735论文无变化。reproduction.json中的runner iteration V182是复现工具版本，paper_version明确V184；不作冷环境或服务器验证。

双仓远端已核：GitHub载荷`fc6938bbe6ea5dae030afc1bbd27d2d1243bce55`，Overleaf`81ab5cffaefdbc24d7454f87adb8b716f5fd6899`，均普通push且核验时工作区干净；PDF SHA `4f373582a809581b463a58e2bb3208df4fff028255d6b8cf275c45247a6c0a0f`。10份选定证据逐字节一致，另1份目的地README；711旧论文文件保持、仅两导航获准更新。详sync.json、delivery.json，回执另提交；不声称在线编译或比赛提交，长期goal active。
