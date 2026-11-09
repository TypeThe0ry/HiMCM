# V147：新版教育统计的师资口径核查

两份新版官方出版物均提供了可复核数值，但所检查表页没有建立城市高中师生比的匹配分母。本轮新增准入为0，V136原数据与V137扩展保持。新版资料按各行实际年份记录，不把封面年份当测量年份。

| 城市 | 新检查的官方资料 | 原表发现 | 决策 |
| --- | --- | --- | --- |
| Zurich | [2025/2026学校统计](https://www.zh.ch/content/dam/zhweb/bilder-dokumente/themen/bildung/bildungssystem/zahlen/berichte/die_schulen_im_kanton_zuerich_2025_2026.pdf)，2026年7月出版；PDF15／印刷28–29页 | 2025年州公立Mittelschule教学聘任2812、教学FTE1771.6；右表教育部门Mittelschulen雇员年度FTE2227另有定义 | 不以州公立总量或部门雇员FTE替代城市全provider高中教学FTE；不与原城市学生表硬除 |
| Helsinki | [2025统计年鉴](https://www.hel.fi/static/kanslia/Kaupunkitieto/26_03_25_Helsingin_tilastollinen_vuosikirja_2025.pdf)，PDF158／印刷157页，表7.14–7.15 | 最新学生行为2024年：普通高中18661、职业教育47520；相邻表是2000–2021成人教育课时 | 课时不是高中教师FTE；没有可用匹配教师分母，不换算假设FTE、不构造师生比 |

这两份资料的版本分别更新了V124核查的旧教育年鉴。V147没有重复下载旧BISTA州级序列、旧2011Zurich年鉴或旧2024Helsinki年鉴。新版页的结论仅约束这些表，不证明其他来源不存在合适数据。Zurich原教学聘任表排除校长；右侧部门表为另一个雇员总体及会计年度工作量，不能因也使用FTE就混为一谈。1771.6/2812与表中四舍五入的63.0%相容，是表内单位核对，不是城市PTR。

`retrieval.json`记录2026-11-09三份HTTP200原响应的URL、时间、字节及SHA256，仅保留非敏感响应元数据。两完整PDF与Zurich出版说明HTML保持原字节；`*_extracted.txt`和`*_review.png`是指定页的派生提取与已实看的渲染。没有新制论文PDF。

复现：在研究仓库运行`.venv-v120/bin/python research/2026-a/data/task4_v147_education_refresh/extract.py`，再运行`.venv-v120/bin/python research/2026-a/scripts/audit_task4_v147_education.py`。提取器以layout文本核对页和数值；独立审计改用PDF词坐标按行和左右半页提取，防止把并排表列误拼。审计验证139份科学文件和82份现行／历史稿件文件，包括当前V146 PDF及原CSV，确认112点／33部分／15全未知、两目标师资格仍[0,1]。原排名按冻结哈希核验，没有重跑蒙特卡洛。

原件留GitHub研究工作区，Overleaf仅复制本轮scope、精简verification和来源记录作为独立支持材料；论文仍V146、24页。下一次需新取得匹配的城市／学校级教学FTE、学生分母、学段和provider范围，不能继续拿这两页的已知不匹配合计试填。
