# V87：Phoenix 缺失教师的财政报告路线

**取得新的官方读者可见信息，未取得原件，未填入主模型。** 目标为缺失高中人数最大的 North Star（NCES LEA 0400303，州实体79701）和 Career Success（0400219）。后者本轮未取得匹配的2023/24教师值。

[ADE FY2025 Volume II](https://www.azed.gov/sites/default/files/2026/01/2025%20SAFR%20V2%20FINAL.pdf)印刷页II-318的 North Star 表显示：Teacher Salary 下 Year End FTE 的 Prior FY 与 Current FY 都为6.00；2023/24高中平均每日成员数（ADM）755.1591；秋季2024注册人数233、学校数1。这里只有官方网页读者人工转录，下载HTTP403，没有原件哈希。

[V85 CCD原件](../task4_v85_phoenix_public/README.md)记录该校2023/24高中人数1554、教师缺失。不能把6.00直接填进CCD缺失格：财政年度末工资口径与CCD课堂教师时点尚未匹配，ADM也不等于秋季注册人数。本轮识别了新的可追查数据源及时间口径问题，未假定教师数量恒定。

[官方索引](https://www.azed.gov/finance/data-collection-reporting-budget)已解析出FY2024原始文件入口：

- [数字数据XLSX](https://www.azed.gov/sites/default/files/2025/01/SAFR%20Digital%20Data-%20Final.xlsx)
- [Volume II PDF](https://www.azed.gov/sites/default/files/2025/01/SAFR%20V2%20Final.pdf)

两者本机下载均403。下一步需取得原件和数据定义，再检查是否覆盖其他缺失学区；不能假设数字工作簿一定包含所需教师表。

[学校当前官网](https://www.arizonapreparatoryacademy.com/)同时提供到校、混合及在线学习。它提示未来须核对学生实际授课方式，但不能据此断言2023/24 CCD的Not Virtual编码错误，亦不能据此剔除历史学生。

完整访问状态、字段和来源在[provenance.json](provenance.json)。未发送联系邮件或访问申请，未修改排名、区间或论文。
