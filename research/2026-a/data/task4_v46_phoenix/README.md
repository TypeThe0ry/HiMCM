# Phoenix：核验人数图表的数据调用，日期与项目覆盖仍未公开

本轮直接检查ADE官方Report Cards前端及Hope学校页。前端`enrollment`组件调用`/api/DataApi/Student Enrollment`，传递`reportSection`、当前选择的`fiscalYear`和学校`educationOrganizationId`，将`All`组的`total`显示为人数。没有在前端将人数按月份累加，也没有提供October 1、全年去重或现场／在线项目范围的说明。不能据此认定后端人数是某一种统计量。

这确认V42保存的1,178人确实来自学校人数图表使用的API，未解决其与NCES2024–25 October 1人数是否兼容的问题。学校页出现的October 1文字位于每生支出解释，不能移作Enrollment图表定义。人数图表的小样本匿名规则也不是人数口径说明。

另经网页PDF文本阅读核对ADE2026年《Quick Guide: Enrollment Data》：它把学校Report Cards图表和Accountability & Research的Enrollment工作簿列为两个公开查数入口；没有说明FY2025数据快照、去重或Hope项目覆盖。直接PDF下载失败，保存的是明确标注的[网页提取记录](quick_guide_web_extract.json)，不是伪装成原始PDF的文件。

[manifest.json](manifest.json)保存实际取得的三个官方网页／JS原件及SHA256；[audit.json](audit.json)保留调用代码片段和准入判断。未重复请求已受阻的October 1工作簿、县会议字幕或被抑制的NCES人数。没有新城市数值，缺失界与论文保持不变。
