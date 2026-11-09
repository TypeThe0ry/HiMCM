# V180：Amsterdam市府原始站组表形成32个Metro候选子集

已取得市府地图后端原始GeoJSON，补上V129只有页面／配置、没有实体表的缺口。元数据与原表均为239个按短步行距离合并的上车点：200 Tram、39 Metro。39个Metro原生ID、名称和坐标各自唯一；两版市界都将其中35个名义点归在Amsterdam，四个外市点剔除。另剔除距任一边界不足100米的三个点，得到32个候选站组；这是保守数据子集，尚未正式准入主模型。

## 原件、对象和年份

[retrievals.json](retrievals.json)保存九个HTTP200原响应的URL、GET／POST参数、UTC访问时间、长度和SHA。市府[数据目录](https://maps.amsterdam.nl/open_geodata/)的元数据ID649明确原表TRAMMETRO_PUNTEN_2026，数据实际性标2026，精确观测日未给出；[地图说明](https://maps.amsterdam.nl/trammetro/)明确近距离站牌合并为一个上车点，且不含临时改道、不是当前实际路线图。本包计数为已发布的Metro代表点／站组，不是站台数、班次数、完整公交网络或高中生个人可达性，也不能改标2025观测。

市界为市府ID541、March2026的INDELING_GEMEENTE，与CBS/PDOK2025非概化GM0363 MultiPolygon。两个发布版本的点面筛选结果一致，不代表独立定位误差保证。GeoJSON坐标为经纬度顺序；离线PROJ9.7.1的cs2cs从OGC:CRS84转EPSG:28992米制坐标，处理所有外环与孔洞，工具不下载网格。

四个外市点：178 Station Duivendrecht、191 Van der Madeweg、192 Verrijn Stuartweg、213 Station Diemen-Zuid。边界邻近剔除如下：

| 原生ID | 站组 | 距市府2026边界／米 | 距CBS2025边界／米 |
| --- | --- | ---: | ---: |
| 164 | Overamstel | 12.28 | 12.29 |
| 174 | Strandvliet | 78.39 | 78.72 |
| 196 | Venserpolder | 88.50 | 88.54 |

100米是分析者声明的筛选尺度，不是提供方定位误差界；本包没有证明所有入口／站台都在市界内、全部点位误差小于100米或持续运营。保留完整39点分类和距离见[mapped_metro_groups.csv](mapped_metro_groups.csv)，[extraction.json](extraction.json)明确候选32、名义35、排除ID、转换工具及限定。35仅作无边界缓冲的诊断，不用于主候选数。

## 再分发说明与署名

**Municipal data:** Gemeente Amsterdam, Maps Data. The original datasets are freely available to everyone from the municipality under the [Maps Data terms](https://maps.amsterdam.nl/open_geodata/terms.php), which also apply to redistributed original or modified datasets. Archived terms: [maps_terms_original.html](maps_terms_original.html). Attribution is appreciated rather than legally mandatory under these terms; we cite the source under our research standards. This derived selection is not endorsed by the municipality. No municipal logo or official endorsement is claimed. 市府资料不是CC BY。

**Boundary data:** CBS/PDOK, Gebiedsindelingen2025, gemeente_niet_gegeneraliseerd GM0363, [CC BY4.0](https://creativecommons.org/licenses/by/4.0/). 服务能力及许可原件见[pdok_capabilities_original.xml](pdok_capabilities_original.xml)。由经纬度进行的投影、筛选和派生表属于本研究处理，非官方新增统计。

复现`extract.py`只读取本包原件并写派生CSV／JSON，不修改模型。模型预评估及独立审计见[候选结果](../../results/task4_v180_amsterdam_candidate/README.md)。当前仍科学V154、论文V179；后续须完成准入、扩展及稿件迁移才能启用新值。
