# V135：London真实地铁库存候选及可复现原件

本轮找到可核原件，现行V130／V131及文档V134仍不改，0正式准入。[源包与复现](../../research/2026-a/data/task4_v135_london/README.md)记录59个候选operator站／hub实体、原生记录／边界／独立数值审查。原CSV、144个已有信息格、旧新扩展各55份及论文保护。

TfL StopPoint/Mode/tube原始响应1751条mixed对象：272 NaptanMetroStation，其余为站台、入口、access area和换乘等，不能直接计1751。严格站级／tube／有线路／Zone=1得62 ID；省Monument及Edgware Road Bakerloo作保守防重复处理，Paddington两原ID按官方HUBPAD合一，60保留ID形成59实体。未把票区1+2、其他模式或平台另加。该计数约定为operator station/hub库存子集，不冒称全部物理建筑／实时开放／个人可达性。

ONS2025 London region E12000007 BFC全分辨率coastline-clipped原GeoJSON，12 polygon片、EPSG4326；全部60坐标经ray-crossing与matplotlib Path独立核。先取BSC200m简化层发现Thames岸线裁剪会令图层边缘靠近中心站，故未以距这种边缘作行政外界距或准确度保证，最终改全分辨率。原城市人口9122909／2025不外验不更改；库存为本次2026访问的静态发布列表，未声称各对象更新时刻或2025同年普查。

16,228,439字节完整TfL原响应在datasets，同时lossless gzip399,962字节入Git，解压SHA与原响应匹配；已用不存在的外置输入路径实际测试fallback复算通过。完整原件可由研究仓库恢复，派生station_entities明确不是原API。原始请求URL／status／日期／hash、类型枚举、ONS两层metadata／单区几何均保留；仅必要候选及回执复制Overleaf，非整棵研究树。

只读条件计算：效用[.012769306569299622,1]，fixed平均宽度16.092069666942→16.089333559066（0.017003%），equal18.919371949112→18.914257170686（0.027035%）；London仍14、Zurich保守／16可能／0必要保持。效应小，价值主要为覆盖，不能称已激活改善或缩小冠军范围。

Overleaf支持材料提交bbfbee6及lossless回执后续c46162f已授权push；主稿／数值图表／PDF保持。研究正常本地commit，新增公开push仍待原GitHub PUBLIC发布选择。新中英文说明按指定技能，长期goal active。

下一步在上述operator实体约定、城市范围及原件可复现条件下做正式受控准入／撤回／24组主MC，固定已有数据与规则；再重跑全部扩展并统一当前独立稿后激活。源包还未由正式准入表冻结，采用时固定所有所需哈希；不修改旧V130／V131／文档V134证据。控制号、全队AI史、队友具体整合与正式提交回执仍需实际事实。
