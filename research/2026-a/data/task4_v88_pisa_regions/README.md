# V88：Santiago真实高中测评与PISA地域识别审计

取得智利官方 **SIMCE 2024 Segundo medio** 原始数据包。Santiago commune（代码13101）官方公布阅读均值 **256**、数学均值 **264**；学校文件包含该commune的64条学校记录。它补充了高中阶段实际学习成果，但SIMCE与PISA没有共同校准，不能把两种分数直接合并排名。

## Santiago：原件、人数与数据质量

官方公共门户的搜索接口返回715155字节的`Simce 2do medio 2024.rar`。该只读搜索由门户前端公开调用，无账号或申请；原始响应保存在[chile_public_search_2024.json](chile_public_search_2024.json)，下载来源与哈希在[simce_source.json](simce_source.json)。[RAR原件](simce_2medio_2024.rar)、原始学校CSV、commune CSV及[字段词典](simce2m2024_GLOSAS_web_final.xlsx)均保留原字节。

| 项目 | 阅读 | 数学 |
| --- | ---: | ---: |
| 官方commune公布均值 | 256 | 264 |
| 64校报告参加考试人数 | 6366 | 6440 |
| 63校无非代表性标记的参加人数 | 6319 | 6369 |
| RBD8499标记2的参加人数 | 47 | 71 |
| 按参加人数加权的已四舍五入学校均值（仅核对） | 256.209 | 264.273 |

所有64条均为2024年2m，`noaplica=0`，人数与均值非缺失。**RBD8499仍报告数值均值，但marca=2**；词典明确解释为因机构以外原因，结果不代表学生表现。只检查非缺失会漏掉这一质量问题。

RBD8759有阅读8人、数学9人参加，但三个能力等级百分比全为0。没有将这些0解释为真实达标比例，也没有自行构造全commune等级分布。`nalu`是参加人数，不是学校在读人数或居民队列分母；等级百分比的具体分母与这些人数未在本包确认。

官方commune均值直接取自原表；学校加权值只作核对，因为公布的学校均值已经取整，且官方汇总纳入规则尚未完全确认。没有对整数均值编造统计置信区间。学校地域是Santiago单一commune，不是整个Santiago都市圈，考试阶段也不是全部14—18岁居民。

文件名包含`final`，但内部`codigo_bbdd=preliminar20240422v1`、`fecha_bbdd=20250422`。本包保留这项版本差异，不自行认定已完全消除初步版本问题。

[派生学校子集](santiago_school_subset.csv) · [commune原行](santiago_commune_row.csv) · [计算摘要](santiago_summary.json) · [派生哈希](derived_manifest.json)

复算：

```sh
python3 research/2026-a/data/task4_v88_pisa_regions/extract_simce.py
```

独立代理用原始CSV和词典复核64个唯一学校ID、两科人数、质量标记和加权核对结果。

## 其余20城的PISA公开地域字段审计

复用经V86哈希验证的官方613744行学生SAV，对其余20个候选城市对应国家的实际`REGION`、`STRATUM`、`SUBNATIO`取值及官方标签逐项归档：

- 7个候选城市对应国家在该2022发布文件中没有记录：Nairobi、Lagos、Cape Town、Mumbai、Delhi、Dhaka、Shanghai。Hong Kong/Macao记录不代表Shanghai。
- 其余13城有所在国家记录，但这三个公开字段不能给出所需城市对应。Mexico为全国、学校学段/部门/规模；Brazil为大区；Ontario、Victoria、Cataluña不能分别替代Toronto、Melbourne、Barcelona；Greece城市化类别不标识Athens。

[20城结果](candidate_audit.csv) · [实际代码标签与记录数](observed_code_labels.json) · [来源与审计范围](summary.json)。这是对指定公开字段的结论，不证明受限文件或其他国内数据永远不存在城市链接；没有根据匿名学校ID猜真实学校。

复算需要`pyreadstat`和仓库外保存的原始SAV：

```sh
/tmp/task4_pisa_venv/bin/python research/2026-a/data/task4_v88_pisa_regions/audit.py /tmp/task4_pisa_extract/CY08MSP_STU_QQQ.SAV
```

新增可直接进入同尺度PISA城市比较的城市数为0。Santiago SIMCE结果作为独立真实教育证据保留，主模型与缺失区间不改。
