# V6 高中教育证据补充：Istanbul 与 Jakarta

访问日期2026-11-07。只补原25城中的缺失教育指标，不改变候选名单、权重或指标定义。两条观测均为真实高中阶段教育资源，不是成人教育程度、初中数据或学习成果。它们是有范围条件的学生/教师比，不是教育质量因果估计。

## Istanbul：原始PDF可离线提取

来源：土耳其教育部《National Education Statistics, Formal Education 2025/26》，2026年9月30日发布，表2.11，印刷页154–155、PDF第185–186页。

- 入口：https://sgb.meb.gov.tr/istatistik_2026/resmi_istatistik2.html
- 完整原PDF：https://sgb.meb.gov.tr/istatistik_2026/2526.pdf

提取TR100 Istanbul（省级行政范围），**普通高中 general upper-secondary、公立与私立**。同一表左、右跨页配对：普通高中总在校生612,016包含开放教育203,536，扣除后408,480；同表公立309,665＋私立98,815也等于408,480。对应教师公立17,573＋私立10,863＝28,436，计算PTR **14.3648895766**。

教师是永久与合同教师人数，未转换FTE。此记录排除开放教育、职业高中、Imam Hatip高中，不能称“所有高中项目”。不采用全高中984,758/58,463：前者混开放教育，且官方按学段公布的全高中生师比另有宗教高中教师兼计初中学生的说明，不能直接拿总数相除后称统一国际高中比。

`extract_education.py`校验PDF哈希，调用`pdftotext -layout`现场读取同表两页，断言分项和总数一致，输出`istanbul_source_rows.json`，没有从转述媒体取数。表1.17的普通高中教师总数也为28,436。地理范围是Istanbul TR100省级口径，不是假定所有其他来源城市边界已自动相同。

## Jakarta：官方PDF web读取，人工录入明确标记

来源：BPS DKI Jakarta《DKI Jakarta Province in Figures 2025》，表4.1.7，印刷页201–202，2024/25学年。

- 稳定发布入口：https://jakarta.bps.go.id/id/publication/2025/02/28/30874e042a98939928603ee5/provinsi-dki-jakarta-dalam-angka-2025.html
- 官方PDF下载地址记录于`jakarta_download_url.txt`和manifest。

全DKI六个行政市/县，教育部管理下普通高中SMA公私合计学生190,143，教师12,114，PTR **15.6961367013**。原表脚注明确教师数含校长；不包含境外学校。该指标不覆盖职业SMK、宗教MA；与Istanbul、Shanghai普通高中范围近似，但教师定义仍有差异，严格可比性情景应撤回本记录。

原始PDF通过web工具成功读取相关完整表格；本地直接下载连接超时，因此**没有声称已归档原PDF**。`jakarta_sma2024_web_transcription.csv`是人工从官方web PDF表格录入的2024/25分区数据，明确属于派生记录。脚本验证所有六区总和、公私总和与出版物总数一致；这能发现录入加总错误，但不替代原始PDF校验。manifest区分原始下载、人工录入及下载失败。`observations.csv`状态包含`manual_source_scope_conditional`，便于主模型严格情景排除。

不要将其解释成Greater Jakarta/Jabodetabek区域，不要拿South Jakarta单区冒充全DKI。

## 查到但没有硬填的城市

- Toronto：Ontario Auditor General 2024官方审计Figure1确有2022/23 TDSB Grades9–12学生71,251、教师FTE4,464，但TDSB仅英语公立世俗教育，非Toronto所有教育部门（另有天主教、法语、公私机构）。本轮没有同口径完整城市分母，故只记录线索、不进入城市PTR。官方来源：https://www.auditor.on.ca/en/content/annualreports/arreports/en24/pa_TDSB_en24.pdf
- London：DfE School Workforce可得secondary比率，但通常包含11–18岁lower+upper secondary，不等于所需高中阶段教师分母。未直接取England全国16.7或London全secondary值填高中。官方来源：https://explore-education-statistics.service.gov.uk/find-statistics/school-workforce-in-england/2024
- Copenhagen：官方高中学生成果和在校生统计入口可定位，但本轮未配到相同机构/学段/年份教师分母，不填缺失。官方入口：https://uvm.dk/ministeriet/statistik/gymnasiale-uddannelser/

这些未入模线索不应被描述为新城市观测；亦未将学校班额当学生教师比。本轮不修改三城已有真实学生通学数据。

## 复现

从仓库根目录：

```sh
python3 research/2026-a/data/task4_v6_education/extract_education.py
```

运行依赖Python标准库与现有系统`pdftotext`。原始成功文件及人工录入文件均有SHA256，脚本逐一验证。没有访问远程网络的必要。产生两条`observations.csv`与Istanbul同表行审计。额外`indonesia_sma_ratio.html`是曾调查的官方2023指标入口，不是本次2024/25数值的来源。
