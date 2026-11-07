# Phoenix 2024凶杀记录与新增国家面板审计

官方Phoenix一页UCR年度表的Murder and Non-Negligent Manslaughter行合计138，按月和按季度均核对一致。总Criminal Homicide146包含8例negligence，本指标采用138。UCR按每位受害者计一项，区别于多受害者共一案件的计数。

分母取美国人口普查局2025年5月发布的Vintage2024 Phoenix行政市2024年人口1,673,164。城市范围相配，计算138/1,673,164×100000=8.24785/10万人。此处冻结年度发布版本；后续修订总量和人口vintage变化应作为明确新版本更新，不混合进原表。

来源：
- https://www.phoenix.gov/content/dam/phoenix/policesite/documents/crime-stats-and-maps/UCR2024_YTD.pdf
- https://www.census.gov/newsroom/press-releases/2025/vintage-2024-popest.html 表2、3
- https://ucr.fbi.gov/additional-ucr-publications/ucr_handbook.pdf

原PDF可经web工具解析，但本地直接请求403；原始请求失败保存在manifest，结构化人工核验记录标记manual_primary_web_pdf_and_census_html，没有假称拥有原PDF。strict新增归档情景撤回该条。警方报告覆盖作为城市报告口径条件，数字不是未报案件的总体普查。

工作区新增`../country_year_homicide_education/`包含国家年份凶杀与中学师生比。已读取summary，国家面板适合背景分析；城市指标不能用全国均值补齐，且SE.SEC.ENRL.TC.ZS含高中以外学段。本轮不改动或复制该外部任务数据，也不将其填入Phoenix或Istanbul城市缺口。
