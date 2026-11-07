# 各国家和地区凶杀率与中学生师比：国家—年份匹配表

下载日期：2026-11-07。两个指标均来自世界银行 World Development Indicators（WDI）的官方批量CSV下载，归档标注的数据库更新日期均为 **2026-10-08**。原始统计来源分别为 UNODC 和 UNESCO Institute for Statistics（UIS）。本目录是国家级研究数据，不直接改写论文或城市指标矩阵。

## 直接使用

优先打开 **[country_year_homicide_education.xlsx](country_year_homicide_education.xlsx)**，含中文表头、筛选、冻结窗格及以下工作表：

| 工作表 | 内容 |
|---|---|
| 国家年份总表 | 217个国家和地区 × 1960—2025年，14,322行；包含两个指标都缺失的行 |
| 同年双指标完整 | 同一国家、同一年两个指标都有值的1,846行，涉及161个国家和地区；年份1990—2019 |
| 国家覆盖 | 各国家和地区的有效年份数、最早/最晚年份及同年双指标覆盖 |
| 年度覆盖 | 各年两个指标分别有效及同时有效的国家和地区数 |
| 字段与口径 | 字段释义、单位、缺失值处理和地域范围 |
| 数据来源 | 下载链接、获取时间、原始文件SHA-256 |

程序读取可直接用以下UTF-8（带BOM）CSV：

- [country_year.csv](country_year.csv)：完整国家—年份网格，与Excel总表一致。
- [country_year_both_observed.csv](country_year_both_observed.csv)：两个指标同年完整的配对表，适合直接筛选建模样本。
- [country_coverage.csv](country_coverage.csv)、[year_coverage.csv](year_coverage.csv)：覆盖情况。
- [data_dictionary.csv](data_dictionary.csv)：中文字段说明。

完整总表有 **6,563行至少一个指标有值**，另有7,759行两个指标都缺失。1960—2025是批量文件的年份列范围，**不表示每年都有观测**。如只需至少一个指标有值的记录，筛选 `data_status != 'neither'`。

## 指标与有效覆盖

| 字段 | 世界银行代码 | 单位 | 有效观测年份 | 有数据的国家和地区数 | 非空观测数 |
|---|---|---|---|---:|---:|
| `homicide_rate_per_100k` | `VC.IHR.PSRC.P5` | 每10万人中的故意杀人受害者数 | 1990—2023 | 196 | 4,065 |
| `secondary_pupil_teacher_ratio` | `SE.SEC.ENRL.TC.ZS` | 中等教育学生数/教师数，学生/教师 | 1970—2019 | 204 | 4,344 |

来源与定义：

- [世界银行凶杀率指标页](https://data.worldbank.org/indicator/VC.IHR.PSRC.P5)；[指标元数据](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/VC.IHR.PSRC.P5)。故意杀人指意图致人死亡或严重伤害而造成的非法死亡；原始统计来源 UNODC。
- [世界银行中学生师比指标页](https://data.worldbank.org/indicator/SE.SEC.ENRL.TC.ZS)；[指标元数据](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SE.SEC.ENRL.TC.ZS)。中等教育整体包含初中和高中，对应每名教师的学生数；不是平均班额，也不是仅高中指标。教育数据跨年学年按结束年份标记。
- 两个指标页面标明数据许可 **CC BY 4.0**。引用时保留指标名称、代码、WDI及原始统计来源、下载日期。

**生师比到2019年为本次WDI下载的实际覆盖上限，不代表UIS原始数据库也只到2019年。** 本次保持所请求两个WDI指标及其口径一致，未拼接其他教育指标或数据库。如需较新教育数据，可另查 [UIS Data Browser](https://databrowser.uis.unesco.org/)，核实教育阶段和教师统计口径后单独建立数据版本。

## 匹配规则和缺失值

1. 唯一键是 `wb_country_code + year`。使用世界银行三位国家代码，不靠名称模糊匹配；它通常对应ISO3，但不保证每个代码都属于ISO标准。
2. 国家和地区由归档的国家API判断，排除 `region.value == 'Aggregates'` 的世界、区域、收入组等49个汇总项；保留217个国家和单列地区/经济体。因此“217”不表示217个主权国家。
3. 总表保留来源年份列的完整网格；缺失项是空白，既不是0，也不是经过估计的值。不插值、不前向填充、不跨年配对；原始值0仍作为有效观测保留。
4. `data_status`：`both`=同年两项都有；`homicide_only`=仅凶杀率；`secondary_ratio_only`=仅生师比；`neither`=均缺失。
5. CSV保留原始数值字符串精度。Excel存储为数值，默认显示六位小数；可调整显示位数。匹配表逐条通过原始来源核对，Excel数字在浮点表示容差内通过回读核对。
6. 国家覆盖表中的地区和收入组为下载时分类，不是观测年份的历史分类。国家层面的指标不能直接赋给具体城市；城市国家须结合实际边界判断。
7. 同年完整样本不是均衡面板，各国年份覆盖不同；筛选后应再次核对样本范围。全局最早/最晚年份不保证期间连续。

## 原始档案与复现

`raw/`保留原始响应字节：两个ZIP内含官方数据CSV、国家元数据和指标元数据，另有国家API的完整JSON。[download_manifest.json](download_manifest.json)记录各原始文件的URL、实际响应URL、UTC获取时间、字节数和SHA-256；[summary.json](summary.json)保存覆盖统计和验证结果。

构建脚本：[build_country_year_homicide_education.py](../../scripts/build_country_year_homicide_education.py)。从仓库根目录执行：

```bash
python3 -m pip install -r research/2026-a/data/country_year_homicide_education/requirements.txt
python3 research/2026-a/scripts/build_country_year_homicide_education.py
```

默认离线读取当前快照，先校验所有原始文件SHA-256，再重建CSV、Excel和统计摘要。只需CSV时可加 `--csv-only`，无需第三方Python依赖。

下载更新快照时指定新目录，避免覆盖本次原始档案：

```bash
python3 research/2026-a/scripts/build_country_year_homicide_education.py \
  --download --output-dir /absolute/path/to/new_snapshot
```

下载需要本机Python的HTTPS证书配置有效。此次通过桌面应用附带的Python运行。脚本拒绝覆盖已有原始快照。

验证包括：原始文件字节数与SHA-256、国家API完整分页、指标代码、原始国家代码集、非负有限数值、国家—年份唯一性、全部非空数值字符串与ZIP一致、CSV回读、Excel全部数据单元格回读、配对行数与年度覆盖汇总一致。

本次还单独调用WDI JSON API，核对中国、新加坡、美国2018—2023年两个指标共36个值/缺失项，均与整理表一致；在临时目录离线重建全部CSV，逐字节与交付文件一致。
