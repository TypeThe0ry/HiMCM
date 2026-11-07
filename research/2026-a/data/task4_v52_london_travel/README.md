# London候选来源：实际学校旅时表的地域限制

取得DfT官方[NTSQ09082原始ODS](https://assets.publishing.service.gov.uk/media/6a9191fe01bbff0bf8f97b99/ntsq09082.ods)，工作簿更新日为2026年3月26日。它报告实际学校教育旅程时长，而非模拟最近学校可达时间。

| 年份 | 年龄 | 平均分钟/旅程 | 未加权人数 | 未加权旅程（千，原表精度） |
| --- | --- | ---: | ---: | ---: |
| 2023 | 11–16岁 | 23 | 1026 | 6 |
| 2024 | 11–16岁 | 25 | 1145 | 7 |

统计涵盖England，教育旅程须短于50英里，包含去校及返程；时长包括行驶与等待。表内均值经过调查加权，人数与旅程数为未加权样本描述。原表对一处内容误写“percentages”，但列标题和表题明确单位为分钟；保留原件，不改原文。

## 准入判断

该表没有London地域与年龄的联合数据，也没有14–18岁当前高中阶段筛选；不能把England平均值填给London。按旅程汇总的均值亦不同于当前模型的人均通学效用分布。此次London新增准入观察为0，缺失区间保持原状。

[官方专题表目录](https://www.gov.uk/government/statistical-data-sets/ad-hoc-national-travel-survey-analysis)列出了该表。[学校出行目录](https://www.gov.uk/government/statistical-data-sets/nts06-age-gender-and-modal-breakdown)的NTS9908包含地域，但指标为5–16岁交通方式份额，仍不能补旅时。未将方式份额或模拟可达性替换为实际通学分钟。

原始字节和哈希见[manifest.json](manifest.json)，六条全国年龄组观测及范围判断见[audit.json](audit.json)。下一步需要London×当前学段×旅时的联合调查表或可合法获得的相应微数据；重复取得全国均值不能补齐该联合信息。
