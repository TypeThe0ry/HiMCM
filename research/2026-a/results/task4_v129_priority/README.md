# V129：当前 V127 的17格缺失数据采集诊断

**优先寻找 Dublin、Zurich 的同口径高中师生比，以及 Warsaw 的真实高中通学与城市公共交通联合证据。** 单格完全识别的条件信息价值仍以 Dublin、Zurich 为首；同城联合缺项中，Warsaw 的两个缺项有最大的乐观最大遗憾减幅。来源是否能达到这些识别条件，需要另外审查。

输入严格为 `task4_user_v127_revision.revised_bounds()`：16城×10指标，112点、31部分区间、**17全缺失**。143个非全缺失格及全部原始界保持不变。两个权重参照都保守推荐 Zurich、16城可能第一、0必要冠军；这项诊断没有补入观测、修改主榜或运行MC。旧 V126 诊断冻结于 V124 的19格，不能充作当前输入。

## 理论信息限与真实来源

令当前最大遗憾最小值为 `r0`。假定一个全缺失效用被精确识别为 `x∈[0,1]`，固定其他全部界，则条件保证减幅为 `r0−max_x r(x)`，最佳可能减幅为 `r0−min_x r(x)`。单位是 TOPSIS 分数点，没有先验、数据获取成功率或真实夺冠概率。

这与真实来源形成的区间不同：公共交通**子集清单**一般给 `[x,1]`；匹配的 PTR 区间须按成本方向反转两端；真实单程旅时**均值**给 Jensen 下界、上界仍1，分箱／分布才可能同时降低上界。端点 `x=1` 可以只是无限密度等原始值的极限，不能据此承诺可取得的改善。

## 当前单格与联合上限

| 全缺失格 | fixed 完全识别的条件保证减幅 | fixed 最佳可能减幅 | 最多排除可能冠军，fixed / equal |
| --- | ---: | ---: | ---: |
| Dublin PTR | 1.066798 | 5.785906 | 1 / 0 |
| Zurich PTR | 0.793974 | 9.316221 | 5 / 1 |
| Helsinki PTR | 0 | 3.990631 | 0 / 0 |
| Madrid PTR | 0 | 3.522989 | 0 / 0 |
| Paris PTR | 0 | 3.418744 | 0 / 0 |
| Vienna travel | 0 | 2.195661 | 1 / 1 |
| Warsaw travel | 0 | 1.645388 | 1 / 0 |
| Berlin transport | 0 | 0.345200 | 0 / 1 |

“最多排除”包括不利证据排除来源城市自己；例如 Vienna travel 的1城上限来自低效用端点，不代表一份提高下界的均值能排除它。全34个单格／权重组合见 [priority.csv](priority.csv)，68个精确端点见 [endpoint_information.csv](endpoint_information.csv)。equal 下 Dublin 的条件保证／最佳减幅为0.044371／0.169330；其他单格保证减幅为0，Zurich 最佳减幅8.524018。

| 同城全部全缺失组合 | fixed 最佳端点减幅 | 乐观高效用端点排除数，fixed / equal |
| --- | ---: | ---: |
| Zurich PTR | 9.316221 | 5 / 1 |
| Warsaw transport + travel | 5.950096 | 1 / 1 |
| Dublin PTR | 5.785906 | 1 / 0 |
| London PTR + transport | 4.001321 | 0 / 0 |
| Milan PTR + transport | 3.799090 | 0 / 0 |
| Tokyo transport + travel | 2.224695 | 0 / 0 |
| Vienna travel | 2.195661 | 0 / 0 |

联合实验只改变**同一城市当前全缺失的格**，不会重设已有部分界；它不代表跨城同时获得完美信息的总上限。London、Milan 的联合证据可改变保守推荐，却不一定缩小可能冠军集合，两种目的应分别评价。完整组合、所有子集和端点保存在 [joint_priority.csv](joint_priority.csv)、[joint_subset_limits.csv](joint_subset_limits.csv)、[joint_endpoint_information.csv](joint_endpoint_information.csv)。

## 可操作的阈值与证据方向

- **Zurich PTR：** 精确识别后，fixed 推荐切换边界为效用约0.0788076，即 PTR 约175.3369。更低效用选择 Singapore，更高效用选择 Zurich，等号可并列。精确极差 PTR 和只提高效用下界是不同信息；只给 `[x,1]` 的下界更新不会令 Zurich 失去当前推荐。要首次排除其他可能冠军，Zurich 效用下界须严格超过0.67088480，相当于匹配 PTR 上界低于7.35853317；这远强于“保持推荐”的条件。
- **Dublin PTR：** 完全精确效用达到约0.460371（PTR约17.582385）时可进入 fixed 最优；保留效用上界1、仅提高下界时，对应阈值约0.359691（PTR上界约26.702472）。两者保留的竞争上界不同，不能互换。排除 Amsterdam 的阈值更高：效用下界须严格超过约0.97345477，即 PTR 上界低于约0.40903638。
- **Vienna / Warsaw travel：** 其他界不变时，fixed 单格下界进入最优所需效用约0.737991／0.789358。若来源是完整匹配人群的实际旅时均值，Jensen 充分条件约为均值小于9.114725／7.096078分钟；这不是一般平均旅时与期望效用的等价关系，更不是观测结果。较差上界、未知质量与开放尾段仍需分箱证据，不能用均值排除城市。
- **Berlin transport：** 单格 lower-only 进入 fixed 最优需效用下界约0.912144，即已核子集密度严格高于约519.113058个设施／10万人；即使极限下的最佳遗憾减幅也只有0.345200。它有完整性价值，但不是当前最强决策杠杆。
- **Warsaw 联合：** 示范路径把交通与旅行的两个效用下界同时设为同一 `x`、各上界仍1，约 `x=0.520816` 可进入 fixed 最优。这个对角路径不要求真实两项相等；实际来源应分别代入各自下界重新计算。

