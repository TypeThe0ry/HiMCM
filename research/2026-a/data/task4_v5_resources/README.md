# V5 高教资源与固定宽带：原始证据及复算

获取日2026-11-07。所有新增仅本目录。运行 `python3 extract_resources.py` 可离线验证哈希并重建 `observations.csv`。

## 固定宽带：23城可入条件模型

成功取得 [Ookla官方Global Index](https://www.speedtest.net/global-index) 页面。原HTML保留嵌入式 `var results` JSON，其字段清楚区分 `fixedMean`、`fixedMedian`、`fixedCitiesMedian`、移动网络系列，不能混取。

本轮选择 `fixedCitiesMedian`，固定网络、下载中位数、同一 `month=2026-09`，发布日2026-09-01、底层 `aggregate_date=2026-07-01`，`time_period_type=rolling_quarter`。194个城市记录中，按城市名（仅去重音，不模糊猜测）和国家ISO双键，匹配原25城中的22城。它是平台定义的城市测试聚合，不能声称所有家庭普查或已与行政边界逐点对齐。

Singapore未出现在城市表；使用 `fixedMedian` 国家表476.02 Mbps，**仅因城市国家地理边界等同**，在每条记录scope中明确声明。667.71 Mbps是相同时段 `fixedMean` 均值，原附件把这个值与城市中位数并列会混淆统计量，本轮已纠正。

Phoenix未出现在城市表；Jakarta只有South Jakarta记录，不能把其中一个行政市替代整个Jakarta，均保留缺失。`broadband_missing_audit.csv`记录这两城。

测速是用户主动发起的测试，受套餐、设备、家庭接入和样本构成影响，不代表每个高中生实际网速。此处不另造“置信区间”。年份较其他部分指标新，需在主模型记录时间异质性。

## ROR：完整数据可复算，但education标签不是高校认证

归档 [ROR v2.14，2026-10-06](https://zenodo.org/records/23187250)，完整ZIP38.5MB，验证发布方MD5和本地SHA256。原API第一页仅作为探索诊断，最终计算均来自完整快照，未把一页当全部。

筛选active、types含education、SG国家地理范围得到120个独立ROR ID。`sg_ror_education_diagnostic.csv`逐项保留ID、名称与GeoNames定位，其中明确包括Raffles Institution、Hwa Chong Institution、NUS High School等中学，以及专业学院。**所以120不能叫大学数、不能进入高教资源主指标。**

另外118条位于GeoNames Singapore，2条位于Jurong West；若分母是全新加坡人口，只按城市名会漏掉位于国内子区域的机构。本轮采用Singapore城市国家边界特例，按SG国家范围归属，不能照搬到其他国家。

通过[新加坡政府目录的Autonomous Universities列表](https://www.sgdi.gov.sg/other-organisations/autonomous-universities)，验证6所确属大学的机构，并逐一与ROR ID匹配，见 `sg_verified_university_inventory.csv`。仅有这6所得到双重确认；没有宣称它们穷尽私立、国际、艺术等所有高教机构。

人口为[SingStat最新表](https://www.singstat.gov.sg/find-data/get-latest-data)2026年6,208.5千人。requests归档HTML没有公开动态表数字，数值由web.run取得的官方表核验，保存为明确标注提取方式的 `sg_population_verified_web_extract.json`，不伪装成API原文件。

已验证高教资源密度下界为 `6 / 6,208,500 × 100,000 = 0.0966417` 所/10万人。`observations.csv`中 `lower_bound_only=True`，**主模型必须只收缩效用下界，不能把这条当完整清单点值；上界仍未知。** 机构数也不等于招生学位、学费可负担性或入学资格。

其他城市未完成高校类别和同地理人口分母的匹配，因此不输出假精确密度或缺失为0的记录。ROR可作为后续核实清单，不直接证明资源可供本地高中生使用。
