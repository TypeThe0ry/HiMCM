# V7 Istanbul：部分辖区风险界与官方高校总量

访问日期2026-11-07。产出两条`bounds.csv`，均明确为条件证据。没有新增真实高中生通学值，通学继续[0,1]。

## 1. 全年警方谋杀死亡子集 → 全省风险下界

Anadolu Agency（AA）2026年1月5日原始报道，注明2025全年Istanbul警方责任辖区发生291宗谋杀案件，307人死亡。当地警方与宪兵辖区不能默认相同，因此不把它当全省完整统计。分子是**307死亡而非291案件**。

- 原始报道：https://www.aa.com.tr/tr/gundem/istanbul-polisi-gecen-yil-faili-mechul-cinayet-birakmadi/3789805
- 原始HTML完整保存`homicide_aa2025.html`；脚本直接提取辖区、案件数和死亡数，核对发布日期。
- 原文是记者基于警方信息报道，并非公开逐案微数据；属于primary news reporting，不冒称直接警方数据库。报道用`cinayet`（谋杀）并列明枪杀、刀杀、殴打等致死方式；未采用所有死亡、未遂案件或自杀数。未逐案复核国际ICCS分类，因此严格定义情景可撤回。
- 全省2025年末常住人口15,754,053来自TÜİK ADNKS官方发布。人口来源：https://data.tuik.gov.tr/Bulten/Index?p=Adrese-Dayali-Nufus-Kayit-Sistemi-Sonuclari-2025-53899 。官方《Statistics on Children2025》表1.8亦一致。原始入口当前返回JavaScript壳，数字由官方索引及PDFweb读取交叉核对，结构化记录明确标为人工转录，未宣称本地HTML中包含该数字。

令D_city为全省同类谋杀死亡数，P为同年同省年末常住人口。在警方地域包含于省域且报告无重复/误分类的条件下，D_city≥307，因此

```
H_city = 100000 D_city/P ≥ 100000×307/15754053 = 1.9487048825
u_H = 2/(2+H_city) ∈ [0,0.5064951825]
```

下界仍0（闭包）；未给省域漏报死亡总量设上限。此处**不是用子辖区死亡/全省人口冒充子辖区率**，而是计算全省固定分母下的可证明率下界。该操作只在目标是省域事件数/常住人口率的定义下成立，不是个人遇害概率、年均暴露人年率或高中生专属受害率。原模型的全年龄公共安全指标保持不变。

`status=conditional_partial_jurisdiction_risk_bound`。锚点变化时必须从raw_lower重算效用上界；不应固定0.5065用于全部权重/尺度情景。

## 2. 2022完整行政高教机构总量，保留原指标范围

V5规范⑥是“经核验高等教育机构密度”，并不限于大学。因此主指标必须保留**13所state universities＋43所foundation universities＋4所独立foundation vocational higher schools＝60所独立高等教育机构**，不能为了数值较低而只取56所大学。

官方Istanbul Development Agency（İSTKA）《2024–2028 Istanbul Regional Plan》5.3.4/Table5.5引用YÖK2022整省三类行政总量。官方报告地址：https://www.istka.org.tr/media/pdf/jUnXem7E05fo5rmajTVWXZ5z6X6TXelaYMoVRPn0sIkZTwcCaJTR.pdf 。同报告Figure5.2列2022年Istanbul省人口15,907,951。

独立职业高教资格另由土耳其高等教育质量委员会YÖKAK官方2024自评报告印刷页8核对：三类高教机构包括state universities、foundation universities及foundation vocational schools；独立基金会职业学校不附属于大学/技术学院。它们是高等教育（而非高中），故4所应该纳入；院系及附属职业学院不另外重复计数。资格来源：https://www.yokak.gov.tr/documents/enqa/YOKAK-SAR-RAPORU-2024.pdf 。该定义核验通过官方web PDF读取，记录于`official_web_verified_values.json`。

同年同省：

```
HE = 60/15907951×100000 = 0.3771698819 independentHEIs/100000 residents
u_HE = HE/(1+HE) = 0.2738731705
```

仅大学的56所、密度0.3520252231另存`university_only_diagnostic.csv`，不进入主模型。主状态为`conditional_official_complete_he_aggregate`。这是发布方完整行政汇总，不是ROR搜索前N条；本轮无逐机构ID审计，不能称逐校核验。保留2022年份，不冒充2026最新总量；严格时效或逐机构准入情景可重开[0,1]。

本地下载官方区域计划PDF收到HTTP200但实际是HTML防护页，已重命名`region_plan2024_download_response.html`并标记`html_challenge_not_pdf`；不冒称PDF下载成功。数据通过官方PDF的web全文表格核验，人工转录记录注明来源、表号、范围和抽取机制。派生JSON的哈希只能保证保存后的完整性，不代替原始PDF字节校验。

## 3. 通学调查准入审计：没有合格高中生全市证据

| 线索 | 查到的内容 | 处理 |
|---|---|---|
| IBB Transportation and Mobility2007 Table2.3 | High-school一行38.6分钟，但正文明确是按已取得教育程度分组的人的出行 | 拒绝；不是在读高中生家校行程 |
| BAU Transport and Traffic survey | 全龄工作或学校混合单程约50分钟 | 拒绝；工作/学校与学段未分离 |
| Children’s Active School Travel2021 | Istanbul18校，12–14岁grades6–8 | 拒绝；初中不是高中 |
| Gebze Technical thesis，Pendik小学 | 家长报告805名小学儿童分箱 | 拒绝；小学且单区，不能替代高中全市 |
| High-school out-of-school time study2021 | 单所公立高中180名10/11年级学生 | 未取得可代表全市的通学分布及抽样权重；不据此缩全市区间 |
| School bus boarding-time study2023 | 高中乘客平均上车4.2秒 | 拒绝；上车时间不是单程通学时间 |

线索原文地址保存在`travel_rejection_audit.csv`。本轮没有把开学时间、校车计价、成人通勤或受教育程度代理包装成真实高中生通学。

## 4. 离线验证

```
python3 research/2026-a/data/task4_v7_istanbul/extract_istanbul.py
```

依赖现有BeautifulSoup与标准库。验证已保存来源SHA256、AA原始段落与死亡/案件区分、单侧成本界单调性、13+43+4=60独立高教机构计数（56大学另诊断），重新输出`bounds.csv`。原始获取成功、JS壳、HTML挑战、失败和人工转录分别记载，所有原始值及分母均保留。
