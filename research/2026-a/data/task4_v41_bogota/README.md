# Bogotá EODH2023：新增官方合同附件线索，尚未取得微数据

本轮没有可准入的高中生通学观测。官方目录列有2023年家庭、人员、旅程和阶段数据，但当前下载页面分别返回403、502或空响应，未取得这些模块的原始记录；通学效用保持[0,1]。

新定位[SECOP官方合同2022-1972](https://community.secop.gov.co/Public/Tendering/ContractDetailView/Index?AwardContractDetailId=2675496&IsFromContractNotice=True&IsFromMarketplace=False&UniqueIdentifier=CO1.PCCNTR.4232446)，合同明确覆盖2023年Bogotá及周边地区EODH/EODI。搜索索引列出附件`Etapa Publicacion datos SIMUR.txt`以及调查实地工作ZIP，可作为后续官方取数路径。合同页首次网页读取成功，后续读取及本地GET均403，尚未获得附件内容，不把附件名视为已下载数据。

核查[Observatorio2023目录](https://observatorio.movilidadbogota.gov.co/publicaciones/resultados/encuesta-de-movilidad-2023)和[SIMUR目录](https://www.simur.gov.co/index.php/encuestas-de-movilidad)的访问结果见`access_audit.json`。GitHub研究仓库`anyoalmanza-cmd/Bogota-mobility-analysis`根目录仅见两个notebook及README，未取得原始调查数据。

**口径分开保留：** V11保存EODH2019，教育字段是最高教育程度；V33核验的是另一项调查EM2021的当前Media及通学分钟变量。不能将EM2021变量代码用于EODH2023，也不能把2019教育程度直接当作当前高中在读。

取得实际2023记录后，还需逐项确认当前高中就读、Bogotá家庭居住地域、从家到校旅程、时长特殊码及缺失、家庭/人员扩张权重和聚类抽样结构。没有用年龄、全年龄均值或旅程权重替代这些定义。未修改模型、论文或提交。
