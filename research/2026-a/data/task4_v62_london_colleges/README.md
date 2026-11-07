# London：补入FE院校教师原始记录，尚不构成城市高中人数界

取得DfE最新发布的2024/25 Further Education Workforce provider原始CSV（60360行），覆盖原School Workforce Census不包含的一部分六年级学院及16–19机构。以UKPRN与Ofsted2025年7月院校位置原始CSV一对一匹配后，得到9家登记在London、类型为Sixth Form College或School Based Providers的机构。

这些机构报告的Teacher主角色人数合计667，详见[london_provider_matches.csv](london_provider_matches.csv)。例如Leyton141、Sir George Monoux87、St Charles62、St Dominic54、St Francis Xavier60、Woodhouse78。此数是机构报告计数的算术和，不是去重后的全城高中教师人数。

新来源使后续可以按UKPRN核对FE院校，补上旧校级学校工作簿之外的数据渠道。但总部位置不保证所有教学场所在London，机构类型不保证全部教师服务当前高中阶段，尚未取得同快照、同范围的学生分母。主模型London教育区间保持[0,1]，main_admitted=false。

## 关键口径

[DfE数据说明](https://explore-education-statistics.service.gov.uk/data-catalogue/data-set/d9ddcd0e-903d-4653-b5c9-0bb7554af129)明确机构位置按ILR总部记录；0既可能表示无人，也可能表示未完整填报。[官方方法](https://explore-education-statistics.service.gov.uk/methodology/further-education-workforce)说明仅按人员主角色发布，不能把缺失副角色当作不存在。

[Ofsted位置原表](https://www.gov.uk/csv-preview/6893474af97cd7adaa2be039/Management_information_-_further_education_and_skills_-_as_at_31_July_2025.csv)提供UKPRN、URN、地方当局和地区。这里仅定位已匹配机构；不把其被检查机构集合当作完整城市学校名册。名称未用于推断地理或学段。

尝试核验GIAS机构130443、148421及141030的年龄范围，直接请求均403；未据此填入年龄或学生人数。未使用第三方学校目录的年龄字段。

## 复现

`python3 research/2026-a/data/task4_v62_london_colleges/extract.py`

脚本验证4份原件哈希和字节数，筛定年份、主角色和Total合同类型（避免与Permanent and fixed term行重复相加），核对UKPRN唯一与9家真实记录。原件、来源URL及获取时间见[manifest.json](manifest.json)，准入条件见[audit.json](audit.json)。未改动模型、历史资料或论文。
