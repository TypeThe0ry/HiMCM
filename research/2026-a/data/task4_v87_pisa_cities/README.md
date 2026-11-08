# V87：用当前教育项目识别高中阶段学习成果

直接复用完整下载的[OECD PISA2022学生原件](https://webfs.oecd.org/pisa2022/STU_QQQ_SPSS.zip)，提取5个可识别学校地区共19012条记录。保留 `ISCEDP`、国际年级、年龄、10个合理值及80个Fay-BRR复制权重。原始SAV仍在仓库外；[manifest](manifest.json)记录其SHA及派生子集SHA、学校地区筛选式、原始代码标签。

## 人群定义及实测差异

OECD的 `ISCEDP` 表示当前就读项目的ISCED2011层级及类型。`300 <= ISCEDP < 400` 为高中阶段，包含普通及职业项目；不是父母教育程度，也不是已完成最高学历。定义见[OECD技术报告](https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/03/pisa-2022-technical-report_599753f0/01820d6d-en.pdf)。原始文件标签同步保存在manifest。

| 学校地区 | 全部PISA样本 | ISCED3样本 | 年级≥10样本 | ISCED3数学达Level2比例（SE） |
| --- | ---: | ---: | ---: | ---: |
| Bogotá | 1986 | 1399 | 1399 | 58.05%（2.59个百分点） |
| Dubai抽样地区 | 7374 | 6030 | 5934 | 69.91%（0.79个百分点） |
| Greater London | 777 | 777 | 777 | 78.30%（2.64个百分点） |
| DKI Jakarta | 2269 | 1145 | 1145 | 46.45%（4.14个百分点） |
| Singapore | 6606 | 6534 | 6194 | 92.06%（0.41个百分点） |

统一“十年级以上”的筛选会漏掉Singapore340人和Dubai96人。原件明确把这些九年级学生的项目列为ISCED344；Dubai另外1274名九年级学生则属ISCED244。不能仅按年级数字推断跨国学段。Bogotá的ISCED3与V86的10—11年级集合完全一致。

年级筛选下Singapore、Dubai达标比例分别为92.66%、70.98%；纠正学段后为92.06%、69.91%，下降约0.59、1.06个百分点。这是样本定义修正，不是教育水平的时间变化或学校效应。完整[学段交叉表](stage_grade_crosstab.csv)、[各域规模](domains.csv)、[学习成果](outcomes.csv)保留可核对数值。

## 地理与覆盖边界

- Bogotá：`CNT=COL, REGION=17001`，与原有城市抽样域相同。
- Singapore：`CNT=SGP`，城市国家整体，不能把该项目分类等同于本研究旧有预科教师资源口径。
- Dubai：原始STRATUM标签明确的Dubai七类公私校抽样层，按该抽样地区报告；未证明与任意GIS城市建成区或居民边界完全一致。不能拿本结果直接复现只含私校的KHDA宣传均值。
- Greater London：四类明确标注Greater London的英国学校抽样层；不是City of London小行政区，也不是整个英国。
- Jakarta：`CNT=IDN, STRATUM=IDN01`，原始标签为DKI JAKARTA首都地区，不是整个Jabodetabek都市圈。

全部为PISA2022在校年龄队列。实际年龄范围：Bogotá和Singapore15.33—16.33，Dubai15.33—16.42，London15.25—16.25，Jakarta15.42—16.42岁。年龄、地区及学段筛选不能覆盖所有14—18岁居民或未在校青少年；高中子群还受各国入学进度和留级选择影响。复制权重反映调查设计抽样不确定性，不能消除非响应、测量偏差或地区边界差异。

## 估计方法与阈值

数学Level2下界为420.07，来自[NCES官方PISA2022技术说明](https://nces.ed.gov/surveys/pisa/pisa2022/technical-notes/index.asp)及OECD技术报告Annex Table17.A.1。[NCES网页原件](nces_pisa2022_technical_notes.html)及[sources_manifest](sources_manifest.json)保留字节和哈希。对每个合理值先判断是否达到该阈值，再用调查权重估计比例；不能先把某个学生10个合理值平均后分类。

对每个合理值 $m$ 得到估计 $\theta_m$ 与80个复制估计 $\theta_{mr}$，

$$\bar\theta=\frac1{10}\sum_m\theta_m,\quad
V=\frac1{10}\sum_m\frac4{80}\sum_r(\theta_{mr}-\theta_m)^2+
\frac{1.1}{9}\sum_m(\theta_m-\bar\theta)^2.$$

[输出](summary.json)保留均值、SE、方差分解及逐项近似正态95%区间，不宣称联合覆盖。比例原始区间不自动截断。三科学业均值使用同一PV和Fay-BRR方法。[逐PV复制估计](pv_replicate_estimates.csv)允许独立核算。

程序复现Bogotá全年级达标率48.192695594%，与V85公布分级比例合计一致；高中三科均值复现V86。学习成果是新构念，此包 `main_admitted=false`，没有自动替换教师资源、修改主模型权重或把国家分数填给无法识别的城市。

```sh
/tmp/task4_pisa_venv/bin/python research/2026-a/data/task4_v87_pisa_cities/extract.py /tmp/task4_pisa_extract/CY08MSP_STU_QQQ.SAV
python3 research/2026-a/data/task4_v87_pisa_cities/analyse.py
```

提取需要pyreadstat、pandas；分析需要numpy、pandas。提取前校验原件，分析前校验派生数据及前轮来源manifest。代码不写入其他目录。
