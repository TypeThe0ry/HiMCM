# 真实矢量底图数据

取得日期：2026-11-07。目的：四座城市的指定出图范围；不依赖CARTO密钥或OSM栅格瓦片离线下载。

## 文件

- `copenhagen.json`、`toronto.json`、`dubai.json`、`shanghai.json`：Overpass原生JSON。每条`elements`为way，`geometry`是按次序排列的`{lat, lon}`坐标，`tags`含道路等级等属性。
- 对应`.overpassql`：实际请求语句；full与detail边界由上一级`map_viewports.json`从EPSG:3857反投影得到。
- `ne_10m_land/ne_10m_land.shp`、`ne_10m_lakes/ne_10m_lakes.shp`及配套文件：Natural Earth 1:10m陆地与湖泊。原始ZIP保留。
- `manifest.json`：来源URL、请求文件、SHA256、OSM底库时间戳、要素数量及查询边界。
- `fetch_vector.py`：可复现下载脚本；已有文件复用。本次四城均由`https://overpass-api.de/api/interpreter`成功返回。

## 覆盖与边界

主图范围取得motorway/trunk/primary/secondary及其link；水系取得river/canal线，海岸为coastline线。detail范围额外取tertiary/residential及其link。没有查询全部建筑、全部道路或学校点位；这些底图线也不是求得可达性时采用的路网快照。

OSM查询以way相交边界选取，完整way可能越出画面，渲染必须在设定视口裁切。住宅街道只覆盖detail框，不能暗示其他区域没有支路。闭合道路不应当水体填色。Natural Earth水体是独立的概化地理数据，不是OSM返回的全部海岸/内水。

取得的OSM时间为2026-11-07，现有学习设施可达性来自另一个归档快照，二者用途不同：新OSM线仅作地理参照，不能声称重新使用2026路网计算了通学可达性。

署名：**© OpenStreetMap contributors**；OSM数据为ODbL。Natural Earth数据为公共领域，建议署名 **Made with Natural Earth**。

## 检查

四城响应均无`remark`、非空，且每个way都有geometry；已记录SHA256。查询得到：Copenhagen 10,344，Toronto 74,806，Dubai 33,299，Shanghai 68,359条way。这些是线要素分段数，不是独立道路或公交线路条数。

## GitHub source archives

The four raw Overpass JSON responses are stored as lossless .json.gz files in Git. Decompressed bytes match the SHA-256 hashes in manifest.json. The city renderer reads either representation. Query files and retrieval metadata are included.
