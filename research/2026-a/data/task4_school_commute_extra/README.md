# 墨尔本高中年龄段真实通学：VISTA 2024–25

访问日：2026-11-07（Asia/Singapore）。来源为维多利亚州交通与规划部门（DTP）公开发布、去标识化的 VISTA 数据，CC BY 4.0。原始文件及逐文件URL/SHA256见 manifest.json。

## 入模口径

- 地理：`homeregion_ASGS == Greater Melbourne`，即大墨尔本 GCCSA，不是狭小的 City of Melbourne 地方政府区。
- 学段：Persons 中 `studying == Secondary`；年龄只能识别五岁组，本次使用 `agegroup == 15->19`，**不能称精确14—18岁，也不能识别仅11—12年级**。
- 日期：2024年7月—2025年6月，`dayType == Weekday`。
- 按 `persid` 将 Journey to Education 与 Persons 做多对一连接；检查唯一性、连接未丢行、时间和权重有效。
- 使用 `journey_elapsed_time`，包括途中等待；这是调查记录的从家出发到就读地点的单程旅程，**不是最近学校的路网时间**。
- 用官方 `journey_weight × 7/5` 计算工作日总量，比例和均值中的7/5相消。未采用全年龄权重平均。

[数据集](https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista) · [Journey字段字典](https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista/resource/5cab66ec-8752-4982-97e5-e417c932e576) · [Persons字段字典](https://opendata.transport.vic.gov.au/dataset/victorian-integrated-survey-of-travel-and-activity-vista/resource/2a38732d-04dc-4af5-8a52-f281a8ecebb7)。

## 实际计算

15—19岁中学生样本为108条旅程、107人、93户。扩展加权的单程时间均值21.0284分钟，45分钟以内占93.0252%。在假设效用 `u=exp(-t/30)` 下，均值0.553543；效用最低20%旅程权重的均值0.230336；`0.7平均+0.3低尾` 为0.456581。20%是旅程权重分位，不是精确人口分位。

仅保留每人第一次旅程有107条，平均20.8184分钟、效用0.555554。此敏感性用于检查同人多次旅程的影响，不偷偷改变官方旅程口径。全部年龄中学生208条，平均23.0666分钟；不将这个更宽样本混入主15—19岁结果。

完整逐分钟加权分布见 `melbourne_elapsed_histogram.csv`；摘要见 `melbourne_summary.csv`。

## 采样与可迁移性

这是抽样调查结果，不是全市所有高中生的普查。没有上学旅程的学生不在通学旅程条件样本内。年龄、年级、居住边界与其他城市仍可能不同。

说明文档提供家庭/个人/行程等部分文件的jackknife重复权重，但 **Journey文件只提供单一旅程权重**。本轮不冒称采用官方设计方差。`melbourne_exploratory_bootstrap.csv` 是以家庭为抽样单元、保留固定旅程权重、2000次重采样（种子20261107）的探索性敏感性范围。均值效用2.5%—97.5%分位约为[0.503907,0.601583]；它**不是经过完整调查设计校正的95%置信区间**，也未覆盖测量、年龄、年份或跨城市迁移误差。不能把108个样本视为总体确定值。

复现：在任意目录执行 `python3 /absolute/path/to/derive_melbourne.py`，需要pandas和numpy，离线读取已归档源文件。所有输出由脚本计算；未填入模拟观测。

## 其他城市搜寻审计

- Dubai：找到GEMS Metropole单校材料称校车用户25%、平均45分钟，但没有全市和高中学段可代表性，排除。RTA跨学段满意度与出行方式比例不等于高中生时间分布，也排除。
- Toronto：StudentMoveTO是大学等高等教育人群，排除。TTS确有数据下载入口，但本轮未取得经学校学段和市域核对的时长结果，不转写成高中通学数值。
- Tokyo：搜索命中的JASSO大学通学时间以及全国高中生活调查不能当东京高中市域估计，排除。

这些排除记录避免“为了覆盖25城而借用错误人群”。除墨尔本外，本目录不声称新取得其他城市可入模的高中通学数据。
