# V91：Phoenix市界内2024年PM2.5监测网络原件

取得EPA官方2024年度监测汇总ZIP，共68956行。Phoenix法定市域内，参数88101（PM2.5 FRM/FEM）、2024年度标准、包含异常事件的完整且认证记录共有**6个站点、8个监测器记录**。年度浓度范围为 **7.041457—11.575910 µg/m³**。

这是市内监测记录的加权可能范围，补充了此前只有Phoenix–Mesa–Scottsdale都市圈记录的地域缺口；不代表全市每个街区、高中生个人或人口加权暴露都在此范围内。

## 原件与筛选

- [官方ZIP](https://aqs.epa.gov/aqsweb/airdata/annual_conc_by_monitor_2024.zip)：3979542字节，完整原件及SHA保留在本目录。[源清单](manifest.json)。
- [EPA字段说明](https://aqs.epa.gov/aqsweb/airdata/FileFormats.html)：City Name明确指法定建制市域，不是CBSA；POC区分同站多个监测器；年度标准和事件类型可能重复同一底层记录。完整率Y指满足该监测指标的监管汇总完整性标准，不等于每一天都有观测。
- [T640数据修订通知](https://aqs.epa.gov/aqsweb/airdata/Data_Advisory_PM25_88101_Pregen_Files.pdf)：排除原始236/238方法，应优先使用校正数据。[说明原件及哈希](documentation_manifest.json)。

选择规则：State Code=04，Parameter Code=88101，Pollutant Standard=`PM25 Annual 2024`，Event Type=`Events Included`或`No Events`，City Name=`Phoenix`。全部选中记录实际满足Completeness Indicator=`Y`、Certification Indicator=`Certified`，Observation Percent为93—100%。没有把观测百分比写成全年天数比例。West Phoenix的24小时重力法POC2全年只有30次观测，但按其计划频次报告100%；这条稀疏记录也位于其他连续监测器确定的凸包内部，剔除它不改变端点。

`Arithmetic Mean`对应指标为 **Quarterly Means of Daily Means**，而不是直接把逐小时数据等权平均。只选一个年度标准，不重复计入1997/2006/2012标准；保持异常事件数据，未用“Events Excluded”低值替代居民可能经历的空气情况。

| 站点编号 | 名称 | 监测器数 | 年均浓度范围 µg/m³ |
| --- | --- | ---: | ---: |
| 04-013-0019 | West Phoenix | 2 | 9.236667—10.091160 |
| 04-013-1004 | North Phoenix | 1 | 7.240000 |
| 04-013-4003 | South Phoenix | 1 | 11.575910 |
| 04-013-4021 | Eastwood | 1 | 7.041457 |
| 04-013-9812 | Durango Complex | 1 | 10.188630 |
| 04-013-9997 | JLG Supersite | 2 | 9.120822—9.631897 |

JLG两条记录标为`Multiple Methods Used`，单靠年度文件不能识别每种方法，故保留方法不确定标记。其他5个站点的已识别方法为TEOM1405-DF或重力法；年度24小时块平均中的空方法字段由同POC的原始小时汇总方法说明交叉核对。未把空方法当作未知数据直接忽略。**去掉JLG两条方法不明确的记录后，最大和最小值完全相同**，两端均由方法明确的TEOM站点确定。

EPA City Name作为地域主依据。另复用已核验Phoenix边界进行坐标交叉检查，所有Arizona年度候选的市界判定与City Name一致。源坐标同时有NAD83与WGS84，此交叉检查没有做大地基准转换，因此明确只作辅助检查；当前边界不被宣称为2024历史边界。复用文件哈希见[边界清单](reused_boundary.json)。

## 保留未知权重的区间

对本组已观测、完整的监测年度值$x_m$，若目标被定义为其未知非负权重加权量，

$$\theta=\sum_m\lambda_m x_m,\quad\lambda_m\ge0,\quad\sum_m\lambda_m=1,$$

则

$$\theta\in[\min_mx_m,\max_mx_m]=[7.041457,11.575910].$$

无需猜人口权重，不把同站POC、多个标准或事件版本重复加权。按既有成本效用$u=15/(15+x)$得到

$$u\in[0.5644209361034109,0.6805357740189316].$$

该凸包只覆盖上述已观测网络值的加权量。未监测地点、空间代表性、测量偏差、采样外时段和不同年度不由此界覆盖；它不是置信区间，也不是高中生暴露的普遍物理界。是否用于条件主模型由根代理的显式修订决定；本数据包`main_admitted=false`，本身不修改主模型。

## 复现与输出

```sh
python3 research/2026-a/data/task4_v91_phoenix_air/extract.py
```

计算前核验原件哈希及ZIP CRC；核对全年份、站点唯一性、年度汇总规则、完整性/认证、边界一致及方法不明确记录剔除后的端点稳定性。

[选中记录](phoenix_selected_monitors.csv) · [站点范围](phoenix_site_intervals.csv) · [Phoenix所有标准原始行](phoenix_all_standard_rows.csv) · [Arizona年度候选](arizona_annual_candidates.csv) · [结果](summary.json)。未修改其他目录、论文或提交Git。
