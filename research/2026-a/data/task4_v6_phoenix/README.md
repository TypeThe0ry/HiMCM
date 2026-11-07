# Phoenix 高中教育与真实通学：V6 数据审计

获取日期：2026-11-07。仅使用原始官方来源作数值提取。本目录不将Phoenix Union学区当成Phoenix市，不以成人通勤替代学生通学，不把教师FTE冒充教师人数。

## 可复算的教育新证据

从NCES EDGE官方 `School_Characteristics_Current/FeatureServer/1` 查询Arizona且最高年级12的全体记录，获得939条2024–25学校记录（服务未截断；NCES学校ID唯一）。从City of Phoenix官方ArcGIS服务取得当前市界，按学校经纬度做点在多边形筛选，158条位于市界内，其中99条学校年级范围为9–12。**不是用邮寄地址城市名筛选，也不限于Phoenix Union学区。**

明确可比子群定义：位于当前市界、开放/运行、非虚拟、仅9–12年级、四个年级人数非负且与学生总数一致、对应教师FTE为正、学生总数非负的公校。其余记录全部保留在逐校审计中。

| 统计 | 实测值 |
|---|---:|
| 完整记录子群学校数 | 64 |
| 独立教育机构/学区LEA数 | 37 |
| 9–12年级学生合计 | 50,621 |
| 教师FTE合计 | 2,480.97 |
| 子群学生/FTE | 20.40371306384 |
| 若使用15锚点的子群效用 | 0.42368437381 |

`observations.csv`仅含此**诊断子群**观测，状态为`diagnostic_complete_record_subset_not_admitted_citywide`。该行不得被“不是missing就入模”的规则自动准入。

可以另做“将Phoenix评价目标限定为以上完整公校子群、并接受FTE与其他城市headcount的可比性假设”的单独情景；不能称作完成全市高中教育数据，也不是教育质量或学生学习成果指标。

主模型Phoenix全市高中教师headcount目标仍为未知效用[0,1]。原因：

1. 私校不在CCD，混合学段学校不能把全校教师全部归给高中；学生在学校的位置也不等于居住地。
2. 部分纯高中记录存在负数缺失代码。Accelerated Learning Center的133名学生有记录，但FTE=-1，NCES学校详情也显示缺失。没有用往年人数、第三方估算或全区教师补值。
3. 多个职业教育附属记录为0或1名学生且FTE缺失，不能把负数当作真实教师数求和，也不能假定附属教学资源完全独立。
4. Hope College and Career Readiness Academy学生总数为负数特殊码，完整记录子群排除；不依据第三方网页的不同年份数值补齐。
5. 市界是本次下载的当前边界，学校数据是2024–25；没有证明这段时间边界不变。保留这一地理时间条件。

部分学校的**比率不是全市比率下界或上界**：未观测学生和教师既可使合计比率上升，也可使其下降。故不能像大学个数名录那样把子群比率转成城市单侧界。

## 真实高中生通学线索与未准入原因

Maricopa County官方Travel Reduction Program（TRP）确实存在真实学生问卷，而不是成人代理。网页工具可读取官方学生问卷，其题目区分High School/Prep School，并询问通常居家到学校单程分钟；直接HTTP下载返回404，因此本目录仅归档字段核对JSON，不冒称保存了问卷PDF原件。条例的调查对象是每周到单一学校至少三日的driving-age学生，可能还包含社区学院和大学。

但本轮未取得Phoenix市内学校、限定高中学段的有效回复分布/权重/非回复规模。公开项目页说明逐学校调查摘要由TRP制作，handbook说明摘要通过邮件给参与机构；这不是公开完整城市微观数据的证据。没有联系学校、发送邮件或提交信息申请。

因此TRP问卷证明**存在可获取的正确测量设计**，不证明我们已经获得其测量结果；本轮Phoenix真实高中生通学仍[0,1]。

MAG官方目录的网页检索结果列出2017区域家庭出行调查报告及旧2008区域数据（直接HTTP下载403，未归档成功）。区域调查、全龄出行和Phoenix行政市高中生不是同一对象，本轮没有拿区域均值/样本设计直接压缩城市通学区间。历史Maricopa学生均值（2004–05）即使可检索，也混合学段、地域与年代，不准入。

## 来源与复现

- NCES学校来源：<https://services1.arcgis.com/Ua5sjt3LWTPigjyD/arcgis/rest/services/School_Characteristics_Current/FeatureServer/1>
- NCES字段与方法描述：`nces_layer.json`，明确2024–25、教师FTE和各年级人数。
- 市界官方来源：<https://services.arcgis.com/cfKakmeHE95cgeEK/arcgis/rest/services/CityLimit/FeatureServer/1>
- TRP项目：<https://www.maricopa.gov/2388/Travel-Reduction-Program>
- TRP学生问卷：<https://www.maricopa.gov/DocumentCenter/View/40221/Sample-Student-Survey?bidId=>
- TRP手册：<https://www.hsd.maricopa.gov/DocumentCenter/View/72751/MCAQD-TRP-Handbook>
- NCES缺失教师核对：<https://nces.ed.gov/ccd/schoolsearch/school_detail.asp?ID=040012101581>

`manifest.json`记录成功原始下载SHA256以及失败请求。抓取失败不记为成功原始归档，网页检索可读不代表HTTP下载成功。`school_audit.csv`给出全部939条记录与逐条件布尔列；`summary.json`与`observations.csv`由脚本生成。

```sh
python3 research/2026-a/data/task4_v6_phoenix/extract_phoenix.py
```

只依赖既有numpy/pandas/matplotlib。脚本校验所有成功归档hash、查询未截断、ID唯一、年份、有限坐标、分年级总和及非负有效分母。ArcGIS固定宽度字符串尾空格仅在派生表strip，原始JSON字节不变。

## 覆盖诊断供下一轮使用

`coverage_diagnostic.json`：本次GSHI=12查询市内158条记录中，9–12年级非负已知人数合计74,365；7个年级人数格为负数特殊码，涉及4所学校；15所全虚拟、143所非虚拟；30所FTE缺失或非正，其中24所为纯9–12。计数含混合学段学校，但不是居住在Phoenix的去重学生总数，也不包括最高年级13或其他代码学校，不能直接算成完整覆盖率。
