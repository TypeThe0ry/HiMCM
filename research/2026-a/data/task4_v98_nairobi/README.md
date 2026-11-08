# Nairobi：新取得两份官方原件，城市师生分母仍未识别

本轮取得 KNBS《2024 National School Census: Pilot Census Report》（205 页）和 NGEC《Teachers of Kenya: Status of Equality and Inclusion in the Teaching Workforce in Kenya, 2025》（41 页）完整原件。两份资料分别推进普查字段与近期师资范围的核查；新增模型准入观测为 0，Nairobi 教育区间保留 [0,1]。

KNBS 原件 PDF 第 10—11 页明确采用有目的选择的县和调查区。Nairobi 实际覆盖 Kibra subcounty 的 Kibra zone：139 所各阶段机构，其中 secondary 11 所、junior 31 所，不能相加当高中，也不能视为全城。报告附录为调查工具，不是已填写的学校数据。第 129—130 页的 SD01/SD03 询问 2023 年 Form 1—4 在校生及年龄；第 137 页 SF01 分 2023/2024、公私立、TSC/BoM/志愿者/实习等教师类别。后续应找这些字段的正式结果或公开微观数据，而非从空白问卷生成观测。

NGEC 原件第 16 页（印刷第 3 页，已渲染目视检查）限定 2025 年 6 月 TSC 雇员，排除私立、县政府及 BoM 雇员。第 33 页附录的 secondary 教师 128,960 是全国数；没有 Nairobi 分县行。该数不能与 Nairobi 学生相除。教师总数是雇员人数，未建立 FTE 换算。

此前 V35 的教育部 2020 年手册官方端点、本轮再次连接超时；Elimu Yetu DOCX 也连接超时，均未保存伪原件。本轮不声称解决 V61 的 2023 年学生／3 月教师时点配对。两份新文件及其字节数、SHA256、原始 URL 见 [manifest.json](manifest.json)。

复现：`python3 research/2026-a/data/task4_v98_nairobi/audit.py`。脚本核验原件、学校分阶段计数、附录字段及全国教师行，输出 [audit.json](audit.json)。地理与范围判断结合正文检查，不能仅凭关键词不存在判定。

来源：[KNBS 原始报告](https://www.knbs.or.ke/wp-content/uploads/2025/01/2024-National-School-Census-Pilot-Report.pdf)；[NGEC 原始报告](https://www.ngeckenya.org/img/downloads/TEACHERS%20OF%20KENYA.PDF)；[NGEC 发布页](https://www.ngeckenya.org/report/status-of-equality-and-inclusion-in-the-teaching-workforce-in-kenya-2025/234)。访问日期：2026-11-08。
