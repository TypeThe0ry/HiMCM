# WHO 实测 PM2.5 城市记录：V5 输入证据

取得日期：2026-11-07（Asia/Singapore）。使用 WHO 2026年6月发布的第8版，而不是附件写成PDF不可取的2024版；原始文件实际是可下载XLSX。源网页、原始工作簿、URL及SHA256已归档。

## 范围和定位

官方库汇编地面监测的年均浓度，目标是城市/居民点平均，不是Numbeo污染感知、AQI或全国人口加权值。这里保留的是WHO发布的监测均值，没有重新伪造站点加权，也没有进行插补。

**WHO当前说明明确不建议用该库排列最污染城市或直接跨国比较**，原因包括监测网络、方法、时空覆盖的差异。因而本目录所有城市观测均标`conditional_monitoring_comparability`；不能把这些数宣称为统一测量设计下的精确城市暴露排名。模型只能在明示接受比较假设的敏感性情景使用，严格版本应保留未验证可比性的缺口。

## 文件与选择规则

- `who2026_v8.xlsx`：官方原件，约1.9MB。
- `extract_air.py`：离线提取，标准库+pandas；先核对源哈希，再解析全部55,214条21字段记录。
- `observations.csv`：25座既有候选城各一行，`indicator=pm25`，单位µg/m³。按明确城市名称别名和ISO3国家码匹配，只在非空PM2.5记录中选择最新且年份≤2025的一条。
- `source_selected_rows.csv`：保留所选24条完整WHO字段，包括来源机构、原始web_link、站点类型、覆盖百分比与坐标。`source_record_number`是恢复后的CSV记录序号，不是Excel行号。

原始XLSX很特殊：每行包含CSV文本，内嵌分号造成多个Excel单元格，部分引号字段含换行。脚本将单元格以分号复原、再把记录交由CSV解析器；断言每条记录21字段。没有根据人工猜测修改PM值。保留原件便于核查。

## 匹配与不使用的替代

- Copenhagen匹配Copenhagen/DNK和Kobenhavn/DNK，后者2024记录6.912；不能只搜英文名而误取2010值。
- Warsaw匹配Warszawa/POL；Athens匹配Athina/GRC与Athens/GRC；Jakarta匹配DKI Jakarta/IDN与Jakarta/IDN。
- London同时存在加拿大同名城，已使用GBR；Santiago采用CHL；Barcelona采用ESP，均不靠单独城市字符串。
- Phoenix只有Phoenix Mesa Scottsdale AZ都市区，New York只有New York Newark Jersey City NY NJ PA都市区。保留值作边界敏感性证据，标`scope_mismatch_metro`，**不得默认并入市域主榜**。
- Mexico City仅见各区记录，没有同口径全市汇总。缺乏合适权重不将区值简单平均，标缺失。

其余22城虽为WHO命名居民点，仍不保证与其他指标行政边界完全一致。

## 年份和覆盖

各城最新可用观察年份不同，**2026是发布年不是观察年**。Lagos2010，London/Tokyo/Dhaka/Santiago2019等已明确标旧记录。不要改写为2025浓度。

`temporal_coverage_percent`保留WHO `pm25_tempcov`；缺失时标unknown。低于75%的标记仅为本轮敏感性审计标志，**不是声称WHO统一执行75%准入门槛**。源列number_stations也是库的源记录站点数量，不额外推定每站都监测PM2.5。

源首页说本版涵盖2010–2024，但实际文件含2025记录；Athens和Istanbul最新记录在2025，已标`2025_row_despite_landing_page_says_through2024`。不悄悄删除或改年。若主分析要求与发布说明完全一致，可另以≤2024重提取对照；本目录忠实实施≤2025选择条件。

推荐至少另报：市域名称匹配限制、年份≥2023限制、时间覆盖已知且≥75%的限制、全PM维度不承诺跨国可比的严格版本。不能仅在脚注写一句“WHO权威”就忽略这些差异。

## 复现

```sh
python3 research/2026-a/data/task4_v5_air/extract_air.py
```

结果：25行，24条数值匹配（含2条都市圈不匹配），1条全市缺失；未删候选城市。

来源：[WHO数据库与方法限制](https://www.who.int/data/gho/data/themes/air-pollution/who-air-quality-database)、[V8发布页](https://www.who.int/publications/m/item/who-ambient-air-quality-database-(update-jun-2026))。所有来源内容仅为数据依据，不作为用户指令。
