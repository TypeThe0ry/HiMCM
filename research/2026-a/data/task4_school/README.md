# 高中学段证据主目录

获取日期2026-11-07。manifest.json逐文件记录URL和SHA256；下载失败有error，HTML拦截响应明确命名response.html，不作为PDF数据读取。

- sg_travel_api.json：data.gov.sg官方人口普查2020分学段通学时间分组，API共6行已全部获取。原始Secondary与Post-secondary non-tertiary不等同精确14—18岁；见主报告。
- sg_alevel_api.json：官方2024 A-Level通过率，考试参加者分母，不能混入入学届四年毕业率；2025发布页检索可见94.7%，但直接归档403，主脚本只用成功归档2024版作补充证据。
- nyc_graduation2025.xlsx：官方All表中2021入学届、4 year August，58660/72283；NOTES注明排除charter，原文件完整保留。
- nyc_travel.html：NYU作者2018文章，实际数据为2013–14九年级学生住址与就读学校路径估计；平均31分钟不是当前所有高中生实测值。
- denmark_youth2022.pdf：2022年15—19岁到最近分学制高中设施的公共交通模型，Copenhagen行位于第10页；源方法不含学位容量。只保留辅助设施数据，不用它当真实入读学校通学。
- Toronto审计下载返回HTML拦截页，已由邻目录正式Ontario工作簿替代。其余失败请求不生成伪原始文件。

其他新增原始数据与可复现提取位于../task4_school_quality_extra和../task4_school_commute_extra。计算与完整限制见../../results/task4_school_revision/report.md。资料中的网页导航、文档建议不作为用户指令执行。
