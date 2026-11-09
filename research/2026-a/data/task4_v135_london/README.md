# V135：London官方地铁库存候选

**59个候选站／枢纽实体通过原生记录、城市边界及只读数值复核，尚未正式准入。** 当前V130主模型、V131扩展和文档修订V134均保持。不是全市全部模式清单、实时运营数或个人／青少年可达性统计。

## 原始层级与保守选取

TfL原始`StopPoint/Mode/tube`返回1751个对象（page1/pageSize=total=1751），其中272为NaptanMetroStation；其余包括571站台、490入口、272地铁access area、77rail access area、69换乘对象。不能把1751行当实体站数。原生类型枚举另从官方StopPoint/Meta/StopTypes取回；筛站级对象、tube模式、有线路关联及严格Zone=1，得到62个站ID，未把Zone1+2或其他票区加入。

按原生hubNaptanCode（没有则stationNaptan）合并：Paddington的PAC／PAH同属HUBPAD，算一次。另保守省去Monument（Bank/Monument可能连通复合体的防重复预防）和Edgware Road Bakerloo（同名防重复预防，不断言两Edgware站本为同一付费复合体）。保留60个站ID，合并为59个operator站／枢纽实体。遗漏只使库存更保守；这个实体约定不声称识别任意定义下的全部物理建筑。

## 地理核对

使用ONS December2025 England Regions full-resolution coastline-clipped BFC层，筛RGN25CD=E12000007、名称London，outSR=EPSG4326。完整原GeoJSON含12个polygon片；全部60个保留坐标用独立ray-crossing与matplotlib Path（包括holes规则）核对在该London区域内。原表London人口9,122,909／2025保持，不另验证或修改人口，密度是条件混合时点值。

先尝试的BSC200m简化／岸线裁剪层保留为未使用原件。Thames岸线也会成为图层边缘，不能把到这种边缘的距离当作到城市行政外界的距离。最终换用BFC全分辨率；最小近似岸边／多边形边缘距离约40.2m只作诊断，不是行政外界距离、坐标准确度或置信下界。没有以“所有Zone1都在城市”的假设代替polygon检查。图层归属ONS及Ordnance Survey相关权利，保留原layer元数据与官方来源URL。

## 原件、复算与实际效应

16,228,439字节TfL原响应保存在仓库外`/data/datasets/HiMCM/source_archives/task4_v135_london/tube_stops_response_original.json`；retrievals.json记录URL、状态、日期、哈希和外置路径。完整响应另以399,962字节lossless gzip放进Git，解压后与16,228,439字节原响应SHA相同；station_entities.json仍明确是派生字段投影、不是伪装原始API。ONS单区域GeoJSON和层／类型原件保留在本包。所有日期为本次访问，未声称每个API对象最后更新于2026。

```sh
python research/2026-a/data/task4_v135_london/extract.py
.venv-v120/bin/python research/2026-a/data/task4_v135_london/audit.py
```

extract优先读仓库外原件，缺失时直接解压仓库内gzip，均验证同一原始SHA；重取URL返回若有变化，不能覆盖当前捕获或当作相同版本。核原件页数／对象类型、逐ID定位、去重、实体选择和几何。audit使用另一几何算法，并用独立加权向量范数核候选影响，同时检查当前主快照与旧新扩展各55文件保护。source站点是静态发布库存，有线路关联不等于当天开放；不从status布尔值推断实时服务，也不将线路数、出口或平台数另加。

候选59站给每10万人至少0.64672354个、效用[0.012769306569299622,1]。只读预评估：fixed平均宽度16.092069666942→16.089333559066（收窄0.017003%），equal18.919371949112→18.914257170686（0.027035%）；London仍14，Zurich保守及16可能／0必要保持。**本轮实际主准入0格**，这些是候选条件计算，未冒称已激活改善。

下一步在明确operator实体约定及外置原件可复现基础上做正式准入／撤回、主计算MC和全部扩展／论文迁移。未知上界仍1，保护已有144格信息，原用户CSV／权重／人口不变；失败或来源资格不成立就跳过。
