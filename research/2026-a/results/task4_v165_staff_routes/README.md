# V165：调查覆盖与公开数据覆盖的区别

本轮取得8份新原响应，核清Zurich与Dublin三条师资路线。Zurich的州级教学工作量已从官方图表追溯到原始API；Dublin两个官方API的变量结构已逐项核对。均未取得同城市、同学段、同提供者范围的教师分母，因此0格入模，固定权重平均评分宽度保持16.061435141，等权保持18.860967022。Zurich仍为保守推荐，16可能／0必要冠军。

## Zurich：全量调查不等于每张公开图表都覆盖全量

[州教育部门SSP调查说明](https://www.zh.ch/de/bildung/bildungssystem/studien-in-der-bildung/lehrpersonen-und-schulpersonal.html)将学校所在地作为范围，调查对象包括公私立学校，每年9月15日采集。[公开高中师资页面](https://www.zh.ch/de/bildung/bildungssystem/zahlen-fakten/entwicklung-des-schulpersonals-an-mittelschulen-und-berufsfachschulen.html)及其数据元信息则明确限定公共资助学校。二者描述不同层次：调查总体与本张图的发布子集。

页面的图表片段指向Observable模块，模块的uri与官方basicapi客户端共同确定[原始数据端点](https://www.bista.zh.ch/basicapi/zhweb/p_entwicklung_der_anzahl_vollzeiteinheiten_an_mittelschulen_und_berufsfachschulen?refreshcache=false)。20行数据只有Schuljahr、Schultyp、Vollzeiteinheiten三个字段，覆盖2016/17—2025/26两类学校。Mittelschule教学VZE在2024/25为1759.942307910003，2025/26为1774.584821416001；原始精度保留，解读约为1759.9与1774.6。这里一VZE表示100%工作量，不能换成教师人数。元信息明确FMS、HMS、IMS纳入Mittelschule，统计日为9月15日。

已取得的表没有城市／学校或独立Sekundarstufe II选择器，也没有证明公共资助子集覆盖全部私立学校。故它既不能替代市级高中教学FTE点值，也未建立T_city≤T_published。州范围大于市范围，并不能单独解决提供者子集问题。API的statusDate单独记录，未作观测年或经核实的发布日期。未将学年、当前抓取时间或日历2025基线混同，也未计算错范围比率。

六原件及URL／UTC／状态／字节／SHA见data/task4_v165_zurich_staff；远程JS只作文本核对，没有执行。extract.py核来源链及20行观测，observations.csv保持原值。

## Dublin：先核变量，再考虑组合分子与分母

并行研究核得[Eurostat urb_ceduc原响应](https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/urb_ceduc?lang=EN&cities=IE001C)的Dublin标签为greater city，返回14项教育指标，未包含教师分母；未把其边界视为Dublin City市政府边界。[CSO WMI07原响应](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/WMI07/JSON-stat/2.0/en)只有Statistic、Year、Sex、Country四维，教师统计项分Primary与Secondary，地理为国家／地区及汇总类别（41项，含EU27汇总），无Dublin城市、提供者或独立高中阶段维度。地理已不匹配，无需猜测教师项是否FTE即可拒收。

两原JSON与本次抓取记录、离线提取和范围审计见data/task4_v165_dublin_routes。结论针对本轮实际检查的两表，不宣称所有官方来源都缺少该数据；不重试已否定的ETB分配额上界或错学年学生配对。

## 前后对照与保护核验

scripts/task4_v165_staff_routes_audit.py独立解页面属性、模块uri、API路径及返回维度，并将当前工厂产生的160格效用界与冻结V154输出比较。固定／等权共32城市案例的得分、遗憾、推荐名次与冠军标记保持，浮点比较容差3e-13。comparison.json保存前后宽度；0准入、0实际收窄。没有重新抽样MC、增加模型或生成新PDF。

187个科学快照文件、491个已有Overleaf文件保持。当前科学V154、当前自有审阅稿V164（25页用户mcmthesis格式）不变；只同步新增的独立来源核对材料。无连接文档会话，未验证服务器编译或更改在线Main设置。队友main/ref/class及全部旧稿保持。公开GitHub推送仍待既有用户选择；长期goal active。

后续跳过将SSP全量调查说明自动套给公开公共资助图表的路线，优先带城市／学校、学段及提供者范围的实际教学工作量表。只有新增证据改变可识别集合时才扩展主评分或MC。

离线复现（仓库根目录）：

```bash
python3 research/2026-a/data/task4_v165_zurich_staff/extract.py
python3 research/2026-a/data/task4_v165_dublin_routes/extract.py
.venv-v120/bin/python research/2026-a/scripts/task4_v165_staff_routes_audit.py
```

fetch.py仅记录原始抓取方式，已有原件时拒绝覆盖；新抓取应另建版本目录。
