# Jakarta SMA与SMK：取得2025/26原始统计书

两份官方原始PDF确认同一2025年11月30日Dapodik截面，并可分开校长、induk教师及noninduk教师任教关系。此前SMA索引转录的186461名学生、11983名校长及教师得到原件核验。

| 类型 | 学生 | 校长及induk教师 | 校长 | induk教师 | noninduk教师任教关系 |
| --- | ---: | ---: | ---: | ---: | ---: |
| SMA普通高中 | 186461 | 11983 | 453 | 11530 | 1188 |
| SMK职业高中 | 194178 | 11519 | 525 | 10994 | 1621 |

学校数分别510和553，均包括公私校。SMA学生/教职摘要为PDF第23/26页（印刷4/7页），校长第105页（86页），教师分类第121页（102页）；SMK对应PDF第25/28/115/131页（印刷4/7/94/110页）。表1.10.1明确后续教师表只采用induk教师。两类合计学生380639、induk教师22524、校长978；若延续含校长口径，分母23502。Induk保留原语标记为主要行政归属计数；英文表将其译为permanent，不能因此解读为FTE或具体授课小时。

新增SMK是扩大高中项目覆盖；去除校长则是另一项分母口径修订，应分别比较。两本书不自动覆盖宗教部MA/MAK、特殊教育或等同教育；网页分类标签SMA/MA、SMK/MAK不是这些人群已经纳入表内的证明。也不能把学生/教师人数比称为学习成果。

来源为[官方SMA出版页](https://data.kemendikdasmen.go.id/publikasi/p/buku-statistik/statistik-sekolah-menengah-atas-sma-tahun-2025-2026-2026-sma-ma-sederajat)和[官方SMK出版页](https://data.kemendikdasmen.go.id/publikasi/p/buku-statistik/statistik-sekolah-menengah-kejuruan-smk-tahun-2025-2026-2026-smk-mak-sederajat)，页面给出2026年4月8日发布日期及PDF链接，原页面HTML及PDF字节已保存。SMK原件58444921字节，gzip仍超过50MB，故按原字节分成3个part文件；按manifest顺序拼接即可恢复原PDF，重组SHA256在manifest中。没有重新编码或降低图像质量。

运行`python3 research/2026-a/data/task4_v58_jakarta_education/extract.py`可离线校验所有原件与分片哈希、重组SMK并抽取表格，验证induk+校长等于摘要分母。`observation.json`保存具体页码和计数。额外[induk归属规则核查](induk_rule_audit.json)明确标为官方索引文本，原网页403，未伪装为已取得原件。本目录不修改主模型或论文。
