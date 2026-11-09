# V175：Zurich州薪资统计区分全年教学工作量与统计时点FTE

新取得的[官方原PDF](payroll2024_original.pdf)补充了一条教学FTE来源路线：第5页2024年Mittelschule教学人员为1826全年VZE、职业学校为1340，均含Lehrbeauftragte。该表属于州政府就业系统；第3页明确VZE按1月1日至12月31日工作量折算，而任职关系数按12月31日计。两种时间口径不可互换。

第7页7301学校行政组2188.9全年VZE、3490份任职关系还混合其他岗位类别，不能直接取代教学分母。第3、5、7页已渲染实看，原始响应、HTTP状态、访问时间和SHA见[retrievals.json](retrievals.json)，逐项判断见[observations.json](observations.json)。[官方方法网页](https://www.zh.ch/de/finanzdirektion/personalamt/personal-und-lohnstatistik.html)另有[原响应](method_original.html)。

全年平均可与某个秋季时点有不同大小关系；现有报告未给出单侧误差或时点包络，也未证明市域全部公私提供者覆盖。因此本轮保留为来源记录，0准入、0区间收窄，不能与已有BFS私校年表直接拼成保证上界。下一步需要覆盖目标学校集合且时间匹配的教师存量或可证明包络；不重复用年度工作量代替统计时点。科学V154、原始用户值与权重保持。
