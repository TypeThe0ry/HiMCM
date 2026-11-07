# 更新中学生师比，并与2023年凶杀率对应

下载及整理日期：2026-11-07。建议直接使用 **[Excel工作簿](homicide_2023_updated_secondary_ratio.xlsx)** 或 [严格2023年完整配对CSV](matched_2023_complete.csv)。上一版原始官方生师比及历史面板仍完整保存在相邻 [country_year_homicide_education](../country_year_homicide_education/) 目录。

## 这次更新了什么

旧的世界银行 `SE.SEC.ENRL.TC.ZS` 普通中学生师比序列仍停留在2019年，但其两个基础计数已经更新：

- [中等教育学生总数 SE.SEC.ENRL](https://data.worldbank.org/indicator/SE.SEC.ENRL)。
- [中等教育教师总数 SE.SEC.TCHR](https://data.worldbank.org/indicator/SE.SEC.TCHR)。

世界银行元数据说明两项新计数来自 **UIS 2026年2月发布版本**，世界银行获取日期为2026-03-19；本次下载的WDI文件更新日为2026-10-08。它们已含2023、2024及部分2025年的国家数据。

本项目用 **同一国家、同一年学生总数÷教师总数** 计算更新的中学生师比，字段名明确为 `secondary_pupil_teacher_ratio_derived`，来源类型为 `derived_from_official_counts`。**它是根据官方计数计算的派生值，不是旧官方比率序列发布的新观测。** 不将新值混填进旧官方序列。

## 2023年对应结果

| 覆盖项 | 国家和地区数 |
|---|---:|
| 有2023年凶杀率 | 83 |
| 有2023年学生总数及教师总数，可以计算生师比 | 125 |
| 凶杀率和派生生师比均严格为2023年 | **59** |
| 另允许2021—2025年邻近教育数据，凶杀率仍只用2023年 | **67** |

总范围仍为世界银行列出的217个国家和单列地区/经济体，排除世界、区域和收入组等汇总。“125”和“59”来自本次下载实数，不保证全体国家数据齐全。2023年凶杀率沿用上一版原始WDI下载，未用其他年份补凶杀率。

**主分析优先使用严格2023年的59条完整配对。** 邻近年份补充表的67条完整配对中，教育年份分别为：2023年59条、2022年4条、2021年2条、2024年2条。其余国家仍缺失，未插值或补零。

额外8条的实际年份如下，不应称为严格2023年观测：

| 国家或地区 | 教育年份 |
|---|---:|
| Algeria | 2024 |
| Colombia | 2022 |
| Estonia | 2021 |
| Honduras | 2022 |
| Ireland | 2022 |
| Nigeria | 2021 |
| Puerto Rico (US) | 2024 |
| Serbia | 2022 |

## 文件和字段

Excel含“2023同年完整”“2023全部国家”“邻近年份补充”“近年教育明细”“年度覆盖”“方法与限制”“数据来源”工作表；具有中文表头、筛选和冻结窗格，计数与比率存为数值，默认显示六位小数。

| 文件 | 用途 |
|---|---|
| [matched_2023_complete.csv](matched_2023_complete.csv) | 59条严格同年完整配对，优先使用 |
| [countries_2023_all.csv](countries_2023_all.csv) | 全217个国家和地区的2023年情况，保留缺失 |
| [nearby_years_2021_2025.csv](nearby_years_2021_2025.csv) | 全217个国家和地区的邻近年份补充，67条完整配对；其余行保留缺失 |
| [secondary_counts_ratios_2018_2025.csv](secondary_counts_ratios_2018_2025.csv) | 217×8年网格，共1,736行；含原始学生数、教师数、派生比率、UIS旗标和数值核对状态 |
| [year_coverage.csv](year_coverage.csv) | 每个教育年的数据覆盖及其与2023凶杀率的交集 |
| [uis_observation_notes.csv](uis_observation_notes.csv) | UIS两项计数2018—2025年的2,779条原始观测元数据，保留估计、来源等文字 |
| [method_notes.csv](method_notes.csv) | 中文方法和限制说明 |
| [summary.json](summary.json) | 覆盖统计与验证摘要 |

CSV采用UTF-8 BOM和LF换行，保留官方计数与凶杀率原始数值字符串。派生比率按十进制除法计算并保存15位有效数字；不将显示的小数位误当原始测量精度。

关键字段：

- `wb_country_code`：世界银行三位代码，通常对应ISO3，但不保证每个代码属于ISO标准。按代码匹配，不按名称模糊匹配。
- `homicide_year`：固定目标年2023；`homicide_rate_per_100k`为每10万人故意杀人受害者数。数值为空表示2023年没有观测。
- `education_year`：严格表固定目标年2023，即使该国计数缺失也仍标2023；邻近表记录所选实际教育年，没有可用计数时为空。
- `secondary_students`、`secondary_teachers`：相同国家、相同教育年的发布计数。
- `secondary_pupil_teacher_ratio_derived`：学生总数÷教师总数，学生/教师。教师数缺失、为0或明确不适用时不计算。
- `education_year_gap`：教育年份减2023，只在派生比率存在时填值。
- `education_after_homicide`：1表示教育年晚于2023，0表示不晚于2023，缺失时为空。
- `pair_status`：`exact_2023`=严格同年完整；`nearby_year`=邻近教育年且2023凶杀率有效；`homicide_missing`、`education_missing`、`both_missing`分别标明缺失。
- `ratio_origin`：比率存在时为 `derived_from_official_counts`，否则为空。
- `uis_reference_status`：`both_counts_agree_within_tolerance`表示两项WDI计数都与UIS摘录数值在容差内一致；`incomplete_reference`表示两项核对未全部具备，不意味着比率必然有效。
- `students_magnitude/qualifier`、`teachers_magnitude/qualifier`：UIS数值旗标原样保留；空白不保证不存在估计或其他统计限制。

## 时间与口径规则

1. 邻近年只从2021—2025中选择，按距2023绝对年差最小选取；距离相同优先较早年，即 **2023→2022→2024→2021→2025**。学生和教师不能跨年相除。凶杀率始终只取2023，不替换成邻近年。
2. 2024年的两条是晚于凶杀率的教育数据，只用于补充或敏感性分析；若用来预测2023年凶杀率，应排除这些未来信息。它们不会出现在严格2023年完整表。
3. 两项计数覆盖中等教育整体（ISCED 2+3，公私立），不把“仅初中”“仅高中”“仅合格教师”的比率自动补进来。生师比也不是平均班级人数。
4. 教师数定义包括全职和兼职教师，并排除没有教学职责的人员；但各国人数与全时当量（headcount/FTE）的处理可能不同。**本次保留发布计数口径，不声称是统一FTE比率，也不保证与旧官方生师比序列完全等价。** 分层OECD/Eurostat比率没有直接混入本表。
5. 教育跨年学年通常以结束年标记，所以“同年”是国际数据库参考年一致，不表示教育调查期与凶杀率日历期逐日相同。国家数据不能自动替代具体城市数据。
6. UIS原始数值字段 `MAGNITUDE` 为 `NA`、`SUPP`、`INCLUDED` 时不计算比率；元数据 `Data Status:Data reporting` 的文字 `NA` 不能误判为数值缺失。当前选中两项计数的全部1,920条UIS记录，其数值旗标 `MAGNITUDE` 和 `QUALIFIER` 均为空；仍保留观测元数据以供核查。

官方定义：[WDI学生数元数据](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SE.SEC.ENRL)、[WDI教师数元数据](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SE.SEC.TCHR)。原始HTML也已归档。

## 来源、原始档案与Overleaf大小限制

[download_manifest.json](download_manifest.json)保存每份原始档案URL、获取时间（如适用）、字节数及SHA-256。`raw/`保存：

- WDI学生数、教师数、凶杀率和旧官方生师比的原始ZIP，ZIP内包含官方国家及指标元数据；国家API JSON。凶杀率、国家API、旧比率ZIP从上一版原样复制，并记录复制来源。
- WDI学生数和教师数定义的原始HTML。
- UIS官方2026年2月OPRI包的选定计数与观测元数据摘录ZIP。完整上游包68,300,100字节，**仅在仓库外临时下载，未上传GitHub**，避免Overleaf单文件50MB限制。
- 新加坡官方中学PTR JSON，用于有限的独立旁证。

UIS摘录来自 [官方OPRI.zip](https://download.uis.unesco.org/bdds/202602/OPRI.zip)，筛选 `INDICATOR_ID∈{20082,20182}` 且 `2018≤YEAR≤2025`，保留全部国家行及其原始数值、旗标和元数据文字。选中数据1,920条，元数据2,779条；两份CSV按原字段重新序列化为LF换行。国家表、完整指标标签表、发行说明三个ZIP成员保留原字节。**摘录ZIP是本项目筛选产物，不冒称完整官方原包。** 完整原包SHA-256及大小在manifest的 `upstream_uis_archive` 中可核验；摘录ZIP约52KB。

许可：WDI两个计数页面为 **CC BY 4.0**；UIS上游README声明 **CC BY-SA 3.0 IGO**，摘录保留发行说明和来源。引用请同时注明UNESCO UIS、WDI、具体计数代码、本项目派生公式和下载日期。

## 校验与复现

已完成：全部原始文件字节数和SHA-256、国家API完整性、指标代码、国家唯一性、同国同年计算、零分母与缺失保护、CSV回读、Excel全部数值与空白回读、年度覆盖一致性。另有1,873条WDI国家计数与UIS原始摘录逐条核对，相对/绝对容差均为1e-7（允许发布舍入差异），没有实质不一致。

新加坡2023年的派生值为 `163746/13601=12.0392618189839`，四舍五入一位小数为12.0，与 [SingStat/MOE官方数据API](https://data.gov.sg/api/action/datastore_search?resource_id=d_9a283a2aa12aa018759cb4bb753a2ca6&limit=100) 的中学PTR一致。这只是旁证；不同教育系统层级边界不能仅凭四舍五入相同就认定完全一致。

离线重建（仓库根目录）：

```bash
python3 -m pip install -r research/2026-a/data/homicide_2023_secondary_ratio_updated/requirements.txt
python3 research/2026-a/scripts/build_homicide_2023_updated_education.py
```

加 `--csv-only` 时不需要第三方依赖。构建脚本复用上一版的原始WDI解析与CSV写出函数，不改写上一版数据。

若要从完整UIS原包独立验证摘录，先将官方包下载到**仓库外**，再执行：

```bash
python3 research/2026-a/scripts/extract_uis_secondary_snapshot.py /absolute/path/outside_repo/OPRI.zip
```

该脚本核验完整原包SHA-256，重新执行筛选，并逐字节核对摘录内所有成员；加 `--write-to /new/path/excerpt.zip` 可输出新摘录，拒绝覆盖已有文件。下载URL与所有来源文件均在manifest中列明；重建固定归档快照，不把未来数据库改版静默混入本版。
