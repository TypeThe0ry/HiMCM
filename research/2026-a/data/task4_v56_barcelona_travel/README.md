# Barcelona：EMEF 2024实际就学旅时及学段核查

新取得官方EMEF 2024查看器的旅时和人口分组原始页面，以及第二轮问卷PDF原件。Barcelona居民的“Estudis”旅程公布平均28分钟、平均距离4.7公里。这是16岁及以上居民、所有就学类型的每旅程均值，不是当前14—18岁高中生的单向通学分布。

问卷P01只设通用“Estudiant”身份；S04明确询问“ESTUDIS FINALITZATS”，即已完成学历。不能将其二级教育类别误作当前高中在读。公开人口分析的年龄组为16—29等，未提供Barcelona×14—18岁×当前高中阶段的旅时联合结果。该调查总体也不覆盖14—15岁受访者。

因此，不把28分钟代入Barcelona的高中生效用，不使用`exp(-28/30)`冒充学生平均效用；原通学缺失区间保持不变。本轮走的是新的EMEF旅时路线，没有重复FRESC已核查的方式表。即使以后取得微数据，仍须验证当前学段或保留成员资格未知，并区分旅程均值与学生人口指标。

## 原件与复现

- [官方查看器](https://emef.institutmetropoli.cat/visor-EMEF-beta/index.html)
- [旅时章节](https://emef.institutmetropoli.cat/visor-EMEF-beta/chapters/11_durada_distancia_mitjana.html)：Table12的Barcelona表直接公布28分钟。
- [人口分组章节](https://emef.institutmetropoli.cat/visor-EMEF-beta/chapters/12_mobilitat_segons_segments_poblacio.html)：年龄及已完成学历分组。
- [官方问卷](https://www.omc.cat/documents/662112/2083735/Questionari_EMEF24_2aonada.pdf/83c1dbc5-9431-4556-6d0b-c9223e9a2a70?t=1745403900250)：422453字节原始PDF，含实际旅程分钟字段和身份/学历问题。

大HTML包含查看器图表资源，以gzip无损保存；manifest同时记录压缩文件及解压原始响应的字节数和SHA256。其他HTML与PDF原字节保留。原始PDF由方法页列出的官方www.omc.cat链接成功下载，未将失败的ca.atm.cat响应保存为原件。

`python3 research/2026-a/data/task4_v56_barcelona_travel/audit.py`使用BeautifulSoup与pdftotext离线核验原件、唯一Barcelona表、就学行数值、已完成学历问题和年龄分组。输出[audit.json](audit.json)；验证通过。未改模型、未申请数据、未发送消息给外部机构。
