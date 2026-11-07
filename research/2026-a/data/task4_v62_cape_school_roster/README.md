# Cape Town官方学校名录与缺失计数

取得南非基础教育部[EMIS下载页](https://www.education.gov.za/EMIS/EMISDownloads/tabid/466/Default.aspx)“Quarter 3 of 2025 / Western Cape”原始工作簿。页首ECD标题不能代表文件范围：实际工作簿含普通、特殊及其他学校，1935行，列名明确Learners2025与Educators2025。

以LMunName= CITY OF CAPE TOWN且Status=OPEN筛得1093校，NatEmis唯一。248所公立SECONDARY SCHOOL记录学生275384、教师9254；27所独立SECONDARY SCHOOL已报告学生6056、教师425，但其中4校缺学生计数、3校缺教师计数。COMBINED SCHOOL也可能含高中；学校phase无法单独识别当前10—12年级及教师分配。

这些是原表全校计数，不能将275384/9254当作高中阶段师生比。缺失学校的人数不设为零，分组CSV的reported_*_sum只加总非空字段，须与missing_*列共同阅读。本轮模型单元更新0、原有Cape Town实际学生通学界保留。名录提供下一步按NatEmis匹配年级数据及补缺学校的依据；完整性、教师计数定义及普查参考日仍需核验。

[原件](western_cape_q3_2025.xlsx) · [来源哈希](manifest.json) · [分组计数](city_phase_counts.csv) · [缺失学校](missing_count_schools.csv) · [审计摘要](audit.json)。执行 `python3 research/2026-a/data/task4_v62_cape_school_roster/extract.py` 验证哈希、按单元格位置读取，核验城市学校ID唯一并重建统计。
