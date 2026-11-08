# V127：Vienna具名地铁站区下界

已核实 **99个市内既有地铁站区**：2026-11-08版本的运营方DIVA站区，与StadtWien官方既有地铁站GeoJSON逐项交叉，所有代表点均在官方Vienna行政多边形内。沿用附件2025人口2,028,399和交通锚点50，候选效用为 **[0.08893284626879548, 1]**。这是当前登记的设施供给子集；其他模式、运营方及未覆盖记录不计，上界保留1，不能推断各家庭／高中生的实际可达性。

## 原件与资格核对

原HTTP响应、URL、文件哈希及访问日见`retrievals.json`；`version.csv`记录`2026-11-08T17:50:01+01:00`，2026-11-09为新加坡访问日期。`ogd_schema.pdf`为2022年V1.3文档，其第4页把DIVA定义为多处停车位置的站区分组；2026是数据导出版本，不是schema发表年。`stop_positions.csv`与`route_patterns.csv`把线路映到停车位置，再映到DIVA。`stop_areas.csv`使用具名站区，不能把位置、平台、重复路线或出入口各计一个站。

`vienna_boundary.geojson`来自StadtWien官方`LANDESGRENZEOGD`，EPSG:4326，行政代码90001，边界记录日期2026-09-01；运营方`MunicipalityID=49000001`不是同一个编码制。脚本同时要求运营方`Wien`标签与点在市界内，不由代码字面相等推断市域。`review_source_ubahn_stations_original.geojson`来自独立的官方**既有**`UBAHNHALTOGD`层；同一能力表另有规划层，规划站没有使用。

99个DIVA逐项匹配99个既有站，换乘只一次。按线路相加24／21／21／20／24共110次，不能当110个复合体。拼写标点规范化及明确别名保留在`review.json`完整crosswalk和父级脚本；两个来源代表点距离最大约301m，并非入口定位精度。Hauptbahnhof还由位置名SüdtirolerPlatz交叉支撑。现有站层及StadtWien启用新闻支持Lina-Loos-Platz为2026已启用乘客站；网络图／运营方新闻取得的是挑战HTML，按`failed_response`归档，没有伪存成PDF或声称看过原PDF。

## 被拒收的更大计数

- `data.wien.gv.at/csv/`的另一路原CSV HTTP Last-Modified为2024-12-06，保存为`rejected_stale_stop_areas.csv`作来源版本对照，未假定为2026版。HTTP更新时间也不被重写成实测统计年份。
- 广义metro／tram／city-bus route patterns关联1722个DIVA；地理筛选1703个，8对同名合并后1695。独立审查发现其中有车厂／车库对象，pattern文件还包括未证明是乘客服务的运行与dummy位置。**1695不准入**，也没有简单删几个关键词后把其余强当公众站点。
- 最终只计经独立既有乘客地铁层确认的99个具名站区。原始大清单仅用于拒收诊断，不给当前评分制造1695个公共站点的下界。

`review.json`独立核验99项、地理、原件和别名；`extract.py`可离线复算两个来源、99名单及效用，生成`audit.json`、`vienna_stop_area_subset.csv`和候选`observations.json`。本包提供2026静态登记资料配原2025人口，不声称统一2025普查、访问时刻所有车站持续运行、零票价、资格无限制或精确通学时长。原CSV、已有区间、权重和模型锚点保持。

```bash
.venv-v120/bin/python research/2026-a/data/task4_v127_vienna_transport/extract.py
```

数据署名：Wiener Linien；Datenquelle: Stadt Wien – data.wien.gv.at。Exa文本表示单独保存在`provider_capture.json`，实际数值从另存原CSV／GeoJSON计算；该工具表示不冒充原件。候选需经父级准入表与完整受控复算后才进入主模型。
