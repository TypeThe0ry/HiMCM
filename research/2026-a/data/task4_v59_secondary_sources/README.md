# V59：Lagos真实高中统计表与Dhaka新原件

取得尼日利亚教育部DNEMIS公开门户使用的8份原始Parquet表，新增可追溯的Lagos State高中阶段计数。门户标示学年2024/25，底层年度字段2024，页面生成时间2026-09-22；不是把生成日期当观测年份。数据入口为[官方Lagos页](https://emis.education.gov.ng/portal/asc/state-H2ZhSMudlMI/)，其公开客户端引用`/portal/data/manifest.json`及数据表，原件和发现路径已归档。

| 字段及范围 | 人数或学校数 |
| --- | ---: |
| SSS阶段学生，公私合计 | 413720 |
| 公立SSS阶段学生 | 268413 |
| 私立SSS阶段学生 | 145307 |
| SSS学校类型的MD教师数，交叉表仅列Public | 8920 |
| Private学校类型的教师池，所有学段合并 | 104805 |
| 公立SSS实际/预期报告 | 329 / 333 |
| 私立全学段实际/预期报告 | 10213 / 11922 |

20个LGA的SSS学生和公立SSS教师字段均与州汇总相等。**不能用413720除以8920**：前者含私立高中学生，后者所在学校类型仅覆盖公立。私立104805名教师没有高中阶段分配。即使268413/8920约30.091，也只作算术诊断；教师字段为`MD: Total teachers`，尚未证明其人员总体与329所报告学校的学生总体完全对应。

这批计数覆盖的是报告资料，缺报学校未记作零，85.2%的全州全学段报告率不能当作高中学生覆盖率。Lagos State与模型中城市地理范围的映射也未确定。因此本轮不填入全市高中PTR，主模型缺失区间保留。新数据的作用是提供真正的学段、公私立与LGA明细，为下一轮配对分母及报告覆盖提供入口。

`audit_lagos.py`校验14份原件哈希、年度、分项、学校类型与所有权交叉、20个LGA加总和报告计数，输出`lagos_lga_sss.csv`及`lagos_audit.json`。运行需要pandas和pyarrow；本次使用临时依赖目录`/tmp/himcm_v59_arrow`，没有修改项目或系统依赖。`lagos_queries.json`是从原HTML内嵌查询提取的派生文件，其余脚本、HTML、Parquet按原字节保存。

另从[BANBEIS官方2025统计出版页](https://banbeis.gov.bd/pages/files/annual-education-statistics-2026-6iav4j-6abb61ee54b917a30a16991c)取得18,873,871字节的`bangladesh_education2025.pdf`，来源和哈希记在`manifest.json`，交由主agent继续核查Dhaka城市及高中口径；本目录本轮未从该PDF生成模型观测。没有修改论文。
