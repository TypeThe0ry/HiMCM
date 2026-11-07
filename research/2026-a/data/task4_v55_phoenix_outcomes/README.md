# Phoenix Union：直接发布的四年毕业队列

新增ADE官方学区级毕业接口记录：Phoenix Union High School District（实体4286、NCES LEA0406330）的FY2025发布包含**6285名队列成员、4813名毕业生**，两者相除为76.57915672%，接口公布整数百分数77。官方前端的四年毕业图标题将FY2025对应到**2024届**，不能把它写成2025届毕业。

这条记录直接来自学区All汇总，不是96所市界学校记录相加。学区接口分组键为`studentGroupDescription`，与原学校接口的`subgroups`不同；程序只选择唯一All行，未重复累加重叠人口分组。Female与Male人数分别相加可独立复核All的队列及毕业总量；特殊码原样保存，不反推受保护小组。

## 范围与缺口

原始[PXU2025官方说明书](https://files-backend.assets.thrillshare.com/documents/asset/uploaded_file/4844/Pxu/8a058348-5d2b-4319-8880-28ecea997431/2025_Capital_Override_Fact_Sheet-21M-R4-s_100_.pdf?disposition=inline)的2024–25学区介绍列23所学校，其中1所Digital Academy。这个教育服务范围不是此前排除线上学校的Phoenix市界学校集合，更不是所有实际居民高中生。

因此，本次取得可独立引用的真实学区毕业结果及正确分母，但不能将76.58%直接替换全市毕业率，也不能据此宣布旧学校记录已经全部去重。要改善V14的城市集合界，仍需同届学区／市界学校的包含关系、线上等非目标群体的覆盖及行政人数归属证明。

说明书另列在校生25108及毕业率76.5%，但未给该毕业率的队列分子、分母和明确届别。本次不以总在校生充当毕业届分母，也不强行使说明书百分数与接口精确人数一致。

FY2026毕业请求返回空数组，表示此请求未取得数据，不是零毕业生。实体详情请求2025却返回2026；它验证现有学区标识，不证明所有2024历史属性。毕业响应自身明确返回FY2025。

## 原件、公式与检查

原始请求URL、字节数和SHA256见[manifest.json](manifest.json)，归档包括FY2025、FY2026毕业响应、实体响应及说明书PDF；前端年期规则复用V9官方JavaScript原件。直接发布学区比例使用`q=G/N=4813/6285`，不增加统计抽样区间或人为给出城市覆盖权重。

运行`python3 research/2026-a/data/task4_v55_phoenix_outcomes/audit.py`可离线核验源哈希、实体ID、分组唯一性、人数及性别分项总和、前端届别规则和PDF学校范围。输出[audit.json](audit.json)。检查通过；主模型及Phoenix城市毕业界未修改。

## Digital-academy subtraction follow-up

The existing official FY2025 response for Phoenix Digital Academy (entity875776) reports cohort485, graduates286, and thus199 non-graduates. The same FY maps to cohort2024. This is an exact All row, not a reconstruction from suppressed demographic cells.

If a complete historical roster established that this academy accounts for all district provision excluded from the physical-city target, and district/school statuses refer to compatible unique-person cohorts, set subtraction would give target graduate lower4813−286=4527 and non-graduate lower1472−199=1273. These are **unadmitted conditional arithmetic**, not measured city bounds.

The reused V42 NCES audit contains21 PXU schools (20 nonvirtual, one virtual), all within the current Phoenix boundary; the official2024–25 PXU profile describes23 schools. This count discrepancy and historical cohort membership remain unreconciled. Current school locations do not prove complete cohort-era coverage. The district aggregate also does not certify deduplication of the earlier city school responses. V14 city uncertainty therefore remains unchanged. The next evidence needed is a reconciled cohort-era district school list and explicit district/school cohort membership and transfer treatment.
