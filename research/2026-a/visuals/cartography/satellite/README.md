# 卫星影像与城市可达性的地理对应

四城使用 NASA GIBS 提供的 **HLS S30 Sentinel-2 地表反射率 RGB 浏览影像**，与城市可达性图采用完全相同的 EPSG:3857 地理范围。海岸、湖泊、河口和建成区形态可直接与人口网格和道路图对读。

[四城卫星图 PDF](07_satellite_city_context.pdf) · [PNG](07_satellite_city_context.png) · [SVG](07_satellite_city_context.svg)

| 城市 | 影像日期 | 在论证中的用途 |
|---|---|---|
| Copenhagen | 2024-06-27 | 辨识紧凑城市形态、海岸与港口位置 |
| Toronto | 2024-10-17 | 对照安大略湖岸、都市连片区与外围空间 |
| Dubai | 2024-09-04 | 对照沿海带状建成区、沙漠腹地与人工海岸 |
| Shanghai | 2025-04-07 | 对照长江口、河网与连续建成区 |

## 数据与尺度

HLS S30 源产品像元为 **30 m**；交付影像是 GIBS 服务器渲染的 **1200 × 1132 像素 RGB 图像**。输出像素大小随地图范围而变，`manifest.json` 另列每城图中心的地面米／输出像素。增大输出像素不会增加源数据的空间信息。

四幅图采用相同产品与制图语言；各城使用独立比例尺。选取地表可辨识的日期作为地理背景，日期直接标在各图标题中。选择依据是地表可见性、完整覆盖和与城市地图范围一致；影像中的局部云与薄霾保留原貌。

## 多源证据的分工

- **卫星 RGB**：支持城市形态、地表背景和水陆位置的视觉解释。
- **OpenStreetMap 道路／水系**：提供道路拓扑与地名定位的地理背景，见上级 `vector_data/`。
- **归档人口网格与 Learning POI 模型时间**：支持人口加权可达性与尾部不均衡结论，见上级 `city_map_audit.json`。
- **Natural Earth**：提供全球国界、城市图陆地与湖泊背景。

RGB 浏览图用于地理解释；光谱指数、土地覆盖面积和变化量应从带 QA 的原始反射率波段计算。当前四个日期承担空间对照，时间变化研究需统一观测窗口、云掩膜和季节条件。

## 制图与复核

- 全图最小字号 11 pt，城市和日期为 12.5 pt；适合独立整页或大幅图使用。缩印时按最终印刷尺寸检查字号。
- 原始返回文件位于 `imagery/`，不改变颜色、不做生成式填补。
- `manifest.json` 保存请求 URL、图层、日期、边界、投影、文件 SHA-256、覆盖比例及输出分辨率。
- `build_satellite.py` 可重新获取并绘制四城面板；已有原始影像时直接使用缓存。
- `candidate_manifest.json` 和 `hls_candidates.json` 保存候选查询；试选影像置于忽略上传的 `cache/`。

```bash
python build_satellite.py
```

依赖：requests、Pillow、numpy、matplotlib、pyproj。

## 官方来源

- [NASA HLS S30 产品说明：30 m 地表反射率](https://hls.gsfc.nasa.gov/products-description/s30/)
- [NASA GIBS 官方 WMS 接入说明](https://nasa-gibs.github.io/gibs-api-docs/access-basics/)
- [NASA GIBS 可视化产品与 RGB 渲染说明](https://nasa-gibs.github.io/gibs-api-docs/available-visualizations/)
- [NASA HLS 数据产品与 QA](https://hls.gsfc.nasa.gov/data-products/)

## 论文图注

**Satellite context of the four accessibility case studies.** NASA HLS S30 imagery shows urban form and water–land structure over the same geographical extents as the accessibility maps. Acquisition dates are shown above each panel; scale bars are city-specific. The source reflectance product has 30 m pixels, rendered here as RGB browse imagery through NASA GIBS.
