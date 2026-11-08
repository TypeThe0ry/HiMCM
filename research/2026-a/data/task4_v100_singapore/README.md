# Singapore：推荐关键来源复核与真实谋杀受害人数更新

当前模型使用的凶杀率仍可追溯至WDI/UNODC的2023年值0.0690954942050905／10万人。新刷新官方API后，2024、2025仍为空，最新非空年仍是2023。取得的指标元数据将intentional homicide定义为意图导致死亡或严重伤害的非法致死；没有用犯罪案件总数代替受害者人数。

本轮另取得SingStat转发SPF的完整135行《Victims Of Selected Major Offences By Sex And Broad Age Group》原始API，以及SingStat完整29行人口指标API。得到以下可复算的本地谋杀描述量：

| 年份 | 谋杀受害人数 | 同年总人口 | 每10万人记录受害人数 | 按2/(2+r)转换的情景效用 |
| --- | ---: | ---: | ---: | ---: |
| 2023 | 4 | 5917648 | 0.067594423 | 0.967307697 |
| 2024 | 10 | 6036860 | 0.165649029 | 0.923510676 |
| 2025 | 8 | 6111175 | 0.130907722 | 0.938567156 |

人口采用全城市国家的Total Population原始整数，包含居民与非居民；不使用四舍五入的611万，也不将居民人口与全体受害人数混配。该分母是官方年度人口存量，不是警方受害者总体的逐人暴露时间。API年龄分组包括21岁及以下和其内嵌的7—19岁，不能重复加总，也不能当作14—18岁当前高中学生统计。

本地分类为Murder，WDI为Intentional homicide；本轮未取得可核验的ICCS对应关系。因此三年本地序列可作同定义年份情景，WDI与本地2023之间则是来源／定义敏感性，不能声称仅年份差异。没有将本地值替换主模型，也没有靠猜测法律分类构造单侧凶杀率界。人数变化是年度记录变化，不据此推断政策效果或个人未来风险。

## 宽带来源保持

重新从V5归档的Ookla原始HTML嵌入JSON提取：Singapore的`fixedMedian`国家表、固定下载中位数为476.02 Mbps，2026-09发布分组，`aggregate_date=2026-07-01`，`time_period_type=rolling_quarter`。同组`fixedMean`为667.71 Mbps，未混入；城市表没有Singapore，使用国家表仅基于城市国家地理同一性。

它是平台测速聚合指标，不是家庭覆盖率、学校网络可达性或高中生实际网速。此次原始字段复核没有给出校正学生覆盖偏差所需的数据，也没有为其创造置信区间。对应效用仍为476.02/(100+476.02)=0.8263949168431651。

## 复现与来源

运行 `python3 research/2026-a/data/task4_v100_singapore/extract.py`。`extract()`不写文件，可供情景脚本调用；命令行运行重建[summary.json](summary.json)。脚本核验[manifest.json](manifest.json)所有新旧原件哈希、API分页完整性、2024/25 WDI空值、男女及年龄非重叠加总、居民／非居民人口分解，以及宽带统计字段。

- [SPF／SingStat受害者表](https://data.gov.sg/datasets/d_43bc9a5106f4264642dc38e7cc39fcd3/view)：M890911，2011—2025；网页注明2026-09-01更新。
- [SingStat人口表](https://data.gov.sg/datasets/d_3d227e5d9fdec73f3bcadce671c333a6/view)：M810001；原始整数人数。
- [WDI指标定义](https://api.worldbank.org/v2/indicator/VC.IHR.PSRC.P5?format=json)与[Singapore序列](https://api.worldbank.org/v2/country/SGP/indicator/VC.IHR.PSRC.P5?format=json&per_page=100)。
- [既有Ookla原始资料及范围审计](../task4_v5_resources/README.md)。

查阅日2026-11-08。另尝试旧SingStat Population Trends2025的pdf/ashx端点均404，NPTD2025报告与正文端点403，TableBuilder元数据端点403；没有保存错误响应冒充原件，也未据此声称取得更细人口参考日或法律分类映射。主模型新增准入为0，未修改论文。
