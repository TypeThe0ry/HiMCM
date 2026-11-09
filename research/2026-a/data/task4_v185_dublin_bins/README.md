# V185：Dublin历史居民工作旅时分布，独立保留范围

新取CSO F7068原JSON给出Dublin City在2011年的六个旅时分箱、未报告人数和27.1分钟均值。原2011 Census Profile10表6（PDF物理43／印刷42页）逐项确认八个计数，已渲染实看：总计215384人，报告时长199103人、未报告16281人。对象为15岁以上在职、非主要在家工作、普查夜通常居住且实际在场者，按居住县／市分类。

它不是保留的Eurostat28.8分钟所对应人群已被验证的分布，也不是高中学生通学。Dublin City与当前greater-city标签不能自动相等。EC2012《Cities in Europe: The new OECD-EC definition》图5（物理6页）列历史greater-city代码IE001K1，但未提供其与IE001C、Dublin City或四县聚合的已核边界转换。四县分箱总量517800与原报告Dublin合计一致；四个已发布均值27.1、28.5、32.1、28.6经过舍入，不能凭加权接近28.8就建立人群同一性。

本包0主模型准入、0基线收窄，原CSV、权重与论文保持。父任务可将该居民工作人群作为**单独标明范围的历史替代情景**，不得与28.8直接取交、替换原均值或称当前高中分布。独立分箱效用计算须保留未报告质量及90分钟以上开放尾，不把27.1额外强加为全215384人的均值。

`dublin_city2011_duration_bins.csv`与`cso2011_dublin_four_counties.json`为派生提取；四份HTTP200原件、URL／访问UTC／SHA见`retrievals.json`。`verify.py`离线核响应身份、JSON-stat轴解码、计数和原2011表格。六次限定查询见`searches.json`，未重复下载Eurostat数值接口或2004手册。

原件：[CSO F7068](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/F7068/JSON-stat/2.0/en)、[2011普查原报告](https://www.cso.ie/en/media/csoie/census/documents/census2011profile10/Profile_10_Full_Document.pdf)、[EC2012定义](https://ec.europa.eu/regional_policy/sources/focus/2012_01_city.pdf)。完整原件仅在研究仓库，未复制到Overleaf。
