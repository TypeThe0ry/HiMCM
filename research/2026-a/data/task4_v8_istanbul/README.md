# Istanbul V8：高中生通学字段核验（没有新增准入值）

本包检验是否存在足以证明通学效用上界 < 0.3521967322 的真实证据。结果：本轮没有找到可准入的 Istanbul 全市高中生通学时间分布，原缺失区间 [0,1] 不变；阈值是待检验目标，绝不是反推数据的约束。

## OECD PISA 2022：两个独立缺口

原始 OECD 2024-06-27 版完整 codebook 已下载，SHA256 在 manifest.json。运行 `python3 audit_pisa.py` 可离线解析 XLSX（标准库，无 openpyxl），生成全部 1279 个学生文件变量标签与候选字段逐行审计。官方入口：https://www.oecd.org/en/data/datasets/pisa-2022-database.html 。

1. **结果字段不匹配**：ST265Q01JA 是上学路安全感；PA009Q04NA 是家长因路线不安全而难以参与学校活动；PA006Q01TA 是择校时距离近的重要性。它们均不是上学单程分钟数。ST342Q08JA 是旅行兴趣，数学题的 distance 是能力情境。公开学生代码簿候选字段未发现可用通学时间。
2. **地区无法验证**：学生文件 REGION 的 Türkiye 值为 79200，SUBNATIO 为 7920000，两者全国计数均 7250。STRATUM TUR01–36 是学校类型加 A/B/C 等标签，不含可验证的 Istanbul 映射。本包不根据字母猜省份，也不把抽样覆盖 Istanbul 等同于公开记录可识别 Istanbul。

上述判断针对归档的 2022 国际公开代码簿；不是宣称所有 PISA 年份、国家附加问卷或受限地理数据都不存在通学字段。没有下载大型学生微数据，因为已核验的公开字段不能支持目标识别。

官方主学生问卷印刷 p34 ST265 再次确认安全感题目：https://www.oecd.org/content/dam/oecd/en/data/datasets/pisa/pisa-2022-datasets/questionnaires/COMPUTER-BASED%20STUDENT%20questionnaire%20PISA%202022.pdf 。这一 PDF 由 web 工具核验，未归档为原始文件。

## 地方新线索

Yıldız 大学公开论文 https://dspace.yildiz.edu.tr/xmlui/bitstream/handle/1/12519/5792.pdf?isAllowed=y&sequence=1 确有四区上学时长分箱（印刷 p22–23），但样本为初中（ortaokul）学生；不是高中。全文另有样本 148 与部分分箱人数合计不一致，未据此估计城市值。这里只记录拒绝原因，不复制 V7 已拒绝的 2007 教育程度、Pendik 小学等线索。

## 下一步可检验的数据请求

需要同一份公开/授权数据同时提供：Istanbul 居住地或学校地域定义、在读高中阶段/年级、家庭到学校单程分钟或分箱、调查年、样本覆盖及权重。若分箱可得，按现有单调效用对每箱端点计算上下界，尾箱保留开放上端；不能用均值代替效用期望，不能为跨过 0.3521967322 改尾部假设。PISA 若有受限地区映射也仍须额外核验通学时间题目，当前两项缺口缺一不可。

`field_audit.json` / `student_variable_labels.csv` 为原 XLSX 自动提取；README 地方 PDF 结论为 web 核验记录，未声称已下载该 PDF。没有生成可准入 bounds 行。
