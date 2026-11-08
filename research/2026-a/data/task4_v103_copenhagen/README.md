# Copenhagen：取得真实学生调查，市级通学区间保持未知

本轮找到并保存两份此前未使用的学生出行调查原件。核验结果支持继续寻找市级旅时分组，**本轮不改变Copenhagen的通学区间[0,1]**。

| 原件 | 实际测量与人群 | 市级准入判断 |
| --- | --- | --- |
| [CeFU/Aalborg大学2025报告](eud.pdf) | 2024年3—4月，1732名25岁以下GF2职业教育学生报告从住所到学校的通常旅时；PDF85页、正文80页图6.1给出五档分钟 | 全国学校调查，公开表没有Copenhagen市居民交叉结果；年龄含19—24岁，不能直接用于14—18岁城市指标 |
| [Rysensteen高中调查报告](rysensteen.pdf) | 2010年2月学生问卷、2011年出版；PDF34页、正文33页为从家到学校的通常交通方式 | 图表为步行、自行车、公交/火车、接送方式，未给旅时；单校历史方式比例不能变成当前城市分钟 |

CeFU五档为小于5、5—15、16—30、31—60、大于60分钟，图示分别4%、18%、29%、33%、17%，舍入后合计101%，原样保留。方法部分PDF36—38页说明年龄、样本与调查时段：首都大区占样本8.1%，且部分学校跨多个大区，连学校所在大区都不能对所有受访者精确分配。报告提到向参与学校提供专门结果，但该公开报告未提供能定位Copenhagen居民的旅时微观记录；研究机构位于Copenhagen并不等于样本来自该市。

另核对两个新线索：

- [MOVE 2024高中出行调查](https://move-interreg.eu/nyheder-og-kommunikation/nyheder/unge-blev-inddraget-med-croissanter-og-workshops/)覆盖Herning、Silkeborg、Viby三校1864人，地理范围不包括Copenhagen。
- [UVM 2026/27招生分配旅时表](https://uvm.dk/media/g0tb3rh0/260512-oversigt-over-transporttider-for-elevfordelingen-til-skoleaaret-2026-27.pdf)列学校招生分配阈值；它衡量招生算法计算的路程条件，不是学生实际通学分布，不能拿Rysensteen的11分钟当全校或全市均值。

已先读V41 TU公开界面权限审计和V62教育源说明，没有重试合作方登录或以首都大区替代市级数据。下一步需要带14—18岁/高中在读、Copenhagen居住地、通常住所到学校旅时及样本权重的公开交叉表，或可界定目标覆盖份额的真实校级旅时资料。

## 复核

运行`python3 research/2026-a/data/task4_v103_copenhagen/audit.py`。两个原始PDF的SHA-256、样本与图表字段核验通过；两张原图已目视检查。`manifest.json`保存URL与下载校验，`summary.json`区分真实测量、地理与年龄限制，`audit.json`记录0格准入。未改模型、registry或论文。
