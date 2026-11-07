# Mumbai：取得官方高等中学分类统计，年级口径待核对

已从Konkan政府[年报目录](https://divcomkonkan.gov.in/en/document-category/annual-reports/)取得Mumbai City及Mumbai Suburban《District Social and Economic Review 2025》原件。表8.3参考年均为2024–25，父agent与独立agent目视核对表头及总计。

| 报告区 | 学校 | 教师 | 男学生 | 女学生 | PDF页／印刷页 |
| --- | ---: | ---: | ---: | ---: | --- |
| Mumbai City | 50 | 1074 | 27671 | 29854 | 118／108 |
| Mumbai Suburban | 116 | 3767 | 104436 | 102262 | 104／94 |

标题是地区“高等中学信息”，字段为学校数、教师数、在册学生男女数。表内没有明确11–12年级筛选、混合学段教师分配、教师人数/FTE定义，也没有注明只含纯高等中学。因此既不把它断言为全部高中年级统计，也不擅自认定仅含纯高中学校。

郊区表脚注明确数据来自UDISE，按教育division而非taluka列示；City表来源为南部教育监察处。要合并为城市指标，还需核验学校类别与年级映射、教师口径，以及南/西/北教育分区与候选城市边界。比率高低本身不构成拒绝理由，当前阻碍是统计范围尚未确立。

`extract.py`校验原件哈希及PDF文本中完整总计行，保存各报告区的真实学校分类统计。派生分类比率仅描述原表，未合并成Mumbai城市高中PTR。主模型教育格仍为[0,1]。

早期Statistical Abstract网址证书主机名不匹配，未绕过验证。改用官方Konkan目录链接的政府CDN成功取得本包原件；Python本机证书链失败后改用正常验证的curl下载。原始字节与访问日期见`manifest.json`。
