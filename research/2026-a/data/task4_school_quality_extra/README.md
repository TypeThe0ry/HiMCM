# 高中教育结果：新增原始证据

取得日期：2026-11-07。仅教育结果证据，不将毕业率称为教学因果效果或国际统一学业水平。

## Toronto：可进入明确限定对象的情景

Ontario Ministry of Education 官方目录：
https://data.ontario.ca/dataset/school-board-achievements-and-progress

通过公开 CKAN API 取得目录及原始 XLSX，URL与哈希分别见 `ontario_source.json`、`manifest.json`。目录说明毕业数据来自 OnSIS 2023–2024，目录更新时间2026-06-01；不要把后者当观察年份。

`ontario_board2026.xlsx` 第1表 O1 定义为 **Four Year Graduation Rate 2020-2021 Grade 9 Cohort**。

| 教育局 | Excel单元格 | 四年毕业率 | 五年毕业率（不同入学届） |
|---|---|---:|---:|
| Toronto DSB | O64 | 81.8% | 87.4% |
| Toronto CDSB | O63 | 88.4% | 91.5% |

这是2020–2021年进入Grade 9、截至2023–2024学年的四年毕业结果。`extract_quality.py` 离线直接读取源单元格，生成 `toronto_extracted.csv/json`，断言表头与教育局身份。

两个英语公费教育局的入学届人数权重没有同时提供，因此不得简单平均。若目标明确限制为这两个教育局的学生，混合率在两局端点之间；再采用四舍五入到0.1个百分点的分析假设，可取 `[0.8175, 0.8845]`。四舍五入规则未在目录明确给出，因此端点扩展是保守分析约定，不是置信区间。**该区间不能覆盖整个多伦多所有学校**：法语教育局、私校及跨市就读未全面匹配；若拒绝样本范围向目标群体的迁移，城市教育维度仍应未知。

比此前审计报告中2022–2023年、取整的TDSB 81%更近期也更精细，但不是同一届学生的重复测量，不能直接解释为改进幅度。

## Melbourne：真实高中学业数据，暂不合并跨城率

VCAA 发布页：
https://www.vcaa.vic.edu.au/administration/school-administration/performance-senior-secondary/senior-secondary-completion-and-achievement-information

已下载 `vcaa2025.xlsx`，包含2025年高中VCE、VCE VM、VPC项目和学校结果；原表指出数据截至2025-12-06，后续学校更正窗口至2026-02。该表可进一步用于高中学校分布分析。

本轮**不把学校结果汇总成 Melbourne 城市四年毕业率**：

- VCE完成资格分母与纽约/多伦多Grade 9入学届四年毕业分母不同。
- 学校所在地不等于学生居住城市；未完成都市边界和所有学校的映射。
- 原表第4行明确提醒不能从SSCAI推导全州数据，第6行存在小样本抑制（<4、I/D）；简单把校数或总入读数当毕业分母会失真。
- 某所名校的100%不能替代整座城市。

2024 XLSX与参考指南的直接下载返回403，已记入manifest；2025原表可正常验证ZIP文件签名。

## 未纳入的检索

- 丹麦官方可按高中部门查询完成/中止学生，但本轮尚未取得可与Grade 9入学届对应的Copenhagen全市四年率；全国STx率不代替城市值。
- Arizona官方2025四年毕业XLSX存在，但下载返回403；没有将搜索结果或Phoenix Union教育局冒充整个Phoenix市。
- 未用日本/澳大利亚/丹麦的全国PISA替代Tokyo/Melbourne/Copenhagen市值。

全部新增仅本目录；未修改手稿或提交git。
