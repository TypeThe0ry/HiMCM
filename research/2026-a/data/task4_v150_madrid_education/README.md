# V150：Madrid市级教师计数候选与分层核对

新取得官方市级Bachillerato教师计数的20列历史资料：年末标签2005–2024，对应2004/05–2023/24学年。最后一列原标记“2024 (P)”保留；Madrid市计数1008，Comunidad总计1922。**这仍不是已核实的城市高中教学FTE或师生比，0项准入，Madrid的PTR效用仍[0,1]。**

## 来源与实际取得的材料

- [市级序列1902424](https://gestiona.comunidad.madrid/desvan/AccionDatosTemaMunicipal.icm?codTema=1902424)：单位Número，含区域总计、11统计分区和179市镇。它不同于V129已查的ESO/Bachillerato合并序列1902423。表尾明确按两年学年的最后一年标记，故2024不是2024/25，更不是2025年测量。P只作为原表标记保存。
- [官方2025报告入口](https://www.comunidad.madrid/educacion/informe-sistema-educativo-comunidad-madrid)链接的B章新版本URL见provider_request_manifest。报告的实际学年为2023/24，区分专教Bachillerato教师计数1922与其他教学类别；其12.6师生比则覆盖整个Comunidad的Régimen General，并注明部分工作量转全时当量。这不是Madrid市上阶段师生比。
- 保存的是Exa返回的官方HTML／PDF提取表示，完整序列化响应见provider_capture.json；**不是原HTML／PDF字节**。直接HTTP的5条资源请求及1条新版本PDF请求超时，均无已保存原件；另一次CSV provider请求返回CRAWL_TIMEOUT。所有路径与失败记录保留，不把检索片段或错误当下载成功，也不因此断言适配数据不存在。
- PDF表示有乱码与图表行序问题。本轮只用其可读叙述确定范围与单位，没有从乱码表格准入数值，也未声称看过原PDF版面。市级序列来自独立的HTML表格表示。

## 可重复的数据处理

provider_request_manifest记录工具、两个确切URL、maxCharacters=500000、已保存响应字节／哈希和归档时间；不虚构原站HTTP200。provider_capture.json全文含244641字符，报告用定位偏移及段落SHA保存核对线索，原始表示在研究目录。

表的三个层级重复描述同一地域总体。20年逐年满足：区域总计=11分区之和=179市镇之和；市镇Madrid行与分区Municipio de Madrid行也逐年一致。2023/24若把全部层级平铺相加会得到5766，恰为1922的三倍，不能解释为更多教师。共3820个源计数单元经过列结构和汇总恒等式核查；这不等于独立验证每个原测量。欧洲千位分隔点在计数列转为整数，未当小数。

candidate_city_teacher_counts.csv仅保留Madrid及各层级校验，20行均标记FTE_identified=False、primary_model_admitted=False，不加入179座城市到主分析。extract.py按行／层级提取，独立audit_task4_v150_madrid_education.py按年头索引与分段重新汇总。复现时从研究仓库用现有`.venv-v120/bin/python`分别运行`research/2026-a/data/task4_v150_madrid_education/extract.py`和`research/2026-a/scripts/audit_task4_v150_madrid_education.py`。

## 准入决定与当前结论

Número没有建立教学FTE；Bachillerato计数也没有恢复保留指标所需的全部上阶段／职业教育分配与匹配学生总体。报告1922与区域表数值吻合，不能单凭吻合就认定两个序列的专教学段定义完全相同。区域全Régimen-General比值12.6同时存在地理与学段错配。没有假设每人1 FTE、没有由计数反造PTR、没有把历史序列外推为未来趋势。下一步须取得匹配城市／学段／provider的实际教学FTE及学生分母。

139科学文件、82稿件文件与原CSV保持，主仍V13616城×10指标／112点33部分15全未知，扩展V137，论文文档V148。0新准入／0得分区间收窄；Zurich保守、16可能／0必要保持。原排名按冻结结果核验，不重跑未受影响的MC。Overleaf仅接收精简范围、候选序列与核对回执，原始provider表示留研究；当前V149交付对照仍对应同一未改PDF。
