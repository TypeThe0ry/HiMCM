# Bogotá EM2021下载入口核查

新增定位官方SDP原始[SPSS ZIP](https://www.sdp.gov.co/sites/default/files/encuestas-multiproposito/em2021_sav_0.zip)，来源为哥伦比亚科技部学术库所收论文的明确数据引用。本地GET连接超时，没有取得原始字节。

官方[主CSV资源元数据](https://datosabiertos.bogota.gov.co/en/dataset/encuesta-multiproposito-2021-sdp/resource/b3fd892e-b9f9-4f34-ac22-6cc50612eac9)已可读：大小1254896789字节，CC BY4.0，Datastore active=False。因此不能把附加变量资源的活跃datastore状态套到主调查CSV，暂不具备通过CKAN SQL直接筛选学生的依据。

此记录仅保存下一步取数入口及访问结果，不提供观测或排名更新。完整访问记录见access_audit.json。