[recommendation_thresholds.csv](recommendation_thresholds.csv) 保存27个推荐边界，按两侧独立范数和自排除遗憾验算；等号可能并列。[exclusion_thresholds.csv](exclusion_thresholds.csv) 保存单格冠军排除边界，严格不等式按完整精度使用。[lower_only_information.csv](lower_only_information.csv) 保存924个下界更新情景，保留上界1，未套用完全识别的保证值。

## 具体搜索顺序与准入门槛

1. **Dublin、Zurich 匹配 PTR。** 寻找新的市内高中学生与实际教师 FTE／明确匹配教师人数的同年、同学段、同提供方汇总，或直接发布的同定义比例。Dublin 2024议会问题仅有提问、部分邮区，需真正回答及人口资格；Zurich canton/public-school staffing 不匹配城市全提供方。已拒收路线见 [V127教育审查](../../data/task4_v127_education/README.md)及[V124审查](../../data/task4_v124_education/README.md)。不重复把区域、分配职位或未答问题当新数据。
2. **Warsaw 通学 + 交通。** 优先新的官方高中居民／学生实际单程时长分箱、未知质量与总分母，再配同市界的已核乘客站点实体子集。只有OD人数、出行方式、工作／大学混合均值或学校最近距离时不填旅行值。联合来源可有价值，即使每项独立的完美信息值较低。
3. **Vienna 新时期真实高中通学。** 当前仅 travel 全缺失；99个metro下界已保护。既有 [2001历史审查](../../data/task4_v127_vienna_travel/README.md)明确0当前准入，不能因本轮理论价值提高而恢复为当前代理。需要新时期、可核迁移或同定义现期资料。
4. **London、Milan 的联合师资／交通；Berlin、Amsterdam、Tokyo 的有界库存路线。** 交通可从官方城市／运营方实体清单、站点层级和市界开始核查，先证明乘客资格与复合体去重，再只提高下界。London 的 NaPTAN access point 行不能直接当站点实体；Tokyo 练马区泳池已是保护部分界，当前联合缺项只有交通与旅行。若师资或旅时资格无法满足，快速记录拒收并跳过。

这些是基于已保存审查的采集方向，本轮没有声称重新访问官方页面、恢复远端接口或取得真实新观测。Helsinki／Madrid／Paris PTR 的单格乐观作用仍高于多数交通项；出现新的同口径来源时可优先复核，不能用旧不匹配数据补格。

## 相对 V126 的真实差异与复现

Prague、Vienna transport 从全缺失任务中移除，现为31个受保护部分界之一。其余17个单格在3项主要信息指标（条件保证／最佳减幅／最大排除数）中，**只有 fixed Vienna travel 的最佳减幅改变：1.713913→2.195661**；其余对应行在数值容差内一致。Vienna 原来的 transport+travel 两格完美对照已不适用，当前单项计算保留真实99站区下界。详细逐行对照见 [V126_comparison.csv](V126_comparison.csv)。主模型仍是 V127，保守推荐和可能冠军集合没有实际改变。

```sh
.venv-v120/bin/python research/2026-a/scripts/task4_v129_priority.py
```

[audit.json](audit.json) 记录3879个独立分数／自排除遗憾／冠军和名次检查、34个独立双分支完美信息优化、420个联合混合坐标探针及27个推荐阈值两侧验算。生产分数与独立加权向量范数核对，权重只乘一次；所有143个非全缺失格均逐次保持。端点上限依赖当前矩形集及单城单调性，不是物理联合可实现性证明。

[summary.json](summary.json) 保存198个保护文件的前后SHA，包括原 CSV、注册表、原快照、全部现有V127／V128研究结果与相关脚本、V127来源包和冻结V126诊断。原V127快照9项逐个匹配，全部160格界前后完全相同；live注册表仅作前后保护，计算读取59edddf中的冻结V127注册表，允许未来版本推进后重放。不覆盖旧priority、主审计、快照或论文。

Berlin100站的只读预评估见[candidate_lower_only_previews.csv](candidate_lower_only_previews.csv)。该文件按未验证候选假设生成，主准入数为0；来源独立审查另见[候选审查](../task4_v129_candidate_review/README.md)，资格结论不反写此历史诊断。
