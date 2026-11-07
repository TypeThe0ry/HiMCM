# London：九家院校同学年学生与教师记录已匹配

取得DfE2025/26发布中的2024/25全年under19参与数据，按UKPRN与V62的九家London院校教师记录准确匹配。531条居住地交叉行中，education-and-training参与计数按机构加总为14249，其中London居住地计数13780；对应Teacher主角色计数667。每家机构的参与计数与另一份官方按十位公布的摘要相差不超过5。

这补上了V62尚缺的同学年机构学生记录。两项资料都覆盖2024/25学年：教师方法明确为学年内有雇佣合同的人员，学生为全年参与者。因此不能再简单描述为两套不同学年的数据；同时，它们也不是同日学校在校人数快照。

## 已识别范围与未识别范围

- under19是年龄分类，未给当前高中学段，不能自动等同14—18岁高中生。
- 教师只按主角色计数；其服务的年龄、课程学段及副角色尚未分配。
- 每人每机构计一次，跨机构仍可能重复；14249与667均为机构计数的和，不是全London去重人数。
- 机构总部位于London的条件沿用V62；学生居住地与学习地点分别记录，13780不用于替换机构分母。
- 这是发展中的统计，官方以透明性用途发布。未把其他字段的low/z转成零。

因此本轮新增可匹配原始计数，主模型London高中教育区间仍保留[0,1]；main_admitted=false。不用14249/667冒充城市高中师生比。

## 原件与复现

[官方发布页](https://explore-education-statistics.service.gov.uk/find-statistics/further-education-and-skills/2025-26/explore)的Supporting files提供“FE and skills provider participation by provision type and learner characteristic”及“Under 19 learner participation by provision type”。两份原始CSV分别52.3MB和58.8MB，按字节无损gzip保存；[manifest](manifest.json)同时记录原始和压缩字节哈希，避免上传超限单文件。附元数据PDF和发布HTML原件。

教师原件沿用[V62](../task4_v62_london_colleges/README.md)，引用哈希见[reuse_manifest](reuse_manifest.json)。执行 `python3 research/2026-a/data/task4_v63_london_students/extract.py`，核验所有哈希、九个UKPRN、531个不重复地理组合及摘要交叉检查。

[配对表](matched_provider_counts.csv) · [匹配的原始参与行](matched_under19_source_rows.csv) · [审计](audit.json) · [元数据原件](metadata.pdf)。没有更改模型、历史文件或论文。
