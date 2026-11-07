# Phoenix：Valley Metro 2023 OD调查字段核查

新取得[Valley Metro 2023 Origin and Destination Survey报告](https://vulcan-production.nyc3.cdn.digitaloceanspaces.com/pages/downloads/about/agency/surveys-studies/origin-destination-surveys/2023-od-report_11-7-23_sb.pdf)完整原件，5,077,739字节、103页。报告署名Valley Metro及ETC Institute；同一CDN链接被[National Academies参考文献](https://www.nationalacademies.org/read/29221/chapter/8)引用。官方目录页返回403，CDN原件HTTP200；[manifest](manifest.json)记录来源、访问状态及哈希。

这是区域公共交通乘客OD调查，有实际问卷，覆盖不同公交与轨道服务。它提供比全年龄员工TRP更相关的学生渠道，但目前仍不能作为Phoenix高中生家到校时长输入：

| 已核验定义 | 具体限制 |
| --- | --- |
| PDF第71页／印刷66页 `STUDENT_STATUS` 的学生类型包含K–12 | 未单列当前9–12年级；年龄不能直接代替在读学段 |
| PDF第72页／印刷67页 `YOUR_AGE` 为under16、16–18等组 | 无法单独识别14–15岁 |
| PDF第59页／印刷54页地点类型为K–12学生学校 | 未区分小学、初中与高中 |
| `TIME_ON`为登车时钟；`OPPO_DIR_TRIP_TIME`为反向行程出发时钟 | 不是同一次家到校行程的出发、到达时间对，不能相减得到通学时长 |

手工阅读报告数据字典（印刷53–70页）未找到可直接计算完整家到校时长的字段；这不是对所有未公开后台数据的不存在证明。问卷PDF第52页已渲染目视核验，学校目的地同样合并K–12。原始个体记录未取得，不能建立城市居民、当前高中阶段、通学时长和覆盖权重的联合筛选。乘客样本还不覆盖步行、骑行或汽车通学者。

**本轮新增可准入通学观测为0，Phoenix现有缺失区间保留。** 后续若取得去标识联合汇总，仍需明确目标学生分母与非公交学生覆盖。仅有登车时钟、线路地址或未来预计到站不能补成实测全程时间。

[dictionary_excerpt.txt](dictionary_excerpt.txt)为相关PDF页的直接文本提取；原件字节不变。`python3 research/2026-a/data/task4_v69_phoenix/audit.py`验证哈希、页数与关键变量定义；没有将简单关键词检查冒充完整变量语义审计。未联系机构、访问学生私人系统、修改模型或论文。
