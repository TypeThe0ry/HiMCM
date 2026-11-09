# V184：Dublin28.8分钟找到官方同值记录，城市／人群范围保持区分

Eurostat原始JSON中，`urb_ctran`、`TT1019V`、`IE001C`、2011年给出28.8分钟，与原表Dublin通勤均值／年份相同。指标名称为平均工作旅程时间；当前官方地理标签为 **Dublin (greater city)**，不等于原表的city proper。这个同值记录加强了来源线索，但不证明原表实际抄录链或2011具体边界相同，不据此重写原值或范围。

2004版官方Urban Audit方法手册（物理47页／印刷46页）将一般工作旅程定义为居住地至工作地的最短旅程，包括换乘；工作地在指定边界内，居住地可在边界外甚至跨境。该页已渲染核读。历史通用定义不替代2011爱尔兰具体实施、人群、地理对应和学生学段证明。

原API的17个指标没有年龄或旅时分箱维度。未取得与保留测量匹配的高中实际单程分布，因此0准入、0评分变化；保留原28.8分钟／2011／STALE、Jensen规则及现有区间。当前科学V181、自有稿V182保持。

两个HTTP200原件、请求／UTC／长度／SHA见`retrievals.json`；维度解码和范围判断见`findings.json`及`verification.json`。查询限定六次、两条路线；CSO定向查询未恢复额外匹配原件。未修改论文或注册表。

原API：[Eurostat Dublin2011交通表](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/urb_ctran?lang=EN&cities=IE001C&time=2011)。方法原件：[Urban Audit2004手册](https://ec.europa.eu/eurostat/documents/3859598/5885077/KS-BD-04-002-EN.PDF.pdf/c1a47e5c-5adb-44a4-bf79-e0165a952de5?t=1414781121000)。原件保存完整字节，未将手册年份冒充观测年或用同值匹配宣称完全验证用户来源。
