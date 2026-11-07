# London四校缺失：确认一所转制，不能自动拼接教师数

官方GIAS索引确认London Nautical旧学校URN100642于2024-12-31因转为学院关闭，继任学校URN150889于2025-01-01开放。前后地址相同，并有明确predecessor/successor链接。GIAS中的关联登记日期为2024年6/7月，不应误作实际开关校日期。

已有November2024教师工作簿确实包含100642：教师人数42、FTE39.16；January2025学生表使用新URN150889，Year12/13学生181人。这解释一项直接URN缺失，但两次快照之间教师人数是否保持不变仍未知。

**直接匹配基准仍为407校、105274人，4校772人未知，不自动改为408校。** 若另做“转制前后教师数连续”情景，可将181人对应前身42名全学段教师，但必须明确该额外假设，不能称新增2025教师观测，也不能把全学段人数当高中专属分母。

另外3校Ark Globe Academy(135584)、Alec Reed Academy(134369)、Gumley House(137928)的官方开校日期分别为2008-09-01、2003-09-01、2012-03-01；本轮没有找到与2024-11至2025-01对应的编号转换。已查到的Ark Globe与Gumley旧前身不在当前工作簿中，不能靠名称或历史关联修复为观察值。

## 来源与复现

GIAS直接HTML访问403；以下内容来自官方页面的搜索索引读取，`gias_index_transcription.json`明确标记人工事实转录，未冒称归档网页原件。`access.json`记录本地访问失败。

- [旧London Nautical](https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/100642)
- [新London Nautical](https://www.get-information-schools.service.gov.uk/Establishments/Establishment/Details/150889)
- [Ark Globe](https://www.get-information-schools.service.gov.uk/Establishments/Establishment/Details/135584)
- [Alec Reed](https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/134369)
- [Gumley House](https://get-information-schools.service.gov.uk/Establishments/Establishment/Details/137928)

`extract.py`校验原工作簿SHA256、November2024表头、单工作表结构、URN唯一性、4个当前URN确实缺失，并提取100642的真实教师行及核对当前学生181人。输出`predecessor_row.json`。本目录不修改任何主模型区间。
